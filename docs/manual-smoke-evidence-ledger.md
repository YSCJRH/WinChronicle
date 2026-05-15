# Manual Smoke Evidence Ledger

This ledger tracks the latest known manual smoke evidence without committing
observed-content artifacts. It is a release-planning index, not a substitute
for fresh manual smoke when a release gate requires it.

Record only command, result, timestamp, environment notes, and local artifact
path. Do not paste observed text, screenshots, OCR output, raw helper JSON, raw
watcher JSONL, local page contents, editor buffer contents, passwords, secrets,
or token canaries.

## Current Baseline

| Field | Value |
| --- | --- |
| Stable release baseline | `v0.1.18` |
| Current maintenance plan | [Post-v0.1.18 maintenance plan](next-round-plan-post-v0.1.18.md) |
| Current public metadata audit | [Public metadata audit after v0.1.18](public-metadata-audit-post-v0.1.18.md) |
| Current helper/watcher diagnostics sweep | [Helper and watcher diagnostics sweep after v0.1.18](helper-watcher-diagnostics-sweep-post-v0.1.18.md) |
| Current MCP/memory contract sweep | [MCP and memory contract sweep after v0.1.18](mcp-memory-contract-sweep-post-v0.1.18.md) |
| Current compatibility guardrail sweep | [Compatibility guardrail sweep after v0.1.18](compatibility-guardrail-sweep-post-v0.1.18.md) |
| Latest release-readiness decision | [Release-readiness decision after v0.1.18](release-readiness-decision-post-v0.1.18.md) |
| Current next blueprint lane selection | [Next blueprint lane selection after v0.1.18](next-blueprint-lane-selection-post-v0.1.18.md) |
| Completed watcher privacy fixture parity | [Watcher privacy fixture parity after v0.1.18](watcher-privacy-fixture-parity-post-v0.1.18.md) |
| Completed fixture/helper privacy index parity | [Fixture/helper privacy index parity after v0.1.18](fixture-helper-privacy-index-parity-post-v0.1.18.md) |
| Completed fixture/privacy parity matrix | [Fixture/privacy parity matrix after v0.1.18](privacy-fixture-parity-matrix-post-v0.1.18.md) |
| Completed fixture/privacy residual gap audit | [Fixture/privacy residual gap audit after v0.1.18](privacy-residual-gap-audit-post-v0.1.18.md) |
| Current privacy-output release-readiness decision | [Privacy-output release-readiness decision after v0.1.18](privacy-output-release-readiness-decision-post-v0.1.18.md) |
| Current release-readiness record | [v0.1.19 release-readiness record](release-v0.1.19.md) |
| Previous release-readiness decision | [v0.1.18 maintenance release record](release-v0.1.18.md) |
| Previous pre-v0.1.18 release-readiness decision | [Privacy-check release-readiness decision after v0.1.17](privacy-check-release-readiness-decision-post-v0.1.17.md) |
| Previous maintenance plan | [Post-v0.1.17 maintenance plan](next-round-plan-post-v0.1.17.md) |
| Previous pre-v0.1.17 maintenance plan | [Post-v0.1.16 maintenance plan](next-round-plan-post-v0.1.16.md) |
| Previous public metadata audit | [Public metadata audit after v0.1.17](public-metadata-audit-post-v0.1.17.md) |
| Previous post-v0.1.16 release-readiness decision | [Release-readiness decision after v0.1.16](release-readiness-decision-post-v0.1.16.md) |
| Current release record | [v0.1.18 maintenance release record](release-v0.1.18.md) |
| Completed final-release plan | [v0.1.16 final-release plan](next-round-plan-v0.1.16-final-release.md) |
| Previous prerelease record | [v0.1.16-rc.0 release candidate record](release-candidate-v0.1.16-rc.0.md) |
| Previous pre-v0.1.16 maintenance plan | [Post-v0.1.15 maintenance plan](next-round-plan-post-v0.1.15.md) |
| Published release record | [v0.1.18 maintenance release record](release-v0.1.18.md) |
| Latest published release record | [v0.1.18 maintenance release record](release-v0.1.18.md) |
| Previous stable release record | [v0.1.17 maintenance release record](release-v0.1.17.md) |
| Latest full manual UIA smoke source | [v0.1.18 maintenance release record](release-v0.1.18.md) |
| Freshness policy | Manual smoke inherited from older releases is inherited/stale unless rerun and recorded for the current release. |
| Last freshness decision | For the published `v0.1.18` maintenance release, fresh hard-gate manual UIA smoke was rerun because privacy-check validation behavior changed after `v0.1.17`. Notepad and Edge passed, VS Code metadata passed with the known Monaco diagnostic warning, VS Code strict remains a diagnostic non-blocking failure, and watcher preview live smoke returned heartbeat-only liveness evidence. Artifact paths are local only. |
| Next freshness decision | The current `v0.1.19` release-readiness record reran fresh hard-gate manual UIA smoke because privacy-output and read-only MCP response behavior changed after `v0.1.18`. |

