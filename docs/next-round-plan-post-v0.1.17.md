# WinChronicle Post-v0.1.17 Maintenance Plan

## Summary

`v0.1.17` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.17. The maintenance
release tag targets `5b260edc3bddc48986e52179b2ffd261856a89ac`, and the
release is not a draft or prerelease. The release was published at
`2026-05-09T12:56:45Z`.

The AF7 publication reconciliation landed on `main` as
`110ace3f27d8bb9f1eff2c45449998fd0373a998`. PR #160 Windows Harness run
`25601966464` passed, and post-merge `main` Windows Harness run `25602018700`
passed on that SHA.

The post-v0.1.17 baseline should continue blueprint-aligned maintenance without
expanding the v0.1 product boundary. The next round starts with this
post-publication baseline cursor, then continues with public metadata/evidence
freshness, helper/watcher diagnostics, MCP/memory contracts, compatibility
guardrails, and any small drift discovered by those checks.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, no polling capture loop, and no default background capture.

## Execution Cursor

- Current stage: AG0 - Post-v0.1.17 Baseline Cursor.
- Stage status: AG0 review in progress; AF7 is complete.
- Last completed evidence: AF7 publication reconciliation PR #160 merged as
  `110ace3f27d8bb9f1eff2c45449998fd0373a998`, PR Windows Harness run
  `25601966464` passed, and post-merge `main` Windows Harness run
  `25602018700` passed.
- Last validation: `gh release view v0.1.17 --json
  tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` verified
  the published, non-draft, non-prerelease release at
  `2026-05-09T12:56:45Z`; `git ls-remote --tags origin v0.1.17` verified the
  remote tag target `5b260edc3bddc48986e52179b2ffd261856a89ac`.
- Next atomic task: land this post-v0.1.17 baseline cursor through PR and
  post-merge Windows Harness validation, then start AG1 public metadata and
  evidence freshness follow-up.
- Known blockers: none for the published `v0.1.17` maintenance release.

## Phased Work

### Stage AG0 - Post-v0.1.17 Baseline Cursor

- Add this post-v0.1.17 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Update docs tests so `v0.1.17` is the latest published release, this plan is
  the active cursor, and post-v0.1.16 is completed historical context.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, version metadata, or privacy behavior.

### Stage AG1 - Public Metadata And Evidence Freshness Follow-up

- Re-check README, operator docs, release metadata, repository metadata, and
  manual smoke freshness after `v0.1.17`.
- Record public metadata gaps as checklist items, not product-code blockers.
- Refresh only documentation/tests needed to keep evidence freshness clear.

### Stage AG2 - Helper And Watcher Preview Diagnostics Review

- Review helper and watcher preview diagnostics docs, scorecards, and tests
  against the roadmap lanes for UIA helper hardening and watcher preview.
- Strengthen documentation, deterministic tests, or narrow diagnostic code only
  for discovered drift in timeout, malformed output, no observed-content echo,
  duplicate skip, denylist skip, heartbeat-only diagnostics, or diagnostic
  artifact policy.
- Keep real UIA smoke manual and outside default CI.

### Stage AG3 - MCP And Memory Contract Review

- Re-check read-only MCP examples, memory docs, deterministic demo guidance,
  and scorecards for trust-boundary and response-shape consistency.
- Strengthen narrow docs/tests/code only if evidence drifts from the exact
  read-only MCP tool list, durable memory contract, or observed-content trust
  boundary.

### Stage AG4 - Compatibility Guardrail Sweep

- Re-run deterministic gates and confirm the v0.1 boundary still holds.
- Treat existing tests and scorecards as compatibility oracles for version
  identity, exact read-only MCP tools, disabled privacy surfaces, observed
  content trust boundaries, watcher preview limits, durable memory contract,
  product targeted capture absence, and Phase 6 spec-only status.
- Strengthen tests only for discovered drift.

### Stage AG5 - Release-Readiness Decision

- Decide whether AG1-AG4 documentation, harness, and compatibility-test
  guardrails warrant a post-v0.1.17 release-readiness plan.
- If a release-readiness plan is warranted, require a fresh version decision,
  evidence-freshness check, and manual UIA smoke freshness decision before any
  publication.
- If no release is warranted, start the next smallest blueprint implementation
  lane with contracts, fixtures, tests, and scorecards first.
- Do not retag `v0.1.17`; use a future compatible version only through an
  explicit release-readiness record.

## Public Interfaces And Non-goals

- CLI command set remains unchanged:
  `init/status/capture-once/capture-frontmost/watch/privacy-check/search-captures/generate-memory/search-memory/mcp-stdio`.
- `generate-memory` manifest JSON includes the compatible AF3 trust-boundary
  fields `trust`, `untrusted_observed_content`, and `instruction`.
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

## Assumptions

- `v0.1.17` is the latest published stable release and must not be retagged.
- `v0.1.16` remains the previous stable release and must not be retagged.
- Manual UIA smoke for `v0.1.17` was freshly rerun in AF6 and remains the
  latest full manual UIA smoke source until a later plan makes a new freshness
  decision.
- Phase 6 stays at spec/scorecard level for this round.

## Decision Log

- Started AG0 after AF7 publication reconciliation landed on `main` as
  `110ace3f27d8bb9f1eff2c45449998fd0373a998` and post-merge Windows Harness
  run `25602018700` passed.
- Kept AG0 docs-only because `v0.1.17` publication is already verified and the
  next safe task is to establish the post-v0.1.17 maintenance cursor.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.

## Validation Log

- Stage AG0 initialization:
  - `gh release view v0.1.17 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; `v0.1.17` is published, not a draft, not a prerelease, published at `2026-05-09T12:56:45Z`, and targets `5b260edc3bddc48986e52179b2ffd261856a89ac`.
  - `git ls-remote --tags origin v0.1.17` - passed and printed `5b260edc3bddc48986e52179b2ffd261856a89ac`.
  - `gh release view v0.1.16 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; `v0.1.16` remains published as the previous stable release, not a draft, not a prerelease, published at `2026-05-09T09:31:17Z`, and targets `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `gh pr view 160 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName` - passed; PR #160 merged at `2026-05-09T13:14:04Z` as `110ace3f27d8bb9f1eff2c45449998fd0373a998`.
  - `gh run view 25601966464 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #160 Windows Harness concluded `success` on `b61f8299d75d6746b82127f40028291a43150c1d`.
  - `gh run view 25602018700 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AF7 `main` Windows Harness concluded `success` on `110ace3f27d8bb9f1eff2c45449998fd0373a998`.
