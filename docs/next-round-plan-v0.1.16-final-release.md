# WinChronicle v0.1.16 Final Release Plan

## Summary

`v0.1.16-rc.0` is published as a prerelease at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16-rc.0. The
prerelease tag targets `70caf364f68d8c159eb74bbbc23e7469db22a244`, and the
release is not a draft.

The current `main` baseline after prerelease publication reconciliation is
`b260ebaa8808bddcce20da166038511de23bf3b5`. Windows Harness run
`25596579705` passed on that SHA. The diff from `v0.1.16-rc.0` to current
`main` is documentation and documentation-test evidence only:

- `docs/manual-smoke-evidence-ledger.md`
- `docs/next-round-plan-post-v0.1.15.md`
- `docs/release-candidate-v0.1.16-rc.0.md`
- `docs/release-checklist.md`
- `docs/release-evidence.md`
- `tests/test_compatibility_evidence_docs.py`
- `tests/test_operator_diagnostics_docs.py`

No product code, schemas, CLI/MCP JSON shape, helper/watcher behavior, privacy
runtime behavior, or capture surfaces changed after the prerelease tag.

This plan was the active final-release cursor after `v0.1.16-rc.0` and is now
completed historical final-release evidence. It did not publish `v0.1.16` by
itself. Direct final release proceeded only after fresh final gates, explicit
final manual smoke evidence, a final release record, review, PR and post-merge
Windows Harness validation, and explicit publication approval. If future
release-readiness work requires any product or contract change, stop the direct
final path and prepare a new release-candidate path instead.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, no polling capture loop, and no default background capture.

## Execution Cursor

- Current stage: AE4 - v0.1.16 Final Publication Reconciliation.
- Stage status: AE4 complete; `v0.1.16` is published as the latest stable
  release and this final-release plan is complete.
- Last completed evidence: AE3 release-record PR #147 merged as
  `255f2a01cddde330d756a87359c4d3a8be4b11a2`, post-merge Windows Harness run
  `25597678444` passed, and GitHub release publication passed for
  `v0.1.16`.
- Last validation: `v0.1.16` release metadata, final tag target, remote tag,
  and `v0.1.16-rc.0` prerelease metadata were verified after publication.
- Next atomic task: start the post-`v0.1.16` maintenance cursor in
  [Post-v0.1.16 maintenance plan](next-round-plan-post-v0.1.16.md).
- Known blockers: none for the published `v0.1.16` final release.

## Phased Work

### Stage AE0 - Post-v0.1.16-rc.0 Final Baseline Decision

- Add this active final-release plan and keep the post-v0.1.15 plan as the
  completed prerelease path.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators start from this final
  cursor.
- Verify `v0.1.16-rc.0` is published, `v0.1.16` is not published, current
  `main` has green Windows Harness evidence, and tag-to-main drift is
  docs/tests-only.
- Do not publish or retag `v0.1.16` during AE0.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, privacy behavior, capture surfaces, version metadata, or release
  tags.

### Stage AE1 - Deterministic Final Gate Refresh

- Run the full deterministic final gate set on the current final target:
  pytest, helper build, watcher build, install CLI smoke, full harness, and
  `git diff --check`.
- Confirm package/runtime/MCP version identity remains `0.1.16`.
- Confirm exact read-only MCP tool list, disabled privacy surfaces, product
  targeted capture absence, watcher preview limits, durable memory contract,
  and Phase 6 spec-only status remain unchanged.
- If any product or contract fix is required, stop the direct final path and
  prepare `v0.1.16-rc.1`.

### Stage AE2 - Manual Final Smoke Refresh

- Rerun fresh final manual UIA smoke instead of automatically inheriting the
  `v0.1.16-rc.0` smoke result:
  - Notepad targeted UIA smoke: hard gate.
  - Edge targeted UIA smoke: hard gate.
  - VS Code metadata smoke: hard gate when `code.cmd` is available.
  - VS Code strict Monaco marker: diagnostic and non-blocking.
  - Watcher preview live smoke: preview diagnostic/manual confidence gate.
- Record commands, pass/fail results, timestamps, environment notes, and local
  artifact paths only.
- Do not commit raw helper JSON, raw watcher JSONL, screenshots, OCR output,
  observed text, local page contents, editor buffer contents, passwords,
  secrets, or token canaries.

### Stage AE3 - v0.1.16 Final Release Record And Publication

- Add `docs/release-v0.1.16.md` using the established final release record
  shape: metadata, deterministic gates, manual smoke, watcher preview, release
  notes, privacy/scope, rollback, and publication decision.
- Update docs tests and operator entry points to distinguish the final release
  record from the prerelease candidate record.
