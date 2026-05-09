# WinChronicle v0.1.16 Final Release Plan

## Summary

`v0.1.16-rc.0` is published as a prerelease at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16-rc.0. The
prerelease tag targets `70caf364f68d8c159eb74bbbc23e7469db22a244`, and the
release is not a draft.

The current `main` baseline after prerelease publication reconciliation is
`b260ebaa8808bddcce20da166038511de23bf3b5`. Windows Harness run
`25596579705` passed on that SHA. The diff from `v0.1.16-rc.0` to current
`main` is documentation and documentation-test evidence only:

- `docs/manual-smoke-evidence-ledger.md`
- `docs/next-round-plan-post-v0.1.15.md`
- `docs/release-candidate-v0.1.16-rc.0.md`
- `docs/release-checklist.md`
- `docs/release-evidence.md`
- `tests/test_compatibility_evidence_docs.py`
- `tests/test_operator_diagnostics_docs.py`

No product code, schemas, CLI/MCP JSON shape, helper/watcher behavior, privacy
runtime behavior, or capture surfaces changed after the prerelease tag.

This plan is the active final-release cursor after `v0.1.16-rc.0`. It does not
publish `v0.1.16` by itself. Direct final release can proceed only after fresh
final gates, explicit final manual smoke evidence, a final release record,
review, PR and post-merge Windows Harness validation, and explicit publication
approval. If final-readiness work requires any product or contract change, stop
the direct final path and prepare `v0.1.16-rc.1` instead.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, no polling capture loop, and no default background capture.

## Execution Cursor

- Current stage: AE0 - Post-v0.1.16-rc.0 Final Baseline Decision.
- Stage status: AE0 in progress; direct `v0.1.16` final planning is open, but
  `v0.1.16` is not published and final publication is not authorized by this
  plan.
- Last completed evidence: AD5 published `v0.1.16-rc.0` as a prerelease and
  publication reconciliation passed. The latest verified `main` evidence is
  Windows Harness run `25596579705`, which passed on
  `b260ebaa8808bddcce20da166038511de23bf3b5`.
- Next atomic task: run AE1 deterministic final gates on the current final
  target and confirm the direct final path still has no product or contract
  changes after `v0.1.16-rc.0`.
- Known blockers: final publication is blocked until AE1, AE2, AE3, review,
  PR Windows Harness, post-merge Windows Harness, and explicit publication
  approval complete.

## Phased Work

### Stage AE0 - Post-v0.1.16-rc.0 Final Baseline Decision

- Add this active final-release plan and keep the post-v0.1.15 plan as the
  completed prerelease path.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators start from this final
  cursor.
- Verify `v0.1.16-rc.0` is published, `v0.1.16` is not published, current
  `main` has green Windows Harness evidence, and tag-to-main drift is
  docs/tests-only.
- Do not publish or retag `v0.1.16` during AE0.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, privacy behavior, capture surfaces, version metadata, or release
  tags.

### Stage AE1 - Deterministic Final Gate Refresh

- Run the full deterministic final gate set on the current final target:
  pytest, helper build, watcher build, install CLI smoke, full harness, and
  `git diff --check`.
- Confirm package/runtime/MCP version identity remains `0.1.16`.
- Confirm exact read-only MCP tool list, disabled privacy surfaces, product
  targeted capture absence, watcher preview limits, durable memory contract,
  and Phase 6 spec-only status remain unchanged.
- If any product or contract fix is required, stop the direct final path and
  prepare `v0.1.16-rc.1`.

### Stage AE2 - Manual Final Smoke Refresh

- Rerun fresh final manual UIA smoke instead of automatically inheriting the
  `v0.1.16-rc.0` smoke result:
  - Notepad targeted UIA smoke: hard gate.
  - Edge targeted UIA smoke: hard gate.
  - VS Code metadata smoke: hard gate when `code.cmd` is available.
  - VS Code strict Monaco marker: diagnostic and non-blocking.
  - Watcher preview live smoke: preview diagnostic/manual confidence gate.
- Record commands, pass/fail results, timestamps, environment notes, and local
  artifact paths only.
- Do not commit raw helper JSON, raw watcher JSONL, screenshots, OCR output,
  observed text, local page contents, editor buffer contents, passwords,
  secrets, or token canaries.

### Stage AE3 - v0.1.16 Final Release Record And Publication

- Add `docs/release-v0.1.16.md` using the established final release record
  shape: metadata, deterministic gates, manual smoke, watcher preview, release
  notes, privacy/scope, rollback, and publication decision.
