# v0.1.16 Final Release Record

This record prepares the `v0.1.16` final release from the published
`v0.1.16-rc.0` prerelease baseline. It records commands, results, commit
identifiers, CI URLs, environment notes, and local artifact paths only. It does
not commit observed-content artifacts.

## Release Decision

`v0.1.16` final is published. The release-record PR, post-merge `main` Windows
Harness, GitHub release publication, release metadata verification, and remote
tag verification passed.

The direct final path is allowed because `v0.1.16-rc.0` is published, AE0-AE2
recorded final-readiness evidence, deterministic gates passed, fresh manual
final UIA smoke passed for the required hard gates, and no product behavior,
schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
capture-surface change is required after the prerelease.

If any product behavior, schema, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture-surface regression is found before
publication, do not publish final. Prepare `v0.1.16-rc.1` instead. If such a
regression is found after publication, publish a follow-up release candidate
instead of retagging `v0.1.16`.

Publication status: published final release.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.16` |
| Stage | AE3 final release record and publication readiness |
| Evidence date | 2026-05-09, Asia/Shanghai |
| Current candidate `main` SHA before this record | `1ea902a8630b9d0b18397af69cfcd84a9ce4d24a` |
| Publication status | Published final release |
| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16 |
| Published at | 2026-05-09T09:31:17Z |
| Final tag target | `255f2a01cddde330d756a87359c4d3a8be4b11a2` |
| Previous prerelease baseline | `v0.1.16-rc.0` |
| Previous prerelease URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16-rc.0 |
| `v0.1.16-rc.0` tag target | `70caf364f68d8c159eb74bbbc23e7469db22a244` |
| Previous stable release | `v0.1.15` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.15 |
| `v0.1.15` tag target | `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2` |
| AE0 PR | https://github.com/YSCJRH/WinChronicle/pull/144 |
| AE0 PR Windows Harness | Passed, run `25596958129`, https://github.com/YSCJRH/WinChronicle/actions/runs/25596958129 |
| AE0 post-merge `main` Windows Harness | Passed, run `25597001825`, https://github.com/YSCJRH/WinChronicle/actions/runs/25597001825 |
| AE1 PR | https://github.com/YSCJRH/WinChronicle/pull/145 |
| AE1 PR Windows Harness | Passed, run `25597196866`, https://github.com/YSCJRH/WinChronicle/actions/runs/25597196866 |
| AE1 post-merge `main` Windows Harness | Passed, run `25597248992`, https://github.com/YSCJRH/WinChronicle/actions/runs/25597248992 |
| AE2 PR | https://github.com/YSCJRH/WinChronicle/pull/146 |
| AE2 PR Windows Harness | Passed, run `25597418104`, https://github.com/YSCJRH/WinChronicle/actions/runs/25597418104 |
| AE2 post-merge `main` Windows Harness | Passed, run `25597463319`, https://github.com/YSCJRH/WinChronicle/actions/runs/25597463319 |
| AE3 PR | https://github.com/YSCJRH/WinChronicle/pull/147 |
| AE3 PR Windows Harness | Passed, run `25597623991`, https://github.com/YSCJRH/WinChronicle/actions/runs/25597623991 |
| AE3 post-merge `main` Windows Harness | Passed, run `25597678444`, https://github.com/YSCJRH/WinChronicle/actions/runs/25597678444 |
| AE4 publication reconciliation PR | https://github.com/YSCJRH/WinChronicle/pull/148 |
| AE4 publication reconciliation Windows Harness | Passed, run `25598038285`, https://github.com/YSCJRH/WinChronicle/actions/runs/25598038285 |
| AE4 post-publication `main` Windows Harness | Passed, run `25598080136`, https://github.com/YSCJRH/WinChronicle/actions/runs/25598080136 |
| AD5 release-candidate PR | https://github.com/YSCJRH/WinChronicle/pull/140 |
| AD5 release-candidate PR Windows Harness | Passed, run `25596082939`, https://github.com/YSCJRH/WinChronicle/actions/runs/25596082939 |
| AD5 final pre-publication `main` Windows Harness | Passed, run `25596273094`, https://github.com/YSCJRH/WinChronicle/actions/runs/25596273094 |
| AD5 prerelease publication reconciliation PR | https://github.com/YSCJRH/WinChronicle/pull/142 |
| AD5 prerelease publication reconciliation Windows Harness | Passed, run `25596387380`, https://github.com/YSCJRH/WinChronicle/actions/runs/25596387380 |
| AD5 post-publication `main` Windows Harness | Passed, run `25596453899`, https://github.com/YSCJRH/WinChronicle/actions/runs/25596453899 |

Environment:

- Windows interactive desktop, PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual smoke artifact root:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-ae2-final-smoke-a3da7c0177fc42059a484cf07435777a`.
- Manual watcher temporary state:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-ae2-final-smoke-a3da7c0177fc42059a484cf07435777a\watch-state`.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `151 passed` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The AE1 local deterministic gates, AE1 PR Windows Harness, AE1 post-merge
`main` Windows Harness, AE2 PR Windows Harness, AE2 post-merge `main` Windows
Harness, AE3 PR Windows Harness, AE3 post-merge `main` Windows Harness, and
GitHub release publication passed.

## Manual UIA Smoke Gates

Manual smoke used local temporary artifacts only. Do not commit the artifact
JSON files; they may contain observed screen content.

| Gate | Result | Evidence |
| --- | --- | --- |
| Notepad targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-notepad.ps1 -ArtifactDir <artifact-root>\notepad -TimeoutSeconds 30`; artifact `<artifact-root>\notepad\notepad-capture.json` |
| Edge targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-edge.ps1 -ArtifactDir <artifact-root>\edge -TimeoutSeconds 45`; artifact `<artifact-root>\edge\edge-capture.json` |
| VS Code availability | Available | `code.cmd` available in the Windows interactive desktop environment |
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
| Real watcher/helper short preview | Pass | `python -m winchronicle watch --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper dotnet --helper-arg resources/win-uia-helper/bin/Debug/net8.0-windows/win-uia-helper.dll --duration 5 --depth 2 --heartbeat-ms 500 --capture-on-start` returned `captures_written: 3`, `denylisted_skipped: 0`, `duplicates_skipped: 1`, `heartbeats: 6` using temporary `WINCHRONICLE_HOME` |

## Release Notes

- Promotes the published `v0.1.16-rc.0` prerelease contract to `v0.1.16`
  final readiness.
- Aligns package, runtime, and MCP server version identity to `0.1.16`.
- Keeps WinChronicle local-first, UIA-first, harness-first, and read-only MCP
  first.
- Keeps CLI and MCP surfaces stable from `v0.1.16-rc.0`.
- Keeps screenshots, OCR, audio, keyboard capture, clipboard capture, network
  upload, LLM calls, desktop control, product targeted capture, daemon/service
  install, polling capture loops, and default background capture out of v0.1.
- Carries the AD2-AD4 privacy/runtime guardrail fixes through prerelease review
  and final readiness without adding capture surfaces or MCP tools.
- Records fresh final manual UIA smoke for the `v0.1.16` final path.

## Known Limitations

- VS Code Monaco editor buffer text may not be exposed through standard UIA
  `TextPattern` or `ValuePattern`, even when accessibility support is enabled.
- VS Code strict editor marker capture remains diagnostic and non-blocking for
  v0.1.
- Watcher remains a preview path and must be invoked explicitly with a finite
  duration.
- Live watcher/frontmost capture can be heartbeat-only in agent-hosted desktop
  environments where `GetForegroundWindow` does not resolve a capturable
  target.
- Product CLI still does not expose targeted `--hwnd`, `--pid`,
  `--window-title`, `--window-title-regex`, or `--process-name` capture flags.

## Compatibility Evidence

- `pyproject.toml`, `winchronicle.__version__`, and MCP `serverInfo.version`
  must report `0.1.16`.
- The exact read-only MCP tool list remains unchanged:
  `current_context`, `search_captures`, `search_memory`,
  `read_recent_capture`, `recent_activity`, and `privacy_status`.
- MCP exposes no write tools, arbitrary file read tools, desktop control tools,
  screenshot/OCR tools, audio tools, keyboard tools, clipboard tools, network
  tools, or product targeted capture flags.
- Product CLI exposes no targeted `--hwnd`, `--pid`, `--window-title`,
  `--window-title-regex`, or `--process-name` capture flags.
- Phase 6 remains specification-only; this final release introduces no
  screenshot capture code, no OCR engine integration, no screenshot cache, no
  cache cleanup path, and no OCR-derived storage path.

## Privacy And Scope Confirmation

This final release does not expand the capture surface beyond `v0.1.16-rc.0`.

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

- Keep `v0.1.16` as the latest stable release after publication verification.
- Keep `v0.1.16-rc.0` as historical prerelease evidence.
- Keep `v0.1.15` as the previous stable release.
- Do not retag or modify `v0.1.16-rc.0`; publish `v0.1.16-rc.1` if a
  replacement candidate is needed.
- If a regression is found before final publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, stop the final path and prepare `v0.1.16-rc.1`.
- If a regression is found after final publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, publish a follow-up release candidate instead of
  retagging `v0.1.16`.
- If a regression is limited to final release documentation, tests, GitHub
  metadata, CI/runtime metadata, or version metadata, fix it on a small PR and
  rerun Windows Harness before publishing.

## Release Decision Summary

- Release path: direct `v0.1.16` final published after explicit approval, the
  release-record PR, and post-merge `main` Windows Harness passed.
- Fallback path: `v0.1.16-rc.1` if any product or contract change is required.
- Deterministic gates: passed locally and in GitHub Actions.
- Manual hard gates: Notepad passed; Edge passed.
- Conditional hard gate: VS Code metadata passed because `code.cmd` is
  available.
- Diagnostic non-blocking gate: VS Code strict Monaco marker failed as a known
  limitation, with local artifact path recorded.
- Watcher preview: deterministic/fake-helper preview passed; live preview
  passed with `captures_written: 3`, `denylisted_skipped: 0`,
  `duplicates_skipped: 1`, and `heartbeats: 6`.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: standing user goal authorizes publishing after review
  and validation.
- GitHub release publication: passed.
- Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16.
- Final tag target: `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
