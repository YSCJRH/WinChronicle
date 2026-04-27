# Manual Smoke Evidence Template

Use this template for release-candidate manual smoke notes. Keep the completed
evidence in the release record or PR comment; do not commit observed-content
artifacts by default.

Do not paste observed text, screenshots, OCR output, raw helper JSON, raw
watcher JSONL, secrets, passwords, local page contents, or editor buffer
contents into this document. Record only commands, pass/fail result, artifact
paths, timestamps, and environment notes.

## Run Metadata

- Release candidate:
- Operator:
- Started at:
- Completed at:
- Machine:
- Windows version:
- Shell:
- Python:
- .NET SDK:
- WinChronicle commit:
- `WINCHRONICLE_HOME`:
- Artifact root:

## Preflight

| Check | Command | Result | Notes |
| --- | --- | --- | --- |
| Clean worktree | `git status --short --branch` |  |  |
| Unit tests | `python -m pytest -q` |  |  |
| Helper build | `dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo` |  |  |
| Watcher build | `dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo` |  |  |
| Deterministic harness | `python harness/scripts/run_harness.py` |  |  |

## Notepad Targeted Smoke

Hard gate. The helper-only targeted path must capture the unique Notepad marker
without activating, clicking, typing, moving, resizing, or controlling the
target window.

| Field | Evidence |
| --- | --- |
| Command | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-notepad.ps1` |
| Started at |  |
| Completed at |  |
| Result |  |
| Artifact path |  |
| Notes |  |

## Edge Targeted Smoke

Hard gate. The helper-only targeted path must capture the local HTML body marker
from Edge. URL extraction is best effort and is not a hard gate.

| Field | Evidence |
| --- | --- |
| Command | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-edge.ps1` |
| Started at |  |
| Completed at |  |
| Result |  |
| Artifact path |  |
| URL attempt result |  |
| Notes |  |

## VS Code Metadata Smoke

Conditional hard gate when `code.cmd` is available. Metadata must pass even when
Monaco editor marker text is not exposed through standard UIA.

| Field | Evidence |
| --- | --- |
| Availability check | `where code.cmd` |
| Command | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1` |
| Started at |  |
| Completed at |  |
| Result |  |
| Artifact path |  |
| Notes |  |

## VS Code Strict Monaco Diagnostic

Diagnostic, non-blocking gate. Strict marker failure is a known Monaco/UIA
limitation and is not a v0.1 release blocker. If it fails, record the diagnostic
artifact path only.

| Field | Evidence |
| --- | --- |
| Command | `powershell -ExecutionPolicy Bypass -File harness/scripts/smoke-uia-vscode.ps1 -Strict` |
| Started at |  |
| Completed at |  |
| Result |  |
| Diagnostic artifact path |  |
| Notes |  |

## Watcher Preview Smoke

Preview gate. Use a temporary `WINCHRONICLE_HOME`; do not save or commit raw
watcher JSONL. Confirm event-driven behavior and diagnostics only.

| Check | Command or observation | Result | Artifact path | Notes |
| --- | --- | --- | --- | --- |
| Foreground switch emits event | `python -m winchronicle watch --watcher <watcher> --helper <helper> --duration 30` |  |  |  |
| Typing burst debounced | Manual observation during the same timed run |  |  |  |
| Duplicate skip | Manual observation or deterministic fixture confirmation |  |  |  |
| Denylisted app skipped | Manual observation with temporary config |  |  |  |
| Failure mode diagnostic | Record nonzero watcher/helper/malformed/timeout result without observed content |  |  |  |

## Release Decision

- Hard gates passed:
- Conditional hard gates skipped and why:
- Diagnostic failures:
- Follow-up issue or PR:
- Operator sign-off:
