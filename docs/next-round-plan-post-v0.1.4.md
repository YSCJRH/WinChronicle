# WinChronicle Post-v0.1.4 Maintenance Plan

## Summary

`v0.1.4` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.4. The release tag
targets `31164abe0a391a4cf4e2bf5741395fe7a8ae8750`. The post-publication
reconciliation `main` commit is
`eea9ed944f0b47f9c94e5ab5f41f3e45b48a4654`, and the post-reconciliation
Windows Harness run `25432718007` passed on that SHA.

The next round should be a small compatible maintenance pass toward `v0.1.5`.
It should keep release evidence current, preserve operator entry points, decide
manual smoke freshness before any release, and maintain compatibility
guardrails. It must not expand the capture surface or start Phase 6
implementation.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, and no default background capture.

## Execution Cursor

- Current stage: P1 - Release Evidence And Entry Hygiene.
- Stage status: C - P1 complete; ready to enter P2 on the next turn.
- Last completed evidence: `v0.1.4` is published at
  https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.4 and targets
  `31164abe0a391a4cf4e2bf5741395fe7a8ae8750`. The post-publication
  reconciliation commit is `eea9ed944f0b47f9c94e5ab5f41f3e45b48a4654`, and
  Windows Harness run `25432718007` passed on that SHA. P0 added this
  post-v0.1.4 plan and updated README, operator quickstart, release checklist,
  release evidence guide, manual smoke ledger, and docs tests so this plan is
  the active cursor and post-v0.1.3 is historical. The post-merge Windows
  Harness run `25466653439` exposed a deterministic watcher-smoke harness
  assertion issue after a capture was written before any heartbeat was emitted.
  P1 audited operator-facing entry points and scorecards, found no stale older
  plan presented as current, and strengthened README current/history ordering
  coverage.
- Last validation: P0 full local validation passed: `python -m pytest -q`,
  both .NET builds, `python harness/scripts/run_install_cli_smoke.py`,
  `python harness/scripts/run_harness.py`, and `git diff --check`. The
  watcher-smoke stability fix also passed local `tests/test_watcher_events.py`,
  full pytest, both .NET builds, install CLI smoke, full harness, and
  `git diff --check`. P1 targeted docs validation passed after the README
  entry-ordering test update, followed by full pytest, both .NET builds,
  install CLI smoke, full harness, and `git diff --check`.
- Next atomic task: start P2 by deciding whether the next compatible release
  can explicitly inherit older manual UIA smoke evidence or must refresh manual
  Notepad, Edge, VS Code metadata, and diagnostic smoke.
- Known blockers: none.

## Phased Work

### Stage P0 - Post-v0.1.4 Baseline Cursor

- Add this post-v0.1.4 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Keep the post-v0.1.3 plan closed and historical.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, or privacy behavior.

### Stage P1 - Release Evidence And Entry Hygiene

- Audit docs and scorecards that still describe older release plans as current
  and refresh only operator-facing entry points.
- Add or strengthen narrow docs tests only for discovered drift around active
  cursor links, latest release identity, and evidence freshness wording.
- Keep `v0.1.4` as the stable release baseline until release-readiness work
  explicitly prepares `v0.1.5`.
- Do not bump package/server version in P1.

### Stage P2 - Manual Smoke Freshness Decision

- Decide whether the next release can inherit older manual UIA smoke evidence
  or requires a fresh manual run.
- If fresh manual smoke is required, record only command, result, timestamp,
  environment notes, and local artifact paths with the existing template.
- Keep real UIA smoke outside default CI and keep all artifacts local.
- Do not commit observed text, screenshots, OCR output, raw helper JSON, raw
  watcher JSONL, local HTML page contents, editor buffer contents, passwords,
  secrets, or token canaries.

### Stage P3 - Compatibility Guardrail Maintenance

- Re-run deterministic gates and confirm the v0.1 boundary still holds.
- Strengthen tests only for discovered drift around version identity,
  read-only MCP tool list, privacy surface parity, memory/search trust
  boundaries, release evidence freshness, and Phase 6 spec-only status.
- Do not add helper/watcher product capabilities, MCP write tools, arbitrary
  file reads, screenshots, OCR, audio, keyboard capture, clipboard capture,
  network upload, desktop control, daemon/service install, polling capture
  loop, or default background capture.

### Stage P4 - v0.1.5 Release Readiness

- If P0-P3 only change documentation, tests, version metadata, or compatible
  drift fixes, prepare a compatible `v0.1.5` maintenance release.
- Before release, align package and server version metadata to `0.1.5`, add a
  release record, and record local gates plus PR and post-merge Windows Harness
  evidence.
- If any change alters product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture surface, stop the direct
  `v0.1.5` path and prepare a release candidate instead.
- Publication remains blocked on explicit user approval.

## Test Plan

Every implementation stage should run:

- `python -m pytest -q`
- `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo`
- `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo`
- `python harness/scripts/run_install_cli_smoke.py`
- `python harness/scripts/run_harness.py`
- `git diff --check`
- GitHub Actions `Windows Harness` on PR and after merge to `main`

Stage-specific gates:

- P0: grep or doc inspection confirms the active cursor points to this
  post-v0.1.4 plan and historical plans remain historical.
