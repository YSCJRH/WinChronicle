# Compatibility Guardrail Sweep After v0.1.16

This sweep records the AF4 compatibility check for the post-v0.1.16
maintenance round. It records three narrow documentation and guardrail
precision fixes: the public MCP tool list is ordered to match the exact
contract, operator docs now name every disabled targeted-capture flag, and the
standalone MCP smoke compares the ordered literal tool list instead of a set.
It also records one compatibility-test hardening item: `generate-memory`
manifest JSON now has a frozen trust-boundary shape after the AF3 compatible
field addition. It does not change schemas, MCP tool schemas, helper/watcher
output contracts, capture storage shape, privacy behavior, capture surfaces,
or version metadata.

## Guardrails Checked

| Guardrail | Evidence | Result |
| --- | --- | --- |
| Version identity | `tests/test_version_identity.py` remains in the focused compatibility set. | No drift found; version remains `0.1.16`. |
| Exact read-only MCP tool list | `tests/test_mcp_tools.py`, `harness/scorecards/mcp-quality.md`, `docs/mcp-readonly-examples.md`, README, and `harness/scripts/run_mcp_smoke.py` remain the compatibility oracles for `current_context`, `search_captures`, `search_memory`, `read_recent_capture`, `recent_activity`, and `privacy_status`. | AF4 fixed README ordering and made MCP smoke compare ordered tool names. |
| Disabled privacy surfaces | `tests/test_compatibility_contracts.py`, `tests/test_phase6_privacy_scorecard.py`, `harness/scorecards/privacy-gates.md`, and CLI/MCP status contracts cover disabled screenshot, OCR, audio, keyboard, clipboard, network/cloud upload, LLM, desktop control, product targeted capture, and MCP write surfaces. | Disabled-surface contract still holds. |
| Observed-content trust boundary | CLI capture/search, `generate-memory`, memory search, MCP, deterministic demo, and scorecard tests require `trust = "untrusted_observed_content"` for observed capture and memory content. | AF4 added a compatibility test for the generated memory manifest JSON trust fields. |
| Watcher preview limits | `tests/test_watcher_events.py`, `docs/watcher-preview.md`, and `docs/operator-diagnostics.md` keep watcher behavior explicit, finite-duration, preview-only, and non-daemonized. | Preview boundary still holds. |
| Durable memory contract | `tests/test_memory_pipeline.py`, `tests/test_redaction.py`, and `harness/scorecards/memory-quality.md` cover deterministic Markdown, SQLite `entries` / `entries_fts`, source capture paths, app names, time ranges, idempotence, manifest trust metadata, filtered search parity, and secret-canary exclusion. | Durable memory contract still holds. |
| Phase 6 spec-only status | `tests/test_phase6_privacy_scorecard.py` and `harness/scorecards/phase6-privacy-enrichment.md` keep screenshot/OCR as future opt-in enrichment only. | No screenshot/OCR implementation found. |
| Product targeted capture absence | CLI compatibility tests and operator docs reject product `--hwnd`, `--pid`, `--window-title`, `--window-title-regex`, and `--process-name` flags. | AF4 fixed quickstart wording to name every disabled targeted flag. |

## Commands

Focused guardrail tests:

```powershell
python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py tests/test_version_identity.py -q
```

Result: `50 passed`.

Boundary scan:

```powershell
rg -n -e "--hwnd|--pid|--window-title|--window-title-regex|--process-name|screenshot|ocr|audio|keyboard|clipboard|network_upload|cloud_upload|llm_calls|desktop_control|write_memory|read_file|click|type" src/winchronicle tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py harness/scorecards docs/mcp-readonly-examples.md docs/watcher-preview.md docs/deterministic-demo.md docs/roadmap.md CONTRIBUTING.md .github
```

Reviewed result: matches are existing disabled-surface contracts, sentinels,
documentation, scorecards, deterministic fixtures/tests, schema field names,
or allowed helper-only harness wording. No new product CLI/MCP targeted
capture, write/control tool, screenshot/OCR, audio, keyboard, clipboard,
network upload, cloud upload, LLM, desktop control, daemon/service, polling
capture, or default background capture surface was found.

Control/capture dependency scan:

```powershell
rg -n -g "*.py" -g "*.cs" -g "*.md" -g "*.json" -g "*.yml" -e "SetForegroundWindow|AttachThreadInput|SendInput|mouse_event|keybd_event|GetAsyncKeyState|OpenClipboard|GetClipboardData|BitBlt|CopyFromScreen|PrintWindow|Tesseract|OpenAI|Anthropic|requests|httpx|aiohttp|selenium|playwright" src resources tests harness .github docs CONTRIBUTING.md README.md
```

Reviewed result: matches are prior compatibility sweep command text,
historical plan evidence, privacy-policy canary text, deterministic
fixture/golden content, explicit forbidden-term tests, and the local MCP smoke
request variable name. No new runtime dependency or implementation path was
found.

## Decision

AF4 found no required schema, MCP tool-schema, helper/watcher output contract,
capture storage shape, privacy, capture-surface, or version-metadata change. It
found and fixed four narrow compatibility evidence drifts:

- README listed the read-only MCP tools out of contract order. AF4 aligned the
  public list with the source/tests/scorecard order.
- Operator quickstart omitted `--window-title-regex` and `--process-name` from
  its product targeted-capture warning. AF4 added the full disabled targeted
  flag set.
- Standalone MCP smoke used a literal expected list but compared sets. AF4 made
  it compare ordered tool names so order and duplicate drift fail the smoke.
- The AF3 `generate-memory` manifest JSON trust-field addition needed a
  compatibility-level shape test. AF4 added that guardrail while preserving the
  stable CLI command set.

The next smallest implementation task is to land this AF4 review through PR and
post-merge Windows Harness validation, then record AF4 completion before
deciding whether a post-v0.1.16 release-readiness stage is warranted.
