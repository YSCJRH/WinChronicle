# Roadmap

This roadmap describes the current v0.1 baseline and the human-approved
directions available after closure of the previous maintenance loop. It does
not authorize new capture surfaces or product behavior by itself.

## Current Stable Baseline

WinChronicle remains local-first, UIA-first, harness-first, and read-only MCP
first. The current stable baseline is the `v0.1` harness-first baseline in this
repository. The fixture/privacy maintenance loop that followed `v0.1.18` is
closed for now; its evidence remains available through the
[maintenance index](maintenance-index.md) and the
[v0.1 closure note](goal-closure-v0.1.md). This roadmap does not start a new
release-readiness path or maintenance cursor.

The baseline includes deterministic fixture capture, privacy gates, redaction,
SQLite capture search, deterministic Markdown memory, read-only MCP examples,
an explicit UIA helper preview, and explicit finite watcher preview paths.

## Closed For Automatic Continuation

The previous public metadata, helper/watcher diagnostics, MCP/memory contract,
compatibility, fixture/privacy parity, residual gap, release-readiness, release,
and publication reconciliation work is complete for this goal run. Do not turn
those records into another autonomous maintenance loop.

Any future runtime behavior, capture-surface expansion, release path, manual
smoke refresh, or broad evidence sweep needs explicit human product approval
before work starts.

## Future Product Directions

These are options for human review, not an automatically authorized backlog.

| Direction | Current baseline | Requires human approval before |
| --- | --- | --- |
| Fixture and privacy baseline | Deterministic fixtures, schema validation, privacy gates, SQLite search, and scorecards are covered by tests. | New broad parity matrices, residual gap audits, or release-readiness loops. |
| UIA helper hardening | `capture-frontmost` is explicit opt-in; targeted UIA remains helper-only harness smoke. | Product targeted capture flags, window control, or helper behavior changes. |
| Watcher preview | Watcher use is explicit, finite-duration, and preview-only. Deterministic watcher fixtures and fake-helper smoke are covered. | Daemon/service install, default background capture, polling loops, or broader watcher capture. |
| Read-only MCP | MCP exposes only `current_context`, `search_captures`, `search_memory`, `read_recent_capture`, `recent_activity`, and `privacy_status`. | MCP write tools, arbitrary file reads, desktop control, screenshot/OCR/audio/keyboard/clipboard/network tools, or response-contract changes. |
| Durable memory | Deterministic Markdown memory and `entries` / `entries_fts` search are implemented with goldens. | LLM reducer/classifier calls, network upload, or new memory output contracts. |
| Screenshot/OCR enrichment | Not implemented in v0.1. | Any screenshot or OCR implementation, artifact storage, privacy policy change, or UI exposure. |

## Issue Routing

Before implementation, classify any new work as one of:

- Harness-first task: deterministic fixtures, tests, docs, scorecards, CI, or
  compatible metadata inside the current baseline.
- Privacy boundary review: any proposal touching capture surfaces, observed
  content, storage, MCP output, memory output, or release evidence.
- Human product decision: any runtime expansion, new capture surface, release
  path, or continuation of the closed maintenance loop.

Every implementation issue should identify the expected validation commands and
whether fresh manual UIA smoke is required. Fresh manual UIA smoke is required
only when helper behavior, watcher product behavior, manual smoke scripts,
capture behavior, privacy behavior, product CLI/MCP shape, capture surfaces, or
release approver requirements change.

## Definition Of Done

- Contracts, fixtures, tests, scorecards, or documentation are updated before
  behavior changes.
- `python -m pytest -q`, `python harness/scripts/run_harness.py`, and
  `git diff --check` pass unless the issue documents why a narrower validation
  set is sufficient.
- Product CLI and MCP boundaries remain unchanged unless an explicit
  human-approved product plan allows a compatible contract change.
- Do not commit generated state, captures, memory artifacts, screenshots, OCR
  output, raw helper JSON, raw watcher JSONL, local state, secrets, passwords,
  or observed-content diagnostics.
