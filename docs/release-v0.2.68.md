# v0.2.68 Release Record

This record tracks the `v0.2.68` Workday start privacy-boundary and runner
cleanup release path. It records commands, results, environment notes, and
local artifact paths only. It does not commit observed screen-content artifacts.

## Release Decision

`v0.2.68` is warranted by a Workday start privacy-boundary fix and cleanup
hardening:

- `workday start` now sanitizes the existing active-marker session id and PID
  before returning `workday_session_already_active`.
- Windows runner cleanup now snapshots descendant PIDs, waits for the process
  tree to exit, and applies a bounded fallback termination pass when needed.

Publication status: published.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.2.68` |
| Stage | `v0.2.68` Workday start privacy-boundary release |
| Evidence date | 2026-06-29, Asia/Shanghai |
| Publication status | Published, not a draft, not a prerelease |
| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.68 |
| Published at | `2026-06-29T03:35:33Z` |
| Final tag target | `8ad9a5790395a70e2b8569b43d61292ec2f5a586` |
| Windows Harness | Passed, https://github.com/YSCJRH/WinChronicle/actions/runs/28346732386, head `8ad9a5790395a70e2b8569b43d61292ec2f5a586` |
| Previous package/tag release | `v0.2.67` |
| Previous package/tag release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.67 |
| Previous package/tag Windows Harness | Passed, https://github.com/YSCJRH/WinChronicle/actions/runs/28342791863, head `557cc6d6f804efd6fc26b89cd3e27e0ded2b9bff` |
| Manual smoke artifact root | `C:\Users\34793\AppData\Local\Temp\winchronicle-v0268-smoke-54e7f4fa1d0646de9655a64444a0e791` |

Environment:

- Windows interactive desktop, PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0.202`.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| RED: `python -m pytest tests/test_workday.py::test_workday_start_sanitizes_existing_active_marker_response -q` | Failed before fix | `1 failed`; old code returned the raw active-marker `session_id` instead of the redacted slug |
| `python -m pytest tests/test_workday.py::test_workday_start_sanitizes_existing_active_marker_response tests/test_workday.py::test_workday_duplicate_start_is_rejected_until_stopped -q` | Pass | `2 passed` |
| Existing cleanup regression before process-tree fix | Failed | `test_workday_start_cleans_up_runner_when_active_marker_write_fails` repeatedly left the sentinel watcher PID running past the test wait window |
| `python -m pytest tests/test_workday.py::test_workday_start_cleans_up_runner_when_active_marker_write_fails -q` | Pass | `1 passed in 11.99s` after descendant PID wait/fallback cleanup |
| `python -m pytest tests/test_workday.py::test_workday_start_sanitizes_existing_active_marker_response tests/test_workday.py::test_workday_duplicate_start_is_rejected_until_stopped tests/test_workday.py::test_workday_start_cleans_up_runner_when_active_marker_write_fails -q` | Pass | `3 passed in 21.57s` |
| `python -m pytest tests/test_workday.py -q` | Pass | `65 passed in 143.97s` |
| `python -m pytest -q` | Pass | final tree rerun `434 passed in 233.23s` |
| `python -m pytest tests/test_version_identity.py tests/test_release_evidence_validator.py tests/test_operator_diagnostics_docs.py::test_release_evidence_freshness_guard_labels_inherited_manual_smoke tests/test_operator_diagnostics_docs.py::test_manual_smoke_ledger_tracks_freshness_without_observed_artifacts -q` | Pass | `27 passed in 11.80s` |
| `python -m pytest tests/test_codex_workday_plugin.py::test_codex_workday_plugin_manifest_is_repo_scoped_and_versioned tests/test_manual_smoke_freshness_validator.py::test_manual_smoke_freshness_validator_accepts_repository_docs tests/test_release_evidence_validator.py::test_release_evidence_guide_passes_release_state_validator -q` | Pass | `3 passed in 2.96s` |
| `python harness\scripts\check_release_evidence.py --project pyproject.toml --require-release-state docs\release-evidence.md` | Pass | pre-publication run accepted current `v0.2.67` plus `v0.2.68` preflight; post-publication rerun accepted current `v0.2.68` release evidence without preflight |
| `python harness\scripts\check_manual_smoke_freshness.py --project pyproject.toml --ledger docs\manual-smoke-evidence-ledger.md --guide docs\release-evidence.md --checklist docs\release-checklist.md` | Pass | package/tag release and manual UIA smoke source are explicitly separated |
| `git diff --check` | Pass | no whitespace errors |
| `python harness\scripts\run_harness.py` | Pass | `WinChronicle harness passed`; final tree run included internal pytest `434 passed in 186.97s`; release validators, manual-smoke freshness validator, .NET helper/watcher builds, quick demo, productization self-eval, watcher smokes, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and fake-helper watcher smoke passed |

