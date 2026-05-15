# v0.1.19 Maintenance Release Record

This record captures the published narrow `v0.1.19` compatible maintenance release from
the published `v0.1.18` stable baseline. It records commands, results, commit
identifiers, CI URLs, environment notes, and local artifact paths only. It does
not commit observed-content artifacts.

## Release Decision

`v0.1.19` is published as a compatible maintenance release. The release is
warranted by the post-`v0.1.18` privacy-output hardening from AH14: read-only MCP
`search_captures` and `search_memory` responses now redact secret-like
`result.query` echoes, and standalone private-key boundary markers are covered
by redaction.

Publication completed after local deterministic validation, PR review, PR
Windows Harness, post-merge `main` Windows Harness, GitHub release publication,
release metadata verification, and remote tag verification. This publication
reconciliation records those post-publication facts for mainline evidence after
the tag was created. Do not retag `v0.1.19` or `v0.1.18`; both are published
and immutable.

Publication status: published maintenance release.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.19` |
| Stage | `v0.1.19` published maintenance release |
| Evidence date | 2026-05-11, Asia/Shanghai |
| Base `main` SHA before this record | `d2d4d9bc90039ff9fbc2edcee9754b8955a5f6ed` |
| Candidate branch | `codex/v0.1.19-release-readiness-record` |
| Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/206 |
| Publication reconciliation branch | `codex/v0.1.19-publication-reconciliation` |
| Publication status | Published maintenance release |
| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.19 |
| Published at | `2026-05-15T02:31:50Z` |
| Final tag target | `c087f9e5daaf9e48b5529b5f7188d047714f3552` |
| Previous stable release | `v0.1.18` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.18 |
| `v0.1.18` tag target | `2e22ec9805edb0efd48e5ef4aacbcff13f0490ec` |
| `v0.1.18` published at | `2026-05-09T21:38:33Z` |
| AH14 residual gap audit PR | https://github.com/YSCJRH/WinChronicle/pull/203 |
| PR #203 Windows Harness | Passed, run `25617962810`, https://github.com/YSCJRH/WinChronicle/actions/runs/25617962810 |
| PR #203 post-merge `main` Windows Harness | Passed, run `25618020212`, https://github.com/YSCJRH/WinChronicle/actions/runs/25618020212 |
| AH15 evidence reconciliation PR | https://github.com/YSCJRH/WinChronicle/pull/204 |
| PR #204 Windows Harness | Passed, run `25618201016`, https://github.com/YSCJRH/WinChronicle/actions/runs/25618201016 |
| PR #204 post-merge `main` Windows Harness | Passed, run `25618271963`, https://github.com/YSCJRH/WinChronicle/actions/runs/25618271963 |
| Privacy-output release decision PR | https://github.com/YSCJRH/WinChronicle/pull/205 |
| PR #205 Windows Harness | Passed, run `25648554264`, https://github.com/YSCJRH/WinChronicle/actions/runs/25648554264 |
| PR #205 post-merge `main` Windows Harness | Passed, run `25648668344`, https://github.com/YSCJRH/WinChronicle/actions/runs/25648668344 |
| Candidate PR Windows Harness | Passed, run `25896736903`, https://github.com/YSCJRH/WinChronicle/actions/runs/25896736903 |
| Candidate post-merge `main` Windows Harness | Passed, run `25896975136`, https://github.com/YSCJRH/WinChronicle/actions/runs/25896975136 |
| Publication reconciliation PR | https://github.com/YSCJRH/WinChronicle/pull/207 |
| Publication reconciliation PR Windows Harness | Passed, run `25897590925`, https://github.com/YSCJRH/WinChronicle/actions/runs/25897590925 |

Environment:

- Windows interactive desktop, PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual smoke artifact root:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-v019-smoke-410f3fb03ccf4c2d861ce33e93598919`.
- Manual watcher temporary state:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-v019-smoke-410f3fb03ccf4c2d861ce33e93598919\watch-state`.
- Controlled Notepad watcher temporary state:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-v019-smoke-410f3fb03ccf4c2d861ce33e93598919\watch-state-notepad`.

## Publication Checks

