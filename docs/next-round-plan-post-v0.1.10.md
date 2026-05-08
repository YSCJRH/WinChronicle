# WinChronicle Post-v0.1.10 Maintenance Plan

## Summary

`v0.1.10` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.10. The release tag
targets `28b062a531519d4360911b51dfc083782b6dcbad`, and post-merge `main`
Windows Harness run `25569567825` passed on that SHA.

The post-v0.1.10 baseline starts from the compatible `v0.1.10` maintenance
release. `main` is green, package/runtime/MCP version identity reports
`0.1.10`, and no product behavior, schema, CLI/MCP JSON shape, privacy
behavior, helper/watcher behavior, or capture-surface change was introduced by
the post-v0.1.9 round.

This next round remains a conservative compatible maintenance pass. It should
keep release evidence current, preserve operator entry points, audit inherited
manual smoke freshness, and maintain compatibility guardrails. It must not
expand the capture surface or start Phase 6 implementation.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, and no default background capture.

## Execution Cursor

- Current stage: Y2 - CI Runtime And Dependency Maintenance Scan.
- Stage status: B - Y2 CI/runtime and dependency scan docs/tests are
  implemented and local deterministic validation passed; PR Windows Harness
  and post-merge Windows Harness are pending.
- Last completed evidence: Y1 PR #103 passed PR Windows Harness run
  `25571224423`, merged as `3ed5db90e4e630b3e3920a798001ae9ec7a4a14a`, and
  post-merge `main` Windows Harness run `25571374301` passed on that SHA.
- Last validation: Y2 CI/runtime docs tests, full pytest, helper build,
  watcher build, install CLI smoke, full harness, and `git diff --check` passed
  locally.
- Next atomic task: open the Y2 PR, then verify PR and post-merge Windows
  Harness.
- Known blockers: none.

## Phased Work

### Stage Y0 - Post-v0.1.10 Baseline Cursor

- Add this post-v0.1.10 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Update docs tests so `v0.1.10` is the latest published release, this plan is
  the active cursor, and post-v0.1.9 is completed historical context.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, version metadata, or privacy behavior.

### Stage Y1 - Evidence Freshness And Entry Hygiene

- Audit operator-facing docs and scorecards for stale current/latest release
  wording after `v0.1.10`.
- Decide whether inherited `v0.1.0` manual UIA smoke remains acceptable for a
  compatible maintenance path after `v0.1.10`.
- Require fresh manual UIA smoke if helper behavior, watcher product behavior,
  manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP
  shape, capture surfaces, or release approver requirements change.
- Strengthen narrow docs tests only for discovered drift around active cursor
  links, latest release identity, and evidence freshness wording.
- Do not commit observed-content artifacts.

### Stage Y2 - CI Runtime And Dependency Maintenance Scan

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

### Stage Y3 - Compatibility Guardrail Sweep

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

### Stage Y4 - v0.1.11 Release Readiness

- If Y0-Y3 only change documentation, tests, CI/runtime metadata, version
  metadata, or compatible drift fixes, prepare a compatible `v0.1.11`
  maintenance release.
- Before release, align package and server version metadata to `0.1.11`, add a
  release record, and record local gates plus PR and post-merge Windows
  Harness evidence.
- If any change alters product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture surface, stop the direct
  `v0.1.11` path and prepare a release candidate instead.
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

- Y0: docs tests confirm the active cursor points to this post-v0.1.10 plan,
  `v0.1.10` is the latest published release, PR #101 and Windows Harness run
  `25569567825` are recorded, and post-v0.1.9 is completed historical context.
- Y1: README, operator quickstart, release checklist, release evidence guide,
  and manual smoke evidence ledger do not describe older post-v0.1.x plans as
  the current cursor; inherited manual smoke is labeled stale/inherited unless
  explicitly accepted.
- Y2: CI runtime and dependency maintenance keeps the existing deterministic
  gate set, avoids screenshot/OCR dependency drift, and does not add
  interactive UIA smoke to default CI.
- Y3: MCP tools remain exactly read-only, privacy surfaces remain disabled,
  memory/search trust boundaries remain stable, watcher remains preview-only,
  product targeted capture remains absent, and Phase 6 remains spec-only.
- Y4: release checklist, release evidence, rollback notes, and Windows Harness
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

- `v0.1.10` is the current stable release baseline and must not be modified or
  retagged.
- The next compatible release target is `v0.1.11`.
- Phase 6 remains privacy spec/scorecard work only until a future tests-first
  round explicitly authorizes implementation.
- Manual UIA smoke remains outside default CI because it depends on an
  interactive Windows desktop.

## Decision Log

- Chose a compatible `v0.1.11` maintenance target because the published
  `v0.1.10` round changed release evidence, docs, tests, CI/runtime metadata,
  deterministic harness evidence, compatibility evidence, and version metadata
  only, without product behavior changes.
- Chose Y0 as a docs-only active cursor so post-v0.1.10 work does not begin
  from a completed post-v0.1.9 plan.
