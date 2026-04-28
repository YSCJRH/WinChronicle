# Release Checklist

Use this checklist before publishing alpha, beta, release-candidate, or final
releases.

For operator setup and the current documentation map, start with
[Operator quickstart](operator-quickstart.md).
For release-candidate evidence shape, use
[Release evidence guide](release-evidence.md).

## Deterministic Gates

- `python -m pytest -q`
- `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo`
- `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo`
- `python harness/scripts/run_install_cli_smoke.py`
- `python harness/scripts/run_harness.py`
- `git diff --check`

These gates must pass on Windows CI and should be rerun locally before release.

## Manual UIA Smoke Gates

Run these on an interactive Windows desktop with temporary state:

- `harness/scripts/smoke-uia-notepad.ps1`: hard gate; marker text must be captured.
- `harness/scripts/smoke-uia-edge.ps1`: hard gate; local HTML body marker must be captured.
- `harness/scripts/smoke-uia-vscode.ps1`: hard gate when `code.cmd` is available; metadata must pass.
- `harness/scripts/smoke-uia-vscode.ps1 -Strict`: diagnostic only; Monaco editor marker failure is not a v0.1 release blocker, but the diagnostic artifact must be kept.

Manual smoke scripts must not print observed content and must not activate,
click, type, move, resize, or control windows.

Record manual smoke evidence with
[Manual smoke evidence template](manual-smoke-evidence-template.md). See
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

## Post-Publication Reconciliation

After publishing, confirm the repository records the release URL, exact tag
target, PR Windows Harness URL, post-merge `main` Windows Harness URL, and
next active execution cursor. Do not commit observed-content artifacts while
reconciling release evidence.
