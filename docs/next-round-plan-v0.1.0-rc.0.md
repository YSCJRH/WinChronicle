# v0.1.0-rc.0 Readiness Plan

## Summary

`v0.1.0-beta.1` is published and green. The next round should prepare a
`v0.1.0-rc.0` candidate by tightening installation, operator documentation,
and release evidence, not by adding new capture surfaces.

This plan keeps the product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, screenshots/OCR/audio/keyboard/clipboard
capture off or absent by default, no LLM reducer/classifier, no network upload,
and no desktop control.

## Execution Cursor

- Current stage: published `v0.1.0-beta.1` baseline planning.
- Stage status: G - `v0.1.0-beta.1` is published; the next implementation
  round starts at RC0.
- Last completed evidence: release
  `https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.0-beta.1`
  targets `2caf922733693ff5c63e39375d1882b19dcd508f`; `main` Windows Harness
  run `24987887814` passed on that target.
- Last validation: GitHub release metadata and local tag resolution both point
  to `2caf922733693ff5c63e39375d1882b19dcd508f`.
- Next atomic task: start Stage RC0 on a new branch and perform a published
  baseline audit without product behavior changes.
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

- `v0.1.0-beta.1` remains the published beta baseline.
- The next release target is `v0.1.0-rc.0`.
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

## Validation Log

- `gh release view v0.1.0-beta.1` confirmed the release is a prerelease, not a
  draft, and targets `2caf922733693ff5c63e39375d1882b19dcd508f`.
- `git rev-parse v0.1.0-beta.1` resolved to
  `2caf922733693ff5c63e39375d1882b19dcd508f`.
- GitHub Actions `Windows Harness` run `24987887814` passed on `main` at the
  published target.
