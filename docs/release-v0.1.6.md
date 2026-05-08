# v0.1.6 Maintenance Release Readiness Record

This record prepares the compatible `v0.1.6` maintenance release from the
published `v0.1.5` baseline. It records commands, results, commit identifiers,
CI URLs, environment notes, and local artifact paths only. It does not commit
observed-content artifacts.

## Release Decision

`v0.1.6` is a release-readiness candidate. Publication remains pending until
the S4 PR Windows Harness, post-merge `main` Windows Harness, and publication
step complete.

The direct compatible release path is allowed because S0-S4 change release
evidence, documentation, tests, CI/runtime metadata, and version metadata only.
No product behavior, schema, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture-surface change is included.

If any product behavior, schema, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture-surface change is required before
publication, stop the direct `v0.1.6` path and prepare a release candidate
instead.

Publication status: release-readiness candidate; publication pending.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.6` |
| Stage | Release-readiness candidate |
| Evidence date | 2026-05-08, Asia/Shanghai |
| Base `main` SHA before S4 readiness | `4a8222f24423c565b64c065da3b151ee5e246b99` |
| Candidate PR | Pending S4 PR |
| Candidate PR Windows Harness | Pending S4 PR |
| Candidate post-merge `main` Windows Harness | Pending S4 merge |
| Publication status | Pending |
| Release URL | Pending |
| Final tag target | Pending |
| Previous stable release | `v0.1.5` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.5 |
| `v0.1.5` tag target | `89f0c1d5e6c094ed36c0ecf75e18bb7afcd5aaf4` |
| Post-publication reconciliation `main` SHA for `v0.1.5` | `df15810c0b5022bebd1fe8a488f677e74fe8eae1` |
| Post-publication reconciliation Windows Harness for `v0.1.5` | Passed, run `25546003233`, https://github.com/YSCJRH/WinChronicle/actions/runs/25546003233 |
| S0 PR | https://github.com/YSCJRH/WinChronicle/pull/75 |
| S0 PR Windows Harness | Passed, run `25546758389`, https://github.com/YSCJRH/WinChronicle/actions/runs/25546758389 |
| S0 post-merge `main` Windows Harness | Passed, run `25546857375`, https://github.com/YSCJRH/WinChronicle/actions/runs/25546857375 |
| S1 PR | https://github.com/YSCJRH/WinChronicle/pull/76 |
| S1 PR Windows Harness | Passed, run `25547398940`, https://github.com/YSCJRH/WinChronicle/actions/runs/25547398940 |
| S1 post-merge `main` Windows Harness | Passed, run `25547572839`, https://github.com/YSCJRH/WinChronicle/actions/runs/25547572839 |
| S2 PR | https://github.com/YSCJRH/WinChronicle/pull/77 |
| S2 PR Windows Harness | Passed, run `25548402922`, https://github.com/YSCJRH/WinChronicle/actions/runs/25548402922 |
| S2 post-merge `main` Windows Harness | Passed, run `25548518832`, https://github.com/YSCJRH/WinChronicle/actions/runs/25548518832 |
| S3 PR | https://github.com/YSCJRH/WinChronicle/pull/78 |
| S3 PR Windows Harness | Passed, run `25549622445`, https://github.com/YSCJRH/WinChronicle/actions/runs/25549622445 |
| S3 post-merge `main` Windows Harness | Passed, run `25549851891`, https://github.com/YSCJRH/WinChronicle/actions/runs/25549851891 |

Environment:

- Windows PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual UIA smoke is not refreshed for this release-readiness branch because
  S0-S4 changes are documentation, tests, CI/runtime metadata, deterministic
  harness evidence, compatibility evidence, and version metadata only. This S4
  record explicitly accepts inherited `v0.1.0` Notepad, Edge, VS Code metadata,
  VS Code strict diagnostic, and watcher preview manual evidence for the
  compatible `v0.1.6` path only because helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior, product
  CLI/MCP shape, and capture surfaces are unchanged. If release approval
  requires fresh manual smoke, use
  [Manual smoke evidence template](manual-smoke-evidence-template.md) and keep
  artifacts local.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `106 passed in 23.25s` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The S4 PR Windows Harness and post-merge `main` Windows Harness are required
before publication.

## Release Notes

- Aligns package, runtime, and MCP server version identity to `0.1.6`.
- Records the `v0.1.6` maintenance release readiness evidence from the
  post-v0.1.5 maintenance round.
- Keeps the v0.1 product boundary unchanged: no new capture surfaces, no new
  MCP tools, no helper/watcher product behavior changes, and no Phase 6
  implementation.
- Adds compatibility guardrails for Phase 6 source-surface absence and refreshes
  manual-smoke freshness wording for the post-v0.1.5 path.

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
  must report `0.1.6`.
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

This maintenance release does not expand the capture surface from `v0.1.5`.

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

- Keep `v0.1.5` as the previous stable release.
- Do not retag or modify `v0.1.5`.
- If a regression is found before or after publication and requires product
  code, schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior,
  or capture-surface changes, publish a follow-up release candidate instead of
  retagging `v0.1.6`.
- If a regression is limited to release documentation, tests, CI/runtime
  metadata, or version metadata, fix it on a small PR and rerun Windows Harness
  before publishing.

## Release Decision Summary

- Release path: compatible `v0.1.6` maintenance release-readiness candidate.
- Fallback path: release candidate if any product or contract change is
  required before publication.
- Deterministic gates: local S4 validation passed; S4 PR Windows Harness and
  post-merge `main` Windows Harness remain pending.
- Manual UIA gates: inherited `v0.1.0` Notepad, Edge, VS Code metadata, VS
  Code strict diagnostic, and watcher preview manual evidence is explicitly
  accepted by this S4 record for the compatible `v0.1.6` path only because
  product UIA helper behavior, watcher product behavior, manual UIA smoke
  scripts, capture behavior, privacy behavior, product CLI/MCP shape, and
  capture surfaces are unchanged.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: pending until S4 PR and post-merge Windows Harness
  pass.
- Release URL: pending.
- Final tag target: pending.
