# v0.1.1 Post-Beta Stabilization Plan

## Summary

`v0.1.0-beta.0` is published and establishes the current baseline. The next
round should be a narrow post-beta stabilization pass, not a redesign of the
blueprint and not Phase 6 screenshot/OCR implementation.

Goal: make the beta easier to maintain, verify, and manually smoke without
expanding the product boundary.

## Execution Cursor

- Current stage: next-round planning from the published `v0.1.0-beta.0`
  baseline.
- Stage status: C - next-round plan is established; implementation should start
  with Stage N0 only.
- Last completed evidence: `v0.1.0-beta.0` prerelease is published from
  `d1162151ae09f573a661bb5faf5899b9d52b0af4`; `main` is green at
  `b23b70d2e3152b8332e80e47fc2b6e1bfb01160e`.
- Last validation: GitHub Actions `Windows Harness` succeeded on `main`; local
  release/tag verification succeeded.
- Next atomic task: create a branch for Stage N0 and address the GitHub Actions
  Node 20 deprecation warning without changing product behavior.
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
- The next release target is a small `v0.1.1` or `v0.1.0-beta.1` maintenance
  prerelease, chosen after Stage N0 depending on whether behavior changes are
  needed.
- Phase 6 remains specification-only until a future tests-first round.

## Decision Log

- Chose post-beta stabilization because the beta is already published and the
  visible outstanding signal is CI maintenance, not missing core capability.
- Chose Stage N0 as the first implementation step because the latest successful
  GitHub Actions run reports a Node 20 deprecation annotation.
- Kept manual UIA smoke outside default CI because it depends on an interactive
  Windows desktop.

## Validation Log

- `v0.1.0-beta.0` prerelease verified on GitHub.
- Local `v0.1.0-beta.0` tag resolves to the published target commit.
- Latest `main` Windows Harness run succeeded after the release baseline record.
