# WinChronicle Post-v0.1.9 Maintenance Plan

## Summary

`v0.1.9` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.9. The release tag
targets `d06ab5bc8bea7520bac2719adb457794c72911d3`, and post-merge `main`
Windows Harness run `25565697723` passed on that SHA.

The post-v0.1.9 baseline starts from the compatible `v0.1.9` maintenance
release. `main` is green, package/runtime/MCP version identity reports
`0.1.9`, and no product behavior, schema, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture-surface change was introduced by the
post-v0.1.8 round.

This next round is a conservative compatible maintenance pass. It should keep
release evidence current, preserve operator entry points, audit inherited
manual smoke freshness, and maintain compatibility guardrails. It must not
expand the capture surface or start Phase 6 implementation.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, and no default background capture.

## Execution Cursor

- Current stage: X3 - Compatibility Guardrail Sweep.
- Stage status: B - X3 compatibility guardrail docs/tests are implemented and
  local deterministic validation passed; PR Windows Harness and post-merge
  Windows Harness are pending.
- Last completed evidence: X2 PR #99 passed PR Windows Harness run
  `25567947799`, merged as `f49a5774f4c5fb1dd2dcef64e1dca3affbf15d68`, and
  post-merge `main` Windows Harness run `25568061526` passed on that SHA.
- Last validation: X3 compatibility tests, full pytest, helper build, watcher
  build, install CLI smoke, full harness, and `git diff --check` passed
  locally.
- Next atomic task: open a small X3 PR, verify PR and post-merge Windows
  Harness, then advance to X4 v0.1.10 release readiness in the next branch.
- Known blockers: none.

## Phased Work

### Stage X0 - Post-v0.1.9 Baseline Cursor

- Add this post-v0.1.9 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Update docs tests so `v0.1.9` is the latest published release, this plan is
  the active cursor, and post-v0.1.8 is completed historical context.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, version metadata, or privacy behavior.

### Stage X1 - Evidence Freshness And Entry Hygiene

- Audit operator-facing docs and scorecards for stale current/latest release
  wording after `v0.1.9`.
- Decide whether inherited `v0.1.0` manual UIA smoke remains acceptable for a
  compatible maintenance path after `v0.1.9`.
- Require fresh manual UIA smoke if helper behavior, watcher product behavior,
  manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP
  shape, capture surfaces, or release approver requirements change.
- Strengthen narrow docs tests only for discovered drift around active cursor
  links, latest release identity, and evidence freshness wording.
- Do not commit observed-content artifacts.

### Stage X2 - CI Runtime And Dependency Maintenance Scan

- Review Windows Harness annotations, runner/runtime maintenance signals, and
  package/build warnings.
- Review deterministic dependency and package metadata for accidental Phase 6
  surface drift, including screenshot/OCR-related packages.
- If CI image, action-runtime, or deterministic dependency updates are needed,
  make the smallest workflow or metadata update without removing gates or
  changing gate order.
- Preserve pytest, helper build, watcher build, install CLI smoke, full
  harness, and `git diff --check` in CI.
- Do not add real UIA smoke to default CI.

### Stage X3 - Compatibility Guardrail Sweep

- Re-run deterministic gates and confirm the v0.1 boundary still holds.
- Treat existing tests and scorecards as compatibility oracles for version
  identity, exact read-only MCP tool list, disabled privacy surfaces, observed
  content trust boundaries, Phase 6 spec-only status, watcher preview limits,
  and product targeted capture absence.
- Strengthen tests only for discovered drift.
- Do not add helper/watcher product capabilities, MCP write tools, arbitrary
  file reads, screenshots, OCR, audio, keyboard capture, clipboard capture,
  network upload, desktop control, daemon/service install, polling capture
  loop, or default background capture.

### Stage X4 - v0.1.10 Release Readiness

- If X0-X3 only change documentation, tests, CI/runtime metadata, version
  metadata, or compatible drift fixes, prepare a compatible `v0.1.10`
  maintenance release.
- Before release, align package and server version metadata to `0.1.10`, add a
  release record, and record local gates plus PR and post-merge Windows
  Harness evidence.
- If any change alters product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture surface, stop the direct
  `v0.1.10` path and prepare a release candidate instead.
- Publication is authorized by the active goal only after required local, PR,
  and post-merge release gates pass.

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

- X0: docs tests confirm the active cursor points to this post-v0.1.9 plan,
  `v0.1.9` is the latest published release, PR #96 and Windows Harness run
  `25565697723` are recorded, and post-v0.1.8 is completed historical context.
- X1: README, operator quickstart, release checklist, release evidence guide,
  and manual smoke evidence ledger do not describe older post-v0.1.x plans as
  the current cursor; inherited manual smoke is labeled stale/inherited unless
  explicitly accepted.
