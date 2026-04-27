# Release Checklist

Use this checklist before publishing alpha, beta, or release-candidate
prereleases.

For operator setup and the current documentation map, start with
[Operator quickstart](operator-quickstart.md).

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
diagnostic gate meanings.

## Privacy Boundary

Before release, confirm the release notes state that screenshots, OCR, audio,
keyboard capture, clipboard capture, network upload, LLM summarization, and
desktop control remain absent or disabled by default.

Observed content returned through CLI, memory, and MCP must remain marked as
`untrusted_observed_content`.

Related docs:

- [Watcher preview](watcher-preview.md)
- [Read-only MCP compatibility examples](mcp-readonly-examples.md)
- [Known limitations](known-limitations.md)
