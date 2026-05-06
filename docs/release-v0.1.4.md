# v0.1.4 Maintenance Release Readiness Record

This record prepares the compatible `v0.1.4` maintenance release from the
published `v0.1.3` baseline. It records commands, results, commit identifiers,
CI URLs, environment notes, and local artifact paths only. It does not commit
observed-content artifacts.

## Release Decision

`v0.1.4` is prepared but not published. The release-readiness PR and
post-merge `main` Windows Harness passed. Publication remains blocked on
explicit user approval.

If any product behavior, schema, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture-surface change is required before
publication, do not publish direct `v0.1.4`. Prepare a release candidate
instead.

Publication status: pending explicit approval.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.4` |
| Stage | Release readiness, pending publication approval |
| Evidence date | 2026-05-06, Asia/Shanghai |
| Base `main` SHA before P4 readiness | `6a9667eb216906cfdf8846c59b0a716296f25bde` |
| Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/64 |
| Candidate PR Windows Harness | Passed, run `25411926176`, https://github.com/YSCJRH/WinChronicle/actions/runs/25411926176 |
| Candidate post-merge `main` Windows Harness | Passed, run `25411989748`, https://github.com/YSCJRH/WinChronicle/actions/runs/25411989748 |
| Publication status | Pending explicit approval |
| Release URL | Pending |
| Final tag target | Pending |
| Previous stable release | `v0.1.3` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.3 |
| `v0.1.3` tag target | `0aa5c1b6e1959ef6504e6d70e4aad79a60594926` |
| P0 PR | https://github.com/YSCJRH/WinChronicle/pull/59 |
| P0 post-merge `main` Windows Harness | Passed, run `25211231820`, https://github.com/YSCJRH/WinChronicle/actions/runs/25211231820 |
| P1 PR | https://github.com/YSCJRH/WinChronicle/pull/60 |
| P1 post-merge `main` Windows Harness | Passed, run `25237272516`, https://github.com/YSCJRH/WinChronicle/actions/runs/25237272516 |
| P2 PR | https://github.com/YSCJRH/WinChronicle/pull/61 |
| P2 PR Windows Harness | Passed after rerun, run `25410417019`, https://github.com/YSCJRH/WinChronicle/actions/runs/25410417019 |
| P2 post-merge `main` Windows Harness | Failed, run `25410609944`, superseded by P3 harness stability fix |
| P3 smoke stability PR | https://github.com/YSCJRH/WinChronicle/pull/62 |
| P3 smoke stability PR Windows Harness | Passed, run `25410884216`, https://github.com/YSCJRH/WinChronicle/actions/runs/25410884216 |
| P3 smoke stability post-merge `main` Windows Harness | Passed, run `25410946398`, https://github.com/YSCJRH/WinChronicle/actions/runs/25410946398 |
| P3 completion PR | https://github.com/YSCJRH/WinChronicle/pull/63 |
| P3 completion PR Windows Harness | Passed, run `25411148924`, https://github.com/YSCJRH/WinChronicle/actions/runs/25411148924 |
| P3 completion post-merge `main` Windows Harness | Passed, run `25411231216`, https://github.com/YSCJRH/WinChronicle/actions/runs/25411231216 |

Environment:

- Windows PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual UIA smoke is not refreshed for this release-readiness branch because
  P4 changes version metadata, release evidence, and tests only. P3 changed
  deterministic watcher smoke timing and diagnostics, but did not change
  helper behavior, watcher product behavior, manual UIA smoke scripts, capture
  behavior, privacy behavior, product CLI/MCP shape, or capture surfaces.
  Deterministic watcher smoke was refreshed through local and Windows Harness
  evidence. If release approval requires fresh manual smoke, use
  [Manual smoke evidence template](manual-smoke-evidence-template.md) and keep
  artifacts local.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `99 passed in 15.14s` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The P4 PR Windows Harness and post-merge `main` Windows Harness passed.
Publication still requires explicit user approval.

## Release Notes

- Aligns package, runtime, and MCP server version identity to `0.1.4`.
- Records `v0.1.4` release-readiness evidence from the post-v0.1.3 maintenance
  round.
- Keeps the v0.1 product boundary unchanged: no new capture surfaces, no new
  MCP tools, no helper/watcher product behavior changes, and no Phase 6
  implementation.
- Stabilizes deterministic watcher smoke evidence from P3 without changing
  product watcher behavior or manual UIA smoke scripts.

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
  must report `0.1.4`.
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

This maintenance release does not expand the capture surface from `v0.1.3`.

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

- If publication is not approved, keep `v0.1.3` as the latest stable release.
- Do not retag or modify `v0.1.3`.
- If a regression is found before publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, stop the direct `v0.1.4` path and prepare a release
  candidate.
- If a regression is limited to release documentation, tests, or version
  metadata, fix it on a small PR and rerun Windows Harness before requesting
  publication approval.

## Release Decision Summary

- Release path: compatible `v0.1.4` maintenance release, pending explicit
  approval.
- Fallback path: release candidate if any product or contract change is
  required.
- Deterministic gates: local P4 validation, PR Windows Harness, and post-merge
  `main` Windows Harness passed.
- Manual UIA gates: inherited `v0.1.0` Notepad, Edge, and VS Code metadata
  evidence is accepted for readiness only because product UIA helper behavior
  and manual UIA smoke scripts are unchanged; deterministic watcher smoke was
  refreshed through P3 local and Windows Harness evidence.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: pending explicit user approval.
- Release URL: pending.
- Final tag target: pending.
