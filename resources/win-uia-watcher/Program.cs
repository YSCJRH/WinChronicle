using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text.Json;
using System.Threading;

return Run(args);

static int Run(string[] args)
{
    if (args.Length == 0 || args[0] != "watch")
    {
        Console.Error.WriteLine("usage: win-uia-watcher watch [--depth 80] [--debounce-ms 750] [--duration-ms 0] [--helper path] [--capture-on-start]");
        return 2;
    }

    var options = WatchOptions.Parse(args);
    using var watcher = new WinEventWatcher(options);
    return watcher.Run();
}

sealed class WinEventWatcher : IDisposable
{
    private readonly WatchOptions _options;
    private readonly JsonSerializerOptions _jsonOptions = new() { WriteIndented = false };
    private readonly NativeMethods.WinEventDelegate _callback;
    private readonly List<IntPtr> _hooks = new();
    private readonly Stopwatch _clock = Stopwatch.StartNew();
    private readonly object _gate = new();
    private long _lastCaptureMs = -1_000_000;
    private long _lastHeartbeatMs = -1_000_000;
    private bool _cancelled;

    public WinEventWatcher(WatchOptions options)
    {
        _options = options;
        _callback = HandleEvent;
    }

    public int Run()
    {
        Console.CancelKeyPress += (_, eventArgs) =>
        {
            eventArgs.Cancel = true;
            _cancelled = true;
        };

        if (!InstallHooks())
        {
            Console.Error.WriteLine("failed to install WinEvent hooks");
            return 1;
        }

        if (_options.CaptureOnStart)
        {
            WriteCaptureEvent("foreground_changed");
        }

        while (!_cancelled)
        {
            if (_options.DurationMs > 0 && _clock.ElapsedMilliseconds >= _options.DurationMs)
            {
                break;
            }

            NativeMessage message;
            while (NativeMethods.PeekMessage(out message, IntPtr.Zero, 0, 0, 1))
            {
                NativeMethods.TranslateMessage(ref message);
                NativeMethods.DispatchMessage(ref message);
            }

            if (_clock.ElapsedMilliseconds - _lastHeartbeatMs >= _options.HeartbeatMs)
            {
                _lastHeartbeatMs = _clock.ElapsedMilliseconds;
                WriteHeartbeat();
            }

            Thread.Sleep(50);
        }

        return 0;
    }

    private bool InstallHooks()
    {
        return InstallHook(NativeConstants.EventSystemForeground, NativeConstants.EventSystemForeground)
            && InstallHook(NativeConstants.EventObjectNameChange, NativeConstants.EventObjectNameChange)
            && InstallHook(NativeConstants.EventObjectValueChange, NativeConstants.EventObjectValueChange);
    }

    private bool InstallHook(int eventMin, int eventMax)
    {
        IntPtr hook = NativeMethods.SetWinEventHook(
            eventMin,
            eventMax,
            IntPtr.Zero,
            _callback,
            0,
            0,
            NativeConstants.WineventOutOfContext | NativeConstants.WineventSkipOwnProcess);
        if (hook == IntPtr.Zero)
        {
            return false;
        }

        _hooks.Add(hook);
        return true;
    }

    private void HandleEvent(
        IntPtr hook,
        int eventType,
        IntPtr hwnd,
        int idObject,
        int idChild,
        int eventThread,
        int eventTime)
    {
        lock (_gate)
        {
            if (_clock.ElapsedMilliseconds - _lastCaptureMs < _options.DebounceMs)
            {
                return;
            }

            _lastCaptureMs = _clock.ElapsedMilliseconds;
        }

        string eventName = eventType switch
        {
            NativeConstants.EventSystemForeground => "foreground_changed",
            NativeConstants.EventObjectNameChange => "name_changed",
            NativeConstants.EventObjectValueChange => "value_changed",
            _ => "foreground_changed",
        };

        WriteCaptureEvent(eventName);
    }

    private JsonElement? CaptureForeground()
    {
        var startInfo = new ProcessStartInfo
        {
            FileName = _options.HelperCommand,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
        };
        foreach (string arg in _options.HelperArgs)
        {
            startInfo.ArgumentList.Add(arg);
        }
        startInfo.ArgumentList.Add("capture-frontmost");
        startInfo.ArgumentList.Add("--depth");
        startInfo.ArgumentList.Add(_options.Depth.ToString());

        using Process? process = Process.Start(startInfo);
        if (process is null)
        {
            return null;
        }

        string stdout = process.StandardOutput.ReadToEnd();
        _ = process.StandardError.ReadToEnd();
        process.WaitForExit();
        if (process.ExitCode != 0 || string.IsNullOrWhiteSpace(stdout))
        {
            return null;
        }

        using JsonDocument document = JsonDocument.Parse(stdout);
        return document.RootElement.Clone();
    }

