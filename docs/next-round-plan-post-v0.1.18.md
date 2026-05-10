# WinChronicle Post-v0.1.18 Maintenance Plan

## Summary

`v0.1.18` is published at
https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.18. The maintenance
release tag targets `2e22ec9805edb0efd48e5ef4aacbcff13f0490ec`, and the
release is not a draft or prerelease. The release was published at
`2026-05-09T21:38:33Z` after PR #187 Windows Harness run `25612336939`,
post-merge `main` Windows Harness run `25612391276`, release metadata
verification, and remote tag verification passed.

The `v0.1.18` publication reconciliation landed on `main` as
`f40e165ce35464e5eb8df65f10ef153f8145177b`. PR #188 Windows Harness run
`25612920731` passed, and post-merge `main` Windows Harness run `25612977738`
passed on that SHA.

The post-v0.1.18 baseline should continue blueprint-aligned maintenance without
expanding the v0.1 product boundary. The next round starts with this
post-publication baseline cursor, then continues with public metadata/evidence
freshness, helper/watcher diagnostics, MCP/memory contracts, compatibility
guardrails, and any small drift discovered by those checks.

Keep the v0.1 product boundary unchanged: local-first, UIA-first,
harness-first, read-only MCP first, no screenshot/OCR implementation, no audio
recording, no keyboard capture, no clipboard capture, no network upload, no
LLM calls, no desktop control, no product targeted capture flags, no daemon or
service install, no polling capture loop, and no default background capture.

## Execution Cursor

- Current stage: AH15 - Post-AH14 Evidence Reconciliation.
- Stage status: AH15 in progress. This branch records AH14 merge and
  post-merge evidence, then moves the Fixture/privacy baseline cursor to the
  next release-readiness decision for the privacy-positive MCP output change.
- Last completed evidence: AH14 fixture/privacy residual gap audit PR #203
  merged as `9442e4026affb1cb17d2554cb4dd5799d4d6f359`, PR Windows Harness run
  `25617962810` passed on `f589a3bbf866995132f204de397f9695f3bd74eb`, and
  post-merge `main` Windows Harness run `25618020212` passed on
  `9442e4026affb1cb17d2554cb4dd5799d4d6f359`.
- Last validation: `gh run view 25618020212 --json
  databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt`
  verified the post-AH14 `main` Windows Harness concluded `success`.
- Next atomic task: land this AH15 evidence reconciliation PR, then start a
  privacy-output release-readiness decision for the AH14 MCP search query echo
  redaction and private-key boundary marker redaction.
- Known blockers: none for product code. Live UIA smoke remains manual and
  outside default CI.

## Phased Work

### Stage AH0 - Post-v0.1.18 Baseline Cursor

- Add this post-v0.1.18 active next-round plan and keep older plans as
  historical release evidence.
- Update README, operator quickstart, release checklist, release evidence
  guide, and manual smoke evidence ledger so operators can find this active
  cursor.
- Update docs tests so `v0.1.18` is the latest published release, this plan is
  the active cursor, and post-v0.1.17 is completed historical context.
- Do not change product code, schemas, CLI/MCP JSON shape, helper/watcher
  behavior, capture surfaces, version metadata, or privacy behavior.

### Stage AH1 - Public Metadata And Evidence Freshness Follow-up

- Re-check README, operator docs, release metadata, repository metadata, and
  manual smoke freshness after `v0.1.18`.
- Record public metadata gaps as checklist items, not product-code blockers.
- Add a post-v0.1.18 public metadata/evidence freshness audit if drift is
  found or if evidence freshness needs new operator-facing documentation.
- Refresh only documentation/tests needed to keep evidence freshness clear.
- Do not run new manual UIA smoke unless product behavior, helper/watcher
  behavior, manual smoke scripts, capture behavior, privacy behavior, product
  CLI/MCP shape, capture surfaces, or release approval requirements change.

### Stage AH2 - Helper And Watcher Preview Diagnostics Review

- Review helper and watcher preview diagnostics docs, scorecards, and tests
  against the roadmap lanes for UIA helper hardening and watcher preview.
- Strengthen documentation, deterministic tests, or narrow diagnostic code only
  for discovered drift in timeout, malformed output, no observed-content echo,
  duplicate skip, denylist skip, heartbeat-only diagnostics, or diagnostic
  artifact policy.
- Keep real UIA smoke manual and outside default CI.

### Stage AH3 - MCP And Memory Contract Review

- Re-check read-only MCP examples, memory docs, deterministic demo guidance,
  and scorecards for trust-boundary and response-shape consistency.
- Strengthen narrow docs/tests/code only if evidence drifts from the exact
  read-only MCP tool list, durable memory contract, or observed-content trust
  boundary.
- Keep real UIA smoke manual and outside default CI.

### Stage AH4 - Compatibility Guardrail Sweep

- Re-run deterministic gates and confirm the v0.1 boundary still holds.
- Treat existing tests and scorecards as compatibility oracles for version
  identity, exact read-only MCP tools, disabled privacy surfaces,
  observed-content trust boundaries, watcher preview limits, durable memory
  contract, product targeted capture absence, and Phase 6 spec-only status.
- Strengthen tests only for discovered drift.
- Keep real UIA smoke manual and outside default CI.

### Stage AH5 - Release-Readiness Decision

- Decide whether AH1-AH4 documentation, harness, and compatibility-test
  guardrails warrant a post-v0.1.18 release-readiness plan.
- If a release-readiness plan is warranted, require a fresh version decision,
  evidence-freshness check, and manual UIA smoke freshness decision before any
  publication.
- If no release is warranted, start the next smallest blueprint implementation
  lane with contracts, fixtures, tests, and scorecards first.
- Do not retag `v0.1.18`; use a future compatible version only through an
  explicit release-readiness record.

### Stage AH6 - Post-AH5 Cursor Reconciliation

- Record AH5 PR and post-merge `main` Windows Harness evidence after the
  no-release decision lands.
- Return the active cursor to blueprint implementation without retagging
  `v0.1.18` or opening a publication path.
- Select the next atomic task as a post-v0.1.18 next-blueprint-lane selection
  record before any behavior change.

### Stage AH7 - Next Blueprint Lane Selection

