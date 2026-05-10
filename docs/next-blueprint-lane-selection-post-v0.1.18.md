# Next Blueprint Lane Selection After v0.1.18

This AH7 record selects the next blueprint lane after the completed
post-v0.1.18 release-readiness no-release decision and AH6 cursor
reconciliation. The selected lane is Fixture and privacy baseline.

The first task in that lane is watcher privacy fixture parity. It should use
deterministic watcher JSONL fixtures, focused tests, and scorecard/docs updates
to prove watcher-dispatched captures preserve redaction, denylist skipping,
trust-boundary metadata, raw JSONL non-persistence, and no searchable
secret/password content before any behavior change.

## Baseline Evidence

- AH5 release-readiness decision PR #194 merged as
  `0bc33714d8fe2e9926d6c4753c8c7780fb1e9e00`.
- PR #194 Windows Harness run `25614929381` concluded `success` on
  `9016b49678cbb9faefd98ab80ff003fad57e08d1`.
- Post-merge `main` Windows Harness run `25614978807` concluded `success` on
  `0bc33714d8fe2e9926d6c4753c8c7780fb1e9e00`.
- AH6 cursor reconciliation PR #195 merged as
  `545be8dd326b2e9453c1949db44d3445e218b789`.
- PR #195 Windows Harness run `25615214406` concluded `success` on
  `4956bf2e02563bc0f0334115d70b027f68cfae2e`.
- Post-merge `main` Windows Harness run `25615262484` concluded `success` on
  `545be8dd326b2e9453c1949db44d3445e218b789`.
- `git diff --name-only v0.1.18..HEAD -- src\winchronicle resources
  pyproject.toml` printed no files through AH7 initialization.

## Selection Matrix

| Lane | Decision | Evidence | First safe task |
| --- | --- | --- | --- |
| Fixture and privacy baseline | Selected. | `harness/specs/privacy-policy.md` applies the privacy contract to explicit watcher preview events before writes and indexing. The prior privacy-policy parity audit recorded watcher-specific parity as out of scope. `harness/fixtures/watcher` currently has only the basic `notepad_burst.jsonl` fixture. | Watcher privacy fixture parity audit/expansion using deterministic watcher JSONL fixtures and focused tests for redaction, denylist skip, trust boundary, no raw JSONL persistence, and no searchable secret/password content. |
| UIA helper hardening | Defer. | AH2 found no helper/watcher diagnostics drift after `v0.1.18`, and helper work carries higher risk if it drifts into live UIA behavior, product targeted capture, or desktop control. | Revisit only through helper-contract diagnostics, synthetic fixtures, and manual smoke evidence templates. |
| Watcher preview | Defer as standalone behavior work. | Watcher preview remains explicit, finite-duration, and preview-only. Selecting watcher privacy parity here does not authorize watcher behavior changes. | Revisit watcher behavior only after deterministic fixture coverage identifies a narrow tests-first gap. |
| Read-only MCP | Defer. | AH3 found no read-only MCP or memory contract drift, and the exact read-only MCP tool list remains frozen. | Revisit only for read-only response-shape evidence or trust-boundary drift. |
| Durable memory | Defer. | AH3 found no durable-memory drift, with idempotence, FTS, trust metadata, and secret exclusion already covered by deterministic tests. | Revisit only for deterministic golden or parity gaps. |
| Docs and deterministic demo | Defer. | Operator docs and deterministic demo already link fixture capture, search, memory, watcher replay, MCP smoke, and artifact policy. | Revisit when a selected lane changes operator flow. |
| Phase 6 privacy enrichment | Closed for this pass. | Phase 6 contract closure remains complete for the v0.1 maintenance boundary. | Do not reopen Phase 6 unless a future tests-first plan explicitly authorizes new work. |

## Decision

Start the Fixture and privacy baseline lane with watcher privacy fixture parity.

The first task is an audit/fixture/test expansion, not runtime implementation.
It may add committed synthetic watcher fixtures, focused tests, docs, or
scorecard evidence. It does not authorize product runtime behavior changes,
live UIA capture changes, screenshot/OCR implementation, CLI/MCP output
changes, helper/watcher behavior changes, new capture surfaces, schema
expansion, or release-version changes.

The audit should decide whether the existing watcher path already satisfies
the privacy contract for watcher-dispatched captures, or whether a later
tests-first fix is needed. Any runtime/output change found necessary by that
future audit must get its own focused implementation and release-readiness
decision.

## Validation

Local validation for this lane-selection record:

```powershell
python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q
python -m pytest -q
git diff --check
git diff --name-only v0.1.18..HEAD -- src\winchronicle resources pyproject.toml
python harness/scripts/run_harness.py
```

Result: passed locally before PR review. Focused docs/version validation
reported 92 tests, full pytest reported 214 tests, `git diff --check`
passed, the `v0.1.18..HEAD` product diff printed no files, the stale
AH6/pending-roadmap wording scan returned no matches, and the full
deterministic harness passed, including 214 pytest tests, helper/watcher
builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI
smoke, privacy check, fixture capture/search/memory, deterministic watcher
fixture, and watcher fake-helper smoke.

## Privacy And Security

This selection preserves the v0.1 privacy boundary. It does not authorize
screenshot capture, OCR, raw screenshot caches, runtime allowlist parsing,
audio recording, keyboard capture, clipboard capture, network/cloud upload,
LLM calls, desktop control, product targeted capture, daemon/service install,
polling capture loops, default background capture, MCP write tools, arbitrary
file read tools, real UIA capture changes, helper/watcher behavior changes,
or committed observed-content artifacts.

Watcher privacy fixture parity must use synthetic deterministic fixtures. No
local state, generated captures, generated memory, raw helper JSON, raw watcher
JSONL, screenshots, OCR output, passwords, secrets, token canaries, or
observed-content diagnostics should be committed.

## Next Task

Start watcher privacy fixture parity. Add or audit deterministic watcher JSONL
fixtures and focused tests for redaction, denylist skip, trust-boundary
metadata, raw JSONL non-persistence, and search/memory exclusion of secrets
before considering any runtime behavior change.
