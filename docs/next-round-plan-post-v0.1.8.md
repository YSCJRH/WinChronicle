# WinChronicle Post-v0.1.8 Maintenance Plan

## Summary

`v0.1.8` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.8. The release tag
targets `1ea1e378aedb0a509d202fd32bc69704dbe903d4`.

The post-v0.1.8 baseline starts from the compatible `v0.1.8` maintenance
release. PR #91 merged as `1ea1e378aedb0a509d202fd32bc69704dbe903d4`; its PR
Windows Harness run `25561704868` passed, and its post-merge `main` Windows
Harness run `25561832883` passed on that SHA.

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

- Current stage: W4 - v0.1.9 Release Readiness.
- Stage status: B - release-readiness version metadata and release record are
  implemented and local deterministic validation passed; PR Windows Harness,
  post-merge Windows Harness, and publication are pending.
- Last completed evidence: W3 PR #95 passed PR Windows Harness run
  `25564810377`, merged as `36d430c478e65ad107125b7e87ed4ec18ac18709`, and
  post-merge `main` Windows Harness run `25564926634` passed on that SHA.
- Last validation: W3 compatibility guardrail tests, full pytest, helper build,
  watcher build, install CLI smoke, full harness, `git diff --check`, PR
  Windows Harness, and post-merge `main` Windows Harness passed.
- Next atomic task: open the W4 release-readiness PR, verify PR and post-merge
  Windows Harness, then publish `v0.1.9` if all gates pass.
- Known blockers: none.

## Phased Work

### Stage W0 - Post-v0.1.8 Baseline Cursor

- Add this post-v0.1.8 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Update docs tests so `v0.1.8` remains the latest published release, this
  plan is the active cursor, and post-v0.1.7 is completed historical context.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, version metadata, or privacy behavior.

### Stage W1 - Evidence Freshness And Entry Hygiene

- Audit operator-facing docs and scorecards for stale current/latest release
  wording after `v0.1.8`.
- Decide whether inherited `v0.1.0` manual UIA smoke remains acceptable for a
  compatible maintenance path after `v0.1.8`.
- Require fresh manual UIA smoke if helper behavior, watcher product behavior,
  manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP
  shape, capture surfaces, or release approver requirements change.
- Strengthen narrow docs tests only for discovered drift around active cursor
  links, latest release identity, and evidence freshness wording.
- Do not commit observed-content artifacts.

### Stage W2 - CI Runtime And Dependency Maintenance Scan

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

### Stage W3 - Compatibility Guardrail Sweep

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

### Stage W4 - v0.1.9 Release Readiness

- If W0-W3 only change documentation, tests, CI/runtime metadata, version
  metadata, or compatible drift fixes, prepare a compatible `v0.1.9`
  maintenance release.
- Before release, align package and server version metadata to `0.1.9`, add a
  release record, and record local gates plus PR and post-merge Windows
  Harness evidence.
- If any change alters product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture surface, stop the direct
  `v0.1.9` path and prepare a release candidate instead.
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

- W0: docs tests confirm the active cursor points to this post-v0.1.8 plan,
  `v0.1.8` remains the latest published release, PR #91 and Windows Harness
  run `25561832883` are recorded, and post-v0.1.7 is completed historical
  context.
- W1: README, operator quickstart, release checklist, release evidence guide,
  and manual smoke evidence ledger do not describe older post-v0.1.x plans as
  the current cursor; inherited manual smoke is labeled stale/inherited unless
  explicitly accepted.
- W2: CI runtime and dependency maintenance keeps the existing deterministic
  gate set, avoids screenshot/OCR dependency drift, and does not add
  interactive UIA smoke to default CI.
- W3: MCP tools remain exactly read-only, privacy surfaces remain disabled,
  memory/search trust boundaries remain stable, watcher remains preview-only,
  product targeted capture remains absent, and Phase 6 remains spec-only.
- W4: release checklist, release evidence, rollback notes, and Windows Harness
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

- `v0.1.8` is the current stable release baseline and must not be modified or
  retagged.