- Select the next blueprint implementation lane with evidence from roadmap,
  prior parity audits, current fixtures, and current tests.
- Keep the selection record docs/tests-only; do not authorize runtime behavior
  changes, new capture surfaces, release-version changes, or manual smoke
  reuse for publication.
- Start the selected lane with contracts, fixtures, tests, scorecards, and docs
  first.

### Stage AH8 - Watcher Privacy Fixture Parity

- Add deterministic watcher JSONL coverage for the existing watcher dispatch
  privacy pipeline without live UIA capture.
- Prove watcher-dispatched captures preserve password-field redaction, obvious
  secret redaction, denylist skip-before-storage, untrusted observed-content
  metadata, SQLite search safety, memory search safety, MCP memory-search
  safety, and raw watcher JSONL non-persistence.
- Update watcher preview docs, privacy scorecards, release/operator evidence
  indexes, and focused tests before any behavior change. If tests expose a
  product gap, make the smallest compatible fix in a separate, test-led step.

### Stage AH9 - Post-AH8 Evidence Reconciliation

- Record AH8 PR and post-merge `main` Windows Harness evidence after watcher
  privacy fixture parity lands.
- Return the active cursor to the Fixture/privacy baseline lane without opening
  a release-readiness or publication path.
- Select the next atomic task as fixture/helper privacy index parity so the
  direct capture and helper paths get the same raw-secret absence evidence that
  AH8 added for watcher-dispatched captures.

### Stage AH10 - Fixture/Helper Privacy Index Parity

- Reuse existing synthetic privacy fixtures to cover direct fixture capture and
  synthesized UIA helper capture paths without committing new raw helper,
  watcher, capture, memory, screenshot, OCR, or observed-content artifacts.
- Prove raw passwords and token canaries are absent from capture files, memory
  Markdown, SQLite `captures`, `captures_fts`, `entries`, `entries_fts`,
  `search_captures`, `search_memory_entries`, and MCP `search_memory`.
- Update the privacy scorecard and operator/release evidence indexes before any
  behavior change. If tests expose a product gap, make the smallest compatible
  fix in a separate, test-led step.

### Stage AH11 - Post-AH10 Evidence Reconciliation

- Record AH10 PR and post-merge `main` Windows Harness evidence after
  fixture/helper privacy index parity lands.
- Return the active cursor to the Fixture/privacy baseline lane without opening
  a release-readiness or publication path.
- Select the next atomic task as fixture/privacy parity matrix consolidation so
  watcher, direct fixture, and synthesized helper privacy evidence are auditable
  in one matrix before any additional behavior change.

### Stage AH12 - Fixture/Privacy Parity Matrix Consolidation

- Add a canonical Fixture/privacy parity matrix to the privacy scorecard and a
  post-v0.1.18 audit record that maps direct fixture, synthesized UIA helper,
  and watcher-dispatched privacy evidence.
- Link the matrix from operator/release evidence indexes and helper/watcher
  documentation so future privacy fixture, helper, watcher, storage, memory, or
  MCP search changes have one freshness checkpoint.
- Keep the task docs/tests/scorecard only; do not change product runtime,
  schemas, version metadata, helper/watcher behavior, live UIA capture,
  screenshot/OCR, clipboard, keyboard, audio, network, LLM, desktop-control,
  daemon/service, polling, default background, MCP write, or product targeted
  capture behavior.

### Stage AH13 - Post-AH12 Evidence Reconciliation

- Record AH12 PR and post-merge `main` Windows Harness evidence after
  fixture/privacy parity matrix consolidation lands.
- Return the active cursor to the Fixture/privacy baseline lane without opening
  a release-readiness or publication path.
- Select the next atomic task as a fixture/privacy residual gap audit so the new
  matrix is reviewed for any remaining direct fixture, synthesized helper,
  watcher, storage, memory, MCP, scorecard, or evidence-index gaps before any
  behavior change.

### Stage AH14 - Fixture/Privacy Residual Gap Audit

- Audit the AH12 fixture/privacy parity matrix for remaining direct fixture,
  synthesized helper, watcher, storage, memory, MCP, scorecard, or
  evidence-index gaps.
- Close narrow evidence or privacy-output gaps with tests before behavior
  changes. Any product change must be privacy-positive, local-only, and keep the
  read-only MCP tool list and input schemas unchanged.
- Keep live UIA capture, helper/watcher binaries, screenshot/OCR, clipboard,
  keyboard, audio, network, LLM, desktop-control, daemon/service, polling,
  default-background, MCP write, arbitrary file-read, and product targeted
  capture behavior out of scope.

### Stage AH15 - Post-AH14 Evidence Reconciliation

- Record AH14 PR and post-merge `main` Windows Harness evidence after the
  residual gap audit lands.
- Return the active cursor to the Fixture/privacy baseline lane without
  opening a publication path, retagging `v0.1.18`, or treating AH15 itself as a
  release approval.
- Select the next smallest follow-up from the updated matrix, privacy policy,
  read-only MCP contract, roadmap, and release/operator evidence indexes.

### Stage AH16 - Privacy Output Release-Readiness Decision

- Decide whether AH14's privacy-positive MCP output and redaction hardening
  warrants a narrow release-readiness path.
- If a release-readiness path is warranted, require a fresh version decision,
  evidence-freshness check, and manual UIA smoke freshness decision before any
  publication.
- Do not retag `v0.1.18`; use a future compatible version only through an
  explicit release-readiness record.

## Public Interfaces And Non-goals

- CLI command set remains unchanged:
  `init/status/capture-once/capture-frontmost/watch/privacy-check/search-captures/generate-memory/search-memory/mcp-stdio`.
- `generate-memory` manifest JSON includes the compatible trust-boundary fields
  `trust`, `untrusted_observed_content`, and `instruction`.
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

## Assumptions

- `v0.1.18` is the latest published stable release and must not be retagged.
- `v0.1.17` remains the previous stable release and must not be retagged.
- Manual UIA smoke for `v0.1.18` was freshly rerun in the release-readiness
  branch and remains the latest full manual UIA smoke source until a later plan
  makes a new freshness decision.
- Phase 6 stays at spec/scorecard level for this round.

