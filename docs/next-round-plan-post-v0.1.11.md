# WinChronicle Post-v0.1.11 Maintenance Plan

## Summary

`v0.1.11` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.11. The release tag
targets `1724b0e47e6f6b915a99842fb971d7f9c503f65a`, and post-merge `main`
Windows Harness run `25573347339` passed on that SHA.

The post-v0.1.11 baseline starts from the compatible `v0.1.11` maintenance
release. `main` is green, package/runtime/MCP version identity reports
`0.1.11`, and no product behavior, schema, CLI/MCP JSON shape, privacy
behavior, helper/watcher behavior, or capture-surface change was introduced by
the post-v0.1.10 round.

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

- Current stage: Z4 - v0.1.12 Release Readiness.
- Stage status: B - Z4 release-readiness docs/tests/version metadata are
  implemented and local
  deterministic validation passed; PR Windows Harness and post-merge Windows
  Harness are pending.
- Last completed evidence: Z3 PR #110 passed PR Windows Harness run
  `25575910225`, merged as
  `86be82cb153269bad68fb92806fa7701a1e8579c`, and post-merge `main`
  Windows Harness run `25576068774` passed on that SHA.
- Last validation: Z4 release-readiness checks, version identity tests,
  release evidence docs tests, full pytest, helper build, watcher build,
  install CLI smoke, full
  harness, and `git diff --check` passed locally.
- Next atomic task: open the Z4 PR, then verify PR and post-merge Windows
  Harness.
- Known blockers: none.

## Phased Work

### Stage Z0 - Post-v0.1.11 Baseline Cursor

- Add this post-v0.1.11 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Update docs tests so `v0.1.11` is the latest published release, this plan is
  the active cursor, and post-v0.1.10 is completed historical context.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, version metadata, or privacy behavior.

### Stage Z1 - Evidence Freshness And Entry Hygiene

- Audit operator-facing docs and scorecards for stale current/latest release
  wording after `v0.1.11`.
- Decide whether inherited `v0.1.0` manual UIA smoke remains acceptable for a
  compatible maintenance path after `v0.1.11`.
- Require fresh manual UIA smoke if helper behavior, watcher product behavior,
  manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP
  shape, capture surfaces, or release approver requirements change.
- Strengthen narrow docs tests only for discovered drift around active cursor
  links, latest release identity, and evidence freshness wording.
- Do not commit observed-content artifacts.

### Stage Z2 - CI Runtime And Dependency Maintenance Scan

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

### Stage Z3 - Compatibility Guardrail Sweep

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

### Stage Z4 - v0.1.12 Release Readiness

- If Z0-Z3 only change documentation, tests, CI/runtime metadata, version
  metadata, or compatible drift fixes, prepare a compatible `v0.1.12`
  maintenance release.
- Before release, align package and server version metadata to `0.1.12`, add a
  release record, and record local gates plus PR and post-merge Windows
  Harness evidence.
- If any change alters product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture surface, stop the direct
  `v0.1.12` path and prepare a release candidate instead.
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

- Z0: docs tests confirm the active cursor points to this post-v0.1.11 plan,
  `v0.1.11` is the latest published release, PR #106 and Windows Harness run
  `25573347339` are recorded, and post-v0.1.10 is completed historical
  context.
- Z1: README, operator quickstart, release checklist, release evidence guide,
  and manual smoke evidence ledger do not describe older post-v0.1.x plans as
  the current cursor; inherited manual smoke is labeled stale/inherited unless
  explicitly accepted.
- Z2: CI runtime and dependency maintenance keeps the existing deterministic
  gate set, avoids screenshot/OCR dependency drift, and does not add
  interactive UIA smoke to default CI.
- Z3: MCP tools remain exactly read-only, privacy surfaces remain disabled,
  memory/search trust boundaries remain stable, watcher remains preview-only,
  product targeted capture remains absent, and Phase 6 remains spec-only.
- Z4: release checklist, release evidence, rollback notes, and Windows Harness
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

- `v0.1.11` is the current stable release baseline and must not be modified or
  retagged.
- The next compatible release target is `v0.1.12`.
- Phase 6 remains privacy spec/scorecard work only until a future tests-first
  round explicitly authorizes implementation.
- Manual UIA smoke remains outside default CI because it depends on an
  interactive Windows desktop.

## Decision Log

