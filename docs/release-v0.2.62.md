# v0.2.62 Release Record

This record tracks the `v0.2.62` redaction hardening release path. It records
commands, results, environment notes, and local artifact paths only. It does not
commit observed screen-content artifacts.

## Release Decision

`v0.2.62` is warranted by a privacy-positive redaction hardening: obvious
API-key labels now redact long values assigned with common `:` or spaced `=`
syntax, while preserving local-first storage and read-only MCP boundaries.

Publication status: pre-publication package preflight.

## Candidate Metadata

| Field | Value |
| --- | --- |
| Release | `v0.2.62` |
| Stage | `v0.2.62` redaction hardening release |
| Evidence date | 2026-06-20, Asia/Shanghai |
| Publication status | Published final release |
| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.62 |
| Published at | `2026-06-20T04:52:36Z` |
| Final tag target | `f42528c52e5e61b602671382617e97ca5c94ad69` |
| Windows Harness | https://github.com/YSCJRH/WinChronicle/actions/runs/27860594785, head `f42528c52e5e61b602671382617e97ca5c94ad69`, conclusion `success` |
| Previous package/tag release | `v0.2.61` |
| Previous package/tag release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.61 |
| Manual smoke artifact root | `C:\Users\34793\AppData\Local\Temp\winchronicle-v0262-smoke-8382047382604e3590ec4074c8a260e2` |

Environment:

- Windows interactive desktop, PowerShell.
- Python: `3.11`.
- .NET SDK: `8.0`.

## Deterministic Gates

| Gate | Result | Evidence |
| --- | --- | --- |
| `python -m pytest tests/test_redaction.py tests/test_privacy_policy_contract.py tests/test_privacy_check.py tests/test_privacy_index_parity.py tests/test_mcp_tools.py tests/test_version_identity.py tests/test_release_evidence_validator.py tests/test_manual_smoke_freshness_validator.py tests/test_codex_workday_plugin.py -q` | Pass | `82 passed` |
| `python -m pytest -q` | Pass | `419 passed` |
| `python harness/scripts/check_release_evidence.py --project pyproject.toml --require-release-state docs/release-evidence.md` | Pass | release evidence has expected-repo GitHub release URL and Windows Harness Actions run URL |
| `python harness/scripts/check_manual_smoke_freshness.py --project pyproject.toml --ledger docs/manual-smoke-evidence-ledger.md --guide docs/release-evidence.md --checklist docs/release-checklist.md` | Pass | package/tag release and manual UIA smoke source are explicitly separated |
| `git diff --check` | Pass | no whitespace errors |
| `python harness/scripts/run_harness.py` | Pass | full harness passed: 419 pytest tests, release validators, helper/watcher builds with 0 warnings and 0 errors, quick demo, watcher smokes, MCP smoke, install CLI smoke, privacy check, fixture capture/search/memory, deterministic watcher fixture, and watcher fake-helper smoke |

## Manual UIA Smoke Gates

Manual smoke used local temporary artifacts only. Do not commit the artifact JSON
files; they may contain observed screen content.

| Gate | Result | Evidence |
| --- | --- | --- |
| Notepad targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-notepad.ps1 -ArtifactDir <artifact-root>\notepad -TimeoutSeconds 30`; artifact `<artifact-root>\notepad\notepad-capture.json` |
| Edge targeted UIA smoke | Pass | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-edge.ps1 -ArtifactDir <artifact-root>\edge -TimeoutSeconds 45`; artifact `<artifact-root>\edge\edge-capture.json` |
| VS Code metadata smoke | Pass with diagnostic warning | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -ArtifactDir <artifact-root>\vscode-metadata -TimeoutSeconds 45`; metadata passed, editor marker was not exposed through UIA |
| VS Code strict Monaco marker | Diagnostic failure, non-blocking | `powershell -ExecutionPolicy Bypass -File harness\scripts\smoke-uia-vscode.ps1 -Strict -ArtifactDir <artifact-root>\vscode-strict -TimeoutSeconds 45`; known Monaco/UIA limitation |
| Fake-helper monitor watcher | Pass | `python -m winchronicle monitor --watcher dotnet --watcher-arg resources/win-uia-watcher/bin/Debug/net8.0-windows/win-uia-watcher.dll --helper python --helper-arg harness/scripts/fake_uia_helper.py --duration 1 --heartbeat-ms 250 --capture-on-start --session-id release-fake-helper-v0262` returned `captures_written: 1`, `duplicates_skipped: 0`, `denylisted_skipped: 0`, `heartbeats: 4`, and local session/report paths under the temporary `WINCHRONICLE_HOME` |

## Release Notes

- Extends obvious API-key redaction to long values assigned with common `:` or
  spaced `=` syntax for existing key labels such as `SECRET_KEY`,
  `ACCESS_TOKEN`, and `BEARER_TOKEN`.
- Keeps labels and separators in redacted text while replacing only the secret
  value with `[REDACTED:api_key]`.
- Updates the privacy policy spec and manual-smoke freshness validator so
  fresh-smoke and inherited-smoke preflight decisions are both explicit.
- Aligns package, runtime, plugin, and MCP server version identity to `0.2.62`.

## Privacy And Scope Confirmation

- Local-first: captured content remains local; no cloud or network upload is
  implemented.
- UIA-first and harness-first boundaries remain in place.
- Screenshots, OCR, audio recording, keyboard capture, clipboard capture, LLM
  calls, desktop control, MCP write tools, daemon/service installation, polling
  capture loops, default background capture, and product targeted capture remain
  out of scope.
- Observed content remains untrusted and must remain marked as
  `untrusted_observed_content` in captures, memory, CLI search, session
  summaries, and MCP responses.
- Password fields and obvious secrets must not be stored, including API keys,
  private keys, JWTs, GitHub tokens, Slack tokens, and token canaries.

## Publication Reconciliation

Publication was verified against the `v0.2.62` GitHub release, remote tag target,
and Windows Harness run. `docs/release-evidence.md`,
`docs/release-checklist.md`, and `docs/manual-smoke-evidence-ledger.md` now
record `v0.2.62` as the latest package/tag release, and no
`Next Package Release Preflight` section remains for the published project
version.
