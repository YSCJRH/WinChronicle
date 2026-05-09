# Phase 6 Privacy Contract Residual Policy Fixtures After v0.1.17

This record starts the targeted Phase 6 privacy-enrichment residual policy
fixture expansion after the residual schema coverage audit. It is
contract-only. It does not implement or authorize screenshot capture, OCR, raw
screenshot caches, runtime allowlist parsing, CLI/MCP output changes,
helper/watcher behavior changes, product targeted capture, desktop control,
network upload, LLM calls, daemon/service install, polling capture loops, or
default background capture.

## Scope

| Surface | Decision |
| --- | --- |
| Runtime behavior | Unchanged. |
| Product CLI/MCP JSON shape | Unchanged. |
| Screenshot/OCR implementation | Not authorized. |
| Contract artifacts | Added targeted negative fixtures for residual high-signal policy branches. |
| Tests | Expanded committed negative fixture validation under the Phase 6 scorecard test. |

## Fixture Additions

The residual schema coverage audit identified remaining high-signal policy
branches already rejected by the schema but not yet represented by their own
committed invalid fixture. This step commits those cases as stable negative
fixtures:

Future opt-in requirements:

- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_future_screenshots_opt_in_not_required.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_future_ocr_opt_in_not_required.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_future_screenshot_allowlist_not_required.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_future_ocr_allowlist_not_required.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_future_global_default_allowlist_not_forbidden.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_future_implicit_all_apps_not_forbidden.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_future_uia_first_fallback_not_required.json`

Raw cache artifact controls:

- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_raw_cache_nonlocal_state_allowed.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_raw_cache_artifact_commit_allowed.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_raw_cache_encryption_exception_missing.json`

Derived text pipeline controls:

- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_derived_text_redaction_after_storage_allowed.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_derived_text_denylist_skip_after_storage_allowed.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_derived_text_schema_validation_after_storage_allowed.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_derived_text_sqlite_index_before_redaction_allowed.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_derived_text_memory_from_raw_allowed.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_derived_text_prompt_injection_trusted.json`

MCP trust-boundary controls:

- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_mcp_trust_boundary_not_required.json`

These fixtures are not runtime configuration. Product code must not read them
in v0.1.

## Deferred Residual Branches

The lower-priority residual branches remain schema-enforced and positively
covered by the spec-only fixture, but are not expanded in this batch:

- `allowlist_policy.sample_allowlist_entries_only`;
- empty allowlist array and alternate `app_name` selector shape variants;
- individual `non_goals.contains`, `uniqueItems`, and enum variants beyond the
  existing missing-non-goal fixture.

These are deferred fixture-coverage candidates, not product behavior gaps.

## Privacy And Security

This expansion is privacy-positive and behavior-neutral. It makes unsafe
future policy states durable review artifacts without adding any capture,
storage, upload, control, MCP write, runtime parsing, allowlist, screenshot,
OCR, or raw cache surface.

## Validation

Local residual-policy-fixture validation:

```powershell
python -m pytest tests/test_phase6_privacy_scorecard.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q
python -m pytest -q
rg -n "phase6-privacy-enrichment-contract|privacy_enrichment_contract|harness/fixtures/phase6|harness\\fixtures\\phase6" src resources
git diff --check
python harness/scripts/run_harness.py
```

Result: passed; focused Phase 6/docs validation reported 91 tests, full pytest
reported 188 tests, the product-source contract-artifact reference scan
returned no matches, `git diff --check` passed, and the full deterministic
harness passed, including 188 pytest tests, helper/watcher builds with 0
warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy
check, fixture capture/search/memory, deterministic watcher fixture, and
watcher fake-helper smoke.

PR and post-merge validation:

- PR #179 merged at `2026-05-09T19:03:47Z` as
  `013ea612eb6cfe885130d0646ce816038fab2da4`.
- PR #179 Windows Harness run `25609287443` concluded `success` on
  `d0576d133792dba88b8d1cb746ea5312314d15f5`.
- Post-residual-policy-fixtures `main` Windows Harness run `25609341275`
  concluded `success` on `013ea612eb6cfe885130d0646ce816038fab2da4`.

## Next Task

Decide whether to add lower-priority deferred Phase 6 contract fixtures for
the sample-only allowlist marker, empty allowlist arrays, alternate
`app_name` selector shape variants, and deeper `non_goals` variants, or close
Phase 6 fixture coverage as adequate for the v0.1 maintenance boundary.
Screenshot/OCR implementation remains out of scope for v0.1 maintenance unless
a future plan explicitly authorizes tests-first runtime work.
