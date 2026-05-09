# Release Checklist

Use this checklist before publishing alpha, beta, release-candidate, or final
releases.

For operator setup and the current documentation map, start with
[Operator quickstart](operator-quickstart.md).
The latest published release record is
[v0.1.17 maintenance release record](release-v0.1.17.md). The previous stable
release record is [v0.1.16 final release record](release-v0.1.16.md). The
active post-v0.1.17 execution cursor lives in
[Post-v0.1.17 maintenance plan](next-round-plan-post-v0.1.17.md), and the
completed post-v0.1.17 public metadata/evidence freshness audit is
[Public metadata audit after v0.1.17](public-metadata-audit-post-v0.1.17.md). The
completed post-v0.1.17 helper/watcher diagnostics review is
[Helper and watcher diagnostics sweep after v0.1.17](helper-watcher-diagnostics-sweep-post-v0.1.17.md). The
completed post-v0.1.17 MCP/memory contract review is
[MCP and memory contract sweep after v0.1.17](mcp-memory-contract-sweep-post-v0.1.17.md). The
completed post-v0.1.17 compatibility guardrail review is
[Compatibility guardrail sweep after v0.1.17](compatibility-guardrail-sweep-post-v0.1.17.md). The
completed post-v0.1.17 release-readiness decision is
[Release-readiness decision after v0.1.17](release-readiness-decision-post-v0.1.17.md). The
completed Phase 6 privacy contract preflight is
[Phase 6 privacy contract preflight after v0.1.17](phase6-privacy-contract-preflight-post-v0.1.17.md). The
completed Phase 6 privacy contract fixture expansion is
[Phase 6 privacy contract fixture expansion after v0.1.17](phase6-privacy-contract-fixture-expansion-post-v0.1.17.md). The
completed Phase 6 remaining negative contract fixture expansion is
[Phase 6 privacy contract remaining fixtures after v0.1.17](phase6-privacy-contract-remaining-fixtures-post-v0.1.17.md). The
completed Phase 6 privacy contract coverage audit is
[Phase 6 privacy contract coverage audit after v0.1.17](phase6-privacy-contract-coverage-audit-post-v0.1.17.md). The
completed Phase 6 privacy contract gap fixture expansion is
[Phase 6 privacy contract gap fixtures after v0.1.17](phase6-privacy-contract-gap-fixtures-post-v0.1.17.md). The
completed Phase 6 residual schema coverage audit is
[Phase 6 privacy contract residual schema coverage audit after v0.1.17](phase6-privacy-contract-residual-schema-coverage-audit-post-v0.1.17.md). The
completed Phase 6 residual policy fixture expansion is
[Phase 6 privacy contract residual policy fixtures after v0.1.17](phase6-privacy-contract-residual-policy-fixtures-post-v0.1.17.md). The
completed Phase 6 deferred fixture closure is
[Phase 6 privacy contract deferred fixture closure after v0.1.17](phase6-privacy-contract-deferred-fixture-closure-post-v0.1.17.md). The
completed Phase 6 contract closure release-readiness decision is
[Phase 6 contract closure release-readiness decision after v0.1.17](phase6-contract-closure-release-readiness-decision-post-v0.1.17.md). The
completed post-v0.1.16 execution cursor lives in
[Post-v0.1.16 maintenance plan](next-round-plan-post-v0.1.16.md), and the
completed post-v0.1.16 public metadata/evidence freshness audit is
[Public metadata audit after v0.1.16](public-metadata-audit-post-v0.1.16.md). The
completed post-v0.1.16 helper/watcher diagnostics review is
[Helper and watcher diagnostics sweep after v0.1.16](helper-watcher-diagnostics-sweep-post-v0.1.16.md). The
completed post-v0.1.16 MCP/memory contract review is
[MCP and memory contract sweep after v0.1.16](mcp-memory-contract-sweep-post-v0.1.16.md). The
completed post-v0.1.16 compatibility guardrail review is
[Compatibility guardrail sweep after v0.1.16](compatibility-guardrail-sweep-post-v0.1.16.md). The
completed post-v0.1.16 release-readiness decision is
[Release-readiness decision after v0.1.16](release-readiness-decision-post-v0.1.16.md). The
current `v0.1.17` maintenance release record is
[v0.1.17 maintenance release record](release-v0.1.17.md). The
completed `v0.1.16` final-release cursor is recorded in
[v0.1.16 final-release plan](next-round-plan-v0.1.16-final-release.md), and
the historical prerelease record is
[v0.1.16-rc.0 release candidate record](release-candidate-v0.1.16-rc.0.md).
The previous published release record is
[v0.1.15 maintenance release record](release-v0.1.15.md), and the completed
post-v0.1.15 prerelease path is recorded in
[Post-v0.1.15 maintenance plan](next-round-plan-post-v0.1.15.md). For release
evidence shape, use [Release evidence guide](release-evidence.md). The
completed post-v0.1.14 execution cursor is recorded in
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

