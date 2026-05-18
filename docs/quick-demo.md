# 5-Minute Demo

This demo shows the product shape without reading the live desktop. It uses
fixture captures, local temporary state, deterministic search, a finite monitor
session, and a read-only MCP smoke path.

## What You Will See

- A local WinChronicle state directory.
- Redacted fixture captures indexed into SQLite.
- A deterministic monitor session from watcher fixture events.
- A saved session JSON file and local HTML report.
- Read-only MCP tools that expose local context without write or control tools.

## Run It

From the repository root in PowerShell:

```powershell
$env:WINCHRONICLE_HOME = Join-Path $env:TEMP ("winchronicle-demo-" + [guid]::NewGuid().ToString("N"))
python -m winchronicle init
python -m winchronicle status
python -m winchronicle capture-once --fixture harness/fixtures/uia/terminal_error.json
python -m winchronicle search-captures "AssertionError"
python -m winchronicle monitor --events harness/fixtures/watcher/notepad_burst.jsonl --session-id demo
python -m winchronicle summarize-session demo
python harness/scripts/run_mcp_smoke.py
```

## Expected Shape

`status` should report local state and disabled high-risk surfaces: screenshots,
OCR, audio, keyboard capture, clipboard capture, cloud upload, LLM calls,
desktop control, product targeted capture, and MCP write tools.

`search-captures` should return a local match with:

```text
trust = "untrusted_observed_content"
```

`summarize-session demo` should read the saved local session and point to the
HTML report path under the temporary state directory.

## What This Demo Does Not Do

This demo does not start live UIA capture, install a service, run a background
daemon, poll the desktop, save raw watcher JSONL, call an LLM, upload data, or
capture screenshots, OCR, audio, keyboard input, or clipboard content.

## Clean Up

```powershell
Remove-Item -LiteralPath $env:WINCHRONICLE_HOME -Recurse -Force
Remove-Item Env:\WINCHRONICLE_HOME
```

For deeper validation, continue with [Deterministic demo](deterministic-demo.md)
and [Operator quickstart](operator-quickstart.md).