## Manual UIA Smoke Gates

Manual smoke uses local temporary artifacts only. Do not commit the artifact
JSON files; they may contain observed screen content.

| Gate | Result | Evidence |
| --- | --- | --- |
| Notepad targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-notepad.ps1 -ArtifactDir C:\Users\34793\AppData\Local\Temp\winchronicle-v0268-smoke-54e7f4fa1d0646de9655a64444a0e791\notepad -TimeoutSeconds 30`; artifact `notepad\notepad-capture.json` |
| Edge targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-edge.ps1 -ArtifactDir C:\Users\34793\AppData\Local\Temp\winchronicle-v0268-smoke-54e7f4fa1d0646de9655a64444a0e791\edge -TimeoutSeconds 45`; artifact `edge\edge-capture.json` |
| VS Code metadata smoke | Pass with diagnostic warning | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -ArtifactDir C:\Users\34793\AppData\Local\Temp\winchronicle-v0268-smoke-54e7f4fa1d0646de9655a64444a0e791\vscode-metadata -TimeoutSeconds 45`; editor marker was not exposed through UIA; artifact `vscode-metadata\vscode-capture.json` |
| VS Code strict Monaco marker | Diagnostic failure, non-blocking | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -Strict -ArtifactDir C:\Users\34793\AppData\Local\Temp\winchronicle-v0268-smoke-54e7f4fa1d0646de9655a64444a0e791\vscode-strict -TimeoutSeconds 45`; known Monaco/UIA limitation persisted; artifact `vscode-strict\vscode-capture.json` |
| Fake-helper monitor watcher | Pass | `$env:WINCHRONICLE_HOME='C:\Users\34793\AppData\Local\Temp\winchronicle-v0268-smoke-54e7f4fa1d0646de9655a64444a0e791\home'; python -m winchronicle monitor --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper python --helper-arg harness/scripts/fake_uia_helper.py --duration 1 --heartbeat-ms 250 --capture-on-start --session-id release-fake-helper-v0268`; `captures_written=1`, `duplicates_skipped=0`, `heartbeats=1` |

## Release Notes

- Sanitizes the `workday start` already-active response so contaminated
  `workday-active.json` fields cannot leak raw marker session ids, non-integer
  PID values, observed text, or marker-controlled trust/capture-surface labels.
- Keeps the duplicate-start guard behavior intact while matching the existing
  status/stop active-marker sanitization boundary.
- Hardens Windows runner cleanup after active-marker write failures by waiting
  on the runner process tree rather than only the parent PID.
- Aligns package, runtime, plugin, and MCP server version identity to `0.2.68`.

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

Published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.68.
Remote tag `v0.2.68` points to
`8ad9a5790395a70e2b8569b43d61292ec2f5a586`. GitHub Windows Harness run
https://github.com/YSCJRH/WinChronicle/actions/runs/28346732386 passed on the
same head SHA. Post-publication reconciliation updates
`docs/release-evidence.md`, `docs/release-checklist.md`, and
`docs/manual-smoke-evidence-ledger.md` so `v0.2.68` is the current package/tag
release and latest full manual UIA smoke source.
