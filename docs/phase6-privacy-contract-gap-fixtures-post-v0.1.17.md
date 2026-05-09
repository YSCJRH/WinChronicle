# Phase 6 Privacy Contract Gap Fixtures After v0.1.17

This record starts the targeted Phase 6 privacy-enrichment contract gap fixture
expansion after the coverage audit. It is contract-only. It does not implement
or authorize screenshot capture, OCR, raw screenshot caches, runtime allowlist
parsing, CLI/MCP output changes, helper/watcher behavior changes, product
targeted capture, desktop control, network upload, LLM calls, daemon/service
install, polling capture loops, or default background capture.

## Scope

| Surface | Decision |
| --- | --- |
| Runtime behavior | Unchanged. |
| Product CLI/MCP JSON shape | Unchanged. |
| Screenshot/OCR implementation | Not authorized. |
| Contract artifacts | Added targeted negative fixtures for high-signal schema-enforced branches. |
| Tests | Expanded committed negative fixture validation under the Phase 6 scorecard test. |

## Fixture Additions

The coverage audit identified high-signal branches already rejected by the
schema but not yet represented by their own committed invalid fixture. This
step commits those cases as stable negative fixtures:

- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_raw_screenshot_cache_default_enabled.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_global_allowlist_default_enabled.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_global_default_allowlist_allowed.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_implicit_all_apps_allowed.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_raw_cache_enabled_by_default.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_mcp_write_tools_allowed.json`

These fixtures are not runtime configuration. Product code must not read them
in v0.1.

## Privacy And Security

This expansion is privacy-positive and behavior-neutral. It makes unsafe
future contract states durable review artifacts without adding any capture,
storage, upload, control, MCP write, runtime parsing, allowlist, screenshot,
OCR, or raw cache surface.

## Validation

Local gap-fixture validation:

```powershell
python -m pytest tests/test_phase6_privacy_scorecard.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q
python -m pytest -q
rg -n "phase6-privacy-enrichment-contract|privacy_enrichment_contract|harness/fixtures/phase6|harness\\fixtures\\phase6" src resources
git diff --check
python harness/scripts/run_harness.py
```

Result: passed; focused Phase 6/docs validation reported 89 tests, full pytest
reported 186 tests, the product-source contract-artifact reference scan
returned no matches, `git diff --check` passed, and the full deterministic
harness passed, including 186 pytest tests, helper/watcher builds with 0
warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy
check, fixture capture/search/memory, deterministic watcher fixture, and
watcher fake-helper smoke.

PR and post-merge validation:

- PR #176 merged at `2026-05-09T18:18:56Z` as
  `05811145444af93178b957bd1a3fc11b47f64cfd`.
- PR #176 Windows Harness run `25608336721` concluded `success` on
  `d9fc229304ce7f613db7b06c3f89c29190ae0981`.
- Post-gap-fixtures `main` Windows Harness run `25608403951` concluded
  `success` on `05811145444af93178b957bd1a3fc11b47f64cfd`.

## Next Task

Audit the remaining Phase 6 schema-enforced branches that still do not have a
targeted committed invalid fixture, especially opt-in requirement booleans,
raw cache local-state/encryption/artifact controls, derived text pipeline
controls, and MCP trust-boundary requirements. Screenshot/OCR implementation
remains out of scope for v0.1 maintenance unless a future plan explicitly
authorizes tests-first runtime work.