- X2: CI runtime and dependency maintenance keeps the existing deterministic
  gate set, avoids screenshot/OCR dependency drift, and does not add
  interactive UIA smoke to default CI.
- X3: MCP tools remain exactly read-only, privacy surfaces remain disabled,
  memory/search trust boundaries remain stable, watcher remains preview-only,
  product targeted capture remains absent, and Phase 6 remains spec-only.
- X4: release checklist, release evidence, rollback notes, and Windows Harness
  pass before publication; manual UIA smoke refresh is required only if
  helper/smoke behavior, smoke docs, or the evidence ledger requires it.

## Public Interfaces And Non-goals

- CLI remains:
  `init/status/capture-once/capture-frontmost/watch/privacy-check/search-captures/generate-memory/search-memory/mcp-stdio`.
- Product CLI still does not expose targeted `--hwnd`, `--pid`, or
  `--window-title` capture.
- MCP remains read-only with:
  `current_context/search_captures/search_memory/read_recent_capture/recent_activity/privacy_status`.
- Version metadata may be updated only during release-readiness work, but MCP
  wire shape, tool schema, CLI JSON fields, and capture schema must not change
  in this maintenance pass.
- No screenshot capture, OCR, audio recording, keyboard capture, clipboard
  capture, network upload, LLM calls, MCP write tools, arbitrary file reads,
  service/daemon install, polling capture loop, default background capture, or
  desktop control.

## Assumptions

- `v0.1.9` is the current stable release baseline and must not be modified or
  retagged.
- The next compatible release target is `v0.1.10`.
- Phase 6 remains privacy spec/scorecard work only until a future tests-first
  round explicitly authorizes implementation.
- Manual UIA smoke remains outside default CI because it depends on an
  interactive Windows desktop.

## Decision Log

- Chose a compatible `v0.1.10` maintenance target because the published
  `v0.1.9` round changed release evidence, docs, tests, CI/runtime metadata,
  deterministic harness evidence, compatibility evidence, and version metadata
  only, without product behavior changes.
- Chose X0 as a docs-only active cursor so post-v0.1.9 work does not begin
  from a completed post-v0.1.8 plan.
- Recorded PR #96 and post-merge Windows Harness run `25565697723` in this
  active plan instead of modifying the published release tag. Do not retag
  `v0.1.9`.
- Recorded X0 PR #97 and post-merge Windows Harness run `25566750349` before
  starting X1; this keeps the active cursor aligned with the current `main`
  baseline without retagging `v0.1.9`.
- During X1, accepted inherited `v0.1.0` manual UIA smoke as inherited/stale
  evidence for the post-v0.1.9 compatible maintenance path because X0/X1 only
  changed docs/tests and did not change helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior, product
  CLI/MCP shape, capture surfaces, or release approver requirements.
- During X2, reviewed the latest `main` Windows Harness run `25567503424`,
  `.github/workflows/windows-harness.yml`, and package metadata. The workflow
  already uses `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: "true"`, pins
  `windows-2025-vs2026`, uses `actions/checkout@v6`,
  `actions/setup-python@v6`, and `actions/setup-dotnet@v5`, preserves the
  deterministic gate order, and showed no Node 20/deprecation annotation.
- During X2, kept dependency metadata unchanged because `pyproject.toml`
  depends only on `jsonschema` at runtime and `pytest`, `jsonschema`, and
  `wheel` for dev. Existing Phase 6 tests continue to guard against
  screenshot/OCR/audio/keyboard/clipboard/network/LLM/control-oriented
  dependency drift.
- During X3, treated existing compatibility tests and scorecards as the
  contract oracle. The focused guardrail tests confirmed exact read-only MCP
  tool names, disabled privacy surfaces, search and memory trust boundaries,
  version identity, watcher preview limits, product targeted capture absence,
  and Phase 6 spec-only status.
- During X3, reviewed source and docs references for targeted capture,
  screenshots/OCR, desktop control, clipboard, keyboard, network, and LLM
  surfaces. Matches were expected helper-only harness targeting, disabled
  surface contracts, fixtures, specs, scorecards, and tests; no product
  CLI/MCP targeted capture or new capture/control implementation was found.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.

## Validation Log

- Stage X0 initialization:
  - `gh release view v0.1.9 --json name,tagName,url,isDraft,isPrerelease,publishedAt,targetCommitish` - passed; `v0.1.9` is published and targets `d06ab5bc8bea7520bac2719adb457794c72911d3`.
  - `gh run view 25565697723 --json databaseId,status,conclusion,headSha,url,createdAt,updatedAt,name,displayTitle` - passed; conclusion `success` on `d06ab5bc8bea7520bac2719adb457794c72911d3`.
  - `git show-ref --tags v0.1.9` - passed; local tag points to `d06ab5bc8bea7520bac2719adb457794c72911d3`.
  - `python -c "import winchronicle; print(winchronicle.__version__)"` - passed and printed `0.1.9`.
