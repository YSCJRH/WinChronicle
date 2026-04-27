using System.ComponentModel;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Windows.Automation;
using AutomationControlType = System.Windows.Automation.ControlType;

return Run(args);

static int Run(string[] args)
{
    try
    {
        HelperOptions options = HelperOptions.Parse(args);
        CaptureTarget target = TargetResolver.Resolve(options);
        CaptureOutput output = CaptureWindow(target, options);
        var serializerOptions = new JsonSerializerOptions { WriteIndented = true };
        Console.WriteLine(JsonSerializer.Serialize(output.ToJson(), serializerOptions));
        return 0;
    }
    catch (UsageException exc)
    {
        Console.Error.WriteLine(exc.Message);
        Console.Error.WriteLine(UsageText());
        return 2;
    }
    catch (TargetNotFoundException exc)
    {
        Console.Error.WriteLine(exc.Message);
        return 1;
    }
    catch (PrivacySkipException exc)
    {
        Console.Error.WriteLine($"capture skipped: {exc.Message}");
        return 0;
    }
    catch (Exception exc) when (UiaErrors.IsRecoverable(exc))
    {
        Console.Error.WriteLine($"uia capture failed: {exc.Message}");
        return 1;
    }
}

static string UsageText()
{
    return string.Join(
        Environment.NewLine,
        [
            "usage:",
            "  win-uia-helper capture --frontmost [--depth 80]",
            "  win-uia-helper capture --harness --hwnd <hwnd>",
            "  win-uia-helper capture --harness --pid <pid> --window-title-regex <regex>",
            "  win-uia-helper capture --harness --process-name <name> --window-title-regex <regex>",
            "  win-uia-helper capture-frontmost [--depth 80]  # compatibility alias",
        ]);
}

static CaptureOutput CaptureWindow(CaptureTarget target, HelperOptions options)
{
    UiaStats stats = new(options.Depth, options.MaxNodes, options.MaxTextChars, options.TimeBudgetMs);
    ProcessInfo process = ProcessInfo.FromPid(target.ResolvedPid);
    AutomationElement root = AutomationElement.FromHandle(target.Hwnd);
    string title = WindowFinder.GetWindowTitle(target.Hwnd);
    if (string.IsNullOrWhiteSpace(title))
    {
        title = ElementSnapshot.SafeName(root, stats);
    }

    string? denylistReason = PrivacyGate.DenylistReason(process.ProcessName, title);
    if (denylistReason is not null)
    {
        throw new PrivacySkipException(denylistReason);
    }

    ElementNode tree = TreeExtractor.Capture(
        root,
        options.Depth,
        options.MaxNodes,
        options.MaxTextChars,
        stats);
    ElementSnapshot focused = ElementSnapshot.FromElement(
        FocusedElementForTarget(root, target, stats),
        options.MaxTextChars,
        stats);
    WindowRect rect = NativeMethods.GetWindowRect(target.Hwnd, out WindowRect bounds) ? bounds : new WindowRect();
    string visibleText = TextCollector.VisibleText(tree, options.MaxTextChars, stats);
    string? url = TextCollector.FirstUrl(tree);
    stats.Stop();

    return new CaptureOutput(
        Command: options.OutputCommand,
        Timestamp: DateTimeOffset.Now.ToString("o"),
        Window: new WindowSnapshot(
            Hwnd: HwndFormatting.Format(target.Hwnd),
            Pid: target.ResolvedPid,
            ProcessName: process.ProcessName,
            ExePath: process.ExePath,
            AppName: process.AppName,
            Title: title,
            Bounds: [rect.Left, rect.Top, rect.Right, rect.Bottom],
            Elevated: false),
        FocusedElement: focused,
        VisibleText: visibleText,
        Url: url,
        UiaTree: tree,
        Limits: new Limits(options.Depth, options.MaxNodes, options.MaxTextChars, stats.NodesVisited),
        Truncated: tree.Truncated || stats.Truncated,
        CaptureTarget: target,
        Stats: stats);
}

static AutomationElement FocusedElementForTarget(
    AutomationElement root,
    CaptureTarget target,
    UiaStats stats)
{
    if (!target.FrontmostAtCapture)
    {
        return root;
    }

    AutomationElement? focused = GetFocusedElement(stats);
    if (focused is null)
    {
        return root;
    }

    int? focusedPid = ElementSnapshot.SafeProcessId(focused, stats);
    return focusedPid == target.ResolvedPid ? focused : root;
}

static AutomationElement? GetFocusedElement(UiaStats stats)
{
    try
    {
        return AutomationElement.FocusedElement;
    }
    catch (Exception exc) when (UiaErrors.IsRecoverable(exc))
    {
        stats.RecordException(exc);
        return null;
    }
}

