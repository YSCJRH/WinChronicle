# Helper And Watcher Diagnostics Sweep After v0.1.18

This AH2 sweep reviews helper and watcher preview diagnostics after the
published `v0.1.18` maintenance release, AH1 public metadata audit, and AH1
merge to `main`. It records current deterministic evidence and follow-up
boundaries only. It does not change schemas, successful CLI/MCP JSON shape,
helper/watcher capture behavior, privacy storage behavior, or capture surfaces.

## Reviewed Surfaces

| Surface | Evidence | Assessment |
| --- | --- | --- |
| Helper quality matrix | `docs/uia-helper-quality-matrix.md` lists deterministic fixtures, wrapper diagnostics, harness-only targeted smoke, manual frontmost smoke, artifact policy, privacy risk, and blocking status. | Current matrix still separates hard automated gates, hard manual gates, and diagnostic/manual confidence gates without promoting live UIA smoke to default CI. |
| Watcher preview docs | `docs/watcher-preview.md` documents explicit/time-bounded preview usage, manual smoke expectations, operator-facing diagnostics, deterministic coverage, and no raw watcher JSONL persistence under product preview state. | Current docs cover preview reliability without authorizing daemon/service install, default background capture, polling capture loops, or live watcher CI. |
| Operator diagnostics | `docs/operator-diagnostics.md` lists stable helper and watcher diagnostic lines and the no observed-content echo policy. | Current guide tells operators to record stable diagnostic lines and local artifact paths only, not raw helper JSON, raw watcher JSONL, screenshots, OCR output, or observed text. |
| Capture quality scorecard | `harness/scorecards/capture-quality.md` requires helper wrapper diagnostics, helper harness-only targeting, watcher reliability modes, fake-helper watcher smoke, heartbeat-only handling, and raw watcher JSONL policy. | Scorecard remains aligned with v0.1 preview boundaries and treats heartbeat-only watcher runs as liveness evidence, not capture success. |
| Deterministic tests | `tests/test_cli.py`, `tests/test_uia_helper_contract.py`, `tests/test_watcher_events.py`, `tests/test_operator_diagnostics_docs.py`, `tests/test_compatibility_contracts.py`, and `tests/test_uia_helper_quality_matrix.py` cover helper wrapper failure modes, content-free skip diagnostics, UIA traversal budget/stale metadata, watcher skip/failure modes, product targeted-capture pass-through rejection, current `v0.1.18` manual-smoke matrix rows, and docs signals. | No new helper/watcher behavior change is warranted for AH2. |

## Failure-mode Matrix

