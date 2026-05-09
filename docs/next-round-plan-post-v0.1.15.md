# WinChronicle Post-v0.1.15 Maintenance Plan

## Summary

`v0.1.15` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.15. The release tag
targets `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`. The post-publication
reconciliation on `main` is
`54208c51819a45140e355272d8cb3f0e3fbff900`, and Windows Harness run
`25589775129` passed on that SHA.

The post-v0.1.15 baseline is green. Package/runtime/MCP version identity
reports `0.1.15`, and the previous maintenance round changed documentation,
tests, GitHub metadata evidence, deterministic harness evidence, compatibility
evidence, release-planning records, and version metadata only. It did not
change product behavior, schemas, CLI/MCP JSON shape, privacy behavior,
helper/watcher behavior, or capture surfaces.

This next round should continue blueprint-aligned maintenance without
expanding the v0.1 product boundary. The focus is evidence freshness, operator
entry clarity, helper/watcher preview diagnostics, MCP/memory contract
stability, compatibility guardrail evidence, and any small drift discovered by
those checks. It must not start Phase 6 implementation.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, no polling capture loop, and no default background capture.

## Execution Cursor

- Current stage: AD5 - v0.1.16-rc.0 Published Prerelease Reconciliation.
- Stage status: A - `v0.1.16-rc.0` is published as a prerelease; publication
  reconciliation is in progress.
- Last completed evidence: AD4 added the post-v0.1.15 compatibility guardrail
  sweep and two narrow privacy/compatibility drift fixes in PR #139, merged as
  `2c7d0b0b24d9a159c084f262cb24ec7ee9873a39`, and post-merge `main` Windows
  Harness run `25595513141` passed.
- Last validation: final pre-publication `main` Windows Harness run
  `25596273094` passed on `70caf364f68d8c159eb74bbbc23e7469db22a244`, and
  GitHub published `v0.1.16-rc.0` as a prerelease at that tag target.
- Next atomic task: complete the `v0.1.16-rc.0` publication reconciliation PR
  by recording the release URL, tag target, and final post-publication
  Windows Harness evidence.
- Known blockers: post-publication reconciliation PR and post-merge Windows
  Harness evidence are pending.

## Phased Work

### Stage AD0 - Post-v0.1.15 Baseline Cursor

- Add this post-v0.1.15 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Update docs tests so `v0.1.15` is the latest published release, this plan is
  the active cursor, and post-v0.1.14 is completed historical context.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, version metadata, or privacy behavior.

### Stage AD1 - Public Metadata And Evidence Freshness Follow-up

- Re-check public-facing repository evidence after `v0.1.15`: README,
  operator docs, release metadata, and GitHub repository metadata.
- Record manually maintained public metadata gaps as checklist items, not
  product-code changes.
- Refresh only documentation/tests needed to keep evidence freshness clear.
- Do not require fresh manual UIA smoke unless helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior, product
  CLI/MCP shape, capture surfaces, or release approver requirements changed.

### Stage AD2 - Helper And Watcher Preview Diagnostics Review

- Review helper and watcher preview diagnostics docs, scorecards, and tests
  against the roadmap lanes for UIA helper hardening and watcher preview.
- Strengthen documentation, deterministic tests, or narrow diagnostic code only
  for discovered drift in timeout, malformed output, no observed-content echo,
  duplicate skip, denylist skip, heartbeat-only diagnostics, or diagnostic
  artifact policy.
- Keep real UIA smoke manual and outside default CI.
- Do not add helper product targeting, daemon/service install, polling capture
  loops, default background capture, screenshots, OCR, audio, keyboard,
  clipboard, network calls, LLM calls, or desktop control.

### Stage AD3 - MCP And Memory Contract Review

- Re-check read-only MCP examples, memory docs, deterministic demo guidance,
  and scorecards for trust-boundary and response-shape consistency.
- Strengthen narrow docs/tests only if examples drift from the exact read-only
  MCP tool list or durable memory contract.
- Do not add MCP write tools, arbitrary file reads, desktop control tools,
  screenshot/OCR/audio/keyboard/clipboard/network tools, or LLM
  reducer/classifier calls.

### Stage AD4 - Compatibility Guardrail Sweep

- Re-run deterministic gates and confirm the v0.1 boundary still holds.
- Treat existing tests and scorecards as compatibility oracles for version
  identity, exact read-only MCP tool list, disabled privacy surfaces, observed
  content trust boundaries, Phase 6 spec-only status, watcher preview limits,
  durable memory contract, and product targeted capture absence.
- Strengthen tests only for discovered drift.

