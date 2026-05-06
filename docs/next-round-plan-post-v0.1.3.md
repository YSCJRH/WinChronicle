# WinChronicle Post-v0.1.3 Maintenance Plan

## Summary

`v0.1.3` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.3. The release tag
targets `0aa5c1b6e1959ef6504e6d70e4aad79a60594926`. The post-publication
reconciliation `main` commit is
`917a1f4b70d6ae1527332fe97cad3e0cc0d9d520`, and the post-reconciliation
Windows Harness run `25209330825` passed on that SHA.

The next round should be a small compatible maintenance pass toward `v0.1.4`.
It should keep release evidence current, preserve operator entry points, decide
manual smoke freshness before any release, and maintain compatibility
guardrails. It must not expand the capture surface or start Phase 6
implementation.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, and no default background capture.

## Execution Cursor

- Current stage: P4 - v0.1.4 Release Readiness.
- Stage status: F - v0.1.4 release-readiness gates have passed; publication
  requires explicit user approval.
- Last completed evidence: P2 documented the manual smoke freshness decision:
  inherited `v0.1.0` manual smoke may be explicitly accepted for a compatible
  `v0.1.4` maintenance release only when no helper, watcher, smoke script,
  capture, privacy, product CLI/MCP shape, or capture-surface behavior changes.
  P1 refreshed stale UIA helper quality matrix wording so it no longer presents
  the `v0.1.3` readiness round as current, kept post-v0.1.3 as the active
  maintenance plan, and updated narrow docs tests. P0 added this post-v0.1.3
  plan, updated README, operator quickstart, release checklist, release
  evidence guide, manual smoke ledger, and narrow docs tests so this plan is
  the active cursor. `v0.1.3` was published at
  https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.3 and targets
  `0aa5c1b6e1959ef6504e6d70e4aad79a60594926`; post-publication
  reconciliation merged at `917a1f4b70d6ae1527332fe97cad3e0cc0d9d520`.
- Last validation: P4 local deterministic validation, PR #64 Windows Harness
  run `25411926176`, and post-merge `main` Windows Harness run `25411989748`
  passed.
- Next atomic task: wait for explicit publication approval; if approved,
  publish `v0.1.4` and reconcile the release URL, tag target, and publication
  evidence.
- Known blockers: publication requires explicit user approval.

## Phased Work

### Stage P0 - Post-v0.1.3 Baseline Cursor

- Add this post-v0.1.3 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence guide,
  and manual smoke evidence ledger so operators can find this active cursor.
- Keep the post-v0.1.2 plan closed and historical.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, or privacy behavior.

### Stage P1 - Release Evidence And Entry Hygiene

- Audit docs and scorecards that still describe older release plans as current
  and refresh only operator-facing entry points.
- Add or strengthen narrow docs tests only for discovered drift around active
  cursor links, latest release identity, and evidence freshness wording.
- Keep `v0.1.3` as the stable release baseline until release-readiness work
  explicitly prepares `v0.1.4`.
- Do not bump package/server version in P1.

### Stage P2 - Manual Smoke Freshness Decision

- Decide whether the next release can inherit older manual UIA smoke evidence
  or requires a fresh manual run.
- If fresh manual smoke is required, record only command, result, timestamp,
  environment notes, and local artifact paths with the existing template.
- Keep real UIA smoke outside default CI and keep all artifacts local.
- Do not commit observed text, screenshots, OCR output, raw helper JSON, raw
  watcher JSONL, local HTML page contents, editor buffer contents, passwords,
  secrets, or token canaries.

### Stage P3 - Compatibility Guardrail Maintenance

- Re-run deterministic gates and confirm the v0.1 boundary still holds.
- Strengthen tests only for discovered drift around version identity,
  read-only MCP tool list, privacy surface parity, memory/search trust
  boundaries, release evidence freshness, and Phase 6 spec-only status.
- Do not add helper/watcher product capabilities, MCP write tools, arbitrary
  file reads, screenshots, OCR, audio, keyboard capture, clipboard capture,
  network upload, desktop control, daemon/service install, polling capture loop,
  or default background capture.

### Stage P4 - v0.1.4 Release Readiness

- If P0-P3 only change documentation, tests, version metadata, or compatible
  drift fixes, prepare a compatible `v0.1.4` maintenance release.
- Before release, align package and server version metadata to `0.1.4`, add a
  release record, and record local gates plus PR and post-merge Windows Harness
  evidence.
- If any change alters product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture surface, stop the direct
  `v0.1.4` path and prepare a release candidate instead.
- Publication remains blocked on explicit user approval.

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

- P0: grep or doc inspection confirms the active cursor points to this
  post-v0.1.3 plan and historical plans remain historical.
- P1: README, operator quickstart, release checklist, and release evidence
  guide do not describe older post-v0.1.x plans as the current cursor.
- P2: manual smoke freshness policy records only commands, results,
  timestamps, environment notes, and local artifact paths; observed-content
  artifacts remain uncommitted.
- P3: MCP tools remain exactly read-only, privacy surfaces remain disabled,
  memory/search trust boundaries remain stable, and Phase 6 remains spec-only.
- P4: release checklist, release evidence, rollback notes, and Windows Harness
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

- `v0.1.3` is the current stable release baseline and must not be modified or
  retagged.
- The next compatible release target is `v0.1.4`.
- Phase 6 remains privacy spec/scorecard work only until a future tests-first
  round.
