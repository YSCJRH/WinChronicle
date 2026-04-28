# WinChronicle v0.1.0 Final Release Plan

## Summary

`v0.1.0-rc.1` is published and green. Its tag targets
`ad2c33feffb151ffe6c52d651c05ace5e007db97`, and the current `main` at
`99f432204f53390c971726c4f132badc2ef57603` is green on Windows Harness run
`25032840199`.

The only commits after the `v0.1.0-rc.1` tag are publication-reconciliation
docs in `docs/next-round-plan-v0.1.0-final.md` and
`docs/release-candidate-v0.1.0-rc.1.md`. No product code, schema, CLI/MCP JSON
shape, helper/watcher behavior, or privacy contract changed after rc.1.

The next public release can be `v0.1.0` final if the final gates pass without
requiring product behavior, schema, CLI/MCP JSON shape, privacy contract, or
`src/` / `resources/` changes. If any such change is needed, publish
`v0.1.0-rc.2` first.

The product boundary remains unchanged: local-first, UIA-first, harness-first,
read-only MCP first, no screenshot/OCR implementation, no audio recording, no
keyboard capture, no clipboard capture, no network upload, no LLM calls, no
desktop control, and no product targeted capture flags.

## Execution Cursor

- Current stage: Stage V3 - Final Release Decision.
- Stage status: F - deterministic gates and V2 manual hard gates passed; final
  release evidence is prepared and publication requires explicit approval.
- Last completed evidence: Stage V1 deterministic evidence was merged in
  PR #26, post-merge `main` Windows Harness run `25033323560` passed, and V2
  manual smoke refresh completed on the local interactive Windows machine.
- Last validation: Notepad targeted UIA smoke passed, Edge targeted UIA smoke
  passed, `code.cmd` was available, VS Code metadata smoke passed with the known
  Monaco editor-marker diagnostic warning, VS Code strict mode failed as the
  documented non-blocking diagnostic, and live watcher preview returned
  heartbeat-only liveness using temporary `WINCHRONICLE_HOME`.
- Next atomic task: open the `docs/release-v0.1.0.md` evidence PR, wait for
  Windows Harness, merge it, and verify post-merge `main` Windows Harness; do
  not publish `v0.1.0` final without explicit approval.
- Known blockers: none.

## Phased Work

### Stage V0 - Post-rc.1 Baseline

- Confirm `v0.1.0-rc.1` release URL, tag target, prerelease status, and latest
  post-publication `main` Windows Harness.
- Confirm tag-to-main drift is docs-only and does not change product behavior
  or operator-facing contracts.
- Establish this final-release plan as the active cursor.
- Do not publish final from this stage.

### Stage V1 - Deterministic Final Gates

- Rerun the full deterministic release checklist on the final candidate branch:
  - `python -m pytest -q`
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo`
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo`
  - `python harness/scripts/run_install_cli_smoke.py`
  - `python harness/scripts/run_harness.py`
  - `git diff --check`
- Verify Windows Harness on the PR and post-merge `main`.
- If any fix requires product behavior, schema, CLI/MCP JSON shape, privacy
  behavior, or `src` / `resources` changes, stop final and prepare
  `v0.1.0-rc.2` instead.

### Stage V2 - Manual Final Smoke Refresh

- Rerun manual smoke on an interactive Windows desktop with temporary state:
  - Notepad targeted smoke: hard gate.
  - Edge targeted smoke: hard gate.
  - VS Code metadata smoke: conditional hard gate when `code.cmd` is available.
  - VS Code strict Monaco marker: diagnostic and non-blocking.
  - Watcher preview: diagnostic/manual confidence gate with temporary
    `WINCHRONICLE_HOME`.
- Record only commands, pass/fail results, timestamps, environment notes, and
  local artifact paths. Do not commit observed-content artifacts.

### Stage V3 - Final Release Decision

- Create `docs/release-v0.1.0.md` with:
  - deterministic gate evidence;
  - manual smoke evidence;
  - final tag target;
  - release notes;
  - known limitations;
  - rollback notes;
  - privacy/scope confirmation.
- Publish `v0.1.0` final only after explicit approval.
- Tag the current verified `main` SHA as `v0.1.0`; do not retag `v0.1.0-rc.1`.

### Stage V4 - Post-Final Reconciliation

