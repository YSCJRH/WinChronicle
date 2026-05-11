# Privacy-Output Release-Readiness Decision After v0.1.18

This AH16 record decides whether AH14's privacy-positive MCP output and
redaction hardening warrant a new release-readiness path. The decision is yes:
start a narrow `v0.1.19` release-readiness path.

Do not retag `v0.1.18`. It is already published and immutable. Immediate
publication is not warranted from this decision alone; publication still
requires a release-readiness record, version decision, evidence-freshness
review, manual UIA smoke freshness decision, deterministic gates, PR Windows
Harness, post-merge `main` Windows Harness, and explicit publication step.

## Decision

| Question | Decision | Evidence |
| --- | --- | --- |
| Is a release-readiness path warranted? | Yes. | AH14 changed `search_captures` and `search_memory` read-only MCP result payloads so secret-like `result.query` echoes are redacted, and expanded redaction for standalone private-key boundary markers. |
| Is immediate publication warranted? | No. | A release path needs a dedicated `v0.1.19` release-readiness record, version bump decision, release evidence, manual-smoke freshness decision, deterministic gates, PR Windows Harness, post-merge `main` Windows Harness, and explicit publication step. |
| Should `v0.1.18` be retagged? | No. | `v0.1.18` is already published and must remain immutable. |
| Should the next release-readiness target be `v0.1.19`? | Yes. | The change is compatible and privacy-positive, but it is still a post-`v0.1.18` product privacy-output behavior change. |
| Is fresh manual UIA smoke decided here? | No. | This decision does not publish. The future `v0.1.19` release-readiness record must decide whether to inherit the published `v0.1.18` manual smoke or rerun it. |
| What is the next smallest implementation task? | Create the narrow `v0.1.19` release-readiness record. | The privacy-output hardening has passed remote deterministic validation; local decision validation is recorded below. |

## Diff Against v0.1.18

| Surface | Post-v0.1.18 change | Release-readiness implication |
| --- | --- | --- |
| `src/winchronicle/mcp/server.py` | `search_captures` and `search_memory` still use raw queries internally for local SQLite search, but returned `result.query` values are redacted through the existing redaction pipeline. | Read-only MCP output behavior changed in a privacy-positive way; release-readiness path is warranted. |
| `src/winchronicle/redaction.py`, `harness/specs/privacy-policy.md` | Standalone `BEGIN ... PRIVATE KEY` and `END ... PRIVATE KEY` boundary markers are now covered by the private-key redaction rule and privacy policy. | Privacy redaction behavior changed in a compatible way. |
| `tests/`, `harness/scorecards/`, `docs/` | Added helper-only denylist parity evidence, full MCP payload query-echo redaction coverage, private-key boundary marker redaction tests, privacy scorecard updates, and AH14/AH15 evidence records. | Deterministic privacy regression coverage supports the release path. |
| `resources`, `pyproject.toml` | No diff. | No helper/watcher binary, dependency, or package-version metadata change in this decision. |

## Evidence

- Latest published release remains
  https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.18.
- `v0.1.18` is not a draft or prerelease, was published at
  `2026-05-09T21:38:33Z`, and targets
  `2e22ec9805edb0efd48e5ef4aacbcff13f0490ec`.
- `pyproject.toml`, `winchronicle.__version__`, and MCP
  `serverInfo.version` remain `0.1.18`; the future release-readiness branch
  must decide and implement any `v0.1.19` version bump.
- AH14 fixture/privacy residual gap audit PR #203 merged as
  `9442e4026affb1cb17d2554cb4dd5799d4d6f359`.
- PR #203 Windows Harness run `25617962810` concluded `success` on
  `f589a3bbf866995132f204de397f9695f3bd74eb`.
- Post-AH14 `main` Windows Harness run `25618020212` concluded `success` on
  `9442e4026affb1cb17d2554cb4dd5799d4d6f359`.
- AH15 evidence reconciliation PR #204 merged as
  `5bb6408ee7a8f674bb60c8d04b2dac16f1697aeb`.
- PR #204 Windows Harness run `25618201016` concluded `success` on
  `48715b92447630765bbb03bd459acdf71e466a72`.
- Post-AH15 `main` Windows Harness run `25618271963` concluded `success` on
  `5bb6408ee7a8f674bb60c8d04b2dac16f1697aeb`.

## Commands

Release metadata:

```powershell
gh release view v0.1.18 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt
```

Result: passed; `v0.1.18` is published, not a draft, not a prerelease, targets
`2e22ec9805edb0efd48e5ef4aacbcff13f0490ec`, and was published at
`2026-05-09T21:38:33Z`.

Post-v0.1.18 product/privacy diff:

```powershell
git diff --name-status v0.1.18..HEAD
git diff --name-only v0.1.18..HEAD -- pyproject.toml src\winchronicle resources
git diff --stat v0.1.18..HEAD -- pyproject.toml src\winchronicle resources harness\specs\privacy-policy.md
```

Result: passed; the product/runtime diff since `v0.1.18` is limited to
`src/winchronicle/mcp/server.py` and `src/winchronicle/redaction.py`, the
privacy policy diff is limited to `harness/specs/privacy-policy.md`, and
`pyproject.toml` plus `resources` printed no files.

Remote validation:

```powershell
gh pr view 203 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title
gh run view 25617962810 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt
gh run view 25618020212 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt
gh pr view 204 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName,title
gh run view 25618201016 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt
gh run view 25618271963 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt
```

Result: passed; PR #203 and PR #204 merged, their PR Windows Harness runs
concluded `success`, and the post-AH14 and post-AH15 `main` Windows Harness
runs concluded `success`.

Local release-decision validation:

```powershell
python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_privacy_policy_contract.py tests/test_uia_helper_quality_matrix.py tests/test_version_identity.py -q
python -m pytest -q
git diff --check
git diff --name-only -- pyproject.toml src\winchronicle resources
rg -n --glob "!docs/privacy-output-release-readiness-decision-post-v0.1.18.md" "Current stage: AH15|Stage status: AH15|Next atomic task: land this AH15|privacy-output release-readiness decision tracked by|next Fixture/privacy follow-up of privacy-output release-readiness decision" README.md docs tests
python harness/scripts/run_harness.py
```

Result: passed; focused docs/privacy/version validation reported 108 tests,
full pytest reported 228 tests, `git diff --check` passed, the current
decision branch printed no files under `pyproject.toml`, `src\winchronicle`,
or `resources`, the stale AH15/current-follow-up wording scan returned no
matches, and the full deterministic harness passed, including 228 pytest
tests, helper/watcher builds with 0 warnings and 0 errors, watcher smoke, MCP
smoke, install CLI smoke, privacy check, fixture capture/search/memory,
deterministic watcher fixture, and watcher fake-helper smoke.

## Privacy And Security

This decision is privacy-positive but not release-complete. It recognizes that
read-only MCP search responses no longer echo secret-like query strings in
clear text and standalone private-key boundary markers are now redacted.

This decision does not authorize implementation of screenshot capture, OCR,
audio recording, keyboard capture, clipboard capture, network/cloud upload,
LLM calls, desktop control, product targeted capture, daemon/service install,
polling capture loops, default background capture, MCP write tools, or
arbitrary file read tools.

Observed content remains untrusted. No observed-content artifacts, raw helper
JSON, raw watcher JSONL, screenshots, OCR output, local state, generated
captures, generated memory, passwords, secrets, or token canaries should be
committed.

## Next Task

Create the narrow `v0.1.19` release-readiness record. It should decide the
version bump, manual UIA smoke freshness, deterministic evidence requirements,
and publication path for the privacy-output hardening.