| Check | Result | Evidence |
| --- | --- | --- |
| `gh release view v0.1.19 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` | Pass | release not found, confirming no existing `v0.1.19` release to retag |
| `git tag --list "v0.1.19*"` | Pass | no local tags returned |
| `git ls-remote --tags origin v0.1.19 v0.1.19-rc.0` | Pass | no remote tags returned |
| `gh release view v0.1.18 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` | Pass | `v0.1.18` is published, not a draft, not a prerelease, published at `2026-05-09T21:38:33Z`, and targets `2e22ec9805edb0efd48e5ef4aacbcff13f0490ec` |
| `git diff --name-only v0.1.18..HEAD -- pyproject.toml src\winchronicle resources` before this branch | Pass | product/runtime diff was limited to `src/winchronicle/mcp/server.py` and `src/winchronicle/redaction.py`; `pyproject.toml` and `resources` printed no files before the `0.1.19` version bump |
| `gh release create v0.1.19 --target c087f9e5daaf9e48b5529b5f7188d047714f3552` | Pass | release created at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.19 |
| `gh release view v0.1.19 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` | Pass | `v0.1.19` is published, not a draft, not a prerelease, published at `2026-05-15T02:31:50Z`, and targets `c087f9e5daaf9e48b5529b5f7188d047714f3552` |
| `git ls-remote --tags origin v0.1.19` | Pass | `c087f9e5daaf9e48b5529b5f7188d047714f3552` |

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest tests/test_mcp_tools.py tests/test_redaction.py tests/test_privacy_index_parity.py tests/test_privacy_policy_contract.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` | Pass | `123 passed` |
| `python -m pytest -q` | Pass | `229 passed` |
| `git diff --check` | Pass | no whitespace errors |
| `git diff --name-only -- src\winchronicle resources pyproject.toml` | Pass | printed only `pyproject.toml` and `src/winchronicle/_version.py`, confirming version metadata plus docs/tests only |
| `python harness/scripts/run_harness.py` | Pass | full harness passed: 229 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke |

The candidate PR Windows Harness and post-merge `main` Windows Harness passed
before publication. This publication reconciliation updates the mainline
evidence record after the tag was created; the `v0.1.19` tag remains immutable
at `c087f9e5daaf9e48b5529b5f7188d047714f3552`.

## Manual UIA Smoke Gates

Manual smoke used local temporary artifacts only. Do not commit the artifact
JSON files; they may contain observed screen content.

The `v0.1.19` release-readiness path reran fresh hard-gate manual UIA smoke
because the release is triggered by privacy and read-only MCP output behavior
changes after `v0.1.18`. Helper behavior, watcher product behavior, manual
smoke scripts, capture behavior, and capture surfaces remain unchanged, but
fresh smoke keeps publication evidence explicit for a privacy-output release.

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
| Deterministic watcher fixture and fake-helper preview | Pass | `python harness/scripts/run_harness.py` passed; deterministic fixture returned `captures_written: 1`, `duplicates_skipped: 1`, `heartbeats: 1`, and fake-helper watcher smoke returned `captures_written: 1`, `denylisted_skipped: 0`, `duplicates_skipped: 0`, `heartbeats: 3` |
| Real watcher/helper short preview | Heartbeat-only liveness diagnostic | `python -m winchronicle watch --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper dotnet --helper-arg resources/win-uia-helper/bin/Debug/net8.0-windows/win-uia-helper.dll --duration 5 --depth 2 --heartbeat-ms 500 --capture-on-start` returned `captures_written: 0`, `denylisted_skipped: 0`, `duplicates_skipped: 0`, `heartbeats: 10` using temporary `WINCHRONICLE_HOME` |
| Controlled Notepad live watcher retry | Heartbeat-only liveness diagnostic | Same watcher/helper command after starting a temporary Notepad window returned `captures_written: 0`, `denylisted_skipped: 0`, `duplicates_skipped: 0`, `heartbeats: 10` using temporary `WINCHRONICLE_HOME` |

The heartbeat-only live preview is diagnostic liveness evidence, not a hard
failure by itself. The release gate relies on the fresh Notepad, Edge, and
conditional VS Code targeted UIA hard gates plus deterministic watcher gates.

## Release Notes

- Aligns package, runtime, and MCP server version identity to `0.1.19`.
- Includes the post-`v0.1.18` privacy-output hardening from PR #203:
  `search_captures` and `search_memory` still search with raw local queries,
  but returned read-only MCP `result.query` values are redacted before reaching
  clients.
- Extends private-key redaction to standalone `BEGIN ... PRIVATE KEY` and
  `END ... PRIVATE KEY` boundary markers.
- Keeps WinChronicle local-first, UIA-first, harness-first, and read-only MCP
  first.
- Keeps screenshots, OCR, audio, keyboard capture, clipboard capture, network
  upload, LLM calls, desktop control, product targeted capture, daemon/service
  install, polling capture loops, and default background capture out of v0.1.
- Records fresh manual hard-gate UIA smoke for the `v0.1.19` release path.

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
  must report `0.1.19`.
- The exact read-only MCP tool list remains unchanged:
  `current_context`, `search_captures`, `search_memory`,
  `read_recent_capture`, `recent_activity`, and `privacy_status`.
- MCP exposes no write tools, arbitrary file read tools, desktop control tools,
  screenshot/OCR tools, audio tools, keyboard tools, clipboard tools, network
  tools, or product targeted capture flags.
- Product CLI exposes no targeted `--hwnd`, `--pid`, `--window-title`,
  `--window-title-regex`, or `--process-name` capture flags.
- `generate-memory` manifest JSON keeps the compatible trust-boundary fields
  `trust`, `untrusted_observed_content`, and `instruction`.
- Phase 6 remains specification-only; this maintenance release introduces no
  screenshot capture code, no OCR engine integration, no screenshot cache, no
  cache cleanup path, and no OCR-derived storage path.

## Privacy And Scope Confirmation

This maintenance release does not expand the capture surface beyond `v0.1.18`.

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

- Keep `v0.1.19` as the latest stable release after publication verification.
- Keep `v0.1.18` as the previous stable release after publication verification.
- Do not retag or modify `v0.1.19`, `v0.1.18`, `v0.1.17`, or `v0.1.16`.
- If a regression is found after publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, publish a follow-up release instead of retagging
  `v0.1.19`.
- If a regression is limited to release documentation, tests, GitHub metadata,
  CI/runtime metadata, or version metadata, fix it on a small PR and rerun
  Windows Harness before publishing.

## Release Decision Summary

- Release path: direct `v0.1.19` compatible maintenance publication completed
  after local deterministic validation, PR review, PR Windows Harness,
  post-merge `main` Windows Harness, and explicit publication verification.
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
- Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.19.
- Final tag target: `c087f9e5daaf9e48b5529b5f7188d047714f3552`.
