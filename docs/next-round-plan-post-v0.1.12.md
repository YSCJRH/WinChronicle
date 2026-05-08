# WinChronicle Post-v0.1.12 Maintenance Plan

## Summary

`v0.1.12` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.12. The release tag
targets `df16ea301243e2d3a612a5d09bd59f1436723fb4`. The post-publication
reconciliation on `main` is
`3164d185e5d203b504bd78432032fa13003983f8`, and Windows Harness run
`25577701036` passed on that SHA.

The post-v0.1.12 baseline is green. Package/runtime/MCP version identity
reports `0.1.12`, and the previous maintenance round changed release evidence,
operator docs, tests, and version metadata only. It did not change product
behavior, schemas, CLI/MCP JSON shape, privacy behavior, helper/watcher
behavior, or capture surfaces.

This next round should move beyond release-record bookkeeping without
expanding the product boundary. The focus is a blueprint gap audit, public
surface hygiene, deterministic demo/operator documentation, and compatibility
guardrail evidence. It must not start Phase 6 implementation.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, and no default background capture.

## Execution Cursor

- Current stage: G - v0.1.13 Published Baseline Reconciliation.
- Stage status: G - `v0.1.13` published; baseline reconciliation complete.
- Last completed evidence: publication reconciliation PR #119 passed PR Windows
  Harness run `25581510176`, merged as
  `f4781a91f2120f3eca5088b87bf9034be752274f`, and post-merge `main` Windows
  Harness run `25581662790` passed on that SHA.
- Last validation: v0.1.13 publication reconciliation validation passed with
  local deterministic gates, PR Windows Harness, and post-merge `main` Windows
  Harness.
- Next atomic task: follow the post-v0.1.13 maintenance plan before starting
  new implementation work.
- Known blockers: none.

## Phased Work

### Stage AA0 - Post-v0.1.12 Baseline Cursor

- Add this post-v0.1.12 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Update docs tests so `v0.1.12` is the latest published release, this plan is
  the active cursor, and post-v0.1.11 is completed historical context.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, version metadata, or privacy behavior.

### Stage AA1 - Blueprint Gap And Public Surface Audit

- Compare the implemented v0.1 surface against `WinChronicle.md` sections on
  north star, README positioning, demo route, issue templates, roadmap, MCP,
  memory, watcher, and Phase 6 boundaries.
- Record gaps as documentation or test follow-up candidates, separating
  evidence from inference.
- Strengthen narrow docs tests only where current docs drift from the published
  product boundary.
- Do not implement new helper/watcher/product capture behavior.

### Stage AA2 - Deterministic Demo And Operator Experience Refresh

- Refresh deterministic demo instructions around fixture capture, search,
  memory generation, read-only MCP smoke, watcher preview, and privacy status.
- Prefer existing fixture and harness paths; do not add live UIA smoke to
  default CI.
- Ensure demo docs do not ask operators to commit observed-content artifacts.
- Do not add screenshots, OCR, audio, keyboard capture, clipboard capture,
  network calls, LLM calls, or desktop control.

### Stage AA3 - Issue, Roadmap, And Contribution Hygiene

- Add or refresh lightweight roadmap/issue guidance that maps to the blueprint:
  fixtures/privacy, UIA helper hardening, watcher preview, MCP read-only,
  memory pipeline, docs/demo, and Phase 6 spec-only work.
- Keep contribution guidance scoped to harness-first work and explicit privacy
  boundaries.
- Do not create tasks that imply default screenshot/OCR, audio, keyboard,
  clipboard, network upload, LLM reducer, desktop control, daemon/service
  install, or product targeted capture.

### Stage AA4 - Compatibility Guardrail Sweep

- Re-run deterministic gates and confirm the v0.1 boundary still holds.
- Treat existing tests and scorecards as compatibility oracles for version
  identity, exact read-only MCP tool list, disabled privacy surfaces, observed
  content trust boundaries, Phase 6 spec-only status, watcher preview limits,
  and product targeted capture absence.
