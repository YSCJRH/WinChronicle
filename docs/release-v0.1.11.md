# v0.1.11 Maintenance Release Record

This record captures the compatible `v0.1.11` maintenance release-readiness candidate
from the published `v0.1.10` baseline. It records commands, results, commit
identifiers, CI URLs, environment notes, and local artifact paths only. It does
not commit observed-content artifacts.

## Release Decision

`v0.1.11` is a release-readiness candidate. Local Y4 validation has passed; PR Windows Harness, post-merge
`main` Windows Harness, and GitHub release publication are pending.

The direct compatible release path is allowed because Y0-Y4 change release
evidence, documentation, tests, CI/runtime metadata, compatibility evidence,
and version metadata only. No product behavior, schema, CLI/MCP JSON shape,
privacy behavior, helper/watcher behavior, or capture-surface change is
included.

If any product behavior, schema, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture-surface regression is found after
publication, prepare a follow-up release candidate instead of retagging
`v0.1.11`.

Publication status: release-readiness candidate; publication pending.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.11` |
| Stage | Release-readiness candidate |
| Evidence date | 2026-05-09, Asia/Shanghai |
| Base `main` SHA before Y4 readiness | `b7a6651d829c914fe9d8eeea0896238d0d880249` |
| Candidate PR | Pending Y4 PR |
| Candidate PR Windows Harness | Pending Y4 PR Windows Harness |
| Candidate post-merge `main` Windows Harness | Pending Y4 post-merge Windows Harness |
| Publication status | Pending release publication |
| Release URL | Pending publication |
| Final tag target | Pending publication |
| Previous stable release | `v0.1.10` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.10 |
| `v0.1.10` tag target | `28b062a531519d4360911b51dfc083782b6dcbad` |
| Y0 PR | https://github.com/YSCJRH/WinChronicle/pull/102 |
| Y0 PR Windows Harness | Passed, run `25570444498`, https://github.com/YSCJRH/WinChronicle/actions/runs/25570444498 |
| Y0 post-merge `main` Windows Harness | Passed, run `25570603780`, https://github.com/YSCJRH/WinChronicle/actions/runs/25570603780 |
| Y1 PR | https://github.com/YSCJRH/WinChronicle/pull/103 |
| Y1 PR Windows Harness | Passed, run `25571224423`, https://github.com/YSCJRH/WinChronicle/actions/runs/25571224423 |
| Y1 post-merge `main` Windows Harness | Passed, run `25571374301`, https://github.com/YSCJRH/WinChronicle/actions/runs/25571374301 |
| Y2 PR | https://github.com/YSCJRH/WinChronicle/pull/104 |
| Y2 PR Windows Harness | Passed, run `25571923026`, https://github.com/YSCJRH/WinChronicle/actions/runs/25571923026 |
| Y2 post-merge `main` Windows Harness | Passed, run `25572048167`, https://github.com/YSCJRH/WinChronicle/actions/runs/25572048167 |
| Y3 PR | https://github.com/YSCJRH/WinChronicle/pull/105 |
| Y3 PR Windows Harness | Passed, run `25572434735`, https://github.com/YSCJRH/WinChronicle/actions/runs/25572434735 |
| Y3 post-merge `main` Windows Harness | Passed, run `25572553734`, https://github.com/YSCJRH/WinChronicle/actions/runs/25572553734 |

Environment:

- Windows PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual UIA smoke is not refreshed for this maintenance release candidate
  because Y0-Y4 changes are documentation, tests, CI/runtime metadata,
  deterministic harness evidence, compatibility evidence, and version metadata
  only. This Y4 record explicitly accepts inherited `v0.1.0` Notepad, Edge, VS
  Code metadata, VS Code strict diagnostic, and watcher preview manual evidence
  for the compatible `v0.1.11` path only because helper behavior, watcher
  product behavior, manual smoke scripts, capture behavior, privacy behavior,
  product CLI/MCP shape, and capture surfaces are unchanged. If release
  approval requires fresh manual smoke, use
  [Manual smoke evidence template](manual-smoke-evidence-template.md) and keep
  artifacts local.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `117 passed in 13.75s` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The Y4 PR Windows Harness and post-merge `main` Windows Harness are pending before publication.

## Release Notes

- Aligns package, runtime, and MCP server version identity to `0.1.11`.
- Records the `v0.1.11` maintenance release-readiness evidence from the
  post-v0.1.10 maintenance round.
- Keeps the v0.1 product boundary unchanged: no new capture surfaces, no new
  MCP tools, no helper/watcher product behavior changes, and no Phase 6
  implementation.
- Records Y0-Y3 post-v0.1.10 maintenance evidence and accepts inherited manual
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
  must report `0.1.11`.
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

This maintenance release does not expand the capture surface from `v0.1.10`.

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

- Keep `v0.1.10` as the previous stable release.
- Do not retag or modify `v0.1.10`.
- If a regression is found before publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, prepare a release candidate instead of publishing
  `v0.1.11`.
- If a regression is found after publication and requires product code, schema,
  CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, publish a follow-up release candidate instead of
  retagging `v0.1.11`.
- If a regression is limited to release documentation, tests, CI/runtime
  metadata, or version metadata, fix it on a small PR and rerun Windows Harness
  before publishing.

## Release Decision Summary

- Release path: compatible `v0.1.11` maintenance release-readiness candidate; publication pending.
- Fallback path: release candidate if any product or contract change is
  required after publication.
- Deterministic gates: local Y4 validation is recorded above; PR Windows
  Harness, post-merge `main` Windows Harness, and GitHub release publication
  are pending.
- Manual UIA gates: inherited `v0.1.0` Notepad, Edge, VS Code metadata, VS Code
  strict diagnostic, and watcher preview manual evidence is explicitly accepted
  by this Y4 record for the compatible `v0.1.11` path only because product UIA
  helper behavior, watcher product behavior, manual UIA smoke scripts, capture
  behavior, privacy behavior, product CLI/MCP shape, and capture surfaces are
  unchanged.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: authorized by the active thread goal after required local,
  PR, and post-merge gates pass.
- Release URL: pending publication.
- Final tag target: pending publication.

