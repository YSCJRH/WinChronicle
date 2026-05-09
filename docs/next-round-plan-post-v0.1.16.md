# WinChronicle Post-v0.1.16 Maintenance Plan

## Summary

`v0.1.16` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16. The final release
tag targets `255f2a01cddde330d756a87359c4d3a8be4b11a2`, and the release is not
a draft or prerelease. The release was published at `2026-05-09T09:31:17Z`
after AE3 release-record review and post-merge Windows Harness run
`25597678444` passed on the tag target.

The post-v0.1.16 baseline should continue blueprint-aligned maintenance without
expanding the v0.1 product boundary. The next round should start with a
post-publication baseline cursor, then continue with public metadata/evidence
freshness, helper/watcher diagnostics, MCP/memory contracts, compatibility
guardrails, and any small drift discovered by those checks.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, no polling capture loop, and no default background capture.

## Execution Cursor

- Current stage: AF0 - Post-v0.1.16 Published Baseline Cursor.
- Stage status: AF0 ready to start after AE4 publication reconciliation.
- Last completed evidence: `v0.1.16` final publication passed and was verified
  with GitHub release metadata, remote tag lookup, and tag target
  `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
- Last validation: AE3 PR #147 Windows Harness run `25597623991` and
  post-merge `main` Windows Harness run `25597678444` passed before final
  publication.
- Next atomic task: start AF0 by recording the post-v0.1.16 baseline after
  this publication reconciliation lands on `main`.
- Known blockers: none for the published `v0.1.16` final release.

## Phased Work

### Stage AF0 - Post-v0.1.16 Baseline Cursor

- Add or update the active post-v0.1.16 maintenance cursor after final
  publication reconciliation.
- Confirm `v0.1.16` is the latest published release and `v0.1.16-rc.0` remains
  historical prerelease context.
- Confirm package/runtime/MCP version identity reports `0.1.16`.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, version metadata, or privacy behavior.

### Stage AF1 - Public Metadata And Evidence Freshness Follow-up

- Re-check README, operator docs, release metadata, repository metadata, and
  manual smoke freshness after `v0.1.16`.
- Record public metadata gaps as checklist items, not product-code blockers.
- Refresh only documentation/tests needed to keep evidence freshness clear.

### Stage AF2 - Helper And Watcher Preview Diagnostics Review

- Review helper and watcher preview diagnostics docs, scorecards, and tests
  against the roadmap lanes for UIA helper hardening and watcher preview.
- Strengthen documentation, deterministic tests, or narrow diagnostic code only
  for discovered drift in timeout, malformed output, no observed-content echo,
  duplicate skip, denylist skip, heartbeat-only diagnostics, or diagnostic
  artifact policy.
- Keep real UIA smoke manual and outside default CI.

### Stage AF3 - MCP And Memory Contract Review

- Re-check read-only MCP examples, memory docs, deterministic demo guidance,
  and scorecards for trust-boundary and response-shape consistency.
- Strengthen narrow docs/tests only if examples drift from the exact read-only
  MCP tool list or durable memory contract.

### Stage AF4 - Compatibility Guardrail Sweep

- Re-run deterministic gates and confirm the v0.1 boundary still holds.
- Treat existing tests and scorecards as compatibility oracles for version
  identity, exact read-only MCP tools, disabled privacy surfaces, observed
  content trust boundaries, watcher preview limits, durable memory contract,
  product targeted capture absence, and Phase 6 spec-only status.
- Strengthen tests only for discovered drift.

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

## Assumptions

- `v0.1.16` is the latest published stable release and must not be retagged.
- `v0.1.16-rc.0` remains historical prerelease evidence and must not be
  retagged.
- Manual UIA smoke for `v0.1.16` was freshly run in AE2 and is current for the
  final release record only. Future releases must make a new freshness
  decision.
- Phase 6 stays at spec/scorecard level for this round.

## Decision Log

- Chose AF0 as a docs-only active cursor so post-v0.1.16 work does not begin
  from the completed final-release plan.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.

## Validation Log

- Stage AF0 initialization:
  - `gh release view v0.1.16 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; the release is published, not a draft, not a prerelease, published at `2026-05-09T09:31:17Z`, and targets `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `git rev-parse v0.1.16` - passed and printed `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `git ls-remote --tags origin v0.1.16` - passed and printed `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `gh release view v0.1.16-rc.0 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt,name` - passed; the prerelease remains published and targets `70caf364f68d8c159eb74bbbc23e7469db22a244`.
