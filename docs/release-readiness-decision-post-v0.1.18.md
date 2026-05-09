# Release-Readiness Decision After v0.1.18

This AH5 record decides whether the post-v0.1.18 AH1-AH4 maintenance changes
warrant a new release-readiness path. The decision is no: do not start a new
release-readiness or publication path from these changes alone.

Do not retag `v0.1.18`. It is already published and immutable. The
post-v0.1.18 changes are documentation, evidence, deterministic-test, and
compatibility guardrail maintenance only. They do not change runtime code,
package version identity, helper/watcher binaries, CLI/MCP output contracts,
capture storage, privacy runtime behavior, or capture surfaces.

## Decision

| Question | Decision | Evidence |
| --- | --- | --- |
| Is a release-readiness path warranted? | No. | AH1-AH4 add docs/tests/evidence guardrails after the published `v0.1.18` tag, with no diff under `src/winchronicle`, `resources`, or `pyproject.toml`. |
| Is immediate publication warranted? | No. | There is no release-readiness path to publish, and publication would still require a future version decision, release record, evidence-freshness review, manual UIA smoke freshness decision, deterministic gates, PR Windows Harness, post-merge `main` Windows Harness, and explicit publication step. |
| Should `v0.1.18` be retagged? | No. | `v0.1.18` is already published and must remain immutable. |
| Should the next release-readiness target be chosen here? | No. | No unreleased runtime/output change exists in AH1-AH4. A future implementation lane should make its own compatible-version decision if it changes runtime behavior or published contracts. |
| Is fresh manual UIA smoke decided here? | No. | No publication path is opened. The published `v0.1.18` release record remains the latest full manual UIA smoke source until a future release-readiness record decides whether to inherit or rerun it. |
| What is the next smallest implementation task? | Start the next blueprint implementation lane with contracts, fixtures, tests, and scorecards first. | The post-v0.1.18 evidence maintenance loop is complete and found no product drift requiring a release path. |

## Diff Against v0.1.18

| Surface | Post-v0.1.18 change | Release-readiness implication |
| --- | --- | --- |
| `docs/` | Added AH1 public metadata audit, AH2 helper/watcher diagnostics sweep, AH3 MCP/memory contract sweep, AH4 compatibility guardrail sweep, and this AH5 decision; refreshed operator and release evidence indexes. | Evidence maintenance only; no release path needed. |
| `tests/` | Hardened documentation and compatibility assertions for current docs, exact read-only MCP/memory evidence, disabled pass-through flags, and compatibility guardrail records. | Deterministic guardrails only; no user-facing runtime output change. |
| `src/winchronicle`, `resources`, `pyproject.toml` | No diff from the published `v0.1.18` tag through AH5 initialization. | No runtime, binary, or version-metadata release trigger. |

## Evidence

- Latest published release remains
  https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.18.
- `v0.1.18` is not a draft or prerelease, was published at
  `2026-05-09T21:38:33Z`, and targets
  `2e22ec9805edb0efd48e5ef4aacbcff13f0490ec`.
- `pyproject.toml`, `winchronicle.__version__`, and MCP
  `serverInfo.version` remain `0.1.18`; no future version target is selected
  by this AH5 decision.
- AH4 completion merged as `a773bcd6535bcac9bdfef87162aa1c5f8fc23369`
  through PR #193 at `2026-05-09T23:33:38Z`.
- AH4 PR Windows Harness run `25614535578` concluded `success` on
  `245372e32b55e69eb148c4488581dff8247b33b1`.
- AH4 completion post-merge `main` Windows Harness run `25614585178`
  concluded `success` on
  `a773bcd6535bcac9bdfef87162aa1c5f8fc23369`.
- The latest full manual UIA smoke source remains the published `v0.1.18`
  release record. AH5 does not accept, reject, refresh, or publish with that
  evidence; a future release-readiness record must decide manual smoke
  freshness if a release path opens.

## Commands

Release metadata:

```powershell
gh release view v0.1.18 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt
```

Result: passed; `v0.1.18` is published, not a draft, not a prerelease, targets
`2e22ec9805edb0efd48e5ef4aacbcff13f0490ec`, and was published at
`2026-05-09T21:38:33Z`.

Tag fetch and identity:

```powershell
git fetch origin tag v0.1.18
git rev-parse v0.1.18
```

Result: passed and printed
`2e22ec9805edb0efd48e5ef4aacbcff13f0490ec`.

Post-AH4 main Windows Harness:

```powershell
gh run view 25614585178 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt
```

Result: passed; run `25614585178` concluded `success` on
`a773bcd6535bcac9bdfef87162aa1c5f8fc23369`.

Post-v0.1.18 diff:

```powershell
git diff --name-status v0.1.18..HEAD
git diff --stat v0.1.18..HEAD -- src\winchronicle resources pyproject.toml
git diff --name-only v0.1.18..HEAD -- src\winchronicle resources pyproject.toml
```

Result: passed; the name-status diff contains docs/tests changes only, and
the runtime/resource/version diff commands printed no files.

Local AH5 validation:

```powershell
python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q
python -m pytest -q
git diff --check
git diff --name-only -- src\winchronicle resources pyproject.toml
rg -n "Current stage: AH4|AH4 in progress|Next atomic task: land this AH4|post-v0.1.18 release-readiness stage is warranted in AH5|Last completed evidence: AH3|post-AH3 `main` Windows Harness run `25614220171`|Latest release-readiness decision \| \[v0.1.18 maintenance release record\]" README.md docs\next-round-plan-post-v0.1.18.md docs\operator-quickstart.md docs\release-checklist.md docs\release-evidence.md docs\manual-smoke-evidence-ledger.md tests\test_compatibility_evidence_docs.py tests\test_operator_diagnostics_docs.py
python harness/scripts/run_harness.py
```

Result: passed; focused docs/version validation reported 91 tests, full
pytest reported 213 tests, `git diff --check` passed, the
`src\winchronicle`/`resources`/`pyproject.toml` diff command printed no files,
the stale AH4 cursor scan returned no matches, and the full deterministic
harness passed, including 213 pytest tests, helper/watcher builds with 0
warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy
check, fixture capture/search/memory, deterministic watcher fixture, and
watcher fake-helper smoke.

## Privacy And Security

AH5 does not authorize implementation of screenshot capture, OCR, audio
recording, keyboard capture, clipboard capture, network/cloud upload, LLM
calls, desktop control, product targeted capture, daemon/service install,
polling capture loops, default background capture, MCP write tools, or
arbitrary file read tools.

The post-v0.1.18 AH1-AH4 changes are privacy-neutral guardrails and evidence
maintenance. They keep observed content untrusted, preserve local-first
behavior, and add no new capture, storage, upload, control, helper/watcher, or
MCP write surface.

Observed content remains untrusted. No observed-content artifacts, raw helper
JSON, raw watcher JSONL, screenshots, OCR output, local state, generated
captures, generated memory, passwords, secrets, or token canaries should be
committed.

## Next Task

Start the next blueprint implementation lane with contracts, fixtures, tests,
scorecards, and docs first. Do not implement screenshot capture, OCR, raw
screenshot caches, runtime allowlist parsing, or any new capture surface unless
a future explicit plan authorizes that work with harness-first boundaries.