## Latest Known Manual Evidence

| Gate | Release meaning | Latest known result | Freshness | Evidence source | Refresh requirement | Artifact policy |
| --- | --- | --- | --- | --- | --- | --- |
| Notepad targeted UIA smoke | Hard manual release gate | Pass | Fresh for the published `v0.1.18` maintenance release; previous fresh source was published `v0.1.17` maintenance in AF6 | [v0.1.18 maintenance release record](release-v0.1.18.md) | Refresh if helper behavior, manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP shape, capture surfaces, or release approval requirements change | Local JSON artifact path only; do not commit capture JSON |
| Edge targeted UIA smoke | Hard manual release gate | Pass | Fresh for the published `v0.1.18` maintenance release; previous fresh source was published `v0.1.17` maintenance in AF6 | [v0.1.18 maintenance release record](release-v0.1.18.md) | Refresh if helper behavior, manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP shape, capture surfaces, or release approval requirements change | Local JSON artifact path only; do not commit local HTML or capture JSON |
| VS Code metadata smoke | Conditional hard manual release gate when `code.cmd` is available | Pass with diagnostic warning | Fresh for the published `v0.1.18` maintenance release; previous fresh source was published `v0.1.17` maintenance in AF6 | [v0.1.18 maintenance release record](release-v0.1.18.md) | Refresh if helper behavior, manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP shape, capture surfaces, or release approval requirements change | Local JSON artifact only; do not commit editor contents |
| VS Code strict Monaco marker | Diagnostic, non-blocking for v0.1 | Diagnostic failure, known Monaco/UIA limitation | Fresh diagnostic for the published `v0.1.18` maintenance release | [v0.1.18 maintenance release record](release-v0.1.18.md) | Refresh only if investigating Monaco/UIA exposure, changing smoke scripts, or release approval requires a new diagnostic | Local diagnostic artifact path only |
| Watcher preview live smoke | Preview diagnostic/manual confidence gate | Heartbeat-only liveness diagnostic; `captures_written: 0`, `heartbeats: 9`, `duplicates_skipped: 0`, `denylisted_skipped: 0` | Fresh diagnostic for the published `v0.1.18` maintenance release; deterministic watcher gates remain required | [v0.1.18 maintenance release record](release-v0.1.18.md) and `python harness/scripts/run_harness.py` | Refresh only if watcher preview behavior, live smoke scripts, deterministic watcher gates, or release approval requirements change | Do not save or commit raw watcher JSONL |
| Notepad targeted UIA smoke | Hard manual release gate | Pass | Fresh for the pending `v0.1.19` maintenance release-readiness path | [v0.1.19 release-readiness record](release-v0.1.19.md) | Rerun before publication if helper behavior, manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP shape, capture surfaces, or release approval requirements change again | Local JSON artifact path only; do not commit capture JSON |
| Edge targeted UIA smoke | Hard manual release gate | Pass | Fresh for the pending `v0.1.19` maintenance release-readiness path | [v0.1.19 release-readiness record](release-v0.1.19.md) | Rerun before publication if helper behavior, manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP shape, capture surfaces, or release approval requirements change again | Local JSON artifact path only; do not commit local HTML or capture JSON |
| VS Code metadata smoke | Conditional hard manual release gate when `code.cmd` is available | Pass with diagnostic warning | Fresh for the pending `v0.1.19` maintenance release-readiness path | [v0.1.19 release-readiness record](release-v0.1.19.md) | Rerun before publication if helper behavior, manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP shape, capture surfaces, or release approval requirements change again | Local JSON artifact only; do not commit editor contents |
| VS Code strict Monaco marker | Diagnostic, non-blocking for v0.1 | Diagnostic failure, known Monaco/UIA limitation | Fresh diagnostic for the pending `v0.1.19` maintenance release-readiness path | [v0.1.19 release-readiness record](release-v0.1.19.md) | Refresh only if investigating Monaco/UIA exposure, changing smoke scripts, or release approval requires a new diagnostic | Local diagnostic artifact path only |
| Watcher preview live smoke | Preview diagnostic/manual confidence gate | Heartbeat-only liveness diagnostic; `captures_written: 0`, `heartbeats: 10`, `duplicates_skipped: 0`, `denylisted_skipped: 0` | Fresh diagnostic for the pending `v0.1.19` maintenance release-readiness path; deterministic watcher gates passed locally and remain required in PR/post-merge Windows Harness | [v0.1.19 release-readiness record](release-v0.1.19.md) and `python harness/scripts/run_harness.py` | Refresh only if watcher preview behavior, live smoke scripts, deterministic watcher gates, or release approval requirements change | Do not save or commit raw watcher JSONL |

