# v0.1.18 Release-Readiness Record

This record prepares a narrow `v0.1.18` compatible maintenance release from
the published `v0.1.17` stable baseline. It records commands, results, commit
identifiers, CI URLs, environment notes, and local artifact paths only. It does
not commit observed-content artifacts.

## Release Decision

`v0.1.18` is ready for PR review as a compatible maintenance release
candidate. The release is warranted by the post-`v0.1.17` privacy-check
validation hardening in `src/winchronicle/capture.py`: already-normalized
denylisted captures and raw password-field artifacts now fail
`privacy-check` instead of being under-validated.

This record does not publish by itself. Publication still requires PR review,
PR Windows Harness, post-merge `main` Windows Harness, GitHub release
publication targeting the post-merge SHA, release metadata verification, remote
tag verification, and a publication reconciliation update. Do not retag
`v0.1.17`; it is published and immutable.

Publication status: ready for reviewed `v0.1.18` maintenance publication.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.18` |
| Stage | `v0.1.18` release-readiness record |
| Evidence date | 2026-05-10, Asia/Shanghai |
| Base `main` SHA before this record | `db9b388298facd0a8b387f86bc0dcfa1fa546bc5` |
| Candidate branch | `codex/v0.1.18-release-readiness-record` |
| Publication status | Ready for reviewed maintenance publication |
| Release URL | Pending: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.18 |
| Published at | Pending |
| Final tag target | Pending post-merge `main` SHA |
| Previous stable release | `v0.1.17` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.17 |
| `v0.1.17` tag target | `5b260edc3bddc48986e52179b2ffd261856a89ac` |
| `v0.1.17` published at | `2026-05-09T12:56:45Z` |
| Privacy-policy parity PR | https://github.com/YSCJRH/WinChronicle/pull/185 |
| PR #185 Windows Harness | Passed, run `25611312314`, https://github.com/YSCJRH/WinChronicle/actions/runs/25611312314 |
| PR #185 post-merge `main` Windows Harness | Passed, run `25611363701`, https://github.com/YSCJRH/WinChronicle/actions/runs/25611363701 |
| Privacy-check release decision PR | https://github.com/YSCJRH/WinChronicle/pull/186 |
| PR #186 Windows Harness | Passed, run `25611769944`, https://github.com/YSCJRH/WinChronicle/actions/runs/25611769944 |
| PR #186 post-merge `main` Windows Harness | Passed, run `25611836358`, https://github.com/YSCJRH/WinChronicle/actions/runs/25611836358 |

Environment:

- Windows interactive desktop, PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual smoke artifact root:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-v018-smoke-486b0dd9a2cd4c8d867a6ea2fe048a86`.
- Manual watcher temporary state:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-v018-smoke-486b0dd9a2cd4c8d867a6ea2fe048a86\watch-state`.
- Controlled Notepad watcher temporary state:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-v018-smoke-486b0dd9a2cd4c8d867a6ea2fe048a86\watch-state-notepad`.

## Pre-Publication Checks

