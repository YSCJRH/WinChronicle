# WinChronicle Post-v0.1.14 Maintenance Plan

## Summary

`v0.1.14` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.14. The release tag
targets `e7e339f4e08828b9954599db76b87201dbcb139b`. The post-publication
reconciliation on `main` is
`2627e17dd215d3b7233d237ca5f094eacaff2983`, and Windows Harness run
`25585707220` passed on that SHA.

The post-v0.1.14 baseline is green. Package/runtime/MCP version identity
reports `0.1.14`, and the previous maintenance round changed documentation,
tests, GitHub metadata evidence, deterministic harness evidence, compatibility
evidence, release-planning records, and version metadata only. It did not
change product behavior, schemas, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture surfaces.

This next round should continue blueprint-aligned hardening without expanding
the v0.1 product boundary. The focus is evidence freshness, operator entry
clarity, helper/watcher preview diagnostics, MCP/memory contract stability, and
compatibility guardrail evidence. It must not start Phase 6 implementation.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, no polling capture loop, and no default background capture.

## Execution Cursor

- Current stage: G - v0.1.15 Published Baseline Reconciliation.
- Stage status: G - `v0.1.15` published; baseline reconciliation is in
  progress on `main`.
- Last completed evidence: `v0.1.14` is published at
  https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.14, targets
  `e7e339f4e08828b9954599db76b87201dbcb139b`, publication reconciliation PR
  #126 merged as `2627e17dd215d3b7233d237ca5f094eacaff2983`, AC4 PR #131
  merged as `48994134a3d348745f735e2a6fad56ea82495266`, and post-merge
  `main` Windows Harness run `25588297846` passed. AC5 PR #132 merged as
  `7a7f065817b9d7f660248916935fd7b66fadbdd6`, and post-merge `main` Windows
  Harness run `25588898702` passed. AC5 evidence PR #133 merged as
  `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`, and `v0.1.15` was published
  at https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.15 targeting
  `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`.
- Last validation: AC5 local validation passed with focused docs/version
  pytest, full pytest, helper build, watcher build, install CLI smoke, full
  harness, runtime version check, `git diff --check`, PR Windows Harness run
  `25588833988`, post-merge `main` Windows Harness run `25588898702`, release
  URL https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.15, tag target
  `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`, and latest `main` Windows
  Harness run `25589165182`.
- Next atomic task: open the `v0.1.15` publication reconciliation PR, verify
  PR and post-merge Windows Harness, then establish the post-v0.1.15
  maintenance cursor before starting new implementation work.
- Known blockers: none.

## Phased Work

### Stage AC0 - Post-v0.1.14 Baseline Cursor

- Add this post-v0.1.14 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Update docs tests so `v0.1.14` is the latest published release, this plan is
  the active cursor, and post-v0.1.13 is completed historical context.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, version metadata, or privacy behavior.

### Stage AC1 - Public Metadata And Evidence Freshness Follow-up

- Re-check public-facing repository evidence after `v0.1.14`: README,
  operator docs, release metadata, and GitHub repository metadata.
- Record manually maintained public metadata gaps as checklist items, not
  product-code changes.
- Refresh only documentation/tests needed to keep evidence freshness clear.
- Do not require fresh manual UIA smoke unless helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior, product
  CLI/MCP shape, capture surfaces, or release approver requirements changed.

### Stage AC2 - Helper And Watcher Preview Diagnostics Review

- Review helper and watcher preview diagnostics docs, scorecards, and tests
  against the roadmap lanes for UIA helper hardening and watcher preview.
- Strengthen documentation or deterministic tests only for discovered drift in
  timeout, malformed output, no observed-content echo, duplicate skip,
  denylist skip, heartbeat-only diagnostics, or diagnostic artifact policy.
- Keep real UIA smoke manual and outside default CI.
- Do not add helper product targeting, daemon/service install, polling capture
  loops, default background capture, screenshots, OCR, audio, keyboard,
  clipboard, network calls, LLM calls, or desktop control.

### Stage AC3 - MCP And Memory Contract Review

- Re-check read-only MCP examples, memory docs, deterministic demo guidance,
  and scorecards for trust-boundary and response-shape consistency.
- Strengthen narrow docs/tests only if examples drift from the exact read-only
  MCP tool list or durable memory contract.
- Do not add MCP write tools, arbitrary file reads, desktop control tools,
  screenshot/OCR/audio/keyboard/clipboard/network tools, or LLM
  reducer/classifier calls.

### Stage AC4 - Compatibility Guardrail Sweep

- Re-run deterministic gates and confirm the v0.1 boundary still holds.
- Treat existing tests and scorecards as compatibility oracles for version
  identity, exact read-only MCP tool list, disabled privacy surfaces, observed
  content trust boundaries, Phase 6 spec-only status, watcher preview limits,
  durable memory contract, and product targeted capture absence.
