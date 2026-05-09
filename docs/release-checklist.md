# Release Checklist

Use this checklist before publishing alpha, beta, release-candidate, or final
releases.

For operator setup and the current documentation map, start with
[Operator quickstart](operator-quickstart.md).
The latest published release record is
[v0.1.15 maintenance release record](release-v0.1.15.md). The active
`v0.1.16` final-release cursor lives in
[v0.1.16 final-release plan](next-round-plan-v0.1.16-final-release.md). The
completed post-v0.1.15 prerelease path is recorded in
[Post-v0.1.15 maintenance plan](next-round-plan-post-v0.1.15.md). The current
published prerelease candidate remains
[v0.1.16-rc.0 release candidate record](release-candidate-v0.1.16-rc.0.md)
because AD2-AD4 include compatible privacy/runtime drift fixes. For release
evidence shape, use [Release evidence guide](release-evidence.md). The
previous published release record is
[v0.1.14 maintenance release record](release-v0.1.14.md), the completed
post-v0.1.14 execution cursor is recorded in
[Post-v0.1.14 maintenance plan](next-round-plan-post-v0.1.14.md), the completed
post-v0.1.13 execution cursor is recorded in
[Post-v0.1.13 maintenance plan](next-round-plan-post-v0.1.13.md), the completed
post-v0.1.12 execution cursor lives in
[Post-v0.1.12 maintenance plan](next-round-plan-post-v0.1.12.md), and the
post-v0.1.10 plan is completed historical evidence.

## Deterministic Gates

- `python -m pytest -q`
- `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo`
- `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo`
- `python harness/scripts/run_install_cli_smoke.py`
- `python harness/scripts/run_harness.py`
- `git diff --check`

These gates must pass on Windows CI and should be rerun locally before release.

## Evidence Freshness

Before release, confirm the evidence record distinguishes current evidence from
inherited historical evidence:

- the stable baseline is `v0.1.15` until a later plan explicitly prepares
  another version;
- `v0.1.15` is the latest published release; its release URL, tag target, and
  Windows Harness evidence are recorded in the release record;
- `v0.1.16-rc.0` is the current published prerelease candidate, not the latest
  published final release, because AD2-AD4 tighten privacy/runtime behavior
  and therefore require a prerelease path before direct final;
- the active `v0.1.16` final-release cursor records `v0.1.16-rc.0`
  publication, the current `main` SHA
  `b260ebaa8808bddcce20da166038511de23bf3b5`, post-prerelease-reconciliation
  Windows Harness run `25596579705`, and docs/tests-only drift from the
  prerelease tag;
- the completed post-v0.1.15 execution cursor records AD4 PR #139, PR Windows
  Harness run `25595449096`, post-merge Windows Harness run `25595513141`,
  AD5 prerelease publication, and publication reconciliation evidence;
- the completed post-v0.1.14 execution cursor records `v0.1.15` publication,
  PR #132, PR #133, publication reconciliation PR #134, post-merge Windows
  Harness run `25589775129`, and release
  URL https://github.com/YSCJRH/WinChronicle/releases/tag/v0.1.15;
- the completed post-v0.1.13 execution cursor records `v0.1.14` publication,
  PR #125, and post-merge Windows Harness run `25585147402`;
- the completed post-v0.1.13 execution cursor also records the `v0.1.14`
  post-publication reconciliation PR #126 plus post-merge Windows Harness run
  `25585707220`;
- the post-v0.1.13 execution cursor also records the initial `v0.1.13`
  post-publication reconciliation PR #119 plus post-merge Windows Harness run
  `25581662790`;
- public metadata and evidence-freshness checks record repository description,
  homepage, topics, release metadata, and social preview status or manual
  follow-up items without treating empty repository metadata as a product-code
  blocker;
- the post-v0.1.12 execution cursor is completed historical context and records
  PR #118 plus post-merge Windows Harness run `25580877004`;
- the post-v0.1.11 execution cursor is completed historical context and
  records PR #111 plus post-merge Windows Harness run `25576867729`;
- the post-v0.1.10 execution cursor is completed historical context and
  records PR #101 plus post-merge Windows Harness run `25569567825`;
- the post-v0.1.9 execution cursor is completed historical context and records
  PR #96 plus
  post-merge Windows Harness run `25565697723`, and X0 PR #97 plus
  post-merge Windows Harness run `25566750349`, X1 PR #98 plus post-merge
  Windows Harness run `25567503424`, X2 PR #99 plus post-merge Windows Harness
  run `25568061526`, and X3 PR #100 plus post-merge Windows Harness run
  `25568639603`;
