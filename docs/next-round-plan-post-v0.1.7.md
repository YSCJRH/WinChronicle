# WinChronicle Post-v0.1.7 Maintenance Plan

## Summary

`v0.1.7` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.7. The release tag
targets `0b5969509754f78b218f823d0e6bb7a0ea61392b`.

The post-v0.1.7 publication reconciliation is complete. PR #86 merged as
`5e310f9c37836c5e6baa1bee7f89f91f701ff6e8`; its PR Windows Harness run
`25556946503` passed, and its post-merge `main` Windows Harness run
`25557058094` passed on that SHA.

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

- Current stage: U4 - v0.1.8 Release Readiness.
- Stage status: B - release-readiness docs, tests, release record, and version
  metadata are implemented and local deterministic validation passed; PR
  Windows Harness and post-merge Windows Harness are pending.
- Last completed evidence: U3 PR #90 passed PR Windows Harness run
  `25560353073`, merged as `8a25ec8abf2f91a912aaffd807ae4a4897847578`, and
  post-merge `main` Windows Harness run `25560483461` passed on that SHA.
- Last validation: U4 version/docs tests, full pytest, helper build, watcher
  build, install CLI smoke, full harness, and `git diff --check` passed.
- Next atomic task: open the U4 PR, verify PR and post-merge Windows Harness,
  then publish `v0.1.8` if no product, schema, CLI/MCP JSON shape, privacy,
  helper/watcher behavior, or capture-surface change is discovered.
- Known blockers: none.

## Phased Work

### Stage U0 - Post-v0.1.7 Baseline Cursor

- Add this post-v0.1.7 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Update docs tests so `v0.1.7` remains the latest published release, this
  plan is the active cursor, and post-v0.1.6 is completed historical context.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, version metadata, or privacy behavior.

### Stage U1 - Evidence Freshness And Entry Hygiene

- Audit operator-facing docs and scorecards for stale current/latest release
  wording after `v0.1.7`.
- Decide whether inherited `v0.1.0` manual UIA smoke remains acceptable for a
  compatible maintenance path after `v0.1.7`.
- Require fresh manual UIA smoke if helper behavior, watcher product behavior,
  manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP
  shape, capture surfaces, or release approver requirements change.
- Strengthen narrow docs tests only for discovered drift around active cursor
  links, latest release identity, and evidence freshness wording.
- Do not commit observed-content artifacts.

### Stage U2 - CI Runtime And Dependency Maintenance Scan

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

### Stage U3 - Compatibility Guardrail Sweep

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

### Stage U4 - v0.1.8 Release Readiness

- If U0-U3 only change documentation, tests, CI/runtime metadata, version
  metadata, or compatible drift fixes, prepare a compatible `v0.1.8`
  maintenance release.
- Before release, align package and server version metadata to `0.1.8`, add a
  release record, and record local gates plus PR and post-merge Windows
  Harness evidence.
- If any change alters product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture surface, stop the direct
  `v0.1.8` path and prepare a release candidate instead.
- Publication requires explicit release approval unless a newer active goal
  explicitly authorizes publishing the prepared release.

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

- U0: docs tests confirm the active cursor points to this post-v0.1.7 plan,
  `v0.1.7` remains the latest published release, PR #86 and Windows Harness
  run `25557058094` are recorded, and post-v0.1.6 is completed historical
  context.
- U1: README, operator quickstart, release checklist, release evidence guide,
  and manual smoke evidence ledger do not describe older post-v0.1.x plans as
  the current cursor; inherited manual smoke is labeled stale/inherited unless
  explicitly accepted.
- U2: CI runtime and dependency maintenance keeps the existing deterministic
  gate set, avoids screenshot/OCR dependency drift, and does not add
  interactive UIA smoke to default CI.
- U3: MCP tools remain exactly read-only, privacy surfaces remain disabled,
  memory/search trust boundaries remain stable, watcher remains preview-only,
  product targeted capture remains absent, and Phase 6 remains spec-only.
- U4: release checklist, release evidence, rollback notes, and Windows Harness
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

- `v0.1.7` is the current stable release baseline and must not be modified or
  retagged.