- Chose a compatible `v0.1.12` maintenance target because the published
  `v0.1.11` round changed release evidence, docs, tests, CI/runtime metadata,
  deterministic harness evidence, compatibility evidence, and version metadata
  only, without product behavior changes.
- Chose Z0 as a docs-only active cursor so post-v0.1.11 work does not begin
  from a completed post-v0.1.10 plan.
- Recorded PR #106 and post-merge Windows Harness run `25573347339` in this
  active plan instead of modifying the published release tag. Do not retag
  `v0.1.11`.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.
- Recorded Z0 PR #107 and post-merge Windows Harness run `25574042929` as the
  post-publication baseline reconciliation for `v0.1.11`.
- During Z1, accepted inherited `v0.1.0` manual UIA smoke as inherited/stale
  evidence for the active post-v0.1.11 compatible maintenance path because
  Z0/Z1 changed only docs/tests and did not change helper behavior, watcher
  product behavior, manual smoke scripts, capture behavior, privacy behavior,
  product CLI/MCP shape, capture surfaces, or release approver requirements.
  This does not make inherited manual smoke fresh or current release evidence;
  Z4 must explicitly accept inherited evidence before `v0.1.12` publication or
  record fresh manual smoke.
- Recorded Z1 PR #108 and post-merge Windows Harness run `25574855474` as the
  evidence freshness and entry hygiene completion evidence.
- During Z2, reviewed the latest `main` Windows Harness run `25574855474` and
  found no deprecation, action-runtime, failed-log, or runner maintenance signal
  requiring workflow changes.
- During Z2, kept the existing CI gate order unchanged:
  `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: "true"`, `windows-2025-vs2026`,
  `actions/checkout@v6`, `actions/setup-python@v6`, `actions/setup-dotnet@v5`,
  pytest, helper build, watcher build, full harness, and `git diff --check`.
- During Z2, confirmed `pyproject.toml` remains limited to deterministic
  project dependencies: runtime `jsonschema`, and dev `pytest`, `jsonschema`,
  and `wheel`. No screenshot/OCR/audio/keyboard/clipboard/network/LLM
  dependency drift was found.
- Recorded Z2 PR #109 and post-merge Windows Harness run `25575439821` as the
  CI/runtime and dependency maintenance completion evidence.
- During Z3, treated the existing compatibility tests and scorecards as the
  compatibility oracles for exact read-only MCP tools, disabled privacy
  surfaces, observed content trust boundaries, watcher preview-only behavior,
  product targeted capture absence, and Phase 6 spec-only status.
- During Z3, found no product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture-surface drift. No additional
  product tests or code changes were needed.
- Recorded Z3 PR #110 and post-merge Windows Harness run `25576068774` as the
  compatibility guardrail sweep completion evidence.
- During Z4, chose the direct compatible `v0.1.12` path because Z0-Z4 changed
  only release evidence, documentation, tests, CI/runtime scan evidence,
  compatibility evidence, and version metadata.
- During Z4, aligned package, runtime, and MCP server version identity to
  `0.1.12`.
- During Z4, the `v0.1.12` release-readiness record explicitly accepts
  inherited `v0.1.0` manual UIA smoke for the compatible `v0.1.12` path only
  because helper behavior, watcher product behavior, manual smoke scripts,
  capture behavior, privacy behavior, product CLI/MCP shape, and capture
  surfaces are unchanged.

## Validation Log

- Stage Z0 initialization:
  - `gh release view v0.1.11 --json name,tagName,url,isDraft,isPrerelease,publishedAt,targetCommitish` - passed; `v0.1.11` is published and targets `1724b0e47e6f6b915a99842fb971d7f9c503f65a`.
  - `git show-ref --tags v0.1.11` - passed; local tag points to `1724b0e47e6f6b915a99842fb971d7f9c503f65a`.
  - `python -c "import winchronicle; print(winchronicle.__version__)"` - passed and printed `0.1.11`.
- Stage Z0 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 27 tests.
  - `python -m pytest -q` - passed, 118 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage Z0 remote validation:
  - PR #107 Windows Harness run `25573927712` - passed.
  - PR #107 merged as `8ca63acf7298564385f2a7ca777ff973aa7cb09b`.
  - Post-merge `main` Windows Harness run `25574042929` - passed on
    `8ca63acf7298564385f2a7ca777ff973aa7cb09b`.