- Strengthen tests only for discovered drift.

### Stage AA5 - v0.1.13 Release Readiness

- If AA0-AA4 only change documentation, tests, CI/runtime metadata, version
  metadata, or compatible drift fixes, prepare a compatible `v0.1.13`
  maintenance release.
- Before release, align package and server version metadata to `0.1.13`, add a
  release record, and record local gates plus PR and post-merge Windows
  Harness evidence.
- If any change alters product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture surface, stop the direct
  `v0.1.13` path and prepare a release candidate instead.
- Publication remains gated on local, PR, and post-merge validation.

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

- AA0: docs tests confirm `v0.1.12` is latest published, this plan is active,
  and post-v0.1.11 is completed historical context.
- AA1: blueprint gap audit separates evidence from inference and does not
  expand product scope.
- AA2: demo/operator docs rely on deterministic fixture/harness paths and do
  not require observed-content artifacts.
- AA3: issue/roadmap guidance preserves harness-first and privacy boundaries.
- AA4: compatibility guardrails still prove exact MCP read-only tools,
  disabled privacy surfaces, product targeted capture absence, and Phase 6
  spec-only status.
- AA5: release record includes local, PR, post-merge, release URL, tag target,
  rollback notes, privacy/scope confirmation, and manual smoke freshness
  decision.

## Assumptions

- `v0.1.12` is the current stable published baseline and must not be retagged.
- The next compatible release target is `v0.1.13`.
- Manual UIA smoke remains outside default CI.
- Fresh manual UIA smoke is required only if helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior,
  product CLI/MCP shape, capture surfaces, or release approver requirements
  change.
- Phase 6 stays at spec/scorecard level for this round.

## Decision Log

- Chose a compatible `v0.1.13` maintenance target because the published
  `v0.1.12` round changed release evidence, docs, tests, CI/runtime metadata,
  deterministic harness evidence, compatibility evidence, and version metadata
  only, without product behavior changes.
- Chose AA0 as a docs-only active cursor so post-v0.1.12 work does not begin
  from a completed post-v0.1.11 plan.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.
- Recorded AA0 PR #113 and post-merge Windows Harness run `25578252392` as the
  post-v0.1.12 baseline cursor completion evidence.
- During AA1, found no required product-code change. The concrete gaps are
  deterministic public demo consolidation, public roadmap, issue templates,
  harness-first contribution entry, manual smoke freshness tracking, and
  manually maintained GitHub metadata/social surface.
- Recorded AA1 PR #114 and post-merge Windows Harness run `25578855299` as the
  blueprint gap audit completion evidence.
- During AA2, consolidated the deterministic public demo into a fixture-only
  operator path that covers capture search, memory generation/search, watcher
  fixture replay, read-only MCP smoke, privacy status, and artifact policy
  without adding live UIA smoke to default CI.
- Recorded AA2 PR #115 and post-merge Windows Harness run `25579389224` as the
  deterministic demo completion evidence.
- During AA3, added lightweight roadmap, contribution guidance, issue templates,
  and a PR template that route work through harness-first lanes and repeat the
  v0.1 privacy/scope boundaries without creating product behavior work.
- Recorded AA3 PR #116 and post-merge Windows Harness run `25579869673` as the
  issue/roadmap/contribution hygiene completion evidence.
- During AA4, treated existing compatibility tests and scorecards as the
  authoritative guardrails. The focused tests and scans found no drift requiring
  product code, schema, CLI/MCP shape, helper/watcher behavior, or privacy
  behavior changes.
- Recorded AA4 PR #117 and post-merge Windows Harness run `25580333158` as the
  compatibility guardrail sweep completion evidence.
- During AA5, chose the direct compatible `v0.1.13` path because AA0-AA4 changed
  documentation, tests, GitHub metadata, deterministic harness evidence,
  compatibility evidence, and release-planning records only. AA5 changes
  release documentation, tests, and version metadata only.
- During AA5, aligned package, runtime, and MCP server version identity to
  `0.1.13`.
