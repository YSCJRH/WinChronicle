# Compatibility Guardrail Sweep After v0.1.15

This sweep records the AD4 compatibility check for the post-v0.1.15
maintenance round. It records two narrow compatibility drift fixes: broader
obvious-secret redaction canaries and product helper/watcher pass-through
rejection for disabled target/control/privacy-surface flags. It does not
change schemas, CLI/MCP JSON shape, MCP tool schemas, helper/watcher output
contracts, capture storage shape, or version metadata.

## Guardrails Checked

| Guardrail | Evidence | Result |
| --- | --- | --- |
| Version identity | `tests/test_version_identity.py` remains in the focused compatibility set. | No drift found. |
| Exact read-only MCP tool list | `tests/test_mcp_tools.py`, `harness/scorecards/mcp-quality.md`, and `docs/mcp-readonly-examples.md` remain the compatibility oracles for `current_context`, `search_captures`, `search_memory`, `read_recent_capture`, `recent_activity`, and `privacy_status`. | No write/control/file/screenshot/OCR/audio/keyboard/clipboard/network tools found. |
| Disabled privacy surfaces | `tests/test_compatibility_contracts.py`, `tests/test_phase6_privacy_scorecard.py`, `harness/scorecards/privacy-gates.md`, and CLI/MCP status contracts cover disabled screenshot, OCR, audio, keyboard, clipboard, network/cloud upload, LLM, desktop control, product targeted capture, and MCP write surfaces. | AD4 now rejects forbidden target/control/privacy flags passed through `--helper-arg` / `--watcher-arg`. |
| Observed-content trust boundary | CLI, memory, MCP, deterministic demo, and scorecard tests continue to require `trust = "untrusted_observed_content"` for observed capture and memory content. | Trust boundary still holds. |
| Watcher preview limits | `tests/test_watcher_events.py`, `docs/watcher-preview.md`, and `docs/operator-diagnostics.md` keep watcher behavior explicit, finite-duration, preview-only, and non-daemonized. | Preview boundary still holds. |
| Durable memory contract | `tests/test_memory_pipeline.py`, `tests/test_redaction.py`, and `harness/scorecards/memory-quality.md` cover deterministic Markdown, SQLite `entries` / `entries_fts`, source capture paths, app names, time ranges, idempotence, filtered search parity, and secret-canary exclusion. | AD4 broadened obvious-secret canaries before release readiness. |
| Phase 6 spec-only status | `tests/test_phase6_privacy_scorecard.py` and `harness/scorecards/phase6-privacy-enrichment.md` keep screenshot/OCR as future opt-in enrichment only. | No screenshot/OCR implementation found. |
| Product targeted capture absence | CLI compatibility tests reject product `--hwnd`, `--pid`, `--window-title`, `--window-title-regex`, and `--process-name` flags. | Product targeted capture remains absent. |

## Commands

Focused guardrail tests before AD4 fixes:

```powershell
python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py tests/test_version_identity.py -q
```

Result: `48 passed`.

Focused drift-fix tests:

```powershell
python -m pytest tests/test_redaction.py tests/test_compatibility_contracts.py -q
```

Result: `6 passed`.

Boundary scan:

```powershell
rg -n -e "--hwnd|--pid|--window-title|--window-title-regex|--process-name|screenshot|ocr|audio|keyboard|clipboard|network_upload|cloud_upload|llm_calls|desktop_control|write_memory|read_file|click|type" src/winchronicle tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py harness/scorecards docs/mcp-readonly-examples.md docs/watcher-preview.md docs/deterministic-demo.md docs/roadmap.md CONTRIBUTING.md .github
```

Reviewed result: matches are existing disabled-surface contracts, sentinels,
AD4 pass-through rejection tests, documentation, scorecards, deterministic
fixtures/tests, schema field names, or allowed helper-only harness wording.
No new product CLI/MCP targeted capture, write/control tool, screenshot/OCR,
audio, keyboard, clipboard, network upload, cloud upload, LLM, desktop control,
daemon/service, polling capture, or default background capture surface was
found.

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

AD4 found no required schema, CLI/MCP JSON, MCP tool schema, helper/watcher
output contract, capture storage shape, or version-metadata change. It found
and fixed two narrow compatibility guardrail drifts:

- The redaction test matrix did not cover newer obvious GitHub/Slack token
  families or long labeled API-key values. AD4 broadened deterministic canary
  coverage and redaction patterns before capture writes, SQLite indexing,
  memory generation, and MCP search exposure.
- Product helper/watcher pass-through arguments were not covered by the
  product targeted-capture absence guardrail. AD4 now rejects disabled
  target/control/privacy-surface flags passed through `--helper-arg` and
  `--watcher-arg`, while preserving existing explicit helper/watcher wrapper
  paths used by deterministic smoke tests.

The next smallest implementation task is AD5 release readiness for the
compatible `v0.1.16` maintenance target, with publication still gated on local,
PR, post-merge validation, and explicit release approval.
