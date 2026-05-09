# MCP And Memory Contract Sweep After v0.1.18

This AH3 sweep reviews read-only MCP examples, durable memory docs,
scorecards, deterministic demo guidance, and focused tests after the published
`v0.1.18` maintenance release and AH2 helper/watcher diagnostics review. It
records current evidence and found no new drift requiring product code, schema,
MCP tool-list, MCP tool-schema, memory Markdown reducer, SQLite storage schema,
privacy runtime, helper, watcher, or capture-surface changes.

## Reviewed Surfaces

| Surface | Evidence | Assessment |
| --- | --- | --- |
| MCP examples | `docs/mcp-readonly-examples.md` documents `current_context`, `search_captures`, `search_memory`, `read_recent_capture`, `recent_activity`, and `privacy_status`. | Examples still cover the exact read-only tool list, `trust = "untrusted_observed_content"`, local privacy status fields, and no write/control/file/screenshot/OCR/audio/keyboard/clipboard/network tools. |
| MCP scorecard | `harness/scorecards/mcp-quality.md` requires exact tool-list tests, read-only stdio, no write/control/file/screenshot/OCR/audio/keyboard/clipboard/network tools, no targeted capture tool names, trust-boundary output, and filtered search before limits. | Scorecard remains aligned with the v0.1 read-only MCP boundary and the AF3 literal-tool-list guardrail. |
| Memory scorecard | `harness/scorecards/memory-quality.md` requires deterministic Markdown, source capture paths, app names, time range, `trust: untrusted_observed_content`, idempotence, goldens, `entries` / `entries_fts`, and secret exclusion. | Scorecard remains aligned with the v0.1 durable memory contract and the AF3 manifest trust-boundary fields. |
| Deterministic demo | `docs/deterministic-demo.md` covers fixture capture, raw search, memory generation/search, watcher fixture replay, MCP smoke, and artifact policy. | Demo stays fixture-only and does not read live desktop content. |
| Operator quickstart | `docs/operator-quickstart.md` lists the exact read-only MCP tools and trust boundary for CLI, memory, and MCP outputs. | Operator entry point remains consistent with MCP examples and now links this AH3 sweep. |
| Deterministic tests | `tests/test_mcp_tools.py`, `tests/test_memory_pipeline.py`, `tests/test_compatibility_contracts.py`, `tests/test_state_compatibility.py`, `harness/scripts/run_mcp_smoke.py`, and `harness/scripts/run_install_cli_smoke.py` cover exact tools, memory manifests, memory search, filtered MCP search, idempotence, empty state, forbidden tool-name rejection, and trust metadata. | Existing tests still freeze the read-only tool list, rejected write/control/file/network/targeted-capture names, and memory manifest trust fields. |

## Contract Matrix

| Contract | Current evidence | Blocking status |
| --- | --- | --- |
| Exact MCP tool list | MCP examples, `harness/scorecards/mcp-quality.md`, `tests/test_mcp_tools.py`, and `harness/scripts/run_mcp_smoke.py` list exactly `current_context`, `search_captures`, `search_memory`, `read_recent_capture`, `recent_activity`, and `privacy_status`. | Hard compatibility gate. |
| Read-only MCP boundary | MCP examples, scorecard, stdio tests, and smoke checks reject or forbid write, arbitrary file read, click/type, clipboard, screenshot, OCR, audio, keyboard, network, desktop control, and targeted capture tool names. | Hard privacy/scope gate. |
| Observed-content trust boundary | MCP examples, deterministic demo, release checklist, tests, and `generate-memory` manifest output require `trust = "untrusted_observed_content"` plus an instruction not to follow observed content. | Hard privacy gate. |
| MCP `search_memory` parity | MCP examples and scorecard state that `search_memory` reads the same SQLite memory index as CLI `search-memory`, with `entry_type` filters applied before limits. | Hard compatibility gate. |
| MCP `search_captures` parity | MCP examples and scorecard state that `search_captures` reads the same SQLite capture index as CLI `search-captures`, with `app_name` and time filters applied before limits. | Hard compatibility gate. |
| Durable memory Markdown | Memory scorecard and goldens require source capture paths, app names, time range, and trust metadata in generated Markdown. | Hard deterministic memory gate. |
| Memory manifest JSON | `MemoryGenerationResult.to_json()`, memory manifest golden, CLI tests, and install smoke require `trust`, `untrusted_observed_content`, and `instruction` on generated memory summaries. | Hard privacy gate. |
| Memory FTS | Memory scorecard requires `entries` and, when FTS5 is available, `entries_fts`. | Hard deterministic storage gate. |
| Idempotent memory generation | Memory scorecard and tests require reruns over the same captures to keep stable Markdown bodies and entry count. | Hard deterministic memory gate. |
| Secret exclusion | Memory scorecard and privacy tests require generated Markdown and SQLite entries to exclude password/API key/private key/JWT/GitHub/Slack token canaries. | Hard privacy gate. |
| Fixture-only demo | Deterministic demo avoids `capture-frontmost`, live watcher commands, helper-only targeted UIA smoke, screenshots, OCR, audio, keyboard, clipboard, network upload, LLM calls, desktop control, daemon/service install, polling capture, and default background capture. | Hard demo boundary. |