- The next compatible release target is `v0.1.9`.
- Phase 6 remains privacy spec/scorecard work only until a future tests-first
  round explicitly authorizes implementation.
- Manual UIA smoke remains outside default CI because it depends on an
  interactive Windows desktop.

## Decision Log

- Chose a compatible `v0.1.9` maintenance target because the published
  `v0.1.8` round changed release evidence, docs, tests, CI/runtime metadata,
  deterministic harness evidence, compatibility evidence, and version metadata
  only, without product behavior changes.
- Chose W0 as a docs-only active cursor so post-v0.1.8 work does not begin
  from a completed post-v0.1.7 plan.
- Recorded PR #91 and post-merge Windows Harness run `25561832883` in this
  active plan instead of modifying the published release tag. Do not retag
  `v0.1.8`.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.
- Kept inherited manual UIA smoke as historical context only until W1 makes a
  release-specific freshness decision.
- During W0, merged PR #92 as
  `6d44aad77eedfb2480147ae8c112c3e001da4710`; PR Windows Harness
  `25562785206` and post-merge `main` Windows Harness `25562905132` passed.
- During W1, decided that inherited `v0.1.0` manual UIA smoke remains
  stale/inherited for the active post-v0.1.8 maintenance path. It is not fresh
  or current release evidence unless a later release-readiness record
  explicitly accepts it for a compatible release, or fresh manual smoke is
  rerun and recorded. No fresh manual smoke is required in W1 because no helper
  behavior, watcher product behavior, manual smoke scripts, capture behavior,
  privacy behavior, product CLI/MCP shape, or capture surfaces changed.
- During W1, merged PR #93 as
  `9c91f262ebb06f0b4fd8b4c38eeb17e8c688ecb9`; PR Windows Harness
  `25563462333` and post-merge `main` Windows Harness `25563589781` passed.
- During W2, reviewed the latest `main` Windows Harness run, workflow, and
  workflow guard test. The workflow still uses
  `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: "true"`, pins
  `windows-2025-vs2026`, preserves deterministic gate order, and produced no
  deprecation or failed-log signal requiring a workflow/runtime change.
  Therefore W2 records a no-action-needed CI runtime scan.
- During W2, reviewed package metadata and the direct-dependency guard against
  screenshot/OCR/audio/keyboard/clipboard/network/LLM/control-oriented
  packages. `pyproject.toml` remains limited to deterministic project and dev
  dependencies for the current maintenance path.
- During W2, merged PR #94 as
  `f9dff37828abdedb95511aeaf204a1313b75727c`; PR Windows Harness
  `25564182547` and post-merge `main` Windows Harness `25564339025` passed.
- During W3, re-ran the existing compatibility guardrail tests for CLI/MCP
  surface shape, exact read-only MCP tool list, disabled privacy surfaces,
  observed-content trust boundaries, Phase 6 spec-only status, watcher preview
  limits, helper harness-only capture, Windows Harness guardrails, and product
  targeted capture absence. No compatibility drift requiring product code,
  schema, CLI/MCP shape, helper/watcher behavior, or capture-surface changes was
  found, so W3 records a no-action-needed compatibility sweep.
- During W3, merged PR #95 as
  `36d430c478e65ad107125b7e87ed4ec18ac18709`; PR Windows Harness
  `25564810377` and post-merge `main` Windows Harness `25564926634` passed.
- During W4, chose the direct compatible `v0.1.9` path because W0-W4 change
  release evidence, documentation, tests, CI/runtime metadata, deterministic
  harness evidence, compatibility evidence, and version metadata only. If any
  product behavior, schema, CLI/MCP JSON shape, privacy behavior,
  helper/watcher behavior, or capture-surface regression is found before
  publication, stop the direct `v0.1.9` path and prepare a release candidate
  instead.
- During W4, the `v0.1.9` release-readiness record explicitly accepts inherited
  `v0.1.0` manual UIA smoke for the compatible `v0.1.9` path only because
  helper behavior, watcher product behavior, manual smoke scripts, capture
  behavior, privacy behavior, product CLI/MCP shape, and capture surfaces are
  unchanged.
