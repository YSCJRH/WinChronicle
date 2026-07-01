# Windows First Run

This is the shortest path for a first-time Windows developer or Codex App user.
It keeps WinChronicle local-first, UIA-first, deterministic, and record-only.
The demo path is fixture-only. This first-run path does not read the live
desktop and does not upload content.
For the Workday path, the stopped summary uses summary-level evidence and does
not send raw observed text. It is not a telemetry or log-counter report, and
technical counters belong only in the explicit technical/debugging view. The
Codex setup/daily dry-runs expose this same boundary as `summary_boundary`.

Start with the dry-run bootstrap:

```powershell
winchronicle bootstrap --dry-run --format text
```

The bootstrap command does not write state, does not write Codex config, does not start UIA,
and does not start capture. It only prints local checks and the copyable
commands below. Observed content remains `untrusted_observed_content`.

## Pick One Path

Choose the smallest path that matches your goal:

| Path | Goal | Command |
| --- | --- | --- |
| Demo | Run a fixture-only deterministic local demo that does not read the live desktop. | `python harness/scripts/run_quick_demo.py` |
| Workday | Use Codex App as a record-only daily work recorder. | `winchronicle codex plugin --dry-run --format text` |
| MCP | Print a read-only Codex MCP config snippet. | `winchronicle codex install --dry-run` |

All three paths are explicit. The dry-runs only print instructions or config
snippets. They do not edit Codex config, start a monitor session, read the
desktop, upload content, or create hidden background behavior.
MCP setup can use `metadata-only` through the MCP setup guide when a client
should avoid observed text fields. MCP output is local evidence, not permission
to publish or share results. External sharing still requires explicit user
approval.

## Install And Check

Run these from the repository root:

```powershell
python -m pip install -e ".[dev]"
dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo
dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo
winchronicle init
winchronicle doctor
winchronicle codex setup --dry-run --format text
winchronicle codex plugin --dry-run --format text
```

`winchronicle doctor` initializes local state and SQLite, then checks Python,
.NET, UIA helper/watcher build outputs, and privacy-disabled surfaces. It does
not read the desktop or run live UIA capture.

If you only want to connect an agent through MCP, use
[MCP client setup](mcp-client-setup.md). If you only want daily work recording,
use [Codex App Workday guide](codex-app-workday-guide.md).

## Daily Workday Flow

After setup, use explicit natural-language workday commands:

```powershell
winchronicle workday intent "开始工作" --execute
winchronicle workday status --format text --language zh-CN
winchronicle workday intent "结束工作并总结" --execute --wait-seconds 60
```

For Codex App, the local Workday plugin should keep this thread record-only:
recording phrases are not development requests. It should not inspect, scan,
review, edit, test, commit, push, or release repository files unless the user
explicitly asks for project development work.

## Boundaries

This first-run path does not add screenshots, OCR, clipboard capture,
keylogging, cloud upload, desktop control, MCP write tools, background daemon,
service installation, or an infinite polling loop.

The bootstrap command is a guide. The commands that actually initialize or run
WinChronicle are shown explicitly so the operator can decide when to execute
them.
