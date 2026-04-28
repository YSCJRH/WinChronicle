# v0.1.0-rc.0 Readiness Plan

## Summary

`v0.1.0-beta.1` was published and green. This completed round prepared and
published the `v0.1.0-rc.0` candidate by tightening installation, operator
documentation, and release evidence, not by adding new capture surfaces.

This plan is now closed. The active post-rc.0 execution cursor lives in
[v0.1.0 Final Readiness Plan](next-round-plan-v0.1.0-final.md).

This plan keeps the product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, screenshots/OCR/audio/keyboard/clipboard
capture off or absent by default, no LLM reducer/classifier, no network upload,
and no desktop control.

## Execution Cursor

- Current stage: Closed - `v0.1.0-rc.0` published.
- Stage status: Completed - Stage RC4 release-candidate evidence was reviewed,
  merged, validated by PR and post-merge Windows Harness, and published as
  `v0.1.0-rc.0`.
- Last completed evidence: release
  `https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.0-rc.0`
  targets `069e8cff9434c83b00a7a857aaf9eee441cf16ff`; post-merge `main`
  Windows Harness run `25022034701` passed on that SHA. Historical beta
  baseline: release
  `https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.0-beta.1`
  targets `2caf922733693ff5c63e39375d1882b19dcd508f`; latest `main` Windows
  Harness run `24990257758` passed on
  `51140bf8dfcb2cfcf65776653c927b9598d3247e`; release checklist, manual smoke
  evidence template, watcher preview docs, MCP examples, Windows UIA smoke
  docs, and known limitations docs are present under `docs/`; RC1 adds
  `harness/scripts/run_install_cli_smoke.py` and includes it in the full
  deterministic harness; RC2 adds `docs/operator-quickstart.md` and links it
  from README and the release checklist; RC3 adds `docs/release-evidence.md`
  and aligns the manual smoke template with deterministic gates.
- Last validation: RC4 local gates passed on
  `codex/stage-rc4-rc-candidate`: pytest, helper build, watcher build, install
  CLI smoke, full deterministic harness, `git diff --check`, Notepad targeted
  smoke, Edge targeted smoke, VS Code metadata smoke, and a bounded depth 2
  watcher preview. VS Code strict Monaco marker failed as a documented
  diagnostic/non-blocking limitation, and a depth 80 watcher preview attempt
  timed out as diagnostic evidence. PR Windows Harness run `25021868203`
  passed, and post-merge `main` Windows Harness run `25022034701` passed on
  `069e8cff9434c83b00a7a857aaf9eee441cf16ff`.
- Next atomic task: continue from
  [v0.1.0 Final Readiness Plan](next-round-plan-v0.1.0-final.md), with the
  next implementation stage being F1 - Privacy Contract Parity after F0 lands
  and `main` is green.
- Known blockers: none.

## Phased Work

### Stage RC0 - Published Baseline Audit

- Verify `v0.1.0-beta.1` release metadata, local tag resolution, and latest
  `main` Windows Harness status.
- Confirm the release checklist, manual smoke evidence template, watcher
  preview docs, and MCP examples are discoverable from docs.
- Update only baseline or cursor documentation if drift is found.
- Do not change product code.

### Stage RC1 - Install And CLI Packaging Smoke

- Add or document a fresh-environment smoke that installs the project into a
  temporary virtual environment and runs:
  `python -m winchronicle --help`, `status`, `init`, fixture `capture-once`,
  `search-captures`, `generate-memory`, and `search-memory`.
- Keep the smoke deterministic and fixture-based.
- Do not introduce cloud upload, external service dependencies, or real UIA
  requirements into this install smoke.

### Stage RC2 - Operator Quickstart And Privacy Polish

- Make the README and docs point clearly to the release checklist, manual smoke
  template, Windows UIA smoke docs, watcher preview docs, MCP examples, and
  known limitations.
- Re-state default privacy posture: screenshots and OCR disabled or absent by
  default; no audio, keyboard, clipboard, network upload, LLM calls, or desktop
  control in v0.1.
- Re-state that observed content is untrusted and must remain marked as
  `untrusted_observed_content` in captures, memory, and MCP responses.

### Stage RC3 - Evidence Consolidation

- Consolidate deterministic and manual release evidence expectations for the
  RC path.
- Keep manual UIA smoke artifacts outside git; record only commands, pass/fail
  status, timestamps, environment notes, and local artifact paths.
- Preserve the Phase 2 decision that VS Code metadata smoke is conditional hard
  when `code.cmd` exists, while strict Monaco editor marker capture remains
  diagnostic/non-blocking.

### Stage RC4 - RC Candidate Preparation

- Run the full deterministic release checklist and available manual smoke gates
  on `main`.
- Prepare a `v0.1.0-rc.0` release-candidate note with validation evidence,
  release notes, rollback notes, and tag target.
- Do not publish `v0.1.0-rc.0` without explicit approval.

## Test Plan

- `python -m pytest -q`
- `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo`
- `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo`
- `python harness/scripts/run_harness.py`
- `git diff --check`
- GitHub Actions `Windows Harness` on each PR and after merges to `main`

Manual Windows UIA gates remain manual and interactive:

- Notepad targeted UIA smoke - hard gate.
- Edge targeted UIA smoke - hard gate.
- VS Code metadata targeted UIA smoke - hard/conditional when `code.cmd`
  exists.
- VS Code strict Monaco editor marker - diagnostic/non-blocking artifact.
- Watcher preview smoke - manual preview gate using a temporary
  `WINCHRONICLE_HOME`.

## Public Interfaces And Non-goals

- CLI remains:
  `init/status/capture-once/capture-frontmost/watch/privacy-check/search-captures/generate-memory/search-memory/mcp-stdio`.