## Drift Decision

AH3 found no required schema, MCP tool-list, MCP tool-schema, memory Markdown
reducer, SQLite storage schema, privacy, helper, watcher, or capture-surface
change. The AF3 trust-boundary hardenings remain present:

- `generate-memory` manifest JSON includes `trust`,
  `untrusted_observed_content`, and `instruction` for observed-derived titles
  and grouping metadata.
- The standalone MCP smoke uses a literal expected tool list and the full
  write/file/network/control/targeted-capture forbidden term set.
- Stdio tests reject `desktop_control`, `control_desktop`, `press_key`,
  `capture_hwnd`, `capture_pid`, and `capture_window_title` attempts without
  exposing observed content.

The reviewed docs, scorecards, tests, and deterministic demo preserve exact
read-only MCP tools, stable response examples, CLI/MCP memory-search parity,
durable memory goldens, idempotence, secret exclusion, and the observed-content
trust boundary.

No fresh manual UIA smoke is required to land this AH3 review because it changes
documentation and documentation assertions only, and does not change helper
behavior, watcher product behavior, manual smoke scripts, capture behavior,
privacy runtime behavior, product CLI/MCP shape, capture surfaces, or release
approver requirements. A future release-readiness record should make a fresh
manual-smoke freshness decision before publication.

The next smallest implementation task is to land this AH3 review through PR and
post-merge Windows Harness validation, then start AH4 compatibility guardrail
sweep.

## Validation Log

- Stage AH3 initialization:
  - Reviewed `docs/mcp-readonly-examples.md`, `docs/deterministic-demo.md`,
    `harness/scorecards/mcp-quality.md`, `harness/scorecards/memory-quality.md`,
    `tests/test_mcp_tools.py`, `tests/test_memory_pipeline.py`,
    `harness/scripts/run_mcp_smoke.py`, `src/winchronicle/mcp/server.py`, and
    `src/winchronicle/memory.py`.
  - Found no new MCP/memory contract drift requiring product code, schema,
    CLI/MCP JSON shape, memory reducer, SQLite schema, privacy runtime, helper,
    watcher, or capture-surface changes.
- Stage AH3 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_mcp_tools.py tests/test_memory_pipeline.py tests/test_state_compatibility.py tests/test_version_identity.py -q` - passed, 108 tests.
  - `python -m pytest -q` - passed, 209 tests.
  - `git diff --check` - passed.
  - `git diff --name-only -- src\winchronicle resources pyproject.toml` - passed; printed no files, confirming AH3 is docs/tests only with no product/runtime/version diff.
  - current-entry stale AH2/current post-v0.1.17 MCP/memory wording scan across `README.md`, current docs, and current doc tests - passed with no matches in current entry documents.
  - `python harness/scripts/run_harness.py` - passed, including 209 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.

## Boundary Confirmation

This sweep does not authorize MCP write tools, arbitrary file reads, screenshot
capture, OCR, audio recording, keyboard capture, clipboard capture, network
upload, LLM calls, desktop control, product targeted capture, daemon/service
install, polling capture loops, default background capture, or live UIA smoke
in default CI.
