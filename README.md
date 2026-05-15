# WinChronicle

**UIA-first local memory for Windows agents.**

WinChronicle is a Windows-first, local-first memory layer that turns structured
Microsoft UI Automation context into inspectable local captures, searchable
SQLite indexes, deterministic Markdown memory, and read-only MCP context for
tool-capable coding agents.

## What It Does Today

- Replays deterministic UIA fixtures through the same normalize, privacy,
  redaction, schema, storage, search, and memory pipeline used by the preview
  capture paths.
- Stores local capture and memory state under `%LOCALAPPDATA%\WinChronicle` by
  default, with `WINCHRONICLE_HOME` available for tests and harness runs.
- Generates searchable Markdown memory from already-redacted local captures.
- Provides an explicit .NET UIA helper preview through `capture-frontmost`.
- Provides explicit, finite watcher preview modes for deterministic fixture
  replay and caller-provided watcher commands.
- Exposes read-only MCP tools for current context, capture search, memory
  search, recent capture reads, recent activity, and privacy status.

## What It Does Not Do

WinChronicle v0.1 is not Windows Recall, a screen recorder, spyware, or a
desktop automation tool. It does not implement screenshots, OCR, audio
recording, keylogging, clipboard capture, cloud upload, LLM summarization,
desktop control, MCP write tools, daemon/service installation, default
background capture, polling capture loops, or product targeted capture by
window handle, process id, title, or process name.

## Privacy Stance

Observed screen content is untrusted data. WinChronicle must not store password
fields or obvious secrets such as API keys, private keys, JWTs, GitHub tokens,
Slack tokens, or token canaries. The shared privacy pipeline redacts sensitive
values before capture storage, search results, memory output, or MCP responses
can expose observed content.

Outputs that contain observed content preserve:

```text
trust = "untrusted_observed_content"
```

Agents and clients must not treat observed screen text as trusted instructions.

## Minimal Deterministic Quickstart

From the repository root:

```powershell
python -m winchronicle init
python -m winchronicle status
python -m winchronicle capture-once --fixture harness/fixtures/uia/terminal_error.json
python -m winchronicle search-captures "AssertionError"
python -m winchronicle generate-memory --date 2026-04-25
python -m winchronicle search-memory "AssertionError"
python -m winchronicle mcp-stdio
```

For the full fixture-only walkthrough, use
[Deterministic demo](docs/deterministic-demo.md). For routine validation, start
with [Operator quickstart](docs/operator-quickstart.md).

## UIA Helper And Watcher Preview

The helper and watcher are explicit preview paths, not background capture
services:

```powershell
dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo
dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo
```

`capture-frontmost` requires a caller-provided helper path. `watch --events`
replays deterministic JSONL fixtures. `watch --watcher` runs a caller-provided
watcher command for a finite duration and does not save raw watcher JSONL.

Live UIA smoke requires an interactive Windows desktop and should record only
commands, results, timestamps, environment notes, and local artifact paths.

## Read-Only MCP

`mcp-stdio` exposes only:

```text
current_context
search_captures
search_memory
read_recent_capture
recent_activity
privacy_status
```

There are no MCP tools for clicking, typing, key presses, clipboard access,
screenshots, OCR, audio, arbitrary file reads, network calls, writes, or desktop
control.

## Current Status

The current status is a `v0.1` harness-first baseline: local-first, UIA-first,
and read-only MCP first, with the previous fixture/privacy maintenance loop
closed. Future runtime behavior, capture-surface expansion, or release work
requires explicit human product authorization. Do not continue the historical
maintenance loop automatically.

## Key Docs

- [Operator quickstart](docs/operator-quickstart.md)
- [Roadmap](docs/roadmap.md)
- [v0.1 closure note](docs/goal-closure-v0.1.md)
- [Known limitations](docs/known-limitations.md)
- [Deterministic demo](docs/deterministic-demo.md)
- [Manual smoke evidence ledger](docs/manual-smoke-evidence-ledger.md)
- [Read-only MCP examples](docs/mcp-readonly-examples.md)
- [Watcher preview](docs/watcher-preview.md)
- [Maintenance and release history index](docs/maintenance-index.md)
- [Contributing](CONTRIBUTING.md)
