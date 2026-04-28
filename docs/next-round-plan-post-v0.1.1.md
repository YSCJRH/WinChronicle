# WinChronicle Post-v0.1.1 Maintenance Plan

## Summary

`v0.1.1` is published and reconciled. The release URL is
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.1, the release tag
targets `8ac594176d251c867e34c2a139a1029a3fc474da`, and the
post-reconciliation `main` Windows Harness run `25042828969` passed on
`5d8d69c9be8f32a333e7f1aa6a5a6bc49f8ae867`.

The next round is a conservative compatible maintenance pass toward `v0.1.2`.
It should fix post-release baseline drift, version identity consistency,
operator documentation entry points, and release evidence. It must not expand
the capture surface or start Phase 6 implementation.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, and no default background capture.

## Execution Cursor

- Current stage: V4 - v0.1.2 Release Readiness.
- Stage status: B - V4 release readiness is locally complete; the Stage V4
  pull request, PR Windows Harness, post-merge `main` Windows Harness, and
  explicit publication approval remain pending.
- Last completed evidence: V4 aligned package/runtime/MCP version metadata to
  `0.1.2`, added the `v0.1.2` release readiness record, and kept publication
  status pending explicit approval.
- Last validation: V4 local validation passed with version/release-evidence
  docs tests, full pytest, helper build, watcher build, install CLI smoke,
  full harness, and `git diff --check`.
- Next atomic task: open the Stage V4 pull request, wait for PR Windows
  Harness, merge after review if green, then wait for post-merge `main`
  Windows Harness. Do not publish `v0.1.2` without explicit approval.
- Known blockers: none.

## Phased Work

### Stage V0 - Post-v0.1.1 Baseline Cursor

- Add this post-v0.1.1 active next-round plan and keep the old post-v0.1.0
  plan as historical release evidence.
- Update README and operator quickstart links so operators can find the active
  post-v0.1.1 cursor.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, or privacy behavior.

### Stage V1 - Version Identity Parity

- Add tests that require `pyproject.toml`, `winchronicle.__version__`, and MCP
  `serverInfo.version` to report the same release identity.
- Fix the currently known drift: `pyproject.toml` reports `0.1.1`, while
  `src/winchronicle/__init__.py` and MCP `serverInfo.version` still report
  `0.1.0`.
- Keep this as metadata parity only: no MCP tool list, tool schema, response
  shape, privacy semantic, or capture schema changes.

### Stage V2 - Operator Entry Refresh

- Refresh docs that still describe old release-readiness plans as current entry
  points.
- Treat `v0.1.1` as the published baseline and this document as the active
  next-round cursor.
- Refresh stale `v0.1.1` pre-release language in the helper quality matrix.
- Keep manual smoke evidence policy unchanged: record commands, results,
  timestamps, environment notes, and local artifact paths only; never commit
  observed-content artifacts.

### Stage V3 - Compatibility Evidence Sweep

- Re-run the deterministic maintenance gates and confirm the v0.1 boundary
  still holds.
- Add or adjust only narrow tests/docs for discovered drift around version
  identity, active plan links, exact read-only MCP tools, and Phase 6 spec-only
  status.
- Do not add helper/watcher product capabilities or put real UIA smoke into
  default CI.

### Stage V4 - v0.1.2 Release Readiness

- If V0-V3 only change documentation, tests, version metadata, or compatible
  drift fixes, prepare a compatible `v0.1.2` maintenance release.
- Before release, align package and server version metadata to `0.1.2`, add a
  release record, and record local gates plus PR and post-merge Windows Harness
  evidence.
- If any change alters product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, helper/watcher behavior, or capture surface, stop the direct
  `v0.1.2` path and prepare a release candidate instead.

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

- V0: grep or doc inspection confirms the active cursor points to this
  post-v0.1.1 plan and historical plans remain historical.
- V1: version identity tests cover package metadata, `winchronicle.__version__`,
  and MCP `serverInfo.version`.
- V2: README and operator quickstart do not describe old final-readiness plans
  as current.
- V3: MCP tools remain exactly read-only and Phase 6 remains spec-only.
- V4: release checklist, release evidence, rollback notes, and Windows Harness
  pass before publication; manual UIA smoke refresh is required only if
  helper/smoke behavior or smoke docs materially change.

## Public Interfaces And Non-goals