- the post-v0.1.8 execution cursor is completed historical context;
- the post-v0.1.7 execution cursor is completed historical context;
- the post-v0.1.6 execution cursor is completed historical context;
- the post-v0.1.5 execution cursor is completed historical context;
- manual UIA smoke inherited from an earlier release is labeled as inherited or
  stale, not current;
- stale manual smoke can support context, but a hard release gate needs fresh
  evidence or an explicit documented decision to keep the older result;
- for the post-v0.1.15 release-candidate path toward `v0.1.16-rc.0`, AD5
  records fresh manual UIA smoke because AD2-AD4 changed privacy/runtime
  behavior;
- for the active `v0.1.16` final-release path, fresh final manual UIA smoke is
  required before final publication; do not silently promote `v0.1.16-rc.0`
  smoke evidence to final evidence;
- for the post-v0.1.5 compatible maintenance path that published `v0.1.6`,
  inherited `v0.1.0` manual smoke was explicitly accepted by S4 because no helper,
  watcher product behavior, manual smoke script, capture, privacy, product
  CLI/MCP shape, or capture-surface behavior changed before release;
- for the post-v0.1.6 compatible maintenance path toward `v0.1.7`, inherited
  `v0.1.0` manual smoke is explicitly accepted by the T4 release-readiness
  record because no helper, watcher product behavior, manual smoke script,
  capture, privacy, product CLI/MCP shape, or capture-surface behavior changed
  before release readiness;
- for the completed post-v0.1.7 compatible maintenance path toward `v0.1.8`,
  inherited `v0.1.0` manual smoke remained stale/inherited after the U1
  freshness decision, then is explicitly accepted by the U4
  release-readiness record because no helper, watcher product behavior, manual
  smoke script, capture, privacy, product CLI/MCP shape, or capture-surface
  behavior changed before release readiness;
- for the completed post-v0.1.8 maintenance path, inherited `v0.1.0` manual
  smoke remains stale/inherited after the W1 freshness decision and is not
  fresh or current release evidence unless a later release-readiness record
  explicitly accepts it for a compatible release, or fresh manual smoke is
  recorded;
- for the completed post-v0.1.8 compatible maintenance path toward `v0.1.9`,
  inherited `v0.1.0` manual smoke is explicitly accepted by the W4
  release-readiness record because no helper, watcher product behavior, manual
  smoke script, capture, privacy, product CLI/MCP shape, or capture-surface
  behavior changed before release readiness;
- for the completed post-v0.1.9 compatible maintenance path, inherited `v0.1.0`
  manual smoke is explicitly accepted by the X1 freshness decision as
  inherited/stale evidence because no helper behavior, watcher product
  behavior, manual smoke script, capture behavior, privacy behavior, product
  CLI/MCP shape, capture-surface behavior, or release approver requirement
  changed in X0/X1;
- the X1 decision did not make inherited manual smoke fresh or current release
  evidence; the X4 release-readiness record explicitly accepted inherited
  evidence for `v0.1.10` publication;
- for the completed `v0.1.10` release-readiness path, inherited `v0.1.0`
  manual smoke is explicitly accepted by the X4 release-readiness record
  because no helper, watcher product behavior, manual smoke script, capture,
  privacy, product CLI/MCP shape, or capture-surface behavior changed before
  release readiness;
- for the completed post-v0.1.10 compatible maintenance path, inherited
  `v0.1.0` manual smoke is explicitly accepted by the Y1 freshness decision as
  inherited/stale evidence because Y0/Y1 changed only docs/tests and did not
  change helper behavior, watcher product behavior, manual smoke scripts,
  capture behavior, privacy behavior, product CLI/MCP shape, capture surfaces,
  or release approver requirements;
- the Y1 decision does not make inherited manual smoke fresh or current release
  evidence; release readiness must explicitly accept inherited evidence for
  publication or record fresh manual smoke;
- for the completed `v0.1.11` release-readiness path, inherited `v0.1.0`
  manual smoke is explicitly accepted by the Y4 release-readiness record
  because no helper, watcher product behavior, manual smoke script, capture,
  privacy, product CLI/MCP shape, or capture-surface behavior changed before
  release readiness;
