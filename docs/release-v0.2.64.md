# v0.2.64 Release Record

This record tracks the `v0.2.64` Workday runner-launch safe-failure release path.
It records commands, results, environment notes, and local artifact paths only.
It does not commit observed screen-content artifacts.

## Release Decision

`v0.2.64` is warranted by a Workday CLI safety fix: background runner launch
failures are now converted into a stable `workday_runner_start_failed` Workday
error before any active session marker is written. Natural-language
`workday intent ... --execute` prints concise Chinese failure text instead of
leaking raw local exception text, paths, tracebacks, or token-canary-like
strings.

Publication status: published final release.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.2.64` |
| Stage | `v0.2.64` Workday runner-launch safe-failure release |
| Evidence date | 2026-06-20, Asia/Shanghai |
| Publication status | Published final release |
| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.64 |
| Published at | `2026-06-20T06:26:32Z` |
| Final tag target | `c78839cdfc464e5eff9c927033875bb95e73f6e0` |
| Windows Harness | https://github.com/YSCJRH/WinChronicle/actions/runs/27862752420, head `c78839cdfc464e5eff9c927033875bb95e73f6e0`, conclusion `success` |
| Previous package/tag release | `v0.2.63` |
| Previous package/tag release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.63 |
| Manual smoke artifact root | `C:\Users\34793\AppData\Local\Temp\winchronicle-v0264-smoke-9df8021e9178494bb198dcb41871d39e` |

Environment:

- Windows interactive desktop, PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| RED: `python -m pytest tests/test_workday.py::test_workday_start_reports_safe_json_when_runner_launch_fails tests/test_workday.py::test_workday_intent_execute_start_reports_safe_text_when_runner_launch_fails -q` | Failed before fix | `2 failed`; raw `OSError` escaped from `subprocess.Popen` |
| RED: `python -m pytest tests/test_workday.py::test_workday_start_keeps_safe_error_when_runner_launch_cleanup_fails -q` | Failed before cleanup hardening | cleanup `OSError` masked `workday_runner_start_failed` |
| `python -m pytest tests/test_workday.py -k "runner_launch_fails or runner_launch_cleanup_fails or default_build_output_is_missing or default_helper_build_output_is_missing" -q` | Pass | `6 passed, 50 deselected` |
| `python -m pytest tests/test_workday.py -q` | Pass | `56 passed` |
| `python -m pytest tests/test_cli.py tests/test_codex_workday_plugin.py tests/test_privacy_check.py tests/test_mcp_tools.py -q` | Pass | `59 passed` |
| `python -m pytest -q` | Pass | `425 passed` |
| `git diff --check` | Pass | no whitespace errors |
| `python harness/scripts/run_harness.py` | Pass | full harness passed: 425 pytest tests, release validators, helper/watcher builds with 0 warnings and 0 errors, quick demo, productization self-eval, watcher smokes, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke |

## Manual UIA Smoke Gates

Manual smoke used local temporary artifacts only. Do not commit the artifact JSON
files; they may contain observed screen content.

| Gate | Result | Evidence |
| --- | --- | --- |
| Notepad targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-notepad.ps1 -ArtifactDir <artifact-root>\notepad -TimeoutSeconds 30`; artifact `<artifact-root>\notepad\notepad-capture.json` |
| Edge targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-edge.ps1 -ArtifactDir <artifact-root>\edge -TimeoutSeconds 45`; artifact `<artifact-root>\edge\edge-capture.json` |
| VS Code metadata smoke | Pass with diagnostic warning | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -ArtifactDir <artifact-root>\vscode-metadata -TimeoutSeconds 45`; metadata passed, editor marker was not exposed through UIA |
| VS Code strict Monaco marker | Diagnostic failure, non-blocking | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -Strict -ArtifactDir <artifact-root>\vscode-strict -TimeoutSeconds 45`; known Monaco/UIA limitation |
| Fake-helper monitor watcher | Pass | `python -m winchronicle monitor --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper python --helper-arg harness/scripts/fake_uia_helper.py --duration 1 --heartbeat-ms 250 --capture-on-start --session-id release-fake-helper-v0264` returned `captures_written: 1`, `duplicates_skipped: 0`, `denylisted_skipped: 0`, `heartbeats: 3`, and local session/report paths under the temporary `WINCHRONICLE_HOME` |

## Release Notes

- Handles background Workday runner launch `OSError` with a safe JSON Workday
  error instead of an uncaught traceback.
- Makes launch-failure cleanup best-effort so cleanup errors cannot mask the
  stable `workday_runner_start_failed` result.
- Makes natural-language `workday intent ... --execute` runner-launch failures
  use concise Chinese `工作记录未开始` text output and a `winchronicle doctor`
  recovery hint.
- Aligns package, runtime, plugin, and MCP server version identity to `0.2.64`.

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

Publication was verified against the `v0.2.64` GitHub release, remote tag target,
and Windows Harness run. `docs/release-evidence.md`,
`docs/release-checklist.md`, and `docs/manual-smoke-evidence-ledger.md` now
record `v0.2.64` as the latest package/tag release, and no
`Next Package Release Preflight` section remains for the published project
version.
