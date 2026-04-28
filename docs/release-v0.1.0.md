# v0.1.0 Final Release Readiness Record

This record prepares the `v0.1.0` final release from the published
`v0.1.0-rc.1` baseline. It records commands, results, commit identifiers, CI
URLs, environment notes, and local artifact paths only. It does not commit
observed-content artifacts.

## Release Decision

`v0.1.0` final is ready for explicit publication approval if the release-record
PR and its post-merge `main` Windows Harness pass without requiring product
code, schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
capture-surface changes.

If any such change is required before publication, do not publish final. Prepare
`v0.1.0-rc.2` instead.

Publication status: pending explicit approval. Do not tag or publish final from
this record alone.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.0` |
| Stage | Stage V3 - Final Release Decision |
| Evidence date | 2026-04-28, Asia/Shanghai |
| Current candidate `main` SHA before this record | `355aaf5b88c09cd87db60b1f3215136dff5e8c07` |
| Final tag target | Pending explicit approval; use the latest verified `main` SHA after the release-record PR and post-merge Windows Harness pass |
| Publication status | Not published |
| Previous release-candidate baseline | `v0.1.0-rc.1` |
| Previous release-candidate URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.0-rc.1 |
| `v0.1.0-rc.1` tag target | `ad2c33feffb151ffe6c52d651c05ace5e007db97` |
| Stage V0 PR | https://github.com/YSCJRH/WinChronicle/pull/25 |
| Stage V0 post-merge `main` Windows Harness | Passed, run `25033085206`, https://github.com/YSCJRH/WinChronicle/actions/runs/25033085206 |
| Stage V1 PR | https://github.com/YSCJRH/WinChronicle/pull/26 |
| Stage V1 post-merge `main` Windows Harness | Passed, run `25033323560`, https://github.com/YSCJRH/WinChronicle/actions/runs/25033323560 |
| Stage V2 PR | https://github.com/YSCJRH/WinChronicle/pull/27 |
| Stage V2 post-merge `main` Windows Harness | Passed, run `25033575875`, https://github.com/YSCJRH/WinChronicle/actions/runs/25033575875 |

Environment:

- Windows interactive desktop, PowerShell.
- Python: `3.11.2`.
- .NET SDK: `8.0.202`.
- Manual smoke artifact root:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-final-v2-smoke-20260428-0410`.
- Manual watcher temporary state:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-final-v2-watch-state-20260428-0410`.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `72 passed in 16.83s` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The Stage V1 PR Windows Harness and post-merge `main` Windows Harness passed.
The Stage V2 evidence PR and post-merge `main` Windows Harness also passed.

## Manual UIA Smoke Gates

Manual smoke used local temporary artifacts only. Do not commit the artifact
JSON files; they may contain observed screen content.

| Gate | Result | Evidence |
| --- | --- | --- |
| Notepad targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-notepad.ps1 -ArtifactDir <artifact-root>\notepad -TimeoutSeconds 30`; artifact `<artifact-root>\notepad\notepad-capture.json` |
| Edge targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-edge.ps1 -ArtifactDir <artifact-root>\edge -TimeoutSeconds 45`; artifact `<artifact-root>\edge\edge-capture.json` |
| VS Code availability | Available | `code.cmd` found at `C:\Users\34793\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd` |
| VS Code metadata smoke | Pass with diagnostic warning | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -ArtifactDir <artifact-root>\vscode-metadata -TimeoutSeconds 45`; metadata passed, editor marker was not exposed through UIA; artifact `<artifact-root>\vscode-metadata\vscode-capture.json` |
| VS Code strict Monaco marker | Diagnostic failure, non-blocking | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -Strict -ArtifactDir <artifact-root>\vscode-strict -TimeoutSeconds 45`; known Monaco/UIA limitation; artifact `<artifact-root>\vscode-strict\vscode-capture.json` |

The VS Code strict diagnostic failure is not a v0.1 release blocker. The
metadata smoke is the conditional hard gate when `code.cmd` is available, and
it passed.

## Watcher Preview Smoke

Watcher preview remains explicit, time-bounded, and operator-started. It is not
a daemon, service, polling capture loop, or default background capture.

| Check | Result | Evidence |
| --- | --- | --- |
| Deterministic watcher fixture and fake-helper preview | Pass | Covered by `python harness/scripts/run_harness.py` |
| Real watcher/helper short preview | Heartbeat-only liveness diagnostic | `python -m winchronicle watch --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper dotnet --helper-arg resources/win-uia-helper/bin/Debug/net8.0-windows/win-uia-helper.dll --duration 5 --heartbeat-ms 500 --capture-on-start` returned `captures_written: 0`, `denylisted_skipped: 0`, `duplicates_skipped: 0`, `heartbeats: 10` using temporary `WINCHRONICLE_HOME` |

A direct frontmost capture smoke in the same agent-hosted desktop returned
`SKIPPED: helper returned no capture`. The live watcher result is therefore
heartbeat-only diagnostic evidence; deterministic watcher gates and fake-helper
preview passed.

## Release Notes

- Promotes the `v0.1.0-rc.1` product contract to final readiness.
- Keeps WinChronicle local-first, UIA-first, harness-first, and read-only MCP
  first.
- Keeps CLI and MCP surfaces stable from `v0.1.0-rc.1`.
- Keeps screenshots, OCR, audio, keyboard capture, clipboard capture, network
  upload, LLM calls, desktop control, product targeted capture, daemon/service
  install, polling capture loops, and default background capture out of v0.1.
- Ships deterministic fixture capture/search, privacy gates, SQLite FTS,
  helper/watcher preview harnesses, read-only MCP, and deterministic memory
  generation/search as the v0.1 baseline.

## Known Limitations

- VS Code Monaco editor buffer text may not be exposed through standard UIA
  `TextPattern` or `ValuePattern`, even when accessibility support is enabled.
- VS Code strict editor marker capture remains diagnostic and non-blocking for
  v0.1.
- Watcher remains a preview path and must be invoked explicitly with a finite
  duration.
- Live watcher/frontmost capture can be heartbeat-only in agent-hosted desktop
  environments where `GetForegroundWindow` does not resolve a capturable target.
- Product CLI still does not expose targeted `--hwnd`, `--pid`, or
  `--window-title` capture.

## Privacy And Scope Confirmation

This final release does not expand the capture surface beyond `v0.1.0-rc.1`.

- Local-first: captured content remains local; no cloud or network upload is
  implemented.
- UIA-first and harness-first boundaries remain unchanged.
- Screenshots are absent or off by default; screenshot capture is not
  implemented.
- OCR is absent or off by default; OCR is not implemented.
- Audio recording is not implemented.
- Keyboard capture and keylogging are not implemented.
- Clipboard capture is not implemented in v0.1.
- LLM summarization/classification and LLM calls are not implemented in the
  product path.
- MCP remains read-only with `current_context`, `search_captures`,
  `search_memory`, `read_recent_capture`, `recent_activity`, and
  `privacy_status`.
- MCP exposes no write tools, arbitrary file read tools, desktop control tools,
  screenshot/OCR tools, audio tools, keyboard tools, clipboard tools, or
  network upload tools.
- No daemon/service install, polling capture loop, or default background
  capture is implemented.
- Desktop control is not implemented.
- Observed content remains untrusted and must remain marked as
  `untrusted_observed_content` in captures, memory, CLI search, and MCP
  responses.
- Password fields and obvious secrets must not be stored, including API keys,
  private keys, JWTs, GitHub tokens, Slack tokens, and token canaries.

## Rollback Notes

- If final publication is not approved, keep `v0.1.0-rc.1` as the latest
  published release-candidate baseline.
- Do not retag `v0.1.0-rc.1`; publish `v0.1.0-rc.2` if a replacement candidate
  is needed.
- If a regression is found before final publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, stop the final path and prepare `v0.1.0-rc.2`.
- If a regression is limited to final release documentation, fix it on a small
  docs-only PR and rerun Windows Harness before reconsidering final approval.

## Release Decision Summary

- Release path: direct `v0.1.0` final is allowed after explicit approval if the
  release-record PR and post-merge `main` Windows Harness pass.
- Fallback path: `v0.1.0-rc.2` if any product or contract change is required.
- Deterministic gates: passed locally and in GitHub Actions.
- Manual hard gates: Notepad passed; Edge passed.
- Conditional hard gate: VS Code metadata passed because `code.cmd` is
  available.
- Diagnostic non-blocking gate: VS Code strict Monaco marker failed as a known
  limitation, with local artifact path recorded.
- Watcher preview: deterministic and fake-helper preview passed; live preview
  produced heartbeat-only liveness evidence.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: pending.