    private void WriteCaptureEvent(string eventName)
    {
        JsonElement? capture = CaptureForeground();
        if (capture is null)
        {
            return;
        }

        var payload = new Dictionary<string, object?>
        {
            ["event_schema_version"] = 1,
            ["source"] = "win-uia-watcher",
            ["event_id"] = $"{eventName}-{Guid.NewGuid():N}",
            ["event_type"] = eventName,
            ["timestamp"] = DateTimeOffset.Now.ToString("o"),
            ["capture"] = capture.Value,
        };
        Console.WriteLine(JsonSerializer.Serialize(payload, _jsonOptions));
        Console.Out.Flush();
    }

    private void WriteHeartbeat()
    {
        var payload = new Dictionary<string, object?>
        {
            ["event_schema_version"] = 1,
            ["source"] = "win-uia-watcher",
            ["event_id"] = $"heartbeat-{Guid.NewGuid():N}",
            ["event_type"] = "heartbeat",
            ["timestamp"] = DateTimeOffset.Now.ToString("o"),
            ["heartbeat_id"] = Guid.NewGuid().ToString("N"),
        };
        Console.WriteLine(JsonSerializer.Serialize(payload, _jsonOptions));
        Console.Out.Flush();
    }

    public void Dispose()
    {
        foreach (IntPtr hook in _hooks)
        {
            NativeMethods.UnhookWinEvent(hook);
        }
    }
}

sealed record WatchOptions(
    int Depth,
    int DebounceMs,
    int DurationMs,
    int HeartbeatMs,
    bool CaptureOnStart,
    string HelperCommand,
    IReadOnlyList<string> HelperArgs)
{
    public static WatchOptions Parse(string[] args)
    {
        int depth = 80;
        int debounceMs = 750;
        int durationMs = 0;
        int heartbeatMs = 5000;
        bool captureOnStart = false;
        string? helper = null;
        var helperArgs = new List<string>();

        for (int index = 1; index < args.Length; index++)
        {
            switch (args[index])
            {
                case "--depth" when index + 1 < args.Length:
                    depth = int.Parse(args[++index]);
                    break;
                case "--debounce-ms" when index + 1 < args.Length:
                    debounceMs = int.Parse(args[++index]);
                    break;
                case "--duration-ms" when index + 1 < args.Length:
                    durationMs = int.Parse(args[++index]);
                    break;
                case "--heartbeat-ms" when index + 1 < args.Length:
                    heartbeatMs = int.Parse(args[++index]);
                    break;
                case "--capture-on-start":
                    captureOnStart = true;
                    break;
                case "--helper" when index + 1 < args.Length:
                    helper = args[++index];
                    break;
                case "--helper-arg" when index + 1 < args.Length:
                    helperArgs.Add(args[++index]);
                    break;
            }
        }

        helper ??= Path.Combine(AppContext.BaseDirectory, "win-uia-helper.exe");
        return new WatchOptions(
            Depth: Math.Clamp(depth, 0, 80),
            DebounceMs: Math.Max(0, debounceMs),
            DurationMs: Math.Max(0, durationMs),
            HeartbeatMs: Math.Max(250, heartbeatMs),
            CaptureOnStart: captureOnStart,
            HelperCommand: helper,
            HelperArgs: helperArgs);
    }
}

[StructLayout(LayoutKind.Sequential)]
readonly struct NativeMessage
{
    public readonly IntPtr Hwnd;
    public readonly uint Message;
    public readonly IntPtr WParam;
    public readonly IntPtr LParam;
    public readonly uint Time;
    public readonly int X;
    public readonly int Y;
}

static partial class NativeMethods
{
    public delegate void WinEventDelegate(
        IntPtr hWinEventHook,
        int eventType,
        IntPtr hwnd,
        int idObject,
        int idChild,
        int dwEventThread,
        int dwmsEventTime);

    [DllImport("user32.dll")]
    public static extern IntPtr SetWinEventHook(
        int eventMin,
        int eventMax,
        IntPtr hmodWinEventProc,
        WinEventDelegate lpfnWinEventProc,
        uint idProcess,
        uint idThread,
        uint dwFlags);

    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool UnhookWinEvent(IntPtr hWinEventHook);

    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool PeekMessage(out NativeMessage lpMsg, IntPtr hWnd, uint wMsgFilterMin, uint wMsgFilterMax, uint wRemoveMsg);

    [DllImport("user32.dll")]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool TranslateMessage(ref NativeMessage lpMsg);

    [DllImport("user32.dll")]
    public static extern IntPtr DispatchMessage(ref NativeMessage lpMsg);
}

static class NativeConstants
{
    public const int EventSystemForeground = 0x0003;
    public const int EventObjectNameChange = 0x800C;
    public const int EventObjectValueChange = 0x800E;
    public const uint WineventOutOfContext = 0x0000;
    public const uint WineventSkipOwnProcess = 0x0002;
}