### Stage AD5 - v0.1.16-rc.0 Release Candidate Readiness

- Because AD2-AD4 include compatible privacy/runtime drift fixes, prepare a
  `v0.1.16-rc.0` release candidate before any direct `v0.1.16` final.
- Before prerelease, align package and server version metadata to `0.1.16`,
  add a release-candidate record, and record local gates plus PR and
  post-merge Windows Harness evidence.
- The release-candidate record must explicitly justify that the AD2-AD4 fixes
  narrow exposure without adding schemas, CLI/MCP JSON shape changes, MCP tool
  schemas, helper/watcher capture expansion, or capture surfaces.
- Publication remains gated on local, PR, and post-merge validation plus
  explicit prerelease publication approval.

## Public Interfaces And Non-goals

- CLI remains unchanged:
  `init/status/capture-once/capture-frontmost/watch/privacy-check/search-captures/generate-memory/search-memory/mcp-stdio`.
- MCP tool list remains unchanged and read-only:
  `current_context/search_captures/search_memory/read_recent_capture/recent_activity/privacy_status`.
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

- AD0: docs tests confirm `v0.1.15` is latest published, this plan is active,
  and post-v0.1.14 is completed historical context.
- AD1: public metadata and evidence freshness follow-up separates current
  evidence from inherited/manual evidence and does not expand product scope.
- AD2: helper/watcher diagnostics evidence stays preview-only and does not add
  live UIA smoke to default CI.
- AD3: MCP/memory examples preserve exact read-only MCP tools, stable response
  shapes, and `trust = "untrusted_observed_content"`.
- AD4: compatibility guardrails still prove exact MCP read-only tools,
  disabled privacy surfaces, product targeted capture absence, and Phase 6
  spec-only status.
- AD5: release-candidate record includes local, PR, post-merge, release URL,
  tag target, rollback notes, privacy/scope confirmation, and manual smoke
  freshness decision.

## Assumptions

- `v0.1.15` is the current stable published baseline and must not be retagged.
- The next prerelease target is `v0.1.16-rc.0`; direct `v0.1.16` final must
  wait for separate final-readiness evidence after the runtime/privacy fixes
  have been reviewed through a release candidate.
- Manual UIA smoke remains outside default CI.
- Fresh manual UIA smoke is required for AD5 unless the release owner records
  an explicit exception, because AD2-AD4 changed privacy/runtime behavior while
  keeping capture surfaces closed.
- Phase 6 stays at spec/scorecard level for this round.

## Decision Log

- Chose a compatible `v0.1.16` maintenance target because the published
  `v0.1.15` round changed documentation, tests, GitHub metadata evidence,
  deterministic harness evidence, compatibility evidence, release-planning
  records, and version metadata only, without product behavior changes.
- Chose AD0 as a docs-only active cursor so post-v0.1.15 work does not begin
  from a completed post-v0.1.14 plan.
- Chose AD1 as a docs-only public metadata audit because the repository
  metadata gaps are maintainer settings, not product-code blockers.
- Chose AD2 as a helper/watcher diagnostics sweep because the roadmap asks for
  preview diagnostics evidence without expanding live capture paths.
- Promoted a narrow AD2 privacy diagnostic fix after review found that
  title-denylist skip reasons could echo matched window titles.
- Chose AD3 as an MCP/memory contract sweep because existing tests and
  scorecards define exact read-only tools, memory search parity, and
  trust-boundary evidence.
- Promoted a narrow AD3 documentation fix after review found the
  `privacy_status` MCP example omitted existing local-state fields.
- Promoted a narrow AD3 read-only search parity fix after review found MCP
  filtered search could drop valid matches beyond the first 50 raw results.
- Chose AD4 as a compatibility guardrail sweep because AD1-AD3 included
  compatible drift fixes and the direct `v0.1.16` path requires current
  evidence for the exact read-only MCP tools, disabled privacy surfaces,
  watcher preview limits, durable memory contract, product targeted capture
  absence, and Phase 6 spec-only status.
- Promoted narrow AD4 guardrail fixes after review found broader obvious-token
  canaries and helper/watcher pass-through target/control/privacy flag
  rejection were not covered by deterministic tests.
- Chose a `v0.1.16-rc.0` release-candidate path for AD5 because review found
  AD2-AD4 are compatible privacy/runtime drift fixes rather than docs-only
  changes. The direct `v0.1.16` final path remains blocked until prerelease
  review evidence is recorded.
- Kept Phase 6 out of scope because the screenshot/OCR scorecard remains a
  planning contract, not implementation authorization.

## Validation Log