## Decision Log

- Started AH0 after v0.1.18 publication reconciliation landed on `main` as
  `f40e165ce35464e5eb8df65f10ef153f8145177b` and post-merge Windows Harness
  run `25612977738` passed.
- Kept AH0 docs-only because `v0.1.18` publication is already verified and the
  next safe task is to establish the post-v0.1.18 maintenance cursor.
- Completed AH0 after PR #189 merged as
  `f4d24adf5bb60cd5ad6abfc21ada04fbbeae288c` and post-merge Windows Harness
  run `25613244560` passed.
- Started AH1 as a docs/tests-only public metadata audit because repository
  metadata gaps are manual maintainer follow-up items and not product-code
  blockers.
- Completed AH1 after PR #190 merged as
  `579ee935d9384a1c7640f30e3822a0d441706d75` and post-merge Windows Harness
  run `25613555936` passed.
- Started AH2 as a docs/tests-only helper/watcher diagnostics review because
  existing deterministic tests and scorecards already cover the v0.1 preview
  diagnostic boundary.
- Completed AH2 after PR #191 merged as
  `d6d41eb184caeb2d32cd12f696d432ccb64cbb0e` and post-merge Windows Harness
  run `25613866954` passed.
- Started AH3 as a docs/tests-only MCP/memory contract review because existing
  deterministic tests and scorecards already cover the read-only MCP tool list,
  durable memory contract, and observed-content trust boundary.
- Completed AH3 after PR #192 merged as
  `9df2c5731e10e7553800645c20ab2f71e58f695d` and post-merge Windows Harness
  run `25614220171` passed.
- Started AH4 as a docs/tests-only compatibility guardrail sweep because
  existing deterministic tests and scorecards already cover version identity,
  exact read-only MCP tools, disabled privacy surfaces, watcher preview limits,
  durable memory contracts, product targeted-capture absence, and Phase 6
  spec-only status.
- Completed AH4 after PR #193 merged as
  `a773bcd6535bcac9bdfef87162aa1c5f8fc23369` and post-merge Windows Harness
  run `25614585178` passed.
- Started AH5 as a release-readiness decision because AH1-AH4 completed the
  post-v0.1.18 docs/tests/evidence maintenance loop with no product/runtime,
  helper/watcher, CLI/MCP, privacy, capture-surface, dependency, or
  version-metadata drift.
- Recorded the AH5 decision: do not start a new release-readiness or
  publication path, do not retag `v0.1.18`, and start the next blueprint
  implementation lane with contracts, fixtures, tests, and scorecards first
  after this decision lands.
- Completed AH5 after PR #194 merged as
  `0bc33714d8fe2e9926d6c4753c8c7780fb1e9e00` and post-merge Windows Harness
  run `25614978807` passed.
- Started AH6 as a docs/tests-only cursor reconciliation because AH5 is merged,
  no release path is warranted, and the active plan should not continue to
  present AH5 as in progress.
- Selected the next atomic task as a post-v0.1.18 next-blueprint-lane selection
  record so the next implementation lane is chosen explicitly before behavior
  changes.
- Completed AH6 after PR #195 merged as
  `545be8dd326b2e9453c1949db44d3445e218b789` and post-merge Windows Harness
  run `25615262484` passed.
- Started AH7 as a docs/tests-only next blueprint lane selection because AH6
  reconciled the AH5 evidence and the roadmap should name the next lane before
  implementation resumes.
- Selected Fixture and privacy baseline as the next lane, starting with watcher
  privacy fixture parity using deterministic watcher JSONL fixtures, focused
  tests, scorecards, and docs first.
- Completed AH7 after PR #196 merged as
  `25223872d81486a33b3890b1791d529bf176c8ec` and post-merge Windows Harness
  run `25615551057` passed.
- Started AH8 as a fixture/tests/docs-first watcher privacy parity task because
  the watcher dispatch code already routes through the shared normalization,
  redaction, denylist, storage, search, and memory pipeline, but watcher tests
  did not yet prove password, secret, denylist, trust, and memory parity.
- Completed AH8 after PR #197 merged as
  `3984e736654daeaf858b62ea4710d1b57805043c` and post-merge Windows Harness
  run `25616063920` passed.
- Started AH9 as a docs/tests-only evidence reconciliation because AH8 is
  merged, no release path is warranted, and the active plan should not continue
  to present watcher privacy fixture parity as in progress.
- Selected the next Fixture/privacy baseline follow-up as fixture/helper
  privacy index parity for raw-secret absence across capture files, memory
  files, SQLite search tables, and MCP memory-search results.
- Completed AH9 after PR #198 merged as
  `603519ec3a428f65aae21b0c614f48dc6d4b156a` and post-merge Windows Harness
  run `25616355896` passed.
- Started AH10 as a tests/docs-only fixture/helper privacy index parity task
  because the runtime paths already share normalization, redaction,
  persistence, SQLite indexing, memory generation, and MCP memory search.
- Reused existing synthetic privacy fixtures rather than committing new raw
  helper/watcher artifacts.
- Completed AH10 after PR #199 merged as
  `cf1dab1d58e6e637c73aee748056591b597d70b1` and post-merge Windows Harness
  run `25616673782` passed.
- Started AH11 as a docs/tests-only evidence reconciliation because AH10 is
  merged, no release path is warranted, and public indexes should not keep
  fixture/helper privacy index parity presented as active implementation work.
- Selected the next Fixture/privacy baseline follow-up as fixture/privacy
  parity matrix consolidation across watcher, direct fixture, and synthesized
  helper privacy evidence.
- Completed AH11 after PR #200 merged as
  `32fc7e643c85aeced8ad714c75dbc8830eba77a8` and post-merge Windows Harness
  run `25616951807` passed.
- Started AH12 as a docs/tests/scorecard-only matrix consolidation because
  watcher-dispatched, direct fixture, and synthesized helper privacy parity are
  now proven but split across separate evidence records and tests.
- Completed AH12 after PR #201 merged as
  `3ff86ec086a85bdeedbabb343ca93122e0a47a1e` and post-merge Windows Harness
  run `25617330198` passed.
