# WinChronicle Post-v0.1.2 Maintenance Plan

## Summary

`v0.1.2` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.2. The release tag
targets `8bc8e9adf01e72031e5fb776007d4152a065ccb2`. The release-approved
`main` Windows Harness run `25053851860` passed on that SHA, and the
post-publication reconciliation `main` Windows Harness run `25084360942`
passed on `62d935345746b42ed99fc612354f3f1190fea0f8`.

The next round should be a small compatible maintenance pass toward `v0.1.3`.
It should improve post-release evidence freshness, operator entry points,
manual smoke evidence discipline, and compatibility guardrails. It must not
expand the capture surface or start Phase 6 implementation.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, and no default background capture.

## Execution Cursor

- Current stage: M1 - Release Evidence Freshness Guard.
- Stage status: A - M0 post-v0.1.2 baseline cursor is being established; M1 is
  the next active implementation stage after this docs-only cursor lands.
- Last completed evidence: `v0.1.2` is published and reconciled; release URL,
  tag target, PR Windows Harness, post-merge Windows Harness, and
  post-publication Windows Harness are recorded in the `v0.1.2` release record
  and the closed post-v0.1.1 plan.
- Last validation: post-publication `main` Windows Harness run `25084360942`
  passed on `62d935345746b42ed99fc612354f3f1190fea0f8`.
- Next atomic task: start M1 by auditing release/checklist/evidence docs for
  stale current-cursor, baseline, and manual-smoke evidence language.
- Known blockers: none.

## Phased Work

### Stage M0 - Post-v0.1.2 Baseline Cursor

- Add this post-v0.1.2 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, and release evidence
  guide so operators can find this active cursor.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, or privacy behavior.

### Stage M1 - Release Evidence Freshness Guard

- Audit docs and scorecards that still describe older release plans as current
  and refresh only the operator-facing entry points.
- Add or strengthen narrow docs tests so the active cursor points here, while
  post-v0.1.1 and earlier plans remain historical.
- Confirm `v0.1.2` remains the stable release baseline until release-readiness
  work explicitly prepares `v0.1.3`.
- Do not bump package/server version in M1.

### Stage M2 - Manual Smoke Evidence Ledger

- Add or refresh a manual smoke evidence ledger that records the latest known
  Notepad, Edge, VS Code metadata, VS Code strict Monaco diagnostic, and watcher
  preview evidence status without committing observed-content artifacts.
- Make the ledger explicit about stale manual smoke evidence: document when
  evidence is inherited from an earlier release, when a refresh is required,
  and which gates remain diagnostic.
- Keep real UIA smoke outside default CI and keep all artifacts local.

### Stage M3 - Compatibility Contract Drift Sweep

- Re-run deterministic gates and confirm the v0.1 boundary still holds.
- Strengthen tests only for discovered drift around version identity,
  read-only MCP tool list, privacy surface parity, memory search shape, and
  Phase 6 spec-only status.
- Do not add helper/watcher product capabilities, MCP write tools, arbitrary
  file reads, screenshots, OCR, audio, keyboard capture, clipboard capture,
  network upload, desktop control, daemon/service install, polling capture loop,
  or default background capture.

### Stage M4 - v0.1.3 Release Readiness

- If M0-M3 only change documentation, tests, version metadata, or compatible
  drift fixes, prepare a compatible `v0.1.3` maintenance release.
- Before release, align package and server version metadata to `0.1.3`, add a
  release record, and record local gates plus PR and post-merge Windows Harness
  evidence.
- If any change alters product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture surface, stop the direct
  `v0.1.3` path and prepare a release candidate instead.

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

- M0: grep or doc inspection confirms the active cursor points to this
  post-v0.1.2 plan and historical plans remain historical.
- M1: README, operator quickstart, release checklist, and release evidence
  guide do not describe older post-v0.1.x plans as the current cursor.
- M2: manual smoke ledger records commands/results/timestamps/environment/local
  artifact paths only and does not require committing observed-content
  artifacts.
- M3: MCP tools remain exactly read-only, privacy surfaces remain disabled,
  memory/search trust boundaries remain stable, and Phase 6 remains spec-only.
- M4: release checklist, release evidence, rollback notes, and Windows Harness
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

- `v0.1.2` is the current stable release baseline and must not be modified or
  retagged.
- The next compatible release target is `v0.1.3`.
- Phase 6 remains privacy spec/scorecard work only until a future tests-first
  round.
- Manual UIA smoke remains outside default CI because it depends on an
  interactive Windows desktop.

## Decision Log

- Chose a compatible `v0.1.3` maintenance target because `v0.1.2` changed
  version metadata and release evidence only, without product behavior changes.
- Chose M0 as a docs-only active cursor so post-v0.1.2 work does not begin
  from a closed historical plan.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.

## Validation Log

- `gh release view v0.1.2` confirmed the release is published, not a draft, not
  a prerelease, and targets `8bc8e9adf01e72031e5fb776007d4152a065ccb2`.
- Post-publication reconciliation `main` Windows Harness run `25084360942`
  passed on `62d935345746b42ed99fc612354f3f1190fea0f8`.
- Stage M0 local validation:
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_uia_helper_quality_matrix.py tests/test_compatibility_evidence_docs.py -q` - 12 passed.
  - `python -m pytest -q` - 90 passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
