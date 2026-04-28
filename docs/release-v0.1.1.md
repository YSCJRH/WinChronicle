# v0.1.1 Maintenance Release Readiness Record

This record prepares a compatible `v0.1.1` maintenance release from the
published `v0.1.0` baseline. It records commands, results, commit identifiers,
CI URLs, environment notes, and local artifact paths only. It does not commit
observed-content artifacts.

## Release Decision

`v0.1.1` is prepared but not published. Publishing requires explicit release
approval after this release-preparation PR and its post-merge `main` Windows
Harness pass.

If any product behavior, schema, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture-surface change is required before
publication, do not publish `v0.1.1` directly. Prepare a release candidate
instead.

Publication status: not published.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.1.1` |
| Stage | Post-v0.1 maintenance release preparation |
| Evidence date | 2026-04-28, Asia/Shanghai |
| Current candidate `main` SHA before this record | `4a1ac5abc57b8e01b499eadd329ed880aa09cefa` |
| Planned tag target | TBD after release-preparation PR merge |
| Publication status | Not published |
| Previous stable release | `v0.1.0` |
| Previous stable release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.0 |
| `v0.1.0` tag target | `6d22462c0da185d163cf1b7219e05439ff4666ff` |
| Stage P1 PR | https://github.com/YSCJRH/WinChronicle/pull/31 |
| Stage P1 post-merge `main` Windows Harness | Passed, run `25036973210`, https://github.com/YSCJRH/WinChronicle/actions/runs/25036973210 |
| Stage P2 PR | https://github.com/YSCJRH/WinChronicle/pull/33 |
| Stage P2 post-merge `main` Windows Harness | Passed, run `25037802382`, https://github.com/YSCJRH/WinChronicle/actions/runs/25037802382 |
| Stage P3 PR | https://github.com/YSCJRH/WinChronicle/pull/35 |
| Stage P3 post-merge `main` Windows Harness | Passed, run `25038515262`, https://github.com/YSCJRH/WinChronicle/actions/runs/25038515262 |
| Stage P4 PR | https://github.com/YSCJRH/WinChronicle/pull/37 |
| Stage P4 post-merge `main` Windows Harness | Passed, run `25039294143`, https://github.com/YSCJRH/WinChronicle/actions/runs/25039294143 |
| Stage P5 PR | https://github.com/YSCJRH/WinChronicle/pull/39 |
| Stage P5 post-merge `main` Windows Harness | Passed, run `25040068331`, https://github.com/YSCJRH/WinChronicle/actions/runs/25040068331 |
| Completion cursor PR | https://github.com/YSCJRH/WinChronicle/pull/40 |
| Completion cursor post-merge `main` Windows Harness | Passed, run `25040334839`, https://github.com/YSCJRH/WinChronicle/actions/runs/25040334839 |

Environment:

- Windows PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.
- Manual UIA smoke was not rerun for this release-preparation record because
  the maintenance batch changed docs, tests, scorecards, and version metadata
  only. If release approval requires fresh manual smoke evidence, use
  [Manual smoke evidence template](manual-smoke-evidence-template.md) and keep
  artifacts local.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest -q` | Pass | `83 passed in 17.07s` |
| `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` | Pass | 0 warnings, 0 errors |
| `python harness/scripts/run_install_cli_smoke.py` | Pass | install, `--help`, `init`, `status`, fixture capture, capture search, memory generation, and memory search passed |
| `python harness/scripts/run_harness.py` | Pass | pytest, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search, memory, fixture watcher, and preview watcher smoke passed |
| `git diff --check` | Pass | no whitespace errors |

The release-preparation PR must also pass Windows Harness before publication.

## Release Notes

- Adds operator diagnostics documentation and tests for helper no-capture,
  watcher heartbeat-only, helper wrapper failures, and VS Code Monaco
  diagnostic limitations.
- Hardens watcher preview diagnostics and keeps the watcher explicit,
  time-bounded, and non-daemonized.
- Refreshes the UIA helper compatibility matrix with `v0.1.0` final smoke
  evidence and keeps new app coverage diagnostic by default.
- Freezes read-only MCP examples and memory SQLite/search contracts with
  additional regression tests.
- Expands the Phase 6 screenshot/OCR privacy scorecard as specification-only
  work, without implementing screenshots, OCR, caches, or new capture code.

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

## Privacy And Scope Confirmation

This maintenance release does not expand the capture surface from `v0.1.0`.

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

- If publication is withdrawn, keep `v0.1.0` as the latest stable release.
- Do not retag `v0.1.0`; publish a replacement candidate if a product or
  contract change is required.
- If a regression is found before publication and requires product code,
  schema, CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface changes, stop the direct `v0.1.1` path and prepare a release
  candidate.
- If a regression is limited to release documentation or version metadata, fix
  it on a small PR and rerun Windows Harness before reconsidering release
  approval.

## Release Decision Summary

- Release path: compatible `v0.1.1` maintenance release is prepared but not
  published.
- Fallback path: release candidate if any product or contract change is
  required.
- Deterministic gates: passed locally and in GitHub Actions for the P0-P5
  maintenance batch.
- Manual UIA gates: not rerun for this docs/tests/scorecards maintenance
  batch; use the manual smoke evidence template if fresh manual evidence is
  required before publication.
- Privacy/scope confirmation: unchanged and recorded above.
- Publication approval: pending explicit user approval.
