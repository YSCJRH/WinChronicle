using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Windows.Automation;
using AutomationControlType = System.Windows.Automation.ControlType;

const int MaxDepth = 80;
const int MaxNodes = 5000;
const int MaxTextChars = 20000;
return Run(args);

static int Run(string[] args)
{
    if (args.Length == 0 || args[0] != "capture-frontmost")
    {
        Console.Error.WriteLine("usage: win-uia-helper capture-frontmost [--depth 80]");
        return 2;
    }

    int depth = Math.Clamp(ParseDepth(args), 0, MaxDepth);
    IntPtr hwnd = NativeMethods.GetForegroundWindow();
    if (hwnd == IntPtr.Zero)
    {
        Console.Error.WriteLine("no foreground window");
        return 1;
    }

    try
    {
        CaptureOutput output = CaptureForeground(hwnd, depth);
        var options = new JsonSerializerOptions { WriteIndented = true };
        Console.WriteLine(JsonSerializer.Serialize(output.ToJson(), options));
        return 0;
    }
    catch (PrivacySkipException exc)
    {
        Console.Error.WriteLine($"capture skipped: {exc.Message}");
        return 0;
    }
    catch (Exception exc) when (exc is COMException or InvalidOperationException)
    {
        Console.Error.WriteLine($"uia capture failed: {exc.Message}");
        return 1;
    }
}

static int ParseDepth(string[] args)
{
    for (int index = 1; index < args.Length - 1; index++)
    {
        if (args[index] == "--depth" && int.TryParse(args[index + 1], out int depth))
        {
            return depth;
        }
    }

    return MaxDepth;
}

static CaptureOutput CaptureForeground(IntPtr hwnd, int depth)
{
    NativeMethods.GetWindowThreadProcessId(hwnd, out int pid);
    ProcessInfo process = ProcessInfo.FromPid(pid);
    AutomationElement root = AutomationElement.FromHandle(hwnd);
    string title = SafeString(root.Current.Name);
    string? denylistReason = PrivacyGate.DenylistReason(process.ProcessName, title);
    if (denylistReason is not null)
    {
        throw new PrivacySkipException(denylistReason);
    }

    ElementNode tree = TreeExtractor.Capture(root, depth, MaxNodes, MaxTextChars);
    ElementSnapshot focused = ElementSnapshot.FromElement(GetFocusedElement(), MaxTextChars);
    WindowRect rect = NativeMethods.GetWindowRect(hwnd, out WindowRect bounds) ? bounds : new WindowRect();
    string visibleText = TextCollector.VisibleText(tree, MaxTextChars);
    string? url = TextCollector.FirstUrl(tree);

    return new CaptureOutput(
        Timestamp: DateTimeOffset.Now.ToString("o"),
        Window: new WindowSnapshot(
            Hwnd: $"0x{hwnd.ToInt64():X16}",
            Pid: pid,
            ProcessName: process.ProcessName,
            ExePath: process.ExePath,
            AppName: process.AppName,
            Title: title,
            Bounds: new[] { rect.Left, rect.Top, rect.Right, rect.Bottom },
            Elevated: false),
        FocusedElement: focused,
        VisibleText: visibleText,
        Url: url,
        UiaTree: tree,
        Limits: new Limits(depth, MaxNodes, MaxTextChars, tree.NodeCount),
        Truncated: tree.Truncated);
}

static AutomationElement? GetFocusedElement()
{
    try
    {
        return AutomationElement.FocusedElement;
    }
    catch (InvalidOperationException)
    {
        return null;
    }
}

static string SafeString(string? value)
{
    return value ?? "";
}

static class TreeExtractor
{
    public static ElementNode Capture(AutomationElement root, int maxDepth, int maxNodes, int maxTextChars)
    {
        int nodeCount = 0;
        bool truncated = false;
        ElementNode node = CaptureNode(root, 0, maxDepth, maxNodes, maxTextChars, ref nodeCount, ref truncated);
        node.NodeCount = nodeCount;
        node.Truncated = truncated;
        return node;
    }

    private static ElementNode CaptureNode(
        AutomationElement element,
        int depth,
        int maxDepth,
        int maxNodes,
        int maxTextChars,
        ref int nodeCount,
        ref bool truncated)
    {
        nodeCount++;
        ElementSnapshot snapshot = ElementSnapshot.FromElement(element, maxTextChars);
        var children = new List<ElementNode>();

        if (depth < maxDepth && nodeCount < maxNodes)
        {
            AutomationElement? child = TreeWalker.ControlViewWalker.GetFirstChild(element);
            while (child is not null && nodeCount < maxNodes)
            {
                children.Add(CaptureNode(child, depth + 1, maxDepth, maxNodes, maxTextChars, ref nodeCount, ref truncated));
                child = TreeWalker.ControlViewWalker.GetNextSibling(child);
            }
        }

        if (depth >= maxDepth || nodeCount >= maxNodes)
        {
            truncated = true;
        }

        return new ElementNode(snapshot, children);
    }
}

static class TextCollector
{
    private static readonly Regex UrlPattern = new(@"https?://\S+", RegexOptions.Compiled | RegexOptions.IgnoreCase);

