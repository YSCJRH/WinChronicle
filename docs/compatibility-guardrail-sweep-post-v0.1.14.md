# Compatibility Guardrail Sweep After v0.1.14

This sweep records the AC4 compatibility check for the post-v0.1.14
maintenance round. It does not change product behavior, schemas, CLI/MCP JSON
shape, MCP tool schemas, helper/watcher behavior, capture surfaces, privacy
behavior, or version metadata.

## Guardrails Checked

| Guardrail | Evidence | Result |
| --- | --- | --- |
| Version identity | `tests/test_version_identity.py` remains in the focused compatibility set. | No drift found. |
| Exact read-only MCP tool list | `tests/test_mcp_tools.py`, `harness/scorecards/mcp-quality.md`, and `docs/mcp-readonly-examples.md` remain the compatibility oracles for `current_context`, `search_captures`, `search_memory`, `read_recent_capture`, `recent_activity`, and `privacy_status`. | No write/control/file/screenshot/OCR/audio/keyboard/clipboard/network tools found. |
| Disabled privacy surfaces | `tests/test_compatibility_contracts.py`, `tests/test_phase6_privacy_scorecard.py`, `harness/scorecards/privacy-gates.md`, and CLI/MCP status contracts cover disabled screenshot, OCR, audio, keyboard, clipboard, network/cloud upload, LLM, desktop control, product targeted capture, and MCP write surfaces. | Disabled-surface contract still holds. |
| Observed-content trust boundary | CLI, memory, MCP, deterministic demo, and scorecard tests continue to require `trust = "untrusted_observed_content"` for observed capture and memory content. | Trust boundary still holds. |
| Watcher preview limits | `tests/test_watcher_events.py`, `docs/watcher-preview.md`, and `docs/operator-diagnostics.md` keep watcher behavior explicit, finite-duration, preview-only, and non-daemonized. | Preview boundary still holds. |
| Durable memory contract | `tests/test_memory_pipeline.py` and `harness/scorecards/memory-quality.md` cover deterministic Markdown, SQLite `entries` / `entries_fts`, source capture paths, app names, time ranges, idempotence, and secret-canary exclusion. | No memory contract drift found. |
| Phase 6 spec-only status | `tests/test_phase6_privacy_scorecard.py` and `harness/scorecards/phase6-privacy-enrichment.md` keep screenshot/OCR as future opt-in enrichment only. | No screenshot/OCR implementation found. |
| Product targeted capture absence | CLI compatibility tests reject product `--hwnd`, `--pid`, `--window-title`, `--window-title-regex`, and `--process-name` flags. | Product targeted capture remains absent. |

## Commands

Focused guardrail tests:

```powershell
python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py tests/test_version_identity.py -q
```

Result: `45 passed`.

Boundary scan:

```powershell
rg -n -e "--hwnd|--pid|--window-title|--window-title-regex|--process-name|screenshot|ocr|audio|keyboard|clipboard|network_upload|cloud_upload|llm_calls|desktop_control|write_memory|read_file|click|type" src/winchronicle tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py harness/scorecards docs/mcp-readonly-examples.md docs/watcher-preview.md docs/deterministic-demo.md docs/roadmap.md CONTRIBUTING.md .github
```

Reviewed result: matches are existing disabled-surface contracts, sentinels,
documentation, scorecards, deterministic fixtures/tests, schema field names, or
allowed helper-only harness wording. No new product CLI/MCP targeted capture,
write/control tool, screenshot/OCR, audio, keyboard, clipboard, network upload,
cloud upload, LLM, desktop control, daemon/service, polling capture, or default
background capture surface was found.

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

AC4 found no compatibility drift and no required product-code, schema,
CLI/MCP JSON, MCP tool schema, helper/watcher, privacy, capture-surface, or
version-metadata change. The next smallest implementation task is AC5 release
readiness for the compatible `v0.1.15` maintenance target, with publication
still gated on local, PR, post-merge validation, and explicit release approval.