- During AA5, the `v0.1.13` release-readiness record accepts inherited
  `v0.1.0` manual UIA smoke for the compatible `v0.1.13` path only because
  helper behavior, watcher product behavior, manual smoke scripts, capture
  behavior, privacy behavior, product CLI/MCP shape, release approver
  requirements, and capture surfaces are unchanged.
- AA5 PR #118 passed PR Windows Harness run `25580778260`, merged as
  `1070343d9bcfd60c48238835e26b6c32f9060ae7`, and post-merge `main` Windows
  Harness run `25580877004` passed.
- Published `v0.1.13` from `1070343d9bcfd60c48238835e26b6c32f9060ae7`. Do not
  retag `v0.1.13`; establish a post-v0.1.13 maintenance plan before starting
  new implementation work.
- Reconciled `v0.1.13` publication evidence in PR #119, merged as
  `f4781a91f2120f3eca5088b87bf9034be752274f`. This closes the post-v0.1.12
  maintenance round.

## Validation Log

- Stage AA0 initialization:
  - `gh release view v0.1.12 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; `v0.1.12` is published and targets `df16ea301243e2d3a612a5d09bd59f1436723fb4`.
  - `git rev-parse v0.1.12` - passed and printed `df16ea301243e2d3a612a5d09bd59f1436723fb4`.
  - `gh run view 25577701036 --json databaseId,status,conclusion,headSha,url,displayTitle,jobs` - passed; post-publication `main` Windows Harness concluded `success`.
  - `python -c "import winchronicle; print(winchronicle.__version__)"` - passed and printed `0.1.12`.
- Stage AA0 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 29 tests.
  - `python -m pytest -q` - passed, 120 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage AA0 remote validation:
  - PR #113 Windows Harness run `25578139342` - passed.
  - PR #113 merged as `4a5c5d53d9a6981e81a3ba61625cea847a87d88f`.
  - Post-merge `main` Windows Harness run `25578252392` - passed on
    `4a5c5d53d9a6981e81a3ba61625cea847a87d88f`.
- Stage AA1 blueprint gap audit validation:
  - `rg -n "def main|subparsers|add_parser|capture-frontmost|mcp-stdio|search-memory|generate-memory|watch" src\winchronicle` - reviewed CLI evidence.
  - `rg -n "TOOL_NAMES|current_context|search_captures|search_memory|privacy_status|read_recent_capture|recent_activity" src\winchronicle\mcp tests\test_mcp_tools.py` - reviewed MCP evidence.
  - `rg --files .github docs harness` - reviewed workflow/docs/harness surfaces.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 16 tests.
  - `python -m pytest -q` - passed, 121 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage AA1 remote validation:
  - PR #114 Windows Harness run `25578768178` - passed.
  - PR #114 merged as `b5b5bd7725c47f85fd4811eee3b5798577621e53`.
  - Post-merge `main` Windows Harness run `25578855299` - passed on
    `b5b5bd7725c47f85fd4811eee3b5798577621e53`.
- Stage AA2 deterministic demo validation:
  - First `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` attempt failed because the AA2 cursor assertions still expected an AA1-only evidence phrase; the assertion was corrected to the AA2 cursor.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 17 tests.
  - `python -m pytest -q` - passed, 122 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage AA2 remote validation:
  - PR #115 Windows Harness run `25579283981` - passed.
  - PR #115 merged as `96a5e9145765375818e5b2dc0cb1792f83b7fc0e`.
  - Post-merge `main` Windows Harness run `25579389224` - passed on
    `96a5e9145765375818e5b2dc0cb1792f83b7fc0e`.
- Stage AA3 issue/roadmap/contribution validation:
  - First `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` attempt failed because the new roadmap assertion expected a phrase that was implicit in the definition-of-done list; the roadmap now states the artifact rule explicitly.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 18 tests.
  - `python -m pytest -q` - passed, 123 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage AA3 remote validation:
  - PR #116 Windows Harness run `25579782185` - passed.
  - PR #116 merged as `8da0ba6dd111cfc16170284cb4e7787819d3a67e`.
  - Post-merge `main` Windows Harness run `25579869673` - passed on
    `8da0ba6dd111cfc16170284cb4e7787819d3a67e`.
- Stage AA4 compatibility guardrail sweep:
  - `python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py tests/test_version_identity.py -q` - passed, 45 tests.
  - `rg -n -e "--hwnd|--pid|--window-title|--window-title-regex|--process-name|screenshot|ocr|audio|keyboard|clipboard|network_upload|cloud_upload|llm_calls|desktop_control|write_memory|read_file|click|type" src\winchronicle tests\test_compatibility_contracts.py tests\test_mcp_tools.py tests\test_phase6_privacy_scorecard.py tests\test_watcher_events.py tests\test_state_compatibility.py tests\test_memory_pipeline.py harness\scorecards docs\mcp-readonly-examples.md docs\watcher-preview.md docs\deterministic-demo.md docs\roadmap.md CONTRIBUTING.md .github` - reviewed; matches are existing disabled-surface contracts, sentinels, docs, tests, scorecards, fixture fields, and helper-only harness wording rather than new product capabilities.
  - `rg -n -g "*.py" -g "*.cs" -g "*.md" -g "*.json" -g "*.yml" -e "SetForegroundWindow|AttachThreadInput|SendInput|mouse_event|keybd_event|GetAsyncKeyState|OpenClipboard|GetClipboardData|BitBlt|CopyFromScreen|PrintWindow|Tesseract|OpenAI|Anthropic|requests|httpx|aiohttp|selenium|playwright" src resources tests harness .github docs CONTRIBUTING.md README.md` - reviewed; matches are historical plan evidence, privacy-policy canary text, deterministic fixture/golden content, explicit forbidden-term tests, and the local MCP smoke request variable name rather than new runtime dependencies or implementations.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 19 tests.
  - `python -m pytest -q` - passed, 124 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage AA4 remote validation:
  - PR #117 Windows Harness run `25580215098` - passed.
  - PR #117 merged as `1c9cabec4d27b8c0e4e245d9a27ddcba96ed3a00`.
  - Post-merge `main` Windows Harness run `25580333158` - passed on
    `1c9cabec4d27b8c0e4e245d9a27ddcba96ed3a00`.
- Stage AA5 release-readiness validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 34 tests.
  - `python -m pytest -q` - passed, 125 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage AA5 remote validation:
  - PR #118 Windows Harness run `25580778260` - passed.
  - PR #118 merged as `1070343d9bcfd60c48238835e26b6c32f9060ae7`.
  - Post-merge `main` Windows Harness run `25580877004` - passed on
    `1070343d9bcfd60c48238835e26b6c32f9060ae7`.
- v0.1.13 publication validation:
  - `gh release create v0.1.13 --target 1070343d9bcfd60c48238835e26b6c32f9060ae7 --title "v0.1.13" --notes <inline release notes>` - passed.
  - `gh release view v0.1.13 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; release URL https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.13, not draft, not prerelease, published at `2026-05-08T21:42:32Z`, and target `1070343d9bcfd60c48238835e26b6c32f9060ae7`.
  - `git fetch --tags origin; git rev-parse v0.1.13` - passed and printed `1070343d9bcfd60c48238835e26b6c32f9060ae7`.
  - `python -c "import winchronicle; print(winchronicle.__version__)"` - passed and printed `0.1.13`.
- v0.1.13 publication reconciliation local validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 34 tests.
  - `python -m pytest -q` - passed, 125 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- v0.1.13 publication reconciliation remote validation:
  - PR #119 Windows Harness run `25581510176` - passed.
  - PR #119 merged as `f4781a91f2120f3eca5088b87bf9034be752274f`.
  - Post-merge `main` Windows Harness run `25581662790` - passed on
    `f4781a91f2120f3eca5088b87bf9034be752274f`.