- for the completed post-v0.1.11 compatible maintenance path, inherited
  `v0.1.0` manual smoke is explicitly accepted by the Z1 freshness decision as
  inherited/stale evidence because Z0/Z1 changed only docs/tests and did not
  change helper behavior, watcher product behavior, manual smoke scripts,
  capture behavior, privacy behavior, product CLI/MCP shape, capture surfaces,
  or release approver requirements;
- the Z1 decision does not make inherited manual smoke fresh or current release
  evidence; the Z4 release-readiness record explicitly accepted inherited
  evidence for `v0.1.12` publication;
- for the completed post-v0.1.12 compatible maintenance path, inherited
  `v0.1.0` manual smoke was explicitly accepted by the AA5 release-readiness
  record for `v0.1.13` publication because AA0-AA5 did not change helper
  behavior, watcher product behavior, manual smoke scripts, capture behavior,
  privacy behavior, product CLI/MCP shape, capture surfaces, or release
  approver requirements;
- for the post-v0.1.13 compatible maintenance path toward `v0.1.14`, inherited
  `v0.1.0` manual smoke is explicitly accepted by the AB5 release-readiness
  record because AB0-AB5 did not change helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior, product
  CLI/MCP shape, capture surfaces, or release approver requirements;
- deterministic harness smoke changes require fresh deterministic gate
  evidence, but do not by themselves refresh or invalidate manual UIA smoke
  evidence when product UIA behavior and manual UIA smoke scripts are
  unchanged;
- no observed-content artifact is committed to refresh evidence.

## Manual UIA Smoke Gates

Run these on an interactive Windows desktop with temporary state:

- `harness/scripts/smoke-uia-notepad.ps1`: hard gate; marker text must be captured.
- `harness/scripts/smoke-uia-edge.ps1`: hard gate; local HTML body marker must be captured.
- `harness/scripts/smoke-uia-vscode.ps1`: hard gate when `code.cmd` is available; metadata must pass.
- `harness/scripts/smoke-uia-vscode.ps1 -Strict`: diagnostic only; Monaco editor marker failure is not a v0.1 release blocker, but the diagnostic artifact must be kept.

Manual smoke scripts must not print observed content and must not activate,
click, type, move, resize, or control windows.

Record manual smoke evidence with
[Manual smoke evidence template](manual-smoke-evidence-template.md). Track
latest known freshness in
[Manual smoke evidence ledger](manual-smoke-evidence-ledger.md). See
[Windows UIA smoke gates](windows-uia-smoke.md) for hard, conditional, and
diagnostic gate meanings, and
[UIA helper quality matrix](uia-helper-quality-matrix.md) for expected signals,
artifact policy, privacy risk, and blocking status.

## Privacy Boundary

Before release, confirm the release notes state that screenshots, OCR, audio,
keyboard capture, clipboard capture, network upload, LLM summarization, and
desktop control remain absent or disabled by default.

Observed content returned through CLI, memory, and MCP must remain marked as
`untrusted_observed_content`.

CLI `status` and MCP `privacy_status` must report the same disabled privacy
surfaces: screenshots, OCR, audio, keyboard capture, clipboard capture,
network/cloud upload, LLM calls, desktop control, product targeted capture, and
MCP write tools.

Related docs:

- [Watcher preview](watcher-preview.md)
- [UIA helper quality matrix](uia-helper-quality-matrix.md)
- [Read-only MCP compatibility examples](mcp-readonly-examples.md)
- [Known limitations](known-limitations.md)
- [Release evidence guide](release-evidence.md)

## Compatibility Evidence

Before release, confirm the evidence record says:

- `pyproject.toml`, `winchronicle.__version__`, and MCP `serverInfo.version`
  report the same version.
- The exact read-only MCP tool list is unchanged:
  `current_context`, `search_captures`, `search_memory`,
  `read_recent_capture`, `recent_activity`, and `privacy_status`.
- No MCP write tools, arbitrary file reads, desktop control tools,
  screenshot/OCR tools, audio tools, keyboard tools, clipboard tools, network
  tools, or product targeted capture flags are exposed.
- Phase 6 screenshot/OCR work remains specification-only unless a future
  tests-first plan explicitly changes that boundary.
- No screenshot capture code, OCR engine integration, screenshot cache, cache
  cleanup path, or OCR-derived storage path is introduced by a maintenance
  release.

## Post-Publication Reconciliation

After publishing, confirm the repository records the release URL, exact tag
target, PR Windows Harness URL, post-merge `main` Windows Harness URL, and
next active execution cursor. Do not commit observed-content artifacts while
reconciling release evidence.
