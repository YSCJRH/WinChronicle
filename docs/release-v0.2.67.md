# v0.2.67 Release Record

This record tracks the `v0.2.67` Workday stop path-boundary release path. It
records commands, results, environment notes, and local artifact paths only. It
does not commit observed screen-content artifacts.

## Release Decision

`v0.2.67` is warranted by a Workday stop privacy-boundary fix: `workday stop`
now derives its stop marker, final-result path, and checkpoint path from the
sanitized active-marker `session_id` under the local WinChronicle state layout.
A contaminated or stale `workday-active.json` can no longer redirect stop to
marker-controlled external files or make stop summarize marker-controlled JSON.

Publication status: published.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.2.67` |
| Stage | `v0.2.67` Workday stop path-boundary release |
| Evidence date | 2026-06-29, Asia/Shanghai |
| Publication status | Published, not a draft, not a prerelease |
| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.67 |
| Published at | `2026-06-29T01:26:14Z` |
| Final tag target | `557cc6d6f804efd6fc26b89cd3e27e0ded2b9bff` |
| Windows Harness | Passed, https://github.com/YSCJRH/WinChronicle/actions/runs/28342791863, head `557cc6d6f804efd6fc26b89cd3e27e0ded2b9bff` |
| Previous package/tag release | `v0.2.66` |
| Previous package/tag release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.66 |
| Previous package/tag Windows Harness | Passed, https://github.com/YSCJRH/WinChronicle/actions/runs/27865327396, head `aef5a89d94707c11b7a2e63a7fdddce46649e4b7` |
| Manual smoke artifact root | `C:\Users\34793\AppData\Local\Temp\winchronicle-v0267-smoke-50de1593353a48e1a914732ade23a660` |

Environment:

- Windows interactive desktop, PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0.202`.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| RED: `python -m pytest tests/test_workday.py::test_workday_stop_ignores_marker_controlled_external_paths -q` | Failed before fix | `1 failed`; old code treated marker-controlled external result JSON as `final_result` |
| `python -m pytest tests/test_workday.py::test_workday_stop_ignores_marker_controlled_external_paths -q` | Pass | `1 passed` |
| `python -m pytest tests/test_workday.py::test_workday_stop_uses_checkpoint_when_active_pid_is_malformed tests/test_workday.py::test_workday_stop_derives_stop_marker_when_marker_parent_is_missing tests/test_workday.py::test_workday_stop_ignores_marker_controlled_external_paths tests/test_workday.py::test_workday_stop_preserves_unrecovered_runner_failure_source tests/test_workday.py::test_workday_stop_returns_final_result_when_active_marker_cleanup_fails tests/test_workday.py::test_workday_stop_uses_checkpoint_when_active_marker_cleanup_fails tests/test_workday.py::test_workday_stop_recovers_summary_from_capture_buffer_when_result_is_missing -q` | Pass | `7 passed` |
| Static active-marker path scan | Pass | `rg -n 'active\["session_id"\]\|active\["stop_file"\]\|active\["result_file"\]\|Path\(active\.get\("checkpoint_file"' src\winchronicle\workday.py` returned no matches |
| `python -m pytest tests/test_workday.py -q` | Pass | `64 passed`; run with escalated process-control access after the sandbox blocked the pre-existing runner-cleanup process-tree test |
| `python -m pytest tests/test_cli.py tests/test_codex_workday_plugin.py tests/test_privacy_check.py tests/test_mcp_tools.py -q` | Pass | `59 passed` |
| `python -m pytest tests/test_version_identity.py tests/test_release_evidence_validator.py tests/test_manual_smoke_freshness_validator.py tests/test_operator_diagnostics_docs.py -q` | Pass | `77 passed` |
| `python harness\scripts\check_release_evidence.py --project pyproject.toml --require-release-state docs\release-evidence.md` | Pass | pre-publication run accepted current `v0.2.66` plus `v0.2.67` preflight; post-publication rerun accepted current `v0.2.67` release evidence without preflight |
| `python harness\scripts\check_manual_smoke_freshness.py --project pyproject.toml --ledger docs\manual-smoke-evidence-ledger.md --guide docs\release-evidence.md --checklist docs\release-checklist.md` | Pass | package/tag release and manual UIA smoke source are separated before and after publication |
| `git diff --check` | Pass | no whitespace errors |
| `python -m pytest -q` | Pass | pre-publication run `433 passed in 198.00s`; post-publication reconciliation rerun `433 passed in 246.53s`; both used escalated process-control access |
| `python harness\scripts\run_harness.py` | Pass | pre-publication `WinChronicle harness passed` with internal pytest `433 passed in 169.52s`; post-publication reconciliation rerun passed with internal pytest `433 passed in 226.32s`; release validators, manual-smoke freshness validator, .NET helper/watcher builds, quick demo, MCP smoke, watcher smokes, productization self-eval, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and fake-helper watcher smoke passed |