## Command Patterns

Use a temporary `WINCHRONICLE_HOME` and a local artifact root for all manual
smoke. These command patterns are evidence shapes only; replace
`<artifact-root>` with a local temporary directory when running them.

| Gate | Command pattern |
| --- | --- |
| Notepad targeted UIA smoke | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-notepad.ps1 -ArtifactDir <artifact-root>\notepad -TimeoutSeconds 30` |
| Edge targeted UIA smoke | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-edge.ps1 -ArtifactDir <artifact-root>\edge -TimeoutSeconds 45` |
| VS Code metadata smoke | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -ArtifactDir <artifact-root>\vscode-metadata -TimeoutSeconds 45` |
| VS Code strict Monaco diagnostic | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -Strict -ArtifactDir <artifact-root>\vscode-strict -TimeoutSeconds 45` |
| Watcher preview live smoke | `python -m winchronicle watch --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper dotnet --helper-arg resources/win-uia-helper/bin/Debug/net8.0-windows/win-uia-helper.dll --duration 5 --heartbeat-ms 500 --capture-on-start` |

## Release Use

- A release record must cite this ledger when manual smoke is skipped,
  inherited, or refreshed.
- The AF5 post-v0.1.16 release-readiness decision starts a narrow `v0.1.17`
  release-readiness path. It does not decide manual smoke freshness; the
  `v0.1.17` release-readiness record must decide whether to inherit or rerun
  manual UIA smoke because AF1-AF4 include compatible public CLI/runtime output
  changes, even though helper behavior, watcher product behavior, manual smoke
  scripts, capture behavior, privacy behavior, and capture surfaces remain
  unchanged.
- The AF6 `v0.1.17` release-readiness record reran fresh hard-gate manual UIA
  smoke because public CLI/runtime output shape changed after `v0.1.16`.
  Notepad and Edge passed, VS Code metadata passed with the known Monaco
  diagnostic warning, VS Code strict remains diagnostic and non-blocking, and
  live watcher preview returned heartbeat-only liveness evidence in this
  desktop state.
- The published `v0.1.17` maintenance release kept that AF6 manual smoke as
  the latest full manual UIA smoke source until the published `v0.1.18`
  maintenance release replaced it, with publication verified against the final
  tag target and GitHub release metadata.
- The privacy-check release-readiness decision after `v0.1.17` starts a
  narrow `v0.1.18` release-readiness path for privacy-check validation
  hardening, but it does not decide manual smoke freshness. The `v0.1.18`
  release-readiness record must decide whether to inherit or rerun manual UIA
  smoke.
- The `v0.1.18` release-readiness record reran fresh hard-gate manual UIA
  smoke because privacy-check validation behavior changed after `v0.1.17`.
  Notepad and Edge passed, VS Code metadata passed with the known Monaco
  diagnostic warning, VS Code strict remains diagnostic and non-blocking, and
  live watcher preview returned heartbeat-only liveness evidence in this
  desktop state.
- The published `v0.1.18` maintenance release keeps that manual smoke as the
  latest full manual UIA smoke source, with publication verified against the
  final tag target and GitHub release metadata.
- The post-v0.1.18 release-readiness decision does not open a new publication
  path, does not retag `v0.1.18`, and does not make a fresh manual UIA smoke
  decision because AH1-AH4 are docs/tests/evidence guardrails only.
- The privacy-output release-readiness decision after `v0.1.18` starts a
  narrow `v0.1.19` release-readiness path for AH14 MCP search query echo
  redaction and private-key boundary marker redaction, but it does not decide
  manual smoke freshness. The current `v0.1.19` release-readiness record
  resolves that question by rerunning manual UIA smoke.
- The `v0.1.19` release-readiness record reran fresh hard-gate manual UIA
  smoke because privacy-output and read-only MCP response behavior changed
  after `v0.1.18`. Notepad and Edge passed, VS Code metadata passed with the
  known Monaco diagnostic warning, VS Code strict remains diagnostic and
  non-blocking, and live watcher preview returned heartbeat-only liveness
  evidence in this desktop state.
- Fresh manual smoke must use the
  [Manual smoke evidence template](manual-smoke-evidence-template.md).
- Inherited evidence can provide context, but it is not current evidence unless
  the release record explicitly accepts it for that release.