- After publication, reconcile the repository docs with:
  - final release URL;
  - exact `v0.1.0` tag target;
  - PR Windows Harness URL;
  - post-merge `main` Windows Harness URL;
  - next active execution cursor.
- Establish the post-v0.1 baseline before planning any new capability work.

## Test Plan

Every final-release implementation stage should run:

- `python -m pytest -q`
- `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo`
- `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo`
- `python harness/scripts/run_install_cli_smoke.py`
- `python harness/scripts/run_harness.py`
- `git diff --check`
- GitHub Actions `Windows Harness` on PR and after merge to `main`

Stage-specific gates:

- V0: release/tag/CI verification and docs-only tag-to-main drift check.
- V1: deterministic gates and Windows Harness.
- V2: manual Notepad/Edge/VS Code metadata gates and watcher preview evidence.
- V3: final release evidence and explicit publication approval.
- V4: post-publication reconciliation.

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
- Phase 6 remains specification-only until a future tests-first round after
  `v0.1.0` final.

## Decision Log

- Chose direct final as the next target because `v0.1.0-rc.1` is published,
  post-publication `main` is green, and tag-to-main drift is docs-only.
- Kept `v0.1.0-rc.2` as the fallback if final gates expose any required product
  or contract change.
- Kept manual smoke as a final hard gate for Notepad, Edge, and conditional VS
  Code metadata because those are the established v0.1 release gates.
- Kept VS Code strict Monaco marker diagnostic and non-blocking per the known
  limitation.

## Validation Log

- `gh release view v0.1.0-rc.1` confirmed the release is a prerelease, not a
  draft, and targets `ad2c33feffb151ffe6c52d651c05ace5e007db97`.
- Latest `main` Windows Harness passed on
  `99f432204f53390c971726c4f132badc2ef57603`, run `25032840199`.
- `git diff v0.1.0-rc.1..main` showed only:
  - `docs/next-round-plan-v0.1.0-final.md`;
  - `docs/release-candidate-v0.1.0-rc.1.md`.
- Stage V0 final-release plan merged through PR #25, and post-merge `main`
  Windows Harness run `25033085206` passed on
  `56747bed1a1039356b47200464db289032025b70`.
- Local Stage V1 deterministic gates passed on `2026-04-28`: `72 passed` for
  `python -m pytest -q`, both .NET helper/watcher builds succeeded with
  `0` warnings and `0` errors, install CLI smoke passed, full deterministic
  harness passed, and `git diff --check` passed.
- Stage V1 evidence merged through PR #26, and post-merge `main` Windows
  Harness run `25033323560` passed on
  `55ba9cc321b5e9d9153af792286ca91dfab51d04`.
- Stage V2 manual smoke refresh used artifact root
  `C:\Users\34793\AppData\Local\Temp\winchronicle-final-v2-smoke-20260428-0410`
  and temporary watcher state
  `C:\Users\34793\AppData\Local\Temp\winchronicle-final-v2-watch-state-20260428-0410`.
- Notepad targeted UIA smoke passed; artifact path:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-final-v2-smoke-20260428-0410\notepad\notepad-capture.json`.
- Edge targeted UIA smoke passed; artifact path:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-final-v2-smoke-20260428-0410\edge\edge-capture.json`.
- `code.cmd` was available at
  `C:\Users\34793\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd`.
- VS Code metadata smoke passed with the known Monaco editor-marker diagnostic
  warning; artifact path:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-final-v2-smoke-20260428-0410\vscode-metadata\vscode-capture.json`.
- VS Code strict Monaco marker failed as the documented diagnostic/non-blocking
  limitation; artifact path:
  `C:\Users\34793\AppData\Local\Temp\winchronicle-final-v2-smoke-20260428-0410\vscode-strict\vscode-capture.json`.
- Live watcher preview with real watcher/helper returned `captures_written: 0`,
  `denylisted_skipped: 0`, `duplicates_skipped: 0`, and `heartbeats: 10` over a
  5-second run with temporary `WINCHRONICLE_HOME`. A direct frontmost capture
  smoke in this agent-hosted desktop returned `SKIPPED: helper returned no
  capture`, so the live watcher result remains heartbeat-only diagnostic
  evidence; deterministic watcher and fake-helper preview gates remain covered
  by `python harness/scripts/run_harness.py`.