- Started AH13 as a docs/tests-only evidence reconciliation because AH12 is
  merged, no release path is warranted, and public indexes should not keep
  fixture/privacy parity matrix consolidation presented as active implementation
  work.
- Selected the next Fixture/privacy baseline follow-up as a residual gap audit
  using the consolidated matrix before any additional behavior change.
- Completed AH13 after PR #202 merged as
  `020a9b81dab34cdb145557e57230c49ea83b95a4` and post-merge Windows Harness
  run `25617582514` passed.
- Started AH14 as a fixture/privacy residual gap audit because the AH12 matrix
  made two remaining gaps visible: helper-only denylist evidence and raw
  secret-like query echoes in MCP search results.
- Closed those gaps with a standalone helper denylist parity test, MCP
  search-query echo redaction, and standalone private-key boundary marker
  redaction while preserving the read-only MCP tool list and v0.1 capture
  boundary.
- Completed AH14 after PR #203 merged as
  `9442e4026affb1cb17d2554cb4dd5799d4d6f359` and post-merge Windows Harness
  run `25618020212` passed.
- Started AH15 as a docs/tests-only evidence reconciliation because AH14 is
  merged and public indexes should not keep the residual gap audit presented as
  active implementation work.
- Selected the next Fixture/privacy baseline follow-up as a privacy-output
  release-readiness decision because AH14 changed read-only MCP search query
  echo redaction and private-key boundary marker redaction.

## Validation Log

- Stage AH0 initialization:
  - `gh release view v0.1.18 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; `v0.1.18` is published, not a draft, not a prerelease, published at `2026-05-09T21:38:33Z`, and targets `2e22ec9805edb0efd48e5ef4aacbcff13f0490ec`.
  - `git ls-remote --tags origin v0.1.18` - passed and printed `2e22ec9805edb0efd48e5ef4aacbcff13f0490ec`.
  - `gh run view 25612920731 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #188 Windows Harness concluded `success` on `a8897502c8d0bbb157b68e2214cddc4d206d8e84`.
  - `gh run view 25612977738 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-PR #188 `main` Windows Harness concluded `success` on `f40e165ce35464e5eb8df65f10ef153f8145177b`.
- Stage AH0 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_uia_helper_quality_matrix.py tests/test_version_identity.py -q` - passed, 88 tests.
  - `python -m pytest -q` - passed, 205 tests.
  - `git diff --check` - passed.
  - `git diff --name-only -- src\winchronicle resources pyproject.toml` - passed; printed no files, confirming AH0 is docs/tests only with no product/runtime/version diff.
  - `python harness/scripts/run_harness.py` - passed, including 205 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AH0 completion:
  - `gh pr view 189 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #189 merged as `f4d24adf5bb60cd5ad6abfc21ada04fbbeae288c`.
  - `gh run view 25613203047 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #189 Windows Harness concluded `success` on `ff39e03ce62940a54c8423dba65014c5e39cf45d`.
  - `gh run view 25613244560 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH0 `main` Windows Harness concluded `success` on `f4d24adf5bb60cd5ad6abfc21ada04fbbeae288c`.
- Stage AH1 initialization:
  - `gh repo view YSCJRH/WinChronicle --json nameWithOwner,visibility,defaultBranchRef,description,homepageUrl,repositoryTopics,url,isArchived,isPrivate,isFork,latestRelease,usesCustomOpenGraphImage` - passed; repository is public on `main`, is not archived, forked, or private, has empty description, homepage, and topics, reports latest release `v0.1.18`, and has no custom OpenGraph image.
  - `gh release view v0.1.18 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; `v0.1.18` is published, not a draft, not a prerelease, published at `2026-05-09T21:38:33Z`, and targets `2e22ec9805edb0efd48e5ef4aacbcff13f0490ec`.
  - `gh release view v0.1.17 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; `v0.1.17` remains published as the previous stable release, not a draft, not a prerelease, published at `2026-05-09T12:56:45Z`, and targets `5b260edc3bddc48986e52179b2ffd261856a89ac`.
  - `gh run view 25613244560 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH0 `main` Windows Harness concluded `success` on `f4d24adf5bb60cd5ad6abfc21ada04fbbeae288c`.