- Update docs tests and operator entry points to distinguish the final release
  record from the prerelease candidate record.
- Open a reviewed PR and require Windows Harness success before merge.
- Publish `v0.1.16` only after explicit publication approval. The final tag
  should target the post-merge `main` SHA that contains the final release
  record and passed Windows Harness.
- If publication is not approved or a product/contract change is required,
  do not publish final; prepare the next release-candidate path instead.

### Stage AE4 - v0.1.16 Final Publication Reconciliation

- Verify the GitHub release URL, final tag target, draft status, prerelease
  status, published timestamp, and remote tag.
- Update README, operator quickstart, release checklist, release evidence
  guide, manual smoke evidence ledger, and tests so `v0.1.16` is the latest
  published release.
- Add the post-`v0.1.16` maintenance cursor after final publication.
- Record PR Windows Harness and post-merge `main` Windows Harness evidence.

## Public Interfaces And Non-goals

- CLI remains unchanged:
  `init/status/capture-once/capture-frontmost/watch/privacy-check/search-captures/generate-memory/search-memory/mcp-stdio`.
- MCP tool list remains unchanged and read-only: `current_context`,
  `search_captures`, `search_memory`, `read_recent_capture`,
  `recent_activity`, and `privacy_status`.
- Product CLI still does not expose targeted `--hwnd`, `--pid`,
  `--window-title`, `--window-title-regex`, or `--process-name` capture flags.
- Do not implement screenshot capture, OCR, audio recording, keyboard capture,
  clipboard capture, network upload, LLM calls, desktop control, MCP write
  tools, arbitrary file read tools, daemon/service install, polling capture
  loop, default background capture, or product targeted capture.
- Phase 6 remains privacy spec/scorecard only unless a future plan explicitly
  authorizes tests-first implementation.

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

- AE0: docs tests confirm this final-release plan is the active cursor, the
  post-v0.1.15 plan is the completed prerelease path, `v0.1.16-rc.0` is the
  current published prerelease, and `v0.1.16` is not published.
- AE1: deterministic gates pass on the current final target without requiring
  product or contract changes.
- AE2: fresh final manual UIA smoke is recorded with local artifact paths only.
- AE3: final release record includes local, PR, post-merge, privacy/scope,
  rollback, manual smoke, publication approval, release URL, and tag target
  evidence.
- AE4: publication reconciliation confirms `v0.1.16` is the latest published
  release and opens the post-final maintenance cursor.

## Assumptions

- `v0.1.16-rc.0` is the current published prerelease and must not be retagged.
- `v0.1.16` is not published yet.
- Version identity is already aligned to `0.1.16`.
- Tag-to-main drift after `v0.1.16-rc.0` is docs/tests-only at AE0.
- No required soak window after `v0.1.16-rc.0` has been recorded. If a release
  owner requires one, record it before AE3 publication.
- Fresh final manual UIA smoke is required by this plan before final
  publication.
- Phase 6 stays at spec/scorecard level for this final-release path.

## Decision Log

- Chose a direct-final planning cursor because `v0.1.16-rc.0` is published,
  current `main` is green, and the post-prerelease drift is docs/tests-only.
- Chose not to publish `v0.1.16` in AE0 because final-release evidence,
  manual smoke freshness, reviewed final release record, and publication
  approval are still missing.
- Chose fresh manual final smoke for AE2 because the manual smoke ledger
  requires a final freshness decision and AD5 smoke should not silently become
  final evidence.
- Chose `v0.1.16-rc.1` as the fallback if final-readiness review requires any
  product or contract change.

## Validation Log

- Stage AE0 initialization:
  - `gh release view v0.1.16-rc.0 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; the release is published, not a draft, marked prerelease, published at `2026-05-09T08:18:01Z`, and targets `70caf364f68d8c159eb74bbbc23e7469db22a244`.
  - `git rev-parse v0.1.16-rc.0` - passed and printed `70caf364f68d8c159eb74bbbc23e7469db22a244`.
  - `gh release view v0.1.16 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt,name` - failed with `release not found`, confirming `v0.1.16` is not published.
  - `git tag --list "v0.1.16*"` - passed and printed only `v0.1.16-rc.0`.
  - `git rev-parse HEAD` - passed and printed `b260ebaa8808bddcce20da166038511de23bf3b5`.
  - `gh run view 25596579705 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-prerelease-reconciliation `main` Windows Harness concluded `success` on `b260ebaa8808bddcce20da166038511de23bf3b5`.
  - `git diff --name-status v0.1.16-rc.0..HEAD` - passed; the diff listed only documentation and documentation-test evidence files.
