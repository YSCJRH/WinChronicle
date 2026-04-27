# v0.1.0-beta.1 Release Candidate

## Summary

This candidate promotes the post-beta stabilization slice after
`v0.1.0-beta.0`. It keeps WinChronicle local-first, UIA-first,
harness-first, and read-only MCP first.

Release content baseline before adding this candidate record:
`8ed3f866a04b86dc404e474e786ecafea5ca0854`.

## Execution Cursor

- Current stage: `v0.1.0-beta.1` release candidate.
- Stage status: F - release checklist is complete; prerelease publication
  requires explicit user approval.
- Last completed evidence: N0 through N3 are complete and merged to `main`.
- Last validation: deterministic release gates, GitHub Actions, and available
  manual smoke gates passed; VS Code strict Monaco marker remains diagnostic
  and non-blocking.
- Next atomic task: publish `v0.1.0-beta.1` as a GitHub prerelease after
  explicit approval, then verify the tag and release metadata.
- Known blockers: publication approval is pending.

## Public Interfaces And Non-goals

- CLI remains:
  `init/status/capture-once/capture-frontmost/watch/privacy-check/search-captures/generate-memory/search-memory/mcp-stdio`.
- MCP remains read-only with:
  `current_context`, `search_captures`, `search_memory`, `read_recent_capture`,
  `recent_activity`, and `privacy_status`.
- Product CLI still does not expose targeted `--hwnd`, `--pid`, or
  `--window-title` capture.
- No screenshot, OCR, audio, keyboard capture, clipboard capture, network
  upload, LLM calls, MCP write tools, service/daemon install, polling capture
  loop, default background capture, or desktop control were added.

## Release Notes Draft

Highlights:

- CI Node 24 readiness: Windows Harness now uses Node 24-compatible GitHub
  Actions and no longer emits the Node 20 deprecation annotation.
- Manual smoke evidence template: added a release-candidate template for
  Notepad, Edge, VS Code metadata, VS Code strict diagnostic, and watcher
  preview evidence without committing observed-content artifacts.
- Watcher preview diagnostics: documented operator-facing failure modes for
  nonzero watcher exit, helper failure, malformed JSONL, timeout, denylist skip,
  and duplicate skip.
- MCP examples: added compatibility examples for all read-only MCP tools and
  documented the `untrusted_observed_content` trust boundary.

Privacy/security notes:

- Screenshots and OCR remain absent/disabled by default.
- Audio, keyboard capture, clipboard capture, network upload, LLM
  summarization, desktop control, daemon/service install, and default
  background capture remain out of scope.
- Observed content returned through CLI, memory, and MCP remains marked as
  untrusted observed content.

## Validation Log

Deterministic gates on `8ed3f866a04b86dc404e474e786ecafea5ca0854`:

- `python -m pytest -q` - 60 passed.
- `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - 0 warnings, 0 errors.
- `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - 0 warnings, 0 errors.
- `python harness/scripts/run_harness.py` - passed.
- `git diff --check` - passed.
- GitHub Actions `Windows Harness` run `24987392882` - passed on `main`.

Manual smoke gates:

- Notepad targeted UIA smoke - passed.
  Artifact path:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-beta1-smoke-6cdbf49cb2e64d1084845aed4d598e7f\notepad\notepad-capture.json`.
- Edge targeted UIA smoke - passed.
  Artifact path:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-beta1-smoke-6cdbf49cb2e64d1084845aed4d598e7f\edge\edge-capture.json`.
- VS Code metadata targeted UIA smoke - passed when `code.cmd` was available;
  editor marker was not exposed through UIA.
  Artifact path:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-beta1-smoke-6cdbf49cb2e64d1084845aed4d598e7f\vscode\vscode-capture.json`.
- VS Code strict Monaco marker smoke - diagnostic failure, consistent with the
  documented Monaco/UIA limitation and not a v0.1 release blocker.
  Diagnostic artifact path:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-beta1-smoke-6cdbf49cb2e64d1084845aed4d598e7f\vscode-strict\vscode-capture.json`.
- Watcher preview smoke - passed with temporary `WINCHRONICLE_HOME`.
  Result:
  `captures_written=1`, `denylisted_skipped=0`, `duplicates_skipped=0`,
  `heartbeats=2`.

## Decision Log

- Treated VS Code strict Monaco marker failure as diagnostic/non-blocking per
  the Phase 2 decision and known limitation.
- Kept manual smoke artifacts outside git; only artifact paths and pass/fail
  metadata are recorded.
- Did not publish the prerelease automatically because publication requires
  explicit approval.

## Rollback

If `v0.1.0-beta.1` needs to be withdrawn after publication:

- mark the GitHub release as withdrawn in the release notes or delete the
  prerelease tag if no downstream users depend on it;
- keep `v0.1.0-beta.0` as the last known published beta baseline;
- revert the small post-beta maintenance PRs on a new branch if the regression
  is traced to N0, N1, N2, or N3;
- rerun the deterministic release checklist before publishing a replacement
  prerelease.
