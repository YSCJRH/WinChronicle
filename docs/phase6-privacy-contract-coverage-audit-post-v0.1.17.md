# Phase 6 Privacy Contract Coverage Audit After v0.1.17

This record performs the Phase 6 privacy-enrichment contract coverage audit
after the remaining negative fixture expansion. It is a docs/tests-only
coverage audit. It does not implement or authorize screenshot capture, OCR,
or raw screenshot cache creation. It keeps no screenshot capture, OCR, raw
screenshot cache, runtime allowlist parsing, CLI/MCP output changes,
helper/watcher behavior changes, product targeted capture, desktop control,
network upload, LLM calls, daemon/service install, polling capture loops, or
default background capture in scope.

## Scope

| Surface | Decision |
| --- | --- |
| Runtime behavior | Unchanged. |
| Product CLI/MCP JSON shape | Unchanged. |
| Screenshot/OCR implementation | Not authorized. |
| Contract artifacts | Audited existing schema, scorecard, tests, and fixtures. |
| Tests | Tightened the old in-memory variant test so each variant maps to a committed fixture. |

## Inputs

- `harness/specs/phase6-privacy-enrichment-contract.schema.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_spec_only.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_*.json`
- `harness/scorecards/phase6-privacy-enrichment.md`
- `tests/test_phase6_privacy_scorecard.py`

## Findings

The scorecard-named risk classes now have committed negative fixture coverage:

| Risk class | Committed fixture |
| --- | --- |
| Wildcard allowlist selector | `privacy_enrichment_contract_invalid_global_allowlist.json` |
| Too-long raw cache TTL | `privacy_enrichment_contract_invalid_raw_cache_ttl.json` |
| Runtime-enabled status | `privacy_enrichment_contract_invalid_runtime_status.json` |
| Default-enabled screenshots | `privacy_enrichment_contract_invalid_screenshots_default_enabled.json` |
| Default-enabled OCR | `privacy_enrichment_contract_invalid_ocr_default_enabled.json` |
| Missing raw cache cleanup | `privacy_enrichment_contract_invalid_missing_cleanup.json` |
| Raw screenshot MCP exposure | `privacy_enrichment_contract_invalid_raw_mcp_exposure.json` |
| Runtime allowlist configuration | `privacy_enrichment_contract_invalid_runtime_allowlist_config.json` |
| Runtime capture allowed in v0.1 | `privacy_enrichment_contract_invalid_runtime_capture_allowed.json` |
| Missing required non-goal coverage | `privacy_enrichment_contract_invalid_missing_non_goal.json` |

The seven unsafe variants that were originally exercised in memory now map
one-to-one to committed invalid fixtures:

- `privacy_enrichment_contract_invalid_screenshots_default_enabled.json`
- `privacy_enrichment_contract_invalid_ocr_default_enabled.json`
- `privacy_enrichment_contract_invalid_missing_cleanup.json`
- `privacy_enrichment_contract_invalid_raw_mcp_exposure.json`
- `privacy_enrichment_contract_invalid_runtime_allowlist_config.json`
- `privacy_enrichment_contract_invalid_runtime_capture_allowed.json`
- `privacy_enrichment_contract_invalid_missing_non_goal.json`

The audit found no unsafe variant that remains only an in-memory test case.
The test now asserts that each historical in-memory variant exactly matches a
committed invalid fixture.

Several high-signal schema branches are schema-enforced but not yet represented
by their own targeted negative fixture:

- `defaults.raw_screenshot_cache_enabled`
- `defaults.global_allowlist_enabled`
- `allowlist_policy.global_default_allowlist_allowed`
- `allowlist_policy.implicit_all_apps_allowed`
- `raw_cache_policy.enabled_by_default`
- `mcp_policy.mcp_write_tools_allowed`

These are not product behavior gaps. They remain rejected by the JSON Schema
and the valid spec-only fixture keeps the required safe value. They are good
candidates for the next small fixture-only expansion because they cover
default raw-cache enablement, global allowlist enablement, implicit all-app
capture, and MCP write exposure.

## Privacy And Security

This audit is privacy-positive and behavior-neutral. It makes the fixture
coverage boundary explicit without adding capture, storage, upload, control,
MCP write, runtime parsing, allowlist, screenshot, OCR, or raw cache surface.
Observed content remains untrusted, and Phase 6 artifacts remain specification
only.

## Validation

Local coverage-audit validation:

```powershell
python -m pytest tests/test_phase6_privacy_scorecard.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q
python -m pytest -q
rg -n "phase6-privacy-enrichment-contract|privacy_enrichment_contract|harness/fixtures/phase6|harness\\fixtures\\phase6" src resources
git diff --check
python harness/scripts/run_harness.py
```

Result: passed; focused Phase 6/docs validation reported 88 tests, full pytest
reported 185 tests, the product-source contract-artifact reference scan
returned no matches, `git diff --check` passed, and the full deterministic
harness passed, including 185 pytest tests, helper/watcher builds with 0
warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy
check, fixture capture/search/memory, deterministic watcher fixture, and
watcher fake-helper smoke.

PR and post-merge validation:

- PR #174 merged at `2026-05-09T17:49:10Z` as
  `117cb0f42fe8e7825b15279a6f102e3b18cc0081`.
- PR #174 Windows Harness run `25607674390` concluded `success` on
  `0e3789f30d84db313b778469e5fae8e6bdc3864d`.
- Post-coverage-audit `main` Windows Harness run `25607748205` concluded
  `success` on `117cb0f42fe8e7825b15279a6f102e3b18cc0081`.

## Next Task

Add targeted durable Phase 6 negative fixtures for the highest-signal
schema-enforced branches identified by this audit: raw screenshot cache enabled
by default, global allowlist enabled by default, global default allowlist
allowed, implicit all-app allowlist allowed, raw cache enabled by default, and
MCP write tools allowed. Screenshot/OCR implementation remains out of scope
for v0.1 maintenance unless a future plan explicitly authorizes tests-first
runtime work.
