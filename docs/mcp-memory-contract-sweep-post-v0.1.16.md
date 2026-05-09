# MCP And Memory Contract Sweep After v0.1.16

This AF3 sweep reviews read-only MCP examples, durable memory docs, scorecards,
and deterministic demo guidance after the published `v0.1.16` final release
and AF2 completion reconciliation. It records current evidence plus two
compatible trust-boundary guardrail fixes: `generate-memory` manifest JSON now
marks observed-derived metadata as untrusted, and the standalone MCP smoke now
uses a literal expected tool list plus the full forbidden-term set. It does not
change schemas, MCP tool list, MCP tool schemas, memory Markdown reducer
behavior, SQLite storage schema, privacy behavior, helper or watcher behavior,
or capture surfaces.

## Reviewed Surfaces

| Surface | Evidence | Assessment |
| --- | --- | --- |
| MCP examples | `docs/mcp-readonly-examples.md` documents `current_context`, `search_captures`, `search_memory`, `read_recent_capture`, `recent_activity`, and `privacy_status`. | Examples still cover the exact read-only tool list, `trust = "untrusted_observed_content"`, and `privacy_status` local-state fields. |
| MCP scorecard | `harness/scorecards/mcp-quality.md` requires exact tool-list tests, read-only stdio, no write/control/file/screenshot/OCR/audio/keyboard/clipboard/network tools, trust-boundary output, and filtered search before limits. | Scorecard remains aligned with the v0.1 MCP boundary. AF3 strengthens deterministic stdio and smoke evidence for the forbidden tool-name set. |
| Memory scorecard | `harness/scorecards/memory-quality.md` requires deterministic Markdown, source capture paths, app names, time range, `trust: untrusted_observed_content`, idempotence, goldens, `entries` / `entries_fts`, and secret exclusion. | Scorecard remains aligned with the v0.1 durable memory contract. AF3 adds the same trust boundary to the generated manifest JSON summary. |
| Deterministic demo | `docs/deterministic-demo.md` covers fixture capture, raw search, memory generation/search, watcher fixture replay, MCP smoke, and artifact policy. | Demo stays fixture-only and does not read live desktop content. |
| Operator quickstart | `docs/operator-quickstart.md` lists the exact read-only MCP tools and trust boundary for CLI, memory, and MCP outputs. | Operator entry point remains consistent with MCP examples and now links this AF3 sweep. |
| Deterministic tests | `tests/test_mcp_tools.py`, `tests/test_memory_pipeline.py`, `tests/test_compatibility_contracts.py`, `tests/test_state_compatibility.py`, `harness/scripts/run_mcp_smoke.py`, and `harness/scripts/run_install_cli_smoke.py` cover exact tools, memory manifests, memory search, filtered MCP search, idempotence, empty state, and trust metadata. | AF3 added coverage for `generate-memory` manifest trust fields, more forbidden MCP call names, and standalone smoke literal tool-list enforcement. |

## Contract Matrix

| Contract | Current evidence | Blocking status |
| --- | --- | --- |
| Exact MCP tool list | MCP examples, `harness/scorecards/mcp-quality.md`, `tests/test_mcp_tools.py`, and `harness/scripts/run_mcp_smoke.py` list exactly `current_context`, `search_captures`, `search_memory`, `read_recent_capture`, `recent_activity`, and `privacy_status`. | Hard compatibility gate. |
| Read-only MCP boundary | MCP examples, scorecard, stdio tests, and smoke checks reject or forbid write, arbitrary file read, click/type, clipboard, screenshot, OCR, audio, keyboard, network, desktop control, and targeted capture tool names. | Hard privacy/scope gate. |
| Observed-content trust boundary | MCP examples, deterministic demo, release checklist, tests, and `generate-memory` manifest output require `trust = "untrusted_observed_content"` plus an instruction not to follow observed content. | Hard privacy gate. |
| MCP `search_memory` parity | MCP examples and scorecard state that `search_memory` reads the same SQLite memory index as CLI `search-memory`, with `entry_type` filters applied before limits. | Hard compatibility gate. |
| MCP `search_captures` parity | MCP examples and scorecard state that `search_captures` reads the same SQLite capture index as CLI `search-captures`, with `app_name` filters applied before limits. | Hard compatibility gate. |
| Durable memory Markdown | Memory scorecard and goldens require source capture paths, app names, time range, and trust metadata in generated Markdown. | Hard deterministic memory gate. |
| Memory manifest JSON | `MemoryGenerationResult.to_json()`, memory manifest golden, CLI tests, and install smoke require `trust`, `untrusted_observed_content`, and `instruction` on generated memory summaries. | Hard privacy gate. |
| Memory FTS | Memory scorecard requires `entries` and, when FTS5 is available, `entries_fts`. | Hard deterministic storage gate. |
| Idempotent memory generation | Memory scorecard and tests require reruns over the same captures to keep stable Markdown bodies and entry count. | Hard deterministic memory gate. |
| Secret exclusion | Memory scorecard and privacy tests require generated Markdown and SQLite entries to exclude password/API key/private key/JWT/GitHub/Slack token canaries. | Hard privacy gate. |
| Fixture-only demo | Deterministic demo avoids `capture-frontmost`, live watcher commands, helper-only targeted UIA smoke, screenshots, OCR, audio, keyboard, clipboard, network upload, LLM calls, desktop control, daemon/service install, polling capture, and default background capture. | Hard demo boundary. |

## Drift Fix Decision

AF3 found no required schema, MCP tool-list, MCP tool-schema, memory Markdown
reducer, SQLite storage schema, privacy, helper, watcher, or capture-surface
change. It found two narrow deterministic guardrail drifts:

- `generate-memory` manifest JSON included observed-derived titles and grouping
  metadata but did not include the observed-content trust boundary. AF3 added
  `trust`, `untrusted_observed_content`, and `instruction` to the manifest JSON,
  updated the golden, and added CLI/install-smoke assertions.
- The standalone MCP smoke compared `tools/list` against implementation
  constants and used a narrower forbidden-term set than the scorecard. AF3 made
  the smoke use a literal expected tool list and the full write/file/network/
  control/targeted-capture forbidden term set. Stdio tests now also exercise
  `desktop_control`, `control_desktop`, `press_key`, `capture_hwnd`,
  `capture_pid`, and `capture_window_title` call attempts.

The reviewed docs, scorecards, tests, and deterministic demo preserve exact
read-only MCP tools, stable response examples, CLI/MCP memory-search parity,
durable memory goldens, idempotence, secret exclusion, and the observed-content
trust boundary.

No fresh manual UIA smoke is required to land this AF3 review because it changes
deterministic memory manifest metadata plus MCP smoke/test guardrails, and does
not change helper behavior, watcher product behavior, manual smoke scripts,
capture behavior, privacy runtime behavior, capture surfaces, or release
approver requirements. A future release-readiness record should make a fresh
manual-smoke freshness decision because AF3 adds compatible `generate-memory`
CLI JSON trust fields.

The next smallest implementation task is to land this AF3 review through PR and
post-merge Windows Harness validation, then record AF3 completion before
starting AF4 compatibility guardrail sweep.

## Boundary Confirmation

This sweep does not authorize MCP write tools, arbitrary file reads, screenshot
capture, OCR, audio recording, keyboard capture, clipboard capture, network
upload, LLM calls, desktop control, product targeted capture, daemon/service
install, polling capture loops, default background capture, or live UIA smoke
in default CI.