- Open a reviewed PR and require Windows Harness success before merge.
- Publish `v0.1.16` only after explicit publication approval. The final tag
  should target the post-merge `main` SHA that contains the final release
  record and passed Windows Harness.
- If publication is not approved or a product/contract change is required,
  do not publish final; prepare the next release-candidate path instead.

### Stage AE4 - v0.1.16 Final Publication Reconciliation

- Verify the GitHub release URL, final tag target, draft status, prerelease
  status, published timestamp, and remote tag.
- Update README, operator quickstart, release checklist, release evidence
  guide, manual smoke evidence ledger, and tests so `v0.1.16` is the latest
  published release.
- Add the post-`v0.1.16` maintenance cursor after final publication.
- Record PR Windows Harness and post-merge `main` Windows Harness evidence.

## Public Interfaces And Non-goals

- CLI remains unchanged:
  `init/status/capture-once/capture-frontmost/watch/privacy-check/search-captures/generate-memory/search-memory/mcp-stdio`.
- MCP tool list remains unchanged and read-only: `current_context`,
  `search_captures`, `search_memory`, `read_recent_capture`,
  `recent_activity`, and `privacy_status`.
- Product CLI still does not expose targeted `--hwnd`, `--pid`,
  `--window-title`, `--window-title-regex`, or `--process-name` capture flags.
- Do not implement screenshot capture, OCR, audio recording, keyboard capture,
  clipboard capture, network upload, LLM calls, desktop control, MCP write
  tools, arbitrary file read tools, daemon/service install, polling capture
  loop, default background capture, or product targeted capture.
- Phase 6 remains privacy spec/scorecard only unless a future plan explicitly
  authorizes tests-first implementation.

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

- AE0: docs tests confirmed this final-release plan was the active cursor, the
  post-v0.1.15 plan was the completed prerelease path, and `v0.1.16-rc.0` was
  the published prerelease before final publication.
- AE1: deterministic gates pass on the current final target without requiring
  product or contract changes.
- AE2: fresh final manual UIA smoke is recorded with local artifact paths only.
- AE3: final release record includes local, PR, post-merge, privacy/scope,
  rollback, manual smoke, publication approval, release URL, and tag target
  evidence.
- AE4: publication reconciliation confirms `v0.1.16` is the latest published
  release and opens the post-final maintenance cursor.

## Assumptions

- `v0.1.16` is the published final release and must not be retagged.
- `v0.1.16-rc.0` is historical prerelease evidence and must not be retagged.
- Version identity is already aligned to `0.1.16`.
- Tag-to-main drift after `v0.1.16-rc.0` is docs/tests-only at AE0.
- No required soak window after `v0.1.16-rc.0` has been recorded. If a release
  owner requires one, record it before AE3 publication.
- Fresh final manual UIA smoke is required by this plan before final
  publication.
- Phase 6 stays at spec/scorecard level for this final-release path.

## Decision Log

- Chose a direct-final planning cursor because `v0.1.16-rc.0` is published,
  current `main` is green, and the post-prerelease drift is docs/tests-only.
- Chose not to publish `v0.1.16` in AE0 because final-release evidence,
  manual smoke freshness, reviewed final release record, and publication
  approval are still missing.
- Chose fresh manual final smoke for AE2 because the manual smoke ledger
  requires a final freshness decision and AD5 smoke should not silently become
  final evidence.
- Chose `v0.1.16-rc.1` as the fallback if final-readiness review requires any
  product or contract change.
- Completed AE0 through PR #144 and post-merge Windows Harness before moving
  to deterministic final gates.
- Kept the direct final path open after AE1 because all deterministic final
  gates passed and no product or contract change was required.
- Completed AE2 with fresh final manual UIA smoke, while preserving the known
  VS Code strict Monaco diagnostic as non-blocking.
- Prepared `docs/release-v0.1.16.md` for AE3 so final publication has an
  auditable release decision record before the tag is created.
- Published `v0.1.16` final after PR #147 and post-merge Windows Harness
  passed on the final tag target.
- Opened the post-`v0.1.16` maintenance cursor for follow-up work.

## Validation Log

