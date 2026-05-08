# WinChronicle Post-v0.1.13 Maintenance Plan

## Summary

`v0.1.13` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.13. The release tag
targets `1070343d9bcfd60c48238835e26b6c32f9060ae7`. The post-publication
reconciliation on `main` is
`f4781a91f2120f3eca5088b87bf9034be752274f`, and Windows Harness run
`25581662790` passed on that SHA.

The post-v0.1.13 baseline is green. Package/runtime/MCP version identity
reports `0.1.13`, and the previous maintenance round changed documentation,
tests, GitHub metadata, deterministic demo/operator guidance, release
evidence, compatibility evidence, and version metadata only. It did not change
product behavior, schemas, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture surfaces.

This next round should continue blueprint-aligned hardening without expanding
the v0.1 product boundary. The focus is operator evidence freshness, public
surface metadata, helper/watcher preview diagnostics, MCP/memory example
stability, and compatibility guardrail evidence. It must not start Phase 6
implementation.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, no polling capture loop, and no default background capture.

## Execution Cursor

- Current stage: AB0 - Post-v0.1.13 Baseline Cursor.
- Stage status: B - AB0 baseline cursor docs/tests and local validation are
  complete; PR Windows Harness and post-merge Windows Harness are pending.
- Last completed evidence: `v0.1.13` is published at
  https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.13, targets
  `1070343d9bcfd60c48238835e26b6c32f9060ae7`, publication reconciliation PR
  #119 merged as `f4781a91f2120f3eca5088b87bf9034be752274f`, and post-merge
  `main` Windows Harness run `25581662790` passed on that SHA.
- Last validation: AB0 local validation passed with focused docs/version tests,
  full pytest, helper build, watcher build, install CLI smoke, full harness,
  and `git diff --check`.
- Next atomic task: open the AB0 baseline cursor PR, verify PR and post-merge
  Windows Harness, then continue to AB1.
- Known blockers: none.

## Phased Work

### Stage AB0 - Post-v0.1.13 Baseline Cursor

- Add this post-v0.1.13 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Update docs tests so `v0.1.13` is the latest published release, this plan is
  the active cursor, and post-v0.1.12 is completed historical context.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, version metadata, or privacy behavior.

### Stage AB1 - Public Metadata And Evidence Freshness Audit

- Audit README/operator/release docs against the blueprint public-facing
  positioning and the current GitHub release evidence.
- Record any manually maintained repository metadata or social-surface gaps as
  checklist items, not product code.
- Refresh only documentation/tests needed to keep evidence freshness clear.
- Do not require fresh manual UIA smoke unless helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior,
  product CLI/MCP shape, capture surfaces, or release approver requirements
  changed.

### Stage AB2 - Helper And Watcher Preview Diagnostics Evidence

- Review helper and watcher preview diagnostics docs, scorecards, and tests
  against the roadmap lanes for UIA helper hardening and watcher preview.
- Strengthen documentation or deterministic tests only for discovered drift in
  timeout, malformed output, no observed-content echo, duplicate skip,
  denylist skip, or diagnostic artifact policy.
- Keep real UIA smoke manual and outside default CI.
- Do not add helper product targeting, daemon/service install, polling capture
  loops, default background capture, screenshots, OCR, audio, keyboard,
  clipboard, network calls, LLM calls, or desktop control.

### Stage AB3 - MCP And Memory Operator Contract Sweep

- Re-check read-only MCP examples, memory docs, and deterministic demo
  guidance for trust-boundary and response-shape consistency.
- Strengthen narrow docs/tests only if examples drift from the exact read-only
  MCP tool list or durable memory contract.
- Do not add MCP write tools, arbitrary file reads, desktop control tools,
  screenshot/OCR/audio/keyboard/clipboard/network tools, or LLM
  reducer/classifier calls.

### Stage AB4 - Compatibility Guardrail Sweep

- Re-run deterministic gates and confirm the v0.1 boundary still holds.
- Treat existing tests and scorecards as compatibility oracles for version
  identity, exact read-only MCP tool list, disabled privacy surfaces, observed
  content trust boundaries, Phase 6 spec-only status, watcher preview limits,
  durable memory contract, and product targeted capture absence.
- Strengthen tests only for discovered drift.

### Stage AB5 - v0.1.14 Release Readiness

- If AB0-AB4 only change documentation, tests, CI/runtime metadata, version
  metadata, or compatible drift fixes, prepare a compatible `v0.1.14`
  maintenance release.
- Before release, align package and server version metadata to `0.1.14`, add a
  release record, and record local gates plus PR and post-merge Windows
  Harness evidence.
- If any change alters product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture surface, stop the direct
  `v0.1.14` path and prepare a release candidate instead.
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

- AB0: docs tests confirm `v0.1.13` is latest published, this plan is active,
  and post-v0.1.12 is completed historical context.
- AB1: public metadata and evidence freshness audit separates current evidence
  from inherited/manual evidence and does not expand product scope.
- AB2: helper/watcher diagnostics evidence stays preview-only and does not add
  live UIA smoke to default CI.
- AB3: MCP/memory examples preserve exact read-only MCP tools, stable response
  shapes, and `trust = "untrusted_observed_content"`.
- AB4: compatibility guardrails still prove exact MCP read-only tools,
  disabled privacy surfaces, product targeted capture absence, and Phase 6
  spec-only status.
- AB5: release record includes local, PR, post-merge, release URL, tag target,
  rollback notes, privacy/scope confirmation, and manual smoke freshness
  decision.

## Assumptions

- `v0.1.13` is the current stable published baseline and must not be retagged.
- The next compatible release target is `v0.1.14`.
- Manual UIA smoke remains outside default CI.
- Fresh manual UIA smoke is required only if helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior,
  product CLI/MCP shape, capture surfaces, or release approver requirements
  change.
- Phase 6 stays at spec/scorecard level for this round.

## Decision Log

- Chose a compatible `v0.1.14` maintenance target because the published
  `v0.1.13` round changed documentation, tests, GitHub metadata,
  deterministic harness evidence, compatibility evidence, release-planning
  records, and version metadata only, without product behavior changes.
- Chose AB0 as a docs-only active cursor so post-v0.1.13 work does not begin
  from a completed post-v0.1.12 plan.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.

## Validation Log

- Stage AB0 initialization:
  - `gh release view v0.1.13 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; `v0.1.13` is published and targets `1070343d9bcfd60c48238835e26b6c32f9060ae7`.
  - `git rev-parse v0.1.13` - passed and printed `1070343d9bcfd60c48238835e26b6c32f9060ae7`.
  - `gh run view 25581662790 --json databaseId,status,conclusion,headSha,url,displayTitle` - passed; post-publication reconciliation `main` Windows Harness concluded `success`.
  - `python -c "import winchronicle; print(winchronicle.__version__)"` - passed and printed `0.1.13`.
- Stage AB0 local validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 35 tests.
  - `python -m pytest -q` - passed, 126 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Pending AB0 PR Windows Harness.
- Pending AB0 post-merge `main` Windows Harness.
