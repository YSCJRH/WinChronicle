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

- Current stage: AF3 - MCP And Memory Contract Review.
- Stage status: AF2 complete; AF3 is ready to start.
- Last completed evidence: AF2 diagnostics review PR #152 merged as
  `382cfab357cf13264b141d0bb1eefefc7c9eaf77`, PR Windows Harness run
  `25599095958` passed, and post-merge `main` Windows Harness run
  `25599141386` passed on that SHA.
- Last validation: `docs/helper-watcher-diagnostics-sweep-post-v0.1.16.md`
  records the AF2 content-free `watch --events` validation diagnostic fix and
  deterministic coverage for helper/watcher timeout, malformed output, invalid
  embedded helper payloads, no observed-content echo, duplicate skip,
  denylist skip, heartbeat-only liveness, and diagnostic artifact policy.
- Next atomic task: start AF3 by reviewing read-only MCP examples, memory docs,
  deterministic demo guidance, and scorecards for trust-boundary and
  response-shape consistency.
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
- Completed AF0 after AE4 publication reconciliation landed on `main` and its
  post-merge Windows Harness passed.
- Chose AF1 as a docs-only audit because repository metadata gaps remain manual
  maintainer settings and do not require product-code changes.
- Completed AF1 after PR #150 and post-merge `main` Windows Harness passed.
- Started AF2 as a diagnostics sweep; a read-only review found a narrow
  `watch --events` validation diagnostic leak, so AF2 includes a content-free
  CLI wrapper fix plus deterministic evidence without expanding capture
  surfaces.
- Completed AF2 after PR #152 and post-merge `main` Windows Harness passed.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.

## Validation Log

- Stage AF0 initialization:
  - `gh release view v0.1.16 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; the release is published, not a draft, not a prerelease, published at `2026-05-09T09:31:17Z`, and targets `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `git rev-parse v0.1.16` - passed and printed `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `git ls-remote --tags origin v0.1.16` - passed and printed `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `gh release view v0.1.16-rc.0 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt,name` - passed; the prerelease remains published and targets `70caf364f68d8c159eb74bbbc23e7469db22a244`.
- Stage AF0 baseline landing:
  - PR #148 Windows Harness run `25598038285` - passed.
  - PR #148 merged as `b36581c25a609f801a48cefda7354781d6dfb888`.
  - `gh run view 25598080136 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AE4 `main` Windows Harness concluded `success` on `b36581c25a609f801a48cefda7354781d6dfb888`.
- Stage AF1 initialization:
  - `gh repo view YSCJRH/WinChronicle --json nameWithOwner,visibility,defaultBranchRef,description,homepageUrl,repositoryTopics,url` - passed; repository is public on `main`, with empty description, homepage, and topics.
  - `gh release view v0.1.16 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt,name` - passed; `v0.1.16` is published, not a draft or prerelease, published at `2026-05-09T09:31:17Z`, and targets `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `gh run view 25598257646 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AF0 `main` Windows Harness concluded `success` on `85172956c978fbb6b3355d7e3e75e2ba25fc909a`.
- Stage AF1 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed; 57 tests passed.
  - `python -m pytest -q` - passed; 155 tests passed.
  - `python harness/scripts/run_harness.py` - passed; includes 155 pytest tests, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search/memory, fixture watcher, and preview watcher smoke.
  - `git diff --check` - passed.
- Stage AF1 completion:
  - PR #150 Windows Harness run `25598506221` - passed.
  - PR #150 merged as `b7f65186bd009d625eb29756c642a1c34fc0cccb`.
  - `gh run view 25598562659 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AF1 `main` Windows Harness concluded `success` on `b7f65186bd009d625eb29756c642a1c34fc0cccb`.
- Stage AF1 completion reconciliation:
  - PR #151 Windows Harness run `25598644752` - passed.
  - PR #151 merged as `da5136c80fae1c4a7199279b05fa7e8dee449782`.
  - `gh run view 25598686029 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AF1-completion `main` Windows Harness concluded `success` on `da5136c80fae1c4a7199279b05fa7e8dee449782`.
- Stage AF2 local validation:
  - `python -m pytest tests/test_cli.py tests/test_watcher_events.py tests/test_uia_helper_quality_matrix.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q` - passed; 92 tests passed.
  - `python -m pytest -q` - passed; 160 tests passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed; 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed; 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed; includes 160 pytest tests, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search/memory, fixture watcher, and preview watcher smoke.
  - `git diff --check` - passed.
- Stage AF2 completion:
  - PR #152 Windows Harness run `25599095958` - passed.
  - PR #152 merged as `382cfab357cf13264b141d0bb1eefefc7c9eaf77`.
  - `gh run view 25599141386 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AF2 `main` Windows Harness concluded `success` on `382cfab357cf13264b141d0bb1eefefc7c9eaf77`.