sealed record HelperOptions(
    string OutputCommand,
    TargetRequestKind TargetKind,
    bool Harness,
    IntPtr? Hwnd,
    int? Pid,
    string? ProcessName,
    string? WindowTitleRegex,
    int Depth,
    int MaxNodes,
    int MaxTextChars,
    int TimeBudgetMs)
{
    public bool IsTargeted => TargetKind != TargetRequestKind.Frontmost;

    public static HelperOptions Parse(string[] args)
    {
        if (args.Length == 0)
        {
            throw new UsageException("missing command");
        }

        if (args[0] == "capture-frontmost")
        {
            BudgetOptions legacyBudgets = BudgetOptions.Parse(args, 1);
            return new HelperOptions(
                OutputCommand: "capture-frontmost",
                TargetKind: TargetRequestKind.Frontmost,
                Harness: false,
                Hwnd: null,
                Pid: null,
                ProcessName: null,
                WindowTitleRegex: null,
                Depth: legacyBudgets.Depth,
                MaxNodes: legacyBudgets.MaxNodes,
                MaxTextChars: legacyBudgets.MaxTextChars,
                TimeBudgetMs: legacyBudgets.TimeBudgetMs);
        }

        if (args[0] != "capture")
        {
            throw new UsageException($"unknown command: {args[0]}");
        }

        bool frontmost = false;
        bool harness = false;
        string? hwndText = null;
        int? pid = null;
        string? processName = null;
        string? titleRegex = null;
        BudgetOptions budgets = BudgetOptions.Default;

        for (int index = 1; index < args.Length; index++)
        {
            string arg = args[index];
            switch (arg)
            {
                case "--frontmost":
                    frontmost = true;
                    break;
                case "--harness":
                    harness = true;
                    break;
                case "--hwnd":
                    hwndText = RequireValue(args, ref index, "--hwnd");
                    break;
                case "--pid":
                    pid = ParseInt(RequireValue(args, ref index, "--pid"), "--pid");
                    break;
                case "--process-name":
                    processName = RequireValue(args, ref index, "--process-name");
                    break;
                case "--window-title-regex":
                    titleRegex = RequireValue(args, ref index, "--window-title-regex");
                    _ = CompileTitleRegex(titleRegex);
                    break;
                case "--depth":
                    budgets = budgets with { Depth = ParseBudget(RequireValue(args, ref index, "--depth"), "--depth", 0, HelperLimits.AbsoluteMaxDepth) };
                    break;
                case "--max-nodes":
                    budgets = budgets with { MaxNodes = ParseBudget(RequireValue(args, ref index, "--max-nodes"), "--max-nodes", 1, HelperLimits.AbsoluteMaxNodes) };
                    break;
                case "--max-chars":
                    budgets = budgets with { MaxTextChars = ParseBudget(RequireValue(args, ref index, "--max-chars"), "--max-chars", 1, HelperLimits.AbsoluteMaxTextChars) };
                    break;
                case "--time-budget-ms":
                    budgets = budgets with { TimeBudgetMs = ParseBudget(RequireValue(args, ref index, "--time-budget-ms"), "--time-budget-ms", 1, HelperLimits.AbsoluteMaxTimeBudgetMs) };
                    break;
                case "--no-store":
                    break;
                default:
                    throw new UsageException($"unknown argument: {arg}");
            }
        }

        bool hasHwnd = hwndText is not null;
        bool hasPid = pid is not null;
        bool hasProcessName = processName is not null;
        int targetForms = new[] { frontmost, hasHwnd, hasPid, hasProcessName }.Count(value => value);
        if (targetForms != 1)
        {
            throw new UsageException("exactly one capture target is required");
        }

        TargetRequestKind targetKind;
        IntPtr? hwnd = null;
        if (frontmost)
        {
            if (harness)
            {
                throw new UsageException("--harness is only for targeted harness captures");
            }
            targetKind = TargetRequestKind.Frontmost;
        }
        else
        {
            RequireHarnessGate(harness);
            if (hasHwnd)
            {
                hwnd = ParseHwnd(hwndText!);
                targetKind = TargetRequestKind.Hwnd;
            }
            else if (hasPid)
            {
                if (titleRegex is null)
                {
                    throw new UsageException("--pid requires --window-title-regex");
                }
                targetKind = TargetRequestKind.PidWindowTitleRegex;
            }
            else
            {
                if (titleRegex is null)
                {
                    throw new UsageException("--process-name requires --window-title-regex");
                }
                targetKind = TargetRequestKind.ProcessNameWindowTitleRegex;
            }
        }

        return new HelperOptions(
            OutputCommand: "capture",
            TargetKind: targetKind,
            Harness: harness,
            Hwnd: hwnd,
            Pid: pid,
            ProcessName: processName,
            WindowTitleRegex: titleRegex,
            Depth: budgets.Depth,
            MaxNodes: budgets.MaxNodes,
            MaxTextChars: budgets.MaxTextChars,
            TimeBudgetMs: budgets.TimeBudgetMs);
    }

    private static void RequireHarnessGate(bool harness)
    {
        if (!harness)
        {
            throw new UsageException("targeted capture requires --harness");
        }

        if (Environment.GetEnvironmentVariable("WINCHRONICLE_HARNESS") != "1")
        {
            throw new UsageException("targeted capture requires WINCHRONICLE_HARNESS=1");
        }
    }

    private static string RequireValue(string[] args, ref int index, string option)
    {
        if (index + 1 >= args.Length)
        {
            throw new UsageException($"{option} requires a value");
        }
        index++;
        return args[index];
    }

    private static int ParseInt(string value, string option)
    {
        if (!int.TryParse(value, out int result))
        {
            throw new UsageException($"{option} must be an integer");
        }
        return result;
    }

    private static int ParseBudget(string value, string option, int minimum, int maximum)
    {
        int parsed = ParseInt(value, option);
        if (parsed < minimum || parsed > maximum)
        {
            throw new UsageException($"{option} must be between {minimum} and {maximum}");
        }
        return parsed;
    }

    private static IntPtr ParseHwnd(string value)
    {
        string normalized = value.StartsWith("0x", StringComparison.OrdinalIgnoreCase)
            ? value[2..]
            : value;
        System.Globalization.NumberStyles styles = value.StartsWith("0x", StringComparison.OrdinalIgnoreCase)
            ? System.Globalization.NumberStyles.HexNumber
            : System.Globalization.NumberStyles.Integer;
        if (!long.TryParse(normalized, styles, null, out long parsed) || parsed == 0)
        {
            throw new UsageException("--hwnd must be a non-zero integer or 0x-prefixed hex handle");
        }
        return new IntPtr(parsed);
    }

    internal static Regex CompileTitleRegex(string pattern)
    {
        try
        {
            return new Regex(pattern, RegexOptions.IgnoreCase | RegexOptions.CultureInvariant);
        }
        catch (ArgumentException exc)
        {
            throw new UsageException($"--window-title-regex is invalid: {exc.Message}");
        }
    }
}

