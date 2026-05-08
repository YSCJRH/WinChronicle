# Blueprint Gap Audit After v0.1.12

This audit compares the published `v0.1.12` baseline with `WinChronicle.md`.
It records evidence and follow-up candidates only. It does not authorize new
capture surfaces, helper behavior, watcher behavior, MCP tools, screenshot/OCR
implementation, audio recording, keyboard capture, clipboard capture, network
upload, LLM calls, desktop control, daemon/service install, polling capture, or
default background capture.

## Baseline Evidence

| Surface | Evidence | Assessment |
| --- | --- | --- |
| North star and README positioning | `README.md` opens with "UIA-first local memory for Windows agents" and describes local Markdown + SQLite memory plus read-only MCP. | Matches the blueprint north star and positioning. |
| CLI command surface | `src/winchronicle/cli.py` exposes `init`, `status`, `capture-once`, `capture-frontmost`, `watch`, `privacy-check`, `search-captures`, `generate-memory`, `search-memory`, and `mcp-stdio`. | Published v0.1 surface is broader than the first-pass blueprint but remains within later approved phases. |
| Fixture capture and SQLite search | Harness fixtures and `harness/scripts/run_harness.py` cover terminal, editor, browser capture/search, privacy checks, and memory search. | Phase 1 is covered by deterministic gates. |
| UIA helper preview | `resources/win-uia-helper/` exists; product CLI only captures frontmost through an explicit helper path. Harness-only targeted smoke stays outside product CLI/MCP. | Phase 2 exists as bounded preview. |
| Watcher preview | `resources/win-uia-watcher/`, `docs/watcher-preview.md`, and watcher tests cover explicit finite-duration preview behavior. | Phase 3 exists as bounded preview, not daemonized. |
| Read-only MCP | `src/winchronicle/mcp/server.py` exposes exactly `current_context`, `search_captures`, `search_memory`, `read_recent_capture`, `recent_activity`, and `privacy_status`. | Phase 4 exists and is read-only. |
| Durable memory | `generate-memory`, `search-memory`, memory scorecards, memory fixtures, and memory tests cover deterministic Markdown + SQLite entries. | Phase 5 exists with deterministic reducer only. |
| Phase 6 boundary | `harness/scorecards/phase6-privacy-enrichment.md`, release evidence, compatibility tests, and status output keep screenshot/OCR spec-only. | Phase 6 is explicitly not implemented. |

## Gaps And Follow-up Candidates

| Area | Evidence | Gap | Recommended stage |
| --- | --- | --- | --- |
| Deterministic public demo | README, operator quickstart, and harness docs describe commands, but there is no single "run the deterministic demo" guide that maps fixture capture -> search -> memory -> MCP smoke. | Public demo path is scattered across docs. | AA2 |
| Roadmap | `WinChronicle.md` recommends roadmap/public positioning, but no dedicated `docs/roadmap.md` or equivalent public roadmap exists. | Contributors lack a compact current/future map. | AA3 |
| Issue templates | `.github/` currently contains the Windows Harness workflow but no issue templates. | Blueprint issue-template recommendations are not reflected in repo metadata. | AA3 |
| Contribution entry | README/operator docs explain use and release evidence, but there is no concise harness-first contributor entry that maps safe task classes to tests. | New contributors may not see which tasks are safe without reading multiple files. | AA3 |
| Manual smoke freshness | Manual smoke ledger accepts inherited `v0.1.0` evidence for compatible maintenance releases. | This is acceptable for unchanged helper/watcher behavior but should remain explicit in every release-readiness record. | AA4/AA5 |
| GitHub metadata/social surface | `WinChronicle.md` suggests description/topics/social-card language; repository metadata cannot be fully verified from local files. | Keep as manual release/maintainer checklist, not a code change. | AA3 |

## Non-gaps

- The absence of screenshot/OCR implementation is intentional, not a gap for
  this round.
- The absence of audio, keyboard, clipboard, network upload, LLM calls, MCP
  write tools, arbitrary file reads, and desktop control is intentional.
- The absence of product targeted capture flags is intentional; targeted UIA
  capture remains helper-only harness smoke.
- VS Code Monaco strict editor-marker capture remains diagnostic because
  standard UIA may not expose Monaco buffer text.

## Decision

AA1 finds no required product-code change before continuing. The next smallest
implementation task is AA2: consolidate deterministic demo/operator
instructions around existing fixture and harness paths, without adding live UIA
smoke to default CI and without committing observed-content artifacts.
