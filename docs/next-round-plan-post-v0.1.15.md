# WinChronicle Post-v0.1.15 Maintenance Plan

## Summary

`v0.1.15` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.15. The release tag
targets `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`. The post-publication
reconciliation on `main` is
`54208c51819a45140e355272d8cb3f0e3fbff900`, and Windows Harness run
`25589775129` passed on that SHA.

The post-v0.1.15 baseline is green. Package/runtime/MCP version identity
reports `0.1.15`, and the previous maintenance round changed documentation,
tests, GitHub metadata evidence, deterministic harness evidence, compatibility
evidence, release-planning records, and version metadata only. It did not
change product behavior, schemas, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture surfaces.

This next round should continue blueprint-aligned maintenance without
expanding the v0.1 product boundary. The focus is evidence freshness, operator
entry clarity, helper/watcher preview diagnostics, MCP/memory contract
stability, compatibility guardrail evidence, and any small drift discovered by
those checks. It must not start Phase 6 implementation.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, no polling capture loop, and no default background capture.

## Execution Cursor

- Current stage: AD1 - Public Metadata And Evidence Freshness Follow-up.
- Stage status: A - AD1 is the active docs-only public metadata and evidence
  freshness stage.
- Last completed evidence: AD0 added this active post-v0.1.15 cursor in PR
  #135, merged as `90fff5cc25b770634c92669e70c4067b58a8a6ea`, and
  post-merge `main` Windows Harness run `25593607384` passed.
- Last validation: AD0 validated focused docs/version tests, full
  deterministic harness, PR Windows Harness run `25593554670`, and
  post-merge `main` Windows Harness run `25593607384`.
- Next atomic task: complete AD1 by adding post-v0.1.15 public metadata audit
  evidence and updating operator entry points without changing product code.
- Known blockers: none.

## Phased Work

### Stage AD0 - Post-v0.1.15 Baseline Cursor

- Add this post-v0.1.15 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Update docs tests so `v0.1.15` is the latest published release, this plan is
  the active cursor, and post-v0.1.14 is completed historical context.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, version metadata, or privacy behavior.

### Stage AD1 - Public Metadata And Evidence Freshness Follow-up

- Re-check public-facing repository evidence after `v0.1.15`: README,
  operator docs, release metadata, and GitHub repository metadata.
- Record manually maintained public metadata gaps as checklist items, not
  product-code changes.
- Refresh only documentation/tests needed to keep evidence freshness clear.
- Do not require fresh manual UIA smoke unless helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior, product
  CLI/MCP shape, capture surfaces, or release approver requirements changed.

### Stage AD2 - Helper And Watcher Preview Diagnostics Review

- Review helper and watcher preview diagnostics docs, scorecards, and tests
  against the roadmap lanes for UIA helper hardening and watcher preview.
- Strengthen documentation or deterministic tests only for discovered drift in
  timeout, malformed output, no observed-content echo, duplicate skip,
  denylist skip, heartbeat-only diagnostics, or diagnostic artifact policy.
- Keep real UIA smoke manual and outside default CI.
- Do not add helper product targeting, daemon/service install, polling capture
  loops, default background capture, screenshots, OCR, audio, keyboard,
  clipboard, network calls, LLM calls, or desktop control.

### Stage AD3 - MCP And Memory Contract Review

- Re-check read-only MCP examples, memory docs, deterministic demo guidance,
  and scorecards for trust-boundary and response-shape consistency.
- Strengthen narrow docs/tests only if examples drift from the exact read-only
  MCP tool list or durable memory contract.
- Do not add MCP write tools, arbitrary file reads, desktop control tools,
  screenshot/OCR/audio/keyboard/clipboard/network tools, or LLM
  reducer/classifier calls.

### Stage AD4 - Compatibility Guardrail Sweep

- Re-run deterministic gates and confirm the v0.1 boundary still holds.
- Treat existing tests and scorecards as compatibility oracles for version
  identity, exact read-only MCP tool list, disabled privacy surfaces, observed
  content trust boundaries, Phase 6 spec-only status, watcher preview limits,
  durable memory contract, and product targeted capture absence.
- Strengthen tests only for discovered drift.

### Stage AD5 - v0.1.16 Release Readiness