static class HelperLimits
{
    public const int DefaultDepth = 80;
    public const int DefaultMaxNodes = 5000;
    public const int DefaultMaxTextChars = 20000;
    public const int DefaultTimeBudgetMs = 3000;
    public const int AbsoluteMaxDepth = 80;
    public const int AbsoluteMaxNodes = 5000;
    public const int AbsoluteMaxTextChars = 20000;
    public const int AbsoluteMaxTimeBudgetMs = 10000;
}

static class HwndFormatting
{
    public static string Format(IntPtr hwnd)
    {
        return $"0x{hwnd.ToInt64():X16}";
    }
}

sealed record BudgetOptions(int Depth, int MaxNodes, int MaxTextChars, int TimeBudgetMs)
{
    public static BudgetOptions Default => new(
        HelperLimits.DefaultDepth,
        HelperLimits.DefaultMaxNodes,
        HelperLimits.DefaultMaxTextChars,
        HelperLimits.DefaultTimeBudgetMs);

    public static BudgetOptions Parse(string[] args, int start)
    {
        BudgetOptions budgets = Default;
        for (int index = start; index < args.Length; index++)
        {
            switch (args[index])
            {
                case "--depth":
                    budgets = budgets with
                    {
                        Depth = HelperOptionsExtensions.ParseBudgetForAlias(
                            HelperOptionsValue(args, ref index, "--depth"),
                            "--depth",
                            0,
                            HelperLimits.AbsoluteMaxDepth),
                    };
                    break;
                case "--max-nodes":
                    budgets = budgets with
                    {
                        MaxNodes = HelperOptionsExtensions.ParseBudgetForAlias(
                            HelperOptionsValue(args, ref index, "--max-nodes"),
                            "--max-nodes",
                            1,
                            HelperLimits.AbsoluteMaxNodes),
                    };
                    break;
                case "--max-chars":
                    budgets = budgets with
                    {
                        MaxTextChars = HelperOptionsExtensions.ParseBudgetForAlias(
                            HelperOptionsValue(args, ref index, "--max-chars"),
                            "--max-chars",
                            1,
                            HelperLimits.AbsoluteMaxTextChars),
                    };
                    break;
                case "--time-budget-ms":
                    budgets = budgets with
                    {
                        TimeBudgetMs = HelperOptionsExtensions.ParseBudgetForAlias(
                            HelperOptionsValue(args, ref index, "--time-budget-ms"),
                            "--time-budget-ms",
                            1,
                            HelperLimits.AbsoluteMaxTimeBudgetMs),
                    };
                    break;
                default:
                    throw new UsageException($"unknown argument: {args[index]}");
            }
        }
        return budgets;
    }

    private static string HelperOptionsValue(string[] args, ref int index, string option)
    {
        if (index + 1 >= args.Length)
        {
            throw new UsageException($"{option} requires a value");
        }
        index++;
        return args[index];
    }
}

