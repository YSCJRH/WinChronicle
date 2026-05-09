# Phase 6 Privacy Contract Residual Schema Coverage Audit After v0.1.17

This record audits the remaining Phase 6 privacy-enrichment schema branches
after the targeted gap fixture expansion and its reconciliation. It is a
docs/tests-only audit. It does not implement or authorize screenshot capture,
OCR, raw screenshot caches, runtime allowlist parsing, CLI/MCP output changes,
helper/watcher behavior changes, product targeted capture, desktop control,
network upload, LLM calls, daemon/service install, polling capture loops, or
default background capture.

## Scope

| Surface | Decision |
| --- | --- |
| Runtime behavior | Unchanged. |
| Product CLI/MCP JSON shape | Unchanged. |
| Screenshot/OCR implementation | Not authorized. |
| Contract artifacts | Audited residual schema branches against committed fixtures and scorecard tests. |
| Tests | Added documentation assertions for the residual audit and next fixture-only cursor. |

## Inputs

- `harness/specs/phase6-privacy-enrichment-contract.schema.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_spec_only.json`
- `harness/fixtures/phase6/privacy_enrichment_contract_invalid_*.json`
- `harness/scorecards/phase6-privacy-enrichment.md`
- `tests/test_phase6_privacy_scorecard.py`

## Findings

The high-signal gaps identified by the prior coverage audit now have targeted
committed invalid fixtures:

| Schema branch | Committed fixture |
| --- | --- |
| `defaults.raw_screenshot_cache_enabled` | `privacy_enrichment_contract_invalid_raw_screenshot_cache_default_enabled.json` |
| `defaults.global_allowlist_enabled` | `privacy_enrichment_contract_invalid_global_allowlist_default_enabled.json` |
| `allowlist_policy.global_default_allowlist_allowed` | `privacy_enrichment_contract_invalid_global_default_allowlist_allowed.json` |
| `allowlist_policy.implicit_all_apps_allowed` | `privacy_enrichment_contract_invalid_implicit_all_apps_allowed.json` |
| `raw_cache_policy.enabled_by_default` | `privacy_enrichment_contract_invalid_raw_cache_enabled_by_default.json` |
| `mcp_policy.mcp_write_tools_allowed` | `privacy_enrichment_contract_invalid_mcp_write_tools_allowed.json` |

The remaining high-signal policy branches are schema-enforced and positively
asserted by the valid spec-only fixture, but they do not yet have their own
targeted committed invalid fixture:

| Branch group | Residual branches | Risk if weakened later | Recommendation |
| --- | --- | --- | --- |
| Future opt-in requirements | `future_opt_in_requirements.requires_explicit_screenshots_enabled_true`, `requires_explicit_ocr_enabled_true`, `requires_per_app_screenshot_allowlist`, `requires_per_app_ocr_allowlist`, `forbids_global_default_allowlist`, `forbids_implicit_all_apps`, `requires_uia_first_fallback_only` | Future screenshot/OCR work could loosen explicit opt-in, per-app allowlisting, or UIA-first fallback requirements before implementation exists. | Promote to targeted negative fixtures in the next fixture-only batch. |
| Raw cache artifact controls | `raw_cache_policy.local_state_directory_only`, `raw_artifacts_commit_forbidden`, `encryption_at_rest_required_or_exception_documented` | Raw visual artifacts could escape local state, be committed accidentally, or lack an encryption/exception decision. | Promote to targeted negative fixtures in the next fixture-only batch. |
| Derived text pipeline controls | `derived_text_pipeline.redaction_before_storage`, `denylist_and_lock_screen_skip_before_storage`, `schema_validation_before_storage`, `sqlite_index_after_redaction`, `memory_from_redacted_text_only`, `prompt_injection_marked_untrusted` | OCR-derived text could bypass existing redaction, denylist, schema, indexing, memory, or trust-boundary controls. | Promote to targeted negative fixtures in the next fixture-only batch. |
| MCP trust boundary | `mcp_policy.requires_untrusted_observed_content_trust` | MCP output could expose derived observed text without the required untrusted-content label. | Promote to a targeted negative fixture in the next fixture-only batch. |
| Sample-only allowlist marker | `allowlist_policy.sample_allowlist_entries_only` | Example entries could be mistaken for approved runtime allowlists. | Consider a targeted negative fixture after the higher-signal policy controls. |

The following schema branches are adequately covered by schema validation,
positive fixture assertions, or existing shared negative fixtures and do not
need immediate standalone fixtures:

- root object shape, required fields, `additionalProperties`, and
  `contract_schema_version`;
- `status`, already covered by
  `privacy_enrichment_contract_invalid_runtime_status.json`;
- default screenshot/OCR booleans, already covered by
  `privacy_enrichment_contract_invalid_screenshots_default_enabled.json` and
  `privacy_enrichment_contract_invalid_ocr_default_enabled.json`;
- allowlist selector wildcard rejection, covered through the shared
  `$defs.app_selector` path by
  `privacy_enrichment_contract_invalid_global_allowlist.json`;
- `allowlist_policy.runtime_allowlist_config_allowed`, already covered by
  `privacy_enrichment_contract_invalid_runtime_allowlist_config.json`;
- raw cache TTL maximum and cleanup requirement, already covered by
  `privacy_enrichment_contract_invalid_raw_cache_ttl.json` and
  `privacy_enrichment_contract_invalid_missing_cleanup.json`;
- MCP raw screenshot exposure default, already covered by
  `privacy_enrichment_contract_invalid_raw_mcp_exposure.json`;
- `non_goals` required coverage, minimum length, and contains constraints,
  already covered by `privacy_enrichment_contract_invalid_missing_non_goal.json`.

These findings are contract coverage findings, not product behavior gaps. The
current schema rejects unsafe values and the spec-only fixture keeps the safe
values.

## Privacy And Security

This audit is privacy-positive and behavior-neutral. It identifies the next
fixture-only review targets without adding capture, storage, upload, control,
MCP write, runtime parsing, allowlist, screenshot, OCR, or raw cache surface.
Observed content remains untrusted, and Phase 6 artifacts remain specification
only.

## Validation

Local residual-schema-audit validation:

```powershell
python -m pytest tests/test_phase6_privacy_scorecard.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q
python -m pytest -q
rg -n "phase6-privacy-enrichment-contract|privacy_enrichment_contract|harness/fixtures/phase6|harness\\fixtures\\phase6" src resources
git diff --check
python harness/scripts/run_harness.py
```

Result: passed; focused Phase 6/docs validation reported 90 tests, full pytest
reported 187 tests, the product-source contract-artifact reference scan
returned no matches, `git diff --check` passed, and the full deterministic
harness passed, including 187 pytest tests, helper/watcher builds with 0
warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy
check, fixture capture/search/memory, deterministic watcher fixture, and
watcher fake-helper smoke.

## Next Task

Add targeted durable Phase 6 negative fixtures for the residual high-signal
policy branches: future opt-in requirement booleans, raw cache local-state,
artifact-commit, and encryption/exception controls, derived text pipeline
controls, and MCP untrusted-content trust requirements. Screenshot/OCR
implementation remains out of scope for v0.1 maintenance unless a future plan
explicitly authorizes tests-first runtime work.
