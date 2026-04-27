# Windows UIA Smoke Gates

WinChronicle uses three UIA validation layers. They serve different purposes
and have different release meanings.

## 1. Deterministic Fixture Tests

Fixture tests are the default automated baseline. They use JSON fixtures under
`harness/fixtures/` and never read the live desktop.

Hard expectations:

- normalized captures validate against schemas;
- privacy gates redact password fields and obvious secrets;
- SQLite capture and memory search remain deterministic;
- screenshots, OCR, audio, keyboard capture, clipboard capture, network calls,
  LLM calls, and desktop control stay absent.

These tests are part of `python -m pytest -q` and
`python harness/scripts/run_harness.py`.

## 2. Harness-Only Targeted Real UIA Smoke

Targeted smoke is for Phase 2 release validation on an interactive Windows
machine. It calls the Windows helper directly:

```powershell
.\harness\scripts\smoke-uia-notepad.ps1
.\harness\scripts\smoke-uia-edge.ps1
.\harness\scripts\smoke-uia-vscode.ps1
.\harness\scripts\smoke-uia-vscode.ps1 -Strict
```

These scripts set `WINCHRONICLE_HARNESS=1` and use only:

```powershell
win-uia-helper capture --harness ... --no-store
```

Targeted capture is helper-only. It must not be exposed through the Python
product CLI or MCP. The scripts do not activate, click, type, move, resize, or
control windows.

Phase 2 hard gates:

- Notepad targeted smoke must pass and capture the unique text marker.
- Edge targeted smoke must pass and capture the local HTML body marker.
- VS Code metadata smoke must pass when `code.cmd` is available.

Diagnostic, non-blocking gate:

- VS Code strict Monaco editor marker capture is diagnostic only. If strict mode
  fails, keep the emitted artifact for investigation, but it is not a v0.1
  release blocker.

## 3. Manual Frontmost Smoke

Manual frontmost smoke exercises the product-shaped foreground path:

```powershell
python harness/scripts/run_uia_helper_smoke.py --helper path\to\win-uia-helper.exe --delay-seconds 5 --expect-app Notepad --expect-text "some visible text"
```

This remains useful for checking `GetForegroundWindow` behavior, but it is not
the primary app-specific Phase 2 gate because foreground focus is unreliable in
some agent-hosted desktop environments.

## Product Boundary

`python -m winchronicle capture-frontmost` must continue to capture only
`GetForegroundWindow`. Do not add `--hwnd`, `--pid`, or `--window-title` to the
product CLI or MCP. Do not add screenshot, OCR, audio, keyboard capture,
clipboard capture, network calls, LLM calls, or desktop control to pass smoke.