static class HelperOptionsExtensions
{
    public static int ParseBudgetForAlias(this HelperOptions _, string value, string option, int minimum, int maximum)
    {
        return ParseBudget(value, option, minimum, maximum);
    }

    public static int ParseBudgetForAlias(string value, string option, int minimum, int maximum)
    {
        return ParseBudget(value, option, minimum, maximum);
    }

    private static int ParseBudget(string value, string option, int minimum, int maximum)
    {
        if (!int.TryParse(value, out int parsed))
        {
            throw new UsageException($"{option} must be an integer");
        }
        if (parsed < minimum || parsed > maximum)
        {
            throw new UsageException($"{option} must be between {minimum} and {maximum}");
        }
        return parsed;
    }
}

enum TargetRequestKind
{
    Frontmost,
    Hwnd,
    PidWindowTitleRegex,
    ProcessNameWindowTitleRegex,
}

static class TargetResolver
{
    public static CaptureTarget Resolve(HelperOptions options)
    {
        return options.TargetKind switch
        {
            TargetRequestKind.Frontmost => ResolveFrontmost(options),
            TargetRequestKind.Hwnd => ResolveHwnd(options),
            TargetRequestKind.PidWindowTitleRegex => ResolvePidWindow(options),
            TargetRequestKind.ProcessNameWindowTitleRegex => ResolveProcessWindow(options),
            _ => throw new UsageException("unsupported capture target"),
        };
    }

    private static CaptureTarget ResolveFrontmost(HelperOptions options)
    {
        IntPtr hwnd = NativeMethods.GetForegroundWindow();
        if (hwnd == IntPtr.Zero)
        {
            throw new TargetNotFoundException("no foreground window");
        }
        int pid = WindowFinder.PidForWindow(hwnd);
        return CaptureTarget.Create("frontmost", hwnd, null, pid, false);
    }

    private static CaptureTarget ResolveHwnd(HelperOptions options)
    {
        IntPtr hwnd = options.Hwnd ?? throw new UsageException("--hwnd is required");
        if (!NativeMethods.IsWindow(hwnd))
        {
            throw new TargetNotFoundException($"target hwnd was not found: {HwndFormatting.Format(hwnd)}");
        }
        int pid = WindowFinder.PidForWindow(hwnd);
        return CaptureTarget.Create("hwnd", hwnd, null, pid, true);
    }

    private static CaptureTarget ResolvePidWindow(HelperOptions options)
    {
        int pid = options.Pid ?? throw new UsageException("--pid is required");
        Regex titleRegex = HelperOptions.CompileTitleRegex(options.WindowTitleRegex ?? "");
        IntPtr hwnd = WindowFinder.FindByPidAndTitle(pid, titleRegex);
        if (hwnd == IntPtr.Zero)
        {
            throw new TargetNotFoundException("no visible top-level window matched --pid and --window-title-regex");
        }
        return CaptureTarget.Create("pid_window_title_regex", hwnd, pid, WindowFinder.PidForWindow(hwnd), true);
    }

    private static CaptureTarget ResolveProcessWindow(HelperOptions options)
    {
        string processName = options.ProcessName ?? throw new UsageException("--process-name is required");
        Regex titleRegex = HelperOptions.CompileTitleRegex(options.WindowTitleRegex ?? "");
        IntPtr hwnd = WindowFinder.FindByProcessNameAndTitle(processName, titleRegex);
        if (hwnd == IntPtr.Zero)
        {
            throw new TargetNotFoundException("no visible top-level window matched --process-name and --window-title-regex");
        }
        return CaptureTarget.Create("process_name_window_title_regex", hwnd, null, WindowFinder.PidForWindow(hwnd), true);
    }
}

sealed record CaptureTarget(
    string Kind,
    IntPtr Hwnd,
    int? RequestedPid,
    int ResolvedPid,
    bool FrontmostAtCapture,
    bool HarnessOnly)
{
    public static CaptureTarget Create(
        string kind,
        IntPtr hwnd,
        int? requestedPid,
        int resolvedPid,
        bool harnessOnly)
    {
        bool frontmost = NativeMethods.GetForegroundWindow() == hwnd;
        return new CaptureTarget(kind, hwnd, requestedPid, resolvedPid, frontmost, harnessOnly);
    }

    public Dictionary<string, object?> ToJson()
    {
        return new Dictionary<string, object?>
        {
            ["kind"] = Kind,
            ["hwnd"] = HwndFormatting.Format(Hwnd),
            ["requested_pid"] = RequestedPid,
            ["resolved_pid"] = ResolvedPid,
            ["frontmost_at_capture"] = FrontmostAtCapture,
            ["harness_only"] = HarnessOnly,
        };
    }
}

static class WindowFinder
{
    public static int PidForWindow(IntPtr hwnd)
    {
        NativeMethods.GetWindowThreadProcessId(hwnd, out int pid);
        return pid;
    }

