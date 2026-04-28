# WinChronicle

**UIA-first local memory for Windows agents.**

WinChronicle is an OpenChronicle-compatible, local-first memory layer for Windows
agents. It captures structured app context through Microsoft UI Automation,
turns it into inspectable Markdown + SQLite memory, and exposes read-only
context through MCP for Codex, Claude Code, Cursor, opencode, and other
tool-capable agents.

This repository remains harness-first: deterministic fixtures, schemas, tests,
and privacy gates define behavior, while explicit foreground UIA helper and
watcher preview paths stay bounded by the same harness contracts.

For release-candidate operation, start with
[`docs/operator-quickstart.md`](docs/operator-quickstart.md). It links the
release checklist, manual smoke evidence template, Windows UIA smoke gates,
watcher preview, read-only MCP examples, known limitations, and current
final-readiness plan.

## Why WinChronicle

- **UIA-first**: structured Windows UI context before screenshots or OCR.
- **Local-first**: captured context stays on the user's machine by default.
- **Agent-readable**: the project is designed for read-only MCP context tools.
- **Inspectable**: memory should be stored as human-reviewable local artifacts.
- **Harness-first**: fixtures, schemas, scorecards, and tests define behavior
  before capture integrations are added.

## What this is not

WinChronicle is not a Windows Recall clone, not a screen recorder, not spyware,
and not a desktop automation or control tool.

In v0.1:

- Screenshots are off by default.
- OCR is off by default.
- Audio recording is not implemented.
- Keylogging is not implemented.
- Clipboard capture is not implemented.
- Cloud upload of captured content is not implemented.
- Desktop control tools are not implemented.
- Real Windows UIA capture is limited to an experimental helper; the default
  CLI remains harness-first and fixture-driven.
- LLM summarization is not implemented.

## Privacy stance

Observed screen content is treated as untrusted data. WinChronicle must not store
password fields or obvious secrets such as API keys, private keys, JWTs, GitHub
tokens, Slack tokens, or test canaries. Privacy gates run before captures are
written.

The shared capture pipeline redacts sensitive values, skips denylisted apps,
and marks normalized observed content with `untrusted_observed_content: true`.
CLI search results, MCP responses, and memory outputs that expose observed
content must preserve `trust = "untrusted_observed_content"` and must not treat
observed text as trusted instructions.

## Current CLI

From the repository root:

```powershell
python -m winchronicle init
python -m winchronicle status
python -m winchronicle capture-once --fixture harness/fixtures/uia/notepad_basic.json
python -m winchronicle capture-frontmost --helper path\to\win-uia-helper.exe --depth 80
python -m winchronicle watch --events harness/fixtures/watcher/notepad_burst.jsonl
python -m winchronicle watch --watcher path\to\win-uia-watcher.exe --helper path\to\win-uia-helper.exe --duration 30
python -m winchronicle privacy-check harness/fixtures/privacy/secrets_visible_text.json
python -m winchronicle search-captures "hello"
python -m winchronicle generate-memory --date 2026-04-25
python -m winchronicle search-memory "OpenChronicle"
python -m winchronicle mcp-stdio
```

State is stored in `%LOCALAPPDATA%\WinChronicle` on Windows. Tests and local
harness runs can override this with `WINCHRONICLE_HOME`.

The experimental .NET UIA helper contract can be compiled with:

```powershell
dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj
```

`capture-frontmost` is explicit opt-in and requires a helper path. It does not
enable screenshots, OCR, audio, keyboard capture, clipboard capture, network
calls, or desktop control.

`watch --events` is a deterministic harness mode for JSONL watcher fixtures. It
does not start a real WinEvent hook.
`watch --watcher` is explicit opt-in and runs a caller-provided watcher command;
its JSONL stream is consumed in memory and not saved as a raw event log.

The experimental WinEvent watcher scaffold can be compiled with:

```powershell
dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj
```

The watcher emits JSONL and can invoke the UIA helper for foreground captures,
but automated harness runs only compile it; they do not start a live watcher.
The harness smoke uses `--capture-on-start` with a fake helper so it exercises
watcher JSONL without reading live UI content.
See `docs/watcher-preview.md` for the v0.1 preview boundary and manual smoke
expectations.

`mcp-stdio` exposes a minimal read-only MCP stdio surface for
`current_context`, `search_captures`, `read_recent_capture`,
`search_memory`, `recent_activity`, and `privacy_status`. Every
observed-content response is marked with
`trust = "untrusted_observed_content"` and no desktop control, screenshot,
OCR, audio, keyboard, clipboard, or network tool is exposed.

`generate-memory` creates deterministic event, project, and tool Markdown
entries from already-redacted local captures and indexes them in SQLite
`entries` / `entries_fts`.
`search-memory` searches those durable entries; raw capture search remains
available through `search-captures`.

## Operator Docs

- [Operator quickstart](docs/operator-quickstart.md)
- [Release checklist](docs/release-checklist.md)
- [Release evidence guide](docs/release-evidence.md)
- [Manual smoke evidence template](docs/manual-smoke-evidence-template.md)
- [Windows UIA smoke gates](docs/windows-uia-smoke.md)
- [Watcher preview](docs/watcher-preview.md)
- [Read-only MCP examples](docs/mcp-readonly-examples.md)
- [Known limitations](docs/known-limitations.md)
- [v0.1.0 final-readiness plan](docs/next-round-plan-v0.1.0-final.md)
- [v0.1.0-rc.0 release record](docs/release-candidate-v0.1.0-rc.0.md)

Screenshot/OCR enrichment remains a future tests-first phase; the current Phase
6 privacy scorecard is only a planning contract and does not enable either
surface.

## Competitive positioning

Many adjacent tools focus on screenshot timelines, OCR search, screen replay, or
desktop automation. WinChronicle is intentionally narrower: it is an agent memory
layer for Windows, using UI Automation as the primary signal, with read-only MCP
as the first integration target and privacy gates as a project contract.
