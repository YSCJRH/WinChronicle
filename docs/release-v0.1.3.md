# v0.1.3 Maintenance Release Record

This record reconciles the compatible `v0.1.3` maintenance release from the
published `v0.1.2` baseline. It records commands, results, commit identifiers,
CI URLs, environment notes, and local artifact paths only. It does not commit
observed-content artifacts.

## Release Decision

`v0.1.3` was published after explicit approval. The release tag targets the
release-approved `main` SHA whose Windows Harness passed.

If any product behavior, schema, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture-surface change is required before
publication, do not retag `v0.1.3`. Prepare a follow-up release candidate or
maintenance release instead.

Publication status: published maintenance release.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.3` |
| Stage | Published maintenance release |
| Evidence date | 2026-05-01, Asia/Shanghai |
| Base `main` SHA before M4 readiness | `49dc210f3ebd3b98ebd8e38c3cf64fb664a7e202` |
| Final tag target | `0aa5c1b6e1959ef6504e6d70e4aad79a60594926` |
| Publication status | Published maintenance release |
| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.3 |
| Published at | 2026-05-01T09:06:46Z |
| Previous stable release | `v0.1.2` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.2 |
| `v0.1.2` tag target | `8bc8e9adf01e72031e5fb776007d4152a065ccb2` |
| M3 PR | https://github.com/YSCJRH/WinChronicle/pull/56 |
| M3 PR Windows Harness | Passed, run `25106125079`, https://github.com/YSCJRH/WinChronicle/actions/runs/25106125079 |
| M3 post-merge `main` Windows Harness | Passed, run `25106280110`, https://github.com/YSCJRH/WinChronicle/actions/runs/25106280110 |
| M4 PR | https://github.com/YSCJRH/WinChronicle/pull/57 |
| M4 PR Windows Harness | Passed, run `25193474129`, https://github.com/YSCJRH/WinChronicle/actions/runs/25193474129 |
| M4 final PR Windows Harness after evidence update | Passed, run `25193581576`, https://github.com/YSCJRH/WinChronicle/actions/runs/25193581576 |
| M4 post-merge `main` Windows Harness | Passed, run `25193726729`, https://github.com/YSCJRH/WinChronicle/actions/runs/25193726729 |

Environment:

- Windows PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual UIA smoke is not refreshed for this release-readiness branch because
  M4 changes version metadata, release evidence, and tests only. It does not
  change helper behavior, watcher behavior, smoke scripts, capture behavior, or
  smoke documentation. If release approval requires fresh manual smoke, use
  [Manual smoke evidence template](manual-smoke-evidence-template.md) and keep
  artifacts local.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `97 passed in 15.42s` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The M4 final PR Windows Harness and post-merge `main` Windows Harness passed
before publication.

## Release Notes

- Aligns package, runtime, and MCP server version identity to `0.1.3`.
- Records `v0.1.3` release evidence from the post-v0.1.2 maintenance
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
  must report `0.1.3`.
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

This maintenance release does not expand the capture surface from `v0.1.2`.

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

- If publication is withdrawn, keep `v0.1.2` as the latest stable release.
- Do not retag or modify `v0.1.2`.
- If a regression is found before publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, publish a follow-up release candidate or
  maintenance release instead of retagging `v0.1.3`.
- If a regression is limited to release documentation, tests, or version
  metadata, fix it on a small PR and rerun Windows Harness before
  reconsidering release approval.

## Release Decision Summary

- Release path: compatible `v0.1.3` maintenance release was published after
  explicit approval.
- Fallback path: release candidate if any product or contract change is
  required.
- Deterministic gates: local M4 validation, PR Windows Harness, and post-merge
  `main` Windows Harness passed.
- Manual UIA gates: not rerun for this version/evidence-only maintenance step;
  use the manual smoke evidence template if fresh manual evidence is required
  before publication.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: granted by the user message `approve publication`.
- Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.3.
- Final tag target: `0aa5c1b6e1959ef6504e6d70e4aad79a60594926`.