    public static IntPtr FindByPidAndTitle(int pid, Regex titleRegex)
    {
        return FindWindow(hwnd =>
        {
            int windowPid = PidForWindow(hwnd);
            return windowPid == pid && titleRegex.IsMatch(GetWindowTitle(hwnd));
        });
    }

    public static IntPtr FindByProcessNameAndTitle(string processName, Regex titleRegex)
    {
        string expected = NormalizeProcessName(processName);
        return FindWindow(hwnd =>
        {
            int pid = PidForWindow(hwnd);
            ProcessInfo process = ProcessInfo.FromPid(pid);
            return string.Equals(process.ProcessName, expected, StringComparison.OrdinalIgnoreCase)
                && titleRegex.IsMatch(GetWindowTitle(hwnd));
        });
    }

    public static string GetWindowTitle(IntPtr hwnd)
    {
        int length = NativeMethods.GetWindowTextLength(hwnd);
        if (length <= 0)
        {
            return "";
        }
        StringBuilder builder = new(length + 1);
        _ = NativeMethods.GetWindowText(hwnd, builder, builder.Capacity);
        return builder.ToString();
    }

    private static IntPtr FindWindow(Func<IntPtr, bool> predicate)
    {
        IntPtr result = IntPtr.Zero;
        NativeMethods.EnumWindows((hwnd, _) =>
        {
            if (!NativeMethods.IsWindowVisible(hwnd))
            {
                return true;
            }
            if (predicate(hwnd))
            {
                result = hwnd;
                return false;
            }
            return true;
        }, IntPtr.Zero);
        return result;
    }

    private static string NormalizeProcessName(string value)
    {
        return value.EndsWith(".exe", StringComparison.OrdinalIgnoreCase) ? value : $"{value}.exe";
    }
}

static class TreeExtractor
{
    private static readonly TreeWalker[] OrderedWalkers =
    [
        TreeWalker.ContentViewWalker,
        TreeWalker.ControlViewWalker,
        TreeWalker.RawViewWalker,
    ];

    public static ElementNode Capture(
        AutomationElement root,
        int maxDepth,
        int maxNodes,
        int maxTextChars,
        UiaStats stats)
    {
        ElementNode? node = CaptureNode(root, 0, maxDepth, maxNodes, maxTextChars, stats);
        if (node is null)
        {
            stats.NodesSkipped++;
            return new ElementNode(ElementSnapshot.Empty, []);
        }
        node.NodeCount = stats.NodesVisited;
        node.Truncated = stats.Truncated;
        return node;
    }

    private static ElementNode? CaptureNode(
        AutomationElement element,
        int depth,
        int maxDepth,
        int maxNodes,
        int maxTextChars,
        UiaStats stats)
    {
        if (!stats.TryVisitNode(depth))
        {
            stats.NodesSkipped++;
            return null;
        }

        ElementSnapshot snapshot = ElementSnapshot.FromElement(element, maxTextChars, stats);
        var children = new List<ElementNode>();

        if (depth >= maxDepth)
        {
            stats.MaxDepthReached = true;
            return new ElementNode(snapshot, children) { Truncated = true };
        }

        var seenChildIds = new HashSet<string>(StringComparer.Ordinal);
        foreach (TreeWalker walker in OrderedWalkers)
        {
            if (stats.BudgetExceeded)
            {
                break;
            }

            AutomationElement? child = SafeFirstChild(walker, element, stats);
            while (child is not null && !stats.BudgetExceeded)
            {
                string runtimeId = RuntimeIdKey(child, stats);
                if (seenChildIds.Add(runtimeId))
                {
                    ElementNode? childNode = CaptureNode(child, depth + 1, maxDepth, maxNodes, maxTextChars, stats);
                    if (childNode is not null)
                    {
                        children.Add(childNode);
                    }
                }
                child = SafeNextSibling(walker, child, stats);
            }
        }

        return new ElementNode(snapshot, children) { Truncated = stats.Truncated };
    }

    private static AutomationElement? SafeFirstChild(TreeWalker walker, AutomationElement element, UiaStats stats)
    {
        try
        {
            return walker.GetFirstChild(element);
        }
        catch (Exception exc) when (UiaErrors.IsRecoverable(exc))
        {
            stats.RecordException(exc);
            return null;
        }
    }

    private static AutomationElement? SafeNextSibling(TreeWalker walker, AutomationElement element, UiaStats stats)
    {
        try
        {
            return walker.GetNextSibling(element);
        }
        catch (Exception exc) when (UiaErrors.IsRecoverable(exc))
        {
            stats.RecordException(exc);
            return null;
        }
    }