    public static string VisibleText(ElementNode root, int maxTextChars)
    {
        var parts = new List<string>();
        CollectText(root, parts, maxTextChars);
        return Truncate(string.Join("\n", parts.Where(part => !string.IsNullOrWhiteSpace(part)).Distinct()), maxTextChars);
    }

    public static string? FirstUrl(ElementNode root)
    {
        foreach (string value in root.FlattenText())
        {
            Match match = UrlPattern.Match(value);
            if (match.Success)
            {
                return match.Value;
            }
        }

        return null;
    }

    private static void CollectText(ElementNode node, List<string> parts, int maxTextChars)
    {
        if (parts.Sum(part => part.Length) >= maxTextChars)
        {
            return;
        }

        parts.AddRange(node.Snapshot.TextValues());
        foreach (ElementNode child in node.Children)
        {
            CollectText(child, parts, maxTextChars);
        }
    }

    public static string Truncate(string value, int maxTextChars)
    {
        return value.Length <= maxTextChars ? value : value[..maxTextChars];
    }
}

sealed record CaptureOutput(
    string Timestamp,
    WindowSnapshot Window,
    ElementSnapshot FocusedElement,
    string VisibleText,
    string? Url,
    ElementNode UiaTree,
    Limits Limits,
    bool Truncated)
{
    public Dictionary<string, object?> ToJson()
    {
        return new Dictionary<string, object?>
        {
            ["helper_schema_version"] = 1,
            ["source"] = "win-uia-helper",
            ["command"] = "capture-frontmost",
            ["timestamp"] = Timestamp,
            ["window"] = Window.ToJson(),
            ["focused_element"] = FocusedElement.ToJson(),
            ["visible_text"] = VisibleText,
            ["url"] = Url,
            ["uia_tree"] = UiaTree.ToJson(),
            ["limits"] = Limits.ToJson(),
            ["truncated"] = Truncated,
            ["capture_surfaces"] = new Dictionary<string, object?>
            {
                ["screenshots"] = false,
                ["ocr"] = false,
                ["audio"] = false,
                ["keyboard"] = false,
                ["clipboard"] = false,
                ["desktop_control"] = false,
            },
        };
    }
}

sealed record WindowSnapshot(
    string Hwnd,
    int Pid,
    string ProcessName,
    string ExePath,
    string AppName,
    string Title,
    int[] Bounds,
    bool Elevated)
{
    public Dictionary<string, object?> ToJson()
    {
        return new Dictionary<string, object?>
        {
            ["hwnd"] = Hwnd,
            ["pid"] = Pid,
            ["process_name"] = ProcessName,
            ["exe_path"] = ExePath,
            ["app_name"] = AppName,
            ["title"] = Title,
            ["bounds"] = Bounds,
            ["elevated"] = Elevated,
        };
    }
}

sealed record ElementSnapshot(
    string ControlType,
    string Name,
    string AutomationId,
    string ClassName,
    bool IsEditable,
    bool IsPassword,
    string? Value,
    string? Text)
{
    public static ElementSnapshot FromElement(AutomationElement? element, int maxTextChars)
    {
        if (element is null)
        {
            return new ElementSnapshot("", "", "", "", false, false, null, null);
        }

        bool isPassword = SafeBool(element, AutomationElement.IsPasswordProperty);
        string? value = isPassword ? Constants.RedactedPassword : TryValue(element, maxTextChars);
        string? text = isPassword ? Constants.RedactedPassword : TryText(element, maxTextChars);
        AutomationControlType controlType = SafeControlType(element);

        return new ElementSnapshot(
            ControlType: controlType.ProgrammaticName.Replace("ControlType.", ""),
            Name: SafeProperty<string>(element, AutomationElement.NameProperty) ?? "",
            AutomationId: SafeProperty<string>(element, AutomationElement.AutomationIdProperty) ?? "",
            ClassName: SafeProperty<string>(element, AutomationElement.ClassNameProperty) ?? "",
            IsEditable: SupportsPattern(element, ValuePattern.Pattern) || SupportsPattern(element, TextPattern.Pattern),
            IsPassword: isPassword,
            Value: value,
            Text: text);
    }

    public Dictionary<string, object?> ToJson()
    {
        return new Dictionary<string, object?>
        {
            ["control_type"] = ControlType,
            ["name"] = Name,
            ["automation_id"] = AutomationId,
            ["class_name"] = ClassName,
            ["is_editable"] = IsEditable,
            ["is_password"] = IsPassword,
            ["value"] = Value,
            ["text"] = Text,
        };
    }

    public IEnumerable<string> TextValues()
    {
        if (!string.IsNullOrWhiteSpace(Name))
        {
            yield return Name;
        }

        if (!string.IsNullOrWhiteSpace(Value))
        {
            yield return Value;
        }

        if (!string.IsNullOrWhiteSpace(Text))
        {
            yield return Text;
        }
    }

    private static bool SupportsPattern(AutomationElement element, AutomationPattern pattern)
    {
        return element.TryGetCurrentPattern(pattern, out _);
    }

    private static string? TryValue(AutomationElement element, int maxTextChars)
    {
        if (element.TryGetCurrentPattern(ValuePattern.Pattern, out object pattern)
            && pattern is ValuePattern valuePattern)
        {
            return TextCollector.Truncate(valuePattern.Current.Value ?? "", maxTextChars);
        }

        return null;
    }

    private static string? TryText(AutomationElement element, int maxTextChars)
    {
        if (element.TryGetCurrentPattern(TextPattern.Pattern, out object pattern)
            && pattern is TextPattern textPattern)
        {
            return TextCollector.Truncate(textPattern.DocumentRange.GetText(maxTextChars), maxTextChars);
        }

        return null;
    }

    private static bool SafeBool(AutomationElement element, AutomationProperty property)
    {
        object value = element.GetCurrentPropertyValue(property, true);
        return value is bool result && result;
    }

    private static AutomationControlType SafeControlType(AutomationElement element)
    {
        object value = element.GetCurrentPropertyValue(AutomationElement.ControlTypeProperty, true);
        return value as AutomationControlType ?? AutomationControlType.Custom;
    }

    private static T? SafeProperty<T>(AutomationElement element, AutomationProperty property)
    {
        object value = element.GetCurrentPropertyValue(property, true);
        return value is T typed ? typed : default;
    }
}

