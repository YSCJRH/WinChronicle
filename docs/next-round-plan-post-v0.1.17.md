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

- Current stage: AG4 - Compatibility Guardrail Sweep.
- Stage status: AG4 review in progress; AG3 landed through PR #164 and
  post-merge Windows Harness.
- Last completed evidence: AG3 MCP/memory contract review PR #164 merged as
  `bf38d3d580fafd50ce9ea4752bca31735869083f`, PR Windows Harness run
  `25603703247` passed, and post-AG3 `main` Windows Harness run `25603752386`
  passed on that SHA.
- Last validation: `gh run view 25603752386 --json
  databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt`
  verified the post-AG3 `main` Windows Harness concluded `success`; current
  compatibility docs and tests still cover version identity, exact read-only
  MCP tools, disabled privacy surfaces, observed-content trust boundaries,
  watcher preview limits, durable memory contract, product targeted-capture
  absence, and Phase 6 spec-only status.
- Next atomic task: land this AG4 compatibility guardrail review through PR and
  post-merge Windows Harness validation, then decide whether a post-v0.1.17
  release-readiness stage is warranted.
- Known blockers: none for product code. Live UIA smoke remains manual and
  outside default CI.

## Phased Work

### Stage AG0 - Post-v0.1.17 Baseline Cursor

- Add this post-v0.1.17 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Update docs tests so `v0.1.17` is the latest published release, this plan is
  the active cursor, and post-v0.1.16 is completed historical context.
- Completed in PR #161 with PR Windows Harness run `25602296648` and
  post-merge `main` Windows Harness run `25602345201`.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, version metadata, or privacy behavior.

### Stage AG1 - Public Metadata And Evidence Freshness Follow-up

- Re-check README, operator docs, release metadata, repository metadata, and
  manual smoke freshness after `v0.1.17`.
- Record public metadata gaps as checklist items, not product-code blockers.
- Add `docs/public-metadata-audit-post-v0.1.17.md`.
- Refresh only documentation/tests needed to keep evidence freshness clear.
- Do not run new manual UIA smoke unless product behavior, helper/watcher
  behavior, manual smoke scripts, capture behavior, privacy behavior, product
  CLI/MCP shape, capture surfaces, or release approval requirements change.
- Completed in PR #162 with PR Windows Harness run `25602763122` and
  post-merge `main` Windows Harness run `25602836902`.

### Stage AG2 - Helper And Watcher Preview Diagnostics Review

- Review helper and watcher preview diagnostics docs, scorecards, and tests
  against the roadmap lanes for UIA helper hardening and watcher preview.
- Strengthen documentation, deterministic tests, or narrow diagnostic code only
  for discovered drift in timeout, malformed output, no observed-content echo,
  duplicate skip, denylist skip, heartbeat-only diagnostics, or diagnostic
  artifact policy.
- Add `docs/helper-watcher-diagnostics-sweep-post-v0.1.17.md`.
- Keep real UIA smoke manual and outside default CI.
- Completed in PR #163 with PR Windows Harness run `25603218933` and
  post-merge `main` Windows Harness run `25603274783`.

### Stage AG3 - MCP And Memory Contract Review

- Re-check read-only MCP examples, memory docs, deterministic demo guidance,
  and scorecards for trust-boundary and response-shape consistency.
- Strengthen narrow docs/tests/code only if evidence drifts from the exact
  read-only MCP tool list, durable memory contract, or observed-content trust
  boundary.
- Add `docs/mcp-memory-contract-sweep-post-v0.1.17.md`.
- Keep real UIA smoke manual and outside default CI.
- Completed in PR #164 with PR Windows Harness run `25603703247` and
  post-merge `main` Windows Harness run `25603752386`.

### Stage AG4 - Compatibility Guardrail Sweep

- Re-run deterministic gates and confirm the v0.1 boundary still holds.
- Treat existing tests and scorecards as compatibility oracles for version
  identity, exact read-only MCP tools, disabled privacy surfaces, observed
  content trust boundaries, watcher preview limits, durable memory contract,
  product targeted capture absence, and Phase 6 spec-only status.
- Strengthen tests only for discovered drift.
- Add `docs/compatibility-guardrail-sweep-post-v0.1.17.md`.
- Keep real UIA smoke manual and outside default CI.

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
- Completed AG0 after PR #161 merged as
  `a994ab768deeaf08746bad296c1f8100d6ed22fb` and post-merge `main` Windows
  Harness run `25602345201` passed.
- Started AG1 as a docs/tests-only public metadata audit because repository
  metadata remains manually maintained and empty public metadata is not a
  product-code blocker.
- Completed AG1 after PR #162 merged as
  `0a5d72ea12ac030161ed387286dc15dc63c80b01` and post-merge `main` Windows
  Harness run `25602836902` passed.
