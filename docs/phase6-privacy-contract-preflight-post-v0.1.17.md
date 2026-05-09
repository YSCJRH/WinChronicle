# Phase 6 Privacy Contract Preflight After v0.1.17

This record starts the next blueprint lane after the completed post-v0.1.17
AG5 release-readiness decision. It is contract-only. It does not implement or
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
| Contract artifacts | Added a spec-only Phase 6 privacy-enrichment contract schema and fixtures. |
| Tests | Added validation for the positive contract and unsafe negative variants. |

## Contract Artifacts

- `harness/specs/phase6-privacy-enrichment-contract.schema.json` defines the
  future pre-implementation contract shape.
- `harness/fixtures/phase6/privacy_enrichment_contract_spec_only.json`
  validates a compliant spec-only contract. Its allowlist entries are sample
  shape examples only, not approved apps, and the contract requires
  `runtime_allowlist_config_allowed: false`.
- Negative fixtures reject wildcard/global allowlist behavior, excessive raw
  cache TTL, and runtime-enabled status.

These artifacts are not runtime configuration. Product code must not read them
in v0.1.

## Threat Model Coverage

The Phase 6 scorecard now records that raw screenshots can expose passwords,
private messages, browser sessions, source code, local files, and other
observed content. OCR-derived text can reintroduce secrets after UIA redaction.
Broad allowlists can silently become all-app capture. Raw caches can outlive
user intent. MCP exposure can leak visual artifacts across agent boundaries.

Future implementation remains blocked until contracts, fixtures, tests,
scorecards, and operator docs define explicit opt-in, per-app allowlists,
UIA-first fallback-only behavior, short-TTL raw cache cleanup, local-state-only
storage, encryption-at-rest or a documented exception, redaction before
storage, denylist/lock-screen skips, schema validation before storage, and MCP
default non-exposure of raw screenshots.

## Privacy And Security

This preflight is privacy-positive and behavior-neutral. It tightens future
requirements without adding any capture, storage, upload, control, MCP write,
or runtime parsing surface. Observed content remains untrusted, and generated
state or raw visual artifacts must not be committed.

## Validation

Baseline:

- AG6 post-merge `main` Windows Harness run `25605064828` concluded `success`
  on `0b05b88018679d1fdaee8cb5e6440768badbc21a`.

Local preflight validation:

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

Land this contract preflight through PR and post-merge Windows Harness
validation. A later Phase 6 step may refine operator docs or add more negative
contract fixtures, but screenshot/OCR implementation remains out of scope for
v0.1 maintenance unless a future plan explicitly authorizes tests-first
runtime work.
