# 5-Minute Demo

This fixture-only demo shows the product shape. It does not read the live
desktop and does not upload content. It uses fixture captures, a deterministic
fake UIA helper, local temporary state, deterministic search, a finite monitor
session, and a read-only MCP smoke path.

## What You Will See

- A local WinChronicle state directory.
- Redacted fixture captures indexed into SQLite.
- A deterministic `capture-frontmost` path backed by `fake_uia_helper.py`.
- A finite monitor session from deterministic watcher/helper output.
- A saved session JSON file and local HTML report.
- Read-only MCP tools that expose local context without write or control tools.

MCP output is local evidence, not permission to publish or share results.
External sharing still requires explicit user approval.

## Run It

From the repository root in PowerShell:

```powershell
python -m pip install -e ".[dev]"
$env:WINCHRONICLE_HOME = Join-Path $env:TEMP ("winchronicle-demo-" + [guid]::NewGuid().ToString("N"))
winchronicle init
winchronicle status
winchronicle doctor
winchronicle capture-once --fixture harness/fixtures/uia/terminal_error.json
winchronicle search-captures "AssertionError"
winchronicle capture-frontmost --helper python --helper-arg harness/scripts/fake_uia_helper.py --depth 2
winchronicle search-captures "helper contract"
winchronicle monitor --events harness/fixtures/watcher/notepad_burst.jsonl --session-id demo
winchronicle summarize-session demo
python harness/scripts/run_mcp_smoke.py
```

Source checkouts can use `python -m winchronicle ...` as a fallback for every
`winchronicle ...` command.

To run the same bounded path as a single deterministic smoke:

```powershell
dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo
dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo
python harness/scripts/run_quick_demo.py
```

The fake-helper step simulates frontmost capture by returning
`harness/fixtures/uia-helper/notepad_frontmost.json`. It does not read the real
desktop, inspect open windows, take screenshots, use OCR, read the clipboard,
or collect keyboard input.

## Expected Shape

`status` should report local state and disabled high-risk surfaces: screenshots,
OCR, audio, keyboard capture, clipboard capture, cloud upload, LLM calls,
desktop control, product targeted capture, and MCP write tools.

`doctor` should report JSON checks for Python, SQLite, `.NET` availability,
helper/watcher build outputs, and disabled privacy surfaces. Missing helper
build outputs are reported as check failures, not as observed-content capture.

`search-captures` should return a local match with:

```text
trust = "untrusted_observed_content"
```

`capture-frontmost` in this demo should write a local capture from the
deterministic fake helper, and `summarize-session demo` should read the saved
local session and point to the HTML report path under the temporary state
directory.

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