- Stage AH1 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 84 tests.
  - `python -m pytest -q` - passed, 206 tests.
  - `git diff --check` - passed.
  - `git diff --name-only -- src\winchronicle resources pyproject.toml` - passed; printed no files, confirming AH1 is docs/tests only with no product/runtime/version diff.
  - current-entry stale AH0/current-v0.1.17 wording scan across `README.md`, current docs, and current doc tests - passed with no matches in current entry documents.
  - `python harness/scripts/run_harness.py` - passed, including 206 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AH1 completion:
  - `gh pr view 190 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #190 merged at `2026-05-09T22:36:06Z` as `579ee935d9384a1c7640f30e3822a0d441706d75`.
  - `gh run view 25613512871 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #190 Windows Harness concluded `success` on `f5c78f679afa4ac9da4d7a81d74e872e5f5090af`.
  - `gh run view 25613555936 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH1 `main` Windows Harness concluded `success` on `579ee935d9384a1c7640f30e3822a0d441706d75`.
- Stage AH2 initialization:
  - Reviewed `docs/uia-helper-quality-matrix.md`, `docs/watcher-preview.md`, `docs/operator-diagnostics.md`, `harness/scorecards/capture-quality.md`, `tests/test_cli.py`, `tests/test_uia_helper_contract.py`, `tests/test_watcher_events.py`, `tests/test_operator_diagnostics_docs.py`, `tests/test_compatibility_contracts.py`, and `tests/test_uia_helper_quality_matrix.py`.
  - Found no new helper/watcher diagnostics drift requiring product code, schema, CLI/MCP JSON, helper/watcher capture behavior, privacy storage behavior, or capture-surface changes.
- Stage AH2 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_watcher_events.py tests/test_uia_helper_quality_matrix.py tests/test_version_identity.py -q` - passed, 108 tests.
  - `python -m pytest -q` - passed, 207 tests.
  - `git diff --check` - passed.
  - `git diff --name-only -- src\winchronicle resources pyproject.toml` - passed; printed no files, confirming AH2 is docs/tests only with no product/runtime/version diff.
  - current-entry stale AH1/current post-v0.1.17 helper/watcher wording scan across `README.md`, current docs, and current doc tests - passed with no matches in current entry documents.
  - `python harness/scripts/run_harness.py` - passed, including 207 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AH2 completion:
  - `gh pr view 191 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #191 merged at `2026-05-09T22:52:52Z` as `d6d41eb184caeb2d32cd12f696d432ccb64cbb0e`.
  - `gh run view 25613817162 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #191 Windows Harness concluded `success` on `a3811e8be25e3c554da9cd9fb39e61d92b6546ad`.
  - `gh run view 25613866954 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH2 `main` Windows Harness concluded `success` on `d6d41eb184caeb2d32cd12f696d432ccb64cbb0e`.
- Stage AH3 initialization:
  - Reviewed `docs/mcp-readonly-examples.md`, `docs/deterministic-demo.md`, `harness/scorecards/mcp-quality.md`, `harness/scorecards/memory-quality.md`, `tests/test_mcp_tools.py`, `tests/test_memory_pipeline.py`, `harness/scripts/run_mcp_smoke.py`, `src/winchronicle/mcp/server.py`, and `src/winchronicle/memory.py`.
  - Found no new MCP/memory contract drift requiring product code, schema, CLI/MCP JSON shape, memory reducer, SQLite schema, privacy runtime, helper, watcher, or capture-surface changes.
- Stage AH3 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_mcp_tools.py tests/test_memory_pipeline.py tests/test_state_compatibility.py tests/test_version_identity.py -q` - passed, 108 tests.
  - `python -m pytest -q` - passed, 209 tests.
  - `git diff --check` - passed.
  - `git diff --name-only -- src\winchronicle resources pyproject.toml` - passed; printed no files, confirming AH3 is docs/tests only with no product/runtime/version diff.
  - current-entry stale AH2/current post-v0.1.17 MCP/memory wording scan across `README.md`, current docs, and current doc tests - passed with no matches in current entry documents.
  - `python harness/scripts/run_harness.py` - passed, including 209 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AH3 completion:
  - `gh pr view 192 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #192 merged at `2026-05-09T23:12:54Z` as `9df2c5731e10e7553800645c20ab2f71e58f695d`.
  - `gh run view 25614178190 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #192 Windows Harness concluded `success` on `cfc1daf25a0812ac30b64af242d44b5d0ee30d96`.
  - `gh run view 25614220171 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH3 `main` Windows Harness concluded `success` on `9df2c5731e10e7553800645c20ab2f71e58f695d`.
- Stage AH4 initialization:
  - Reviewed `docs/compatibility-guardrail-sweep-post-v0.1.17.md`, `tests/test_compatibility_contracts.py`, `tests/test_mcp_tools.py`, `tests/test_phase6_privacy_scorecard.py`, `tests/test_watcher_events.py`, `tests/test_state_compatibility.py`, `tests/test_memory_pipeline.py`, `tests/test_privacy_check.py`, `tests/test_version_identity.py`, and current release/operator evidence indexes.
  - Found no new compatibility drift requiring schema, MCP tool-schema, helper/watcher output contract, capture storage shape, privacy runtime, capture-surface, dependency, or version-metadata changes.
- Stage AH4 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_contracts.py tests/test_mcp_tools.py tests/test_phase6_privacy_scorecard.py tests/test_watcher_events.py tests/test_state_compatibility.py tests/test_memory_pipeline.py tests/test_privacy_check.py tests/test_privacy_policy_contract.py tests/test_version_identity.py -q` - passed, 161 tests.
  - `python -m pytest -q` - passed, 211 tests.
  - `git diff --check` - passed.
  - `git diff --name-only -- src\winchronicle resources pyproject.toml` - passed; printed no files, confirming AH4 is docs/tests only with no product/runtime/version diff.
  - boundary, background install/polling, and control/capture dependency scans found only existing disabled-surface contracts, docs, scorecards, deterministic fixtures/tests, issue templates, historical command text, canaries, and local smoke variable names; no new product CLI/MCP targeted capture, write/control tool, screenshot/OCR, audio, keyboard, clipboard, network upload, cloud upload, LLM, desktop control, daemon/service install, polling capture loop, startup task, default background capture, runtime dependency, or implementation path was found.
  - current-entry stale AH3/current post-v0.1.17 compatibility wording scan across `README.md`, current docs, and current doc tests - passed with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 211 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AH4 completion:
  - `gh pr view 193 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #193 merged at `2026-05-09T23:33:38Z` as `a773bcd6535bcac9bdfef87162aa1c5f8fc23369`.
  - `gh run view 25614535578 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #193 Windows Harness concluded `success` on `245372e32b55e69eb148c4488581dff8247b33b1`.
  - `gh run view 25614585178 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH4 `main` Windows Harness concluded `success` on `a773bcd6535bcac9bdfef87162aa1c5f8fc23369`.
- Stage AH5 initialization:
  - `gh release view v0.1.18 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt` - passed; `v0.1.18` is published, not a draft, not a prerelease, published at `2026-05-09T21:38:33Z`, and targets `2e22ec9805edb0efd48e5ef4aacbcff13f0490ec`.
  - `git fetch origin tag v0.1.18` and `git rev-parse v0.1.18` - passed and printed `2e22ec9805edb0efd48e5ef4aacbcff13f0490ec`.
  - `git diff --name-status v0.1.18..HEAD` - passed; output is docs/tests changes only.
  - `git diff --stat v0.1.18..HEAD -- src\winchronicle resources pyproject.toml` and `git diff --name-only v0.1.18..HEAD -- src\winchronicle resources pyproject.toml` - passed; printed no files, confirming no runtime/resource/version release trigger.
- Stage AH5 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 91 tests.
  - `python -m pytest -q` - passed, 213 tests.
  - `git diff --check` - passed.
  - `git diff --name-only -- src\winchronicle resources pyproject.toml` - passed; printed no files, confirming AH5 is docs/tests only with no product/runtime/version diff.
  - current-entry stale AH4/current post-v0.1.18 release-readiness wording scan across `README.md`, current docs, and current doc tests - passed with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 213 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AH5 completion:
  - `gh pr view 194 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #194 merged at `2026-05-09T23:56:35Z` as `0bc33714d8fe2e9926d6c4753c8c7780fb1e9e00`.
  - `gh run view 25614929381 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #194 Windows Harness concluded `success` on `9016b49678cbb9faefd98ab80ff003fad57e08d1`.
  - `gh run view 25614978807 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH5 `main` Windows Harness concluded `success` on `0bc33714d8fe2e9926d6c4753c8c7780fb1e9e00`.
