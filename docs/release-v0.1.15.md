# v0.1.15 Maintenance Release Record

This record captures the compatible `v0.1.15` maintenance release-readiness
candidate from the published `v0.1.14` baseline. It records commands, results,
commit identifiers, CI URLs, environment notes, and local artifact paths only.
It does not commit observed-content artifacts.

## Release Decision

`v0.1.15` is a release-readiness candidate. Local AC5 validation passed, PR
Windows Harness passed, and post-merge `main` Windows Harness passed. GitHub
release publication is pending explicit release approval.

The direct compatible release path is allowed because AC0-AC4 changed
documentation, tests, GitHub metadata evidence, deterministic harness evidence,
compatibility evidence, and release-planning records only. AC5 changes release
documentation, tests, and version metadata only. No product behavior, schema,
CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
capture-surface change is included.

If any product behavior, schema, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture-surface regression is found before
publication, prepare a release candidate instead of publishing `v0.1.15`
directly. If such a regression is found after publication, publish a follow-up
release candidate instead of retagging `v0.1.15`.

Publication status: release-readiness candidate; not yet published.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.15` |
| Stage | Release-readiness candidate |
| Evidence date | 2026-05-09, Asia/Shanghai |
| Base `main` SHA before AC5 readiness | `48994134a3d348745f735e2a6fad56ea82495266` |
| Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/132 |
| Candidate PR Windows Harness | Passed, run `25588833988`, https://github.com/YSCJRH/WinChronicle/actions/runs/25588833988 |
| Candidate post-merge `main` Windows Harness | Passed, run `25588898702`, https://github.com/YSCJRH/WinChronicle/actions/runs/25588898702 |
| Candidate post-merge `main` SHA | `7a7f065817b9d7f660248916935fd7b66fadbdd6` |
| Publication status | Release-readiness candidate; not yet published |
| Release URL | Pending |
| Final tag target | Pending |
| Previous stable release | `v0.1.14` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.14 |
| `v0.1.14` tag target | `e7e339f4e08828b9954599db76b87201dbcb139b` |
| AC0 PR | https://github.com/YSCJRH/WinChronicle/pull/127 |
| AC0 PR Windows Harness | Passed, run `25586296541`, https://github.com/YSCJRH/WinChronicle/actions/runs/25586296541 |
| AC0 post-merge `main` Windows Harness | Passed, run `25586359016`, https://github.com/YSCJRH/WinChronicle/actions/runs/25586359016 |
| AC1 PR | https://github.com/YSCJRH/WinChronicle/pull/128 |
| AC1 PR Windows Harness | Passed, run `25586734181`, https://github.com/YSCJRH/WinChronicle/actions/runs/25586734181 |
| AC1 post-merge `main` Windows Harness | Passed, run `25586802404`, https://github.com/YSCJRH/WinChronicle/actions/runs/25586802404 |
| AC2 PR | https://github.com/YSCJRH/WinChronicle/pull/129 |
| AC2 PR Windows Harness | Passed, run `25587197634`, https://github.com/YSCJRH/WinChronicle/actions/runs/25587197634 |
| AC2 post-merge `main` Windows Harness | Passed, run `25587281619`, https://github.com/YSCJRH/WinChronicle/actions/runs/25587281619 |
| AC3 PR | https://github.com/YSCJRH/WinChronicle/pull/130 |
| AC3 PR Windows Harness | Passed, run `25587827078`, https://github.com/YSCJRH/WinChronicle/actions/runs/25587827078 |
| AC3 post-merge `main` Windows Harness | Passed, run `25587885292`, https://github.com/YSCJRH/WinChronicle/actions/runs/25587885292 |
| AC4 PR | https://github.com/YSCJRH/WinChronicle/pull/131 |
| AC4 PR Windows Harness | Passed, run `25588225151`, https://github.com/YSCJRH/WinChronicle/actions/runs/25588225151 |
| AC4 post-merge `main` Windows Harness | Passed, run `25588297846`, https://github.com/YSCJRH/WinChronicle/actions/runs/25588297846 |

Environment:

- Windows PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual UIA smoke was not refreshed for this maintenance release-readiness
  candidate because AC0-AC5 do not change helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior, product
  CLI/MCP shape, release approver requirements, or capture surfaces. This AC5
  record explicitly accepts inherited `v0.1.0` Notepad, Edge, VS Code metadata,
  VS Code strict diagnostic, and watcher preview manual evidence for the
  compatible `v0.1.15` path only. If release approval requires fresh manual
  smoke, use [Manual smoke evidence template](manual-smoke-evidence-template.md)
  and keep artifacts local.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `137 passed` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The AC5 PR Windows Harness and post-merge `main` Windows Harness passed.
GitHub release publication is pending explicit release approval.

## Release Notes

- Aligns package, runtime, and MCP server version identity to `0.1.15`.
- Adds post-v0.1.14 public metadata, helper/watcher diagnostics, MCP/memory
  contract, and compatibility guardrail evidence.
- Keeps the v0.1 product boundary unchanged: no new capture surfaces, no new
  MCP tools, no helper/watcher product behavior changes, and no Phase 6
  implementation.
- Records AC0-AC4 post-v0.1.14 maintenance evidence and accepts inherited
  manual UIA smoke only for this compatible maintenance path.

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
  must report `0.1.15`.
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

This maintenance release does not expand the capture surface from `v0.1.14`.

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

- Keep `v0.1.14` as the previous stable release.
- Do not retag or modify `v0.1.14`.
- If a regression is found before publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, prepare a release candidate instead of publishing
  `v0.1.15`.
- If a regression is found after publication and requires product code, schema,
  CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, publish a follow-up release candidate instead of
  retagging `v0.1.15`.
- If a regression is limited to release documentation, tests, GitHub metadata,
  CI/runtime metadata, or version metadata, fix it on a small PR and rerun
  Windows Harness before publishing.

## Release Decision Summary

- Release path: compatible `v0.1.15` maintenance release-readiness candidate.
- Fallback path: release candidate if any product or contract change is
  required before publication.
- Deterministic gates: AC5 local validation passed; PR Windows Harness,
  post-merge `main` Windows Harness, and GitHub release publication are
  pending.
- Manual UIA gates: inherited `v0.1.0` Notepad, Edge, VS Code metadata, VS Code
  strict diagnostic, and watcher preview manual evidence is accepted by this
  AC5 record for the compatible `v0.1.15` path only because product UIA helper
  behavior, watcher product behavior, manual UIA smoke scripts, capture
  behavior, privacy behavior, product CLI/MCP shape, and capture surfaces are
  unchanged.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: pending explicit release approval.
- Release URL: pending.
- Final tag target: pending.
