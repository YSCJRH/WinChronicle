# v0.1.5 Maintenance Release Record

This record captures the published compatible `v0.1.5` maintenance release
from the published `v0.1.4` baseline. It records commands, results, commit
identifiers, CI URLs, environment notes, and local artifact paths only. It
does not commit observed-content artifacts.

## Release Decision

`v0.1.5` is published. The release-readiness PR and post-merge `main` Windows
Harness passed. Publication completed after the active thread goal explicitly
directed stage completion, remote push, and publication.

If any product behavior, schema, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture-surface change is required after
publication, prepare a follow-up release candidate instead of retagging
`v0.1.5`.

Publication status: published maintenance release.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.5` |
| Stage | Published maintenance release |
| Evidence date | 2026-05-08, Asia/Shanghai |
| Base `main` SHA before P4 readiness | `7984a604b225392c29f31ece2abf90d46cc4d482` |
| Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/71 |
| Candidate PR Windows Harness | Passed, run `25544005112`, https://github.com/YSCJRH/WinChronicle/actions/runs/25544005112 |
| Candidate post-merge `main` Windows Harness | Passed, run `25544114712`, https://github.com/YSCJRH/WinChronicle/actions/runs/25544114712 |
| Final pre-publication `main` Windows Harness | Passed, run `25544832155`, https://github.com/YSCJRH/WinChronicle/actions/runs/25544832155 |
| Publication status | Published maintenance release |
| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.5 |
| Final tag target | `89f0c1d5e6c094ed36c0ecf75e18bb7afcd5aaf4` |
| Previous stable release | `v0.1.4` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.4 |
| `v0.1.4` tag target | `31164abe0a391a4cf4e2bf5741395fe7a8ae8750` |
| P0 plan PR | https://github.com/YSCJRH/WinChronicle/pull/66 |
| P0 plan PR Windows Harness | Passed, run `25466564276`, https://github.com/YSCJRH/WinChronicle/actions/runs/25466564276 |
| P0 plan post-merge `main` Windows Harness | Failed, run `25466653439`, superseded by watcher smoke stability fix |
| P0 watcher smoke stability PR | https://github.com/YSCJRH/WinChronicle/pull/67 |
| P0 watcher smoke stability PR Windows Harness | Passed, run `25467036435`, https://github.com/YSCJRH/WinChronicle/actions/runs/25467036435 |
| P0 watcher smoke stability post-merge `main` Windows Harness | Passed, run `25467113028`, https://github.com/YSCJRH/WinChronicle/actions/runs/25467113028 |
| P1 PR | https://github.com/YSCJRH/WinChronicle/pull/68 |
| P1 PR Windows Harness | Passed, run `25542149093`, https://github.com/YSCJRH/WinChronicle/actions/runs/25542149093 |
| P1 post-merge `main` Windows Harness | Passed, run `25542239210`, https://github.com/YSCJRH/WinChronicle/actions/runs/25542239210 |
| P2 PR | https://github.com/YSCJRH/WinChronicle/pull/69 |
| P2 PR Windows Harness | Passed, run `25542609391`, https://github.com/YSCJRH/WinChronicle/actions/runs/25542609391 |
| P2 post-merge `main` Windows Harness | Passed, run `25542706517`, https://github.com/YSCJRH/WinChronicle/actions/runs/25542706517 |
| P3 PR | https://github.com/YSCJRH/WinChronicle/pull/70 |
| P3 PR Windows Harness | Passed, run `25542950919`, https://github.com/YSCJRH/WinChronicle/actions/runs/25542950919 |
| P3 post-merge `main` Windows Harness | Passed, run `25543079012`, https://github.com/YSCJRH/WinChronicle/actions/runs/25543079012 |

Environment:

- Windows PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual UIA smoke is not refreshed for this release-readiness branch because
  P0-P4 changes documentation, tests, deterministic harness evidence, and
  version metadata only. P2 explicitly accepted inherited `v0.1.0` Notepad,
  Edge, VS Code metadata, VS Code strict diagnostic, and watcher preview manual
  evidence for this compatible path only because helper behavior, watcher
  product behavior, manual smoke scripts, capture behavior, privacy behavior,
  product CLI/MCP shape, and capture surfaces are unchanged. If release
  approval requires fresh manual smoke, use
  [Manual smoke evidence template](manual-smoke-evidence-template.md) and keep
  artifacts local.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `102 passed in 23.20s` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The P4 PR Windows Harness and post-merge `main` Windows Harness passed.
The final pre-publication `main` Windows Harness run `25544832155` also
passed on `89f0c1d5e6c094ed36c0ecf75e18bb7afcd5aaf4`.

## Release Notes

- Aligns package, runtime, and MCP server version identity to `0.1.5`.
- Records the published `v0.1.5` maintenance release evidence from the
  post-v0.1.4 maintenance round.
- Keeps the v0.1 product boundary unchanged: no new capture surfaces, no new
  MCP tools, no helper/watcher product behavior changes, and no Phase 6
  implementation.
- Carries forward the P2 manual smoke freshness decision without committing
  observed-content artifacts.

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
  must report `0.1.5`.
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

This maintenance release does not expand the capture surface from `v0.1.4`.

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

- Keep `v0.1.4` as the previous stable release.
- Do not retag or modify `v0.1.4`.
- If a regression is found after publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, publish a follow-up release candidate instead of
  retagging `v0.1.5`.
- If a regression is limited to release documentation, tests, or version
  metadata, fix it on a small PR and rerun Windows Harness before publishing.

## Release Decision Summary

- Release path: compatible `v0.1.5` maintenance release, published.
- Fallback path: release candidate if any product or contract change is
  required after publication.
- Deterministic gates: local P4 validation, PR Windows Harness, post-merge
  `main` Windows Harness, and GitHub release publication passed.
- Manual UIA gates: inherited `v0.1.0` Notepad, Edge, VS Code metadata, VS
  Code strict diagnostic, and watcher preview manual evidence is accepted by
  the P2 decision only because product UIA helper behavior, watcher product
  behavior, manual UIA smoke scripts, capture behavior, privacy behavior,
  product CLI/MCP shape, and capture surfaces are unchanged.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: completed by the active thread goal directing stage
  completion, remote push, and publication.
- Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.5.
- Final tag target: `89f0c1d5e6c094ed36c0ecf75e18bb7afcd5aaf4`.
