# v0.1.0 Final Readiness Plan

## Summary

`v0.1.0-rc.0` is published and green at
`069e8cff9434c83b00a7a857aaf9eee441cf16ff`. The next round prepares
WinChronicle for `v0.1.0` final by reconciling published evidence, tightening
privacy contracts, and freezing UIA helper, watcher, MCP, memory, and local
state behavior. If any product behavior, schema, CLI/MCP JSON shape, privacy
contract, or `src/`/`resources/` code changes, the next public release must be
`v0.1.0-rc.1` rather than final.

The product boundary remains unchanged: local-first, UIA-first, harness-first,
read-only MCP first, no screenshot/OCR implementation, no audio recording, no
keyboard capture, no clipboard capture, no network upload, no LLM calls, no
desktop control, and no product targeted capture flags.

## Execution Cursor

- Current stage: Stage F5 - Final Or rc.1 Release Decision.
- Stage status: F - F5 release decision evidence is merged and post-merge
  `main` Windows Harness passed; `v0.1.0-rc.1` publication approval is still
  pending.
- Last completed evidence: `docs/release-candidate-v0.1.0-rc.1.md` records
  that F1 changed CLI/MCP JSON shape and privacy behavior, so the next public
  candidate must be `v0.1.0-rc.1` rather than direct final. Deterministic and
  manual smoke evidence are recorded without committing observed-content
  artifacts.
- Last validation: local deterministic gates, manual Notepad/Edge/VS Code
  smoke, watcher preview, PR Windows Harness, post-merge `main` Windows Harness,
  and `git diff --check` passed or were recorded as diagnostic where
  appropriate.
- Next atomic task: request explicit approval to publish `v0.1.0-rc.1`; before
  publishing, verify the current `main` SHA and use that SHA as the tag target.
- Known blockers: none.

## Phased Work

### Stage F0 - Published Baseline Reconciliation

- Update rc.0 records to reflect the actual published prerelease, tag target,
  release URL, PR Windows Harness, and post-merge Windows Harness.
- Create this post-rc.0 final-readiness plan so the rc.0 readiness plan no
  longer carries the next execution cursor.
- Do not modify product code, schemas, fixtures, helper/watcher behavior, CLI
  JSON shape, MCP shape, or scorecards.

### Stage F1 - Privacy Contract Parity

- Add tests before behavior or doc changes.
- Align CLI `status`, MCP `privacy_status`, scorecards, operator docs, and
  privacy specs on the same disabled surfaces and trust boundary.
- Update stale privacy language that still describes WinChronicle as
  fixture-only; rc.0 includes explicit `capture-frontmost` and watcher preview
  paths.
- Add `trust = "untrusted_observed_content"` to CLI search outputs if the
  contract is changed to expose trust metadata. This changes CLI JSON shape and
  therefore requires `v0.1.0-rc.1`.

### Stage F2 - UIA Helper Quality Matrix

- Build a helper quality matrix for existing helper contract and manual smoke
  coverage without expanding product capture surfaces.
- Include gate type, app, expected signal, current result, artifact policy,
  privacy risk, and blocking status.
- Keep Notepad and Edge targeted smoke as hard gates; keep VS Code metadata as
  conditional hard when `code.cmd` exists; keep VS Code strict Monaco marker
  diagnostic and non-blocking.
- Treat any new app coverage as diagnostic unless explicitly promoted in a
  future scorecard update.

### Stage F3 - Watcher Reliability Contract

- Harden only the explicit, time-bounded watcher preview path.
- Cover timeout, malformed JSONL, helper failure, heartbeat-only behavior,
  duplicate skip, denylist skip, and no observed-content echo with
  deterministic tests and docs.
- Keep depth 80 live watcher timeout diagnostic until the helper quality
  matrix explains and stabilizes it.
- Do not add daemon/service install, polling capture loop, startup task, or
  default background capture.

### Stage F4 - State, Memory, MCP Freeze

- Freeze local state lifecycle, memory, and MCP compatibility after F1.
- Cover fresh init, idempotent init/status, temporary `WINCHRONICLE_HOME`,
  empty search/memory behavior, memory goldens, and rc.0 local state
  compatibility.
- Assert the exact read-only MCP tool list and deny write/control/file read,
  screenshot/OCR, audio, keyboard, clipboard, and network tools.

### Stage F5 - Final Or rc.1 Release Decision

- Complete release evidence, known limitations, rollback notes, and manual
  smoke evidence.
