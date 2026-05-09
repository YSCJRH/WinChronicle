# Compatibility Guardrail Sweep After v0.1.18

This sweep records the AH4 compatibility check for the post-v0.1.18
maintenance round after AH3 MCP/memory contract review landed. It records
current compatibility evidence and found no required schema, MCP tool-schema,
helper/watcher output contract, capture storage shape, privacy runtime,
capture-surface, dependency, or version-metadata change.

## Guardrails Checked

| Guardrail | Evidence | Result |
| --- | --- | --- |
| Version identity | `tests/test_version_identity.py` remains in the focused compatibility set. | No drift found; version remains `0.1.18`. |
| Exact read-only MCP tool list | `tests/test_mcp_tools.py`, `harness/scorecards/mcp-quality.md`, `docs/mcp-readonly-examples.md`, README, and `harness/scripts/run_mcp_smoke.py` remain the compatibility oracles for `current_context`, `search_captures`, `search_memory`, `read_recent_capture`, `recent_activity`, and `privacy_status`. | Ordered literal tool-list guardrails still hold. |
| Disabled privacy surfaces | `tests/test_compatibility_contracts.py`, `tests/test_phase6_privacy_scorecard.py`, `harness/scorecards/privacy-gates.md`, and CLI/MCP status contracts cover disabled screenshot, OCR, audio, keyboard, clipboard, network/cloud upload, LLM, desktop control, product targeted capture, and MCP write surfaces. | Disabled-surface contract still holds. |
| Observed-content trust boundary | CLI capture/search, `generate-memory`, memory search, MCP, deterministic demo, and scorecard tests require `trust = "untrusted_observed_content"` for observed capture and memory content. | Trust-boundary contract still holds. |
| Watcher preview limits | `tests/test_watcher_events.py`, `docs/watcher-preview.md`, and `docs/operator-diagnostics.md` keep watcher behavior explicit, finite-duration, preview-only, and non-daemonized. | Preview boundary still holds. |
| Durable memory contract | `tests/test_memory_pipeline.py`, `tests/test_redaction.py`, and `harness/scorecards/memory-quality.md` cover deterministic Markdown, SQLite `entries` / `entries_fts`, source capture paths, app names, time ranges, idempotence, manifest trust metadata, filtered search parity, and secret-canary exclusion. | Durable memory contract still holds. |
| Phase 6 spec-only status | `tests/test_phase6_privacy_scorecard.py` and `harness/scorecards/phase6-privacy-enrichment.md` keep screenshot/OCR as future opt-in enrichment only. | No screenshot/OCR implementation found. |
| Product targeted capture absence | CLI compatibility tests and operator docs reject product `--hwnd`, `--pid`, `--window-title`, `--window-title-regex`, and `--process-name` flags. Pass-through rejection tests cover every disabled helper/watcher surface flag. | Product targeted capture remains absent. |

## Commands

Focused guardrail tests:

```powershell
python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py tests/test_privacy_check.py tests/test_privacy_policy_contract.py tests/test_version_identity.py -q
```

Result: `161 passed`.

Boundary scan:

```powershell
rg -n -e "--hwnd|--pid|--window-title|--window-title-regex|--process-name|screenshot|ocr|audio|keyboard|clipboard|network_upload|cloud_upload|llm_calls|desktop_control|write_memory|read_file|click|type" src\winchronicle tests\test_compatibility_contracts.py tests\test_mcp_tools.py tests\test_phase6_privacy_scorecard.py tests\test_watcher_events.py tests\test_state_compatibility.py tests\test_memory_pipeline.py harness\scorecards docs\mcp-readonly-examples.md docs\watcher-preview.md docs\deterministic-demo.md docs\roadmap.md CONTRIBUTING.md .github
```

Reviewed result: matches are existing disabled-surface contracts, sentinels,
documentation, scorecards, deterministic fixtures/tests, schema field names,
or allowed helper-only harness wording. No new product CLI/MCP targeted
capture, write/control tool, screenshot/OCR, audio, keyboard, clipboard,
network upload, cloud upload, LLM, or desktop control surface was found.