- Stage AE0 initialization:
  - `gh release view v0.1.16-rc.0 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; the release is published, not a draft, marked prerelease, published at `2026-05-09T08:18:01Z`, and targets `70caf364f68d8c159eb74bbbc23e7469db22a244`.
  - `git rev-parse v0.1.16-rc.0` - passed and printed `70caf364f68d8c159eb74bbbc23e7469db22a244`.
  - `gh release view v0.1.16 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt,name` - failed with `release not found`, confirming `v0.1.16` is not published.
  - `git tag --list "v0.1.16*"` - passed and printed only `v0.1.16-rc.0`.
  - `git rev-parse HEAD` - passed and printed `b260ebaa8808bddcce20da166038511de23bf3b5`.
  - `gh run view 25596579705 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-prerelease-reconciliation `main` Windows Harness concluded `success` on `b260ebaa8808bddcce20da166038511de23bf3b5`.
  - `git diff --name-status v0.1.16-rc.0..HEAD` - passed; the diff listed only documentation and documentation-test evidence files.
- Stage AE0 completion:
  - PR #144 Windows Harness run `25596958129` - passed.
  - PR #144 merged as `c61c52ca67e40f689223d8307738f9b49f09deee`.
  - `gh run view 25597001825 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AE0 `main` Windows Harness concluded `success` on `c61c52ca67e40f689223d8307738f9b49f09deee`.
- Stage AE1 deterministic final gate refresh:
  - `git rev-parse HEAD` - passed and printed `c61c52ca67e40f689223d8307738f9b49f09deee`.
  - `python -m pytest -q` - passed; 151 tests passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed; includes 151 pytest tests, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search/memory, fixture watcher, and preview watcher smoke.
  - `git diff --check` - passed.
- Stage AE1 completion:
  - PR #145 Windows Harness run `25597196866` - passed.
  - PR #145 merged as `d990b77c0bd60b850c22f5783bf0126a8e137aa8`.
  - `gh run view 25597248992 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AE1 `main` Windows Harness concluded `success` on `d990b77c0bd60b850c22f5783bf0126a8e137aa8`.
- Stage AE2 manual final smoke validation:
  - `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-notepad.ps1 -ArtifactDir <artifact-root>\notepad -TimeoutSeconds 30` - passed; artifact `<artifact-root>\notepad\notepad-capture.json`.
  - `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-edge.ps1 -ArtifactDir <artifact-root>\edge -TimeoutSeconds 45` - passed; artifact `<artifact-root>\edge\edge-capture.json`.
  - `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -ArtifactDir <artifact-root>\vscode-metadata -TimeoutSeconds 45` - passed with diagnostic warning; metadata passed, editor marker was not exposed through UIA.
  - `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -Strict -ArtifactDir <artifact-root>\vscode-strict -TimeoutSeconds 45` - diagnostic failure, non-blocking; known Monaco/UIA limitation.
  - `python -m winchronicle watch --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper dotnet --helper-arg resources/win-uia-helper/bin/Debug/net8.0-windows/win-uia-helper.dll --duration 5 --depth 2 --heartbeat-ms 500 --capture-on-start` with temporary `WINCHRONICLE_HOME` - passed; `captures_written: 3`, `heartbeats: 6`, `duplicates_skipped: 1`, `denylisted_skipped: 0`.
  - Artifact root: `C:\Users\34793\AppData\Local\Temp\winchronicle-ae2-final-smoke-a3da7c0177fc42059a484cf07435777a`. Local artifacts were not committed.
- Stage AE2 completion:
  - PR #146 Windows Harness run `25597418104` - passed.
  - PR #146 merged as `1ea902a8630b9d0b18397af69cfcd84a9ce4d24a`.
  - `gh run view 25597463319 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AE2 `main` Windows Harness concluded `success` on `1ea902a8630b9d0b18397af69cfcd84a9ce4d24a`.
- Stage AE3 final release record preparation:
  - Added `docs/release-v0.1.16.md` with deterministic gate evidence, manual
    smoke evidence, watcher preview evidence, release notes, compatibility
    evidence, privacy/scope confirmation, rollback notes, and publication
    decision summary.
  - Publication was pending until this AE3 PR and post-merge `main` Windows
    Harness passed.
- Stage AE3 completion:
  - PR #147 Windows Harness run `25597623991` - passed.
  - PR #147 merged as `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `gh run view 25597678444 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AE3 `main` Windows Harness concluded `success` on `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
- Stage AE3 final publication:
  - `gh release create v0.1.16 --target 255f2a01cddde330d756a87359c4d3a8be4b11a2 --title "v0.1.16" --notes ...` - passed.
  - `gh release view v0.1.16 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; the release is published, not a draft, not a prerelease, published at `2026-05-09T09:31:17Z`, and targets `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `git rev-parse v0.1.16` - passed and printed `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `git ls-remote --tags origin v0.1.16` - passed and printed `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
  - `gh release view v0.1.16-rc.0 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt,name` - passed; the prerelease remains published and targets `70caf364f68d8c159eb74bbbc23e7469db22a244`.
