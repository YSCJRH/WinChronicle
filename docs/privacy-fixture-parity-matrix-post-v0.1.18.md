# Fixture/Privacy Parity Matrix After v0.1.18

## Purpose

This AH12 matrix consolidates the Fixture and privacy baseline evidence from
AH8 watcher privacy fixture parity and AH10 fixture/helper privacy index parity.
It is an audit map for deterministic coverage; it does not add runtime capture
behavior, helper/watcher behavior, schemas, CLI/MCP output, or release-version
changes.

## Scope

- Direct fixture capture means `capture_once_from_fixture` using committed
  synthetic privacy fixtures.
- Synthesized UIA helper capture means `capture_once_from_uia_helper_record`
  using helper-shaped records derived in tests from the same synthetic privacy
  fixtures.
- Watcher-dispatched capture means `dispatch_watcher_events` or `watch
  --events` consuming temporary watcher JSONL generated under `tmp_path` from
  existing synthetic privacy fixtures.
- Generated capture files, memory files, SQLite state, helper outputs, and
  watcher JSONL stay under temporary test state only.
- No raw helper JSON, no raw watcher JSONL, generated capture-buffer JSON,
  generated memory Markdown, screenshots, OCR output, passwords, secrets, token
  canaries, or observed-content artifacts are committed.

## Matrix

| Privacy gate | Direct fixture evidence | Synthesized helper evidence | Watcher-dispatched evidence | Blocking status |
| --- | --- | --- | --- | --- |
| Password-field redaction | `tests/test_privacy_index_parity.py::test_fixture_privacy_capture_and_memory_indexes_exclude_raw_terms` reuses `harness/fixtures/privacy/password_field.json`. | `tests/test_privacy_index_parity.py::test_uia_helper_privacy_capture_and_memory_indexes_exclude_raw_terms` derives a helper-shaped record from `password_field.json`. | `tests/test_watcher_events.py::test_watcher_privacy_fixture_preserves_redaction_skip_and_trust` emits a temporary watcher event from `password_field.json`. | Hard automated privacy gate. |
| Obvious secret canary redaction | `tests/test_privacy_index_parity.py::test_fixture_privacy_capture_and_memory_indexes_exclude_raw_terms` reuses `secrets_visible_text.json`. | `tests/test_privacy_index_parity.py::test_uia_helper_privacy_capture_and_memory_indexes_exclude_raw_terms` derives a helper-shaped record from `secrets_visible_text.json`. | `tests/test_watcher_events.py::test_watcher_privacy_fixture_preserves_redaction_skip_and_trust` emits a temporary watcher event from `secrets_visible_text.json`. | Hard automated privacy gate. |
| Raw term absence across storage and search | Direct fixture parity asserts raw terms are absent from capture-buffer JSON, memory Markdown, SQLite `captures`, `captures_fts`, `entries`, `entries_fts`, `search_captures`, `search_memory_entries`, and MCP `search_memory`. | Synthesized helper parity asserts the same absence surfaces as direct fixture parity. | Watcher parity asserts raw terms are absent from capture files, memory files, capture search, memory search, and MCP memory search, and keeps watcher JSONL out of `WINCHRONICLE_HOME`. | Hard automated privacy gate. |
| Untrusted observed-content metadata | Direct fixture parity asserts every capture has `untrusted_observed_content = true`; memory contract tests cover trust preservation from fixture captures. | Synthesized helper parity asserts every capture has `untrusted_observed_content = true`. | Watcher parity asserts prompt-injection text remains searchable only with `trust = "untrusted_observed_content"` in capture search, memory search, MCP memory search, and memory Markdown. | Hard trust-boundary gate. |
| Denylist skip-before-storage | `tests/test_fixture_capture.py::test_denylisted_app_capture_is_skipped` covers direct denylisted fixture skip behavior. | Helper-derived denylist behavior is exercised through watcher helper payloads rather than a separate committed helper artifact. | Watcher parity asserts denylisted app and title-denylisted watcher events increment `denylisted_skipped`, write no capture artifact, and leave no searchable observed text. | Hard privacy gate; helper-only follow-up only if a future product gap is found. |
| Raw stream and artifact non-persistence | Direct fixture parity writes generated captures and memory only under temporary `WINCHRONICLE_HOME`. | Synthesized helper parity derives helper records in test memory and writes generated captures and memory only under temporary `WINCHRONICLE_HOME`. | Watcher parity writes temporary watcher JSONL outside `WINCHRONICLE_HOME`, asserts no raw `.jsonl` stream persists under state, and covers fake watcher stdout without committing raw events. | Hard artifact-policy gate. |
| Disabled capture surfaces | Direct fixture paths stay fixture-only and do not enable screenshots, OCR, audio, keyboard, clipboard, desktop control, network upload, LLM calls, MCP writes, or product targeted capture. | Synthesized helper records explicitly keep `capture_surfaces` disabled for screenshots, OCR, audio, keyboard, clipboard, and desktop control. | Watcher preview remains explicit, time-bounded, no-service, no-daemon, no-default-background, and no raw JSONL persistence. | Hard v0.1 boundary gate. |

## Evidence Sources

- `docs/watcher-privacy-fixture-parity-post-v0.1.18.md`
- `docs/fixture-helper-privacy-index-parity-post-v0.1.18.md`
- `docs/watcher-preview.md`
- `docs/uia-helper-quality-matrix.md`
- `harness/scorecards/privacy-gates.md`
- `tests/test_watcher_events.py`
- `tests/test_privacy_index_parity.py`
- `tests/test_fixture_capture.py`
- `tests/test_memory_pipeline.py`
- `tests/test_privacy_policy_contract.py`

## Validation

Local validation for this matrix record should include:

```powershell
python -m pytest tests/test_privacy_index_parity.py tests/test_watcher_events.py tests/test_fixture_capture.py tests/test_privacy_policy_contract.py -q
python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_uia_helper_quality_matrix.py tests/test_version_identity.py -q
python -m pytest -q
git diff --check
git diff --name-only v0.1.18..HEAD -- pyproject.toml src\winchronicle\_version.py src\winchronicle\mcp\server.py resources
python harness/scripts/run_harness.py
```

## Privacy And Security

This task strengthens auditability only. It does not add a new capture surface,
does not store password fields or obvious secrets, does not commit raw helper or
watcher streams, does not commit generated captures or memory, and does not
change live UIA, watcher, MCP, screenshot, OCR, clipboard, keyboard, audio,
network, LLM, or desktop-control behavior.