- MCP tools remain read-only:
  `current_context`, `search_captures`, `search_memory`, `read_recent_capture`,
  `recent_activity`, and `privacy_status`.
- Product CLI still does not expose targeted `--hwnd`, `--pid`, or
  `--window-title` capture.
- No screenshot capture, OCR, audio recording, keyboard capture, clipboard
  capture, network upload, LLM calls, MCP write tools, arbitrary file reads,
  service/daemon install, polling capture loop, default background capture, or
  desktop control.
- Phase 6 remains specification-only until a future tests-first round.

## Assumptions

- `v0.1.0-rc.0` is the published release-candidate baseline.
- The next active target is governed by
  [v0.1.0 Final Readiness Plan](next-round-plan-v0.1.0-final.md): final only
  if no product/schema/CLI/MCP/privacy contract changes require another public
  candidate; otherwise `v0.1.0-rc.1`.
- Work proceeds as small PRs, with one stage per branch unless the user
  explicitly asks for a different batching strategy.
- Manual UIA smoke continues to require an interactive Windows desktop and does
  not move into default CI.

## Decision Log

- Chose RC readiness because Phase 0 through Phase 5 have runnable v0.1
  surfaces and the remaining risk is release confidence, installability,
  operator clarity, and evidence quality.
- Deferred Phase 6 implementation because screenshots/OCR are optional future
  enrichment and would expand the capture surface.
- Kept RC0 documentation-only because the first post-release task is to confirm
  the published baseline before changing behavior.
- Treated file-level presence under `docs/` as sufficient for RC0
  discoverability because RC2 explicitly owns README and operator quickstart
  polish. README currently links the release checklist and watcher preview; the
  broader docs index polish remains the next documentation-focused stage.
- Added the RC1 install/CLI smoke as a deterministic harness script rather than
  a live UIA smoke because installability is the risk under test, not capture
  breadth.
- Created the RC1 smoke virtual environment with access to the already
  installed gate dependencies and installed WinChronicle with `--no-deps`; this
  keeps the smoke local and avoids introducing a network dependency into the
  release gate.
- Added a dedicated operator quickstart for RC2 instead of expanding README
  into a long manual. README now points to the quickstart and the main docs,
  while the quickstart owns the operator flow, privacy posture, and trust
  boundary summary.
- Kept RC2 documentation-only because the task was discoverability and privacy
  posture, not a product interface change.
- Added a dedicated release evidence guide for RC3 so release-candidate records
  have a single source for deterministic gates, manual smoke evidence,
  artifact handling, privacy/scope confirmation, and VS Code strict diagnostic
  treatment.
- Updated the manual smoke evidence template to include the install/CLI smoke
  and whitespace check so the manual evidence preflight mirrors the release
  checklist.

## Validation Log

- `gh release view v0.1.0-beta.1` confirmed the release is a prerelease, not a
  draft, and targets `2caf922733693ff5c63e39375d1882b19dcd508f`.
- `git rev-parse v0.1.0-beta.1` resolved to
  `2caf922733693ff5c63e39375d1882b19dcd508f`.
- GitHub Actions `Windows Harness` run `24987887814` passed on `main` at the
  published target.
- Stage RC0 baseline audit:
  - `gh release view v0.1.0-beta.1` confirmed the release is still a
    prerelease, not a draft, and targets
    `2caf922733693ff5c63e39375d1882b19dcd508f`.
  - `git rev-parse v0.1.0-beta.1` resolved to
    `2caf922733693ff5c63e39375d1882b19dcd508f`.
  - `git rev-parse HEAD` resolved to
    `51140bf8dfcb2cfcf65776653c927b9598d3247e` on the RC0 branch created from
    latest `main`.
  - GitHub Actions `Windows Harness` run `24990257758` passed on latest `main`
    at `51140bf8dfcb2cfcf65776653c927b9598d3247e`.
  - Presence checks passed for `docs/release-checklist.md`,
    `docs/manual-smoke-evidence-template.md`, `docs/watcher-preview.md`,
    `docs/mcp-readonly-examples.md`, `docs/windows-uia-smoke.md`, and
    `docs/known-limitations.md`.
- Stage RC1 install and CLI packaging smoke:
  - Added `harness/scripts/run_install_cli_smoke.py`.
  - Updated `harness/scripts/run_harness.py` so the full deterministic harness
    runs the install/CLI smoke.
  - Updated `docs/release-checklist.md` and `harness/README.md` to document the
    install/CLI smoke.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python -m pytest -q` - 60 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo`
    - 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo`
    - 0 warnings, 0 errors.
  - `python harness/scripts/run_harness.py` - passed, including the new
    install/CLI smoke.
- Stage RC2 operator quickstart and privacy polish:
  - Added `docs/operator-quickstart.md`.
  - Updated README to link the operator quickstart, release checklist, manual
    smoke template, Windows UIA smoke gates, watcher preview, MCP examples,
    known limitations, and RC readiness plan.
  - Updated `docs/release-checklist.md` to link the operator quickstart and
    related manual/MCP/watcher docs.
  - Re-stated the default privacy posture and
    `trust = "untrusted_observed_content"` boundary in operator-facing docs.
- Stage RC3 evidence consolidation:
  - Added `docs/release-evidence.md`.
  - Updated README, operator quickstart, and release checklist to link the
    release evidence guide.
  - Updated the manual smoke evidence template preflight with
    `python harness/scripts/run_install_cli_smoke.py` and `git diff --check`.
  - Preserved the Phase 2 decision that VS Code metadata smoke is conditional
    hard when `code.cmd` exists, while VS Code strict Monaco marker capture is
    diagnostic/non-blocking.
