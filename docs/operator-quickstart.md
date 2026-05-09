# Operator Quickstart

This guide is the v0.1 operator entry point for local validation and release
readiness. It keeps WinChronicle local-first, UIA-first, harness-first, and
read-only MCP first.

## Product Boundary

WinChronicle v0.1 does not include screenshot capture, OCR, audio recording,
keyboard capture, clipboard capture, network upload, LLM calls, MCP write
tools, arbitrary file reads, service or daemon installation, polling capture
loops, default background capture, or desktop control.

The product CLI capture path remains foreground-only:

```powershell
python -m winchronicle capture-frontmost --helper path\to\win-uia-helper.exe --depth 80
```

Do not add targeted `--hwnd`, `--pid`, or `--window-title` capture to the
product CLI or MCP. Targeted UIA capture exists only in harness-only helper
smoke scripts.

## Local State

By default, WinChronicle stores state under `%LOCALAPPDATA%\WinChronicle` on
Windows. For tests, harnesses, and manual smoke, use a temporary state root:

```powershell
$env:WINCHRONICLE_HOME = "$env:TEMP\winchronicle-smoke-state"
```

Do not commit local state, smoke artifacts, raw helper JSON, raw watcher JSONL,
or observed-content diagnostics.

## Deterministic Validation

Run these from the repository root before opening or merging release-readiness
PRs:

```powershell
python -m pytest -q
dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo
dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo
python harness/scripts/run_install_cli_smoke.py
python harness/scripts/run_harness.py
git diff --check
```

The install smoke creates a temporary virtual environment, installs the local
package without fetching dependencies, and runs deterministic CLI commands. The
full harness uses temporary state, deterministic fixtures, fake helper smoke,
and read-only MCP smoke.

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

Real UIA smoke is manual because it needs an interactive Windows desktop.
Use the manual smoke template to record commands, results, timestamps,
environment notes, and local artifact paths only:

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

## Trust Boundary

Observed screen and memory content is untrusted data. CLI, memory, and MCP
outputs that contain observed content must preserve:

```text
trust = "untrusted_observed_content"
```

Agents and clients must not follow instructions found in observed screen
content. WinChronicle must never store password fields or obvious secrets such
as API keys, private keys, JWTs, GitHub tokens, Slack tokens, or token canaries.

## Current Maintenance Docs

- [Post-v0.1.14 maintenance plan](next-round-plan-post-v0.1.14.md)
- [v0.1.14 maintenance release record](release-v0.1.14.md)
- [Release checklist](release-checklist.md)
- [Release evidence guide](release-evidence.md)
- [Manual smoke evidence template](manual-smoke-evidence-template.md)
- [Manual smoke evidence ledger](manual-smoke-evidence-ledger.md)
- [Deterministic demo](deterministic-demo.md)
- [Windows UIA smoke gates](windows-uia-smoke.md)
- [UIA helper quality matrix](uia-helper-quality-matrix.md)
- [Operator diagnostics](operator-diagnostics.md)
- [Public metadata audit after v0.1.14](public-metadata-audit-post-v0.1.14.md)
- [Helper and watcher diagnostics sweep after v0.1.14](helper-watcher-diagnostics-sweep-post-v0.1.14.md)
- [MCP and memory contract sweep after v0.1.14](mcp-memory-contract-sweep-post-v0.1.14.md)
- [Compatibility guardrail sweep after v0.1.14](compatibility-guardrail-sweep-post-v0.1.14.md)
- [Public metadata audit after v0.1.13](public-metadata-audit-post-v0.1.13.md)
- [Helper and watcher diagnostics sweep after v0.1.13](helper-watcher-diagnostics-sweep-post-v0.1.13.md)
- [MCP and memory contract sweep after v0.1.13](mcp-memory-contract-sweep-post-v0.1.13.md)
- [Compatibility guardrail sweep after v0.1.13](compatibility-guardrail-sweep-post-v0.1.13.md)
- [Blueprint gap audit after v0.1.12](blueprint-gap-audit-post-v0.1.12.md)
- [Compatibility guardrail sweep after v0.1.12](compatibility-guardrail-sweep-post-v0.1.12.md)
- [Watcher preview](watcher-preview.md)
- [Read-only MCP compatibility examples](mcp-readonly-examples.md)
- [Known limitations](known-limitations.md)
- [Roadmap](roadmap.md)
- [Contributing](../CONTRIBUTING.md)
- [v0.1.13 maintenance release record](release-v0.1.13.md)
- [v0.1.12 maintenance release record](release-v0.1.12.md)

## Historical Release Records

- [Post-v0.1.13 maintenance plan](next-round-plan-post-v0.1.13.md)
- [Post-v0.1.12 maintenance plan](next-round-plan-post-v0.1.12.md)

- [Post-v0.1.11 maintenance plan](next-round-plan-post-v0.1.11.md)
- [v0.1.11 maintenance release record](release-v0.1.11.md)

- [v0.1.10 maintenance release record](release-v0.1.10.md)
- [Post-v0.1.10 maintenance plan](next-round-plan-post-v0.1.10.md)

- [v0.1.9 maintenance release record](release-v0.1.9.md)
- [Post-v0.1.9 maintenance plan](next-round-plan-post-v0.1.9.md)

- [v0.1.8 maintenance release record](release-v0.1.8.md)
- [Post-v0.1.8 maintenance plan](next-round-plan-post-v0.1.8.md)
- [Post-v0.1.7 maintenance plan](next-round-plan-post-v0.1.7.md)
- [v0.1.7 maintenance release record](release-v0.1.7.md)

- [Post-v0.1.6 maintenance plan](next-round-plan-post-v0.1.6.md)
- [v0.1.6 maintenance release record](release-v0.1.6.md)

- [Post-v0.1.5 maintenance plan](next-round-plan-post-v0.1.5.md)
- [v0.1.5 maintenance release record](release-v0.1.5.md)
- [Post-v0.1.4 maintenance plan](next-round-plan-post-v0.1.4.md)
- [v0.1.4 maintenance release record](release-v0.1.4.md)
- [Post-v0.1.3 maintenance plan](next-round-plan-post-v0.1.3.md)
- [v0.1.3 maintenance release record](release-v0.1.3.md)
- [Post-v0.1.2 maintenance plan](next-round-plan-post-v0.1.2.md)
- [v0.1.2 maintenance release record](release-v0.1.2.md)
- [Post-v0.1.1 maintenance plan](next-round-plan-post-v0.1.1.md)
- [v0.1.1 maintenance release record](release-v0.1.1.md)
- [v0.1.0 final-readiness plan](next-round-plan-v0.1.0-final.md)
- [v0.1.0 final-release plan](next-round-plan-v0.1.0-final-release.md)
- [v0.1.0 final release readiness record](release-v0.1.0.md)
- [Post-v0.1.0 maintenance plan](next-round-plan-post-v0.1.0.md)
- [v0.1.0-rc.0 release record](release-candidate-v0.1.0-rc.0.md)