- Recorded PR #101 and post-merge Windows Harness run `25569567825` in this
  active plan instead of modifying the published release tag. Do not retag
  `v0.1.10`.
- Recorded Y0 PR #102 and post-merge Windows Harness run `25570603780` before
  starting Y1; this keeps the active cursor aligned with the current `main`
  baseline without retagging `v0.1.10`.
- During Y1, accepted inherited `v0.1.0` manual UIA smoke as inherited/stale
  evidence for the post-v0.1.10 compatible maintenance path because Y0/Y1 only
  changed docs/tests and did not change helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior, product
  CLI/MCP shape, capture surfaces, or release approver requirements.
- Recorded Y1 PR #103 and post-merge Windows Harness run `25571374301` before
  starting Y2; this keeps the active cursor aligned with the current `main`
  baseline without retagging `v0.1.10`.
- During Y2, reviewed the latest `main` Windows Harness run `25571374301`,
  `.github/workflows/windows-harness.yml`, and package metadata. The workflow
  already uses `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: "true"`, pins
  `windows-2025-vs2026`, uses `actions/checkout@v6`,
  `actions/setup-python@v6`, and `actions/setup-dotnet@v5`, preserves the
  deterministic gate order, and showed no Node 20/deprecation annotation.
- During Y2, kept dependency metadata unchanged because `pyproject.toml`
  depends only on `jsonschema` at runtime and `pytest`, `jsonschema`, and
  `wheel` for dev. Existing Phase 6 tests continue to guard against
  screenshot/OCR/audio/keyboard/clipboard/network/LLM/control-oriented
  dependency drift.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.

## Validation Log

- Stage Y0 initialization:
  - `gh release view v0.1.10 --json name,tagName,url,isDraft,isPrerelease,publishedAt,targetCommitish` - passed; `v0.1.10` is published and targets `28b062a531519d4360911b51dfc083782b6dcbad`.
  - `git show-ref --tags v0.1.10` - passed; local tag points to `28b062a531519d4360911b51dfc083782b6dcbad`.
  - `python -c "import winchronicle; print(winchronicle.__version__)"` - passed and printed `0.1.10`.
- Stage Y0 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 25 tests.
  - Stale-current-wording `rg` scan across `README.md`, `docs`, and `tests` - passed with no matches.
  - `python -m pytest -q` - passed, 116 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage Y0 remote validation:
  - PR #102 Windows Harness run `25570444498` - passed.
  - PR #102 merged as `049fbc3550efe71e553fb0e27be7344f4d686e5c`.
  - Post-merge `main` Windows Harness run `25570603780` - passed on `049fbc3550efe71e553fb0e27be7344f4d686e5c`.
- Stage Y1 evidence freshness validation:
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q` - passed, 24 tests.
  - Stale-current-wording `rg` scan across `README.md`, `docs`, and `tests` - passed with no matches.
  - `python -m pytest -q` - passed, 116 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
  - PR #103 Windows Harness run `25571224423` - passed.
  - PR #103 merged as `3ed5db90e4e630b3e3920a798001ae9ec7a4a14a`.
  - Post-merge `main` Windows Harness run `25571374301` - passed on `3ed5db90e4e630b3e3920a798001ae9ec7a4a14a`.
- Stage Y2 CI/runtime and dependency scan:
  - `gh run view 25571374301 --json databaseId,status,conclusion,headSha,url,createdAt,updatedAt,name,displayTitle` - passed; run succeeded on `3ed5db90e4e630b3e3920a798001ae9ec7a4a14a`.
  - `gh run view 25571374301 --log | Select-String -Pattern "warning|deprecated|deprecation|Node 20|Node.js 20|Node24|FORCE_JAVASCRIPT_ACTIONS_TO_NODE24|error" -CaseSensitive:$false` - reviewed; Node 24 env is present, .NET builds report 0 warnings/0 errors, and the remaining `error` matches are deterministic fixture names or fixture text.
  - `.github/workflows/windows-harness.yml` inspection - passed; runner, action versions, gate set, and gate order are unchanged.
  - `pyproject.toml` inspection - passed; no screenshot/OCR/audio/keyboard/clipboard/network/LLM/control dependency drift.
  - `rg -n "screenshot|ocr|pillow|opencv|tesseract|easyocr|pytesseract|mss|dxcam|pyautogui|keyboard|clipboard|pyperclip|sounddevice|pyaudio|openai|anthropic|requests|httpx|aiohttp|selenium|playwright|comtypes|uiautomation|pywin32|pywinauto|pynput|whisper" pyproject.toml src tests harness docs resources .github` - reviewed; matches are existing disabled-surface contracts, specs, fixtures, docs, and tests rather than new runtime dependencies.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_windows_harness_workflow.py tests/test_phase6_privacy_scorecard.py -q` - passed, 19 tests.
  - `python -m pytest -q` - passed, 116 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
  - Pending PR Windows Harness.
  - Pending post-merge `main` Windows Harness.
