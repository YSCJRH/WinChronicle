# WinChronicle Post-v0.1.5 Maintenance Plan

## Summary

`v0.1.6` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.6. The release tag
targets `914cf361ac5864fa31d393d125d14e45eeba96bc`. The S4 release-readiness
PR Windows Harness run `25551243900` passed, and the post-merge `main` Windows
Harness run `25551362920` passed on that SHA.

This post-v0.1.5 maintenance round completed as the compatible `v0.1.6`
maintenance release. The next atomic task is to establish the post-v0.1.6
baseline cursor before any new implementation work. This completed round did
not expand the capture surface or start Phase 6 implementation.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, and no default background capture.

## Execution Cursor

- Current stage: G - v0.1.6 Published Baseline Reconciliation.
- Stage status: G - v0.1.6 published; baseline reconciliation complete.
- Last completed evidence: `v0.1.6` is published at
  https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.6 and targets
  `914cf361ac5864fa31d393d125d14e45eeba96bc`. The S4 PR Windows Harness run
  `25551243900` passed, and post-merge `main` Windows Harness run
  `25551362920` passed on that SHA. Publication reconciliation PR #80 passed
  PR Windows Harness run `25552120656`, merged as
  `371060498c70a4e1ff4e075b3fd247b704c6d3f7`, and post-merge `main` Windows
  Harness run `25552214063` passed on that SHA.
- Last validation: publication metadata was verified with `gh release view
  v0.1.6`; local tags include `v0.1.6`; package runtime version reports
  `0.1.6`; post-publication reconciliation Windows Harness passed.
- Next atomic task: follow the post-v0.1.6 maintenance plan before starting
  new implementation work.
- Known blockers: none.

## Phased Work

### Stage S0 - Post-v0.1.5 Baseline Cursor

- Add this post-v0.1.5 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Keep the post-v0.1.4 plan closed and historical.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, or privacy behavior.

### Stage S1 - CI Runtime Maintenance Decision

- Review Windows Harness annotations and runner/runtime maintenance signals.
- If CI image or action-runtime updates are needed, make the smallest workflow
  update without removing gates or changing gate order.
- Preserve pytest, helper build, watcher build, full harness, and
  `git diff --check` in CI.
- Do not add real UIA smoke to default CI.

### Stage S2 - Release Evidence And Entry Hygiene

- Audit operator-facing docs and scorecards for stale current/latest release
  wording after `v0.1.5`.
- Strengthen narrow docs tests only for discovered drift around active cursor
  links, latest release identity, and evidence freshness wording.
- Keep `v0.1.5` as the stable release baseline until release-readiness work
  explicitly prepares a later version.
- Do not bump package/server version in S2.

### Stage S3 - Compatibility Guardrail Sweep

- Re-run deterministic gates and confirm the v0.1 boundary still holds.
- Strengthen tests only for discovered drift around version identity,
  read-only MCP tool list, privacy surface parity, memory/search trust
  boundaries, release evidence freshness, and Phase 6 spec-only status.
- Do not add helper/watcher product capabilities, MCP write tools, arbitrary
  file reads, screenshots, OCR, audio, keyboard capture, clipboard capture,
  network upload, desktop control, daemon/service install, polling capture
  loop, or default background capture.

### Stage S4 - v0.1.6 Release Readiness

- If S0-S3 only change documentation, tests, CI/runtime metadata, version
  metadata, or compatible drift fixes, prepare a compatible `v0.1.6`
  maintenance release.
- Before release, align package and server version metadata to `0.1.6`, add a
  release record, and record local gates plus PR and post-merge Windows
  Harness evidence.
- If any change alters product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture surface, stop the direct
  `v0.1.6` path and prepare a release candidate instead.
- Publication requires explicit release approval unless a newer active goal
  explicitly authorizes publishing the prepared release.

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

- S0: grep or doc inspection confirms the active cursor points to this
  post-v0.1.5 plan and historical plans remain historical.
- S1: CI runtime maintenance keeps the existing deterministic gate set and does
  not add interactive UIA smoke to default CI.
- S2: README, operator quickstart, release checklist, and release evidence
  guide do not describe older post-v0.1.x plans as the current cursor.
- S3: MCP tools remain exactly read-only, privacy surfaces remain disabled,
  memory/search trust boundaries remain stable, and Phase 6 remains spec-only.
- S4: release checklist, release evidence, rollback notes, and Windows Harness
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

- `v0.1.6` is the current stable release baseline and must not be modified or
  retagged.
- The next compatible release target must be chosen in the post-v0.1.6 plan.
- Phase 6 remains privacy spec/scorecard work only until a future tests-first
  round.
- Manual UIA smoke remains outside default CI because it depends on an
  interactive Windows desktop.

## Decision Log

- Chose a compatible `v0.1.6` maintenance target because the published
  `v0.1.5` round changed release evidence, docs, tests, and version metadata
  only, without product behavior changes.
- Chose S0 as a docs-only active cursor so post-v0.1.5 work does not begin
  from a closed historical plan.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.
- During S1, pinned the Windows Harness runner to `windows-2025-vs2026` after
  the latest `main` Windows Harness emitted a `windows-2025` redirection
  notice. The workflow gate order and gate set remain unchanged.
- During S2, audited operator-facing docs, scorecards, and tests for stale
  current/latest release wording after `v0.1.5`; no entry-point drift required
  product or documentation changes beyond this cursor update.