- Stage X0 local validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 23 tests.
  - `python -m pytest -q` - passed, 114 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage X0 remote validation:
  - PR #97 Windows Harness run `25566609049` - passed.
  - PR #97 merged as `008c4d02dfef58004a2494c6102f434741a83047`.
  - Post-merge `main` Windows Harness run `25566750349` - passed on `008c4d02dfef58004a2494c6102f434741a83047`.
- Stage X1 evidence freshness validation:
  - `rg -n "active post-v0\.1\.[0-8]|current post-v0\.1\.[0-8]|current cursor.*v0\.1\.[0-8]|latest published v0\.1\.[0-8]" README.md docs tests` - passed with no matches.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py tests/test_uia_helper_quality_matrix.py -q` - passed, 26 tests.
  - `python -m pytest -q` - passed, 114 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage X1 remote validation:
  - PR #98 Windows Harness run `25567381942` - passed.
  - PR #98 merged as `def43279df9f09ae999f02b0c9ebc794e4540094`.
  - Post-merge `main` Windows Harness run `25567503424` - passed on `def43279df9f09ae999f02b0c9ebc794e4540094`.
- Stage X2 CI/runtime and dependency scan:
  - `gh run view 25567503424 --json databaseId,status,conclusion,headSha,url,createdAt,updatedAt,name,displayTitle,jobs` - passed; run succeeded on `def43279df9f09ae999f02b0c9ebc794e4540094`.
  - `gh run view 25567503424 --log | Select-String -Pattern "warning|deprecated|deprecation|Node 20|Node.js 20|Node24|FORCE_JAVASCRIPT_ACTIONS_TO_NODE24|error" -CaseSensitive:$false` - reviewed; Node 24 env is present, .NET builds report 0 warnings/0 errors, and the remaining `error` matches are deterministic fixture names or fixture text.
  - `.github/workflows/windows-harness.yml` inspection - passed; runner, action versions, gate set, and gate order are unchanged.
  - `pyproject.toml` inspection - passed; no screenshot/OCR/audio/keyboard/clipboard/network/LLM/control dependency drift.
  - `rg -n "screenshot|ocr|pillow|opencv|tesseract|easyocr|pytesseract|mss|dxcam|pyautogui|keyboard|clipboard|pyperclip|sounddevice|pyaudio|openai|anthropic|requests|httpx|aiohttp|selenium|playwright" pyproject.toml src tests harness docs resources .github` - reviewed; matches are existing disabled-surface contracts, specs, fixtures, docs, and tests rather than new runtime dependencies.
- Stage X2 local validation:
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_windows_harness_workflow.py tests/test_phase6_privacy_scorecard.py -q` - passed, 18 tests.
  - `python -m pytest -q` - passed, 114 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage X2 remote validation:
  - PR #99 Windows Harness run `25567947799` - passed.
  - PR #99 merged as `f49a5774f4c5fb1dd2dcef64e1dca3affbf15d68`.
  - Post-merge `main` Windows Harness run `25568061526` - passed on `f49a5774f4c5fb1dd2dcef64e1dca3affbf15d68`.
- Stage X3 compatibility guardrail scan:
  - `python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_version_identity.py -q` - passed, 37 tests.
  - `rg -n "TOOL_NAMES|current_context|search_captures|search_memory|read_recent_capture|recent_activity|privacy_status|write|click|type|clipboard|screenshot|ocr|audio|keyboard|network|product_targeted|untrusted_observed_content|Phase 6|specification-only" src tests docs harness -g "*.py" -g "*.md" -g "*.json"` - reviewed existing MCP, privacy, trust-boundary, watcher, and Phase 6 guardrails.
  - `rg -n -g "*.py" -g "*.cs" -g "*.md" -g "*.json" -g "*.yml" -- "--hwnd|--pid|--window-title|--window-title-regex|--process-name|SetForegroundWindow|AttachThreadInput|SendInput|mouse_event|keybd_event|GetAsyncKeyState|OpenClipboard|GetClipboardData|BitBlt|CopyFromScreen|PrintWindow|screenshot|OCR|Tesseract|OpenAI|Anthropic|requests|httpx|aiohttp" src resources tests harness .github docs` - reviewed; matches are expected helper-only harness targeting, disabled-surface docs/specs/tests/fixtures, and existing guardrails rather than product CLI/MCP targeted capture or new capture/control code.
- Stage X3 local validation:
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_version_identity.py -q` - passed, 48 tests.
  - `python -m pytest -q` - passed, 114 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
