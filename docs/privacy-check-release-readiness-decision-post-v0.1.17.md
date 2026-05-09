# Privacy-Check Release-Readiness Decision After v0.1.17

This record decides whether the privacy-policy contract parity audit and its
narrow `privacy-check` validation hardening warrant a new release-readiness or
publication path. The decision is yes: start a narrow `v0.1.18`
release-readiness path.

Do not retag `v0.1.17`. It is already published and immutable. Immediate
publication is not warranted from this decision alone; publication still
requires a release-readiness record, version decision, evidence-freshness
review, manual UIA smoke freshness decision, deterministic gates, PR Windows
Harness, post-merge `main` Windows Harness, and explicit publication step.

## Decision

| Question | Decision | Evidence |
| --- | --- | --- |
| Is a release-readiness path warranted? | Yes. | PR #185 changed `privacy-check` validation behavior in `src/winchronicle/capture.py` so existing normalized denylisted captures and raw password fields fail validation instead of passing as skipped or pattern-clean artifacts. |
| Is immediate publication warranted? | No. | A release path needs a dedicated `v0.1.18` release-readiness record, version bump decision, release evidence, manual-smoke freshness decision, deterministic gates, PR Windows Harness, post-merge `main` Windows Harness, and explicit publication step. |
| Should `v0.1.17` be retagged? | No. | `v0.1.17` is already published and must remain immutable. |
| Should the next release-readiness target be `v0.1.18`? | Yes. | The change is compatible and privacy-positive, but it is still a post-`v0.1.17` privacy-check validation behavior change. |
| Is fresh manual UIA smoke decided here? | No. | This decision does not publish. The future `v0.1.18` release-readiness record must decide whether to inherit the published `v0.1.17` manual smoke or rerun it. |
| What is the next smallest implementation task? | Create the narrow `v0.1.18` release-readiness record. | The privacy-check validation hardening has passed remote deterministic validation; local decision validation is recorded below. |

## Diff Against v0.1.17

| Surface | Post-v0.1.17 change | Release-readiness implication |
| --- | --- | --- |
| `src/winchronicle/capture.py` | Hardened `privacy_check_path` so existing normalized denylisted captures fail as already stored, existing normalized password fields are checked by field semantics, and the successful token message includes WinChronicle canaries. | Privacy-check validation behavior changed; release-readiness path is warranted. |
| `tests/` | Added privacy-policy parity tests, normalized denylisted capture tests, normalized password-field tests, and plain WinChronicle token-canary tests. | Deterministic privacy regression coverage supports the release path. |
| `docs/` | Added the privacy-policy contract parity audit and refreshed operator/release evidence docs. | Evidence maintenance for the privacy-check validation fix. |
| `resources`, `pyproject.toml` | No diff. | No helper/watcher binary, dependency, or package-version metadata change in this decision. |

## Evidence

- Latest published release remains
  https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.17.
- `v0.1.17` is not a draft or prerelease, was published at
  `2026-05-09T12:56:45Z`, and targets
  `5b260edc3bddc48986e52179b2ffd261856a89ac`.
- `pyproject.toml`, `winchronicle.__version__`, and MCP
  `serverInfo.version` remain `0.1.17`; the future release-readiness branch
  must decide and implement any `v0.1.18` version bump.
- Privacy-policy contract parity audit PR #185 merged as
  `ea5283e7ae9f2029fa97c1e9a65fff87eedb813e`.
- PR #185 Windows Harness run `25611312314` concluded `success` on
  `3e59644ed3055e4ca38039c98411c83c130209af`.
- Post-PR #185 `main` Windows Harness run `25611363701` concluded `success`
  on `ea5283e7ae9f2029fa97c1e9a65fff87eedb813e`.

## Commands

Release metadata:

```powershell
gh release view v0.1.17 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt
```

Result: passed; `v0.1.17` is published, not a draft, not a prerelease, targets
`5b260edc3bddc48986e52179b2ffd261856a89ac`, and was published at
`2026-05-09T12:56:45Z`.

Version identity:

```powershell
Select-String -Path pyproject.toml -Pattern "version"
python -c "import winchronicle, winchronicle.mcp.server as server; print(winchronicle.__version__); print(server.__version__)"
```

Result: passed; package metadata, Python package version, and MCP server
version remain `0.1.17`.

Post-v0.1.17 diff:

```powershell
git diff --name-status v0.1.17..HEAD
git diff --name-only v0.1.17..HEAD -- src\winchronicle resources pyproject.toml
```

Result: passed; the runtime/resource/version diff is limited to
`src/winchronicle/capture.py`, and the broader name-status diff also contains
docs, tests, harness contract, fixture, and scorecard history accumulated after
`v0.1.17`.

Remote validation:

```powershell
gh pr view 185 --json number,state,mergedAt,mergeCommit,url,headRefName,baseRefName
gh run view 25611312314 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt
gh run view 25611363701 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt
```

Result: passed; PR #185 merged at `2026-05-09T20:43:47Z` as
`ea5283e7ae9f2029fa97c1e9a65fff87eedb813e`, PR Windows Harness run
`25611312314` concluded `success`, and post-PR #185 `main` Windows Harness run
`25611363701` concluded `success`.

Local release-decision validation:

```powershell
python -m pytest tests/test_cli.py tests/test_privacy_check.py tests/test_redaction.py tests/test_privacy_policy_contract.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py tests/test_version_identity.py -q
python -m pytest -q
git diff --check
git diff --name-only -- src\winchronicle resources pyproject.toml
python harness/scripts/run_harness.py
```

Result: passed; focused privacy-check release-decision validation reported
107 tests, full pytest reported 203 tests, `git diff --check` passed, the
current decision branch printed no files under `src\winchronicle`, `resources`,
or `pyproject.toml`, and the full deterministic harness passed, including 203
pytest tests, helper/watcher builds with 0 warnings and 0 errors, watcher
smoke, MCP smoke, install CLI smoke, privacy check, fixture
capture/search/memory, deterministic watcher fixture, and watcher fake-helper
smoke.

## Privacy And Security

This decision is privacy-positive but not release-complete. It recognizes that
`privacy-check` validation now rejects already-normalized denylisted captures
and raw password-field artifacts that were previously under-validated.

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

Create the narrow `v0.1.18` release-readiness record. It should decide the
version bump, manual UIA smoke freshness, deterministic evidence requirements,
and publication path for the privacy-check validation hardening.