- CLI remains:
  `init/status/capture-once/capture-frontmost/watch/privacy-check/search-captures/generate-memory/search-memory/mcp-stdio`.
- Product CLI still does not expose targeted `--hwnd`, `--pid`, or
  `--window-title` capture.
- MCP remains read-only with:
  `current_context/search_captures/search_memory/read_recent_capture/recent_activity/privacy_status`.
- Version metadata may be updated, but MCP wire shape, tool schema, CLI JSON
  fields, and capture schema must not change in this maintenance pass.
- No screenshot capture, OCR, audio recording, keyboard capture, clipboard
  capture, network upload, LLM calls, MCP write tools, arbitrary file reads,
  service/daemon install, polling capture loop, default background capture, or
  desktop control.

## Assumptions

- `v0.1.1` is the current stable release baseline and must not be modified or
  retagged.
- The next compatible release target is `v0.1.2`.
- Phase 6 remains privacy spec/scorecard work only until a future tests-first
  round.
- Manual UIA smoke remains outside default CI because it depends on an
  interactive Windows desktop.

## Decision Log

- Chose a compatible `v0.1.2` maintenance target because `v0.1.1` shipped
  without product behavior changes and the visible drift is release identity
  and operator documentation.
- Chose V0 as a docs-only baseline cursor so implementation work does not begin
  without an active post-v0.1.1 plan.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.
- During V1, chose a shared `winchronicle._version` module instead of importing
  `__version__` from the package root inside MCP. The first approach broke the
  repository-root bootstrap package used by `python -m winchronicle` from a
  fresh checkout; the shared module keeps source, bootstrap, and MCP metadata
  aligned without changing MCP tools or response shape.
- During V2, kept old final-readiness and post-v0.1.0 documents linked as
  historical records instead of removing them, because they remain useful
  release evidence but should not be presented as the active cursor.
- During V3, treated MCP and Phase 6 scorecards as the compatibility evidence
  oracles and added release checklist/evidence requirements instead of changing
  product behavior.
- During V4, treated the `0.1.2` version bump as release metadata alignment
  only. It does not change MCP wire shape, tool schema, CLI JSON fields,
  capture schema, helper/watcher behavior, or privacy behavior.
- During V4, kept PR and post-merge Windows Harness fields in the release
  record pending until the Stage V4 PR and merge exist, so the release record
  does not chase its own SHA before publication approval.

## Validation Log

- `gh release view v0.1.1` confirmed the release is published, not a draft, not
  a prerelease, and targets `8ac594176d251c867e34c2a139a1029a3fc474da`.
- Post-reconciliation `main` Windows Harness run `25042828969` passed on
  `5d8d69c9be8f32a333e7f1aa6a5a6bc49f8ae867`.
- Stage V0 local validation:
  - `rg -n "Post-v0\.1\.1 maintenance plan|next-round-plan-post-v0\.1\.1|Current stage: V0|Stage status: A|v0\.1\.1 maintenance release record" README.md docs\operator-quickstart.md docs\next-round-plan-post-v0.1.1.md` - passed before the cursor was advanced to V1.
  - `python -m pytest -q` - 83 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
- Stage V1 local validation:
  - `python -m pytest tests/test_version_identity.py tests/test_mcp_tools.py -q` - 10 passed.
  - `python -m pytest tests/test_uia_helper_contract.py::test_uia_helper_smoke_script_uses_fake_helper_without_printing_capture -q` - 1 passed after moving version metadata into the shared module.
  - First `python -m pytest -q` attempt failed because importing `__version__`
    from the package root in MCP broke the repository-root bootstrap package;
    this was fixed before final validation.
  - `python -m pytest -q` - 84 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
- Stage V2 local validation:
  - `python -m pytest tests/test_operator_diagnostics_docs.py tests/test_uia_helper_quality_matrix.py -q` - 7 passed.
  - `python -m pytest -q` - 85 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
- Stage V3 local validation:
  - First `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py -q` attempt failed because two documentation phrases were wrapped differently than the assertions expected; the tests now normalize whitespace while still locking the required evidence language.
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py -q` - 16 passed.
  - `python -m pytest -q` - 88 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
- Stage V4 local validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - 8 passed after clarifying the `v0.1.2` release record's no-OCR evidence wording.
  - `python -m pytest -q` - 89 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