- Stage AD0 initialization:
  - `gh release view v0.1.15 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt,name` - passed; `v0.1.15` is published, not a draft or prerelease, published at `2026-05-09T02:44:06Z`, and targets `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`.
  - `git rev-parse v0.1.15` - passed and printed `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`.
  - `gh run view 25589775129 --json databaseId,status,conclusion,headSha,url,displayTitle` - passed; post-publication reconciliation `main` Windows Harness concluded `success` on `54208c51819a45140e355272d8cb3f0e3fbff900`.
  - `git rev-parse HEAD` - passed and printed `54208c51819a45140e355272d8cb3f0e3fbff900`.
  - `python -c "import winchronicle; print(winchronicle.__version__)"` - passed and printed `0.1.15`.
- Stage AD0 completion:
  - PR #135 Windows Harness run `25593554670` - passed.
  - PR #135 merged as `90fff5cc25b770634c92669e70c4067b58a8a6ea`.
  - `gh run view 25593607384 --json databaseId,status,conclusion,headSha,url,displayTitle` - passed; post-AD0 `main` Windows Harness concluded `success` on `90fff5cc25b770634c92669e70c4067b58a8a6ea`.
- Stage AD1 initialization:
  - `gh repo view YSCJRH/WinChronicle --json nameWithOwner,visibility,defaultBranchRef,description,homepageUrl,repositoryTopics,url` - passed; repository is public on `main`, with empty description, homepage, and topics.
  - `gh release view v0.1.15 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt,name` - passed; `v0.1.15` is published, not a draft or prerelease, and targets `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`.
- Stage AD1 local validation:
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed; 48 tests passed.
  - `python harness/scripts/run_harness.py` - passed; includes 139 pytest tests, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search/memory, and preview watcher smoke.
  - `git diff --check` - passed.
- Stage AD1 completion:
  - PR #136 Windows Harness run `25593788484` - passed.
  - PR #136 merged as `f2a7fbd3ef66275f0688015955d32e58ed330b1f`.
  - `gh run view 25593871698 --json databaseId,status,conclusion,headSha,url,displayTitle` - passed; post-AD1 `main` Windows Harness concluded `success` on `f2a7fbd3ef66275f0688015955d32e58ed330b1f`.
- Stage AD2 initialization:
  - Reviewed `docs/uia-helper-quality-matrix.md`, `docs/watcher-preview.md`, `docs/operator-diagnostics.md`, and `harness/scorecards/capture-quality.md`.
  - `rg "helper timed out|invalid JSON|empty stdout|watcher timed out|malformed JSONL|duplicates_skipped|denylisted_skipped|raw watcher JSONL|capture-on-start|helper failed" tests src harness docs -n` - reviewed; deterministic helper/watcher diagnostics coverage is present in tests, scorecards, and docs.
  - Review found title-denylist skip reasons could echo matched window titles; AD2 added deterministic no-echo tests and changed Python/helper title-denylist diagnostics to `denylisted title pattern`.
- Stage AD2 focused validation:
  - `python -m pytest tests/test_privacy_check.py tests/test_cli.py tests/test_uia_helper_contract.py tests/test_operator_diagnostics_docs.py -q` - passed; 57 tests passed.
  - `python -m pytest tests/test_watcher_events.py tests/test_operator_diagnostics_docs.py -q` - passed; 48 tests passed.
- Stage AD2 local validation:
  - `python -m pytest -q` - passed; 144 tests passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed; includes 144 pytest tests, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search/memory, and preview watcher smoke.
  - `git diff --check` - passed.
- Stage AD2 completion:
  - PR #137 Windows Harness run `25594230290` - passed.
  - PR #137 merged as `37335cd2cefabab4fa9e500b58ede2e96d1cb2de`.
  - `gh run view 25594302410 --json databaseId,status,conclusion,headSha,url,displayTitle` - passed; post-AD2 `main` Windows Harness concluded `success` on `37335cd2cefabab4fa9e500b58ede2e96d1cb2de`.
- Stage AD3 initialization:
  - Reviewed `docs/mcp-readonly-examples.md`, `docs/deterministic-demo.md`, `harness/scorecards/mcp-quality.md`, `harness/scorecards/memory-quality.md`, `docs/operator-quickstart.md`, `tests/test_mcp_tools.py`, and `tests/test_memory_pipeline.py`.
  - `rg -n "current_context|search_captures|search_memory|read_recent_capture|recent_activity|privacy_status|untrusted_observed_content|entries_fts|idempotent|No write/control/file/screenshot/OCR/audio/keyboard/clipboard/network" docs harness tests src` - reviewed; deterministic MCP/memory trust-boundary and exact-tool coverage is present in tests, scorecards, docs, and source contracts.
  - Review found the `privacy_status` MCP example omitted existing `home`, `db_exists`, and `capture_count` response fields and the `read_recent_capture` example showed `url: null` instead of the public empty-string storage shape; AD3 updated the examples and tests to match the implementation.
  - Review found MCP filtered search could miss valid matches beyond the first 50 raw results; AD3 added deterministic >50-result parity tests and moved capture/memory filters into SQLite search.
