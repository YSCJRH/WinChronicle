# Phase 6 Privacy Contract Fixture Expansion After v0.1.17

This record continues the Phase 6 privacy-enrichment contract lane after the
completed contract preflight. It is contract-only. It does not implement or
authorize screenshot capture, OCR, raw screenshot caches, runtime allowlist
parsing, CLI/MCP output changes, helper/watcher behavior changes, product
targeted capture, desktop control, network upload, LLM calls, daemon/service
install, polling capture loops, or default background capture.

## Scope

| Surface | Decision |
| --- | --- |
| Runtime behavior | Unchanged. |
| Product CLI/MCP JSON shape | Unchanged. |
| Screenshot/OCR implementation | Not authorized. |
| Contract artifacts | Added committed negative fixtures for existing unsafe schema cases. |
| Tests | Expanded committed negative fixture validation under the Phase 6 scorecard test. |

## Fixture Additions

The preflight schema already rejected unsafe in-memory variants for
default-enabled screenshots/OCR, missing raw cache cleanup, raw screenshot MCP
exposure, and runtime allowlist configuration. This step commits those cases as
stable negative fixtures:

- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_screenshots_default_enabled.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_ocr_default_enabled.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_missing_cleanup.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_raw_mcp_exposure.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_runtime_allowlist_config.json`

These fixtures are not runtime configuration. Product code must not read them
in v0.1.

## Privacy And Security

This expansion is privacy-positive and behavior-neutral. It makes unsafe future
contract states durable review artifacts without adding any capture, storage,
upload, control, MCP write, runtime parsing, allowlist, screenshot, OCR, or raw
cache surface.

## Validation

Baseline:

- Phase 6 preflight reconciliation PR #169 merged as
  `297f2637a0d1a24a3359076f956322b0fda81575`.
- PR #169 Windows Harness run `25605887788` concluded `success` on
  `9195db0f8c25cbfb26f8f892a9436e2c92616ba7`.
- Post-reconciliation `main` Windows Harness run `25605945162` concluded
  `success` on `297f2637a0d1a24a3359076f956322b0fda81575`.

Local fixture-expansion validation:

```powershell
python -m pytest tests/test_phase6_privacy_scorecard.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q
python -m pytest -q
rg -n "phase6-privacy-enrichment-contract|privacy_enrichment_contract|harness/fixtures/phase6|harness\\fixtures\\phase6" src resources
git diff --check
python harness/scripts/run_harness.py
```

Result: passed; focused Phase 6/docs validation reported 87 tests, full pytest
reported 184 tests, the product-source contract-artifact reference scan
returned no matches, `git diff --check` passed, and the full deterministic
harness passed, including 184 pytest tests, helper/watcher builds with 0
warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy
check, fixture capture/search/memory, deterministic watcher fixture, and
watcher fake-helper smoke.

## Next Task

Land this fixture expansion through PR and post-merge Windows Harness
validation. Screenshot/OCR implementation remains out of scope for v0.1
maintenance unless a future plan explicitly authorizes tests-first runtime
work.