- During W4, aligned version identity to `0.1.9` across `pyproject.toml`,
  `winchronicle.__version__`, and MCP `serverInfo.version` through the shared
  version module.

## Validation Log

- Stage W0 initialization:
  - `gh release view v0.1.8 --json name,tagName,url,isDraft,isPrerelease,publishedAt,targetCommitish` - passed; `v0.1.8` is published and targets `1ea1e378aedb0a509d202fd32bc69704dbe903d4`.
  - `gh run view 25561832883 --json databaseId,status,conclusion,headSha,url,createdAt,updatedAt,name,displayTitle` - passed; conclusion `success` on `1ea1e378aedb0a509d202fd32bc69704dbe903d4`.
  - `git show-ref --tags v0.1.8` - passed; local tag points to `1ea1e378aedb0a509d202fd32bc69704dbe903d4`.
  - `python -c "import winchronicle; print(winchronicle.__version__)"` - passed and printed `0.1.8`.
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_uia_helper_quality_matrix.py tests/test_version_identity.py -q` - passed after establishing this active cursor and updating operator entry-point tests.
  - `python -m pytest -q` - passed with `112 passed`.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage W0 remote validation:
  - PR #92 Windows Harness run `25562785206` - passed.
  - Post-merge `main` Windows Harness run `25562905132` - passed on `6d44aad77eedfb2480147ae8c112c3e001da4710`.
- Stage W1 evidence-freshness validation:
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py tests/test_uia_helper_quality_matrix.py -q` - passed after advancing this cursor to W1 and recording the active post-v0.1.8 manual smoke freshness decision.
  - `python -m pytest -q` - passed with `112 passed`.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage W1 remote validation:
  - PR #93 Windows Harness run `25563462333` - passed.
  - Post-merge `main` Windows Harness run `25563589781` - passed on `9c91f262ebb06f0b4fd8b4c38eeb17e8c688ecb9`.
- Stage W2 CI/runtime scan validation:
  - `gh run view 25563589781 --json databaseId,status,conclusion,headSha,url,createdAt,updatedAt,name,displayTitle,jobs` - passed; latest post-W1 `main` Windows Harness conclusion was `success` on `9c91f262ebb06f0b4fd8b4c38eeb17e8c688ecb9`.
  - `gh run view 25563589781 --log | Select-String -Pattern "warning|deprecated|deprecation|Node 20|Node20|windows-2025|runner image|error" -CaseSensitive:$false` - reviewed; runner image is `windows-2025-vs2026`, Node 24 env is present, .NET builds report 0 warnings/0 errors, and the remaining `error` matches are deterministic fixture names or fixture text.
  - `.github/workflows/windows-harness.yml` inspection - passed; gate order and gate set are unchanged.
  - `tests/test_windows_harness_workflow.py` inspection - passed; workflow guard pins Node 24, the Windows runner, and deterministic gate order.
  - `pyproject.toml` inspection - passed; direct runtime dependency remains `jsonschema`, with dev-only `pytest`, `jsonschema`, and `wheel`.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_windows_harness_workflow.py tests/test_phase6_privacy_scorecard.py -q` - passed with 17 tests.
  - `python -m pytest -q` - passed with 112 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage W2 remote validation:
  - PR #94 Windows Harness run `25564182547` - passed.
  - Post-merge `main` Windows Harness run `25564339025` - passed on `f9dff37828abdedb95511aeaf204a1313b75727c`.
- Stage W3 compatibility guardrail validation:
  - `python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_uia_helper_contract.py tests/test_windows_harness_workflow.py -q` - passed with 48 tests.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_uia_helper_contract.py tests/test_windows_harness_workflow.py -q` - passed with 58 tests.
  - `python -m pytest -q` - passed with 112 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage W3 remote validation:
  - PR #95 Windows Harness run `25564810377` - passed.
  - Post-merge `main` Windows Harness run `25564926634` - passed on `36d430c478e65ad107125b7e87ed4ec18ac18709`.
- Stage W4 release-readiness validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed with 22 tests.
  - `python -m pytest -q` - passed with 113 tests.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
