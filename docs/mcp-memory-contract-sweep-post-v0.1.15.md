# MCP And Memory Contract Sweep After v0.1.15

This AD3 sweep reviews read-only MCP examples, durable memory docs, and the
deterministic demo after the published `v0.1.15` baseline and AD2
helper/watcher diagnostics review. It records current evidence, one
documentation-only MCP example drift fix, and one compatible read-only MCP
filtered-search parity fix. It does not change schemas, CLI/MCP JSON shape,
MCP tool schemas, memory reducer behavior, privacy behavior, or capture
surfaces.

## Reviewed Surfaces

| Surface | Evidence | Assessment |
| --- | --- | --- |
| MCP examples | `docs/mcp-readonly-examples.md` documents `current_context`, `search_captures`, `search_memory`, `read_recent_capture`, `recent_activity`, and `privacy_status`. | Examples cover the exact read-only tool list, show `trust = "untrusted_observed_content"`, and include `privacy_status` local-state fields. |
| MCP scorecard | `harness/scorecards/mcp-quality.md` requires exact tool-list tests, read-only stdio, no write/control/file/screenshot/OCR/audio/keyboard/clipboard/network tools, trust-boundary output, and filtered search before limits. | Scorecard remains aligned with the v0.1 MCP boundary. |
| Memory scorecard | `harness/scorecards/memory-quality.md` requires deterministic Markdown, source capture paths, app names, time range, `trust: untrusted_observed_content`, idempotence, goldens, `entries` / `entries_fts`, and secret exclusion. | Scorecard remains aligned with the v0.1 durable memory contract. |
| Deterministic demo | `docs/deterministic-demo.md` covers fixture capture, raw search, memory generation/search, watcher fixture replay, MCP smoke, and artifact policy. | Demo stays fixture-only and does not read live desktop content. |
| Operator quickstart | `docs/operator-quickstart.md` lists the exact read-only MCP tools and trust boundary. | Operator entry point remains consistent with MCP examples. |
| Deterministic tests | `tests/test_mcp_tools.py`, `tests/test_memory_pipeline.py`, `tests/test_compatibility_contracts.py`, `tests/test_state_compatibility.py`, and harness smoke scripts cover exact tools, memory search, filtered MCP search beyond 50 raw matches, idempotence, empty state, and trust metadata. | AD3 added coverage for filtered MCP search parity before result limits. |

## Contract Matrix

| Contract | Current evidence | Blocking status |
| --- | --- | --- |
| Exact MCP tool list | MCP examples and `harness/scorecards/mcp-quality.md` list exactly `current_context`, `search_captures`, `search_memory`, `read_recent_capture`, `recent_activity`, and `privacy_status`; tests compare against a literal expected list. | Hard compatibility gate. |
| Read-only MCP boundary | MCP examples and scorecard reject write, arbitrary file read, click/type, clipboard, screenshot, OCR, audio, keyboard, network, desktop control, and targeted capture tools. | Hard privacy/scope gate. |
| Observed-content trust boundary | MCP examples, deterministic demo, release checklist, and tests require `trust = "untrusted_observed_content"` for observed capture and memory content. | Hard privacy gate. |
| MCP `search_memory` parity | MCP examples and scorecard state that `search_memory` reads the same SQLite memory index as CLI `search-memory`; AD3 verifies `entry_type` filters are applied before limits. | Hard compatibility gate. |
| MCP `search_captures` parity | MCP examples and scorecard state that `search_captures` reads the same SQLite capture index as CLI `search-captures`; AD3 verifies `app_name` filters are applied before limits. | Hard compatibility gate. |
| Durable memory Markdown | Memory scorecard and goldens require source capture paths, app names, time range, and trust metadata in generated Markdown. | Hard deterministic memory gate. |
| Memory FTS | Memory scorecard requires `entries` and, when FTS5 is available, `entries_fts`. | Hard deterministic storage gate. |
| Idempotent memory generation | Memory scorecard and tests require reruns over the same captures to keep stable Markdown bodies and entry count. | Hard deterministic memory gate. |
| Secret exclusion | Memory scorecard and privacy tests require generated Markdown and SQLite entries to exclude password/API key/private key/JWT/GitHub/Slack token canaries. | Hard privacy gate. |
| Fixture-only demo | Deterministic demo avoids `capture-frontmost`, live watcher commands, helper-only targeted UIA smoke, screenshots, OCR, audio, keyboard, clipboard, network upload, LLM calls, desktop control, daemon/service install, polling capture, and default background capture. | Hard demo boundary. |

## Drift Fix Decision

AD3 found no required schema, tool-list, tool-schema, memory reducer, privacy,
or capture-surface change. It found two narrow drifts:

- The `privacy_status` example omitted the existing `home`, `db_exists`, and
  `capture_count` fields returned by the implementation. AD3 updated the
  example so the documented response shape matches the read-only MCP tool
  payload, and aligned the `read_recent_capture` URL example with the public
  storage shape that returns an empty string when no URL is present.
- MCP `search_captures` and `search_memory` applied filters after a raw
  50-result fetch. AD3 moved capture and memory filters into the SQLite search
  path so valid filtered matches beyond the first 50 raw hits are not dropped.

The reviewed docs, scorecards, tests, and deterministic demo preserve exact
read-only MCP tools, stable response examples, CLI/MCP memory-search parity,
durable memory goldens, idempotence, secret exclusion, and the observed-content
trust boundary.

No fresh manual UIA smoke is required for this AD3 sweep because it changes
only read-only MCP search parity plus documentation/tests, and does not change
helper behavior, watcher product behavior, manual smoke scripts, capture
behavior, privacy behavior, product CLI/MCP shape, capture surfaces, or release
approver requirements.

The next smallest implementation task is AD4: re-run compatibility guardrails
and confirm exact MCP read-only tools, disabled privacy surfaces, product
targeted capture absence, watcher preview limits, durable memory contract, and
Phase 6 spec-only status.

## Boundary Confirmation

This sweep does not authorize MCP write tools, arbitrary file reads, screenshot
capture, OCR, audio recording, keyboard capture, clipboard capture, network
upload, LLM calls, desktop control, product targeted capture, daemon/service
install, polling capture loops, default background capture, or live UIA smoke
in default CI.