- Stage AD3 focused validation:
  - `python -m pytest tests/test_mcp_tools.py tests/test_memory_pipeline.py tests/test_operator_diagnostics_docs.py -q` - passed; 51 tests passed.
- Stage AD3 local validation:
  - `python -m pytest -q` - passed; 147 tests passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed; includes 147 pytest tests, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search/memory, and preview watcher smoke.
  - `git diff --check` - passed.
- Stage AD3 completion:
  - PR #138 Windows Harness run `25594817396` - passed.
  - PR #138 merged as `1f1f55b262a89ca41991401de493791dd1c41e5c`.
  - `gh run view 25594896165 --json databaseId,status,conclusion,headSha,url,displayTitle` - passed; post-AD3 `main` Windows Harness concluded `success` on `1f1f55b262a89ca41991401de493791dd1c41e5c`.
- Stage AD4 initialization:
  - Reviewed `docs/compatibility-guardrail-sweep-post-v0.1.14.md`, `tests/test_compatibility_contracts.py`, `tests/test_mcp_tools.py`, `tests/test_phase6_privacy_scorecard.py`, `tests/test_watcher_events.py`, `tests/test_state_compatibility.py`, `tests/test_memory_pipeline.py`, `tests/test_version_identity.py`, `harness/scorecards`, `docs/mcp-readonly-examples.md`, `docs/watcher-preview.md`, `docs/deterministic-demo.md`, `docs/roadmap.md`, `CONTRIBUTING.md`, `.github`, `README.md`, and `docs/operator-quickstart.md`.
  - `python -m pytest tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py tests/test_version_identity.py -q` - passed; 48 tests passed.
  - `rg -n -e "--hwnd|--pid|--window-title|--window-title-regex|--process-name|screenshot|ocr|audio|keyboard|clipboard|network_upload|cloud_upload|llm_calls|desktop_control|write_memory|read_file|click|type" src/winchronicle tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py harness/scorecards docs/mcp-readonly-examples.md docs/watcher-preview.md docs/deterministic-demo.md docs/roadmap.md CONTRIBUTING.md .github` - reviewed; matches are existing disabled-surface contracts, sentinels, documentation, scorecards, deterministic fixtures/tests, schema field names, and allowed helper-only harness wording.
  - `rg -n -g "*.py" -g "*.cs" -g "*.md" -g "*.json" -g "*.yml" -e "SetForegroundWindow|AttachThreadInput|SendInput|mouse_event|keybd_event|GetAsyncKeyState|OpenClipboard|GetClipboardData|BitBlt|CopyFromScreen|PrintWindow|Tesseract|OpenAI|Anthropic|requests|httpx|aiohttp|selenium|playwright" src resources tests harness .github docs CONTRIBUTING.md README.md` - reviewed; matches are prior compatibility sweep command text, historical plan evidence, privacy-policy canary text, deterministic fixture/golden content, explicit forbidden-term tests, and the local MCP smoke request variable name. No new runtime dependency or implementation path was found.
  - Review found the secret redaction guardrail did not cover newer obvious GitHub/Slack token families or long labeled API-key values; AD4 added deterministic canaries and broadened redaction patterns.
  - Review found product helper/watcher pass-through arguments were not covered by targeted-capture absence tests; AD4 now rejects disabled target/control/privacy-surface flags in `--helper-arg` and `--watcher-arg`.
- Stage AD4 focused drift-fix validation:
  - `python -m pytest tests/test_redaction.py tests/test_compatibility_contracts.py -q` - passed; 6 tests passed.
- Stage AD4 related docs/privacy validation:
  - `python -m pytest tests/test_redaction.py tests/test_privacy_check.py tests/test_golden.py tests/test_operator_diagnostics_docs.py -q` - passed; 41 tests passed.
- Stage AD4 local validation:
  - `python -m pytest -q` - passed; 148 tests passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed; includes 148 pytest tests, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search/memory, and preview watcher smoke.
  - `git diff --check` - passed.
