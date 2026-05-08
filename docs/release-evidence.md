# Release Evidence Guide

Use this guide when preparing maintenance, release-candidate, and final release
evidence. It consolidates what must be recorded for deterministic gates, manual
smoke, and post-publication reconciliation without committing observed-content
artifacts. The latest published release record is
[v0.1.9 maintenance release record](release-v0.1.9.md). The active
release-readiness record is
[v0.1.10 release-readiness record](release-v0.1.10.md), and the active
post-v0.1.9 maintenance cursor is recorded in
[Post-v0.1.9 maintenance plan](next-round-plan-post-v0.1.9.md). The
post-v0.1.8 cursor is completed historical evidence.

## Evidence Location

Release evidence should live in the release-candidate record, final release
record, GitHub release notes, or PR comment. Do not commit raw helper JSON, raw
watcher JSONL, screenshots, OCR output, observed text, local HTML page
contents, editor buffer contents, passwords, secrets, or token canaries.

Record only:

- command;
- pass/fail result;
- timestamp;
- environment notes;
- commit SHA;
- GitHub Actions run URL;
- local artifact path when an artifact exists.

## Evidence Freshness

Release evidence must name which facts are current and which are inherited from
historical records. After the `v0.1.9` publication:

- `v0.1.9` is the stable baseline until a later plan explicitly prepares
  another version;
- `v0.1.9` is the latest published release; its release URL, tag target, and
  Windows Harness evidence are recorded in the release record;
- `v0.1.10` is the active release-readiness candidate and must remain pending
  until local X4 validation, PR Windows Harness, post-merge `main` Windows
  Harness, and GitHub release publication pass;
- the post-v0.1.9 execution cursor is active and records PR #96 plus
  post-merge Windows Harness run `25565697723`, and X0 PR #97 plus
  post-merge Windows Harness run `25566750349`, X1 PR #98 plus post-merge
  Windows Harness run `25567503424`, X2 PR #99 plus post-merge Windows Harness
  run `25568061526`, and X3 PR #100 plus post-merge Windows Harness run
  `25568639603`;
- the post-v0.1.8 execution cursor is completed historical context;
- the post-v0.1.7 execution cursor is completed historical context;
- the post-v0.1.6 execution cursor is completed historical context;
- the post-v0.1.5 execution cursor is completed historical context;
- manual UIA smoke evidence inherited from `v0.1.0` or another older release
  must be labeled as inherited or stale;
- a release record must not present inherited manual smoke as freshly run;
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
- for the active post-v0.1.9 compatible maintenance path, inherited `v0.1.0`
  manual smoke is explicitly accepted by the X1 freshness decision as
  inherited/stale evidence because no helper behavior, watcher product
  behavior, manual smoke script, capture behavior, privacy behavior, product
  CLI/MCP shape, capture-surface behavior, or release approver requirement
  changed in X0/X1;
- the X1 decision does not make inherited manual smoke fresh or current release
  evidence; release readiness must explicitly accept inherited evidence for
  publication or record fresh manual smoke;
- for the active `v0.1.10` release-readiness candidate, inherited `v0.1.0`
  manual smoke is explicitly accepted by the X4 release-readiness record
  because no helper, watcher product behavior, manual smoke script, capture,
  privacy, product CLI/MCP shape, or capture-surface behavior changed before
  release readiness;
- deterministic harness smoke changes require fresh deterministic gate
  evidence, but do not by themselves refresh or invalidate manual UIA smoke
  evidence when product UIA behavior and manual UIA smoke scripts are
  unchanged;
- refreshing manual smoke must record command/result/time/environment/local
  artifact path only, never observed content.

## Deterministic Evidence

Record the result for each deterministic gate:

```powershell
python -m pytest -q
dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo
dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo
python harness/scripts/run_install_cli_smoke.py
python harness/scripts/run_harness.py
git diff --check
```

Also record the GitHub Actions `Windows Harness` run URL for the PR and for
`main` after merge.

## Post-Publication Reconciliation

After a prerelease or final release is published, reconcile the repository
docs with the published facts:

- release URL;
- tag name and exact tag target SHA;
- publication status;
- PR Windows Harness URL and head SHA;
- post-merge `main` Windows Harness URL and head SHA;
- next active execution cursor.

Do not retag an already published release to reconcile documentation. If a
subsequent product, schema, CLI/MCP JSON shape, or privacy behavior change is
needed, publish a new release candidate instead.

## Manual Evidence

Use [Manual smoke evidence template](manual-smoke-evidence-template.md) for
interactive Windows smoke. Use
[Manual smoke evidence ledger](manual-smoke-evidence-ledger.md) to distinguish
fresh evidence from inherited or stale evidence. Manual evidence must use a
temporary `WINCHRONICLE_HOME` and must not paste observed content.

Hard gates:

- Notepad targeted UIA smoke: marker capture must pass.
- Edge targeted UIA smoke: local HTML body marker capture must pass.

Conditional hard gate:

- VS Code metadata targeted UIA smoke must pass when `code.cmd` exists.

Diagnostic, non-blocking gate:

- VS Code strict Monaco editor marker capture may fail as a known Monaco/UIA
  limitation. If it fails, record the diagnostic artifact path only.

Preview gate:

- Watcher preview smoke should record foreground event behavior, debounce,
  duplicate skip, denylist skip, and diagnostic behavior with temporary state.

## Privacy And Scope Evidence

Before release, confirm the evidence record says:

- screenshots and OCR are absent or disabled by default;
- audio recording is not implemented;
- keyboard capture is not implemented;
- clipboard capture is not implemented;
- network upload is not implemented;
- LLM summarization/classification is not implemented;
- MCP remains read-only;
- daemon/service install and default background capture are not implemented;
- desktop control is not implemented;
- observed content remains marked as `untrusted_observed_content`.

## Compatibility Evidence

Before release, record that:

- version identity check passed for `pyproject.toml`,
  `winchronicle.__version__`, and MCP `serverInfo.version`;
- MCP tool list remains exactly `current_context`, `search_captures`,
  `search_memory`, `read_recent_capture`, `recent_activity`, and
  `privacy_status`;
- MCP remains read-only with no write tools, arbitrary file reads, desktop
  control tools, screenshot/OCR tools, audio tools, keyboard tools, clipboard
  tools, network tools, or product targeted capture flags;
- Phase 6 remains specification-only, and no screenshot capture code, OCR
  engine integration, screenshot cache, cache cleanup path, or OCR-derived
  storage path is introduced.

## Release Decision Summary

The release-candidate record should end with:

- deterministic gates passed;
- manual hard gates passed;
- conditional gates skipped and why;
- diagnostic failures and artifact paths;
- privacy/scope confirmation;
- rollback note;
- explicit publication approval status.
