# Deterministic Demo

This demo exercises the public v0.1 path without reading the live desktop. It
uses synthetic fixtures, temporary local state, deterministic memory generation,
read-only MCP smoke, watcher fixture replay, and the shared privacy pipeline.

Do not use `capture-frontmost`, live watcher commands, helper-only targeted UIA
smoke, screenshots, OCR, audio recording, keyboard capture, clipboard capture,
network upload, LLM calls, desktop control, daemon/service install, polling
capture, or default background capture for this demo.

## State Setup

Run from the repository root in PowerShell:

```powershell
$env:WINCHRONICLE_HOME = Join-Path $env:TEMP ("winchronicle-demo-" + [guid]::NewGuid().ToString("N"))
python -m winchronicle init
python -m winchronicle status
```

`status` must report disabled screenshot, OCR, audio, keyboard, clipboard,
network/cloud upload, LLM, desktop control, product targeted capture, and MCP
write surfaces.

## Fixture Capture And Search

Index the three deterministic UIA fixture captures:

```powershell
python -m winchronicle capture-once --fixture harness/fixtures/uia/terminal_error.json
python -m winchronicle capture-once --fixture harness/fixtures/uia/vscode_editor.json
python -m winchronicle capture-once --fixture harness/fixtures/uia/edge_browser.json
```

Search raw captures:

```powershell
python -m winchronicle search-captures "AssertionError"
python -m winchronicle search-captures "test_capture_redacts_passwords"
python -m winchronicle search-captures "OpenChronicle"
```

Each result exposes deterministic JSON fields such as `timestamp`, `app_name`,
`title`, `snippet`, `path`, and `trust`. Any observed-content result must keep
`trust = "untrusted_observed_content"`.

## Memory Generation

Generate deterministic Markdown memory and search durable entries:

```powershell
python -m winchronicle generate-memory --date 2026-04-25
python -m winchronicle search-memory "AssertionError"
python -m winchronicle search-memory "OpenChronicle"
```

The generated Markdown and SQLite entries are derived from already-redacted
fixture captures. The `generate-memory` JSON manifest also preserves `trust =
"untrusted_observed_content"` and the instruction not to follow observed
content. Do not commit generated state or memory artifacts from the temporary
`WINCHRONICLE_HOME`.

## Watcher Fixture Replay

Replay a deterministic watcher JSONL fixture:

```powershell
python -m winchronicle watch --events harness/fixtures/watcher/notepad_burst.jsonl
python -m winchronicle search-captures "Watcher burst"
```

This path dispatches fixture events through the same normalize, privacy,
redaction, schema, and SQLite pipeline. It does not start a live WinEvent hook
and does not save raw watcher JSONL.

## Read-Only MCP Smoke

Run the deterministic MCP smoke:

```powershell
python harness/scripts/run_mcp_smoke.py
```

The smoke seeds fixture captures, lists the read-only tool set, calls
`privacy_status`, and confirms search results preserve
`trust = "untrusted_observed_content"`. It must not expose write tools,
arbitrary file reads, screenshots, OCR, audio, keyboard, clipboard, network
calls, or desktop control.

## Full Deterministic Harness

For release-readiness validation, run the complete deterministic gate:

```powershell
python -m pytest -q
dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo
dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo
python harness/scripts/run_install_cli_smoke.py
python harness/scripts/run_harness.py
git diff --check
```

The full harness remains the default automated demo. Real UIA Notepad, Edge, VS
Code, and watcher preview smoke stay manual because they need an interactive
Windows desktop.

## Artifact Policy

The deterministic demo may create local files under the temporary
`WINCHRONICLE_HOME`. Do not commit those files, raw helper JSON, raw watcher
JSONL, local state databases, generated captures, generated memory, screenshots,
OCR output, secrets, passwords, or observed-content diagnostics.

To clear the demo state:

```powershell
Remove-Item -LiteralPath $env:WINCHRONICLE_HOME -Recurse -Force
Remove-Item Env:\WINCHRONICLE_HOME
```