- Stage AD4 completion:
  - PR #139 Windows Harness run `25595449096` - passed.
  - PR #139 merged as `2c7d0b0b24d9a159c084f262cb24ec7ee9873a39`.
  - `gh run view 25595513141 --json databaseId,status,conclusion,headSha,url,displayTitle` - passed; post-AD4 `main` Windows Harness concluded `success` on `2c7d0b0b24d9a159c084f262cb24ec7ee9873a39`.
- Stage AD5 initialization:
  - `gh release view v0.1.16` - failed with release-not-found, confirming `v0.1.16` is not published.
  - `git tag --list "v0.1.16*"` - passed and printed no matching local tags.
  - `git rev-parse HEAD` - passed and printed `2c7d0b0b24d9a159c084f262cb24ec7ee9873a39`.
  - `git rev-parse v0.1.15` - passed and printed `4869ce7b5b0f6ad3ab41c844e4f010640c0c36c2`.
  - Release-readiness review found the direct `v0.1.16` final path should stop because AD2-AD4 include compatible privacy/runtime drift fixes; AD5 now prepares `v0.1.16-rc.0` instead.
- Stage AD5 manual smoke validation:
  - `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-notepad.ps1 -ArtifactDir <artifact-root>\notepad -TimeoutSeconds 30` - passed; artifact `<artifact-root>\notepad\notepad-capture.json`.
  - `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-edge.ps1 -ArtifactDir <artifact-root>\edge -TimeoutSeconds 45` - passed; artifact `<artifact-root>\edge\edge-capture.json`.
  - `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -ArtifactDir <artifact-root>\vscode-metadata -TimeoutSeconds 45` - passed with diagnostic warning; metadata passed, editor marker was not exposed through UIA.
  - `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -Strict -ArtifactDir <artifact-root>\vscode-strict -TimeoutSeconds 45` - diagnostic failure, non-blocking; known Monaco/UIA limitation.
  - `python -m winchronicle watch --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper dotnet --helper-arg resources/win-uia-helper/bin/Debug/net8.0-windows/win-uia-helper.dll --duration 5 --depth 2 --heartbeat-ms 500 --capture-on-start` with temporary `WINCHRONICLE_HOME` - passed; `captures_written: 3`, `heartbeats: 7`, `duplicates_skipped: 1`, `denylisted_skipped: 0`.
- Stage AD5 local validation:
  - `python -c "import winchronicle; print(winchronicle.__version__)"` - passed and printed `0.1.16`.
  - `python -m pytest tests/test_version_identity.py tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py -q` - passed; 52 tests passed.
  - `python -m pytest -q` - passed; 149 tests passed.
  - `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` - passed, 0 warnings, 0 errors.
  - `python harness/scripts/run_install_cli_smoke.py` - passed.
  - `python harness/scripts/run_harness.py` - passed; includes 149 pytest tests, helper build, watcher build, watcher smoke, MCP smoke, install CLI smoke, fixture capture/search/memory, fixture watcher, and preview watcher smoke.
  - `git diff --check` - passed.
- Stage AD5 readiness PR completion:
  - PR #140 Windows Harness run `25596082939` - passed.
  - PR #140 merged as `bca4b6485f194a46bca7fa6e1e3866b5105479da`.
  - `gh run view 25596122521 --json databaseId,status,conclusion,headSha,url,displayTitle` - passed; post-AD5-readiness `main` Windows Harness concluded `success` on `bca4b6485f194a46bca7fa6e1e3866b5105479da`.
- Stage AD5 CI evidence PR completion:
  - PR #141 Windows Harness run `25596204971` - passed.
  - PR #141 merged as `70caf364f68d8c159eb74bbbc23e7469db22a244`.
  - `gh run view 25596273094 --json databaseId,status,conclusion,headSha,url,displayTitle` - passed; final pre-publication `main` Windows Harness concluded `success` on `70caf364f68d8c159eb74bbbc23e7469db22a244`.
- Stage AD5 prerelease publication:
  - `gh release create v0.1.16-rc.0 --target 70caf364f68d8c159eb74bbbc23e7469db22a244 --title "v0.1.16-rc.0" --prerelease --notes ...` - passed.
  - `gh release view v0.1.16-rc.0 --json tagName,url,targetCommitish,isDraft,isPrerelease,publishedAt,name` - passed; the release is published, not a draft, marked prerelease, published at `2026-05-09T08:18:01Z`, and targets `70caf364f68d8c159eb74bbbc23e7469db22a244`.
  - `git fetch --tags --force` - passed and fetched `v0.1.16-rc.0`.
  - `git ls-remote --tags origin v0.1.16-rc.0` - passed and printed `70caf364f68d8c159eb74bbbc23e7469db22a244`.
