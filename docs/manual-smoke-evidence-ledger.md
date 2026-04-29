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
| Stable release baseline | `v0.1.2` |
| Active maintenance plan | [Post-v0.1.2 maintenance plan](next-round-plan-post-v0.1.2.md) |
| Latest published release record | [v0.1.2 maintenance release record](release-v0.1.2.md) |
| Latest full manual UIA smoke source | [v0.1.0 final release readiness record](release-v0.1.0.md) |
| Freshness policy | Manual smoke inherited from older releases is inherited/stale unless rerun and recorded for the current release. |

## Latest Known Manual Evidence

| Gate | Release meaning | Latest known result | Freshness | Evidence source | Refresh requirement | Artifact policy |
| --- | --- | --- | --- | --- | --- | --- |
| Notepad targeted UIA smoke | Hard manual release gate | Pass | Inherited from `v0.1.0`; stale for a new release unless rerun or explicitly accepted | [v0.1.0 final release readiness record](release-v0.1.0.md) | Refresh before `v0.1.3` release readiness if manual hard gates are required | Local JSON artifact path only; do not commit capture JSON |
| Edge targeted UIA smoke | Hard manual release gate | Pass | Inherited from `v0.1.0`; stale for a new release unless rerun or explicitly accepted | [v0.1.0 final release readiness record](release-v0.1.0.md) | Refresh before `v0.1.3` release readiness if manual hard gates are required | Local JSON artifact path only; do not commit local HTML or capture JSON |
| VS Code metadata smoke | Conditional hard manual release gate when `code.cmd` is available | Pass with diagnostic warning | Inherited from `v0.1.0`; stale for a new release unless rerun or explicitly accepted | [v0.1.0 final release readiness record](release-v0.1.0.md) | Refresh when `code.cmd` is available and manual hard gates are required | Local JSON artifact path only; do not commit editor contents |
| VS Code strict Monaco marker | Diagnostic, non-blocking for v0.1 | Diagnostic failure, known Monaco/UIA limitation | Inherited diagnostic from `v0.1.0` | [v0.1.0 final release readiness record](release-v0.1.0.md) | Refresh only if investigating Monaco/UIA exposure or changing smoke docs/scripts | Local diagnostic artifact path only |
| Watcher preview live smoke | Preview diagnostic/manual confidence gate | Heartbeat-only liveness diagnostic; deterministic watcher gates passed | Inherited diagnostic from `v0.1.0`; deterministic watcher coverage remains current through harness | [v0.1.0 final release readiness record](release-v0.1.0.md) and `python harness/scripts/run_harness.py` | Refresh only if watcher preview behavior, docs, or release checklist requires live evidence | Do not save or commit raw watcher JSONL |

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
- If helper/smoke scripts, watcher preview behavior, or manual smoke docs
  materially change, refresh the relevant manual smoke before release
  readiness.
- Do not use stale manual evidence to justify new capture surfaces or Phase 6
  implementation.

