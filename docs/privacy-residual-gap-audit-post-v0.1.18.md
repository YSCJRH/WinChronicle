# Fixture/Privacy Residual Gap Audit After v0.1.18

## Purpose

This AH14 audit checks the consolidated fixture/privacy parity matrix for
remaining evidence or product-output gaps before the Fixture and privacy
baseline lane moves on. It uses the AH12 matrix as the evidence index and keeps
the v0.1 boundary unchanged.

## Findings

| Finding | Resolution | Boundary |
| --- | --- | --- |
| Helper denylist skip-before-storage had runtime coverage through `capture_once_from_uia_helper_record` and watcher helper payloads, but lacked a standalone helper-only parity test. | Added `tests/test_privacy_index_parity.py::test_uia_helper_denylisted_privacy_captures_are_skipped_without_artifacts` for denylisted app and title-denylisted helper records. The test asserts no capture path, no capture object, no capture-buffer JSON, no memory Markdown, no SQLite capture count, and no capture/memory/MCP search matches. | Uses synthesized helper-shaped records only; does not commit raw helper JSON or generated state. |
| MCP search tools used raw queries for local searches and also echoed those queries in read-only results. That made full MCP payloads reintroduce secret-looking strings when the query itself was a secret canary. | `search_captures` and `search_memory` still use the raw query internally for local SQLite search, but their returned `result.query` is passed through the existing redaction pipeline. Added `tests/test_mcp_tools.py::test_mcp_search_tools_redact_secret_like_query_echoes` and strengthened fixture/helper parity assertions to serialize full MCP results. | Read-only MCP tool names and input schemas remain unchanged; normal non-secret query examples remain unchanged. |
| Existing raw-term gates treated standalone private-key boundary markers as forbidden, while the redaction rule only matched complete PEM blocks. | Expanded `private_key` redaction to cover standalone `BEGIN ... PRIVATE KEY` and `END ... PRIVATE KEY` boundary markers, updated the privacy policy, and added `tests/test_redaction.py::test_redact_text_removes_private_key_boundary_markers`. | Privacy-positive redaction hardening only; no new capture surface or storage behavior expansion. |

## Matrix Updates

- The denylist skip-before-storage row now names the direct helper-only
  denylist test alongside direct fixture and watcher-dispatched evidence.
- The raw storage/search row now states that raw terms are absent from full MCP
  search payloads, including redacted search query echoes.
- The privacy scorecard mirrors those rows as the canonical cross-path audit
  map.

## Validation

Local validation for this audit branch:

```powershell
python -m pytest tests/test_mcp_tools.py tests/test_privacy_index_parity.py tests/test_redaction.py tests/test_privacy_policy_contract.py -q
python -m pytest tests/test_privacy_index_parity.py tests/test_watcher_events.py tests/test_fixture_capture.py tests/test_privacy_policy_contract.py -q
python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_privacy_policy_contract.py tests/test_uia_helper_quality_matrix.py tests/test_version_identity.py -q
python -m pytest -q
git diff --check
git diff --name-only -- pyproject.toml src\winchronicle\_version.py resources
git diff --name-only -- src\winchronicle\mcp\server.py src\winchronicle\redaction.py harness\specs\privacy-policy.md
python harness/scripts/run_harness.py
```

Result: passed locally before PR review. Focused MCP/privacy-redaction
validation reported 25 tests, focused cross-path privacy validation reported 34
tests, focused docs/privacy validation reported 107 tests, full pytest reported
227 tests, `git diff --check` passed, the version/resources/helper/watcher diff
printed no files, the runtime/privacy diff was limited to
`src/winchronicle/mcp/server.py`, `src/winchronicle/redaction.py`, and
`harness/specs/privacy-policy.md`, stale AH13/AH12 residual-gap wording scan
returned no matches, and the full deterministic harness passed, including 227
pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher
smoke, MCP smoke, install CLI smoke, privacy check, fixture
capture/search/memory, deterministic watcher fixture, and watcher fake-helper
smoke.

## Privacy And Security

This audit closes privacy evidence and output-hardening gaps. It does not add
screenshot capture, OCR, audio recording, keyboard capture, clipboard capture,
network upload, LLM calls, desktop control, daemon/service install, polling
capture loops, default background capture, MCP write tools, arbitrary file read
tools, product targeted capture, raw helper JSON persistence, raw watcher JSONL
persistence, or committed observed-content artifacts.
