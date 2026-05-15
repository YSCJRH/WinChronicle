# v0.2.0 Release Record

This record tracks the `v0.2.0` product baseline. It records commands, results,
environment notes, and local artifact paths only. It does not commit observed
screen-content artifacts.

## Release Decision

`v0.2.0` promotes WinChronicle from the closed `v0.1` harness-first baseline to
the first product-facing monitor-session baseline. The release is warranted by
an explicit, finite, local UIA/watcher session path that turns watcher events
into local session JSON, deterministic suggestions, and a local HTML report.

Publication status: pending final GitHub release publication.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.2.0` |
| Stage | `v0.2.0` monitor-session baseline |
| Evidence date | 2026-05-16, Asia/Shanghai |
| Candidate branch | `codex/v0.2-monitor-session` |
| Previous stable release | `v0.1.19` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.19 |

Environment:

- Windows interactive desktop, PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual smoke artifact root:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-v020-smoke-edc290bd73b84066a4797e654ddc3d2b`.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest tests/test_monitor_session.py tests/test_mcp_tools.py tests/test_compatibility_contracts.py -q` | Pass | `24 passed` |
| `python harness/scripts/run_mcp_smoke.py` | Pass | MCP stdio smoke passed |
| `python -m pytest -q` | Pass | `236 passed` |
| `git diff --check` | Pass | no whitespace errors |
| `python harness/scripts/run_harness.py` | Pass | full harness passed: 236 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke |
| `python -c "import winchronicle, winchronicle.mcp.server as server; print(winchronicle.__version__); print(server.__version__)"` | Pass | printed `0.2.0` twice |

## Manual UIA Smoke Gates

Manual smoke used local temporary artifacts only. Do not commit the artifact
JSON files; they may contain observed screen content.

| Gate | Result | Evidence |
| --- | --- | --- |
| Notepad targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-notepad.ps1 -ArtifactDir <artifact-root>\notepad -TimeoutSeconds 30`; artifact `<artifact-root>\notepad\notepad-capture.json` |
| Edge targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-edge.ps1 -ArtifactDir <artifact-root>\edge -TimeoutSeconds 45`; artifact `<artifact-root>\edge\edge-capture.json` |
| VS Code metadata smoke | Pass with diagnostic warning | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -ArtifactDir <artifact-root>\vscode-metadata -TimeoutSeconds 45`; metadata passed, editor marker was not exposed through UIA |
| VS Code strict Monaco marker | Diagnostic failure, non-blocking | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -Strict -ArtifactDir <artifact-root>\vscode-strict -TimeoutSeconds 45`; known Monaco/UIA limitation |
| Fake-helper monitor watcher | Pass | `python -m winchronicle monitor --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper python --helper-arg harness/scripts/fake_uia_helper.py --duration 1 --heartbeat-ms 250 --capture-on-start --session-id release-fake-helper` returned `captures_written: 1`, `duplicates_skipped: 0`, `heartbeats: 3`, and local session/report paths under the temporary `WINCHRONICLE_HOME` |

## Release Notes

- Adds `monitor --events` and `monitor --watcher` for explicit, finite,
  operator-started monitor sessions.
- Adds `summarize-session` for reading saved local session summaries by session
  id from the WinChronicle state directory.
- Adds the session report schema, local `sessions` and `reports` state
  directories, deterministic suggestions, and local HTML reports.
- Adds `--exclude-app` for per-session exact app-name exclusions.
- Keeps raw watcher JSONL out of the product monitor-session storage path.
- Extends read-only MCP `recent_activity` with local monitor session summaries
  and `privacy_status` with `session_count`; the MCP tool list remains
  unchanged.
- Aligns package, runtime, and MCP server version identity to `0.2.0`.

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
- `summarize-session` reads saved session ids under the local state directory;
  it is not an arbitrary JSON file reader.

## Known Limitations

- Monitor sessions are explicit and finite. v0.2 does not install or start a
  daemon, service, startup task, or default background watcher.
- Suggestions are deterministic local heuristics, not LLM summaries or
  classifiers.
- Live watcher/frontmost capture can be heartbeat-only in agent-hosted desktop
  environments where `GetForegroundWindow` does not resolve a capturable target.
- VS Code Monaco editor buffer text may not be exposed through standard UIA
  `TextPattern` or `ValuePattern`, even when accessibility support is enabled.

## Next Product Direction

The next human-approved product direction is a small Windows operator loop:
make explicit monitor-session startup, review, exclusion tuning, and report
review comfortable for a first-time Windows developer without adding screenshots,
OCR, keylogging, clipboard capture, cloud upload, desktop control, or MCP write
tools.