- Stage AH6 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 91 tests.
  - `python -m pytest -q` - passed, 213 tests.
  - `git diff --check` - passed.
  - `git diff --name-only -- src\winchronicle resources pyproject.toml` - passed; printed no files, confirming AH6 is docs/tests only with no product/runtime/version diff.
  - current-entry stale AH5 and stale roadmap lane wording scan across `README.md`, current docs, and current doc tests - passed with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 213 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AH6 completion:
  - `gh pr view 195 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #195 merged at `2026-05-10T00:12:26Z` as `545be8dd326b2e9453c1949db44d3445e218b789`.
  - `gh run view 25615214406 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #195 Windows Harness concluded `success` on `4956bf2e02563bc0f0334115d70b027f68cfae2e`.
  - `gh run view 25615262484 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH6 `main` Windows Harness concluded `success` on `545be8dd326b2e9453c1949db44d3445e218b789`.
- Stage AH7 initialization:
  - Reviewed `docs/roadmap.md`, `docs/privacy-policy-contract-parity-audit-post-v0.1.17.md`, `harness/specs/privacy-policy.md`, `docs/watcher-preview.md`, `harness/fixtures/watcher`, and `tests/test_watcher_events.py`.
  - Found watcher-specific privacy parity was out of scope in the prior privacy-policy parity audit, the privacy policy applies to explicit watcher preview events before writes and indexing, and the committed watcher fixture set currently contains only `notepad_burst.jsonl`.
- Stage AH7 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 92 tests.
  - `python -m pytest -q` - passed, 214 tests.
  - `git diff --check` - passed.
  - `git diff --name-only v0.1.18..HEAD -- src\winchronicle resources pyproject.toml` - passed; printed no files, confirming AH7 is docs/tests only with no product/runtime/version diff.
  - stale AH6 and pending-roadmap wording scan across `README.md`, current docs, and current doc tests - passed with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 214 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AH7 completion:
  - `gh pr view 196 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #196 merged at `2026-05-10T00:29:22Z` as `25223872d81486a33b3890b1791d529bf176c8ec`.
  - `gh run view 25615510542 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #196 Windows Harness concluded `success` on `2e3844f10bb20772ec78a6c7b9a24a888dfbbd9b`.
  - `gh run view 25615551057 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH7 `main` Windows Harness concluded `success` on `25223872d81486a33b3890b1791d529bf176c8ec`.
- Stage AH8 initialization:
  - Reviewed `harness/specs/privacy-policy.md`, `docs/next-blueprint-lane-selection-post-v0.1.18.md`, `docs/watcher-preview.md`, `harness/fixtures/watcher`, `harness/fixtures/privacy`, `tests/test_watcher_events.py`, `tests/test_privacy_check.py`, `tests/test_redaction.py`, `tests/test_memory_pipeline.py`, `src/winchronicle/events.py`, `src/winchronicle/capture.py`, `src/winchronicle/privacy.py`, `src/winchronicle/redaction.py`, `src/winchronicle/storage.py`, and `src/winchronicle/memory.py`.
  - Found watcher dispatch already validates watcher events, validates embedded helper output, checks `denylist_reason`, normalizes through `normalize_uia_helper_output`, redacts before storage, persists through `persist_capture`, indexes SQLite search, and feeds generated memory from indexed captures.
  - Added temp-generated watcher privacy JSONL in focused tests, derived from existing privacy fixtures, to prove the existing path preserves password-field redaction, obvious secret redaction, denylist skip-before-storage, untrusted search/MCP/memory metadata, raw-secret search exclusion, and raw watcher JSONL non-persistence without committing a new sensitive watcher JSONL fixture.
- Stage AH8 local validation:
  - `python -m pytest tests/test_watcher_events.py tests/test_privacy_check.py tests/test_redaction.py -q` - passed, 31 tests.
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 93 tests.
  - `python -m pytest -q` - passed, 218 tests.
  - `git diff --check` - passed.
  - `git diff --name-only v0.1.18..HEAD -- pyproject.toml src\winchronicle\_version.py src\winchronicle\mcp\server.py resources` - passed; printed no files, confirming AH8 does not change version metadata, MCP server code, resources, helper, or watcher binaries/projects.
  - stale AH7 and old committed watcher privacy fixture wording scan across `README.md`, current docs, current tests, and privacy scorecards - passed with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 218 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AH8 completion:
  - `gh pr view 197 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #197 merged at `2026-05-10T00:58:38Z` as `3984e736654daeaf858b62ea4710d1b57805043c`.
  - `gh run view 25616023224 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #197 Windows Harness concluded `success` on `506536b0c55f68beb9eeb7a248cdb42d45337677`.
  - `gh run view 25616063920 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH8 `main` Windows Harness concluded `success` on `3984e736654daeaf858b62ea4710d1b57805043c`.
- Stage AH9 initialization:
  - Reviewed `docs/next-round-plan-post-v0.1.18.md`, `docs/watcher-privacy-fixture-parity-post-v0.1.18.md`, `docs/roadmap.md`, release/operator evidence indexes, and current doc tests.
  - Found AH8 changed tests/docs/scorecards only, did not change product runtime, schemas, version metadata, MCP server code, resources, helper/watcher projects, helper/watcher behavior, live UIA capture, or capture surfaces.
  - Selected fixture/helper privacy index parity as the next smallest Fixture/privacy baseline follow-up because AH8 added direct capture/memory/SQLite/MCP raw-secret absence checks for watcher-dispatched captures, while direct fixture/helper paths should carry equivalent evidence.
- Stage AH9 local validation:
  - Read-only reviewer completed before final validation; stale public index
    labels and missing AH8 release/evidence-index merge/run evidence were
    addressed in README, release checklist, release evidence, manual ledger, and
    doc guard tests.
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 93 tests.
  - `python -m pytest -q` - passed, 218 tests.
  - `git diff --check` - passed.
  - `git diff --name-only v0.1.18..HEAD -- pyproject.toml src\winchronicle\_version.py src\winchronicle\mcp\server.py resources` - passed; printed no files, confirming AH9 does not change version metadata, MCP server code, resources, helper, or watcher binaries/projects.
  - stale AH8/current-watcher wording scan across `README.md`, current docs, and current tests - passed with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 218 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AH9 completion:
  - `gh pr view 198 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #198 merged at `2026-05-10T01:15:20Z` as `603519ec3a428f65aae21b0c614f48dc6d4b156a`.
  - `gh run view 25616305777 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #198 Windows Harness concluded `success` on `a0193c511f8e9df8efd158362efa3e8ffb02c49d`.
  - `gh run view 25616355896 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH9 `main` Windows Harness concluded `success` on `603519ec3a428f65aae21b0c614f48dc6d4b156a`.
