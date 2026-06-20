# v0.2.66 Release Record

This record tracks the `v0.2.66` Workday status privacy-boundary release path.
It records commands, results, environment notes, and local artifact paths only.
It does not commit observed screen-content artifacts.

## Release Decision

`v0.2.66` is warranted by a Workday status output boundary fix: JSON status now
builds its active-session response from typed/redacted active-marker metadata,
preserves only sanitized operator focus notes, derives summary/checkpoint reads
from the sanitized session id under the local WinChronicle state layout, and
forces the local Workday status `trust` and `capture_surface` constants. A
contaminated or stale `workday-active.json` can no longer leak arbitrary
observed-content-like fields such as `visible_text`, `focused_text`, instruction
text, bad status metadata, or marker-controlled external summary files through
`winchronicle workday status`.

Publication status: published.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.2.66` |
| Stage | `v0.2.66` Workday status privacy-boundary release |
| Evidence date | 2026-06-20, Asia/Shanghai |
| Publication status | Published, not a draft, not a prerelease |
| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.66 |
| Published at | `2026-06-20T08:23:20Z` |
| Final tag target | `aef5a89d94707c11b7a2e63a7fdddce46649e4b7` |
| Windows Harness | Passed, https://github.com/YSCJRH/WinChronicle/actions/runs/27865327396, head `aef5a89d94707c11b7a2e63a7fdddce46649e4b7` |
| Previous package/tag release | `v0.2.65` |
| Previous package/tag release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.65 |
| Manual smoke artifact root | `C:\Users\34793\AppData\Local\Temp\winchronicle-v0266-smoke-5e9cd6f495e14e5c80143c7520f224a7` |

Environment:

- Windows interactive desktop, PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| RED: `python -m pytest tests/test_workday.py::test_workday_status_filters_contaminated_active_marker_fields -q` | Failed before fix | `1 failed`; `status["trust"]` came from the contaminated active marker as `untrusted_observed_content` |
| RED: `python -m pytest tests/test_workday.py::test_workday_status_sanitizes_active_marker_session_id tests/test_workday.py::test_workday_status_ignores_marker_controlled_external_result_summary -q` | Failed before path/metadata hardening | `2 failed`; raw marker `session_id` leaked, and marker-controlled external result summary was treated as status summary |
| `python -m pytest tests/test_workday.py::test_workday_status_filters_contaminated_active_marker_fields tests/test_workday.py::test_workday_status_sanitizes_active_marker_session_id tests/test_workday.py::test_workday_status_ignores_marker_controlled_external_result_summary tests/test_workday.py::test_workday_status_ignores_marker_controlled_external_checkpoint_summary -q` | Pass | `4 passed` |
| `python -m pytest tests/test_workday.py -q` | Pass | `63 passed` |
| `python -m pytest tests/test_cli.py tests/test_codex_workday_plugin.py tests/test_privacy_check.py tests/test_mcp_tools.py -q` | Pass | `59 passed` |
| `python -m pytest tests/test_version_identity.py tests/test_release_evidence_validator.py tests/test_manual_smoke_freshness_validator.py tests/test_operator_diagnostics_docs.py -q` | Pass | `77 passed` |
| `python harness\scripts\check_release_evidence.py --project pyproject.toml --require-release-state docs\release-evidence.md` | Pass | pre-publication run accepted current `v0.2.65` plus `v0.2.66` preflight; post-publication rerun accepted current `v0.2.66` release evidence without preflight |
| `python harness\scripts\check_manual_smoke_freshness.py --project pyproject.toml --ledger docs\manual-smoke-evidence-ledger.md --guide docs\release-evidence.md --checklist docs\release-checklist.md` | Pass | package/tag release and manual UIA smoke source are separated before and after publication |
| `python -m pytest -q` | Pass | `432 passed in 149.38s` |
| `python harness\scripts\run_harness.py` | Pass | `WinChronicle harness passed`; internal pytest `432 passed in 133.04s`; release validators, manual-smoke freshness validator, .NET helper/watcher builds, quick demo, MCP smoke, watcher smokes, productization self-eval, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and fake-helper watcher smoke passed |

## Manual UIA Smoke Gates

Manual smoke must use local temporary artifacts only. Do not commit the artifact
JSON files; they may contain observed screen content.

| Gate | Result | Evidence |
| --- | --- | --- |
| Notepad targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-notepad.ps1 -ArtifactDir C:\Users\34793\AppData\Local\Temp\winchronicle-v0266-smoke-5e9cd6f495e14e5c80143c7520f224a7\notepad -TimeoutSeconds 30`; artifact `notepad\notepad-capture.json` |
| Edge targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-edge.ps1 -ArtifactDir C:\Users\34793\AppData\Local\Temp\winchronicle-v0266-smoke-5e9cd6f495e14e5c80143c7520f224a7\edge -TimeoutSeconds 45`; artifact `edge\edge-capture.json` |
| VS Code metadata smoke | Pass with diagnostic warning | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -ArtifactDir C:\Users\34793\AppData\Local\Temp\winchronicle-v0266-smoke-5e9cd6f495e14e5c80143c7520f224a7\vscode-metadata -TimeoutSeconds 45`; editor marker was not exposed through UIA; artifact `vscode-metadata\vscode-capture.json` |
| VS Code strict Monaco marker | Diagnostic failure, non-blocking | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -Strict -ArtifactDir C:\Users\34793\AppData\Local\Temp\winchronicle-v0266-smoke-5e9cd6f495e14e5c80143c7520f224a7\vscode-strict -TimeoutSeconds 45`; known Monaco/UIA limitation persisted; artifact `vscode-strict\vscode-capture.json` |
| Fake-helper monitor watcher | Pass | `WINCHRONICLE_HOME=C:\Users\34793\AppData\Local\Temp\winchronicle-v0266-smoke-5e9cd6f495e14e5c80143c7520f224a7\home python -m winchronicle monitor --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper python --helper-arg harness/scripts/fake_uia_helper.py --duration 1 --heartbeat-ms 250 --capture-on-start --session-id release-fake-helper-v0266`; `captures_written=1`, `duplicates_skipped=1`, `heartbeats=4` |

## Release Notes

- Filters `winchronicle workday status` JSON through an explicit active-marker
  allowlist instead of spreading the whole local active marker payload.
- Prevents contaminated active markers from exposing `visible_text`,
  `focused_text`, instruction text, bad `trust`, bad `capture_surface`, or
  `untrusted_observed_content` fields through public status output.
- Prevents active-marker `result_file` or `checkpoint_file` values from making
  status read marker-controlled external JSON summaries.
- Preserves sanitized `operator_focus` notes in status output without widening
  the public JSON contract to arbitrary active-marker keys.
- Aligns package, runtime, plugin, and MCP server version identity to `0.2.66`.

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

Published at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.66.
Remote tag `v0.2.66` points to
`aef5a89d94707c11b7a2e63a7fdddce46649e4b7`. GitHub Windows Harness run
https://github.com/YSCJRH/WinChronicle/actions/runs/27865327396 passed on the
same head SHA. Post-publication reconciliation updates
`docs/release-evidence.md`, `docs/release-checklist.md`, and
`docs/manual-smoke-evidence-ledger.md` so `v0.2.66` is the current package/tag
release and latest full manual UIA smoke source.