- The next compatible release target is `v0.1.8`.
- Phase 6 remains privacy spec/scorecard work only until a future tests-first
  round explicitly authorizes implementation.
- Manual UIA smoke remains outside default CI because it depends on an
  interactive Windows desktop.

## Decision Log

- Chose a compatible `v0.1.8` maintenance target because the published
  `v0.1.7` round changed release evidence, docs, tests, CI/runtime metadata,
  deterministic harness evidence, compatibility evidence, and version metadata
  only, without product behavior changes.
- Chose U0 as a docs-only active cursor so post-v0.1.7 work does not begin
  from a completed post-v0.1.6 plan.
- Recorded PR #86 and post-merge Windows Harness run `25557058094` in this
  active plan instead of modifying the published release tag. Do not retag
  `v0.1.7`.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.
- Kept inherited manual UIA smoke as historical context only until U1 makes a
  release-specific freshness decision.
- During U0, merged PR #87 as
  `3ca1d2772c16ac11b7cfef8f4fe8b6fc28cb6636`; PR Windows Harness
  `25557993996` and post-merge `main` Windows Harness `25558154805` passed.
- During U1, decided that inherited `v0.1.0` manual UIA smoke remains
  stale/inherited for the active post-v0.1.7 maintenance path. It is not fresh
  or current release evidence unless a later release-readiness record
  explicitly accepts it for a compatible release, or fresh manual smoke is
  rerun and recorded. No fresh manual smoke is required in U1 because no helper
  behavior, watcher product behavior, manual smoke scripts, capture behavior,
  privacy behavior, product CLI/MCP shape, or capture surfaces changed.
- During U1, refreshed operator evidence references so the active
  post-v0.1.7 cursor includes both the publication reconciliation evidence from
  PR #86 and the U0 cursor PR #87 evidence. The UIA helper quality matrix
  maintenance wording now points at compatible maintenance releases after
  `v0.1.7` while preserving historical `v0.1.4`-onward context.
- During U1, merged PR #88 as
  `bf7397711bc4f2f70ca677dc788464d6fa4f03f3`; PR Windows Harness
  `25558809159` and post-merge `main` Windows Harness `25558922168` passed.
- During U2, reviewed the latest `main` Windows Harness run, workflow, and
  workflow guard test. The workflow still uses
  `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: "true"`, pins
  `windows-2025-vs2026`, preserves deterministic gate order, and produced no
  deprecation or failed-log signal requiring a workflow/runtime change.
  Therefore U2 records a no-action-needed CI runtime scan.
- During U2, reviewed package metadata and added a direct-dependency guard
  against screenshot/OCR/audio/keyboard/clipboard/network/LLM/control-oriented
  packages. `pyproject.toml` remains limited to deterministic project and dev
  dependencies for the current maintenance path.
- During U2, merged PR #89 as
  `a6703f500c0140dba7ed4d2bcdf3427050745649`; PR Windows Harness
  `25559501788` and post-merge `main` Windows Harness `25559686547` passed.
- During U3, treated existing tests and scorecards as compatibility oracles.
  The sweep found current coverage for version identity, exact read-only MCP
  tools, disabled privacy surfaces, search/memory trust boundaries, Phase 6
  spec-only and dependency/source absence, watcher preview limits, product
  targeted capture absence, and UIA helper boundary status. Therefore U3
  records a no-action-needed compatibility guardrail sweep with no product
  changes.
- During U3, merged PR #90 as
  `8a25ec8abf2f91a912aaffd807ae4a4897847578`; PR Windows Harness
  `25560353073` and post-merge `main` Windows Harness `25560483461` passed.
- During U4, chose the direct compatible `v0.1.8` path because U0-U4 change
  release evidence, documentation, tests, CI/runtime metadata, compatibility
  evidence, and version metadata only. If any product behavior, schema,
  CLI/MCP JSON shape, privacy behavior, helper/watcher behavior, or
  capture-surface change is required, stop the direct path and prepare a
  release candidate instead.
- During U4, the `v0.1.8` release-readiness record explicitly accepts
  inherited `v0.1.0` manual UIA smoke for the compatible `v0.1.8` path only
  because helper behavior, watcher product behavior, manual smoke scripts,
  capture behavior, privacy behavior, product CLI/MCP shape, and capture
  surfaces are unchanged.
