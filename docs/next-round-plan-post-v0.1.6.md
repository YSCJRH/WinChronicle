# WinChronicle Post-v0.1.6 Maintenance Plan

## Summary

`v0.1.6` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.6. The release tag
targets `914cf361ac5864fa31d393d125d14e45eeba96bc`. The publication
reconciliation PR #80 merged as `371060498c70a4e1ff4e075b3fd247b704c6d3f7`;
its PR Windows Harness run `25552120656` passed, and its post-merge `main`
Windows Harness run `25552214063` passed on that SHA.

The next round should be a conservative compatible maintenance pass toward
`v0.1.7`. It should keep release evidence current, preserve operator entry
points, audit freshness of inherited manual smoke, and maintain compatibility
guardrails. It must not expand the capture surface or start Phase 6
implementation.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, and no default background capture.

## Execution Cursor

- Current stage: T3 - Compatibility Guardrail Sweep.
- Stage status: B - T3 local compatibility guardrail sweep and validation are
  complete; PR Windows Harness and post-merge `main` Windows Harness are
  pending.
- Last completed evidence: `v0.1.6` is published at
  https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.6 and targets
  `914cf361ac5864fa31d393d125d14e45eeba96bc`. Publication reconciliation PR
  #80 passed PR Windows Harness run `25552120656`, merged as
  `371060498c70a4e1ff4e075b3fd247b704c6d3f7`, and post-merge `main` Windows
  Harness run `25552214063` passed on that SHA. T2 PR #83 passed PR Windows
  Harness run `25554431580`, merged as
  `fb84fb2b2bf47cfe89680c898f3694f543d75c52`, and post-merge `main` Windows
  Harness run `25554520036` passed on that SHA.
- Last validation: T3 compatibility guardrail sweep found no required product,
  schema, CLI/MCP, helper/watcher, privacy, or capture-surface changes;
  targeted compatibility tests, the full deterministic gate, and `git diff
  --check` passed.
- Next atomic task: open the T3 PR, wait for PR Windows Harness, merge after
  review, then wait for post-merge `main` Windows Harness before starting T4
  release readiness.
- Known blockers: none.

## Phased Work

### Stage T0 - Post-v0.1.6 Baseline Cursor

- Add this post-v0.1.6 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Update docs tests so `v0.1.6` remains the latest published release and this
  plan is the active cursor.
- Mark the post-v0.1.5 plan as completed after publication reconciliation.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, version metadata, or privacy behavior.

### Stage T1 - Evidence Freshness And Entry Hygiene

- Audit operator-facing docs and scorecards for stale current/latest release
  wording after `v0.1.6`.
- Decide whether inherited `v0.1.0` manual UIA smoke remains acceptable for a
  compatible `v0.1.7` path.
- Require fresh manual UIA smoke if helper behavior, watcher product behavior,
  manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP
  shape, capture surfaces, or release approver requirements change.
- Strengthen narrow docs tests only for discovered drift around active cursor
  links, latest release identity, and evidence freshness wording.
- Do not commit observed-content artifacts.

### Stage T2 - CI Runtime And Dependency Maintenance Scan

- Review Windows Harness annotations, runner/runtime maintenance signals, and
  package/build warnings.
- If CI image, action-runtime, or deterministic dependency updates are needed,
  make the smallest workflow or metadata update without removing gates or
  changing gate order.
- Preserve pytest, helper build, watcher build, install CLI smoke, full
  harness, and `git diff --check` in CI.
- Do not add real UIA smoke to default CI.

### Stage T3 - Compatibility Guardrail Sweep

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

### Stage T4 - v0.1.7 Release Readiness

- If T0-T3 only change documentation, tests, CI/runtime metadata, version
  metadata, or compatible drift fixes, prepare a compatible `v0.1.7`
  maintenance release.
- Before release, align package and server version metadata to `0.1.7`, add a
  release record, and record local gates plus PR and post-merge Windows
  Harness evidence.
- If any change alters product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture surface, stop the direct
  `v0.1.7` path and prepare a release candidate instead.
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

- T0: docs tests confirm the active cursor points to this post-v0.1.6 plan,
  `v0.1.6` remains the latest published release, and post-v0.1.5 is completed
  historical context.
- T1: README, operator quickstart, release checklist, release evidence guide,
  and manual smoke evidence ledger do not describe older post-v0.1.x plans as
  the current cursor; inherited manual smoke is labeled stale/inherited unless
  explicitly accepted.
- T2: CI runtime maintenance keeps the existing deterministic gate set and does
  not add interactive UIA smoke to default CI.
- T3: MCP tools remain exactly read-only, privacy surfaces remain disabled,
  memory/search trust boundaries remain stable, watcher remains preview-only,
  product targeted capture remains absent, and Phase 6 remains spec-only.
- T4: release checklist, release evidence, rollback notes, and Windows Harness
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

- `v0.1.6` is the current stable release baseline and must not be modified or
  retagged.
- The next compatible release target is `v0.1.7`.
- Phase 6 remains privacy spec/scorecard work only until a future tests-first
  round explicitly authorizes implementation.
- Manual UIA smoke remains outside default CI because it depends on an
  interactive Windows desktop.

