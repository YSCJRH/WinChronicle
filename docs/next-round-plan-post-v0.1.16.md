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

- Current stage: AF6 - v0.1.17 Release Readiness.
- Stage status: AF6 review in progress; AF5 is complete.
- Last completed evidence:
  `docs/release-readiness-decision-post-v0.1.16.md` and AF5 decision PR #158
  merged as `bbf6d3c64d7fef435e66d64d4e3b19d2390c391b`, PR Windows Harness run
  `25600947496` passed, and post-merge `main` Windows Harness run
  `25600994238` passed on that SHA.
- Last validation: `docs/release-v0.1.17.md` records the AF6 release-readiness
  candidate, version identity `0.1.17`, fresh hard-gate manual UIA smoke,
  heartbeat-only watcher diagnostic evidence, immutable `v0.1.16` release
  metadata, and compatible runtime/output hardenings without capture-surface
  expansion.
- Next atomic task: land the `v0.1.17` release-readiness record through PR and
  post-merge Windows Harness validation, then publish `v0.1.17` and reconcile
  the release metadata without retagging `v0.1.16`.
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
- Strengthen narrow docs/tests/code only if evidence drifts from the exact
  read-only MCP tool list, durable memory contract, or observed-content trust
  boundary.

### Stage AF4 - Compatibility Guardrail Sweep

- Re-run deterministic gates and confirm the v0.1 boundary still holds.
- Treat existing tests and scorecards as compatibility oracles for version
  identity, exact read-only MCP tools, disabled privacy surfaces, observed
  content trust boundaries, watcher preview limits, durable memory contract,
  product targeted capture absence, and Phase 6 spec-only status.
- Strengthen tests only for discovered drift.

### Stage AF5 - Release-Readiness Decision

- Decide whether the AF1-AF4 documentation, harness, and compatibility-test
  guardrails warrant a post-v0.1.16 release-readiness plan.
- If a release-readiness plan is warranted, require a fresh version decision,
  evidence-freshness check, and manual UIA smoke freshness decision before any
  publication.
- If no release is warranted, start the next smallest blueprint implementation
  lane with contracts, fixtures, tests, and scorecards first.
- Do not retag `v0.1.16`; use a future compatible version only through an
  explicit release-readiness record.

### Stage AF6 - v0.1.17 Release Readiness

- Bump package/runtime/MCP version identity to `0.1.17` only on the
  release-readiness branch.
- Record a direct compatible maintenance release path in
  `docs/release-v0.1.17.md`.
- Rerun fresh hard-gate manual UIA smoke because AF1-AF4 changed public
  CLI/runtime output shape after `v0.1.16`.
- Treat heartbeat-only live watcher preview as diagnostic liveness evidence,
  while deterministic watcher gates remain required.
- Require local deterministic gates, PR Windows Harness, and post-merge `main`
  Windows Harness before publication.
- Do not retag `v0.1.16`; publish `v0.1.17` only after validation and review.

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
  CLI wrapper fix plus deterministic evidence for invalid embedded helper
  payloads without expanding capture surfaces.
- Completed AF2 after PR #152 and post-merge `main` Windows Harness passed.
- Completed AF2 completion reconciliation after PR #153 and post-merge `main`
  Windows Harness passed.
- Started AF3 as an MCP/memory contract sweep; read-only reviews found that
  `generate-memory` manifest JSON omitted observed-content trust metadata and
  that standalone MCP smoke should freeze a literal tool list plus the full
  forbidden write/file/network/control term set.
- Completed AF3 after AF3 MCP/memory review PR #154 merged as
  `f55638cf213b40c07d01f1872a7ff828b3a85d6f` and post-merge `main` Windows
  Harness passed; evidence is recorded in
  `docs/mcp-memory-contract-sweep-post-v0.1.16.md`.
- Started AF4 as a compatibility guardrail sweep; read-only reviews found only
  documentation and guardrail precision drifts around public MCP ordering,
  complete targeted-flag wording, ordered MCP smoke comparison, and the AF3
  `generate-memory` manifest JSON compatibility shape.
- Completed AF4 after PR #156 and post-merge `main` Windows Harness passed.
- Chose AF5 as an explicit release-readiness decision because AF1-AF4 changed
  docs, deterministic tests, and harness guardrails without changing product
  behavior, capture surfaces, schemas, MCP tool schemas, or version metadata.
- Started AF5 as a release-readiness decision; `v0.1.16` remains the immutable
  latest published stable release, and AF1-AF4 warrant a narrow `v0.1.17`
  release-readiness plan because they include compatible unreleased
  runtime/output hardening.
- Completed AF5 after PR #158 and post-merge `main` Windows Harness passed.
- Started AF6 as a direct `v0.1.17` maintenance release-readiness candidate;
  version identity is bumped to `0.1.17`, fresh hard-gate manual UIA smoke was
  rerun, and `v0.1.16` remains immutable until `v0.1.17` publication is
  verified.
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
- Stage AF2 completion reconciliation:
  - PR #153 Windows Harness run `25599243227` - passed.
  - PR #153 merged as `3f819b9c2fa9aaaffc2e23ad72c8142c94cd8a15`.
  - `gh run view 25599306888 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AF2-completion `main` Windows Harness concluded `success` on `3f819b9c2fa9aaaffc2e23ad72c8142c94cd8a15`.
- Stage AF3 local validation:
  - `python -m pytest tests/test_mcp_tools.py tests/test_memory_pipeline.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q` - passed; 80 tests passed.
  - `python harness/scripts/run_mcp_smoke.py` - passed.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python -m pytest tests/test_phase6_privacy_scorecard.py tests/test_mcp_tools.py tests/test_memory_pipeline.py -q` - passed; 25 tests passed.
  - `python -m pytest -q` - passed; 162 tests passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed; 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed; 0 warnings, 0 errors.
  - `python harness/scripts/run_harness.py` - passed; includes 162 pytest tests, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search/memory, fixture watcher, and preview watcher smoke.
  - `git diff --check` - passed.