- Manual UIA smoke remains outside default CI because it depends on an
  interactive Windows desktop.

## Decision Log

- Chose a compatible `v0.1.4` maintenance target because `v0.1.3` changed
  version metadata and release evidence only, without product behavior changes.
- Chose P0 as a docs-only active cursor so post-v0.1.3 work does not begin
  from a closed historical plan.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.
- During P0, updated only documentation and docs tests. No product code,
  schemas, CLI/MCP JSON shape, helper/watcher behavior, capture surfaces, or
  privacy behavior changed.
- During P1, treated the UIA helper quality matrix as an operator-facing
  release evidence surface. The only stale current-release wording found was
  the matrix reference to the `v0.1.3` readiness round; it now points to the
  active post-v0.1.3 maintenance plan and future `v0.1.4` readiness work.
- During P1, renamed a stale test function that still called the published
  `v0.1.2` release record "pending"; this changed test naming only.
- During P2, decided that the post-v0.1.3 compatible maintenance path may
  explicitly accept inherited `v0.1.0` manual smoke in the `v0.1.4` release
  record only if no helper, watcher, smoke script, capture, privacy, product
  CLI/MCP shape, or capture-surface behavior changes. Fresh manual smoke is
  still required for any such behavior change or if the release approver
  requires fresh hard-gate evidence.
- During P3, treated the post-merge `main` Windows Harness watcher smoke
  failure as a harness timing stability issue: the fake-helper
  `--capture-on-start` path can consume an 850 ms smoke budget before the
  heartbeat loop runs on slower CI attempts. Increased only the harness smoke
  default duration and added counts/event diagnostics. This does not change
  product watcher/helper behavior, CLI/MCP shape, capture schema, privacy
  behavior, or capture surface.
- During P3, merged PR #62 after PR Windows Harness run `25410884216` passed;
  post-merge `main` Windows Harness run `25410946398` then passed on
  `63547c9f4ba4c1a218913dca93dbdf3714879f7e`, restoring the mainline gate.
- During P4, aligned package/runtime/MCP version identity to `0.1.4`, added
  the pending `v0.1.4` release-readiness record, and kept `v0.1.3` as the
  latest published release until explicit approval and release creation are
  complete.
- During P4, addressed the P2 manual-smoke freshness policy by treating the P3
  deterministic watcher smoke timing change as requiring fresh deterministic
  gate evidence, not fresh manual UIA smoke, because product UIA behavior and
  manual UIA smoke scripts did not change.
- During P4, merged PR #64 after PR Windows Harness run `25411926176` passed;
  post-merge `main` Windows Harness run `25411989748` passed on
  `5b2b042459874e1197011b4c560c2c7cb93287cc`. The release remains unpublished
  pending explicit approval.
- During P4 evidence follow-up, recorded the final PR #64 and post-merge
  `main` Windows Harness evidence in the release-readiness record without
  changing product behavior or publication status.

## Validation Log

- `gh release view v0.1.3 --json name,tagName,url,isDraft,isPrerelease,publishedAt,targetCommitish`
  confirmed the release is published, not a draft, not a prerelease, targets
  `0aa5c1b6e1959ef6504e6d70e4aad79a60594926`, and is available at
  https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.3.
- `gh run view 25209330825 --json databaseId,conclusion,headSha,status,url,workflowName`
  confirmed the post-publication reconciliation `main` Windows Harness passed
  on `917a1f4b70d6ae1527332fe97cad3e0cc0d9d520`.
- Stage P0 local validation:
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q` - 11 passed.
  - `python -m pytest -q` - 97 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
  - PR #62 Windows Harness run `25410884216` - passed.
  - Post-merge `main` Windows Harness run `25410946398` on `63547c9f4ba4c1a218913dca93dbdf3714879f7e` - passed.
- Stage P3 completion cursor validation:
  - `python -m pytest tests/test_operator_diagnostics_docs.py -q` - 6 passed.
  - `python -m pytest -q` - 98 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage P4 local release-readiness validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - 13 passed.
  - `python -m pytest -q` - 99 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
  - PR #64 Windows Harness run `25411926176` - passed.
  - Post-merge `main` Windows Harness run `25411989748` on `5b2b042459874e1197011b4c560c2c7cb93287cc` - passed.
- Stage P4 evidence follow-up validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - 12 passed.
  - `python -m pytest -q` - 99 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage P1 local validation:
  - `python -m pytest tests/test_uia_helper_quality_matrix.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q` - 15 passed.
  - stale-current-cursor `rg` scan over README.md, docs, and tests - no matches for current `v0.1.3` readiness, `after v0.1.2`, pending post-v0.1.3 plan, or stale pending test names.
  - `python -m pytest -q` - 97 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage P2 local validation:
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_uia_helper_quality_matrix.py tests/test_compatibility_evidence_docs.py -q` - 15 passed.
  - manual-smoke freshness `rg` scan over docs and tests - found the expected P2 decision, `v0.1.4` acceptance policy, fresh-smoke requirement, and capture-surface guard references.
  - `python -m pytest -q` - 97 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage P3 watcher smoke stability validation:
  - `python -m pytest tests/test_watcher_events.py -q` - 14 passed.
  - `python harness/scripts/run_watcher_smoke.py` - passed.
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_watcher_events.py -q` - 20 passed after updating docs-test cursor expectations.
  - `python -m pytest -q` - 98 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed with 0 warnings and 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
