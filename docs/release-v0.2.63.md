# v0.2.63 Release Record

This record tracks the `v0.2.63` Workday safe-failure release path. It records
commands, results, environment notes, and local artifact paths only. It does not
commit observed screen-content artifacts.

## Release Decision

`v0.2.63` is warranted by a Workday CLI safety fix: default helper/watcher build
output resolution now fails through the existing safe Workday error path instead
of raising an uncaught traceback before runner startup.

Publication status: pre-publication package preflight.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.2.63` |
| Stage | `v0.2.63` Workday safe-failure preflight |
| Evidence date | 2026-06-20, Asia/Shanghai |
| Publication status | Not published; pending post-publication reconciliation |
| Expected release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.63 |
| Previous package/tag release | `v0.2.62` |
| Previous package/tag release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.62 |
| Manual smoke artifact root | `C:\Users\34793\AppData\Local\Temp\winchronicle-v0263-smoke-43cc5695faf04420a57f2db6606ed7a3` |

Environment:

- Windows interactive desktop, PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest tests/test_workday.py -k "default_build_output_is_missing or default_helper_build_output_is_missing" -q` | Pass | `3 passed, 50 deselected` |
| `python -m pytest tests/test_workday.py -q` | Pass | `53 passed` |
| `python -m pytest tests/test_cli.py tests/test_codex_workday_plugin.py tests/test_privacy_check.py tests/test_mcp_tools.py -q` | Pass | `59 passed` |
| `python -m pytest -q` | Pass | `422 passed` |
| `git diff --check` | Pass | no whitespace errors |
| `python harness/scripts/run_harness.py` | Pass | full harness passed: 422 pytest tests, release validators, helper/watcher builds with 0 warnings and 0 errors, quick demo, watcher smokes, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke |

## Manual UIA Smoke Gates

Manual smoke used local temporary artifacts only. Do not commit the artifact JSON
files; they may contain observed screen content.

| Gate | Result | Evidence |
| --- | --- | --- |
| Notepad targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-notepad.ps1 -ArtifactDir <artifact-root>\notepad -TimeoutSeconds 30`; artifact `<artifact-root>\notepad\notepad-capture.json` |
| Edge targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-edge.ps1 -ArtifactDir <artifact-root>\edge -TimeoutSeconds 45`; artifact `<artifact-root>\edge\edge-capture.json` |
| VS Code metadata smoke | Pass with diagnostic warning | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -ArtifactDir <artifact-root>\vscode-metadata -TimeoutSeconds 45`; metadata passed, editor marker was not exposed through UIA |
| VS Code strict Monaco marker | Diagnostic failure, non-blocking | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -Strict -ArtifactDir <artifact-root>\vscode-strict -TimeoutSeconds 45`; known Monaco/UIA limitation |
| Fake-helper monitor watcher | Pass | `python -m winchronicle monitor --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper python --helper-arg harness/scripts/fake_uia_helper.py --duration 1 --heartbeat-ms 250 --capture-on-start --session-id release-fake-helper-v0263` returned `captures_written: 1`, `duplicates_skipped: 0`, `denylisted_skipped: 0`, `heartbeats: 4`, and local session/report paths under the temporary `WINCHRONICLE_HOME` |

## Release Notes

- Handles missing default watcher build output with a safe JSON Workday error
  instead of an uncaught traceback.
- Handles missing default helper build output with the same safe Workday error
  path after default watcher resolution succeeds.
- Makes natural-language `workday intent ... --execute` start failures use the
  existing concise Chinese `工作记录未开始` text output instead of raw JSON or a
  traceback.
- Aligns package, runtime, plugin, and MCP server version identity to `0.2.63`.

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

After publication, update `docs/release-evidence.md`,
`docs/release-checklist.md`, and `docs/manual-smoke-evidence-ledger.md` with the
published `v0.2.63` release URL, tag target SHA, Windows Harness run URL, and
publication timestamp. Remove the `Next Package Release Preflight` section once
the project version matches the published current release evidence.
