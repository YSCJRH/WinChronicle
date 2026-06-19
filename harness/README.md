# WinChronicle Harness

The harness contains deterministic contracts, fixtures, scorecards, and scripts
that keep fixture capture, explicit foreground UIA helper capture, watcher
preview, memory, and MCP behavior inside the v0.1 privacy boundary.

Phase 0 covers fixture capture, redaction, schema validation, local storage,
and search. Deterministic fixtures remain the default CI substrate.

Phase 2 starts with helper output contracts in `harness/specs/` and
helper-like JSON fixtures in `harness/fixtures/uia-helper/`; default CI does
not invoke live Windows UIA capture. The harness also compiles the experimental
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
verifies `search_captures`, and verifies `search_memory` without exposing
desktop control tools or any live capture surface.

Phase 5 starts with a deterministic memory reducer. `generate-memory` reads
already-redacted indexed captures, writes `memory/event-YYYY-MM-DD.md`, and
indexes the Markdown in SQLite `entries` / `entries_fts`; `search-memory`
queries that durable memory without changing raw capture search.

The release-candidate install smoke creates a temporary virtual environment,
installs the local package without fetching dependencies, and runs deterministic
CLI commands against a temporary `WINCHRONICLE_HOME`:

```powershell
python harness/scripts/run_install_cli_smoke.py
```

It verifies `python -m winchronicle --help`, `init`, `status`,
`capture-once`, `search-captures`, `generate-memory`, and `search-memory`
without invoking real UIA, screenshots, OCR, audio, keyboard capture, clipboard
capture, network upload, or desktop control.

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
to the user's normal WinChronicle state directory. It also runs the static
release-evidence validator against the published `v0.2.0` release record, the
strict current-release validator against `docs/release-evidence.md`, and the
manual-smoke freshness validator against current release docs. The static suite
does not call GitHub and does not inspect observed content.

To inspect the deterministic gate list without executing the harness, run:

```powershell
python harness/scripts/run_harness.py --list-commands
python harness/scripts/run_harness.py --list-commands --format json
```

This prints the command plan in execution order. The JSON form is intended for
release tooling that needs a stable, machine-readable plan. This mode does not
create harness state, start subprocesses, or read observed content.

## Harness Timeouts

`python harness/scripts/run_harness.py` defaults to 900 seconds per subprocess.
Override this only for local diagnosis with
`WINCHRONICLE_HARNESS_COMMAND_TIMEOUT_SECONDS`.

`python harness/scripts/run_install_cli_smoke.py` defaults to 300 seconds per
subprocess. Override this only for local diagnosis with
`WINCHRONICLE_INSTALL_CLI_SMOKE_COMMAND_TIMEOUT_SECONDS`.

The Windows CI workflow wraps `python harness/scripts/run_harness.py` in a
30-minute outer timeout so a stuck release gate fails instead of hanging. The
step-level timeout is intentionally longer than the per-subprocess default
because the full harness runs several independent commands.

Timeout handlers print the command and timeout value, but do not print partial
stdout or stderr. A timed-out command may already have emitted observed content
before it is killed, so diagnostics must stay content-free. Raising or lowering
these values does not expand capture surfaces, start live UIA capture, enable
screenshots, OCR, clipboard capture, cloud upload, desktop control, or MCP write
tools.

Before publishing alpha or beta releases, use `docs/release-checklist.md`.
Phase 6 screenshot/OCR enrichment is tracked only as a privacy scorecard until
tests and explicit opt-in configuration exist.
