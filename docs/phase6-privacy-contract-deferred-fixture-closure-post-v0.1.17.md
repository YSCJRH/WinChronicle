# Phase 6 Privacy Contract Deferred Fixture Closure After v0.1.17

This targeted Phase 6 privacy-enrichment deferred fixture closure closes the
coverage decision after the residual policy fixture expansion and its evidence
reconciliation. It is contract-only. It does not implement or authorize
screenshot capture, OCR, raw screenshot caches, runtime allowlist parsing,
CLI/MCP output changes, helper/watcher behavior changes, product targeted
capture, desktop control, network upload, LLM calls, daemon/service install,
polling capture loops, or default background capture.

## Scope

| Surface | Decision |
| --- | --- |
| Runtime behavior | Unchanged. |
| Product CLI/MCP JSON shape | Unchanged. |
| Screenshot/OCR implementation | Not authorized. |
| Contract artifacts | Added final low-noise negative fixtures for deferred contract branches. |
| Tests | Expanded committed negative fixture validation under the Phase 6 scorecard test. |

## Decision

The residual policy fixture expansion left four lower-priority schema branches
as deferred candidates: the sample-only allowlist marker, empty allowlist
arrays, alternate `app_name` selector shape variants, and deeper `non_goals`
variants. Those branches were already schema-enforced and positively covered by
the spec-only fixture, but closing without committed negative fixtures would
leave some contract-drift risks unpinned.

This closure promotes the lower-priority deferred candidates to committed
fixtures rather than accepting them as schema-only residual coverage. The added
fixtures keep the v0.1 runtime boundary unchanged and avoid setting a broader
"one fixture per schema keyword" standard outside these privacy-sensitive
allowlist and non-goal controls.

## Fixture Additions

Allowlist marker, empty allowlist, and selector-shape controls:

- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_sample_allowlist_entries_not_sample_only.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_screenshots_allowlist_empty.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_ocr_allowlist_empty.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_empty_app_selector.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_app_name_wildcard_allowlist.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_app_name_all_allowlist.json`

Deeper `non_goals` controls:

- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_non_goals_duplicate.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_non_goals_unknown.json`

Together with the prior fixture batches, Phase 6 now has 41 committed invalid
fixtures. The valid spec-only fixture remains the only positive contract
fixture, and all committed invalid fixtures must be rejected by the schema.

## Coverage Closure

Phase 6 fixture coverage is adequate for the v0.1 maintenance boundary because:

- every high-signal unsafe screenshot/OCR/default/runtime/cache/MCP branch has
  a targeted committed negative fixture;
- the remaining deferred allowlist and non-goal branches now have a small
  committed fixture batch;
- the spec-only positive fixture still asserts the allowed shape;
- product source tests still require Phase 6 artifacts to stay out of runtime
  configuration.

These fixtures are not runtime configuration. Product code must not read them
in v0.1.

## Privacy And Security

This closure is privacy-positive and behavior-neutral. It pins the remaining
deferred allowlist and non-goal contract drift cases without adding capture,
storage, upload, control, MCP write, runtime parsing, allowlist, screenshot,
OCR, or raw cache surface.

There is no runtime, helper/watcher, CLI/MCP output, privacy-runtime,
capture-surface, or version-metadata change.

## Validation

Local deferred-fixture-closure validation:

```powershell
python -m pytest tests/test_phase6_privacy_scorecard.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q
python -m pytest -q
rg -n "phase6-privacy-enrichment-contract|privacy_enrichment_contract|harness/fixtures/phase6|harness\\fixtures\\phase6" src resources
git diff --check
python harness/scripts/run_harness.py
```

Result: passed; focused Phase 6/docs validation reported 92 tests, full pytest
reported 189 tests, the product-source contract-artifact reference scan
returned no matches, `git diff --check` passed, and the full deterministic
harness passed, including 189 pytest tests, helper/watcher builds with 0
warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy
check, fixture capture/search/memory, deterministic watcher fixture, and
watcher fake-helper smoke.

## Next Task

After PR review and merge, reconcile the deferred-fixture-closure evidence by
recording the PR number, merge commit, PR Windows Harness run, and post-merge
`main` Windows Harness run, then select the next blueprint lane. Screenshot/OCR
implementation remains out of scope for v0.1 maintenance unless a future plan
explicitly authorizes tests-first runtime work.