- If AD0-AD4 only change documentation, tests, CI/runtime metadata, version
  metadata, or compatible drift fixes, prepare a compatible `v0.1.16`
  maintenance release.
- Before release, align package and server version metadata to `0.1.16`, add a
  release record, and record local gates plus PR and post-merge Windows Harness
  evidence.
- If any change alters product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture surface, stop the direct
  `v0.1.16` path and prepare a release candidate instead.
- Publication remains gated on local, PR, and post-merge validation plus
  explicit release approval.

## Public Interfaces And Non-goals

- CLI remains unchanged:
  `init/status/capture-once/capture-frontmost/watch/privacy-check/search-captures/generate-memory/search-memory/mcp-stdio`.
- MCP tool list remains unchanged and read-only:
  `current_context/search_captures/search_memory/read_recent_capture/recent_activity/privacy_status`.
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

- AD0: docs tests confirm `v0.1.15` is latest published, this plan is active,
  and post-v0.1.14 is completed historical context.
- AD1: public metadata and evidence freshness follow-up separates current
  evidence from inherited/manual evidence and does not expand product scope.
- AD2: helper/watcher diagnostics evidence stays preview-only and does not add
  live UIA smoke to default CI.
- AD3: MCP/memory examples preserve exact read-only MCP tools, stable response
  shapes, and `trust = "untrusted_observed_content"`.
- AD4: compatibility guardrails still prove exact MCP read-only tools,
  disabled privacy surfaces, product targeted capture absence, and Phase 6
  spec-only status.
- AD5: release record includes local, PR, post-merge, release URL, tag target,
  rollback notes, privacy/scope confirmation, and manual smoke freshness
  decision.

## Assumptions

- `v0.1.15` is the current stable published baseline and must not be retagged.
- The next compatible release target is `v0.1.16`.
- Manual UIA smoke remains outside default CI.
- Fresh manual UIA smoke is required only if helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior,
  product CLI/MCP shape, capture surfaces, or release approver requirements
  change.
- Phase 6 stays at spec/scorecard level for this round.

## Decision Log

- Chose a compatible `v0.1.16` maintenance target because the published
  `v0.1.15` round changed documentation, tests, GitHub metadata evidence,
  deterministic harness evidence, compatibility evidence, release-planning
  records, and version metadata only, without product behavior changes.
- Chose AD0 as a docs-only active cursor so post-v0.1.15 work does not begin
  from a completed post-v0.1.14 plan.
- Chose AD1 as a docs-only public metadata audit because the repository
  metadata gaps are maintainer settings, not product-code blockers.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.

## Validation Log

- Stage AD0 initialization:
  - `gh release view v0.1.15 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt,name` - passed; `v0.1.15` is published, not a draft or prerelease, published at `2026-05-09T02:44:06Z`, and targets `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`.
  - `git rev-parse v0.1.15` - passed and printed `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`.
  - `gh run view 25589775129 --json databaseId,status,conclusion,headSha,url,displayTitle` - passed; post-publication reconciliation `main` Windows Harness concluded `success` on `54208c51819a45140e355272d8cb3f0e3fbff900`.
  - `git rev-parse HEAD` - passed and printed `54208c51819a45140e355272d8cb3f0e3fbff900`.
  - `python -c "import winchronicle; print(winchronicle.__version__)"` - passed and printed `0.1.15`.
- Stage AD0 completion:
  - PR #135 Windows Harness run `25593554670` - passed.
  - PR #135 merged as `90fff5cc25b770634c92669e70c4067b58a8a6ea`.
  - `gh run view 25593607384 --json databaseId,status,conclusion,headSha,url,displayTitle` - passed; post-AD0 `main` Windows Harness concluded `success` on `90fff5cc25b770634c92669e70c4067b58a8a6ea`.
- Stage AD1 initialization:
  - `gh repo view YSCJRH/WinChronicle --json nameWithOwner,visibility,defaultBranchRef,description,homepageUrl,repositoryTopics,url` - passed; repository is public on `main`, with empty description, homepage, and topics.
  - `gh release view v0.1.15 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt,name` - passed; `v0.1.15` is published, not a draft or prerelease, and targets `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`.
- Stage AD1 local validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed; 48 tests passed.
  - `python harness/scripts/run_harness.py` - passed; includes 139 pytest tests, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search/memory, and preview watcher smoke.
  - `git diff --check` - passed.