- During U4, aligned version identity to `0.1.8` across `pyproject.toml`,
  `winchronicle.__version__`, and MCP `serverInfo.version` through the shared
  version module.

## Validation Log

- Stage U0 initialization:
  - `gh release view v0.1.7 --json name,tagName,url,isDraft,isPrerelease,publishedAt,targetCommitish` - passed; `v0.1.7` is published and targets `0b5969509754f78b218f823d0e6bb7a0ea61392b`.
  - `gh run view 25557058094 --json databaseId,status,conclusion,headSha,url,createdAt,updatedAt,name,displayTitle` - passed; conclusion `success` on `5e310f9c37836c5e6baa1bee7f89f91f701ff6e8`.
  - `git show-ref --tags v0.1.7` - passed; local tag points to `0b5969509754f78b218f823d0e6bb7a0ea61392b`.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py tests/test_version_identity.py -q` - passed after adding this active cursor and updating operator entry-point tests.
  - `python -m pytest -q` - passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage U0 remote validation:
  - PR #87 Windows Harness run `25557993996` - passed.
  - Post-merge `main` Windows Harness run `25558154805` - passed on `3ca1d2772c16ac11b7cfef8f4fe8b6fc28cb6636`.
- Stage U1 evidence-freshness validation:
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py tests/test_version_identity.py -q` - passed after advancing this cursor to U1 and recording the active post-v0.1.7 manual smoke freshness decision.
  - `python -m pytest -q` - passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage U1 remote validation:
  - PR #88 Windows Harness run `25558809159` - passed.
  - Post-merge `main` Windows Harness run `25558922168` - passed on `bf7397711bc4f2f70ca677dc788464d6fa4f03f3`.
- Stage U2 CI/runtime scan validation:
  - `gh run view 25558922168 --json databaseId,status,conclusion,headSha,url,createdAt,updatedAt,name,displayTitle,jobs` - passed; latest post-U1 `main` Windows Harness conclusion was `success` on `bf7397711bc4f2f70ca677dc788464d6fa4f03f3`.
  - `gh run view 25558922168 --log | Select-String -Pattern "warning|deprecated|deprecation|Node 20|Node20|windows-2025|Node|runner image|error" -CaseSensitive:$false` - reviewed; runner image is `windows-2025-vs2026`, Node 24 env is present, .NET builds report 0 warnings/0 errors, and the remaining `error` matches are deterministic fixture names or fixture text.
  - `.github/workflows/windows-harness.yml` inspection - passed; gate order and gate set are unchanged.
  - `tests/test_windows_harness_workflow.py` inspection - passed; workflow guard already pins Node 24, the Windows runner, and deterministic gate order.
  - `pyproject.toml` inspection - passed; direct runtime dependency remains `jsonschema`, with dev-only `pytest`, `jsonschema`, and `wheel`.
  - `python -m pytest tests/test_windows_harness_workflow.py tests/test_phase6_privacy_scorecard.py tests/test_operator_diagnostics_docs.py -q` - passed after recording the U2 no-action-needed scan and dependency guard.
  - `python -m pytest -q` - passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage U2 remote validation:
  - PR #89 Windows Harness run `25559501788` - passed.
  - Post-merge `main` Windows Harness run `25559686547` - passed on `a6703f500c0140dba7ed4d2bcdf3427050745649`.
- Stage U3 compatibility guardrail validation:
  - `python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_memory_pipeline.py tests/test_phase6_privacy_scorecard.py tests/test_privacy_check.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py tests/test_watcher_events.py tests/test_uia_helper_quality_matrix.py -q` - passed.
  - `python -m pytest -q` - passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage U3 remote validation:
  - PR #90 Windows Harness run `25560353073` - passed.
  - Post-merge `main` Windows Harness run `25560483461` - passed on `8a25ec8abf2f91a912aaffd807ae4a4897847578`.
- Stage U4 release-readiness validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed after aligning version identity to `0.1.8`, adding the `v0.1.8` release-readiness record, and recording the U4 manual smoke acceptance decision.
  - `python -m pytest -q` - passed with `111 passed`.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
