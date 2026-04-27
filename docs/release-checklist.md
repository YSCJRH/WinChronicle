# Release Checklist

Use this checklist before publishing alpha, beta, or release-candidate
prereleases.

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

## Privacy Boundary

Before release, confirm the release notes state that screenshots, OCR, audio,
keyboard capture, clipboard capture, network upload, LLM summarization, and
desktop control remain absent or disabled by default.

Observed content returned through CLI, memory, and MCP must remain marked as
`untrusted_observed_content`.