- For the post-v0.1.5 path that published `v0.1.6`, inherited `v0.1.0`
  manual smoke was explicitly accepted by the S4 release record only because
  the release path did not change helper behavior, watcher product behavior,
  manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP
  shape, or capture surfaces.
- For the completed post-v0.1.6 path that published `v0.1.7`, inherited
  `v0.1.0` manual smoke is explicitly accepted by the T4 release-readiness
  record for that compatible path because helper behavior, watcher product
  behavior, manual smoke scripts, capture behavior, privacy behavior, product
  CLI/MCP shape, and capture surfaces are unchanged.
- For the completed post-v0.1.7 compatible maintenance path toward `v0.1.8`,
  inherited `v0.1.0` manual smoke remained stale/inherited after the U1
  freshness decision, then is explicitly accepted by the U4
  release-readiness record for that compatible path because helper behavior,
  watcher product behavior, manual smoke scripts, capture behavior, privacy
  behavior, product CLI/MCP shape, and capture surfaces are unchanged.
- For the completed post-v0.1.8 path, inherited `v0.1.0` manual smoke remains
  stale/inherited after the W1 freshness decision. It is not fresh or current
  release evidence unless a later release-readiness record explicitly accepts
  it for a compatible release, or fresh manual smoke is recorded.
- For the completed post-v0.1.8 compatible maintenance path toward `v0.1.9`,
  inherited `v0.1.0` manual smoke is explicitly accepted by the W4
  release-readiness record for that compatible path because helper behavior,
  watcher product behavior, manual smoke scripts, capture behavior, privacy
  behavior, product CLI/MCP shape, and capture surfaces are unchanged.
- For the completed post-v0.1.9 compatible maintenance path, inherited
  `v0.1.0` manual smoke is accepted by the X1 freshness decision as
  inherited/stale evidence because X0/X1 changed only docs/tests and did not
  change helper behavior, watcher product behavior, manual smoke scripts,
  capture behavior, privacy behavior, product CLI/MCP shape, capture surfaces,
  or release approver requirements. This did not make it fresh or current
  release evidence; the X4 release-readiness record now explicitly accepts
  inherited evidence for the compatible `v0.1.10` path.
- For the completed post-v0.1.9 compatible maintenance path that published
  `v0.1.10`, inherited `v0.1.0` manual smoke is explicitly accepted by the X4
  release-readiness record only because X0-X4 do not change helper behavior,
  watcher product behavior, manual smoke scripts, capture behavior, privacy
  behavior, product CLI/MCP shape, or capture surfaces.
- For the completed post-v0.1.10 compatible maintenance path, inherited manual
  smoke is accepted by the Y1 freshness decision as inherited/stale evidence
  because Y0/Y1 changed only docs/tests and did not change helper behavior,
  watcher product behavior, manual smoke scripts, capture behavior, privacy
  behavior, product CLI/MCP shape, capture surfaces, or release approver
  requirements. This did not make it fresh or current release evidence; the Y4
  release-readiness record now explicitly accepts inherited evidence for the
  compatible `v0.1.11` path because Y0-Y4 do not change helper behavior,
  watcher product behavior, manual smoke scripts, capture behavior, privacy
  behavior, product CLI/MCP shape, or capture surfaces.
- For the completed post-v0.1.11 compatible maintenance path, inherited manual
  smoke was accepted by the Z1 freshness decision as inherited/stale evidence
  because Z0/Z1 changed only docs/tests and did not change helper behavior,
  watcher product behavior, manual smoke scripts, capture behavior, privacy
  behavior, product CLI/MCP shape, capture surfaces, or release approver
  requirements. This did not make it fresh or current release evidence; the
  Z4 release-readiness record explicitly accepted inherited evidence for the
  compatible `v0.1.12` path because Z0-Z4 did not change helper behavior,
  watcher product behavior, manual smoke scripts, capture behavior, privacy
  behavior, product CLI/MCP shape, or capture surfaces.
- Fresh manual smoke is required if any helper, watcher, smoke script, capture,
  privacy, product CLI/MCP shape, or capture-surface behavior changes, or if
  the release approver requires fresh hard-gate evidence.
- Deterministic harness smoke changes require fresh deterministic gate
  evidence. They do not by themselves count as fresh manual UIA smoke and do
  not invalidate inherited manual UIA smoke when product UIA behavior and
  manual UIA smoke scripts are unchanged.
- If helper/smoke scripts, watcher preview behavior, or manual smoke docs
  materially change, refresh the relevant manual smoke before release
  readiness.
- Do not use stale manual evidence to justify new capture surfaces or Phase 6
  implementation.
