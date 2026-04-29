# Release Checklist

Use this checklist before publishing alpha, beta, release-candidate, or final
releases.

For operator setup and the current documentation map, start with
[Operator quickstart](operator-quickstart.md).
The active post-v0.1.2 execution cursor lives in
[Post-v0.1.2 maintenance plan](next-round-plan-post-v0.1.2.md). For release
evidence shape, use [Release evidence guide](release-evidence.md).

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

- the active execution cursor points to the current post-v0.1.2 plan until a
  future plan supersedes it;
- the stable baseline is `v0.1.2` unless release-readiness work explicitly
  prepares another version;
- manual UIA smoke inherited from an earlier release is labeled as inherited or
  stale, not current;
- stale manual smoke can support context, but a hard release gate needs fresh
  evidence or an explicit documented decision to keep the older result;
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
