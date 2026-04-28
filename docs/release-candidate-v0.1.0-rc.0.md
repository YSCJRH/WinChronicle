# v0.1.0-rc.0 Release Candidate Record

This record captures the Stage RC4 evidence for the `v0.1.0-rc.0`
candidate. It records commands, results, commit identifiers, CI URLs,
environment notes, and local artifact paths only. It does not commit observed
content artifacts.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release candidate | `v0.1.0-rc.0` |
| Stage | Stage RC4 - RC Candidate Preparation |
| Evidence date | 2026-04-28, Asia/Shanghai |
| Evidence branch | `codex/stage-rc4-rc-candidate` |
| Current verified `main` SHA | `069e8cff9434c83b00a7a857aaf9eee441cf16ff` |
| Final tag target | `069e8cff9434c83b00a7a857aaf9eee441cf16ff` |
| Publication status | Published prerelease |
| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.0-rc.0 |
| Previous prerelease baseline | `v0.1.0-beta.1` |
| Previous prerelease URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.0-beta.1 |
| Release evidence PR | https://github.com/YSCJRH/WinChronicle/pull/16 |
| PR Windows Harness | Passed, run `25021868203`, https://github.com/YSCJRH/WinChronicle/actions/runs/25021868203 |
| Post-merge `main` Windows Harness | Passed, run `25022034701`, https://github.com/YSCJRH/WinChronicle/actions/runs/25022034701 |

Environment:

- Windows interactive desktop, PowerShell.
- Python: `3.11.2`.
- .NET SDK: `8.0.202`.
- Manual smoke artifact root:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-rc0-smoke-76e7371477be486f848a93504d2b1284`.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `60 passed in 24.18s` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The published tag target is green on `main` at
`069e8cff9434c83b00a7a857aaf9eee441cf16ff`. The PR Windows Harness and
post-merge `main` Windows Harness both passed before publication.

## Manual UIA Smoke Gates

Manual smoke used local temporary artifacts only. Do not commit the artifact
JSON files; they may contain observed screen content.

| Gate | Result | Evidence |
| --- | --- | --- |
| Notepad targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-notepad.ps1 -ArtifactDir <artifact-root>\notepad`; artifact `<artifact-root>\notepad\notepad-capture.json` |
| Edge targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-edge.ps1 -ArtifactDir <artifact-root>\edge`; artifact `<artifact-root>\edge\edge-capture.json` |
| VS Code availability | Available | `code.cmd` found at `C:\Users\34793\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd` |
| VS Code metadata smoke | Pass with diagnostic warning | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -ArtifactDir <artifact-root>\vscode-metadata`; metadata passed, editor marker was not exposed through UIA; artifact `<artifact-root>\vscode-metadata\vscode-capture.json` |
| VS Code strict Monaco marker | Diagnostic failure, non-blocking | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -Strict -ArtifactDir <artifact-root>\vscode-strict`; known Monaco/UIA limitation; artifact `<artifact-root>\vscode-strict\vscode-capture.json` |

The VS Code strict diagnostic failure is not a v0.1 release blocker. The
metadata smoke is the conditional hard gate when `code.cmd` is available, and
it passed.

## Watcher Preview Smoke

Watcher preview remains explicit, time-bounded, and operator-started. It is not
a daemon, service, polling capture loop, or default background capture.

| Check | Result | Evidence |
| --- | --- | --- |
| Deterministic watcher fixture and fake-helper preview | Pass | Covered by `python harness/scripts/run_harness.py` |
| Real watcher/helper short preview at depth 80 | Timed out, recorded as diagnostic | `python -m winchronicle watch --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper dotnet --helper-arg resources/win-uia-helper/bin/Debug/net8.0-windows/win-uia-helper.dll --duration 5 --heartbeat-ms 500 --capture-on-start` returned `ERROR: watcher timed out` |
| Real watcher/helper short preview at depth 2 | Pass | Same watcher/helper with `--depth 2 --duration 3 --heartbeat-ms 500 --capture-on-start` returned `captures_written: 4`, `heartbeats: 3`, `duplicates_skipped: 0`, `denylisted_skipped: 0` using temporary `WINCHRONICLE_HOME` |

The depth 80 timeout is treated as preview diagnostic evidence for operator
visibility. The deterministic watcher gates and the bounded depth 2 preview
passed.

## Known Limitations

- VS Code Monaco editor buffer text may not be exposed through standard UIA
  `TextPattern` or `ValuePattern`, even when accessibility support is enabled.
- VS Code strict editor marker capture remains diagnostic and non-blocking for
  v0.1.
- Watcher remains a preview path and must be invoked explicitly with a finite
  duration.
- Product CLI still does not expose targeted `--hwnd`, `--pid`, or
  `--window-title` capture.

## Privacy And Scope Confirmation

This release candidate does not expand the capture surface.

- Local-first: captured content remains local; no cloud or network upload is
  implemented.
- UIA-first and harness-first boundaries remain unchanged.
- Screenshots are absent or off by default; screenshot capture is not
  implemented in this RC.
- OCR is absent or off by default; OCR is not implemented in this RC.
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
  `untrusted_observed_content` in captures, memory, and MCP responses.
- Password fields and obvious secrets must not be stored, including API keys,
  private keys, JWTs, GitHub tokens, Slack tokens, and token canaries.

## Rollback Notes

- If `v0.1.0-rc.0` is withdrawn, keep `v0.1.0-beta.1` as the last known
  published beta baseline.
- Mark the GitHub prerelease as withdrawn, or delete the prerelease tag only if
  it is safe and no downstream consumer depends on it.
- If a regression traces to RC-stage work, revert the relevant RC PR on a new
  branch and rerun the deterministic checklist before publishing any
  replacement prerelease.

## Release Decision Summary

- Deterministic gates: passed locally.
- Published tag target: `069e8cff9434c83b00a7a857aaf9eee441cf16ff`.
- Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.0-rc.0
- PR Windows Harness: passed on
  `ac7ad33ebaf8648bc8dd2361c95d18ba4871a107`, run `25021868203`.
- Post-merge `main` Windows Harness: passed on
  `069e8cff9434c83b00a7a857aaf9eee441cf16ff`, run `25022034701`.
- Manual hard gates: Notepad passed; Edge passed.
- Conditional hard gate: VS Code metadata passed because `code.cmd` is
  available.
- Diagnostic non-blocking gate: VS Code strict Monaco marker failed as a known
  limitation, with local artifact path recorded.
- Watcher preview: deterministic and bounded depth 2 preview passed; depth 80
  short preview timed out and is recorded as diagnostic evidence.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: granted after RC4 evidence review; `v0.1.0-rc.0` was
  published as a prerelease.