## Manual UIA Smoke Gates

Manual smoke must use local temporary artifacts only. Do not commit the artifact
JSON files; they may contain observed screen content.

| Gate | Result | Evidence |
| --- | --- | --- |
| Notepad targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-notepad.ps1 -ArtifactDir C:\Users\34793\AppData\Local\Temp\winchronicle-v0267-smoke-50de1593353a48e1a914732ade23a660\notepad -TimeoutSeconds 30`; artifact `notepad\notepad-capture.json` |
| Edge targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-edge.ps1 -ArtifactDir C:\Users\34793\AppData\Local\Temp\winchronicle-v0267-smoke-50de1593353a48e1a914732ade23a660\edge -TimeoutSeconds 45`; artifact `edge\edge-capture.json` |
| VS Code metadata smoke | Pass with diagnostic warning | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -ArtifactDir C:\Users\34793\AppData\Local\Temp\winchronicle-v0267-smoke-50de1593353a48e1a914732ade23a660\vscode-metadata -TimeoutSeconds 45`; editor marker was not exposed through UIA; artifact `vscode-metadata\vscode-capture.json` |
| VS Code strict Monaco marker | Diagnostic failure, non-blocking | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -Strict -ArtifactDir C:\Users\34793\AppData\Local\Temp\winchronicle-v0267-smoke-50de1593353a48e1a914732ade23a660\vscode-strict -TimeoutSeconds 45`; known Monaco/UIA limitation persisted; artifact `vscode-strict\vscode-capture.json` |
| Fake-helper monitor watcher | Pass | `$env:WINCHRONICLE_HOME='C:\Users\34793\AppData\Local\Temp\winchronicle-v0267-smoke-50de1593353a48e1a914732ade23a660\home'; python -m winchronicle monitor --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper python --helper-arg harness/scripts/fake_uia_helper.py --duration 1 --heartbeat-ms 250 --capture-on-start --session-id release-fake-helper-v0267`; `captures_written=1`, `duplicates_skipped=0`, `heartbeats=1` |

## Release Notes

- Derives `workday stop` stop-marker, result, and checkpoint paths from the
  sanitized active-marker session id under the local WinChronicle state root.
- Prevents marker-controlled external result/checkpoint JSON from becoming the
  stop summary source.
- Preserves Workday stop fallback behavior for malformed PIDs, missing final
  results, checkpoint recovery, active-marker cleanup failures, and
  unrecovered runner failures.
- Aligns package, runtime, plugin, and MCP server version identity to `0.2.67`.

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

Published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.67.
Remote tag `v0.2.67` points to
`557cc6d6f804efd6fc26b89cd3e27e0ded2b9bff`. GitHub Windows Harness run
https://github.com/YSCJRH/WinChronicle/actions/runs/28342791863 passed on the
same head SHA. Post-publication reconciliation updates
`docs/release-evidence.md`, `docs/release-checklist.md`, and
`docs/manual-smoke-evidence-ledger.md` so `v0.2.67` is the current package/tag
release and latest full manual UIA smoke source.
