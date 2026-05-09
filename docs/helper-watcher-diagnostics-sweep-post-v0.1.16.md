# Helper And Watcher Diagnostics Sweep After v0.1.16

This AF2 sweep reviews helper and watcher preview diagnostics after the
published `v0.1.16` final release, AF1 public metadata audit, and AF1
completion reconciliation. It records then-current deterministic evidence and
added a narrow content-free CLI diagnostic fix. It does not change schemas,
successful CLI/MCP JSON shape, helper/watcher capture behavior, privacy storage
behavior, or capture surfaces. This sweep is now historical; the post-v0.1.17
AG2 sweep superseded it, and the active helper/watcher diagnostics review is
the post-v0.1.18 AH2 sweep.

## Reviewed Surfaces

| Surface | Evidence | Assessment |
| --- | --- | --- |
| Helper quality matrix | `docs/uia-helper-quality-matrix.md` lists deterministic fixtures, wrapper diagnostics, harness-only targeted smoke, manual frontmost smoke, artifact policy, privacy risk, and blocking status. | The then-current matrix separated hard automated gates, hard manual gates, and diagnostic/manual confidence gates without promoting live UIA smoke to default CI. |
| Watcher preview docs | `docs/watcher-preview.md` documents explicit/time-bounded preview usage, manual smoke expectations, operator-facing diagnostics, deterministic coverage, and no raw watcher JSONL persistence under product preview state. | The then-current docs covered preview reliability without authorizing daemon/service install, default background capture, polling capture loops, or live watcher CI. |
| Operator diagnostics | `docs/operator-diagnostics.md` lists stable helper and watcher diagnostic lines and the no observed-content echo policy. | The then-current guide told operators to record stable diagnostic lines and local artifact paths only, not raw helper JSON, raw watcher JSONL, screenshots, OCR output, or observed text. |
| Capture quality scorecard | `harness/scorecards/capture-quality.md` requires helper wrapper diagnostics, helper harness-only targeting, watcher reliability modes, fake-helper watcher smoke, heartbeat-only handling, and raw watcher JSONL policy. | Scorecard remains aligned with v0.1 preview boundaries and treats heartbeat-only watcher runs as liveness evidence, not capture success. |
| Deterministic tests | `tests/test_cli.py`, `tests/test_uia_helper_contract.py`, `tests/test_watcher_events.py`, `tests/test_operator_diagnostics_docs.py`, and `tests/test_compatibility_contracts.py` cover helper wrapper failure modes, content-free skip diagnostics, UIA traversal budget/stale metadata, watcher skip/failure modes, and docs signals. | AF2 added focused CLI helper-timeout, `watch --events` invalid-helper-payload no-echo, and watcher denylist artifact assertions; no capture behavior change is warranted. |

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
| Heartbeat-only run | `tests/test_watcher_events.py` and watcher preview docs require `captures_written = 0`, `heartbeats > 0`, no capture artifacts, and no raw JSONL under temporary state. | Diagnostic liveness evidence, not capture success. |
| Duplicate skip | `tests/test_watcher_events.py` covers `duplicates_skipped` without duplicate capture writes. | Hard deterministic preview gate. |
| Denylist or lock-screen skip | `tests/test_watcher_events.py` covers `denylisted_skipped`, no capture artifact, no raw watcher JSONL under state, and no searchable observed content. `tests/test_cli.py` and `tests/test_uia_helper_contract.py` cover content-free title-denylist diagnostics. | Hard privacy/preview gate. |
| Raw watcher JSONL persistence | Product `watch --watcher` consumes watcher stdout in memory; tests assert no raw `.jsonl` stream is persisted under `WINCHRONICLE_HOME`. Harness smoke may use a temporary fake-helper event file outside state that is deleted after the run. | Hard privacy/preview gate. |

## Drift Decision

AF2 found one helper/watcher diagnostics drift in the `watch --events` error
path: invalid embedded helper payloads could let schema validation details echo
observed content. AF2 fixed that path with a stable content-free diagnostic
without changing schemas, successful CLI/MCP JSON shape, helper/watcher capture
behavior, privacy storage behavior, or capture surfaces. It also added focused
deterministic evidence for helper-timeout CLI reporting, denylist-skip artifact
absence, and the fake-helper watcher smoke JSONL exception. The reviewed docs,
scorecards, and tests cover timeout, malformed output, invalid embedded helper
payloads, no observed-content echo, duplicate skip, denylist skip,
heartbeat-only liveness, and diagnostic artifact policy.

Fresh manual UIA smoke remains outside default CI. The AE2 manual UIA smoke is
fresh for the published `v0.1.16` final release record, but future
release-readiness work must make a new freshness decision if product behavior,
helper/watcher behavior, manual smoke scripts, capture behavior, privacy
behavior, CLI/MCP shape, capture surfaces, or release approval requirements
change.

The next smallest implementation task is to land this AF2 review through PR
and post-merge Windows Harness validation, then record AF2 completion before
starting AF3 MCP and memory contract review.

## Boundary Confirmation

This sweep does not authorize screenshot capture, OCR, audio recording,
keyboard capture, clipboard capture, network upload, LLM calls, desktop
control, MCP write tools, arbitrary file read tools, product targeted capture,
daemon/service install, polling capture loops, default background capture, or
live UIA smoke in default CI.