- Stage AH10 initialization:
  - Read-only explorer found direct fixtures, helper output, and watcher captures converge on normalization, redaction, `persist_capture`, SQLite indexing, memory generation, and MCP memory search, but direct fixture/helper tests did not yet prove AH8-width raw-secret absence across capture files, memory Markdown, SQLite search tables, and MCP memory search.
  - Added `tests/test_privacy_index_parity.py` using existing synthetic privacy fixtures to cover direct fixture and synthesized UIA helper privacy captures without committing new raw helper or watcher artifacts.
- Stage AH10 local validation:
  - `python -m pytest tests/test_privacy_index_parity.py -q` - passed, 2 tests.
  - `python -m pytest tests/test_privacy_index_parity.py tests/test_privacy_policy_contract.py -q` - passed, 7 tests.
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 94 tests.
  - `python -m pytest -q` - passed, 221 tests.
  - `git diff --check` - passed.
  - `git diff --name-only v0.1.18..HEAD -- pyproject.toml src\winchronicle\_version.py src\winchronicle\mcp\server.py resources` - passed; printed no files, confirming AH10 does not change version metadata, MCP server code, resources, helper, or watcher binaries/projects.
  - stale AH9/current-follow-up wording scan across `README.md`, current docs, current tests, and privacy scorecards - passed with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 221 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AH10 completion:
  - `gh pr view 199 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #199 merged at `2026-05-10T01:33:45Z` as `cf1dab1d58e6e637c73aee748056591b597d70b1`.
  - `gh run view 25616618385 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #199 Windows Harness concluded `success` on `591a87b4ec237388ec83525083d560285dc62638`.
  - `gh run view 25616673782 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH10 `main` Windows Harness concluded `success` on `cf1dab1d58e6e637c73aee748056591b597d70b1`.
- Stage AH11 initialization:
  - Reviewed AH10 merge evidence, fixture/helper privacy parity record, roadmap, privacy scorecard, release/operator evidence indexes, and current doc tests.
  - Found AH10 changed tests/docs/scorecards only, did not change product runtime, schemas, version metadata, MCP server code, resources, helper/watcher projects, helper/watcher behavior, live UIA capture, or capture surfaces.
  - Selected fixture/privacy parity matrix consolidation as the next smallest Fixture/privacy baseline follow-up because AH8 and AH10 now prove equivalent raw-secret absence for watcher, direct fixture, and synthesized helper paths, but the evidence is distributed across separate records and tests.
- Stage AH11 local validation:
  - Read-only reviewer completed before final validation; stale AH10 next-step wording in the fixture/helper privacy index parity record was addressed, and fixture/privacy parity matrix consolidation remains selected as the next task rather than implemented in AH11.
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 94 tests.
  - `python -m pytest -q` - passed, 221 tests.
  - `git diff --check` - passed.
  - `git diff --name-only v0.1.18..HEAD -- pyproject.toml src\winchronicle\_version.py src\winchronicle\mcp\server.py resources` - passed; printed no files, confirming AH11 does not change version metadata, MCP server code, resources, helper, or watcher binaries/projects.
  - stale AH10/current-fixture-helper wording scan across `README.md`, current docs, current tests, and privacy scorecards - passed with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 221 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AH11 completion:
  - `gh pr view 200 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #200 merged at `2026-05-10T01:49:48Z` as `32fc7e643c85aeced8ad714c75dbc8830eba77a8`.
  - `gh run view 25616911022 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #200 Windows Harness concluded `success` on `eda74918705c6356f15237a3ba5add6d918c50c6`.
  - `gh run view 25616951807 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH11 `main` Windows Harness concluded `success` on `32fc7e643c85aeced8ad714c75dbc8830eba77a8`.
- Stage AH12 initialization:
  - Read-only explorer found AH8 and AH10 privacy evidence already exists across watcher-dispatched, direct fixture, and synthesized helper paths, but is split across separate docs and tests.
  - Added `docs/privacy-fixture-parity-matrix-post-v0.1.18.md` and a canonical `harness/scorecards/privacy-gates.md` matrix to consolidate synthetic inputs, exercised paths, existing test evidence, privacy assertions, artifact policy, and v0.1 boundaries.
- Stage AH12 local validation:
  - `python -m pytest tests/test_privacy_index_parity.py tests/test_watcher_events.py tests/test_fixture_capture.py tests/test_privacy_policy_contract.py -q` - passed, 33 tests.
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_uia_helper_quality_matrix.py tests/test_version_identity.py -q` - passed, 100 tests.
  - `python -m pytest -q` - passed, 223 tests.
  - `git diff --check` - passed.
  - `git diff --name-only v0.1.18..HEAD -- pyproject.toml src\winchronicle\_version.py src\winchronicle\mcp\server.py resources` - passed; printed no files, confirming AH12 does not change version metadata, MCP server code, resources, helper, or watcher binaries/projects.
  - stale AH11/AH10 fixture-helper wording scan across `README.md`, current docs, current tests, and privacy scorecards - passed with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 223 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AH12 completion:
  - `gh pr view 201 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #201 merged at `2026-05-10T02:10:33Z` as `3ff86ec086a85bdeedbabb343ca93122e0a47a1e`.
  - `gh run view 25617277557 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #201 Windows Harness concluded `success` on `8f5845e3ea65dad277665c0dd2c9494d95458915`.
  - `gh run view 25617330198 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH12 `main` Windows Harness concluded `success` on `3ff86ec086a85bdeedbabb343ca93122e0a47a1e`.