- Strengthen tests only for discovered drift.

### Stage AC5 - v0.1.15 Release Readiness

- If AC0-AC4 only change documentation, tests, CI/runtime metadata, version
  metadata, or compatible drift fixes, prepare a compatible `v0.1.15`
  maintenance release.
- Before release, align package and server version metadata to `0.1.15`, add a
  release record, and record local gates plus PR and post-merge Windows Harness
  evidence.
- If any change alters product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture surface, stop the direct
  `v0.1.15` path and prepare a release candidate instead.
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

- AC0: docs tests confirm `v0.1.14` is latest published, this plan is active,
  and post-v0.1.13 is completed historical context.
- AC1: public metadata and evidence freshness follow-up separates current
  evidence from inherited/manual evidence and does not expand product scope.
- AC2: helper/watcher diagnostics evidence stays preview-only and does not add
  live UIA smoke to default CI.
- AC3: MCP/memory examples preserve exact read-only MCP tools, stable response
  shapes, and `trust = "untrusted_observed_content"`.
- AC4: compatibility guardrails still prove exact MCP read-only tools,
  disabled privacy surfaces, product targeted capture absence, and Phase 6
  spec-only status.
- AC5: release record includes local, PR, post-merge, release URL, tag target,
  rollback notes, privacy/scope confirmation, and manual smoke freshness
  decision.

## Assumptions

- `v0.1.14` is the current stable published baseline and must not be retagged.
- The next compatible release target is `v0.1.15`.
- Manual UIA smoke remains outside default CI.
- Fresh manual UIA smoke is required only if helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior,
  product CLI/MCP shape, capture surfaces, or release approver requirements
  change.
- Phase 6 stays at spec/scorecard level for this round.

## Decision Log

- Chose a compatible `v0.1.15` maintenance target because the published
  `v0.1.14` round changed documentation, tests, GitHub metadata evidence,
  deterministic harness evidence, compatibility evidence, release-planning
  records, and version metadata only, without product behavior changes.
- Chose AC0 as a docs-only active cursor so post-v0.1.14 work does not begin
  from a completed post-v0.1.13 plan.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.

## Validation Log

- Stage AC0 initialization:
  - `gh release view v0.1.14 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt,name` - passed; `v0.1.14` is published, not a draft or prerelease, published at `2026-05-08T23:52:43Z`, and targets `e7e339f4e08828b9954599db76b87201dbcb139b`.
  - `git rev-parse v0.1.14` - passed and printed `e7e339f4e08828b9954599db76b87201dbcb139b`.
  - `gh run view 25585707220 --json databaseId,status,conclusion,headSha,url,displayTitle` - passed; post-publication reconciliation `main` Windows Harness concluded `success` on `2627e17dd215d3b7233d237ca5f094eacaff2983`.
  - `git rev-parse HEAD` - passed and printed `2627e17dd215d3b7233d237ca5f094eacaff2983`.
  - `python -c "import winchronicle; print(winchronicle.__version__)"` - passed and printed `0.1.14`.
- Stage AC0 local validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 41 tests.
  - `python -m pytest -q` - passed, 132 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage AC0 remote validation:
  - PR #127 Windows Harness run `25586296541` - passed.
  - PR #127 merged as `42ce9658b0189d37f2e7c80e1b57205ca13cb23e`.
  - Post-merge `main` Windows Harness run `25586359016` - passed.
- Stage AC1 initialization:
  - `gh repo view YSCJRH/WinChronicle --json nameWithOwner,visibility,defaultBranchRef,description,homepageUrl,repositoryTopics,url` - passed; repository is public on `main`, description and homepage are empty, and topics are empty or not configured.
  - `gh release view v0.1.14 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt,name` - passed; release is published, not draft or prerelease, and targets `e7e339f4e08828b9954599db76b87201dbcb139b`.
- Stage AC1 local validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 42 tests.
  - `python -m pytest -q` - passed, 133 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage AC1 remote validation:
  - PR #128 Windows Harness run `25586734181` - passed.
  - PR #128 merged as `157b9e195c5de85588c0df24130bbf99f10c4111`.
  - Post-merge `main` Windows Harness run `25586802404` - passed.
- Stage AC2 initialization:
  - Reviewed `docs/uia-helper-quality-matrix.md`, `docs/watcher-preview.md`, `docs/operator-diagnostics.md`, `harness/scorecards/capture-quality.md`, `tests/test_cli.py`, `tests/test_uia_helper_contract.py`, and `tests/test_watcher_events.py`.
  - `rg "helper timed out|helper returned invalid JSON|helper failed with exit code|watcher failed with exit code|watcher JSONL line|watcher timed out|duplicates_skipped|denylisted_skipped|raw watcher JSONL|capture-on-start|ElementNotAvailable|uia_stats" tests docs harness/scorecards` - passed; deterministic helper/watcher diagnostics coverage is present in tests, docs, and scorecards.
