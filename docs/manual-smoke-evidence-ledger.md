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
| Stable release baseline | `v0.1.7` |
| Current maintenance plan | Establish post-v0.1.7 plan before new implementation |
| Latest completed maintenance plan | [Post-v0.1.6 maintenance plan](next-round-plan-post-v0.1.6.md) |
| Published release record | [v0.1.7 maintenance release record](release-v0.1.7.md) |
| Latest published release record | [v0.1.7 maintenance release record](release-v0.1.7.md) |
| Latest full manual UIA smoke source | [v0.1.0 final release readiness record](release-v0.1.0.md) |
| Freshness policy | Manual smoke inherited from older releases is inherited/stale unless rerun and recorded for the current release. |
| Last freshness decision | For the post-v0.1.6 compatible maintenance path toward `v0.1.7`, inherited `v0.1.0` Notepad, Edge, VS Code metadata, VS Code strict diagnostic, and watcher preview manual evidence is explicitly accepted by the T4 release-readiness record because the release path changed documentation, tests, CI/runtime metadata, version metadata, deterministic harness evidence, and compatibility evidence without changing helper behavior, watcher product behavior, manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP shape, or capture surfaces. Fresh manual smoke is still required if a later stage changes any of those boundaries or if the release approver requires fresh hard-gate evidence. |
| Next freshness decision | The next post-v0.1.7 plan must make a release-specific freshness decision before any later publication path. |

## Latest Known Manual Evidence

| Gate | Release meaning | Latest known result | Freshness | Evidence source | Refresh requirement | Artifact policy |
| --- | --- | --- | --- | --- | --- | --- |
| Notepad targeted UIA smoke | Hard manual release gate | Pass | Inherited from `v0.1.0`; historically accepted for the compatible `v0.1.5` path, explicitly accepted by S4 for the compatible `v0.1.6` path, and explicitly accepted by T4 for the compatible `v0.1.7` path | [v0.1.0 final release readiness record](release-v0.1.0.md) | Refresh if helper behavior, manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP shape, or capture surfaces change, or if the release approver requires fresh hard-gate evidence | Local JSON artifact path only; do not commit capture JSON |
| Edge targeted UIA smoke | Hard manual release gate | Pass | Inherited from `v0.1.0`; historically accepted for the compatible `v0.1.5` path, explicitly accepted by S4 for the compatible `v0.1.6` path, and explicitly accepted by T4 for the compatible `v0.1.7` path | [v0.1.0 final release readiness record](release-v0.1.0.md) | Refresh if helper behavior, manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP shape, or capture surfaces change, or if the release approver requires fresh hard-gate evidence | Local JSON artifact path only; do not commit local HTML or capture JSON |
| VS Code metadata smoke | Conditional hard manual release gate when `code.cmd` is available | Pass with diagnostic warning | Inherited from `v0.1.0`; historically accepted for the compatible `v0.1.5` path, explicitly accepted by S4 for the compatible `v0.1.6` path, and explicitly accepted by T4 for the compatible `v0.1.7` path | [v0.1.0 final release readiness record](release-v0.1.0.md) | Refresh if helper behavior, manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP shape, or capture surfaces change, or if the release approver requires fresh hard-gate evidence | Local JSON artifact only; do not commit editor contents |
| VS Code strict Monaco marker | Diagnostic, non-blocking for v0.1 | Diagnostic failure, known Monaco/UIA limitation | Inherited diagnostic from `v0.1.0`; historically accepted for `v0.1.5` as diagnostic context only, explicitly accepted by S4 for `v0.1.6` as diagnostic context only, and explicitly accepted by T4 for `v0.1.7` as diagnostic context only | [v0.1.0 final release readiness record](release-v0.1.0.md) | Refresh only if investigating Monaco/UIA exposure or changing smoke scripts | Local diagnostic artifact path only |
| Watcher preview live smoke | Preview diagnostic/manual confidence gate | Heartbeat-only liveness diagnostic; deterministic watcher gates passed | Inherited diagnostic from `v0.1.0`; historically accepted for `v0.1.5` as diagnostic context, with deterministic watcher coverage current through harness, explicitly accepted by S4 for `v0.1.6` as diagnostic context only, and explicitly accepted by T4 for `v0.1.7` as diagnostic context only | [v0.1.0 final release readiness record](release-v0.1.0.md) and `python harness/scripts/run_harness.py` | Refresh only if watcher preview behavior or live smoke scripts change, or if release approval requires live evidence | Do not save or commit raw watcher JSONL |

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
- Fresh manual smoke must use the
  [Manual smoke evidence template](manual-smoke-evidence-template.md).
- Inherited evidence can provide context, but it is not current evidence unless
  the release record explicitly accepts it for that release.
- For the post-v0.1.5 path that published `v0.1.6`, inherited `v0.1.0`
  manual smoke was explicitly accepted by the S4 release record only because
  the release path did not change helper behavior, watcher product behavior,
  manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP
  shape, or capture surfaces.
- For the active post-v0.1.6 path toward `v0.1.7`, inherited `v0.1.0`
  manual smoke is explicitly accepted by the T4 release-readiness record for
  this compatible path because helper behavior, watcher product behavior,
  manual smoke scripts, capture behavior, privacy behavior, product CLI/MCP
  shape, and capture surfaces are unchanged.
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
