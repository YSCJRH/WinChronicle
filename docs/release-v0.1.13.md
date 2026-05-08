# v0.1.13 Maintenance Release Record

This record captures the published compatible `v0.1.13` maintenance release
from the published `v0.1.12` baseline. It records commands, results, commit
identifiers, CI URLs, environment notes, and local artifact paths only. It does
not commit observed-content artifacts.

## Release Decision

`v0.1.13` is published. Local AA5 validation, PR Windows Harness, post-merge
`main` Windows Harness, and GitHub release publication passed.

The direct compatible release path is allowed because AA0-AA4 changed
documentation, tests, GitHub metadata, deterministic harness evidence,
compatibility evidence, and release-planning records only. AA5 changes release
documentation, tests, and version metadata only. No product behavior, schema,
CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
capture-surface change is included.

If any product behavior, schema, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture-surface regression is found before
publication, prepare a release candidate instead of publishing `v0.1.13`
directly. If such a regression is found after publication, publish a follow-up
release candidate instead of retagging `v0.1.13`.

Publication status: published maintenance release.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.13` |
| Stage | Published maintenance release |
| Evidence date | 2026-05-09, Asia/Shanghai |
| Base `main` SHA before AA5 readiness | `1c9cabec4d27b8c0e4e245d9a27ddcba96ed3a00` |
| Candidate PR | https://github.com/YSCJRH/WinChronicle/pull/118 |
| Candidate PR Windows Harness | Passed, run `25580778260`, https://github.com/YSCJRH/WinChronicle/actions/runs/25580778260 |
| Candidate post-merge `main` Windows Harness | Passed, run `25580877004`, https://github.com/YSCJRH/WinChronicle/actions/runs/25580877004 |
| Publication status | Published maintenance release |
| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.13 |
| Final tag target | `1070343d9bcfd60c48238835e26b6c32f9060ae7` |
| Previous stable release | `v0.1.12` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.12 |
| `v0.1.12` tag target | `df16ea301243e2d3a612a5d09bd59f1436723fb4` |
| AA0 PR | https://github.com/YSCJRH/WinChronicle/pull/113 |
| AA0 PR Windows Harness | Passed, run `25578139342`, https://github.com/YSCJRH/WinChronicle/actions/runs/25578139342 |
| AA0 post-merge `main` Windows Harness | Passed, run `25578252392`, https://github.com/YSCJRH/WinChronicle/actions/runs/25578252392 |
| AA1 PR | https://github.com/YSCJRH/WinChronicle/pull/114 |
| AA1 PR Windows Harness | Passed, run `25578768178`, https://github.com/YSCJRH/WinChronicle/actions/runs/25578768178 |
| AA1 post-merge `main` Windows Harness | Passed, run `25578855299`, https://github.com/YSCJRH/WinChronicle/actions/runs/25578855299 |
| AA2 PR | https://github.com/YSCJRH/WinChronicle/pull/115 |
| AA2 PR Windows Harness | Passed, run `25579283981`, https://github.com/YSCJRH/WinChronicle/actions/runs/25579283981 |
| AA2 post-merge `main` Windows Harness | Passed, run `25579389224`, https://github.com/YSCJRH/WinChronicle/actions/runs/25579389224 |
| AA3 PR | https://github.com/YSCJRH/WinChronicle/pull/116 |
| AA3 PR Windows Harness | Passed, run `25579782185`, https://github.com/YSCJRH/WinChronicle/actions/runs/25579782185 |
| AA3 post-merge `main` Windows Harness | Passed, run `25579869673`, https://github.com/YSCJRH/WinChronicle/actions/runs/25579869673 |
| AA4 PR | https://github.com/YSCJRH/WinChronicle/pull/117 |
| AA4 PR Windows Harness | Passed, run `25580215098`, https://github.com/YSCJRH/WinChronicle/actions/runs/25580215098 |
| AA4 post-merge `main` Windows Harness | Passed, run `25580333158`, https://github.com/YSCJRH/WinChronicle/actions/runs/25580333158 |

Environment:

- Windows PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual UIA smoke was not refreshed for this maintenance release-readiness
  candidate because AA0-AA5 do not change helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior, product
  CLI/MCP shape, release approver requirements, or capture surfaces. This AA5
  record explicitly accepts inherited `v0.1.0` Notepad, Edge, VS Code metadata, VS Code
  strict diagnostic, and watcher preview manual evidence for the compatible
  `v0.1.13` path only. If release approval requires fresh manual smoke, use
  [Manual smoke evidence template](manual-smoke-evidence-template.md) and keep
  artifacts local.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `125 passed` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The AA5 PR Windows Harness and post-merge `main` Windows Harness passed before
publication.

## Release Notes

- Aligns package, runtime, and MCP server version identity to `0.1.13`.
- Adds the post-v0.1.12 maintenance cursor, blueprint gap audit, deterministic
  demo, roadmap/contribution hygiene, issue templates, and compatibility
  guardrail sweep.
- Keeps the v0.1 product boundary unchanged: no new capture surfaces, no new
  MCP tools, no helper/watcher product behavior changes, and no Phase 6
  implementation.
- Records AA0-AA4 post-v0.1.12 maintenance evidence and accepts inherited
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
  must report `0.1.13`.
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

This maintenance release does not expand the capture surface from `v0.1.12`.

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

- Keep `v0.1.12` as the previous stable release.
- Do not retag or modify `v0.1.12`.
- If a regression is found before publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, prepare a release candidate instead of publishing
  `v0.1.13`.
- If a regression is found after publication and requires product code, schema,
  CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, publish a follow-up release candidate instead of
  retagging `v0.1.13`.
- If a regression is limited to release documentation, tests, GitHub metadata,
  CI/runtime metadata, or version metadata, fix it on a small PR and rerun
  Windows Harness before publishing.

## Release Decision Summary

- Release path: compatible `v0.1.13` maintenance release, published.
- Fallback path: release candidate if any product or contract change is
  required before publication.
- Deterministic gates: AA5 local validation, PR Windows Harness, post-merge
  `main` Windows Harness, and GitHub release publication passed.
- Manual UIA gates: inherited `v0.1.0` Notepad, Edge, VS Code metadata, VS Code
  strict diagnostic, and watcher preview manual evidence is accepted by this
  AA5 record for the compatible `v0.1.13` path only because product UIA helper
  behavior, watcher product behavior, manual UIA smoke scripts, capture
  behavior, privacy behavior, product CLI/MCP shape, and capture surfaces are
  unchanged.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: completed by the active thread goal directing stage
  completion, remote push, and publication after required gates pass.
- Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.13.
- Final tag target: `1070343d9bcfd60c48238835e26b6c32f9060ae7`.
