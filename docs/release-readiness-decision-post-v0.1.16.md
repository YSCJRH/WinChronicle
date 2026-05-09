# Release-Readiness Decision After v0.1.16

This AF5 record decides whether the post-v0.1.16 AF1-AF4 changes warrant a
new release-readiness path. The decision is to start a narrow `v0.1.17`
maintenance release-readiness plan, not immediate publication.

Do not retag `v0.1.16`. It is already published and immutable. The
post-v0.1.16 changes are compatible privacy, trust-boundary, diagnostics,
documentation, deterministic-test, and harness guardrail changes. They do not
expand capture surfaces or authorize new v0.1 product features, but they do
include unreleased runtime/output changes that should be evaluated by a release
record before the next blueprint implementation lane.

## Decision

| Question | Decision | Evidence |
| --- | --- | --- |
| Is a release-readiness path warranted? | Yes. | AF1-AF4 include compatible runtime/output hardening after the published `v0.1.16` tag. |
| Is immediate publication warranted? | No. | Publication still requires a version decision, release record, evidence-freshness review, manual UIA smoke freshness decision, deterministic gates, PR Windows Harness, post-merge `main` Windows Harness, and explicit publication step. |
| Should `v0.1.16` be retagged? | No. | `v0.1.16` is already published and must remain immutable. |
| Should the next release-readiness target be `v0.1.17`? | Yes. | The changes are compatible maintenance hardenings on top of the published `v0.1.16` baseline. |
| Is fresh manual UIA smoke decided here? | No. | The `v0.1.17` release-readiness record must make the freshness decision because AF1-AF4 include public CLI/runtime output changes even though helper behavior, watcher product behavior, manual smoke scripts, and capture surfaces remain unchanged. |
| What is the next smallest implementation task? | Create a narrow `v0.1.17` release-readiness record. | The record should classify the unreleased runtime/output changes, decide manual smoke freshness, run full deterministic gates, and keep screenshot/OCR implementation out of scope. |

## Diff Against v0.1.16

| Surface | Post-v0.1.16 change | Release-readiness implication |
| --- | --- | --- |
| `src/winchronicle/cli.py` | `watch --events` handles invalid embedded helper payloads with a content-free diagnostic instead of leaking observed payload text. | Compatible privacy hardening; include in `v0.1.17` release notes and validation. |
| `src/winchronicle/memory.py` | `generate-memory` manifest JSON now includes `trust`, `untrusted_observed_content`, and `instruction`. | Additive CLI JSON trust-boundary change; requires release evidence and compatibility wording. |
| `src/winchronicle/mcp/server.py` | MCP control-like tool rejection was hardened with broader forbidden write/file/network/control terms. | Compatible read-only MCP hardening; verify exact tool list and forbidden-tool behavior. |
| Docs/tests/harness | AF1-AF4 added public metadata evidence, helper/watcher diagnostics docs/tests, MCP/memory contract docs/tests, ordered MCP smoke, and compatibility evidence. | Evidence maintenance and deterministic guardrails; carry into the release record without expanding product scope. |

## Evidence

- Latest published release remains
  https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.16.
- `v0.1.16` is not a draft or prerelease, was published at
  `2026-05-09T09:31:17Z`, and targets
  `255f2a01cddde330d756a87359c4d3a8be4b11a2`.
- `pyproject.toml`, `winchronicle.__version__`, and MCP `serverInfo.version`
  remain `0.1.16` until a release-readiness branch explicitly changes version
  identity for the next compatible release.
- AF4 completion merged as `74aeadc2e8fd0917ab02e0f73009f87453b4b1e8`.
- AF4 completion post-merge `main` Windows Harness run `25600584258`
  concluded `success` on
  `74aeadc2e8fd0917ab02e0f73009f87453b4b1e8`.
- The latest full manual UIA smoke source remains the published
  `v0.1.16` final release record. AF5 does not accept or reject that evidence
  for `v0.1.17`; the release-readiness record must decide whether to inherit
  or rerun it.

## Commands

Release metadata:

```powershell
gh release view v0.1.16 --json tagName,name,url,targetCommitish,isDraft,isPrerelease,publishedAt
```

Result: passed; `v0.1.16` is published, not a draft, not a prerelease, targets
`255f2a01cddde330d756a87359c4d3a8be4b11a2`, and was published at
`2026-05-09T09:31:17Z`.

Tag identity:

```powershell
git rev-parse v0.1.16
```

Result: passed and printed `255f2a01cddde330d756a87359c4d3a8be4b11a2`.

Post-AF4 main Windows Harness:

```powershell
gh run view 25600584258 --json databaseId,status,conclusion,headSha,url,displayTitle,createdAt,updatedAt
```

Result: passed; run `25600584258` concluded `success` on
`74aeadc2e8fd0917ab02e0f73009f87453b4b1e8`.

Runtime diff:

```powershell
git diff --name-status v0.1.16..HEAD
git diff --stat v0.1.16..HEAD -- src/winchronicle/cli.py src/winchronicle/memory.py src/winchronicle/mcp/server.py
```

Result: passed; runtime changes exist in `src/winchronicle/cli.py`,
`src/winchronicle/memory.py`, and `src/winchronicle/mcp/server.py`.

Local AF5 validation:

```powershell
python -m pytest tests/test_compatibility_evidence_docs.py tests/test_operator_diagnostics_docs.py tests/test_version_identity.py -q
```

Result: passed, 65 tests.

Full AF5 validation:

```powershell
python -m pytest -q
python harness/scripts/run_harness.py
git diff --check
```

Result: passed; full pytest reported 166 tests, the full deterministic harness
passed, and `git diff --check` found no whitespace errors.

## Privacy And Security

AF5 does not authorize implementation of screenshot capture, OCR, audio
recording, keyboard capture, clipboard capture, network/cloud upload, LLM
calls, desktop control, product targeted capture, daemon/service install,
polling capture loops, default background capture, MCP write tools, or
arbitrary file read tools.

The runtime changes since `v0.1.16` are privacy-positive guardrails: observed
payloads are not echoed in invalid watcher-event diagnostics, memory manifest
stdout carries explicit untrusted observed-content metadata, and MCP rejects a
broader set of control-like tool calls while keeping the exact read-only tool
list unchanged.

Observed content remains untrusted. No observed-content artifacts, raw helper
JSON, raw watcher JSONL, screenshots, OCR output, local state, generated
captures, generated memory, passwords, secrets, or token canaries should be
committed.

## Next Task

Land this AF5 release-readiness decision through PR and post-merge Windows
Harness validation. After AF5 completion, create the narrow `v0.1.17`
release-readiness record before any publication decision.