- Started AG2 as a docs/tests-only helper/watcher diagnostics review because
  the current evidence surface already covers the expected v0.1 preview failure
  modes, and no product drift has been found.
- Completed AG2 after PR #163 merged as
  `461eb8b14f6733f5abfe87524da2358730da3b59` and post-merge `main` Windows
  Harness run `25603274783` passed.
- Started AG3 as a docs/tests-only MCP/memory contract review because exact
  read-only MCP tool list, trust metadata, durable memory, and forbidden tool
  boundary behavior are already covered by deterministic tests and scorecards.
- Completed AG3 after PR #164 merged as
  `bf38d3d580fafd50ce9ea4752bca31735869083f` and post-merge `main` Windows
  Harness run `25603752386` passed.
- Started AG4 as a docs/tests-only compatibility guardrail sweep because
  version identity, exact read-only MCP tools, disabled privacy surfaces,
  observed-content trust boundaries, watcher preview limits, durable memory,
  product targeted-capture absence, and Phase 6 spec-only status are already
  covered by deterministic tests and scorecards.
- AG4 found no required product behavior, schema, MCP tool-schema,
  helper/watcher output contract, capture storage shape, privacy runtime,
  capture-surface, dependency, or version-metadata change. It tightened
  docs/tests evidence so pass-through rejection covers every disabled
  helper/watcher surface flag, operator diagnostics names every disabled
  product targeted-capture flag, and daemon/service/polling/background terms
  are checked by an explicit scan.

## Validation Log

- Stage AG0 initialization:
  - `gh release view v0.1.17 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; `v0.1.17` is published, not a draft, not a prerelease, published at `2026-05-09T12:56:45Z`, and targets `5b260edc3bddc48986e52179b2ffd261856a89ac`.
  - `git ls-remote --tags origin v0.1.17` - passed and printed `5b260edc3bddc48986e52179b2ffd261856a89ac`.
  - `gh release view v0.1.16 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; `v0.1.16` remains published as the previous stable release, not a draft, not a prerelease, published at `2026-05-09T09:31:17Z`, and targets `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `gh pr view 160 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName` - passed; PR #160 merged at `2026-05-09T13:14:04Z` as `110ace3f27d8bb9f1eff2c45449998fd0373a998`.
  - `gh run view 25601966464 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #160 Windows Harness concluded `success` on `b61f8299d75d6746b82127f40028291a43150c1d`.
  - `gh run view 25602018700 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AF7 `main` Windows Harness concluded `success` on `110ace3f27d8bb9f1eff2c45449998fd0373a998`.
- Stage AG0 completion:
  - `gh pr view 161 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #161 merged at `2026-05-09T13:30:52Z` as `a994ab768deeaf08746bad296c1f8100d6ed22fb`.
  - `gh run view 25602296648 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #161 Windows Harness concluded `success` on `6781a85bb8423fbe0a13f3641266bf2ec7e0a913`.
  - `gh run view 25602345201 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AG0 `main` Windows Harness concluded `success` on `a994ab768deeaf08746bad296c1f8100d6ed22fb`.
- Stage AG1 initialization:
  - `gh repo view YSCJRH/WinChronicle --json nameWithOwner,visibility,defaultBranchRef,description,homepageUrl,repositoryTopics,url` - passed; repository is public on `main`, with empty description, homepage, and topics.
  - `gh release view v0.1.17 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; `v0.1.17` is published, not a draft, not a prerelease, published at `2026-05-09T12:56:45Z`, and targets `5b260edc3bddc48986e52179b2ffd261856a89ac`.
  - `gh release view v0.1.16 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; `v0.1.16` remains published as the previous stable release, not a draft, not a prerelease, published at `2026-05-09T09:31:17Z`, and targets `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `git ls-remote --tags origin v0.1.17` - passed and printed `5b260edc3bddc48986e52179b2ffd261856a89ac`.
- Stage AG1 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 69 tests.
  - `python -m pytest -q` - passed, 170 tests.
  - `git diff --check` - passed.
  - stale AG0/current-decision wording scan across `README.md`, `docs`, and
    `tests` - passed with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 170 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AG1 completion:
  - `gh pr view 162 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName` - passed; PR #162 merged at `2026-05-09T13:55:16Z` as `0a5d72ea12ac030161ed387286dc15dc63c80b01`.
  - `gh run view 25602763122 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #162 Windows Harness concluded `success` on `ec056dd0c368c1d4d8b182f49383198e5acbbaf0`.
  - `gh run view 25602836902 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AG1 `main` Windows Harness concluded `success` on `0a5d72ea12ac030161ed387286dc15dc63c80b01`.
- Stage AG2 initialization:
  - Reviewed `docs/uia-helper-quality-matrix.md`, `docs/watcher-preview.md`, `docs/operator-diagnostics.md`, `harness/scorecards/capture-quality.md`, `tests/test_cli.py`, `tests/test_uia_helper_contract.py`, `tests/test_watcher_events.py`, `tests/test_operator_diagnostics_docs.py`, and `tests/test_compatibility_contracts.py`.
  - Found no new helper/watcher diagnostics drift requiring product code, schema, CLI/MCP JSON, helper/watcher capture behavior, privacy storage behavior, or capture-surface changes.
- Stage AG2 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_watcher_events.py tests/test_uia_helper_quality_matrix.py tests/test_version_identity.py -q` - passed, 94 tests.
  - `python -m pytest -q` - passed, 172 tests.
  - `git diff --check` - passed.
  - stale AG0/AG1 cursor and v0.1.16 helper/watcher typo scan across
    `README.md`, `docs`, and `tests` - passed with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 172 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AG2 completion:
  - `gh pr view 163 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName` - passed; PR #163 merged at `2026-05-09T14:16:40Z` as `461eb8b14f6733f5abfe87524da2358730da3b59`.
  - `gh run view 25603218933 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #163 Windows Harness concluded `success` on `17c56a8f067988826bec965d1d7f0176f72da25e`.
  - `gh run view 25603274783 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AG2 `main` Windows Harness concluded `success` on `461eb8b14f6733f5abfe87524da2358730da3b59`.
