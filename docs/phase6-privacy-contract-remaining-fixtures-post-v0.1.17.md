# Phase 6 Privacy Contract Remaining Fixtures After v0.1.17

This record continues the Phase 6 privacy-enrichment contract lane after the
first committed negative fixture expansion. It is contract-only. It does not
implement or authorize screenshot capture, OCR, raw screenshot caches, runtime
allowlist parsing, CLI/MCP output changes, helper/watcher behavior changes,
product targeted capture, desktop control, network upload, LLM calls,
daemon/service install, polling capture loops, or default background capture.

## Scope

| Surface | Decision |
| --- | --- |
| Runtime behavior | Unchanged. |
| Product CLI/MCP JSON shape | Unchanged. |
| Screenshot/OCR implementation | Not authorized. |
| Contract artifacts | Added committed negative fixtures for remaining unsafe schema cases. |
| Tests | Expanded committed negative fixture validation under the Phase 6 scorecard test. |

## Fixture Additions

The Phase 6 schema already rejected two unsafe in-memory variants that were not
yet committed as standalone negative fixtures:

- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_runtime_capture_allowed.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_missing_non_goal.json`

These fixtures are not runtime configuration. Product code must not read them
in v0.1.

## Privacy And Security

This expansion is privacy-positive and behavior-neutral. It adds durable review
artifacts for two unsafe contract states without adding any capture, storage,
upload, control, MCP write, runtime parsing, allowlist, screenshot, OCR, or raw
cache surface.

## Validation

Baseline:

- Phase 6 fixture expansion reconciliation PR #171 merged as
  `c9fc41632048db3083dc3ca552030268859d985e`.
- PR #171 Windows Harness run `25606538378` concluded `success` on
  `fd16ce1b9a7ba5cc58c70cbd34287edf5f3d01f3`.
- Post-reconciliation `main` Windows Harness run `25606591806` concluded
  `success` on `c9fc41632048db3083dc3ca552030268859d985e`.

Local remaining-fixtures validation:

```powershell
python -m pytest tests/test_phase6_privacy_scorecard.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q
python -m pytest -q
rg -n -e "phase6-privacy-enrichment-contract" -e "privacy_enrichment_contract" -e "harness/fixtures/phase6" -e "harness\\fixtures\\phase6" src resources
git diff --check
python harness/scripts/run_harness.py
```

Result: passed; focused Phase 6/docs validation reported 87 tests, full pytest
reported 184 tests, the product-source contract-artifact reference scan
returned no matches, `git diff --check` passed, the runtime/resource/version
diff check returned no files, and the full deterministic harness passed,
including 184 pytest tests, helper/watcher builds with 0 warnings and 0
errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture
capture/search/memory, deterministic watcher fixture, and watcher fake-helper
smoke.

## Next Task

Land this remaining fixture expansion through PR and post-merge Windows Harness
validation. Screenshot/OCR implementation remains out of scope for v0.1
maintenance unless a future plan explicitly authorizes tests-first runtime
work.