- During S3, treated the existing MCP, privacy-surface, and memory/search trust
  tests as the compatibility oracles; added a source-level Phase 6 absence
  guard and refreshed manual smoke freshness wording for the post-v0.1.5 path
  toward `v0.1.6`. No product behavior, schema, CLI/MCP shape, helper/watcher
  behavior, or capture surface changed.
- During S4, chose the direct compatible `v0.1.6` path because S0-S4 changed
  only documentation, tests, CI/runtime metadata, version metadata, release
  evidence, and compatibility guardrails. The `v0.1.6`
  release-readiness record explicitly accepts inherited `v0.1.0` manual UIA
  smoke for this compatible path, with no observed-content artifacts committed.
- During publication, published `v0.1.6` from
  `914cf361ac5864fa31d393d125d14e45eeba96bc` after S4 PR Windows Harness
  `25551243900` and post-merge `main` Windows Harness `25551362920` passed.
  Do not retag `v0.1.6`; establish a post-v0.1.6 cursor before starting new
  implementation work.
- During publication reconciliation, merged PR #80 as
  `371060498c70a4e1ff4e075b3fd247b704c6d3f7`; PR Windows Harness
  `25552120656` and post-merge `main` Windows Harness `25552214063` passed.
  This closes the post-v0.1.5 maintenance round.

## Validation Log

- Stage S0 initialization:
  - `gh release view v0.1.5 --json name,tagName,url,isDraft,isPrerelease,publishedAt,targetCommitish` - passed.
  - Post-publication `main` Windows Harness run `25546003233` - passed.
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed after establishing this active cursor.
  - `python -m pytest -q` - passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage S1 CI runtime validation:
  - `rg -n "windows-2025|windows-2025-vs2026|runs-on|FORCE_JAVASCRIPT_ACTIONS_TO_NODE24" .github docs tests` - confirmed the workflow still has the Node 24 environment setting and now pins `windows-2025-vs2026`.
  - `python -m pytest tests/test_windows_harness_workflow.py -q` - passed after adding the workflow guard.
  - `python -m pytest -q` - passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage S2 entry-hygiene validation:
  - `rg -n "latest published `v0\\.1\\.[0-4]`|stable baseline is `v0\\.1\\.[0-4]`|Stable release baseline \\| `v0\\.1\\.[0-4]`|active post-v0\\.1\\.[0-4]|current post-v0\\.1\\.[0-4]|current `v0\\.1\\.[0-4]`|current release.*v0\\.1\\.[0-4]|latest release.*v0\\.1\\.[0-4]|release-readiness candidate, not yet published|Pending publication|Publication approval: pending|v0\\.1\\.5 release-readiness record" README.md docs harness tests` - reviewed matches; only historical validation-log text and historical plans matched.
  - `rg -n "next-round-plan-post-v0\\.1\\.5|release-v0\\.1\\.5|v0\\.1\\.5 maintenance release|Post-v0\\.1\\.5" README.md docs tests` - confirmed current entry points reference the post-v0.1.5 plan and `v0.1.5` release record.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q` - passed.
  - `python -m pytest -q` - passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage S3 compatibility guardrail validation:
  - `rg -n "current_context|search_captures|search_memory|read_recent_capture|recent_activity|privacy_status|tool list|MCP remains read-only|write tools|desktop control|clipboard|screenshot|OCR|audio|keyboard|network" src tests docs harness -g "*.py" -g "*.md" -g "*.json"` - reviewed existing MCP, privacy, and disabled-surface guardrails.
  - `rg -n "untrusted_observed_content|trust|search-captures|search-memory|memory|entries_fts|captures_fts" src tests docs harness -g "*.py" -g "*.md" -g "*.json"` - reviewed search and memory trust-boundary guardrails.
  - `rg -n "Phase 6|screenshot|OCR|screenshots_enabled|ocr_enabled|allowlist|spec-only|not implement|not implemented" README.md docs harness tests src -g "*.py" -g "*.md" -g "*.json"` - reviewed Phase 6 spec-only guardrails.
  - `python -m pytest tests/test_phase6_privacy_scorecard.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_memory_pipeline.py -q` - passed.
  - `python -m pytest -q` - passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage S4 release-readiness validation:
  - `git fetch --tags --quiet` - passed; local tags include `v0.1.5`.
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed after aligning version identity to `0.1.6` and adding the release-readiness record.
  - `python -m pytest -q` - passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- v0.1.6 publication validation:
  - `gh release create v0.1.6 --target 914cf361ac5864fa31d393d125d14e45eeba96bc --title "v0.1.6"` - passed.
  - `gh release view v0.1.6 --json name,tagName,url,isDraft,isPrerelease,publishedAt,targetCommitish` - passed and returned release URL https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.6.
  - `gh run view 25551362920 --json databaseId,status,conclusion,headSha,url,createdAt,updatedAt,name,displayTitle` - passed; conclusion `success` on `914cf361ac5864fa31d393d125d14e45eeba96bc`.
  - `git fetch --tags --quiet` and `git show-ref --tags v0.1.6` - passed; local tag points to `914cf361ac5864fa31d393d125d14e45eeba96bc`.
  - `python -` version check - passed and printed `0.1.6`.
- v0.1.6 post-publication reconciliation validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed.
  - `python -m pytest -q` - passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
  - PR #80 Windows Harness run `25552120656` - passed.
  - Post-merge `main` Windows Harness run `25552214063` - passed on `371060498c70a4e1ff4e075b3fd247b704c6d3f7`.
