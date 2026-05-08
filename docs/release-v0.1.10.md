# v0.1.10 Maintenance Release Readiness Record

This record prepares the compatible `v0.1.10` maintenance release from the
published `v0.1.9` baseline. It records commands, results, commit identifiers,
CI URLs, environment notes, and local artifact paths only. It does not commit
observed-content artifacts.

## Release Decision

`v0.1.10` is a release-readiness candidate. Local X4 validation passed.
Publication is pending PR Windows Harness, post-merge `main` Windows Harness,
and GitHub release creation.

The direct compatible release path is allowed because X0-X4 change release
evidence, documentation, tests, CI/runtime metadata, compatibility evidence,
and version metadata only. No product behavior, schema, CLI/MCP JSON shape,
privacy behavior, helper/watcher behavior, or capture-surface change is
included.

If any product behavior, schema, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture-surface regression is found before
publication, stop the direct `v0.1.10` path and prepare a release candidate
instead.

Publication status: release-readiness candidate; publication pending.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.10` |
| Stage | Release readiness candidate |
| Evidence date | 2026-05-08, Asia/Shanghai |
| Base `main` SHA before X4 readiness | `d13f84d1849b9300cf534cea55c25a3584aeea02` |
| Candidate PR | Pending X4 PR |
| Candidate PR Windows Harness | Pending X4 PR Windows Harness |
| Candidate post-merge `main` Windows Harness | Pending X4 post-merge Windows Harness |
| Publication status | Pending release publication |
| Release URL | Pending publication |
| Final tag target | Pending publication |
| Previous stable release | `v0.1.9` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.9 |
| `v0.1.9` tag target | `d06ab5bc8bea7520bac2719adb457794c72911d3` |
| X0 PR | https://github.com/YSCJRH/WinChronicle/pull/97 |
| X0 PR Windows Harness | Passed, run `25566609049`, https://github.com/YSCJRH/WinChronicle/actions/runs/25566609049 |
| X0 post-merge `main` Windows Harness | Passed, run `25566750349`, https://github.com/YSCJRH/WinChronicle/actions/runs/25566750349 |
| X1 PR | https://github.com/YSCJRH/WinChronicle/pull/98 |
| X1 PR Windows Harness | Passed, run `25567381942`, https://github.com/YSCJRH/WinChronicle/actions/runs/25567381942 |
| X1 post-merge `main` Windows Harness | Passed, run `25567503424`, https://github.com/YSCJRH/WinChronicle/actions/runs/25567503424 |
| X2 PR | https://github.com/YSCJRH/WinChronicle/pull/99 |
| X2 PR Windows Harness | Passed, run `25567947799`, https://github.com/YSCJRH/WinChronicle/actions/runs/25567947799 |
| X2 post-merge `main` Windows Harness | Passed, run `25568061526`, https://github.com/YSCJRH/WinChronicle/actions/runs/25568061526 |
| X3 PR | https://github.com/YSCJRH/WinChronicle/pull/100 |
| X3 PR Windows Harness | Passed, run `25568494398`, https://github.com/YSCJRH/WinChronicle/actions/runs/25568494398 |
| X3 post-merge `main` Windows Harness | Passed, run `25568639603`, https://github.com/YSCJRH/WinChronicle/actions/runs/25568639603 |

Environment:

- Windows PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual UIA smoke is not refreshed for this maintenance release candidate
  because X0-X4 changes are documentation, tests, CI/runtime metadata,
  deterministic harness evidence, compatibility evidence, and version metadata
  only. This X4 record explicitly accepts inherited `v0.1.0` Notepad, Edge, VS
  Code metadata, VS Code strict diagnostic, and watcher preview manual evidence
  for the compatible `v0.1.10` path only because helper behavior, watcher
  product behavior, manual smoke scripts, capture behavior, privacy behavior,
  product CLI/MCP shape, and capture surfaces are unchanged. If release
  approval requires fresh manual smoke, use
  [Manual smoke evidence template](manual-smoke-evidence-template.md) and keep
  artifacts local.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `115 passed in 15.21s` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The X4 PR Windows Harness and post-merge `main` Windows Harness must pass before
publication.

## Release Notes

- Aligns package, runtime, and MCP server version identity to `0.1.10`.
- Records the `v0.1.10` maintenance release-readiness evidence from the
  post-v0.1.9 maintenance round.
- Keeps the v0.1 product boundary unchanged: no new capture surfaces, no new
  MCP tools, no helper/watcher product behavior changes, and no Phase 6
  implementation.
- Records X0-X3 post-v0.1.9 maintenance evidence and accepts inherited manual
  UIA smoke only for this compatible maintenance path.

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
  must report `0.1.10`.
- The exact read-only MCP tool list remains unchanged:
  `current_context`, `search_captures`, `search_memory`,
  `read_recent_capture`, `recent_activity`, and `privacy_status`.
- MCP exposes no write tools, arbitrary file read tools, desktop control tools,
  screenshot/OCR tools, audio tools, keyboard tools, clipboard tools, network
  tools, or product targeted capture flags.
- Phase 6 remains specification-only; this maintenance release introduces no
  screenshot capture code, no OCR engine integration, no screenshot cache, no
  cache cleanup path, and no OCR-derived storage path.

## Privacy And Scope Confirmation

This maintenance release does not expand the capture surface from `v0.1.9`.

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

## Rollback Notes

- Keep `v0.1.9` as the previous stable release.
- Do not retag or modify `v0.1.9`.
- If a regression is found before publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, prepare a release candidate instead of publishing
  `v0.1.10`.
- If a regression is found after publication and requires product code, schema,
  CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, publish a follow-up release candidate instead of
  retagging `v0.1.10`.
- If a regression is limited to release documentation, tests, CI/runtime
  metadata, or version metadata, fix it on a small PR and rerun Windows Harness
  before publishing.

## Release Decision Summary

- Release path: compatible `v0.1.10` maintenance release-readiness candidate.
- Fallback path: release candidate if any product or contract change is
  required before publication.
- Deterministic gates: local X4 validation passed; PR Windows Harness and
  post-merge `main` Windows Harness are pending.
- Manual UIA gates: inherited `v0.1.0` Notepad, Edge, VS Code metadata, VS Code
  strict diagnostic, and watcher preview manual evidence is explicitly accepted
  by this X4 record for the compatible `v0.1.10` path only because product UIA
  helper behavior, watcher product behavior, manual UIA smoke scripts, capture
  behavior, privacy behavior, product CLI/MCP shape, and capture surfaces are
  unchanged.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: active goal authorizes publication after local, PR, and
  post-merge release gates pass.
- Release URL: pending publication.
- Final tag target: pending publication.
