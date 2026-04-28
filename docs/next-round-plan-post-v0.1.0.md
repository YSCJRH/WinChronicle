# WinChronicle Post-v0.1.0 Maintenance Plan

## Summary

`v0.1.0` final is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.0. The tag targets
`6d22462c0da185d163cf1b7219e05439ff4666ff`, and the latest post-final
reconciliation `main` Windows Harness run `25033992786` passed on
`52c0dde74b369e8afa86c2c12481aa50f5baa95f`.

The next round should be a conservative post-final maintenance pass, not a new
capture-surface expansion. The target release can be `v0.1.1` if the work stays
compatible and small. If any change alters product behavior, schema, CLI/MCP
JSON shape, privacy behavior, helper/watcher behavior, or capture surface in a
material way, publish a release candidate first.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, and no default background capture.

## Execution Cursor

- Current stage: Release Preparation - v0.1.1 maintenance.
- Stage status: F - all P0-P5 maintenance stages are merged and validated;
  compatible release preparation can start, but no release has been published.
- Last completed evidence: P5 Phase 6 privacy spec scorecard merged in PR #39
  and post-merge `main` Windows Harness run `25040068331` passed.
- Last validation: Phase 6 scorecard tests, `python -m pytest -q`, both .NET
  helper/watcher builds, install CLI smoke, full deterministic harness, and
  `git diff --check`, PR #39 Windows Harness, and post-merge `main` Windows
  Harness passed.
- Next atomic task: prepare `v0.1.1` release evidence, release notes, rollback
  notes, and any required manual-smoke decision record; do not publish without
  explicit release approval.
- Known blockers: none.

## Phased Work

### Stage P0 - Post-v0.1 Baseline

- Close the final-release cursor as historical.
- Confirm the final release URL, tag target, and latest post-final `main`
  Windows Harness.
- Establish this document as the active next-round cursor.
- Do not implement new product behavior in this stage.

### Stage P1 - Operator Diagnostics Audit

- Improve docs and tests for common operator-facing diagnostics:
  - `capture-frontmost` helper returns no capture;
  - watcher live preview returns heartbeat-only liveness;
  - helper timeout, invalid JSON, empty stdout, or nonzero exit;
  - VS Code strict Monaco marker remains diagnostic.
- Prefer docs, examples, fixtures, and narrow tests before any code change.
- If code is needed, keep it limited to clearer error surfaces without adding
  capture surfaces or observed-content echoing.

### Stage P2 - Watcher Preview Reliability Follow-Up

- Keep `watch --watcher --helper --duration` explicit and time-bounded.
- Add deterministic coverage only where current fixture tests do not already
  express the failure mode.
- Clarify heartbeat-only live runs as diagnostic and environment-dependent.
- Do not add daemon/service install, polling capture loops, startup tasks, or
  default background capture.

### Stage P3 - UIA Helper Compatibility Matrix Refresh

- Refresh the helper quality matrix with post-v0.1 evidence.
- Keep Notepad and Edge as hard targeted smoke gates.
- Keep VS Code metadata as conditional hard gate when `code.cmd` exists.
- Keep VS Code strict Monaco marker diagnostic and non-blocking.
- Any new application coverage is diagnostic by default until it has fixtures,
  privacy analysis, and manual smoke evidence.

### Stage P4 - MCP / Memory Contract Maintenance

- Recheck exact read-only MCP tool list and examples against the released
  contract.
- Recheck memory Markdown and SQLite entries for deterministic rerun behavior,
  trust boundary text, source capture paths, and secret-canary exclusion.
- Do not add MCP write tools, arbitrary file reads, desktop control tools, or
  new capture tools.

### Stage P5 - Phase 6 Privacy Spec Only

- Expand the screenshot/OCR privacy scorecard only as specification work.
- Keep screenshot and OCR implementation absent.
- Document tests-first prerequisites for any future optional enrichment:
  explicit opt-in, per-app allowlist, short-TTL raw cache, clear cleanup path,
  redaction/privacy pipeline parity, and MCP default non-exposure of raw
  screenshots.
- Do not implement screenshot capture, OCR, audio, keyboard capture, clipboard
  capture, network upload, LLM calls, or desktop control.

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

- P1: diagnostic text must not echo observed content.
- P2: watcher changes must keep raw watcher JSONL out of persistent storage.
- P3: manual smoke updates must record artifact paths only, not observed
  content.
- P4: MCP tool list must remain exactly read-only.
- P5: Phase 6 work must remain spec/scorecard only.

## Public Interfaces And Non-goals

