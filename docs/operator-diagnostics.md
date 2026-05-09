# Operator Diagnostics

This guide is for post-v0.1 operator triage when live UIA helper or watcher
smoke does not produce a capture. It describes stable diagnostic signals only.
Do not paste observed text, raw helper JSON, raw watcher JSONL, screenshots,
OCR output, local page contents, editor buffer contents, passwords, or secrets
into issues, PRs, release notes, or committed docs.

Record only:

- command;
- exit code;
- one stable diagnostic line;
- timestamp;
- environment notes;
- local artifact path when a smoke script already created one.

Use a temporary state root for all live diagnostics:

```powershell
$env:WINCHRONICLE_HOME = "$env:TEMP\winchronicle-diagnostics-state"
```

## Frontmost Helper Diagnostics

`capture-frontmost` is the product-shaped live capture path. It only captures
the current foreground window through the caller-provided helper.

```powershell
python -m winchronicle capture-frontmost --helper path\to\win-uia-helper.exe --depth 80
```

Expected operator signals:

| Scenario | Stable signal | Meaning | What to record |
| --- | --- | --- | --- |
| Helper returns no stdout | `SKIPPED: helper returned no capture` | The helper did not find a capturable foreground target. This can happen in hosted desktops or when no accessible foreground window is available. | Command, timestamp, environment, and `WINCHRONICLE_HOME`. |
| Helper times out | `ERROR: helper timed out` | UIA traversal or process startup exceeded the wrapper timeout. | Command, timeout context, and environment notes. |
| Helper returns malformed JSON | `ERROR: helper returned invalid JSON` | The wrapper failed closed and did not store or print helper output. | Command and helper version/build notes. |
| Helper exits nonzero | `ERROR: helper failed with exit code <code>` | The helper failed before producing an accepted capture. | Exit code and helper build notes. |
| Unexpected wrapper failure | `ERROR: helper output could not be captured safely` | The wrapper suppressed raw output because it may contain observed content. | Command and reproduction notes only. |

Never work around a no-capture or timeout by adding product `--hwnd`, `--pid`,
`--window-title`, `--window-title-regex`, or `--process-name` flags.
Targeted capture remains helper-only harness smoke.

## Watcher Preview Diagnostics

The watcher preview is explicit, time-bounded, and operator-started.

```powershell
python -m winchronicle watch --watcher path\to\win-uia-watcher.exe --helper path\to\win-uia-helper.exe --duration 30
```

Expected operator signals:

| Scenario | Stable signal | Meaning | What to record |
| --- | --- | --- | --- |
| Heartbeat-only live run | JSON with `captures_written: 0` and `heartbeats > 0` | The watcher was alive, but no capturable event produced a persisted capture. This is diagnostic liveness evidence, not a hard failure by itself. | JSON counts, command, duration, and environment notes. |
| Watcher exits nonzero | `ERROR: watcher failed with exit code <code>` | The watcher or surfaced helper path failed. Raw stdout/stderr is suppressed. | Exit code and command. |
| Watcher emits malformed JSONL | `ERROR: watcher JSONL line <n> is malformed` | The dispatcher rejected an event line without saving raw JSONL. | Line number and command. |
| Watcher emits an invalid helper payload | `ERROR: watcher output could not be captured safely` | The dispatcher failed closed because validation details may include observed content. | Command and reproduction notes only; do not record schema output or payload text. |
| Watcher timeout | `ERROR: watcher timed out` | The watcher command exceeded the wrapper timeout. | Command, duration, and environment notes. |
| Denylist or lock screen skip | JSON with `denylisted_skipped > 0` and unchanged `captures_written` | Privacy gate skipped observed content before storage. Title-denylist diagnostics use a stable content-free reason. | JSON counts only; do not record the matched title. |
| Duplicate skip | JSON with `duplicates_skipped > 0` | Content fingerprint prevented duplicate persistence. | JSON counts only. |

Do not save or commit raw watcher JSONL from live runs. The Python preview path
consumes watcher JSONL in memory.

## VS Code Monaco Diagnostic

VS Code metadata smoke is the conditional hard gate when `code.cmd` is
available. Strict Monaco editor marker capture is diagnostic and non-blocking.

```powershell
powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1
powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -Strict
```

If strict mode fails with a message that the editor marker was not exposed
through UIA, record the local artifact path only. Do not introduce screenshots,
OCR, keyboard capture, clipboard capture, desktop control, or a bundled VS Code
extension as a workaround.

## Boundary Checklist

Diagnostics must not add or imply:

- screenshot capture;
- OCR;
- audio recording;
- keyboard capture or keylogging;
- clipboard capture;
- network upload;
- LLM calls;
- desktop control;
- product targeted capture flags;
- daemon or service install;
- polling capture loops;
- default background capture.
