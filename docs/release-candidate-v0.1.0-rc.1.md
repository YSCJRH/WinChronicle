# v0.1.0-rc.1 Release Candidate Record

This record prepares the `v0.1.0-rc.1` candidate from the post-`rc.0` final
readiness work. It records commands, results, commit identifiers, CI URLs,
environment notes, and local artifact paths only. It does not commit observed
content artifacts.

## Release Decision

`v0.1.0-rc.1` is required before final. Stage F1 changed the operator-facing
privacy contract and CLI/MCP JSON shape by adding observed-content trust
metadata to CLI capture and memory search results and aligning CLI `status`
with MCP `privacy_status`. Per the final-readiness rule, that change must go
through a new release candidate rather than direct `v0.1.0` final.

Publication is not approved by this document. The F5 PR and post-merge `main`
Windows Harness have passed; publish only after explicit approval. The final
tag target should be the `main` SHA verified immediately before publication.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release candidate | `v0.1.0-rc.1` |
| Stage | Stage F5 - Final Or rc.1 Release Decision |
| Evidence date | 2026-04-28, Asia/Shanghai |
| Evidence branch | `codex/final5-release-readiness` |
| Current verified `main` SHA before F5 PR | `d381bcae2a2de66ebe9346ebf427dc3988b86323` |
| F5 merge commit on `main` | `236f57fb308393522323b3bb1139dd3fe1dbf24b` |
| Planned tag target | The `main` SHA verified immediately before publication |
| Publication status | Not published; approval pending |
| Release URL | Pending |
| Previous release-candidate baseline | `v0.1.0-rc.0` |
| Previous release-candidate URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.0-rc.0 |
| Latest post-merge `main` Windows Harness before F5 | Passed, run `25031913300`, https://github.com/YSCJRH/WinChronicle/actions/runs/25031913300 |
| F5 release evidence PR | https://github.com/YSCJRH/WinChronicle/pull/22 |
| F5 PR Windows Harness | Passed, run `25032173686`, https://github.com/YSCJRH/WinChronicle/actions/runs/25032173686 |
| F5 post-merge `main` Windows Harness | Passed, run `25032281387`, https://github.com/YSCJRH/WinChronicle/actions/runs/25032281387 |

Environment:

- Windows interactive desktop, PowerShell.
- Python: `3.11.2`.
- .NET SDK: `8.0.202`.
- Manual smoke artifact root:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-rc1-smoke-fe0d75102242466994890ddb50b2a59f`.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `72 passed in 15.82s` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | Covered by `python harness/scripts/run_harness.py`; install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The F5 PR Windows Harness and post-merge `main` Windows Harness both passed.
Before publication, verify the current `main` SHA and use that SHA as the tag
target.

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
| Real watcher/helper short preview at depth 2 | Heartbeat-only liveness diagnostic | `python -m winchronicle watch --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper dotnet --helper-arg resources/win-uia-helper/bin/Debug/net8.0-windows/win-uia-helper.dll --duration 3 --depth 2 --heartbeat-ms 500 --capture-on-start` returned `captures_written: 0`, `heartbeats: 6`, `duplicates_skipped: 0`, `denylisted_skipped: 0` using temporary `WINCHRONICLE_HOME` |

The heartbeat-only live preview is treated as diagnostic liveness evidence. The
deterministic watcher gates and fake-helper preview passed.

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
  `untrusted_observed_content` in captures, memory, CLI search, and MCP
  responses.
- Password fields and obvious secrets must not be stored, including API keys,
  private keys, JWTs, GitHub tokens, Slack tokens, and token canaries.

## Rollback Notes

- If `v0.1.0-rc.1` is withdrawn, keep `v0.1.0-rc.0` as the last known
  published release-candidate baseline.
- Do not retag `v0.1.0-rc.0`; publish a replacement `v0.1.0-rc.2` if a
  candidate replacement is needed.
- If a regression traces to the F1 CLI/MCP JSON or privacy contract change,
  revert the relevant post-rc.0 PR on a new branch and rerun the deterministic
  checklist before publishing any replacement prerelease.
- If a regression traces to F2-F4 docs/tests-only work, revert the relevant PR
  and keep the product candidate decision anchored on the F1 JSON/privacy
  change.

## Release Decision Summary

- Release path: `v0.1.0-rc.1`, not direct final.
- Reason: post-rc.0 F1 changed CLI/MCP JSON shape and privacy behavior.
- Deterministic gates: passed locally.
- Latest verified `main` before F5 PR: `d381bcae2a2de66ebe9346ebf427dc3988b86323`.
- Latest pre-F5 post-merge `main` Windows Harness: passed, run `25031913300`.
- F5 PR: https://github.com/YSCJRH/WinChronicle/pull/22.
- F5 PR Windows Harness: passed, run `25032173686`.
- F5 merge commit on `main`: `236f57fb308393522323b3bb1139dd3fe1dbf24b`.
- F5 post-merge `main` Windows Harness: passed, run `25032281387`.
- Manual hard gates: Notepad passed; Edge passed.
- Conditional hard gate: VS Code metadata passed because `code.cmd` is
  available.
- Diagnostic non-blocking gate: VS Code strict Monaco marker failed as a known
  limitation, with local artifact path recorded.
- Watcher preview: deterministic and fake-helper preview passed; live depth 2
  preview produced heartbeat-only liveness evidence.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: pending.