## Decision Log

- Chose a compatible `v0.1.7` maintenance target because the published
  `v0.1.6` round changed release evidence, docs, tests, CI/runtime metadata,
  deterministic harness evidence, compatibility evidence, and version metadata
  only, without product behavior changes.
- Chose T0 as a docs-only active cursor so post-v0.1.6 work does not begin
  from a completed post-v0.1.5 plan.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.
- Kept inherited manual UIA smoke as historical context only until T1 makes a
  release-specific freshness decision.
- During T0, merged PR #81 as
  `94db6c8a0733fb373bdd97246ef9568e9aa2f7ac`; PR Windows Harness
  `25553025094` and post-merge `main` Windows Harness `25553238476` passed.
- During T1, kept inherited `v0.1.0` manual UIA smoke as not-current evidence
  for the active `v0.1.7` path until T1 or a release record explicitly accepts
  it, or fresh manual smoke is recorded. No helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior, product
  CLI/MCP shape, or capture surfaces changed.
- During T2, reviewed the latest `main` Windows Harness run, workflow, and
  workflow guard test. The workflow already uses
  `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: "true"`, pins
  `windows-2025-vs2026`, preserves the deterministic gate order, and produced
  no deprecation or failed-log signal requiring a workflow/runtime change.
  Therefore T2 records a no-action-needed CI runtime scan.
- During T2, merged PR #83 as
  `fb84fb2b2bf47cfe89680c898f3694f543d75c52`; PR Windows Harness
  `25554431580` and post-merge `main` Windows Harness `25554520036` passed.
- During T3, treated existing tests and scorecards as compatibility oracles.
  The sweep found existing coverage for exact read-only MCP tools, disabled
  privacy surfaces, search/memory trust boundaries, watcher preview limits,
  product targeted capture absence, and Phase 6 spec-only status. Therefore
  T3 records a no-action-needed compatibility guardrail sweep with no product
  changes.

## Validation Log

- Stage T0 initialization:
  - `gh release view v0.1.6 --json name,tagName,url,isDraft,isPrerelease,publishedAt,targetCommitish` - passed; `v0.1.6` is published and targets `914cf361ac5864fa31d393d125d14e45eeba96bc`.
  - `gh run view 25552214063 --json databaseId,status,conclusion,headSha,url,createdAt,updatedAt,name,displayTitle` - passed; conclusion `success` on `371060498c70a4e1ff4e075b3fd247b704c6d3f7`.
  - `git show-ref --tags v0.1.6` - passed; local tag points to `914cf361ac5864fa31d393d125d14e45eeba96bc`.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py tests/test_version_identity.py -q` - passed after adding this active cursor and updating operator entry-point tests.
  - `python -m pytest -q` - passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
  - PR #81 Windows Harness run `25553025094` - passed.
  - Post-merge `main` Windows Harness run `25553238476` - passed on `94db6c8a0733fb373bdd97246ef9568e9aa2f7ac`.
- Stage T1 evidence-hygiene validation:
  - `gh run view 25553238476 --json databaseId,status,conclusion,headSha,url,createdAt,updatedAt,name,displayTitle` - passed; conclusion `success` on `94db6c8a0733fb373bdd97246ef9568e9aa2f7ac`.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py tests/test_version_identity.py -q` - passed after advancing this cursor to T1 and tightening manual smoke freshness wording.
  - `python -m pytest -q` - passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage T2 CI runtime scan validation:
  - `gh run view 25554033860 --json databaseId,status,conclusion,headSha,url,createdAt,updatedAt,name,displayTitle,jobs` - passed; latest post-T1 `main` Windows Harness conclusion was `success` on `fccba1ec46126710d29fd1dacbb34f45b9eef938`.
  - `gh run view 25554033860 --log-failed` - passed with no failed log output.
  - `gh run view 25554033860 --log | Select-String -Pattern "warning|deprecated|deprecation|windows-2025|Node|runner image|error" -CaseSensitive:$false` - reviewed; runner image is `windows-2025-vs2026`, Node 24 env is present, .NET builds report 0 warnings/0 errors, and the remaining `error` matches are fixture names or deterministic fixture text.
  - `.github/workflows/windows-harness.yml` inspection - passed; gate order and gate set are unchanged.
  - `tests/test_windows_harness_workflow.py` inspection - passed; workflow guard already pins Node 24, the Windows runner, and deterministic gate order.
  - `python -m pytest tests/test_windows_harness_workflow.py tests/test_operator_diagnostics_docs.py -q` - passed after recording the T2 no-action-needed scan.
  - `python -m pytest -q` - passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
  - PR #83 Windows Harness run `25554431580` - passed.
  - Post-merge `main` Windows Harness run `25554520036` - passed on `fb84fb2b2bf47cfe89680c898f3694f543d75c52`.
- Stage T3 compatibility guardrail validation:
  - `python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_memory_pipeline.py tests/test_phase6_privacy_scorecard.py tests/test_privacy_check.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py tests/test_watcher_events.py tests/test_uia_helper_quality_matrix.py -q` - passed.
  - `python -m pytest -q` - passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