    private static string RuntimeIdKey(AutomationElement element, UiaStats stats)
    {
        try
        {
            int[] runtimeId = element.GetRuntimeId();
            return runtimeId.Length == 0
                ? $"hash:{element.GetHashCode()}"
                : string.Join(".", runtimeId);
        }
        catch (Exception exc) when (UiaErrors.IsRecoverable(exc))
        {
            stats.RecordException(exc);
            return $"stale:{Guid.NewGuid():N}";
        }
    }
}

static class TextCollector
{
    private static readonly Regex UrlPattern = new(@"https?://\S+", RegexOptions.Compiled | RegexOptions.IgnoreCase);

    public static string VisibleText(ElementNode root, int maxTextChars, UiaStats stats)
    {
        var parts = new List<string>();
        var seen = new HashSet<string>(StringComparer.Ordinal);
        CollectText(root, parts, seen, maxTextChars, stats);
        return Truncate(string.Join("\n", parts), maxTextChars);
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

    public static string Truncate(string value, int maxTextChars)
    {
        return value.Length <= maxTextChars ? value : value[..maxTextChars];
    }

    private static void CollectText(
        ElementNode node,
        List<string> parts,
        HashSet<string> seen,
        int maxTextChars,
        UiaStats stats)
    {
        if (stats.CharsCollected >= maxTextChars)
        {
            stats.MaxCharsReached = true;
            return;
        }

        foreach (string value in node.Snapshot.TextValues())
        {
            if (string.IsNullOrWhiteSpace(value) || !seen.Add(value))
            {
                continue;
            }

            int remaining = maxTextChars - stats.CharsCollected;
            string part = value.Length <= remaining ? value : value[..remaining];
            parts.Add(part);
            stats.RecordChars(part.Length);
            if (part.Length < value.Length)
            {
                stats.MaxCharsReached = true;
                return;
            }
        }

        foreach (ElementNode child in node.Children)
        {
            CollectText(child, parts, seen, maxTextChars, stats);
            if (stats.MaxCharsReached)
            {
                return;
            }
        }
    }
}

sealed record CaptureOutput(
    string Command,
    string Timestamp,
    WindowSnapshot Window,
    ElementSnapshot FocusedElement,
    string VisibleText,
    string? Url,
    ElementNode UiaTree,
    Limits Limits,
    bool Truncated,
    CaptureTarget CaptureTarget,
    UiaStats Stats)
{
    public Dictionary<string, object?> ToJson()
    {
        return new Dictionary<string, object?>
        {
            ["helper_schema_version"] = 1,
            ["source"] = "win-uia-helper",
            ["command"] = Command,
            ["timestamp"] = Timestamp,
            ["window"] = Window.ToJson(),
            ["focused_element"] = FocusedElement.ToJson(),
            ["visible_text"] = VisibleText,
            ["url"] = Url,
            ["uia_tree"] = UiaTree.ToJson(),
            ["limits"] = Limits.ToJson(),
            ["uia_stats"] = Stats.ToJson(),
            ["capture_target"] = CaptureTarget.ToJson(),
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
    string? Text,
    string? LegacyText)
{
    public static ElementSnapshot Empty => new("", "", "", "", false, false, null, null, null);

    public static ElementSnapshot FromElement(AutomationElement? element, int maxTextChars, UiaStats stats)
    {
        if (element is null)
        {
            return Empty;
        }

        bool isPassword = SafeBool(element, AutomationElement.IsPasswordProperty, stats);
        AutomationControlType controlType = SafeControlType(element, stats);
        bool isEditable = SupportsPattern(element, ValuePattern.Pattern, stats)
            || SupportsPattern(element, TextPattern.Pattern, stats);
        string? text = isPassword ? Constants.RedactedPassword : TryText(element, maxTextChars, stats);
        string? value = isPassword ? Constants.RedactedPassword : TryValue(element, maxTextChars, stats);
        string? legacy = isPassword ? null : TryLegacyText(element, maxTextChars, stats);

        return new ElementSnapshot(
            ControlType: controlType.ProgrammaticName.Replace("ControlType.", ""),
            Name: SafeProperty<string>(element, AutomationElement.NameProperty, stats) ?? "",
            AutomationId: SafeProperty<string>(element, AutomationElement.AutomationIdProperty, stats) ?? "",
            ClassName: SafeProperty<string>(element, AutomationElement.ClassNameProperty, stats) ?? "",
            IsEditable: isEditable,
            IsPassword: isPassword,
            Value: value,
            Text: text,
            LegacyText: legacy);
    }

    public static string SafeName(AutomationElement element, UiaStats stats)
    {
        return SafeProperty<string>(element, AutomationElement.NameProperty, stats) ?? "";
    }

    public static int? SafeProcessId(AutomationElement element, UiaStats stats)
    {
        return SafeProperty<int>(element, AutomationElement.ProcessIdProperty, stats);
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
        if (!string.IsNullOrWhiteSpace(Text))
        {
            yield return Text;
        }

        if (IsEditable && !string.IsNullOrWhiteSpace(Value))
        {
            yield return Value;
        }

        if (!string.IsNullOrWhiteSpace(Name))
        {
            yield return Name;
        }

        if (!string.IsNullOrWhiteSpace(LegacyText))
        {
            yield return LegacyText;
        }
    }

    private static bool SupportsPattern(AutomationElement element, AutomationPattern pattern, UiaStats stats)
    {
        try
        {
            return element.TryGetCurrentPattern(pattern, out _);
        }
        catch (Exception exc) when (UiaErrors.IsRecoverable(exc))
        {
            stats.RecordException(exc);
            return false;
        }
    }

    private static string? TryValue(AutomationElement element, int maxTextChars, UiaStats stats)
    {
        try
        {
            if (element.TryGetCurrentPattern(ValuePattern.Pattern, out object pattern)
                && pattern is ValuePattern valuePattern)
            {
                return TextCollector.Truncate(valuePattern.Current.Value ?? "", maxTextChars);
            }
        }
        catch (Exception exc) when (UiaErrors.IsRecoverable(exc))
        {
            stats.RecordException(exc);
            return null;
        }

        return null;
    }

    private static string? TryText(AutomationElement element, int maxTextChars, UiaStats stats)
    {
        try
        {
            if (element.TryGetCurrentPattern(TextPattern.Pattern, out object pattern)
                && pattern is TextPattern textPattern)
            {
                return TextCollector.Truncate(textPattern.DocumentRange.GetText(maxTextChars), maxTextChars);
            }
        }
        catch (Exception exc) when (UiaErrors.IsRecoverable(exc))
        {
            stats.RecordException(exc);
            return null;
        }

        return null;
    }

    private static string? TryLegacyText(AutomationElement element, int maxTextChars, UiaStats stats)
    {
        try
        {
            AutomationPattern? legacyPattern = AutomationPattern.LookupById(10018);
            if (legacyPattern is null)
            {
                return null;
            }
            if (element.TryGetCurrentPattern(legacyPattern, out object pattern))
            {
                object? current = pattern.GetType().GetProperty("Current")?.GetValue(pattern);
                string value = string.Join(
                    "\n",
                    new[]
                    {
                        LegacyProperty(current, "Name"),
                        LegacyProperty(current, "Value"),
                        LegacyProperty(current, "Description"),
                    }.Where(part => !string.IsNullOrWhiteSpace(part)).Distinct());
                return TextCollector.Truncate(value, maxTextChars);
            }
        }
        catch (Exception exc) when (UiaErrors.IsRecoverable(exc))
        {
            stats.RecordException(exc);
            return null;
        }

        return null;
    }

    private static string? LegacyProperty(object? current, string name)
    {
        return current?.GetType().GetProperty(name)?.GetValue(current) as string;
    }

    private static bool SafeBool(AutomationElement element, AutomationProperty property, UiaStats stats)
    {
        try
        {
            object value = element.GetCurrentPropertyValue(property, true);
            return value is bool result && result;
        }
        catch (Exception exc) when (UiaErrors.IsRecoverable(exc))
        {
            stats.RecordException(exc);
            return false;
        }
    }

    private static AutomationControlType SafeControlType(AutomationElement element, UiaStats stats)
    {
        try
        {
            object value = element.GetCurrentPropertyValue(AutomationElement.ControlTypeProperty, true);
            return value as AutomationControlType ?? AutomationControlType.Custom;
        }
        catch (Exception exc) when (UiaErrors.IsRecoverable(exc))
        {
            stats.RecordException(exc);
            return AutomationControlType.Custom;
        }
    }

    private static T? SafeProperty<T>(AutomationElement element, AutomationProperty property, UiaStats stats)
    {
        try
        {
            object value = element.GetCurrentPropertyValue(property, true);
            return value is T typed ? typed : default;
        }
        catch (Exception exc) when (UiaErrors.IsRecoverable(exc))
        {
            stats.RecordException(exc);
            return default;
        }
    }
}

sealed record ElementNode(ElementSnapshot Snapshot, List<ElementNode> Children)
{
    public int NodeCount { get; set; }
    public bool Truncated { get; set; }

    public Dictionary<string, object?> ToJson()
    {
        var payload = new Dictionary<string, object?>
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
        if (!string.IsNullOrWhiteSpace(Snapshot.LegacyText))
        {
            payload["legacy_text"] = Snapshot.LegacyText;
        }
        return payload;
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

sealed class UiaStats
{
    private readonly Stopwatch stopwatch = Stopwatch.StartNew();

    public UiaStats(int maxDepth, int maxNodes, int maxChars, int timeBudgetMs)
    {
        MaxDepth = maxDepth;
        MaxNodes = maxNodes;
        MaxChars = maxChars;
        TimeBudgetMs = timeBudgetMs;
    }

    public int MaxDepth { get; }
    public int MaxNodes { get; }
    public int MaxChars { get; }
    public int TimeBudgetMs { get; }
    public int NodesVisited { get; private set; }
    public int NodesSkipped { get; set; }
    public int StaleNodesSkipped { get; private set; }
    public int ExceptionsSkipped { get; private set; }
    public int CharsCollected { get; private set; }
    public int MaxDepthObserved { get; private set; }
    public bool MaxNodesReached { get; set; }
    public bool MaxDepthReached { get; set; }
    public bool MaxCharsReached { get; set; }
    public bool TimeBudgetExceeded => stopwatch.ElapsedMilliseconds >= TimeBudgetMs;
    public bool BudgetExceeded => MaxNodesReached || TimeBudgetExceeded;
    public bool Truncated => MaxNodesReached || MaxDepthReached || MaxCharsReached || TimeBudgetExceeded;

    public bool TryVisitNode(int depth)
    {
        if (TimeBudgetExceeded)
        {
            return false;
        }
        if (NodesVisited >= MaxNodes)
        {
            MaxNodesReached = true;
            return false;
        }
        NodesVisited++;
        MaxDepthObserved = Math.Max(MaxDepthObserved, depth);
        return true;
    }

    public void RecordException(Exception exc)
    {
        ExceptionsSkipped++;
        if (UiaErrors.IsStale(exc))
        {
            StaleNodesSkipped++;
        }
    }

    public void RecordChars(int count)
    {
        CharsCollected += count;
        if (CharsCollected >= MaxChars)
        {
            MaxCharsReached = true;
        }
    }

    public void Stop()
    {
        stopwatch.Stop();
    }

    public Dictionary<string, object?> ToJson()
    {
        return new Dictionary<string, object?>
        {
            ["nodes_visited"] = NodesVisited,
            ["nodes_skipped"] = NodesSkipped,
            ["stale_nodes_skipped"] = StaleNodesSkipped,
            ["exceptions_skipped"] = ExceptionsSkipped,
            ["chars_collected"] = CharsCollected,
            ["elapsed_ms"] = stopwatch.ElapsedMilliseconds,
            ["max_depth_observed"] = MaxDepthObserved,
            ["time_budget_ms"] = TimeBudgetMs,
            ["time_budget_exceeded"] = TimeBudgetExceeded,
            ["max_nodes_reached"] = MaxNodesReached,
            ["max_depth_reached"] = MaxDepthReached,
            ["max_chars_reached"] = MaxCharsReached,
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
            catch (Exception exc) when (exc is InvalidOperationException or Win32Exception)
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
    [
        new("password", RegexOptions.IgnoreCase | RegexOptions.Compiled),
        new("secret", RegexOptions.IgnoreCase | RegexOptions.Compiled),
        new("private key", RegexOptions.IgnoreCase | RegexOptions.Compiled),
        new("recovery phrase", RegexOptions.IgnoreCase | RegexOptions.Compiled),
        new("seed phrase", RegexOptions.IgnoreCase | RegexOptions.Compiled),
    ];

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

static class UiaErrors
{
    private const int RpcEServerCallRetryLater = unchecked((int)0x8001010A);
    private const int RpcECallRejected = unchecked((int)0x80010001);
    private const int RpcEDisconnected = unchecked((int)0x80010108);
    private const int UiaEElementNotAvailable = unchecked((int)0x80040201);

    public static bool IsRecoverable(Exception exc)
    {
        return exc is ElementNotAvailableException
            or InvalidOperationException
            or Win32Exception
            || exc is COMException;
    }

    public static bool IsStale(Exception exc)
    {
        return exc is ElementNotAvailableException
            || exc is COMException comException
                && (
                    comException.HResult == RpcEServerCallRetryLater
                    || comException.HResult == RpcECallRejected
                    || comException.HResult == RpcEDisconnected
                    || comException.HResult == UiaEElementNotAvailable);
    }
}

static class Constants
{
    public const string RedactedPassword = "[REDACTED:password_field]";
}

sealed class UsageException(string message) : Exception(message);

sealed class TargetNotFoundException(string message) : Exception(message);

sealed class PrivacySkipException(string message) : Exception(message);

[StructLayout(LayoutKind.Sequential)]
readonly record struct WindowRect(int Left, int Top, int Right, int Bottom);

static partial class NativeMethods
{
    public delegate bool EnumWindowsProc(IntPtr hWnd, IntPtr lParam);

    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();

    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out int processId);

    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool GetWindowRect(IntPtr hWnd, out WindowRect rect);

    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool IsWindow(IntPtr hWnd);

    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool IsWindowVisible(IntPtr hWnd);

    [DllImport("user32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool EnumWindows(EnumWindowsProc lpEnumFunc, IntPtr lParam);

    [DllImport("user32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    public static extern int GetWindowText(IntPtr hWnd, StringBuilder lpString, int nMaxCount);

    [DllImport("user32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    public static extern int GetWindowTextLength(IntPtr hWnd);
}