- Stage Z1 evidence freshness validation:
  - `rg --pcre2 -n <stale-current-or-latest-v0.1.0-through-v0.1.10-patterns> README.md docs tests` - reviewed; remaining matches were historical records or tests asserting stale wording is absent.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q` - passed, 26 tests.
  - `python -m pytest -q` - passed, 118 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage Z1 remote validation:
  - PR #108 Windows Harness run `25574694437` - passed.
  - PR #108 merged as `a24ae2435264790ba8c2cac243c996ce3db0ce88`.
  - Post-merge `main` Windows Harness run `25574855474` - passed on
    `a24ae2435264790ba8c2cac243c996ce3db0ce88`.
- Stage Z2 CI/runtime and dependency scan:
  - `gh run view 25574855474 --json databaseId,status,conclusion,headSha,displayTitle,createdAt,updatedAt,url,jobs` - passed; run and deterministic harness job concluded `success`.
  - `gh run view 25574855474 --log | Select-String -Pattern "warning|deprecated|deprecation|Node 20|Node.js 20|node20|error|failed"` - reviewed; no deprecation, action-runtime, or failed-log maintenance signal was found.
  - `rg -n "uses: actions/(checkout|setup-python|setup-dotnet)@|runs-on:|FORCE_JAVASCRIPT_ACTIONS_TO_NODE24|python-version|dotnet-version" .github/workflows/windows-harness.yml` - passed; existing Node 24, runner, and action versions remain current for this plan.
  - `rg --files -g "pyproject.toml" -g "requirements*" -g "poetry.lock" -g "uv.lock" -g "Pipfile*" -g "package*.json"` - passed; only `pyproject.toml` is present.
  - `rg -n "pillow|opencv|tesseract|ocr|screenshot|imagegrab|pyautogui|mss|keyboard|clipboard|pyperclip|requests|httpx|aiohttp|openai|anthropic" pyproject.toml .github/workflows/windows-harness.yml` - passed with no matches.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q` - passed, 26 tests.
  - `python -m pytest -q` - passed, 118 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage Z2 remote validation:
  - PR #109 Windows Harness run `25575316043` - passed.
  - PR #109 merged as `6ac84e7ff62a4d5bd11ac4a9ffec85cbf51a3991`.
  - Post-merge `main` Windows Harness run `25575439821` - passed on
    `6ac84e7ff62a4d5bd11ac4a9ffec85cbf51a3991`.
- Stage Z3 compatibility guardrail sweep:
  - `gh run view 25575439821 --json databaseId,status,conclusion,headSha,displayTitle,url,jobs` - passed; run and deterministic harness job concluded `success`.
  - `python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py -q` - passed, 44 tests.
  - `python -c "from winchronicle.mcp.server import TOOL_NAMES; print('\n'.join(TOOL_NAMES))"` - passed; tool list remains exactly `current_context`, `search_captures`, `search_memory`, `read_recent_capture`, `recent_activity`, and `privacy_status`.
  - `WINCHRONICLE_HOME=<temp>; python -m winchronicle init; python -m winchronicle status` - passed; screenshots, OCR, audio, keyboard capture, clipboard capture, network upload, LLM calls, MCP write tools, desktop control, and product targeted capture remained disabled, and observed content trust remained `untrusted_observed_content`.
  - `rg -n -- "--hwnd|--pid|--window-title|--window-title-regex" src/winchronicle` - passed with no matches.
  - `rg -n "import .*keyboard|from .*keyboard|KeyboardHook|SetWindowsHookEx|ImageGrab|pyscreenshot|easyocr|paddleocr|pyautogui|pyperclip|requests\.|httpx|aiohttp|openai|anthropic|SetForegroundWindow|AttachThreadInput" src resources/win-uia-helper resources/win-uia-watcher` - passed with no matches.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q` - passed, 26 tests.
  - `python -m pytest -q` - passed, 118 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage Z3 remote validation:
  - PR #110 Windows Harness run `25575910225` - passed.
  - PR #110 merged as `86be82cb153269bad68fb92806fa7701a1e8579c`.
  - Post-merge `main` Windows Harness run `25576068774` - passed on
    `86be82cb153269bad68fb92806fa7701a1e8579c`.
- Stage Z4 release-readiness validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed, 28 tests.
  - `python -m pytest -q` - passed, 119 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Pending Z4 PR Windows Harness.
- Pending Z4 post-merge `main` Windows Harness.