- Stage AG3 initialization:
  - Reviewed `docs/mcp-readonly-examples.md`, `docs/deterministic-demo.md`,
    `harness/scorecards/mcp-quality.md`, `harness/scorecards/memory-quality.md`,
    `tests/test_mcp_tools.py`, `tests/test_memory_pipeline.py`,
    `harness/scripts/run_mcp_smoke.py`, `src/winchronicle/mcp/server.py`, and
    `src/winchronicle/memory.py`.
  - Found no new MCP/memory contract drift requiring product code, schema,
    CLI/MCP JSON shape, memory reducer, SQLite schema, privacy runtime, helper,
    watcher, or capture-surface changes.
- Stage AG3 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_mcp_tools.py tests/test_memory_pipeline.py tests/test_version_identity.py -q` - passed, 93 tests.
  - `python -m pytest -q` - passed, 175 tests.
  - `git diff --check` - passed.
  - stale AG2 cursor scan across `README.md`, `docs`, and `tests` - passed
    with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 175 pytest
    tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke,
    MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory,
    deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AG3 completion:
  - `gh pr view 164 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName` - passed; PR #164 merged at `2026-05-09T14:40:08Z` as `bf38d3d580fafd50ce9ea4752bca31735869083f`.
  - `gh run view 25603703247 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #164 Windows Harness concluded `success` on `e459de9587c75c6c4cd9ca23f43679907263fc8c`.
  - `gh run view 25603752386 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AG3 `main` Windows Harness concluded `success` on `bf38d3d580fafd50ce9ea4752bca31735869083f`.
- Stage AG4 initialization:
  - Reviewed `tests/test_compatibility_contracts.py`, `tests/test_mcp_tools.py`,
    `tests/test_phase6_privacy_scorecard.py`, `tests/test_watcher_events.py`,
    `tests/test_state_compatibility.py`, `tests/test_memory_pipeline.py`,
    `tests/test_privacy_check.py`, `tests/test_version_identity.py`,
    `harness/scorecards`, `docs/mcp-readonly-examples.md`,
    `docs/watcher-preview.md`, `docs/deterministic-demo.md`,
    `docs/roadmap.md`, `CONTRIBUTING.md`, `.github`, `src/winchronicle`, and
    `resources`.
  - Found no new product compatibility drift requiring schema, MCP tool-schema,
    helper/watcher output contract, capture storage shape, privacy runtime,
    capture-surface, dependency, or version-metadata changes.
  - Tightened docs/tests evidence for full disabled pass-through flag
    rejection, operator diagnostics targeted-capture flag wording, and explicit
    daemon/service/polling/background scanning.
- Stage AG4 local validation:
  - `python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py tests/test_privacy_check.py tests/test_version_identity.py -q` - passed, 55 tests.
  - Boundary scan for targeted capture, screenshot/OCR, audio, keyboard,
    clipboard, upload, LLM, control, and write/read tool terms - reviewed with
    no new product surface found.
  - Background install/polling scan for daemon, service, polling, and
    background terms - reviewed with no new product daemon/service install,
    polling capture loop, startup task, or default background capture
    implementation path found.
  - Control/capture dependency scan for foreground/control APIs, clipboard,
    screenshot capture APIs, OCR engines, LLM/network clients, Selenium, and
    Playwright - reviewed with no new runtime dependency or implementation path
    found.
  - `python -m pytest -q` - passed, 177 tests.
  - `git diff --check` - passed.
  - stale AG3 cursor scan across `README.md`, `docs`, and `tests` - passed
    with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 177 pytest
    tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke,
    MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory,
    deterministic watcher fixture, and watcher fake-helper smoke.