- the stable baseline is `v0.1.17` until a later plan explicitly prepares
  another version;
- `v0.1.17` is the latest published release; its release URL, tag target,
  published timestamp, and Windows Harness evidence are recorded in the release
  record;
- `v0.1.16` is the previous stable release; its release URL, tag target, and
  published timestamp remain recorded in the final release record;
- `v0.1.16-rc.0` is historical prerelease evidence, not the latest published
  final release;
- the active post-v0.1.17 execution cursor records `v0.1.17` publication, AF7
  publication reconciliation, PR #160, PR Windows Harness run `25601966464`,
  post-merge Windows Harness run `25602018700`, the post-v0.1.17 baseline, AG0
  baseline PR #161, PR Windows Harness run `25602296648`, post-AG0 `main`
  Windows Harness run `25602345201`, the AG1 public metadata/evidence
  freshness follow-up, AG2 helper/watcher diagnostics review PR #163 with
  post-AG2 `main` Windows Harness run `25603274783`, AG3 MCP/memory contract
  review PR #164 with post-AG3 `main` Windows Harness run `25603752386`,
  AG4 compatibility guardrail review PR #165 with post-AG4 `main` Windows Harness
  run `25604269757`, AG5 release-readiness decision PR #166 with post-AG5
  `main` Windows Harness run `25604682902`, AG6 post-AG5 cursor
  reconciliation PR #167 with post-AG6 `main` Windows Harness run
  `25605064828`, Phase 6 privacy-enrichment contract preflight PR #168 with
  post-preflight `main` Windows Harness run `25605600008`, Phase 6 preflight
  reconciliation PR #169 with post-reconciliation `main` Windows Harness run
  `25605945162`, Phase 6 committed negative contract fixture expansion PR
  #170 with post-fixture-expansion `main` Windows Harness run `25606329451`,
  Phase 6 fixture expansion reconciliation PR #171 with post-reconciliation
  `main` Windows Harness run `25606591806`, Phase 6 remaining negative fixture
  expansion PR #172 with post-remaining-fixtures `main` Windows Harness run
  `25606999596`, Phase 6 remaining fixture reconciliation PR #173 with
  post-reconciliation `main` Windows Harness run `25607328874`, Phase 6
  contract coverage audit PR #174 with post-coverage-audit `main` Windows
  Harness run `25607748205`, Phase 6 coverage audit reconciliation PR #175
  with post-reconciliation `main` Windows Harness run `25608072563`, and the
  Phase 6 contract gap fixture expansion PR #176 with post-gap-fixtures `main`
  Windows Harness run `25608403951`, Phase 6 gap fixture reconciliation PR
  #177 with post-reconciliation `main` Windows Harness run `25608660366`, and
  Phase 6 residual schema coverage audit PR #178 with post-residual-audit
  `main` Windows Harness run `25609004391`, Phase 6 residual policy fixture
  expansion PR #179 with post-residual-policy-fixtures `main` Windows Harness
  run `25609341275`, Phase 6 residual policy evidence reconciliation PR #180
  with post-reconciliation `main` Windows Harness run `25609534616`, and the
  Phase 6 deferred fixture closure PR #181 with
  post-deferred-fixture-closure `main` Windows Harness run `25609934759`, and
  Phase 6 deferred fixture closure reconciliation PR #182 with
  post-reconciliation `main` Windows Harness run `25610156997`, and the
  current next blueprint lane selection;
