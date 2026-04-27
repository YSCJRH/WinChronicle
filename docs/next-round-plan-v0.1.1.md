# v0.1.0-beta.1 Post-Beta Stabilization Plan

## Summary

`v0.1.0-beta.0` is published and establishes the current baseline. The next
round should be a narrow post-beta stabilization pass, not a redesign of the
blueprint and not Phase 6 screenshot/OCR implementation.

Goal: make the beta easier to maintain, verify, and manually smoke without
expanding the product boundary.

## Execution Cursor

- Current stage: Stage N0 - CI Node 24 maintenance.
- Stage status: C - Stage N0 is complete and ready to merge after the PR
  Windows Harness re-validates this evidence update; Stage N1 is next after
  merge.
- Last completed evidence: `v0.1.0-beta.0` prerelease is published from
  `d1162151ae09f573a661bb5faf5899b9d52b0af4`; `main` is green at
  `b7f83c9157d8d8f489f42963d6a002930cd8d322`; the Windows Harness workflow now
  opts JavaScript actions into Node 24 without changing the deterministic gate
  order.
- Last validation: local Stage N0 validation passed with pytest, helper build,
  watcher build, full harness, and diff check. PR #3 Windows Harness passed at
  `e887066a21b3a1197d8032970da35005013dddfd` with no Node 20 deprecation
  annotation in the checked log.
- Next atomic task: merge the Stage N0 PR after this evidence update re-runs
  green, then start Stage N1 on a separate branch.
- Known blockers: none.

## Phased Work

### Stage N0 - CI Maintenance

- Resolve or suppress the GitHub Actions Node 20 deprecation warning in the
  Windows Harness workflow using the smallest supported workflow change.
- Keep the deterministic gate set unchanged: pytest, helper build, watcher
  build, full harness, and diff check.
- Add a short CI maintenance note if the chosen workflow change is not
  self-explanatory.

### Stage N1 - Manual Smoke Evidence

- Add a small manual smoke evidence template for Notepad, Edge, VS Code
  metadata, VS Code strict diagnostic, and watcher preview.
- Do not commit observed content artifacts.
- Keep real UIA app smoke out of default CI.

### Stage N2 - Watcher Preview Diagnostics

- Strengthen watcher preview docs and tests around operator-facing errors only
  if gaps are found while using the existing preview command.
- Do not add a daemon, service installer, polling capture loop, or default
  background capture.

### Stage N3 - Read-Only MCP Compatibility Polish

- Add compatibility examples for `search_memory` and existing read-only tools.
- Keep MCP read-only and do not add arbitrary file reads, write tools, desktop
  control, screenshots, OCR, audio, keyboard, clipboard, or network tools.

## Test Plan

- `python -m pytest -q`
- `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo`
- `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo`
- `python harness/scripts/run_harness.py`
- `git diff --check`
- GitHub Actions `Windows Harness` on the branch and after merge to `main`
- Manual smoke only when a stage touches smoke docs or helper/watcher preview
  behavior.

## Public Interfaces And Non-goals

- Existing CLI remains unchanged.
- MCP remains read-only; no new write/control tools.
- Product CLI still does not expose targeted `--hwnd`, `--pid`, or
  `--window-title` capture.
- No screenshot, OCR, audio, keyboard capture, clipboard capture, network
  upload, LLM calls, service/daemon install, or desktop control.

## Assumptions

- `v0.1.0-beta.0` remains the published beta baseline.
- The next release target is a small `v0.1.0-beta.1` maintenance prerelease
  after the N0-N3 stabilization stages are complete or the user explicitly asks
  for an earlier release.
- Phase 6 remains specification-only until a future tests-first round.

## Decision Log

- Chose post-beta stabilization because the beta is already published and the
  visible outstanding signal is CI maintenance, not missing core capability.
- Chose Stage N0 as the first implementation step because the latest successful
  GitHub Actions run reports a Node 20 deprecation annotation.
- Kept manual UIA smoke outside default CI because it depends on an interactive
  Windows desktop.
- Chose a workflow-level `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24` environment
  variable
  for Stage N0 because it is the smallest supported workflow opt-in and keeps
  the existing deterministic gates unchanged.
- Promoted the Node 24 opt-in from job-level to workflow-level after the first
  PR run still emitted the Node 20 deprecation annotation while forcing actions
  to Node 24.
- Updated the three official setup actions to their Node 24-compatible major
  versions after GitHub Actions continued to report Node 20 action metadata even
  with the workflow-level opt-in. The deterministic gate order stayed unchanged.
- Treated the first local `run_harness.py` watcher smoke failure as a local
  short-duration flake after the identical watcher smoke passed on direct rerun
  and the full harness passed on rerun; no watcher behavior was changed.

## Validation Log

- `v0.1.0-beta.0` prerelease verified on GitHub.
- Local `v0.1.0-beta.0` tag resolves to the published target commit.
- Latest `main` Windows Harness run succeeded after the release baseline record.
- Stage N0 local validation:
  - `python -m pytest -q` - 60 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - 0 warnings, 0 errors.
  - `git diff --check` - passed.
  - First `python harness/scripts/run_harness.py` attempt hit a local watcher
    smoke write/heartbeat flake; `python harness/scripts/run_watcher_smoke.py`
    then passed, and `python harness/scripts/run_harness.py` passed on rerun.
- Stage N0 PR validation:
  - PR #3 Windows Harness run `24984285240` passed at
    `e887066a21b3a1197d8032970da35005013dddfd`.
  - Checked the run log for `Node.js 20`, `Node 20`, and deprecation matches;
    no Node 20 deprecation annotation remained after upgrading the official
    setup actions and keeping the Node 24 opt-in.
