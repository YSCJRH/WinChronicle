# Release-Readiness Decision After v0.1.17

This AG5 record decides whether the post-v0.1.17 AG1-AG4 maintenance changes
warrant a new release-readiness path. The decision is no: do not start a new
release-readiness or publication path from these changes alone.

Do not retag `v0.1.17`. It is already published and immutable. The
post-v0.1.17 changes are documentation, evidence, deterministic-test, and
compatibility guardrail maintenance only. They do not change runtime code,
package version identity, helper/watcher binaries, CLI/MCP output contracts,
capture storage, privacy runtime behavior, or capture surfaces.

## Decision

| Question | Decision | Evidence |
| --- | --- | --- |
| Is a release-readiness path warranted? | No. | AG1-AG4 add docs/tests/evidence guardrails after the published `v0.1.17` tag, with no diff under `src/winchronicle`, `resources`, or `pyproject.toml`. |
| Is immediate publication warranted? | No. | There is no release-readiness path to publish, and publication would still require a future version decision, release record, evidence-freshness review, manual UIA smoke freshness decision, deterministic gates, PR Windows Harness, post-merge `main` Windows Harness, and explicit publication step. |
| Should `v0.1.17` be retagged? | No. | `v0.1.17` is already published and must remain immutable. |
| Should the next release-readiness target be chosen here? | No. | No unreleased runtime/output change exists in AG1-AG4. A future implementation lane should make its own compatible-version decision if it changes runtime behavior or published contracts. |
| Is fresh manual UIA smoke decided here? | No. | No publication path is opened. The published `v0.1.17` release record remains the latest full manual UIA smoke source until a future release-readiness record decides whether to inherit or rerun it. |
| What is the next smallest implementation task? | Start the next blueprint implementation lane with contracts, fixtures, tests, and scorecards first. | The post-v0.1.17 evidence maintenance loop is complete and found no product drift requiring a release path. |

## Diff Against v0.1.17

| Surface | Post-v0.1.17 change | Release-readiness implication |
| --- | --- | --- |
| `docs/` | Added AG1 public metadata audit, AG2 helper/watcher diagnostics sweep, AG3 MCP/memory contract sweep, AG4 compatibility guardrail sweep, and this AG5 decision; refreshed operator and release evidence indexes. | Evidence maintenance only; no release path needed. |
| `tests/` | Hardened documentation and compatibility assertions for current docs, exact read-only MCP/memory evidence, disabled pass-through flags, and compatibility guardrail records. | Deterministic guardrails only; no user-facing runtime output change. |
| `src/winchronicle`, `resources`, `pyproject.toml` | No diff from the published `v0.1.17` tag through AG5 initialization. | No runtime, binary, or version-metadata release trigger. |

## Evidence

- Latest published release remains
  https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.17.
- `v0.1.17` is not a draft or prerelease, was published at
  `2026-05-09T12:56:45Z`, and targets
  `5b260edc3bddc48986e52179b2ffd261856a89ac`.
- `pyproject.toml`, `winchronicle.__version__`, and MCP
  `serverInfo.version` remain `0.1.17`; no future version target is selected
  by this AG5 decision.
- AG4 completion merged as `ac01afc206852a8b2b52126d61aa91d633e4675b`.
- AG4 PR Windows Harness run `25604208696` concluded `success` on
  `58038a73967eeb1278f29d84884e45ad03830682`.
- AG4 completion post-merge `main` Windows Harness run `25604269757`
  concluded `success` on
  `ac01afc206852a8b2b52126d61aa91d633e4675b`.
- The latest full manual UIA smoke source remains the published `v0.1.17`
  release record. AG5 does not accept, reject, refresh, or publish with that
  evidence; a future release-readiness record must decide manual smoke
  freshness if a release path opens.

## Commands

Release metadata:

```powershell
gh release view v0.1.17 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt
```

Result: passed; `v0.1.17` is published, not a draft, not a prerelease, targets
`5b260edc3bddc48986e52179b2ffd261856a89ac`, and was published at
`2026-05-09T12:56:45Z`.

Tag fetch and identity:

```powershell
git fetch origin tag v0.1.17
git rev-parse v0.1.17
```

Result: passed and printed
`5b260edc3bddc48986e52179b2ffd261856a89ac`.

Post-AG4 main Windows Harness:

```powershell
gh run view 25604269757 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt
```

Result: passed; run `25604269757` concluded `success` on
`ac01afc206852a8b2b52126d61aa91d633e4675b`.

Post-v0.1.17 diff:

```powershell
git diff --name-status v0.1.17..HEAD
git diff --stat v0.1.17..HEAD -- src\winchronicle resources pyproject.toml
git diff --name-only v0.1.17..HEAD -- src\winchronicle resources pyproject.toml
```

Result: passed; the name-status diff contains docs/tests changes only, and
the runtime/resource/version diff commands printed no files.

Local AG5 validation:

```powershell
python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q
python -m pytest -q
git diff --check
rg -n "Current stage: AG4|AG4 review in progress|land this AG4|then decide whether a post-v0.1.17 release-readiness stage is warranted|Last completed evidence: AG3|post-AG3 `main` Windows Harness run `25603752386`" README.md docs tests
python harness/scripts/run_harness.py
```

Result: passed; focused docs/version validation reported 77 tests, full
pytest reported 179 tests, `git diff --check` passed, the stale AG4 cursor
scan returned no matches, and the full deterministic harness passed, including
179 pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher
smoke, MCP smoke, install CLI smoke, privacy check, fixture
capture/search/memory, deterministic watcher fixture, and watcher fake-helper
smoke.

## Privacy And Security

AG5 does not authorize implementation of screenshot capture, OCR, audio
recording, keyboard capture, clipboard capture, network/cloud upload, LLM
calls, desktop control, product targeted capture, daemon/service install,
polling capture loops, default background capture, MCP write tools, or
arbitrary file read tools.

The post-v0.1.17 AG1-AG4 changes are privacy-neutral guardrails and evidence
maintenance. They keep observed content untrusted, preserve local-first
behavior, and add no new capture, storage, upload, control, helper/watcher, or
MCP write surface.

Observed content remains untrusted. No observed-content artifacts, raw helper
JSON, raw watcher JSONL, screenshots, OCR output, local state, generated
captures, generated memory, passwords, secrets, or token canaries should be
committed.

## Next Task

Land this AG5 release-readiness decision through PR and post-merge Windows
Harness validation. After AG5 completion, start the next smallest blueprint
implementation lane with contracts, fixtures, tests, and scorecards first
instead of preparing a new release from docs/tests maintenance alone.