sealed record ElementNode(ElementSnapshot Snapshot, List<ElementNode> Children)
{
    public int NodeCount { get; set; }
    public bool Truncated { get; set; }

    public Dictionary<string, object?> ToJson()
    {
        return new Dictionary<string, object?>
        {
            ["role"] = Snapshot.ControlType,
            ["name"] = Snapshot.Name,
            ["automation_id"] = Snapshot.AutomationId,
            ["class_name"] = Snapshot.ClassName,
            ["is_password"] = Snapshot.IsPassword,
            ["value"] = Snapshot.Value,
            ["text"] = Snapshot.Text,
            ["children"] = Children.Select(child => child.ToJson()).ToArray(),
        };
    }

    public IEnumerable<string> FlattenText()
    {
        foreach (string value in Snapshot.TextValues())
        {
            yield return value;
        }

        foreach (ElementNode child in Children)
        {
            foreach (string value in child.FlattenText())
            {
                yield return value;
            }
        }
    }
}

sealed record Limits(int Depth, int MaxNodes, int MaxTextChars, int NodeCount)
{
    public Dictionary<string, object?> ToJson()
    {
        return new Dictionary<string, object?>
        {
            ["depth"] = Depth,
            ["max_nodes"] = MaxNodes,
            ["max_text_chars"] = MaxTextChars,
            ["node_count"] = NodeCount,
        };
    }
}

sealed record ProcessInfo(string ProcessName, string ExePath, string AppName)
{
    public static ProcessInfo FromPid(int pid)
    {
        try
        {
            using Process process = Process.GetProcessById(pid);
            string processName = process.ProcessName.EndsWith(".exe", StringComparison.OrdinalIgnoreCase)
                ? process.ProcessName
                : $"{process.ProcessName}.exe";
            string exePath = "";
            try
            {
                exePath = process.MainModule?.FileName ?? "";
            }
            catch (Exception exc) when (exc is InvalidOperationException or System.ComponentModel.Win32Exception)
            {
                exePath = "";
            }

            return new ProcessInfo(processName, exePath, process.ProcessName);
        }
        catch (Exception exc) when (exc is ArgumentException or InvalidOperationException)
        {
            return new ProcessInfo("", "", "");
        }
    }
}

static class PrivacyGate
{
    private static readonly HashSet<string> AppDenylist = new(StringComparer.OrdinalIgnoreCase)
    {
        "1Password.exe",
        "Bitwarden.exe",
        "Dashlane.exe",
        "KeePass.exe",
        "KeePassXC.exe",
        "LastPass.exe",
        "LockApp.exe",
    };

    private static readonly Regex[] TitleDenylist =
    {
        new("password", RegexOptions.IgnoreCase | RegexOptions.Compiled),
        new("secret", RegexOptions.IgnoreCase | RegexOptions.Compiled),
        new("private key", RegexOptions.IgnoreCase | RegexOptions.Compiled),
        new("recovery phrase", RegexOptions.IgnoreCase | RegexOptions.Compiled),
        new("seed phrase", RegexOptions.IgnoreCase | RegexOptions.Compiled),
    };

    public static string? DenylistReason(string processName, string title)
    {
        if (AppDenylist.Contains(processName))
        {
            return $"denylisted app: {processName}";
        }

        foreach (Regex pattern in TitleDenylist)
        {
            if (pattern.IsMatch(title))
            {
                return $"denylisted title: {title}";
            }
        }

        return null;
    }
}

static class Constants
{
    public const string RedactedPassword = "[REDACTED:password_field]";
}

sealed class PrivacySkipException(string message) : Exception(message);

[StructLayout(LayoutKind.Sequential)]
readonly record struct WindowRect(int Left, int Top, int Right, int Bottom);

static partial class NativeMethods
{
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out int processId);

    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool GetWindowRect(IntPtr hWnd, out WindowRect rect);
}
