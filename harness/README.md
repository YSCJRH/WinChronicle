# WinChronicle Harness

The harness contains deterministic contracts, fixtures, scorecards, and scripts
used before real Windows UIA capture is implemented.

Phase 0 covers fixture-only capture, redaction, schema validation, local storage,
and search.

Phase 2 starts with helper output contracts in `harness/specs/` and
helper-like JSON fixtures in `harness/fixtures/uia-helper/`; these do not invoke
real Windows UIA capture. The harness also compiles the experimental
`resources/win-uia-helper` .NET helper without running it.

Phase 3 starts with watcher event contracts and JSONL fixtures in
`harness/fixtures/watcher/`. The `watch --events` command dispatches those
deterministic fixtures and does not start a real WinEvent hook yet.
The experimental `resources/win-uia-watcher` .NET watcher scaffold is compiled
by the harness. `harness/scripts/run_watcher_smoke.py` runs it briefly with a
fake helper and temporary state, without reading live UI content.
The full harness also exercises `python -m winchronicle watch --watcher` with
`harness/scripts/fake_uia_helper.py`; this verifies the live-wrapper code path
without storing raw watcher JSONL.

Phase 4 adds a read-only MCP stdio surface. `harness/scripts/run_mcp_smoke.py`
seeds a deterministic fixture capture, lists MCP tools, calls `privacy_status`,
and verifies `search_captures` without exposing desktop control tools or any
live capture surface.

Phase 5 starts with a deterministic memory reducer. `generate-memory` reads
already-redacted indexed captures, writes `memory/event-YYYY-MM-DD.md`, and
indexes the Markdown in SQLite `entries` / `entries_fts`; `search-memory`
queries that durable memory without changing raw capture search.

For a manual foreground-window helper smoke, focus the target app first and run:

```powershell
python harness/scripts/run_uia_helper_smoke.py --helper path\to\win-uia-helper.exe --delay-seconds 5 --expect-app Notepad --expect-text "some visible text"
```

The delay gives you time to focus the target app before capture. The smoke uses
a temporary `WINCHRONICLE_HOME` and does not print observed content.

For Phase 2 app-specific smoke gates, use the harness-only targeted helper path:

```powershell
.\harness\scripts\smoke-uia-notepad.ps1
.\harness\scripts\smoke-uia-edge.ps1
.\harness\scripts\smoke-uia-vscode.ps1
.\harness\scripts\smoke-uia-vscode.ps1 -Strict
```

These scripts set `WINCHRONICLE_HARNESS=1`, call only
`win-uia-helper capture --harness ... --no-store`, and write temporary JSON
artifacts. They do not activate, click, type, move, resize, or control windows,
and the product CLI still captures only `GetForegroundWindow`.

The VS Code smoke treats window metadata as the hard gate by default. Use
`-Strict` to require the editor marker itself; if strict mode fails, keep the
diagnostic artifact because some Monaco editor sessions do not expose buffer
text through UIA even with `editor.accessibilitySupport` enabled.

Run the full local harness from the repository root:

```powershell
python harness/scripts/run_harness.py
.\harness\scripts\run_harness.ps1
```

The runner uses a temporary `WINCHRONICLE_HOME` so CLI smoke checks do not write
to the user's normal WinChronicle state directory.
