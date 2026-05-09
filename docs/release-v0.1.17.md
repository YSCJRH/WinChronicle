# v0.1.17 Maintenance Release Record

This record captures the published narrow `v0.1.17` maintenance release from
the published `v0.1.16` stable baseline. It records commands, results, commit
identifiers, CI URLs, environment notes, and local artifact paths only. It does
not commit observed-content artifacts.

## Release Decision

`v0.1.17` is published as a compatible maintenance release. The release
contains compatible privacy, trust-boundary, diagnostics, documentation, and
test hardening accumulated after `v0.1.16`. It does not retag `v0.1.16` and it
does not expand the v0.1 product boundary.

Publication completed after the release-readiness PR, PR Windows Harness,
post-merge `main` Windows Harness, release metadata verification, and remote tag
verification passed. `v0.1.17` is now the latest published stable release;
`v0.1.16` remains the previous stable release.

Publication status: published maintenance release.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.17` |
| Stage | AF6 v0.1.17 published maintenance release |
| Evidence date | 2026-05-09, Asia/Shanghai |
| Base `main` SHA before this record | `bbf6d3c64d7fef435e66d64d4e3b19d2390c391b` |
| Candidate branch | `codex/v017-release-readiness` |
| Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/159 |
| Publication reconciliation branch | `codex/v017-publication-reconciliation` |
| Publication status | Published maintenance release |
| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.17 |
| Published at | `2026-05-09T12:56:45Z` |
| Final tag target | `5b260edc3bddc48986e52179b2ffd261856a89ac` |
| Previous stable release | `v0.1.16` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16 |
| `v0.1.16` tag target | `255f2a01cddde330d756a87359c4d3a8be4b11a2` |
| `v0.1.16` published at | `2026-05-09T09:31:17Z` |
| AF5 decision PR | https://github.com/YSCJRH/WinChronicle/pull/158 |
| AF5 decision merge SHA | `bbf6d3c64d7fef435e66d64d4e3b19d2390c391b` |
| AF5 PR Windows Harness | Passed, run `25600947496`, https://github.com/YSCJRH/WinChronicle/actions/runs/25600947496 |
| AF5 post-merge `main` Windows Harness | Passed, run `25600994238`, https://github.com/YSCJRH/WinChronicle/actions/runs/25600994238 |
| Candidate PR Windows Harness | Passed, run `25601571665`, https://github.com/YSCJRH/WinChronicle/actions/runs/25601571665 |
| Candidate post-merge `main` Windows Harness | Passed, run `25601624151`, https://github.com/YSCJRH/WinChronicle/actions/runs/25601624151 |

Environment:

- Windows interactive desktop, PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual smoke artifact root:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-v017-smoke-4791eae86c294272b651b9d57a7c3b04`.
- Manual watcher temporary state:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-v017-smoke-4791eae86c294272b651b9d57a7c3b04\watch-state`.
- Controlled Notepad watcher temporary state:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-v017-smoke-4791eae86c294272b651b9d57a7c3b04\watch-state-notepad`.

## Publication Checks

| Check | Result | Evidence |
| --- | --- | --- |
| `gh release view v0.1.17` before readiness | Pass | release not found |
| `git ls-remote --tags origin v0.1.17 v0.1.17-rc.0` before readiness | Pass | no remote tags returned |
| `git tag --list "v0.1.17*"` before readiness | Pass | no local tags returned |
| `gh release view v0.1.16 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` | Pass | `v0.1.16` remains published, not a draft, not a prerelease |
| `git rev-parse v0.1.16` | Pass | `255f2a01cddde330d756a87359c4d3a8be4b11a2` |
| `gh release create v0.1.17 --target 5b260edc3bddc48986e52179b2ffd261856a89ac` | Pass | release created at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.17 |
| `gh release view v0.1.17 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` | Pass | `v0.1.17` is published, not a draft, not a prerelease, published at `2026-05-09T12:56:45Z`, and targets `5b260edc3bddc48986e52179b2ffd261856a89ac` |
| `git ls-remote --tags origin v0.1.17` | Pass | `5b260edc3bddc48986e52179b2ffd261856a89ac` |

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `167 passed` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The candidate PR Windows Harness and post-merge `main` Windows Harness passed
before publication. This publication reconciliation updates the mainline
evidence record after the tag was created; the `v0.1.17` tag remains immutable
at `5b260edc3bddc48986e52179b2ffd261856a89ac`.

## Manual UIA Smoke Gates

Manual smoke used local temporary artifacts only. Do not commit the artifact
JSON files; they may contain observed screen content.

