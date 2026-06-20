# v0.2.65 Release Record

This record tracks the `v0.2.65` Workday watcher-launch safe-failure release
path. It records commands, results, environment notes, and local artifact paths
only. It does not commit observed screen-content artifacts.

## Release Decision

`v0.2.65` is warranted by a Workday runner safety and state-accuracy fix:
watcher process launch failures inside `run_workday()` are now converted into
the stable `workday_watcher_start_failed` Workday error without preserving the
raw local exception as an exception cause. The hidden `workday run` CLI recovery
path writes that stable runner error into the local result payload, and
`workday stop` preserves unrecovered runner-failure state instead of relabeling
missing summaries as `final_result`.

Publication status: published final release.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.2.65` |
| Stage | `v0.2.65` Workday watcher-launch safe-failure release |
| Evidence date | 2026-06-20, Asia/Shanghai |
| Publication status | Published final release |
| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.65 |
| Published at | `2026-06-20T07:15:05Z` |
| Final tag target | `de6e37ad386ba299f9ee82e6a8b4e0d0ff876884` |
| Windows Harness | https://github.com/YSCJRH/WinChronicle/actions/runs/27863842793, head `de6e37ad386ba299f9ee82e6a8b4e0d0ff876884`, conclusion `success` |
| Previous package/tag release | `v0.2.64` |
| Previous package/tag release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.64 |
| Manual smoke artifact root | `C:\Users\34793\AppData\Local\Temp\winchronicle-v0265-smoke-546c79c9bfff47c9a8469fd09ae85196` |

Environment:

- Windows interactive desktop, PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| RED: `python -m pytest tests/test_workday.py::test_workday_run_reports_safe_error_when_watcher_launch_fails tests/test_workday.py::test_workday_run_cli_writes_safe_result_when_watcher_launch_fails -q` | Failed before fix | `2 failed`; direct `run_workday()` leaked raw watcher-launch `OSError`, and CLI recovery wrote generic `workday_runner_failed_before_final_result` |
| RED: `python -m pytest tests/test_workday.py::test_workday_stop_preserves_unrecovered_runner_failure_source -q` | Failed before stop-path fix | `summary_source` was relabeled to `final_result` for an unrecovered runner failure with no summary |
| `python -m pytest tests/test_workday.py::test_workday_run_reports_safe_error_when_watcher_launch_fails tests/test_workday.py::test_workday_run_cli_writes_safe_result_when_watcher_launch_fails tests/test_workday.py::test_workday_stop_preserves_unrecovered_runner_failure_source -q` | Pass | `3 passed` |
| `python -m pytest tests/test_workday.py -q` | Pass | `59 passed` |
| `python -m pytest tests/test_cli.py tests/test_codex_workday_plugin.py tests/test_privacy_check.py tests/test_mcp_tools.py -q` | Pass | `59 passed` |
| `python -m pytest tests/test_version_identity.py tests/test_release_evidence_validator.py tests/test_manual_smoke_freshness_validator.py tests/test_operator_diagnostics_docs.py -q` | Pass | `77 passed` |
| `python harness\scripts\check_release_evidence.py --project pyproject.toml --require-release-state docs\release-evidence.md` | Pass | release evidence accepted current `v0.2.64` plus `v0.2.65` preflight |
| `python harness\scripts\check_manual_smoke_freshness.py --project pyproject.toml --ledger docs\manual-smoke-evidence-ledger.md --guide docs\release-evidence.md --checklist docs\release-checklist.md` | Pass | package/tag release and manual UIA smoke source are separated |
| `python -m pytest -q` | Pass | `428 passed` |
| `python harness\scripts\run_harness.py` | Pass | full harness passed: 428 pytest tests, release validators, helper/watcher builds with 0 warnings and 0 errors, quick demo, productization self-eval, watcher smokes, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke |

## Manual UIA Smoke Gates

Manual smoke used local temporary artifacts only. Do not commit the artifact JSON
files; they may contain observed screen content.

| Gate | Result | Evidence |
| --- | --- | --- |
| Notepad targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-notepad.ps1 -ArtifactDir <artifact-root>\notepad -TimeoutSeconds 30`; artifact `<artifact-root>\notepad\notepad-capture.json` |
| Edge targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-edge.ps1 -ArtifactDir <artifact-root>\edge -TimeoutSeconds 45`; artifact `<artifact-root>\edge\edge-capture.json` |
| VS Code metadata smoke | Pass with diagnostic warning | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -ArtifactDir <artifact-root>\vscode-metadata -TimeoutSeconds 45`; metadata passed, editor marker was not exposed through UIA |
| VS Code strict Monaco marker | Diagnostic failure, non-blocking | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -Strict -ArtifactDir <artifact-root>\vscode-strict -TimeoutSeconds 45`; known Monaco/UIA limitation |
| Fake-helper monitor watcher | Pass | `python -m winchronicle monitor --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper python --helper-arg harness/scripts/fake_uia_helper.py --duration 1 --heartbeat-ms 250 --capture-on-start --session-id release-fake-helper-v0265` returned `captures_written: 1`, `duplicates_skipped: 0`, `denylisted_skipped: 0`, `heartbeats: 4`, and local session/report paths under the temporary `WINCHRONICLE_HOME` |

## Release Notes

- Converts direct `run_workday()` watcher launch `OSError` into stable
  `workday_watcher_start_failed` without retaining the raw exception cause.
- Writes stable watcher-launch failure metadata into the hidden `workday run`
  recovery result payload without echoing raw exception text, tracebacks, or
  token-canary-like strings.
- Preserves unrecovered runner-failure state through `workday stop` instead of
  relabeling missing summaries as `final_result`.
- Aligns package, runtime, plugin, and MCP server version identity to `0.2.65`.

## Privacy And Scope Confirmation

- Local-first: captured content remains local; no cloud or network upload is
  implemented.
- UIA-first and harness-first boundaries remain in place.
- Screenshots, OCR, audio recording, keyboard capture, clipboard capture, LLM
  calls, desktop control, MCP write tools, daemon/service installation, polling
  capture loops, default background capture, and product targeted capture remain
  out of scope.
- Observed content remains untrusted and must remain marked as
  `untrusted_observed_content` in captures, memory, CLI search, session
  summaries, and MCP responses.
- Password fields and obvious secrets must not be stored, including API keys,
  private keys, JWTs, GitHub tokens, Slack tokens, and token canaries.

## Publication Reconciliation

Publication was verified against the `v0.2.65` GitHub release, remote tag
target, and Windows Harness run. `docs/release-evidence.md`,
`docs/release-checklist.md`, and `docs/manual-smoke-evidence-ledger.md` now
record `v0.2.65` as the latest package/tag release, and no
`Next Package Release Preflight` section remains for the published project
version.
