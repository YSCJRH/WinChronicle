# v0.1.2 Maintenance Release Record

This record reconciles the compatible `v0.1.2` maintenance release from the
published `v0.1.1` baseline. It records commands, results, commit identifiers,
CI URLs, environment notes, and local artifact paths only. It does not commit
observed-content artifacts.

## Release Decision

`v0.1.2` was published after explicit approval. The release tag targets the
release-approved `main` SHA whose Windows Harness passed.

If any product behavior, schema, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture-surface change is required before
publication, do not retag `v0.1.2`. Prepare a follow-up release candidate or
maintenance release instead.

Publication status: published maintenance release.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.2` |
| Stage | Published maintenance release |
| Evidence date | 2026-04-29, Asia/Shanghai |
| Current candidate `main` SHA before this record | `b97137e005107b157b9d28fff15e6dce910f58c8` |
| Final tag target | `8bc8e9adf01e72031e5fb776007d4152a065ccb2` |
| Publication status | Published maintenance release |
| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.2 |
| Published at | 2026-04-29T00:05:57Z |
| Previous stable release | `v0.1.1` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.1 |
| `v0.1.1` tag target | `8ac594176d251c867e34c2a139a1029a3fc474da` |
| Stage V0 PR | https://github.com/YSCJRH/WinChronicle/pull/47 |
| Stage V0 post-merge `main` Windows Harness | Passed, run `25050142411`, https://github.com/YSCJRH/WinChronicle/actions/runs/25050142411 |
| Stage V1 PR | https://github.com/YSCJRH/WinChronicle/pull/48 |
| Stage V1 post-merge `main` Windows Harness | Passed, run `25051687214`, https://github.com/YSCJRH/WinChronicle/actions/runs/25051687214 |
| Stage V2 PR | https://github.com/YSCJRH/WinChronicle/pull/49 |
| Stage V2 post-merge `main` Windows Harness | Passed, run `25052277331`, https://github.com/YSCJRH/WinChronicle/actions/runs/25052277331 |
| Stage V3 PR | https://github.com/YSCJRH/WinChronicle/pull/50 |
| Stage V3 post-merge `main` Windows Harness | Passed, run `25052943017`, https://github.com/YSCJRH/WinChronicle/actions/runs/25052943017 |
| Stage V4 PR | https://github.com/YSCJRH/WinChronicle/pull/51 |
| Stage V4 PR Windows Harness | Passed, run `25053694479`, https://github.com/YSCJRH/WinChronicle/actions/runs/25053694479 |
| Stage V4 post-merge `main` Windows Harness | Passed, run `25053851860`, https://github.com/YSCJRH/WinChronicle/actions/runs/25053851860 |

Environment:

- Windows PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual UIA smoke was not required for this release record because no
  helper/smoke behavior or smoke documentation materially changes. This V4
  change updated version metadata and release evidence only. If future release
  approval requires fresh manual smoke evidence, use
  [Manual smoke evidence template](manual-smoke-evidence-template.md) and keep
  artifacts local.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `89 passed in 15.94s` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The Stage V4 PR Windows Harness and post-merge `main` Windows Harness passed
before publication.

## Release Notes

- Aligns package, runtime, and MCP server version identity to `0.1.2`.
- Records `v0.1.2` release evidence from the post-v0.1.1 maintenance
  round.
- Keeps the v0.1 product boundary unchanged: no new capture surfaces, no new
  MCP tools, no helper/watcher behavior changes, and no Phase 6 implementation.

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
  must report `0.1.2`.
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

This maintenance release does not expand the capture surface from `v0.1.1`.

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

- If publication is withdrawn, keep `v0.1.1` as the latest stable release.
- Do not retag `v0.1.2`; publish a replacement candidate if a product or
  contract change is required.
- If a regression is found before publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, stop the direct `v0.1.2` path and prepare a release
  candidate.
- If a regression is limited to release documentation, tests, or version
  metadata, fix it on a small PR and rerun Windows Harness before
  reconsidering release approval.

## Release Decision Summary

- Release path: compatible `v0.1.2` maintenance release was published after
  explicit approval.
- Fallback path: release candidate if any product or contract change is
  required.
- Deterministic gates: local V4 validation, PR Windows Harness, and post-merge
  `main` Windows Harness passed.
- Manual UIA gates: not rerun for this version/evidence-only maintenance step;
  use the manual smoke evidence template if fresh manual evidence is required
  before publication.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: granted by the user message `允许发布 v0.1.2`.
- Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.2.
- Final tag target: `8bc8e9adf01e72031e5fb776007d4152a065ccb2`.