| Check | Result | Evidence |
| --- | --- | --- |
| `gh release view v0.1.18 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` | Pass | release not found, confirming no existing `v0.1.18` release to retag |
| `git tag --list "v0.1.18*"` | Pass | no local tags returned |
| `git ls-remote --tags origin v0.1.18 v0.1.18-rc.0` | Pass | no remote tags returned |
| `gh release view v0.1.17 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` | Pass | `v0.1.17` is published, not a draft, not a prerelease, published at `2026-05-09T12:56:45Z`, and targets `5b260edc3bddc48986e52179b2ffd261856a89ac` |
| `git diff --name-only v0.1.17..HEAD -- src\winchronicle resources pyproject.toml` before this branch | Pass | runtime/resource/version diff was limited to `src/winchronicle/capture.py` before the `0.1.18` version bump |

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest tests/test_cli.py tests/test_privacy_check.py tests/test_redaction.py tests/test_privacy_policy_contract.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py tests/test_version_identity.py -q` | Pass | `108 passed` |
| `python -m pytest -q` | Pass | `204 passed` |
| `git diff --check` | Pass | no whitespace errors |
| `git diff --name-only -- src\winchronicle resources pyproject.toml` | Pass | printed `pyproject.toml` and `src/winchronicle/_version.py`; current branch release-readiness diff is version metadata only |
| `python harness/scripts/run_harness.py` | Pass | full harness passed, including `204` pytest tests, helper/watcher .NET builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke |

PR Windows Harness and post-merge `main` Windows Harness are required before
publication.

## Manual UIA Smoke Gates

Manual smoke used local temporary artifacts only. Do not commit the artifact
JSON files; they may contain observed screen content.

The `v0.1.18` release-readiness path reran fresh hard-gate manual UIA smoke
because the release is triggered by privacy-check validation behavior after
`v0.1.17`. Helper behavior, watcher product behavior, manual smoke scripts,
product CLI/MCP shape, and capture surfaces remain unchanged, but fresh smoke
keeps publication evidence explicit.

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
| Deterministic watcher fixture and fake-helper preview | Pass | `python harness/scripts/run_harness.py` passed; fixture watcher wrote `captures_written: 1`, `duplicates_skipped: 1`, `heartbeats: 1`; fake-helper watcher wrote `captures_written: 1`, `duplicates_skipped: 0`, `heartbeats: 3` |
| Real watcher/helper short preview | Heartbeat-only liveness diagnostic | `python -m winchronicle watch --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper dotnet --helper-arg resources/win-uia-helper/bin/Debug/net8.0-windows/win-uia-helper.dll --duration 5 --depth 2 --heartbeat-ms 500 --capture-on-start` returned `captures_written: 0`, `denylisted_skipped: 0`, `duplicates_skipped: 0`, `heartbeats: 9` using temporary `WINCHRONICLE_HOME` |
| Controlled Notepad live watcher retry | Heartbeat-only liveness diagnostic | Same watcher/helper command after starting a temporary Notepad window returned `captures_written: 0`, `denylisted_skipped: 0`, `duplicates_skipped: 0`, `heartbeats: 9` using temporary `WINCHRONICLE_HOME` |

The heartbeat-only live preview is diagnostic liveness evidence, not a hard
failure by itself. The release gate relies on the fresh Notepad, Edge, and
conditional VS Code targeted UIA hard gates plus deterministic watcher gates.

## Release Notes

- Aligns package, runtime, and MCP server version identity to `0.1.18`.
- Includes the post-`v0.1.17` privacy-check validation hardening from PR #185:
  already-normalized denylisted captures fail as already-written violations,
  normalized password fields are checked by field semantics, and
  WinChronicle token canaries are covered by privacy-check messaging and tests.
- Adds a CLI regression that verifies `privacy-check` fails an existing
  normalized denylisted capture with a content-free diagnostic.
- Keeps WinChronicle local-first, UIA-first, harness-first, and read-only MCP
  first.
- Keeps screenshots, OCR, audio, keyboard capture, clipboard capture, network
  upload, LLM calls, desktop control, product targeted capture, daemon/service
  install, polling capture loops, and default background capture out of v0.1.
- Records fresh manual hard-gate UIA smoke for the `v0.1.18` release path.

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
  must report `0.1.18`.
- The exact read-only MCP tool list remains unchanged:
  `current_context`, `search_captures`, `search_memory`,
  `read_recent_capture`, `recent_activity`, and `privacy_status`.
- MCP exposes no write tools, arbitrary file read tools, desktop control tools,
  screenshot/OCR tools, audio tools, keyboard tools, clipboard tools, network
  tools, or product targeted capture flags.
- Product CLI exposes no targeted `--hwnd`, `--pid`, `--window-title`,
  `--window-title-regex`, or `--process-name` capture flags.
- `generate-memory` manifest JSON keeps the compatible AF3 trust-boundary
  fields `trust`, `untrusted_observed_content`, and `instruction`.
- Phase 6 remains specification-only; this maintenance release introduces no
  screenshot capture code, no OCR engine integration, no screenshot cache, no
  cache cleanup path, and no OCR-derived storage path.

## Privacy And Scope Confirmation

This maintenance release does not expand the capture surface beyond `v0.1.17`.

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

- Keep `v0.1.17` as the latest stable release until `v0.1.18` publication is
  verified.
- Keep `v0.1.16` as the previous stable release until `v0.1.18` publication is
  verified.
- Do not retag or modify `v0.1.17` or `v0.1.16`.
- If a regression is found before publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, stop the direct maintenance path and prepare a
  `v0.1.18-rc.0` release candidate instead.
- If a regression is found after publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, publish a follow-up release instead of retagging
  `v0.1.18`.
- If a regression is limited to release documentation, tests, GitHub metadata,
  CI/runtime metadata, or version metadata, fix it on a small PR and rerun
  Windows Harness before publishing.

## Release Decision Summary

- Release path: direct `v0.1.18` compatible maintenance publication after PR
  review, PR Windows Harness, post-merge `main` Windows Harness, and explicit
  publication verification.
- Fallback path: `v0.1.18-rc.0` if any product or contract change is required
  before publication.
- Deterministic gates: local validation passed; PR Windows Harness and
  post-merge `main` Windows Harness remain required.
- Manual hard gates: Notepad passed; Edge passed.
- Conditional hard gate: VS Code metadata passed because `code.cmd` is
  available.
- Diagnostic non-blocking gate: VS Code strict Monaco marker failed as a known
  limitation, with local artifact path recorded.
- Watcher preview: live preview returned heartbeat-only liveness evidence in
  this desktop state; deterministic watcher gates passed locally and remain
  required in PR/post-merge Windows Harness before publication.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: standing user goal authorizes publishing after review
  and validation.
- GitHub release publication: pending.
- Release URL: pending, https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.18.
- Final tag target: pending post-merge `main` SHA.