- Publish `v0.1.0` final only if all hard gates pass and F1-F4 introduced no
  product behavior, schema, CLI/MCP JSON shape, privacy behavior, or
  `src`/`resources` changes requiring another public candidate.
- Publish `v0.1.0-rc.1` if any such change occurred.
- Do not retag `v0.1.0-rc.0`.

## Test Plan

Every implementation stage should run:

- `python -m pytest -q`
- `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo`
- `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo`
- `python harness/scripts/run_harness.py`
- `git diff --check`
- GitHub Actions `Windows Harness` on PR and after merge to `main`

Stage-specific gates:

- F0: `git diff --check`, documentation consistency grep, PR Windows Harness,
  post-merge Windows Harness.
- F1: privacy/status/MCP/search trust-boundary tests.
- F2: helper contract tests and manual smoke matrix evidence.
- F3: watcher failure-mode tests.
- F4: MCP exact tool-list tests and memory golden tests.
- F5: full release checklist, manual Notepad/Edge/VS Code metadata smoke,
  watcher preview evidence, and final release evidence review.

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
- Phase 6 remains specification-only until a future tests-first round.

## Decision Log

- Chose F0 first because the repository docs still contained pre-publication
  rc.0 language after the prerelease was published.
- Chose a new final-readiness plan file instead of continuing to mutate the
  rc.0 readiness plan, so future agents do not follow stale release-candidate
  instructions.
- Decided that CLI search trust metadata, if implemented in F1, requires
  `v0.1.0-rc.1` because it changes the CLI JSON shape.
- Extended the F1 trust metadata change to CLI `search-memory` as well as
  `search-captures`, because memory search snippets also contain observed
  content and operator docs already require CLI, memory, and MCP parity.
- Generated default config privacy flags from the shared disabled-surface
  contract so `config.toml`, CLI `status`, and MCP `privacy_status` do not drift.
- Added `--no-build-isolation` to the install smoke because the script is a
  no-dependency packaging smoke; this avoids network build-dependency fetches
  while using the already-available local build backend.
- Added `wheel` to the dev dependency set because the no-build-isolation
  editable install smoke needs the local `bdist_wheel` command on GitHub
  Windows runners.
- Kept F2 docs/tests-only: the helper quality matrix records current automated
  and manual gates but does not change product CLI, MCP, helper, watcher, schema,
  or capture behavior.
- Kept F3 docs/tests-only: helper failure is covered as a watcher nonzero
  failure path that suppresses helper-adjacent stdout/stderr, while live helper
  failure semantics remain diagnostic until a future watcher implementation
  change explicitly promotes them.
- Treated heartbeat-only runs as a liveness diagnostic: they increment
  `heartbeats`, write no captures, and do not save raw watcher JSONL.
- Kept F4 docs/tests-only: the state, memory, and MCP freeze adds no new MCP
  tools, CLI commands, schemas, capture surfaces, or product behavior.
- Covered rc.0 local state compatibility with a runtime-constructed synthetic
  state tree rather than a committed SQLite database or observed-content
  artifact.
- Froze the MCP tool list against a literal expected list so future additions
  cannot accidentally update the implementation constant and the test oracle at
  the same time.
- Added a memory manifest golden instead of additional Markdown body goldens so
  the F4 slice freezes entry ordering and metadata without broadening the
  reducer contract.
- Decided F5 must prepare `v0.1.0-rc.1`, not direct final, because F1 changed
  CLI search JSON shape and privacy behavior after the published `rc.0`.
- Recorded manual rc.1 smoke evidence as paths and pass/fail results only; raw
  helper JSON artifacts remain local under the temporary artifact root.
- Treated the live depth 2 watcher run with zero captures and six heartbeats as
  heartbeat-only liveness diagnostic evidence, while deterministic watcher and
  fake-helper preview remain the automated gate.
- Kept Phase 6 out of this round because screenshot/OCR enrichment would expand
  the capture surface.

## Validation Log

- `gh release view v0.1.0-rc.0` confirmed the release is a prerelease, not a
  draft, and targets `069e8cff9434c83b00a7a857aaf9eee441cf16ff`.
- `gh run view 25022034701` confirmed the post-merge Windows Harness passed on
  `069e8cff9434c83b00a7a857aaf9eee441cf16ff`.
- F0 documentation consistency grep found no stale active references to
  pending rc.0 publication, unpublished rc.0 status, or the old rc.0 execution
  cursor.
