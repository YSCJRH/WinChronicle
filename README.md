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

For current maintenance operation, start with
[`docs/operator-quickstart.md`](docs/operator-quickstart.md). It links the
release checklist, manual smoke evidence template, Windows UIA smoke gates,
watcher preview, read-only MCP examples, known limitations, the active
post-v0.1.17 maintenance plan, the completed post-v0.1.17 public metadata
audit, the completed post-v0.1.17 helper/watcher diagnostics sweep, the completed
post-v0.1.17 MCP/memory contract sweep, the completed post-v0.1.17 compatibility
guardrail sweep, the completed post-v0.1.17 release-readiness decision, the
completed Phase 6 privacy contract preflight, the completed Phase 6 privacy
contract fixture expansion, the completed Phase 6 remaining negative contract
fixture expansion, the completed Phase 6 contract coverage audit, the completed
Phase 6 contract gap fixture expansion, the completed Phase 6 residual schema
coverage audit, the completed Phase 6 residual policy fixture expansion, the
completed Phase 6 deferred fixture closure, the completed Phase 6 contract
closure release-readiness decision, the completed next blueprint lane
selection, the completed privacy-policy contract parity audit, the
completed privacy-check release-readiness decision, the
completed post-v0.1.16 maintenance plan and publication reconciliation, the
latest published `v0.1.17` release record, the previous published `v0.1.16`
release record, the completed `v0.1.16` final-release plan, the historical
`v0.1.16-rc.0` release-candidate record, the previous published `v0.1.15`
release record, and older completed maintenance plans.

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
`current_context`, `search_captures`, `search_memory`,
`read_recent_capture`, `recent_activity`, and `privacy_status`. Every
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
- [Post-v0.1.17 maintenance plan](docs/next-round-plan-post-v0.1.17.md)
- [Public metadata audit after v0.1.17](docs/public-metadata-audit-post-v0.1.17.md)
- [Helper and watcher diagnostics sweep after v0.1.17](docs/helper-watcher-diagnostics-sweep-post-v0.1.17.md)
- [MCP and memory contract sweep after v0.1.17](docs/mcp-memory-contract-sweep-post-v0.1.17.md)
- [Compatibility guardrail sweep after v0.1.17](docs/compatibility-guardrail-sweep-post-v0.1.17.md)
- [Release-readiness decision after v0.1.17](docs/release-readiness-decision-post-v0.1.17.md)
- [Phase 6 privacy contract preflight after v0.1.17](docs/phase6-privacy-contract-preflight-post-v0.1.17.md)
- [Phase 6 privacy contract fixture expansion after v0.1.17](docs/phase6-privacy-contract-fixture-expansion-post-v0.1.17.md)
- [Phase 6 privacy contract remaining fixtures after v0.1.17](docs/phase6-privacy-contract-remaining-fixtures-post-v0.1.17.md)
- [Phase 6 privacy contract coverage audit after v0.1.17](docs/phase6-privacy-contract-coverage-audit-post-v0.1.17.md)
- [Phase 6 privacy contract gap fixtures after v0.1.17](docs/phase6-privacy-contract-gap-fixtures-post-v0.1.17.md)
- [Phase 6 privacy contract residual schema coverage audit after v0.1.17](docs/phase6-privacy-contract-residual-schema-coverage-audit-post-v0.1.17.md)
- [Phase 6 privacy contract residual policy fixtures after v0.1.17](docs/phase6-privacy-contract-residual-policy-fixtures-post-v0.1.17.md)
- [Phase 6 privacy contract deferred fixture closure after v0.1.17](docs/phase6-privacy-contract-deferred-fixture-closure-post-v0.1.17.md)
- [Phase 6 contract closure release-readiness decision after v0.1.17](docs/phase6-contract-closure-release-readiness-decision-post-v0.1.17.md)
- [Next blueprint lane selection after v0.1.17](docs/next-blueprint-lane-selection-post-v0.1.17.md)
- [Privacy-policy contract parity audit after v0.1.17](docs/privacy-policy-contract-parity-audit-post-v0.1.17.md)
- [Privacy-check release-readiness decision after v0.1.17](docs/privacy-check-release-readiness-decision-post-v0.1.17.md)
- [Post-v0.1.16 maintenance plan](docs/next-round-plan-post-v0.1.16.md)
- [Public metadata audit after v0.1.16](docs/public-metadata-audit-post-v0.1.16.md)
- [Helper and watcher diagnostics sweep after v0.1.16](docs/helper-watcher-diagnostics-sweep-post-v0.1.16.md)
- [MCP and memory contract sweep after v0.1.16](docs/mcp-memory-contract-sweep-post-v0.1.16.md)
- [Compatibility guardrail sweep after v0.1.16](docs/compatibility-guardrail-sweep-post-v0.1.16.md)
- [Release-readiness decision after v0.1.16](docs/release-readiness-decision-post-v0.1.16.md)
- [v0.1.17 maintenance release record](docs/release-v0.1.17.md)
- [v0.1.16 final release record](docs/release-v0.1.16.md)
- [v0.1.16 final-release plan](docs/next-round-plan-v0.1.16-final-release.md)
- [Post-v0.1.15 maintenance plan](docs/next-round-plan-post-v0.1.15.md)
- [v0.1.16-rc.0 release candidate record](docs/release-candidate-v0.1.16-rc.0.md)
- [Post-v0.1.14 maintenance plan](docs/next-round-plan-post-v0.1.14.md)
- [v0.1.15 maintenance release record](docs/release-v0.1.15.md)
- [v0.1.14 maintenance release record](docs/release-v0.1.14.md)
- [Release checklist](docs/release-checklist.md)
- [Release evidence guide](docs/release-evidence.md)
- [Manual smoke evidence template](docs/manual-smoke-evidence-template.md)
- [Manual smoke evidence ledger](docs/manual-smoke-evidence-ledger.md)
- [Deterministic demo](docs/deterministic-demo.md)
- [Windows UIA smoke gates](docs/windows-uia-smoke.md)
- [Operator diagnostics](docs/operator-diagnostics.md)
- [Public metadata audit after v0.1.15](docs/public-metadata-audit-post-v0.1.15.md)
- [Helper and watcher diagnostics sweep after v0.1.15](docs/helper-watcher-diagnostics-sweep-post-v0.1.15.md)
- [MCP and memory contract sweep after v0.1.15](docs/mcp-memory-contract-sweep-post-v0.1.15.md)
- [Compatibility guardrail sweep after v0.1.15](docs/compatibility-guardrail-sweep-post-v0.1.15.md)
- [Public metadata audit after v0.1.14](docs/public-metadata-audit-post-v0.1.14.md)
- [Helper and watcher diagnostics sweep after v0.1.14](docs/helper-watcher-diagnostics-sweep-post-v0.1.14.md)
- [MCP and memory contract sweep after v0.1.14](docs/mcp-memory-contract-sweep-post-v0.1.14.md)
- [Compatibility guardrail sweep after v0.1.14](docs/compatibility-guardrail-sweep-post-v0.1.14.md)
- [Public metadata audit after v0.1.13](docs/public-metadata-audit-post-v0.1.13.md)
- [Helper and watcher diagnostics sweep after v0.1.13](docs/helper-watcher-diagnostics-sweep-post-v0.1.13.md)
- [MCP and memory contract sweep after v0.1.13](docs/mcp-memory-contract-sweep-post-v0.1.13.md)
- [Compatibility guardrail sweep after v0.1.13](docs/compatibility-guardrail-sweep-post-v0.1.13.md)
- [Blueprint gap audit after v0.1.12](docs/blueprint-gap-audit-post-v0.1.12.md)
- [Compatibility guardrail sweep after v0.1.12](docs/compatibility-guardrail-sweep-post-v0.1.12.md)
- [Watcher preview](docs/watcher-preview.md)
- [Read-only MCP examples](docs/mcp-readonly-examples.md)
- [Known limitations](docs/known-limitations.md)
- [Roadmap](docs/roadmap.md)
- [Contributing](CONTRIBUTING.md)
- [Post-v0.1.13 maintenance plan](docs/next-round-plan-post-v0.1.13.md)
- [v0.1.13 maintenance release record](docs/release-v0.1.13.md)
- [v0.1.12 maintenance release record](docs/release-v0.1.12.md)
- [Post-v0.1.12 maintenance plan](docs/next-round-plan-post-v0.1.12.md)
- [Post-v0.1.11 maintenance plan](docs/next-round-plan-post-v0.1.11.md)
- [v0.1.11 maintenance release record](docs/release-v0.1.11.md)
- [v0.1.10 maintenance release record](docs/release-v0.1.10.md)
- [Post-v0.1.10 maintenance plan](docs/next-round-plan-post-v0.1.10.md)
- [v0.1.9 maintenance release record](docs/release-v0.1.9.md)
- [Post-v0.1.9 maintenance plan](docs/next-round-plan-post-v0.1.9.md)
- [v0.1.8 maintenance release record](docs/release-v0.1.8.md)
- [Post-v0.1.8 maintenance plan](docs/next-round-plan-post-v0.1.8.md)
- [Post-v0.1.7 maintenance plan](docs/next-round-plan-post-v0.1.7.md)
- [v0.1.7 maintenance release record](docs/release-v0.1.7.md)
- [Post-v0.1.6 maintenance plan](docs/next-round-plan-post-v0.1.6.md)
- [v0.1.6 maintenance release record](docs/release-v0.1.6.md)
- [Post-v0.1.5 maintenance plan](docs/next-round-plan-post-v0.1.5.md)
- [v0.1.5 maintenance release record](docs/release-v0.1.5.md)
- [Post-v0.1.4 maintenance plan](docs/next-round-plan-post-v0.1.4.md)
- [v0.1.4 maintenance release record](docs/release-v0.1.4.md)
- [v0.1.3 maintenance release record](docs/release-v0.1.3.md)
- [Post-v0.1.3 maintenance plan](docs/next-round-plan-post-v0.1.3.md)
- [Post-v0.1.2 maintenance plan](docs/next-round-plan-post-v0.1.2.md)
- [Post-v0.1.1 maintenance plan](docs/next-round-plan-post-v0.1.1.md)
- [v0.1.2 maintenance release record](docs/release-v0.1.2.md)
- [v0.1.1 maintenance release record](docs/release-v0.1.1.md)
- [v0.1.0 final-readiness plan](docs/next-round-plan-v0.1.0-final.md)
- [v0.1.0 final-release plan](docs/next-round-plan-v0.1.0-final-release.md)
- [v0.1.0 final release readiness record](docs/release-v0.1.0.md)
- [Post-v0.1.0 maintenance plan](docs/next-round-plan-post-v0.1.0.md)
- [v0.1.0-rc.0 release record](docs/release-candidate-v0.1.0-rc.0.md)

Screenshot/OCR enrichment remains a future tests-first phase; the current Phase
6 privacy scorecard is only a planning contract and does not enable either
surface.

## Competitive positioning

Many adjacent tools focus on screenshot timelines, OCR search, screen replay, or
desktop automation. WinChronicle is intentionally narrower: it is an agent memory
layer for Windows, using UI Automation as the primary signal, with read-only MCP
as the first integration target and privacy gates as a project contract.