Background install/polling scan:

```powershell
rg -n -e "daemon|service|polling|background" src\winchronicle tests\test_compatibility_contracts.py tests\test_mcp_tools.py tests\test_phase6_privacy_scorecard.py tests\test_watcher_events.py tests\test_state_compatibility.py tests\test_memory_pipeline.py tests\test_privacy_check.py harness\scorecards docs\mcp-readonly-examples.md docs\watcher-preview.md docs\deterministic-demo.md docs\roadmap.md CONTRIBUTING.md .github
```

Reviewed result: matches are explicit boundary documentation, scorecards,
tests, and issue-template checklist text that forbid daemon/service install,
polling capture, startup tasks, or default background capture. No product
daemon/service install, polling capture loop, startup task, or default
background capture implementation path was found.

Control/capture dependency scan:

```powershell
rg -n -g "*.py" -g "*.cs" -g "*.md" -g "*.json" -g "*.yml" -e "SetForegroundWindow|AttachThreadInput|SendInput|mouse_event|keybd_event|GetAsyncKeyState|OpenClipboard|GetClipboardData|BitBlt|CopyFromScreen|PrintWindow|Tesseract|OpenAI|Anthropic|requests|httpx|aiohttp|selenium|playwright" src resources tests harness .github docs CONTRIBUTING.md README.md
```

Reviewed result: matches are prior compatibility sweep command text,
historical plan evidence, privacy-policy canary text, deterministic
fixture/golden content, explicit forbidden-term tests, public metadata wording,
and the local MCP smoke request variable name. No new runtime dependency or
implementation path was found.

Full deterministic validation:

```powershell
python -m pytest -q
```

Result: `211 passed`.

```powershell
git diff --check
```

Result: passed.

Stale cursor scan:

```powershell
rg -n "Current stage: AH3|AH3 in progress|Next atomic task: land this AH3|then continue compatibility guardrail review in AH4|Last completed evidence: AH2|post-AH2 `main` Windows Harness run `25613866954`|Current compatibility guardrail sweep \| \[Compatibility guardrail sweep after v0\.1\.17\]" README.md docs\next-round-plan-post-v0.1.18.md docs\operator-quickstart.md docs\release-checklist.md docs\release-evidence.md docs\manual-smoke-evidence-ledger.md tests\test_compatibility_evidence_docs.py tests\test_operator_diagnostics_docs.py
```

Result: no matches.

Harness:

```powershell
python harness/scripts/run_harness.py
```

Result: WinChronicle harness passed, including 211 pytest tests,
helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke,
install CLI smoke, privacy check, fixture capture/search/memory,
deterministic watcher fixture, and watcher fake-helper smoke.

## Decision

AH4 found no required schema, MCP tool-schema, helper/watcher output contract,
capture storage shape, privacy runtime, capture-surface, dependency, or
version-metadata change. The reviewed tests and scorecards preserve version
identity, exact read-only MCP tools, disabled privacy surfaces,
observed-content trust boundaries, watcher preview limits, durable memory
contracts, product targeted-capture absence, and Phase 6 spec-only status.

No fresh manual UIA smoke is required to land this AH4 review because it changes
documentation and documentation assertions only, and does not change helper
behavior, watcher product behavior, manual smoke scripts, capture behavior,
privacy runtime behavior, product CLI/MCP shape, capture surfaces, or release
approver requirements. A future release-readiness record should make a fresh
manual-smoke freshness decision before publication.

The next smallest implementation task is to land this AH4 review through PR and
post-merge Windows Harness validation, then decide whether a post-v0.1.18
release-readiness stage is warranted.

## Boundary Confirmation

This sweep does not authorize screenshot capture, OCR, audio recording,
keyboard capture, clipboard capture, network upload, LLM calls, desktop
control, MCP write tools, arbitrary file read tools, product targeted capture,
daemon/service install, polling capture loops, default background capture, or
live UIA smoke in default CI.