- F0 `git diff --check` passed with no whitespace errors.
- F1 targeted tests passed:
  `python -m pytest tests/test_paths.py tests/test_cli.py tests/test_mcp_tools.py tests/test_memory_pipeline.py tests/test_sqlite_store.py -q`
  reported 28 passed.
- F1 full unit suite passed: `python -m pytest -q` reported 61 passed.
- F1 helper build passed:
  `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo`.
- F1 watcher build passed:
  `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo`.
- F1 install CLI smoke passed:
  `python harness/scripts/run_install_cli_smoke.py`.
- F1 full harness passed: `python harness/scripts/run_harness.py`.
- F1 whitespace check passed: `git diff --check`.
- F1 PR Windows Harness passed:
  https://github.com/YSCJRH/WinChronicle/actions/runs/25030108402.
- F1 post-merge `main` Windows Harness passed:
  https://github.com/YSCJRH/WinChronicle/actions/runs/25030207021.
- F2 focused matrix/helper tests passed:
  `python -m pytest tests/test_uia_helper_quality_matrix.py tests/test_uia_helper_contract.py -q`
  reported 15 passed.
- F2 full unit suite passed: `python -m pytest -q` reported 64 passed.
- F2 helper build passed:
  `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo`.
- F2 watcher build passed:
  `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo`.
- F2 full harness passed: `python harness/scripts/run_harness.py`.
- F2 whitespace check passed: `git diff --check`.
- F2 PR Windows Harness passed:
  https://github.com/YSCJRH/WinChronicle/actions/runs/25030816117.
- F2 post-merge `main` Windows Harness passed:
  https://github.com/YSCJRH/WinChronicle/actions/runs/25030896768.
- F3 watcher-focused tests passed:
  `python -m pytest tests/test_watcher_events.py -q` reported 11 passed.
- F3 full unit suite passed: `python -m pytest -q` reported 66 passed.
- F3 helper build passed:
  `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo`.
- F3 watcher build passed:
  `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo`.
- F3 full harness passed: `python harness/scripts/run_harness.py`.
- F3 whitespace check passed: `git diff --check`.
- F3 PR Windows Harness passed:
  https://github.com/YSCJRH/WinChronicle/actions/runs/25031193780.
- F3 post-merge `main` Windows Harness passed:
  https://github.com/YSCJRH/WinChronicle/actions/runs/25031257910.
- F4 focused tests passed:
  `python -m pytest tests/test_cli.py tests/test_mcp_tools.py tests/test_memory_pipeline.py -q`
  reported 23 passed.
- F4 rc.0 compatibility focused test passed:
  `python -m pytest tests/test_state_compatibility.py tests/test_cli.py tests/test_mcp_tools.py tests/test_memory_pipeline.py -q`
  reported 24 passed.
- F4 full unit suite passed: `python -m pytest -q` reported 72 passed.
- F4 helper build passed:
  `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo`.
- F4 watcher build passed:
  `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo`.
- F4 full harness passed: `python harness/scripts/run_harness.py`.
- F4 whitespace check passed: `git diff --check`.
- F4 PR Windows Harness passed:
  https://github.com/YSCJRH/WinChronicle/actions/runs/25031822924.
- F4 post-merge `main` Windows Harness passed:
  https://github.com/YSCJRH/WinChronicle/actions/runs/25031913300.
- F5 manual Notepad targeted smoke passed; artifact path recorded in
  `docs/release-candidate-v0.1.0-rc.1.md`.
- F5 manual Edge targeted smoke passed; artifact path recorded in
  `docs/release-candidate-v0.1.0-rc.1.md`.
- F5 manual VS Code metadata smoke passed with diagnostic Monaco warning;
  artifact path recorded in `docs/release-candidate-v0.1.0-rc.1.md`.
- F5 manual VS Code strict Monaco marker produced the known diagnostic failure;
  artifact path recorded in `docs/release-candidate-v0.1.0-rc.1.md`.
- F5 live watcher preview at depth 2 returned heartbeat-only liveness evidence:
  `captures_written = 0`, `heartbeats = 6`.
- F5 full unit suite passed: `python -m pytest -q` reported 72 passed.
- F5 helper build passed:
  `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo`.
- F5 watcher build passed:
  `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo`.
- F5 full harness passed: `python harness/scripts/run_harness.py`.
- F5 whitespace check passed: `git diff --check`.
- F5 PR Windows Harness passed:
  https://github.com/YSCJRH/WinChronicle/actions/runs/25032173686.
- F5 post-merge `main` Windows Harness passed:
  https://github.com/YSCJRH/WinChronicle/actions/runs/25032281387.
