# Fixture/Helper Privacy Index Parity After v0.1.18

## Purpose

This record advances the selected Fixture and privacy baseline lane after AH9.
AH8 proved watcher-dispatched privacy parity across capture files, memory files,
SQLite search tables, and MCP memory-search results. This AH10 task gives the
same raw-secret absence evidence to direct fixture captures and synthesized UIA
helper captures without changing product runtime behavior.

## Scope

- Reuse existing synthetic privacy fixtures:
  - `harness/fixtures/privacy/password_field.json`
  - `harness/fixtures/privacy/secrets_visible_text.json`
- Do not add new committed helper, watcher, capture, memory, screenshot, OCR, or
  observed-content artifacts.
- For direct fixture captures, assert raw password and token canaries are absent
  from capture-buffer JSON, memory Markdown, SQLite `captures`, `captures_fts`,
  `entries`, `entries_fts`, `search_captures`, `search_memory_entries`, and MCP
  `search_memory`.
- For synthesized UIA helper captures, derive helper-shaped records in the test
  from the same privacy fixtures and assert the same absence checks.
- Preserve the v0.1 boundary: no screenshot/OCR, audio, keyboard, clipboard,
  network upload, LLM, desktop control, product targeted capture, service
  install, polling capture loop, default background capture, or MCP write tools.

## Evidence

- Added `tests/test_privacy_index_parity.py` to cover direct fixture and
  synthesized helper paths through the shared normalize, redaction, storage,
  memory, SQLite, and MCP search pipeline.
- Direct fixture captures keep `source = "fixture"` and `trigger.source =
  "manual"` while preserving untrusted observed-content metadata.
- Synthesized helper captures keep `source = "uia_helper"` and `trigger.source =
  "win_uia_helper"` while preserving untrusted observed-content metadata.
- Both paths prove password-field redaction and obvious API key, GitHub token,
  Slack token, JWT, and private key redaction before capture or memory indexing.

## Validation

- `python -m pytest tests/test_privacy_index_parity.py -q` - passed, 2 tests.
- `python -m pytest tests/test_privacy_index_parity.py tests/test_privacy_policy_contract.py -q` - passed, 7 tests.
- `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 94 tests.
- `python -m pytest -q` - passed, 221 tests.
- `git diff --check` - passed.
- `git diff --name-only v0.1.18..HEAD -- pyproject.toml src\winchronicle\_version.py src\winchronicle\mcp\server.py resources` - passed; printed no files, confirming AH10 does not change version metadata, MCP server code, resources, helper, or watcher binaries/projects.
- stale AH9/current-follow-up wording scan across `README.md`, current docs,
  current tests, and privacy scorecards - passed with no matches.
- `python harness/scripts/run_harness.py` - passed, including 221 pytest tests,
  helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke,
  install CLI smoke, privacy check, fixture capture/search/memory,
  deterministic watcher fixture, and watcher fake-helper smoke.

## PR And Post-Merge Evidence

- PR #199 merged at `2026-05-10T01:33:45Z` as
  `cf1dab1d58e6e637c73aee748056591b597d70b1`.
- PR #199 Windows Harness run `25616618385` concluded `success` on
  `591a87b4ec237388ec83525083d560285dc62638`.
- Post-AH10 `main` Windows Harness run `25616673782` concluded `success` on
  `cf1dab1d58e6e637c73aee748056591b597d70b1`.

## Privacy And Security

This task strengthens deterministic privacy evidence only. It does not add a
new capture surface, does not persist raw helper/watcher streams, does not
commit generated captures or memory artifacts, and does not change live UIA,
watcher, MCP, screenshot, OCR, clipboard, keyboard, audio, network, LLM, or
desktop-control behavior.

## Completed Follow-Up

AH10 PR and post-merge harness evidence has been reconciled in the active
post-v0.1.18 maintenance plan. Fixture/privacy parity matrix consolidation is
complete and tracked by `docs/privacy-fixture-parity-matrix-post-v0.1.18.md`.