| Required mode | Current evidence | Blocking status |
| --- | --- | --- |
| Helper timeout | `tests/test_uia_helper_contract.py`, `tests/test_cli.py`, and `docs/operator-diagnostics.md` cover `ERROR: helper timed out` without stdout/stderr echo or capture artifacts. | Hard deterministic/wrapper gate. |
| Helper malformed JSON | `tests/test_cli.py` and diagnostics docs cover `ERROR: helper returned invalid JSON`. | Hard deterministic/wrapper gate. |
| Helper empty stdout | `tests/test_cli.py`, `docs/uia-helper-quality-matrix.md`, and diagnostics docs cover `SKIPPED: helper returned no capture` without storing observed content. | Hard deterministic/wrapper gate. |
| Helper nonzero exit | `tests/test_cli.py` and diagnostics docs cover `ERROR: helper failed with exit code <code>`. | Hard deterministic/wrapper gate. |
| Watcher nonzero exit | `tests/test_watcher_events.py`, `docs/watcher-preview.md`, and `docs/operator-diagnostics.md` cover stable exit-code diagnostics without stdout/stderr echo. | Hard deterministic preview gate. |
| Helper failure surfaced by watcher | Watcher preview docs and fake-watcher tests require suppressing helper-adjacent stdout/stderr and reporting only the watcher exit code. | Hard deterministic preview gate. |
| Malformed watcher JSONL | `tests/test_watcher_events.py` and diagnostics docs cover `ERROR: watcher JSONL line <n> is malformed` and no raw JSONL persistence under state. | Hard deterministic preview gate. |
| Invalid embedded helper payload | `tests/test_watcher_events.py`, `docs/watcher-preview.md`, and `docs/operator-diagnostics.md` cover `ERROR: watcher output could not be captured safely` without echoing schema validation details or observed-content canaries. | Hard privacy/preview gate. |
| Watcher timeout | `tests/test_watcher_events.py` and diagnostics docs cover `ERROR: watcher timed out` without printing partial stdout. | Hard deterministic preview gate. |
| Heartbeat-only run | `tests/test_watcher_events.py`, `docs/watcher-preview.md`, `docs/manual-smoke-evidence-ledger.md`, and `docs/release-v0.1.18.md` require or record `captures_written = 0`, `heartbeats > 0`, no capture artifacts, and no raw JSONL under temporary state. | Diagnostic liveness evidence, not capture success. |
| Duplicate skip | `tests/test_watcher_events.py` covers `duplicates_skipped` without duplicate capture writes. | Hard deterministic preview gate. |
| Denylist or lock-screen skip | `tests/test_watcher_events.py` covers `denylisted_skipped`, no capture artifact, no raw watcher JSONL under state, and no searchable observed content. `tests/test_cli.py` and `tests/test_uia_helper_contract.py` cover content-free title-denylist diagnostics. | Hard privacy/preview gate. |
| Raw watcher JSONL persistence | Product `watch --watcher` consumes watcher stdout in memory; tests assert no raw `.jsonl` stream is persisted under `WINCHRONICLE_HOME`. Harness smoke may use a temporary fake-helper event file outside state that is deleted after the run. | Hard privacy/preview gate. |
| Product targeted-capture pass-through | `tests/test_compatibility_contracts.py`, scorecards, and docs reject forbidden target/control/privacy flags passed through `--helper-arg` and `--watcher-arg`. | Hard boundary gate. |

## Drift Decision

AH2 found no new helper/watcher diagnostics drift after `v0.1.18`. The reviewed
docs, scorecards, and tests already cover timeout, malformed output, invalid
embedded helper payloads, no observed-content echo, duplicate skip, denylist
skip, heartbeat-only liveness, diagnostic artifact policy, raw watcher JSONL
non-persistence, product targeted-capture pass-through rejection, and current
`v0.1.18` manual-smoke matrix rows.

No schema, successful CLI/MCP JSON, helper/watcher capture behavior, privacy
storage behavior, or capture-surface change is warranted. AH2 therefore
refreshes documentation/tests only and keeps the AF2 content-free diagnostic
fix plus AG2 product targeted-capture pass-through review as historical
evidence.

Fresh manual UIA smoke remains outside default CI. The `v0.1.18`
release-readiness record reran fresh hard-gate manual UIA smoke because
privacy-check validation behavior changed after `v0.1.17`; AH2 does not require
new manual smoke because it changes no product behavior, helper/watcher
behavior, manual smoke scripts, capture behavior, privacy behavior, CLI/MCP
shape, capture surfaces, or release approval requirements.

The next smallest implementation task is to land this AH2 review through PR
and post-merge Windows Harness validation, then start AH3 MCP and memory
contract review.

## Validation Log

- `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_watcher_events.py tests/test_uia_helper_quality_matrix.py tests/test_version_identity.py -q` - passed, 108 tests.
- `python -m pytest -q` - passed, 207 tests.
- `git diff --check` - passed.
- `git diff --name-only -- src\winchronicle resources pyproject.toml` - passed; printed no files, confirming AH2 is docs/tests only with no product/runtime/version diff.
- Current-entry stale AH1/current post-v0.1.17 helper/watcher wording scan across
  `README.md`, current docs, and current doc tests - passed with no matches in
  current entry documents.
- `python harness/scripts/run_harness.py` - passed, including 207 pytest tests,
  helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke,
  install CLI smoke, privacy check, fixture capture/search/memory,
  deterministic watcher fixture, and watcher fake-helper smoke.

## Boundary Confirmation

This sweep does not authorize screenshot capture, OCR, audio recording,
keyboard capture, clipboard capture, network upload, LLM calls, desktop
control, MCP write tools, arbitrary file read tools, product targeted capture,
daemon/service install, polling capture loops, default background capture, or
live UIA smoke in default CI.
