# Operator Quickstart

This guide is the v0.1 entry point for local validation. It keeps WinChronicle
local-first, UIA-first, harness-first, and read-only MCP first.

## Product Boundary

WinChronicle v0.1 does not include screenshot capture, OCR, audio recording,
keyboard capture, clipboard capture, network upload, LLM calls, MCP write
tools, arbitrary file reads, service or daemon installation, polling capture
loops, default background capture, or desktop control.

The product CLI capture path remains foreground-only:

```powershell
python -m winchronicle capture-frontmost --helper path\to\win-uia-helper.exe --depth 80
```

Do not add targeted `--hwnd`, `--pid`, `--window-title`,
`--window-title-regex`, or `--process-name` capture to the product CLI or MCP.
Targeted UIA capture exists only in harness-only helper smoke scripts.

## Local State

By default, WinChronicle stores state under `%LOCALAPPDATA%\WinChronicle` on
Windows. For tests, harnesses, and manual smoke, use a temporary state root:

```powershell
$env:WINCHRONICLE_HOME = "$env:TEMP\winchronicle-smoke-state"
```

Do not commit local state, smoke artifacts, raw helper JSON, raw watcher JSONL,
or observed-content diagnostics.

## Deterministic Validation

Run these from the repository root before opening or merging product or docs
changes:

```powershell
python -m pytest -q
python harness/scripts/run_harness.py
git diff --check
```

The full harness uses temporary state, deterministic fixtures, fake-helper
smoke, and read-only MCP smoke. It also builds the helper and watcher projects
and runs the install CLI smoke.

For a single fixture-only walkthrough that covers capture search, memory search,
watcher fixture replay, read-only MCP smoke, privacy status, and artifact
policy, use [Deterministic demo](deterministic-demo.md).

## Basic CLI Flow

Use fixture captures for deterministic operator checks:

```powershell
python -m winchronicle init
python -m winchronicle status
python -m winchronicle capture-once --fixture harness/fixtures/uia/terminal_error.json
python -m winchronicle search-captures "AssertionError"
python -m winchronicle generate-memory --date 2026-04-25
python -m winchronicle search-memory "AssertionError"
```

`status` should report screenshots, OCR, audio, keyboard capture, clipboard
capture, network/cloud upload, LLM calls, desktop control, product targeted
capture, and MCP write tools disabled. `capture-once` and memory generation
write only already-redacted fixture-derived content through the shared privacy
pipeline.

## Manual UIA Smoke

Real UIA smoke is manual because it needs an interactive Windows desktop. Use
the manual smoke template to record commands, results, timestamps, environment
notes, and local artifact paths only:

- [Manual smoke evidence template](manual-smoke-evidence-template.md)
- [Windows UIA smoke gates](windows-uia-smoke.md)

Hard or conditional gates:

- Notepad targeted smoke: hard gate.
- Edge targeted smoke: hard gate.
- VS Code metadata smoke: hard gate when `code.cmd` is available.
- VS Code strict Monaco editor marker: diagnostic and non-blocking.

Do not paste observed text, screenshots, OCR output, raw helper JSON, raw
watcher JSONL, secrets, passwords, local page contents, or editor buffer
contents into release notes or committed docs.

## Watcher Preview

The watcher is an explicit, time-bounded preview path. It is not installed as a
service, does not start by default, and does not save raw watcher JSONL.

Read [Watcher preview](watcher-preview.md) before manual watcher smoke. All
watcher events continue through the same normalize, privacy, redaction, schema,
and SQLite pipeline used by fixture and frontmost captures.

For no-capture, heartbeat-only, timeout, invalid JSON, nonzero exit, or VS Code
strict Monaco diagnostics, use [Operator diagnostics](operator-diagnostics.md).
Record stable diagnostic lines and local artifact paths only; do not paste raw
observed content.

## Read-Only MCP

`mcp-stdio` exposes only read-only context tools:

```text
current_context
search_captures
search_memory
read_recent_capture
recent_activity
privacy_status
```

See [Read-only MCP compatibility examples](mcp-readonly-examples.md) for
request and response shapes. There are no MCP tools for click, type, key press,
clipboard, screenshot, OCR, audio, arbitrary file read, network calls, writes,
or desktop control.

## Current v0.1 Docs

- [v0.1 closure note](goal-closure-v0.1.md)
- [Roadmap](roadmap.md)
- [Known limitations](known-limitations.md)
- [Maintenance and release history index](maintenance-index.md)
- [Release checklist](release-checklist.md)
- [Release evidence guide](release-evidence.md)
- [Manual smoke evidence ledger](manual-smoke-evidence-ledger.md)
- [Contributing](../CONTRIBUTING.md)