- Stage AC2 local validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 43 tests.
  - `python -m pytest -q` - passed, 134 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage AC2 remote validation:
  - PR #129 Windows Harness run `25587197634` - passed.
  - PR #129 merged as `7d65cbbb4778f5cf253191c2d3da1e21c54b7b58`.
  - Post-merge `main` Windows Harness run `25587281619` - passed.
- Stage AC3 initialization:
  - Reviewed `docs/mcp-readonly-examples.md`, `harness/scorecards/mcp-quality.md`, `harness/scorecards/memory-quality.md`, `docs/deterministic-demo.md`, `docs/operator-quickstart.md`, `tests/test_mcp_tools.py`, `tests/test_memory_pipeline.py`, `tests/test_compatibility_contracts.py`, and `tests/test_state_compatibility.py`.
  - `rg -n "current_context|search_captures|search_memory|read_recent_capture|recent_activity|privacy_status|untrusted_observed_content|entries_fts|idempotent|No write/control/file/screenshot/OCR/audio/keyboard/clipboard/network" docs harness tests src` - passed; deterministic MCP/memory trust-boundary and exact-tool coverage is present in tests, scorecards, docs, and source contracts.
- Stage AC3 local validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 44 tests.
  - `python -m pytest -q` - passed, 135 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage AC3 remote validation:
  - PR #130 Windows Harness run `25587827078` - passed.
  - PR #130 merged as `79637edd43ac15b425d5a2600a61472c9e27e031`.
  - Post-merge `main` Windows Harness run `25587885292` - passed.
- Stage AC4 initialization:
  - `python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py tests/test_version_identity.py -q` - passed, 45 tests.
  - `rg -n -e "--hwnd|--pid|--window-title|--window-title-regex|--process-name|screenshot|ocr|audio|keyboard|clipboard|network_upload|cloud_upload|llm_calls|desktop_control|write_memory|read_file|click|type" src/winchronicle tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py harness/scorecards docs/mcp-readonly-examples.md docs/watcher-preview.md docs/deterministic-demo.md docs/roadmap.md CONTRIBUTING.md .github` - reviewed; matches are existing disabled-surface contracts, sentinels, documentation, scorecards, deterministic fixtures/tests, schema field names, or allowed helper-only harness wording.
  - `rg -n -g "*.py" -g "*.cs" -g "*.md" -g "*.json" -g "*.yml" -e "SetForegroundWindow|AttachThreadInput|SendInput|mouse_event|keybd_event|GetAsyncKeyState|OpenClipboard|GetClipboardData|BitBlt|CopyFromScreen|PrintWindow|Tesseract|OpenAI|Anthropic|requests|httpx|aiohttp|selenium|playwright" src resources tests harness .github docs CONTRIBUTING.md README.md` - reviewed; matches are prior compatibility sweep command text, historical plan evidence, privacy-policy canary text, deterministic fixture/golden content, explicit forbidden-term tests, and the local MCP smoke request variable name.
- Stage AC4 local validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 45 tests.
  - `python -m pytest -q` - passed, 136 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage AC4 remote validation:
  - PR #131 Windows Harness run `25588225151` - passed.
  - PR #131 merged as `48994134a3d348745f735e2a6fad56ea82495266`.
  - Post-merge `main` Windows Harness run `25588297846` - passed.
- Stage AC5 initialization:
  - `gh release view v0.1.15 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt,name` - confirmed release not found before AC5 readiness.
- Stage AC5 local validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 46 tests.
  - `python -m pytest -q` - passed, 137 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `python -c "import winchronicle; print(winchronicle.__version__)"` - passed and printed `0.1.15`.
  - `git diff --check` - passed.
- Stage AC5 remote validation:
  - PR #132 Windows Harness run `25588833988` - passed.
  - PR #132 merged as `7a7f065817b9d7f660248916935fd7b66fadbdd6`.
  - Post-merge `main` Windows Harness run `25588898702` - passed.
  - PR #133 Windows Harness run `25589110606` - passed.
  - PR #133 merged as `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`.
  - Post-merge `main` Windows Harness run `25589165182` - passed.
- Stage AC5 publication validation:
  - `gh release create v0.1.15 --target 4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2` - passed after explicit release approval.
  - `gh release view v0.1.15 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt,name` - passed; `v0.1.15` is published, not a draft or prerelease, published at `2026-05-09T02:44:06Z`, and targets `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`.
  - `git rev-parse v0.1.15` - passed and printed `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`.
