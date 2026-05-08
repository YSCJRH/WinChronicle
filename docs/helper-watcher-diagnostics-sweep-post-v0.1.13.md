# Helper And Watcher Diagnostics Sweep After v0.1.13

This AB2 sweep reviews helper and watcher preview diagnostics after the
published `v0.1.13` baseline and AB1 public metadata audit. It records current
evidence only. It does not change product behavior, schemas, CLI/MCP JSON
shape, helper/watcher behavior, privacy behavior, or capture surfaces.

## Reviewed Surfaces

| Surface | Evidence | Assessment |
| --- | --- | --- |
| Helper quality matrix | `docs/uia-helper-quality-matrix.md` lists deterministic fixtures, wrapper diagnostics, harness-only targeted smoke, manual frontmost smoke, artifact policy, privacy risk, and blocking status. | Current matrix still separates hard automated gates, hard manual gates, conditional VS Code metadata, and diagnostic-only Monaco/frontmost behavior. |
| Watcher preview docs | `docs/watcher-preview.md` documents explicit/time-bounded preview usage, manual smoke expectations, operator-facing diagnostics, deterministic coverage, and no raw JSONL persistence. | Current docs cover preview reliability without promoting live watcher smoke to default CI. |
| Operator diagnostics | `docs/operator-diagnostics.md` lists stable helper and watcher diagnostic lines and the no observed-content echo policy. | Current guide gives operator-facing signals without raw helper JSON, raw watcher JSONL, screenshots, OCR output, or observed text. |
| Capture quality scorecard | `harness/scorecards/capture-quality.md` requires helper wrapper diagnostics, helper harness-only targeting, watcher reliability modes, fake-helper watcher smoke, and no raw watcher JSONL persistence. | Scorecard remains aligned with v0.1 preview boundaries. |
| Deterministic tests | `tests/test_cli.py`, `tests/test_uia_helper_contract.py`, `tests/test_watcher_events.py`, and `tests/test_operator_diagnostics_docs.py` cover helper wrapper failure modes, UIA traversal budget/stale metadata, watcher skip/failure modes, and docs signals. | No missing deterministic coverage was found for the AB2 failure-mode list. |

## Failure-mode Matrix

| Required mode | Current evidence | Blocking status |
| --- | --- | --- |
| Helper timeout | `tests/test_uia_helper_contract.py` and `docs/operator-diagnostics.md` cover `ERROR: helper timed out`. | Hard deterministic/wrapper gate. |
| Helper invalid JSON | `tests/test_cli.py` and diagnostics docs cover `ERROR: helper returned invalid JSON`. | Hard deterministic/wrapper gate. |
| Helper empty stdout | `docs/uia-helper-quality-matrix.md` and helper wrapper diagnostics cover the stable no-capture path without storing observed content. | Hard deterministic/wrapper gate. |
| Helper nonzero exit | `tests/test_cli.py` and diagnostics docs cover `ERROR: helper failed with exit code <code>`. | Hard deterministic/wrapper gate. |
| Watcher nonzero exit | `tests/test_watcher_events.py`, `docs/watcher-preview.md`, and `docs/operator-diagnostics.md` cover stable exit-code diagnostics without stdout/stderr echo. | Hard deterministic preview gate. |
| Helper failure surfaced by watcher | Watcher preview docs require suppressing helper-adjacent stdout/stderr and reporting the watcher exit code. | Hard deterministic preview gate. |
| Malformed watcher JSONL | `tests/test_watcher_events.py` and diagnostics docs cover `ERROR: watcher JSONL line <n> is malformed`. | Hard deterministic preview gate. |
| Watcher timeout | `tests/test_watcher_events.py` and diagnostics docs cover `ERROR: watcher timed out`. | Hard deterministic preview gate. |
| Heartbeat-only run | `tests/test_watcher_events.py` and watcher preview docs require `captures_written = 0`, `heartbeats > 0`, no capture artifacts, and no raw JSONL. | Diagnostic liveness evidence, not capture success. |
| Duplicate skip | `tests/test_watcher_events.py` covers `duplicates_skipped` without duplicate capture writes. | Hard deterministic preview gate. |
| Denylist or lock-screen skip | `tests/test_watcher_events.py` covers `denylisted_skipped` and no searchable observed content. | Hard privacy/preview gate. |
| Raw watcher JSONL persistence | `tests/test_watcher_events.py` asserts no raw `.jsonl` stream is persisted under temporary `WINCHRONICLE_HOME`. | Hard privacy/preview gate. |

## No-drift Decision

AB2 found no required helper or watcher product-code change. The reviewed docs,
scorecards, and tests already cover timeout, malformed output, no
observed-content echo, duplicate skip, denylist skip, heartbeat-only liveness,
and diagnostic artifact policy.

No fresh manual UIA smoke is required for this AB2 sweep because it changes
only documentation/tests and does not change helper behavior, watcher product
behavior, manual smoke scripts, capture behavior, privacy behavior,
product CLI/MCP shape, capture surfaces, or release approver requirements.

The next smallest implementation task is AB3: re-check read-only MCP examples,
memory docs, and deterministic demo guidance for trust-boundary and
response-shape consistency.

## Boundary Confirmation

This sweep does not authorize screenshot capture, OCR, audio recording,
keyboard capture, clipboard capture, network upload, LLM calls, desktop
control, MCP write tools, product targeted capture, daemon/service install,
polling capture loops, default background capture, or live UIA smoke in
default CI.