| Gate | Result | Evidence |
| --- | --- | --- |
| Notepad targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-notepad.ps1 -ArtifactDir <artifact-root>\notepad -TimeoutSeconds 30`; artifact `<artifact-root>\notepad\notepad-capture.json` |
| Edge targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-edge.ps1 -ArtifactDir <artifact-root>\edge -TimeoutSeconds 45`; artifact `<artifact-root>\edge\edge-capture.json` |
| VS Code availability | Available | `code.cmd` available at `C:\Users\34793\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd` |
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
| Deterministic watcher fixture and fake-helper preview | Pass | Covered by `python harness/scripts/run_harness.py`; fixture watcher wrote 1 capture and skipped 1 duplicate, fake-helper preview wrote 1 capture |
| Real watcher/helper short preview | Heartbeat-only liveness diagnostic | `python -m winchronicle watch --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper dotnet --helper-arg resources/win-uia-helper/bin/Debug/net8.0-windows/win-uia-helper.dll --duration 5 --depth 2 --heartbeat-ms 500 --capture-on-start` returned `captures_written: 0`, `denylisted_skipped: 0`, `duplicates_skipped: 0`, `heartbeats: 9` using temporary `WINCHRONICLE_HOME` |
| Controlled Notepad live watcher retry | Heartbeat-only liveness diagnostic | Same watcher/helper command after starting a temporary Notepad window returned `captures_written: 0`, `denylisted_skipped: 0`, `duplicates_skipped: 0`, `heartbeats: 9` using temporary `WINCHRONICLE_HOME` |

The heartbeat-only live preview is diagnostic liveness evidence, not a hard
failure by itself. The release gate relies on the fresh Notepad, Edge, and
conditional VS Code targeted UIA hard gates plus deterministic watcher gates.

## Release Notes

- Aligns package, runtime, and MCP server version identity to `0.1.17`.
- Includes the AF2 privacy-positive `watch --events` invalid embedded helper
  payload diagnostic, which avoids echoing observed payload text.
- Includes the AF3 additive `generate-memory` manifest JSON trust fields:
  `trust`, `untrusted_observed_content`, and `instruction`.
- Includes the AF3 MCP read-only boundary hardening for broader forbidden
  write, file, network, and desktop-control-like tool names.
- Freezes the exact read-only MCP tool list in standalone smoke:
  `current_context`, `search_captures`, `search_memory`,
  `read_recent_capture`, `recent_activity`, and `privacy_status`.
- Keeps WinChronicle local-first, UIA-first, harness-first, and read-only MCP
  first.
- Keeps screenshots, OCR, audio, keyboard capture, clipboard capture, network
  upload, LLM calls, desktop control, product targeted capture, daemon/service
  install, polling capture loops, and default background capture out of v0.1.
- Records fresh manual hard-gate UIA smoke for the `v0.1.17` release path.

## Compatibility Evidence

- `pyproject.toml`, `winchronicle.__version__`, and MCP `serverInfo.version`
  must report `0.1.17`.
- The exact read-only MCP tool list remains unchanged:
  `current_context`, `search_captures`, `search_memory`,
  `read_recent_capture`, `recent_activity`, and `privacy_status`.
- MCP exposes no write tools, arbitrary file read tools, desktop control tools,
  screenshot/OCR tools, audio tools, keyboard tools, clipboard tools, network
  tools, or product targeted capture flags.
- Product CLI exposes no targeted `--hwnd`, `--pid`, `--window-title`,
  `--window-title-regex`, or `--process-name` capture flags.
- `generate-memory` manifest JSON has an additive trust-boundary shape;
  exact-key consumers must tolerate `trust`, `untrusted_observed_content`, and
  `instruction`.
- Phase 6 remains specification-only; this maintenance release introduces no
  screenshot capture code, no OCR engine integration, no screenshot cache, no
  cache cleanup path, and no OCR-derived storage path.

## Privacy And Scope Confirmation

This maintenance release does not expand the capture surface beyond `v0.1.16`.

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

- Keep `v0.1.17` as the latest stable release after publication verification.
- Keep `v0.1.16` as the previous stable release.
- Do not retag or modify `v0.1.17` or `v0.1.16`.
- Do not create or retag `v0.1.17-rc.0` unless a later regression requires a
  candidate path instead of direct maintenance publication.
- If a regression is found after publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, publish a follow-up release instead of retagging
  `v0.1.17`.

## Release Decision Summary

- Release path: direct `v0.1.17` compatible maintenance publication completed
  after PR review, PR Windows Harness, post-merge `main` Windows Harness, and
  explicit publication verification.
- Fallback path: a later maintenance release if any product or contract change
  is required after publication.
- Deterministic gates: local validation, PR Windows Harness, and post-merge
  `main` Windows Harness passed.
- Manual hard gates: Notepad passed; Edge passed.
- Conditional hard gate: VS Code metadata passed because `code.cmd` is
  available.
- Diagnostic non-blocking gate: VS Code strict Monaco marker failed as a known
  limitation, with local artifact path recorded.
- Watcher preview: live preview returned heartbeat-only liveness evidence in
  this desktop state; deterministic watcher gates passed before publication.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: standing user goal authorizes publishing after review
  and validation.
- GitHub release publication: passed.
- Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.17.
- Final tag target: `5b260edc3bddc48986e52179b2ffd261856a89ac`.