- the completed post-v0.1.17 public metadata/evidence freshness audit records
  repository metadata, `v0.1.17` release metadata, previous stable `v0.1.16`
  release metadata, post-AG0 `main` Windows Harness evidence, manual repository
  metadata gaps, and does not treat empty GitHub metadata as a product-code
  blocker;
- the completed post-v0.1.17 helper/watcher diagnostics review records timeout,
  malformed output, invalid embedded helper payload, no observed-content echo,
  duplicate skip, denylist skip, heartbeat-only liveness, diagnostic artifact
  policy, raw watcher JSONL non-persistence, product targeted-capture
  pass-through rejection, and no new product-code drift;
- the completed post-v0.1.17 MCP/memory contract review records the exact
  read-only MCP tool list, forbidden write/file/network/control and targeted
  capture boundary, durable memory Markdown contract, memory manifest trust
  fields, CLI/MCP capture and memory search parity, fixture-only demo boundary,
  and no new MCP/memory contract drift;
- the completed post-v0.1.17 compatibility guardrail review records version
  identity, exact read-only MCP tools, disabled privacy surfaces,
  observed-content trust boundaries, watcher preview limits, durable memory
  contract, product targeted-capture absence, Phase 6 spec-only status, and no
  new compatibility drift;
- the completed post-v0.1.17 release-readiness decision records that AG1-AG4
  docs/tests/evidence maintenance does not warrant a new release-readiness or
  publication path because there are no runtime, helper/watcher, CLI/MCP
  output, capture-surface, privacy-runtime, or version-metadata changes after
  the published `v0.1.17` tag;
- the completed post-v0.1.16 execution cursor records the `v0.1.16` baseline
  publication and the `v0.1.17` maintenance publication, final tag target
  `5b260edc3bddc48986e52179b2ffd261856a89ac`, published timestamp
  `2026-05-09T12:56:45Z`, PR #159, PR #160, and release metadata/tag
  verification;
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
- helper/watcher diagnostics sweeps record timeout, malformed output, no
  observed-content echo, duplicate skip, denylist skip, heartbeat-only liveness,
  and diagnostic artifact policy without promoting live UIA smoke to default CI;
- MCP/memory contract sweeps record the exact read-only MCP tool list, forbidden
  write/file/network/control tool boundary, durable memory contract, and
  observed-content trust metadata for memory manifests without expanding capture
  surfaces;
- compatibility guardrail sweeps record version identity, exact read-only MCP
  tools, disabled privacy surfaces, durable memory manifest/search contracts,
  watcher preview limits, product targeted-capture absence, and Phase 6
  spec-only status;
- release-readiness decisions record whether current maintenance changes
  warrant a release-readiness path, distinguish release plans from immediate
  publication, and forbid retagging an already published stable release;
- the current `v0.1.17` maintenance release record records the fresh
  version decision, additive CLI JSON trust-boundary shape, fresh hard-gate
  manual UIA smoke, heartbeat-only watcher diagnostic, passed PR/post-merge
  publication gates, release URL, published timestamp, and immutable final tag
  target without retagging `v0.1.16`;
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
- for the published `v0.1.16` final release, AE2 recorded fresh final manual
  UIA smoke; future post-v0.1.16 maintenance or release-readiness work must
  decide whether AE2 smoke remains current or rerun smoke if product behavior,
  helper/watcher behavior, manual smoke scripts, capture behavior, privacy
  behavior, CLI/MCP shape, capture surfaces, or release approval requirements
  change;
- for the published `v0.1.17` maintenance release, fresh hard-gate
  manual UIA smoke was rerun because public CLI/runtime output shape changed
  after `v0.1.16`; Notepad and Edge passed, VS Code metadata passed with the
  known Monaco diagnostic warning, VS Code strict remains diagnostic and
  non-blocking, and live watcher preview returned heartbeat-only liveness
  evidence in this desktop state;
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
