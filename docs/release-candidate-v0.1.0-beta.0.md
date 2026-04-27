# v0.1.0-beta.0 Release Candidate

## Summary

This candidate promotes the v0.1 beta hardening slice after
`v0.1.0-alpha.1`. It keeps WinChronicle UIA-first, harness-first, local-first,
and read-only MCP first.

Current PR: <https://github.com/YSCJRH/WinChronicle/pull/2>

## Execution Cursor

- Current stage: post-merge release candidate validation for v0.1 beta
  hardening.
- Stage status: F - release candidate conditions are met on `main`; do not
  publish automatically.
- Last completed evidence: PR #2 merged to `main` as
  `edec3633a95d209cd0b0f52bb7159fd2f0214d2a`.
- Last validation: release checklist passed on `main`, except VS Code strict
  editor marker diagnostic failure.
- Next atomic task: wait for explicit approval, then publish
  `v0.1.0-beta.0` from the validated `main` baseline.
- Known blockers: release publication still requires explicit approval.

## Public Interfaces And Non-goals

- CLI remains:
  `init/status/capture-once/capture-frontmost/watch/privacy-check/search-captures/generate-memory/search-memory/mcp-stdio`.
- MCP adds only read-only `search_memory`.
- Product CLI still does not expose `--hwnd`, `--pid`, or `--window-title`.
- No screenshot, OCR, audio, keyboard capture, clipboard capture, network
  upload, LLM calls, MCP write tools, or desktop control were added.

## Progress Log

- R0 CI/release gates: Windows Harness workflow added and passed.
- R1 UIA helper hardening: wrapper diagnostics cover timeout, invalid JSON,
  empty stdout, and nonzero exit without observed-content echo.
- R2 watcher preview: malformed JSONL, timeout, and nonzero exit diagnostics
  are covered without saving raw JSONL.
- R3 MCP + memory: `search_memory` is read-only, matches CLI memory search, and
  preserves `untrusted_observed_content`.
- R4 Phase 6 prep: screenshot/OCR privacy scorecard added without
  implementing screenshot/OCR.

## Validation Log

- Post-merge `main` validation completed on
  `edec3633a95d209cd0b0f52bb7159fd2f0214d2a`.
- `python -m pytest -q`: 60 passed.
- `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo`: passed.
- `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo`: passed.
- `python harness/scripts/run_harness.py`: passed.
- `git diff --check`: passed.
- GitHub Actions `Windows Harness / Deterministic harness`: passed.
- Notepad targeted UIA smoke: passed.
- Edge targeted UIA smoke: passed.
- VS Code metadata UIA smoke: passed; editor marker was not exposed through
  UIA.
- VS Code strict marker UIA smoke: diagnostic failure consistent with the
  documented Monaco/UIA limitation.

## Decision Log

- No persistent Execution Cursor file existed, so this release candidate record
  is the current plan/status record for the branch.
- Real UIA app smokes remain manual release gates, not default CI, because they
  need an interactive Windows desktop.
- VS Code strict Monaco editor marker remains diagnostic and non-blocking for
  v0.1.
- Phase 6 remains specification-only; screenshot/OCR implementation is still
  out of scope.
- PR #2 was merged before publication because it was ready, mergeable, and the
  Windows Harness check was green.
- The release checklist was rerun on `main` after merge; no release was created
  because publication still requires explicit approval.

## Rollback

If `v0.1.0-beta.0` needs to be withdrawn after publication:

- mark the GitHub release as a prerelease with withdrawal notes or delete the
  prerelease tag if no downstream users depend on it;
- keep `v0.1.0-alpha.1` as the last known stable prerelease baseline;
- revert the merge commit for PR #2 on a new branch if the beta hardening slice
  is the source of the regression;
- rerun the deterministic release checklist before publishing a replacement
  prerelease.