- P1: README, operator quickstart, release checklist, and release evidence
  guide do not describe older post-v0.1.x plans as the current cursor.
- P2: manual smoke freshness policy records only commands, results,
  timestamps, environment notes, and local artifact paths; observed-content
  artifacts remain uncommitted.
- P3: MCP tools remain exactly read-only, privacy surfaces remain disabled,
  memory/search trust boundaries remain stable, and Phase 6 remains spec-only.
- P4: release checklist, release evidence, rollback notes, and Windows Harness
  pass before publication; manual UIA smoke refresh is required only if
  helper/smoke behavior, smoke docs, or the evidence ledger requires it.

## Public Interfaces And Non-goals

- CLI remains:
  `init/status/capture-once/capture-frontmost/watch/privacy-check/search-captures/generate-memory/search-memory/mcp-stdio`.
- Product CLI still does not expose targeted `--hwnd`, `--pid`, or
  `--window-title` capture.
- MCP remains read-only with:
  `current_context/search_captures/search_memory/read_recent_capture/recent_activity/privacy_status`.
- Version metadata may be updated only during release-readiness work, but MCP
  wire shape, tool schema, CLI JSON fields, and capture schema must not change
  in this maintenance pass.
- No screenshot capture, OCR, audio recording, keyboard capture, clipboard
  capture, network upload, LLM calls, MCP write tools, arbitrary file reads,
  service/daemon install, polling capture loop, default background capture, or
  desktop control.

## Assumptions

- `v0.1.4` is the current stable release baseline and must not be modified or
  retagged.
- The next compatible release target is `v0.1.5`.
- Phase 6 remains privacy spec/scorecard work only until a future tests-first
  round.
- Manual UIA smoke remains outside default CI because it depends on an
  interactive Windows desktop.

## Decision Log

- Chose a compatible `v0.1.5` maintenance target because `v0.1.4` changed
  version metadata and release evidence only, without product behavior changes.
- Chose P0 as a docs-only active cursor so post-v0.1.4 work does not begin
  from a closed historical plan.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.
- During P0, updated only documentation and docs tests. No product code,
  schemas, CLI/MCP JSON shape, helper/watcher behavior, capture surfaces, or
  privacy behavior changed.
- After P0 merged, treated Windows Harness run `25466653439` as a harness-only
  watcher-smoke stability failure: the fake-helper `--capture-on-start` path
  wrote a valid capture before the short smoke emitted a heartbeat. The hard
  deterministic smoke signal is now the persisted/searchable capture; heartbeat
  remains a watcher liveness diagnostic covered by separate tests and docs. This
  does not change product watcher/helper behavior, CLI/MCP shape, capture
  schema, privacy behavior, or capture surface.
- During P1, treated older post-v0.1.x plans and release records as acceptable
  only in historical sections. Strengthened README tests rather than changing
  product docs because the audit found the current operator entry points already
  identify post-v0.1.4 and `v0.1.4` as current.

## Validation Log

- `gh release view v0.1.4 --json name,tagName,url,isDraft,isPrerelease,publishedAt,targetCommitish`
  confirmed the release is published, not a draft, not a prerelease, targets
  `31164abe0a391a4cf4e2bf5741395fe7a8ae8750`, and is available at
  https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.4.
- `gh run list --workflow "Windows Harness" --branch main --limit 5 --json databaseId,status,conclusion,headSha,url,createdAt,displayTitle`
  confirmed post-publication `main` Windows Harness run `25432718007` passed
  on `eea9ed944f0b47f9c94e5ab5f41f3e45b48a4654`.
- Stage P0 local validation:
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q` - 12 passed.
  - `python -m pytest -q` - 99 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage P1 entry-hygiene validation:
  - `rg -n "active cursor|current cursor|current plan|next-round-plan-post-v0\\.1\\.[0-3]|post-v0\\.1\\.[0-3].*(active|current)|v0\\.1\\.[0-3].*(current|latest|stable|baseline)|latest published|stable release baseline|release baseline|current stable|current release|Before v0\\.1\\.[0-4]|Pending release-readiness record|manual smoke.*fresh|fresh manual|freshness" README.md docs harness tests` - reviewed expected historical records and current post-v0.1.4 references.
  - `rg -n "next-round-plan-post-v0\\.1\\.[0-3].*(active|current)|active post-v0\\.1\\.[0-3]|current post-v0\\.1\\.[0-3]|latest published `v0\\.1\\.[0-3]`|stable baseline is `v0\\.1\\.[0-3]`|Stable release baseline \\| `v0\\.1\\.[0-3]`" README.md docs tests` - no matches.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q` - passed after adding README current/history ordering coverage.
  - `python -m pytest -q` - 101 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Post-merge watcher-smoke stability validation:
  - Windows Harness run `25466653439` failed on `main` because
    `run_watcher_smoke.py` required both `captures_written >= 1` and
    `heartbeats >= 1`; the run produced one `foreground_changed` capture and
    zero heartbeats in the short smoke budget.
  - `python -m pytest tests/test_watcher_events.py -q` - 16 passed after
    adding coverage for capture-without-heartbeat acceptance and
    heartbeat-only rejection in deterministic capture smoke.
  - `python harness/scripts/run_watcher_smoke.py` - passed.
  - `python -m pytest -q` - 101 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
