# v0.1.16-rc.0 Release Candidate Record

This record prepares the `v0.1.16-rc.0` release-candidate readiness path from
the published `v0.1.15` baseline. It records commands, results, commit
identifiers, CI URLs, environment notes, and local artifact paths only. It does
not commit observed-content artifacts.

## Release Decision

`v0.1.16-rc.0` is a release-candidate readiness candidate. Local AD5
validation, fresh manual UIA smoke, PR Windows Harness, and post-merge `main`
Windows Harness passed. GitHub prerelease publication is pending.

The release-candidate path is required before direct `v0.1.16` final because
AD2-AD4 included compatible runtime drift fixes, not only documentation and
version metadata. The fixes tighten privacy and compatibility boundaries: AD2
prevents title-denylist diagnostic content echo, AD3 fixes filtered MCP/search
parity without changing MCP schema or tool names, and AD4 broadens
obvious-secret redaction plus rejects disabled helper/watcher target,
control, and privacy-surface pass-through flags. These changes do not add
capture surfaces, MCP tools, desktop control, screenshot/OCR/audio/keyboard/
clipboard/network behavior, schema changes, or CLI/MCP JSON shape changes.
They do change product/runtime privacy behavior, so this record uses a
release-candidate path instead of publishing direct `v0.1.16` final.

If a regression is found before prerelease publication, fix it on a new
candidate PR and rerun local and Windows Harness gates. If a regression is
found after prerelease publication, publish a follow-up release candidate
instead of retagging `v0.1.16-rc.0`.

Publication status: release-candidate readiness; not yet published.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release candidate | `v0.1.16-rc.0` |
| Stage | AD5 release-candidate readiness |
| Evidence date | 2026-05-09, Asia/Shanghai |
| Base `main` SHA before AD5 readiness | `2c7d0b0b24d9a159c084f262cb24ec7ee9873a39` |
| Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/140 |
| Candidate PR Windows Harness | Passed, run `25596082939`, https://github.com/YSCJRH/WinChronicle/actions/runs/25596082939 |
| Candidate post-merge `main` Windows Harness | Passed, run `25596122521`, https://github.com/YSCJRH/WinChronicle/actions/runs/25596122521 |
| Candidate post-merge `main` SHA | `bca4b6485f194a46bca7fa6e1e3866b5105479da` |
| Publication status | Release-candidate readiness; not yet published |
| Release URL | Pending |
| Final tag target | Pending |
| Previous stable release | `v0.1.15` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.15 |
| `v0.1.15` tag target | `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2` |
| AD0 PR | https://github.com/YSCJRH/WinChronicle/pull/135 |
| AD0 PR Windows Harness | Passed, run `25593554670`, https://github.com/YSCJRH/WinChronicle/actions/runs/25593554670 |
| AD0 post-merge `main` Windows Harness | Passed, run `25593607384`, https://github.com/YSCJRH/WinChronicle/actions/runs/25593607384 |
| AD1 PR | https://github.com/YSCJRH/WinChronicle/pull/136 |
| AD1 PR Windows Harness | Passed, run `25593788484`, https://github.com/YSCJRH/WinChronicle/actions/runs/25593788484 |
| AD1 post-merge `main` Windows Harness | Passed, run `25593871698`, https://github.com/YSCJRH/WinChronicle/actions/runs/25593871698 |
| AD2 PR | https://github.com/YSCJRH/WinChronicle/pull/137 |
| AD2 PR Windows Harness | Passed, run `25594230290`, https://github.com/YSCJRH/WinChronicle/actions/runs/25594230290 |
| AD2 post-merge `main` Windows Harness | Passed, run `25594302410`, https://github.com/YSCJRH/WinChronicle/actions/runs/25594302410 |
| AD3 PR | https://github.com/YSCJRH/WinChronicle/pull/138 |
| AD3 PR Windows Harness | Passed, run `25594817396`, https://github.com/YSCJRH/WinChronicle/actions/runs/25594817396 |
| AD3 post-merge `main` Windows Harness | Passed, run `25594896165`, https://github.com/YSCJRH/WinChronicle/actions/runs/25594896165 |
| AD4 PR | https://github.com/YSCJRH/WinChronicle/pull/139 |
| AD4 PR Windows Harness | Passed, run `25595449096`, https://github.com/YSCJRH/WinChronicle/actions/runs/25595449096 |
| AD4 post-merge `main` Windows Harness | Passed, run `25595513141`, https://github.com/YSCJRH/WinChronicle/actions/runs/25595513141 |

Environment:

- Windows PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual UIA smoke was refreshed for this release-candidate path because
  AD2-AD4 changed privacy/runtime behavior, even though the changes narrow
  exposure and do not expand capture surfaces. Artifact root:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-ad5-rc0-smoke-d8337447f78249fc934f40216e996b4a`.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `149 passed` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search/memory, fixture watcher, and preview watcher smoke passed |
| `python -c "import winchronicle; print(winchronicle.__version__)"` | Pass | printed `0.1.16` |
| `git diff --check` | Pass | no whitespace errors |

The AD5 PR Windows Harness and post-merge `main` Windows Harness passed.
GitHub prerelease publication is pending.

## Manual UIA Smoke Gates

Fresh manual smoke used local temporary artifacts only. Do not commit artifact
JSON files because they may contain observed content.

| Gate | Result | Evidence |
| --- | --- | --- |
| Notepad targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-notepad.ps1 -ArtifactDir <artifact-root>\notepad -TimeoutSeconds 30`; artifact `<artifact-root>\notepad\notepad-capture.json` |
| Edge targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-edge.ps1 -ArtifactDir <artifact-root>\edge -TimeoutSeconds 45`; artifact `<artifact-root>\edge\edge-capture.json` |
| VS Code availability | Available | `code.cmd` found at `C:\Users\34793\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd` |
| VS Code metadata smoke | Pass with diagnostic warning | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -ArtifactDir <artifact-root>\vscode-metadata -TimeoutSeconds 45`; metadata passed, editor marker was not exposed through UIA; artifact `<artifact-root>\vscode-metadata\vscode-capture.json` |
| VS Code strict Monaco marker | Diagnostic failure, non-blocking | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -Strict -ArtifactDir <artifact-root>\vscode-strict -TimeoutSeconds 45`; known Monaco/UIA limitation; artifact `<artifact-root>\vscode-strict\vscode-capture.json` |
| Watcher preview live smoke | Pass | `WINCHRONICLE_HOME=<artifact-root>\watcher-state python -m winchronicle watch --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper dotnet --helper-arg resources/win-uia-helper/bin/Debug/net8.0-windows/win-uia-helper.dll --duration 5 --depth 2 --heartbeat-ms 500 --capture-on-start` returned `captures_written: 3`, `heartbeats: 7`, `duplicates_skipped: 1`, `denylisted_skipped: 0` |

## Release Notes

- Aligns package, runtime, and MCP server version identity to `0.1.16`.
- Adds post-v0.1.15 public metadata, helper/watcher diagnostics, MCP/memory
  contract, and compatibility guardrail evidence.
- Fixes narrow privacy and compatibility drift: no title-denylist diagnostic
  observed-content echo, broader obvious-secret redaction canaries, SQLite
  filter-before-limit parity for MCP/CLI search, and rejection of disabled
  helper/watcher target/control/privacy pass-through flags.
- Keeps the v0.1 product boundary intact: no new capture surfaces, no new MCP
  tools, no CLI/MCP JSON shape changes, no helper/watcher capture expansion,
  and no Phase 6 implementation.
- Records fresh AD5 manual UIA smoke for the release-candidate path without
  committing observed-content artifacts.

## Known Limitations

- VS Code Monaco editor buffer text may not be exposed through standard UIA
  `TextPattern` or `ValuePattern`.
- VS Code strict editor marker capture remains diagnostic and non-blocking.
- Watcher remains a preview path and must be invoked explicitly with a finite
  duration.
- Live watcher/frontmost capture can be heartbeat-only in agent-hosted desktop
  environments where `GetForegroundWindow` does not resolve a capturable
  target.
- Phase 6 screenshot/OCR enrichment remains specification-only.

## Compatibility Evidence

- `pyproject.toml`, `winchronicle.__version__`, and MCP `serverInfo.version`
  must report `0.1.16`.
- The exact read-only MCP tool list remains unchanged:
  `current_context`, `search_captures`, `search_memory`,
  `read_recent_capture`, `recent_activity`, and `privacy_status`.
- MCP exposes no write tools, arbitrary file read tools, desktop control tools,
  screenshot/OCR tools, audio tools, keyboard tools, clipboard tools, network
  tools, or product targeted capture flags.
- Phase 6 remains specification-only; this release candidate introduces no
  screenshot capture code, no OCR engine integration, no screenshot cache, no
  cache cleanup path, and no OCR-derived storage path.

## Privacy And Scope Confirmation

This release candidate tightens privacy and compatibility checks without
expanding the capture surface from `v0.1.15`.

- Local-first: captured content remains local; no cloud or network upload is
  implemented.
- UIA-first and harness-first boundaries remain unchanged.
- Screenshots are absent or off by default; screenshot capture is not
  implemented.
- OCR is absent or off by default; OCR is not implemented.
- Audio recording is not implemented.
- Keyboard capture and keylogging are not implemented.
- Clipboard capture is not implemented.
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
- Helper and watcher pass-through arguments must reject disabled target,
  control, and privacy-surface flags.

## Rollback Notes

- Keep `v0.1.15` as the previous stable release.
- Do not retag or modify `v0.1.15`.
- If a regression is found before prerelease publication, fix it on a new
  release-candidate PR and rerun local and Windows Harness gates.
- If a regression is found after prerelease publication, publish a follow-up
  release candidate instead of retagging `v0.1.16-rc.0`.
- If later validation shows the runtime fixes are acceptable for final, prepare
  a separate direct `v0.1.16` final readiness record from the prerelease
  evidence rather than mutating this tag.

## Release Decision Summary

- Release path: `v0.1.16-rc.0` release-candidate readiness, not direct
  `v0.1.16` final.
- Reason: AD2-AD4 include compatible runtime/privacy drift fixes.
- Fallback path: follow-up release candidate if any product or contract
  regression is found.
- Deterministic gates: AD5 local validation, PR Windows Harness, and
  post-merge `main` Windows Harness passed; GitHub prerelease publication is
  pending.
- Manual UIA gates: fresh manual UIA smoke passed for Notepad and Edge; VS
  Code metadata passed with the known Monaco diagnostic warning; VS Code
  strict marker remains a diagnostic non-blocking failure; watcher preview
  live smoke passed.
- Privacy/scope confirmation: no capture-surface expansion and recorded above.
- Publication approval: pending final prerelease publication decision after
  local, PR, and post-merge validation.
- Release URL: pending.
- Final tag target: pending.