- CLI remains:
  `init/status/capture-once/capture-frontmost/watch/privacy-check/search-captures/generate-memory/search-memory/mcp-stdio`.
- Product CLI still does not expose targeted `--hwnd`, `--pid`, or
  `--window-title` capture.
- MCP remains read-only.
- No screenshot capture, OCR, audio recording, keyboard capture, clipboard
  capture, network upload, LLM calls, MCP write tools, arbitrary file reads,
  service/daemon install, polling capture loop, default background capture, or
  desktop control.

## Assumptions

- `v0.1.0` is the current stable baseline.
- The next release target is maintenance-oriented `v0.1.1`, not a Phase 6
  feature release.
- Phase 6 remains specification-only until a future tests-first round.
- Manual UIA smoke remains outside default CI because it depends on an
  interactive Windows desktop.

## Decision Log

- Chose maintenance before Phase 6 because `v0.1.0` already shipped the core
  local memory baseline and the clearest gap is operator diagnostics around
  live helper/watcher environments.
- Chose docs/tests-first diagnostics because product capture boundaries should
  not expand merely to make smoke easier to pass.
- Kept `v0.1.1` as a compatible maintenance target, with release-candidate
  fallback for any material product or contract change.
- Kept P4 as tests-only because the released MCP and memory behavior already
  matched the plan; the smallest useful maintenance step was freezing examples
  and SQLite/search contracts against drift.
- Kept P5 as spec/test-only because Phase 6 remains optional future enrichment
  and this maintenance round must not add screenshot/OCR implementation,
  caches, or capture code.
- Determined the P0-P5 maintenance batch stayed compatible: it changed docs,
  tests, and scorecards only, with no product behavior, schema, CLI/MCP JSON
  shape, helper/watcher behavior, capture surface, or privacy behavior change.

## Validation Log

- `gh release view v0.1.0` confirmed the release is published, not a draft, not
  a prerelease, and targets `6d22462c0da185d163cf1b7219e05439ff4666ff`.
- Local tag `v0.1.0` resolves to
  `6d22462c0da185d163cf1b7219e05439ff4666ff`.
- Post-final reconciliation PR #29 merged to `main` at
  `52c0dde74b369e8afa86c2c12481aa50f5baa95f`.
- Post-final `main` Windows Harness run `25033992786` passed.
- Stage P1 local validation:
  - `python -m pytest tests/test_operator_diagnostics_docs.py -q` - 2 passed.
  - `python -m pytest -q` - 74 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage P1 PR validation:
  - PR #31 Windows Harness run `25036877035` passed.
  - PR #31 merged to `main` at
    `cd7c159bf888ab5d5b4e25e786a7dc39e551aa65`.
  - Post-merge `main` Windows Harness run `25036973210` passed.
- Stage P2 local validation:
  - `python -m pytest tests/test_watcher_events.py -q` - 13 passed.
  - `python -m pytest -q` - 76 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage P2 PR validation:
  - PR #33 Windows Harness run `25037700519` passed.
  - PR #33 merged to `main` at
    `91edc4ccf881328bcf639d9e9687d24479cc12ae`.
  - Post-merge `main` Windows Harness run `25037802382` passed.
- Stage P3 local validation:
  - `python -m pytest tests/test_uia_helper_quality_matrix.py -q` - 4 passed.
  - `python -m pytest -q` - 77 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage P3 PR validation:
  - PR #35 Windows Harness run `25038410329` passed.
  - PR #35 merged to `main` at
    `d669552751255da8a3561287c7af5c018487e66c`.
  - Post-merge `main` Windows Harness run `25038515262` passed.
- Stage P4 local validation:
  - `python -m pytest tests/test_mcp_tools.py tests/test_memory_pipeline.py -q` - 17 passed.
  - `python -m pytest -q` - 79 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage P4 PR validation:
  - PR #37 Windows Harness run `25039162443` passed.
  - PR #37 merged to `main` at
    `c6f5a432eb817d8d8259404e942a1b1f71b60b85`.
  - Post-merge `main` Windows Harness run `25039294143` passed.
- Stage P5 local validation:
  - `python -m pytest tests/test_phase6_privacy_scorecard.py -q` - 4 passed.
  - `python -m pytest -q` - 83 passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed.
  - `git diff --check` - passed.
- Stage P5 PR validation:
  - PR #39 Windows Harness run `25039920238` passed.
  - PR #39 merged to `main` at
    `3986be837302d590696b6fc42b7451a7a30d4020`.
  - Post-merge `main` Windows Harness run `25040068331` passed.
