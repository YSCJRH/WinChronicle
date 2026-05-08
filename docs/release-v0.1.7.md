# v0.1.7 Maintenance Release Record

This record captures the published compatible `v0.1.7` maintenance release
from the published `v0.1.6` baseline. It records commands, results, commit
identifiers, CI URLs, environment notes, and local artifact paths only. It does
not commit observed-content artifacts.

## Release Decision

`v0.1.7` is published. The T4 release-readiness PR, PR Windows Harness,
post-merge `main` Windows Harness, and GitHub release publication passed.

The direct compatible release path is allowed because T0-T4 change release
evidence, documentation, tests, CI/runtime metadata, compatibility evidence,
and version metadata only. No product behavior, schema, CLI/MCP JSON shape,
privacy behavior, helper/watcher behavior, or capture-surface change is
included.

If any product behavior, schema, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture-surface regression is found after
publication, prepare a follow-up release candidate instead of retagging
`v0.1.7`.

Publication status: published maintenance release.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.7` |
| Stage | Published maintenance release |
| Evidence date | 2026-05-08, Asia/Shanghai |
| Base `main` SHA before T4 readiness | `6d1d8f94c56636c23daafcb4ceae24053ff226aa` |
| Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/85 |
| Candidate PR Windows Harness | Passed, run `25556058760`, https://github.com/YSCJRH/WinChronicle/actions/runs/25556058760 |
| Candidate post-merge `main` Windows Harness | Passed, run `25556207363`, https://github.com/YSCJRH/WinChronicle/actions/runs/25556207363 |
| Publication status | Published maintenance release |
| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.7 |
| Final tag target | `0b5969509754f78b218f823d0e6bb7a0ea61392b` |
| Previous stable release | `v0.1.6` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.6 |
| `v0.1.6` tag target | `914cf361ac5864fa31d393d125d14e45eeba96bc` |
| v0.1.6 publication reconciliation PR | https://github.com/YSCJRH/WinChronicle/pull/80 |
| v0.1.6 publication reconciliation Windows Harness | Passed, run `25552120656`, https://github.com/YSCJRH/WinChronicle/actions/runs/25552120656 |
| v0.1.6 publication reconciliation post-merge Windows Harness | Passed, run `25552214063`, https://github.com/YSCJRH/WinChronicle/actions/runs/25552214063 |
| T0 PR | https://github.com/YSCJRH/WinChronicle/pull/81 |
| T0 PR Windows Harness | Passed, run `25553025094`, https://github.com/YSCJRH/WinChronicle/actions/runs/25553025094 |
| T0 post-merge `main` Windows Harness | Passed, run `25553238476`, https://github.com/YSCJRH/WinChronicle/actions/runs/25553238476 |
| T1 PR | https://github.com/YSCJRH/WinChronicle/pull/82 |
| T1 PR Windows Harness | Passed, run `25553940230`, https://github.com/YSCJRH/WinChronicle/actions/runs/25553940230 |
| T1 post-merge `main` Windows Harness | Passed, run `25554033860`, https://github.com/YSCJRH/WinChronicle/actions/runs/25554033860 |
| T2 PR | https://github.com/YSCJRH/WinChronicle/pull/83 |
| T2 PR Windows Harness | Passed, run `25554431580`, https://github.com/YSCJRH/WinChronicle/actions/runs/25554431580 |
| T2 post-merge `main` Windows Harness | Passed, run `25554520036`, https://github.com/YSCJRH/WinChronicle/actions/runs/25554520036 |
| T3 PR | https://github.com/YSCJRH/WinChronicle/pull/84 |
| T3 PR Windows Harness | Passed, run `25555063537`, https://github.com/YSCJRH/WinChronicle/actions/runs/25555063537 |
| T3 post-merge `main` Windows Harness | Passed, run `25555180274`, https://github.com/YSCJRH/WinChronicle/actions/runs/25555180274 |

Environment:

- Windows PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual UIA smoke is not refreshed for this maintenance release candidate
  because T0-T4 changes are documentation, tests, CI/runtime metadata,
  deterministic harness evidence, compatibility evidence, and version metadata
  only. This T4 record explicitly accepts inherited `v0.1.0` Notepad, Edge, VS
  Code metadata, VS Code strict diagnostic, and watcher preview manual evidence
  for the compatible `v0.1.7` path only because helper behavior, watcher
  product behavior, manual smoke scripts, capture behavior, privacy behavior,
  product CLI/MCP shape, and capture surfaces are unchanged. If release
  approval requires fresh manual smoke, use
  [Manual smoke evidence template](manual-smoke-evidence-template.md) and keep
  artifacts local.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `108 passed in 13.35s` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The T4 PR Windows Harness and post-merge `main` Windows Harness passed before
publication.

## Release Notes

- Aligns package, runtime, and MCP server version identity to `0.1.7`.
- Records the `v0.1.7` maintenance release-readiness evidence from the
  post-v0.1.6 maintenance round.
- Keeps the v0.1 product boundary unchanged: no new capture surfaces, no new
  MCP tools, no helper/watcher product behavior changes, and no Phase 6
  implementation.
- Records T0-T3 post-v0.1.6 maintenance evidence and accepts inherited manual
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
  must report `0.1.7`.
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

This maintenance release does not expand the capture surface from `v0.1.6`.

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

- Keep `v0.1.6` as the previous stable release.
- Do not retag or modify `v0.1.6`.
- If a regression is found after publication and requires product code, schema,
  CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, publish a follow-up release candidate instead of
  retagging `v0.1.7`.
- If a regression is limited to release documentation, tests, CI/runtime
  metadata, or version metadata, fix it on a small PR and rerun Windows Harness
  before publishing.

## Release Decision Summary

- Release path: compatible `v0.1.7` maintenance release, published.
- Fallback path: follow-up release candidate if any product or contract change
  is required after publication.
- Deterministic gates: local T4 validation, PR Windows Harness, post-merge
  `main` Windows Harness, and GitHub release publication passed.
- Manual UIA gates: inherited `v0.1.0` Notepad, Edge, VS Code metadata, VS
  Code strict diagnostic, and watcher preview manual evidence is explicitly
  accepted by this T4 record for the compatible `v0.1.7` path only because
  product UIA helper behavior, watcher product behavior, manual UIA smoke
  scripts, capture behavior, privacy behavior, product CLI/MCP shape, and
  capture surfaces are unchanged.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: completed by the active thread goal directing stage
  completion, remote push, and publication.
- Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.7.
- Final tag target: `0b5969509754f78b218f823d0e6bb7a0ea61392b`.