- Stage AF3 completion:
  - PR #154 Windows Harness run `25599715499` - passed.
  - PR #154 merged as `f55638cf213b40c07d01f1872a7ff828b3a85d6f`.
  - `gh run view 25599772190 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AF3 `main` Windows Harness concluded `success` on `f55638cf213b40c07d01f1872a7ff828b3a85d6f`.
- Stage AF4 local validation:
  - `python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py tests/test_version_identity.py -q` - passed; 50 tests passed.
  - `python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py tests/test_version_identity.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q` - passed; 113 tests passed.
  - `python harness/scripts/run_mcp_smoke.py` - passed.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python -m pytest -q` - passed; 165 tests passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
  - Boundary scan and control/capture dependency scan reviewed only existing
    disabled-surface contracts, documentation, tests, scorecards, fixtures,
    privacy canaries, and local smoke variable names; no new product
    CLI/MCP targeted capture, write/control tool, screenshot/OCR, audio,
    keyboard, clipboard, network/cloud upload, LLM, desktop control,
    daemon/service, polling capture, default background capture, or runtime
    dependency path was found.
- Stage AF4 completion:
  - PR #156 Windows Harness run `25600358015` - passed.
  - PR #156 merged as `20758124f5679be3a733ac0de8ed9c99e1d8777b`.
  - `gh run view 25600405807 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AF4 `main` Windows Harness concluded `success` on `20758124f5679be3a733ac0de8ed9c99e1d8777b`.
- Stage AF4 completion reconciliation:
  - PR #157 Windows Harness run `25600542270` - passed.
  - PR #157 merged as `74aeadc2e8fd0917ab02e0f73009f87453b4b1e8`.
  - `gh run view 25600584258 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AF4-completion `main` Windows Harness concluded `success` on `74aeadc2e8fd0917ab02e0f73009f87453b4b1e8`.
- Stage AF5 release-readiness decision:
  - `gh release view v0.1.16 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; `v0.1.16` remains published, not a draft, not a prerelease, published at `2026-05-09T09:31:17Z`, and targets `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `git rev-parse v0.1.16` - passed and printed `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `gh run view 25600584258 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; AF4 completion post-merge `main` Windows Harness concluded `success` on `74aeadc2e8fd0917ab02e0f73009f87453b4b1e8`.
  - `git diff --name-status v0.1.16..HEAD` - passed; AF1-AF4 include runtime/output changes in `src/winchronicle/cli.py`, `src/winchronicle/memory.py`, and `src/winchronicle/mcp/server.py`.
  - `git diff --stat v0.1.16..HEAD -- src/winchronicle/cli.py src/winchronicle/memory.py src/winchronicle/mcp/server.py` - passed; runtime changes are narrow compatible privacy/trust-boundary hardenings.
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed; 65 tests passed.
  - `python -m pytest -q` - passed; 166 tests passed.
  - `python harness/scripts/run_harness.py` - passed; includes 166 pytest tests, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search/memory, fixture watcher, and preview watcher smoke.
  - `git diff --check` - passed.
- Stage AF5 completion:
  - PR #158 Windows Harness run `25600947496` - passed.
  - PR #158 merged as `bbf6d3c64d7fef435e66d64d4e3b19d2390c391b`.
  - `gh run view 25600994238 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AF5 `main` Windows Harness concluded `success` on `bbf6d3c64d7fef435e66d64d4e3b19d2390c391b`.
- Stage AF6 manual smoke:
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-notepad.ps1 -ArtifactDir <artifact-root>\notepad -TimeoutSeconds 30` - passed.
  - `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-edge.ps1 -ArtifactDir <artifact-root>\edge -TimeoutSeconds 45` - passed.
  - `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -ArtifactDir <artifact-root>\vscode-metadata -TimeoutSeconds 45` - passed with the known Monaco diagnostic warning.
  - `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -Strict -ArtifactDir <artifact-root>\vscode-strict -TimeoutSeconds 45` - diagnostic failure, non-blocking; known Monaco/UIA limitation.
  - `python -m winchronicle watch --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper dotnet --helper-arg resources/win-uia-helper/bin/Debug/net8.0-windows/win-uia-helper.dll --duration 5 --depth 2 --heartbeat-ms 500 --capture-on-start` with temporary `WINCHRONICLE_HOME` - heartbeat-only liveness diagnostic; `captures_written: 0`, `heartbeats: 9`, `duplicates_skipped: 0`, `denylisted_skipped: 0`.
- Stage AF6 local deterministic validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_uia_helper_quality_matrix.py -q` - passed; 71 tests passed.
  - `python -m pytest -q` - passed; 167 tests passed.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed; includes 167 pytest tests, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search/memory, fixture watcher, and preview watcher smoke.
  - `git diff --check` - passed.
