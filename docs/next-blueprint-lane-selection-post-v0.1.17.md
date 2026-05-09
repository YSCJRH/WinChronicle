# Next Blueprint Lane Selection After v0.1.17

This record selects the next blueprint lane after the completed Phase 6
privacy-enrichment contract closure and its no-release decision. The selected
lane is Fixture and privacy baseline.

The first task in that lane is a privacy-policy contract parity audit. It
should compare `harness/specs/privacy-policy.md`,
`harness/scorecards/privacy-gates.md`, deterministic privacy fixtures,
redaction and denylist tests, CLI status privacy fields, and MCP
`privacy_status` output before any behavior change.

## Baseline Evidence

- Phase 6 contract closure release-readiness decision PR #183 merged as
  `784a01385c5e77785bdcc3f2298df988f94e5c66`.
- PR #183 Windows Harness run `25610492799` concluded `success` on
  `4fccc6ccb78ab322844e96e0bd3ca82e918aebcc`.
- Post-merge `main` Windows Harness run `25610538811` concluded `success` on
  `784a01385c5e77785bdcc3f2298df988f94e5c66`.
- `git diff --name-only v0.1.17..HEAD -- src\winchronicle resources
  pyproject.toml` printed no files through the selected baseline.

## Selection Matrix

| Lane | Decision | Evidence | First safe task |
| --- | --- | --- | --- |
| Fixture and privacy baseline | Selected. | `docs/roadmap.md` lists this lane's safe next work as strengthening fixtures, schemas, redaction tests, denylist tests, and scorecard evidence. `harness/scorecards/privacy-gates.md` says the privacy-policy spec must match implemented denylist, redaction, and trust-boundary behavior. | Privacy-policy contract parity audit. |
| UIA helper hardening | Defer. | The post-v0.1.17 helper/watcher diagnostics sweep found no required helper or watcher product-code change. Helper work carries higher risk if it drifts into live UIA behavior or product targeted capture. | Revisit only after the privacy baseline audit or a focused helper-contract gap. |
| Watcher preview | Defer. | Watcher preview diagnostics already cover failure modes, heartbeat-only liveness, duplicate skip, denylist skip, and raw JSONL non-persistence. | Revisit only through deterministic watcher fixtures and no daemon/service/polling expansion. |
| Read-only MCP | Defer. | The MCP/memory contract sweep found no current read-only MCP drift and the exact tool list remains frozen. | Revisit only for read-only response-shape evidence or trust-boundary drift. |
| Durable memory | Defer. | The MCP/memory contract sweep found no current durable-memory drift, with idempotence, FTS, trust metadata, and secret exclusion already covered. | Revisit only for deterministic golden or parity gaps. |
| Docs and deterministic demo | Defer. | The deterministic demo and operator docs already link fixture capture, search, memory, watcher replay, MCP smoke, and artifact policy. | Revisit when a selected lane changes operator flow. |
| Phase 6 privacy enrichment | Closed for this pass. | The Phase 6 closure record says fixture coverage is adequate for the v0.1 maintenance boundary, and PR #183 records no release/publication path from the contract-only closure. | Do not reopen Phase 6 unless a future tests-first plan explicitly authorizes new work. |

## Decision

Start the Fixture and privacy baseline lane with a privacy-policy contract
parity audit.

The audit should be docs/tests/fixture/scorecard first. It may identify later
behavior work, but this lane-selection record does not authorize runtime
changes, new capture surfaces, schema expansion, CLI/MCP output changes,
helper/watcher behavior changes, or release-version changes.

Credit-card Luhn-positive redaction remains documented in
`harness/specs/privacy-policy.md` as a broader blueprint item that is not
implemented in v0.1. A future audit may decide whether to keep it as a non-goal
or promote it through tests-first contract work, but this selection does not
promote it.

## Validation

Local validation for this lane-selection record:

```powershell
python -m pytest tests/test_phase6_privacy_scorecard.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q
python -m pytest -q
git diff --check
git diff --name-only v0.1.17..HEAD -- src\winchronicle resources pyproject.toml
python harness/scripts/run_harness.py
```

Result: passed; focused Phase 6/docs validation reported 94 tests, full pytest
reported 191 tests, `git diff --check` passed, the runtime/resource/version
diff command printed no files, and the full deterministic harness passed,
including 191 pytest tests, helper/watcher builds with 0 warnings and 0 errors,
watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture
capture/search/memory, deterministic watcher fixture, and watcher fake-helper
smoke.

## Privacy And Security

This selection preserves the v0.1 privacy boundary. It does not authorize
screenshot capture, OCR, raw screenshot caches, runtime allowlist parsing,
audio recording, keyboard capture, clipboard capture, network/cloud upload,
LLM calls, desktop control, product targeted capture, daemon/service install,
polling capture loops, default background capture, MCP write tools, arbitrary
file read tools, real UIA capture changes, helper/watcher behavior changes, or
committed observed-content artifacts.

Observed content remains untrusted. No local state, generated captures,
generated memory, raw helper JSON, raw watcher JSONL, screenshots, OCR output,
passwords, secrets, token canaries, or observed-content diagnostics should be
committed.

## Next Task

Start the privacy-policy contract parity audit. Map policy statements to
fixtures, tests, scorecards, and docs before considering any runtime behavior.