- Stage AH13 initialization:
  - Reviewed AH12 merge evidence, fixture/privacy parity matrix record, privacy scorecard, roadmap, release/operator evidence indexes, and current doc tests.
  - Found AH12 changed docs/tests/scorecards only, did not change product runtime, schemas, version metadata, MCP server code, resources, helper/watcher projects, helper/watcher behavior, live UIA capture, or capture surfaces.
  - Selected a fixture/privacy residual gap audit as the next smallest follow-up so the consolidated matrix can be checked for remaining evidence gaps before behavior changes.
- Stage AH13 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_privacy_policy_contract.py tests/test_uia_helper_quality_matrix.py tests/test_version_identity.py -q` - passed, 106 tests.
  - `python -m pytest -q` - passed, 223 tests.
  - `git diff --check` - passed.
  - `git diff --name-only v0.1.18..HEAD -- pyproject.toml src\winchronicle\_version.py src\winchronicle\mcp\server.py resources` - passed; printed no files, confirming AH13 does not change version metadata, MCP server code, resources, helper, or watcher binaries/projects.
  - stale AH12/current-matrix wording scan across `README.md`, current docs, current tests, and privacy scorecards - passed with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 223 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AH13 completion:
  - `gh pr view 202 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #202 merged at `2026-05-10T02:23:37Z` as `020a9b81dab34cdb145557e57230c49ea83b95a4`.
  - `gh run view 25617537177 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #202 Windows Harness concluded `success` on `90a29ae645288e3bab1a31f5844da45d954c6346`.
  - `gh run view 25617582514 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH13 `main` Windows Harness concluded `success` on `020a9b81dab34cdb145557e57230c49ea83b95a4`.
- Stage AH14 initialization:
  - Read-only reviewer found no direct capture-path product gap in normalization, redaction, denylist, memory, or read-only MCP boundaries, but identified a helper-only denylist evidence gap and a full-MCP-payload ambiguity because `search_captures` and `search_memory` echoed raw secret-like queries.
  - Reviewed `docs/privacy-fixture-parity-matrix-post-v0.1.18.md`, `harness/scorecards/privacy-gates.md`, `src/winchronicle/capture.py`, `src/winchronicle/events.py`, `src/winchronicle/mcp/server.py`, `src/winchronicle/redaction.py`, and current privacy/MCP tests.
  - Added `docs/privacy-residual-gap-audit-post-v0.1.18.md`, direct helper denylist parity coverage, redacted MCP search query echoes, and standalone private-key boundary marker redaction.
- Stage AH14 local validation:
  - `python -m pytest tests/test_mcp_tools.py tests/test_privacy_index_parity.py tests/test_redaction.py tests/test_privacy_policy_contract.py -q` - passed, 25 tests.
  - `python -m pytest tests/test_privacy_index_parity.py tests/test_watcher_events.py tests/test_fixture_capture.py tests/test_privacy_policy_contract.py -q` - passed, 34 tests.
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_privacy_policy_contract.py tests/test_uia_helper_quality_matrix.py tests/test_version_identity.py -q` - passed, 107 tests.
  - `python -m pytest -q` - passed, 227 tests.
  - `git diff --check` - passed.
  - `git diff --name-only -- pyproject.toml src\winchronicle\_version.py resources` - passed; printed no files, confirming AH14 does not change package version metadata, helper resources, watcher resources, or other bundled resources.
  - `git diff --name-only -- src\winchronicle\mcp\server.py src\winchronicle\redaction.py harness\specs\privacy-policy.md` - passed; printed only `harness/specs/privacy-policy.md`, `src/winchronicle/mcp/server.py`, and `src/winchronicle/redaction.py`, confirming the runtime/privacy diff is limited to MCP search query echo redaction and private-key boundary marker redaction.
  - stale AH13/AH12 residual-gap wording scan across `README.md`, current docs, current tests, and privacy/MCP scorecards - passed with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 227 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
- Stage AH14 completion:
  - `gh pr view 203 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title` - passed; PR #203 merged at `2026-05-10T02:48:11Z` as `9442e4026affb1cb17d2554cb4dd5799d4d6f359`.
  - `gh run view 25617962810 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; PR #203 Windows Harness concluded `success` on `f589a3bbf866995132f204de397f9695f3bd74eb`.
  - `gh run view 25618020212 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt` - passed; post-AH14 `main` Windows Harness concluded `success` on `9442e4026affb1cb17d2554cb4dd5799d4d6f359`.
- Stage AH15 initialization:
  - Reviewed AH14 merge evidence, residual gap audit record, privacy parity matrix, privacy/MCP scorecards, roadmap, release/operator evidence indexes, and current doc tests.
  - Found AH14 changed product privacy output and redaction behavior narrowly, without changing package version metadata, helper/watcher resources, the read-only MCP tool list, MCP input schemas, capture surfaces, helper/watcher binaries, live UIA capture, screenshots, OCR, clipboard, keyboard, audio, network, LLM, desktop-control, daemon/service, polling, default background, MCP write, arbitrary file-read, or product targeted capture behavior.
  - Selected a privacy-output release-readiness decision as the next smallest follow-up before any publication path or additional behavior work.
- Stage AH15 local validation:
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q` - passed, 96 tests.
  - `python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_privacy_policy_contract.py tests/test_uia_helper_quality_matrix.py tests/test_version_identity.py -q` - passed, 107 tests.
  - `python -m pytest -q` - passed, 227 tests.
  - `git diff --check` - passed.
  - `git diff --name-only -- pyproject.toml src\winchronicle resources` - passed; printed no files, confirming AH15 is docs/tests only with no product runtime, package metadata, helper/watcher resource, or other bundled resource diff.
  - stale AH14/current-residual-gap wording scan across `README.md`, current docs, current tests, and privacy/MCP scorecards - passed with no matches.
  - `python harness/scripts/run_harness.py` - passed, including 227 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke.
