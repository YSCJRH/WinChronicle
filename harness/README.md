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

## Command Plan Coverage Integrity

The JSON command plan is schema-bound by
`harness/specs/harness-command-plan.schema.json`. The workflow tests verify
the command-plan schema shape and require every `contract_coverage` entry to
identify its `id`, `command_index`, focused `tests`, and `privacy_boundary` so
metadata consumers can audit what the full `pytest -q` gate protects without
running commands.

Coverage metadata also has two drift gates. The tests run
`pytest --collect-only` against every pytest node listed in
`contract_coverage.tests`, catching renamed or deleted checks before metadata
looks healthier than the suite actually is. They also resolve every `spec` and
`fixtures` path as repo-relative artifact paths and repo-relative file
references, catching moved or deleted schema and fixture artifacts without
allowing absolute paths or parent-directory jumps.

These checks stay metadata-only: `--list-commands --format json` does not run
the harness, and `execution` remains `not_run` with `creates_harness_state`,
`starts_subprocesses`, and `reads_observed_content` all false.
For the current coverage entry table, see `CONTRIBUTING.md` under
"Current coverage examples". Treat the JSON command plan as source of truth.
Use `CONTRIBUTING.md` for the entry-level `spec`, `fixtures`, `tests`, and
`privacy_boundary` anchors; this README stays a navigation and integrity
overview.

## Workday Dry-Run Text Fixtures

The Codex workday dry-run text contracts live under
`harness/fixtures/workday/`:

- `plugin_dry_run_text_contract.json`
- `setup_dry_run_text_contract.json`
- `daily_dry_run_text_contract.json`

Those fixtures are schema-bound by
`harness/specs/workday-dry-run-text-contract.schema.json`. Each fixture must
keep exactly these top-level keys: `command`, `expected_contains`,
`forbidden_substrings`, and `ordered_pairs`.

When changing `winchronicle codex plugin`, `winchronicle codex setup`, or
`winchronicle codex daily` text output, update the matching fixture and keep
the read-desktop boundary explicit. Plugin and daily output should retain
`Reads desktop: no`; setup output should retain `reads desktop: no`; and the
matching `desktop: yes` variant must stay forbidden. Re-run the schema and
golden checks before relying on the text contract:

```powershell
python -m pytest tests\test_cli.py::test_workday_dry_run_text_contract_fixtures_match_schema
python -m pytest tests\test_cli.py::test_codex_plugin_dry_run_text_matches_golden_fixture_contract tests\test_cli.py::test_codex_setup_dry_run_text_matches_golden_fixture_contract tests\test_cli.py::test_codex_daily_dry_run_text_matches_golden_fixture_contract
```

The JSON command plan includes a `contract_coverage` entry named
`workday_dry_run_text_contracts` so release tooling and contributors can see
that these schema and golden checks are covered by the full `pytest -q` gate.
This is metadata only; `--list-commands --format json` still does not create
harness state, start subprocesses, or read observed content.

## Workday Stop Summary Fixture

The Workday stop summary golden fixture lives at
`harness/fixtures/workday/stop_human_summary_contract.json` and is schema-bound
by `harness/specs/workday-stop-summary-contract.schema.json`. It keeps the
default human Workday summary contract and the explicit technical Workday
summary contract in the same fixture so the two views cannot drift silently.

The fixture fields `human_summary_forbidden_markers` and
`technical_summary_required_markers` define the summary-style boundary. The
default human Workday summary must hide technical counters, raw local evidence
field names, and telemetry-style labels. The explicit technical Workday summary
must show the technical evidence boundary and the counter labels used for
debugging. This is a text contract only; it does not add a capture source,
start UIA, read the desktop, store raw watcher JSONL, or expose observed text.

Re-run the schema and focused golden checks before relying on this contract:

```powershell
python -m pytest tests\test_workday.py::test_workday_stop_summary_contract_fixture_matches_schema
python -m pytest tests\test_workday.py::test_workday_stop_text_command_matches_human_summary_golden_fixture tests\test_workday.py::test_workday_stop_text_command_keeps_source_notice_in_technical_style tests\test_workday.py::test_workday_summarize_reads_named_session
```

The JSON command plan includes a `contract_coverage` entry named
`workday_stop_summary_contract` for this schema and fixture. It remains inside
the full `pytest -q` gate and only describes fixture-backed text-contract
coverage; it does not run new capture behavior. Its focused metadata freeze is
`tests/test_windows_harness_workflow.py::test_run_harness_json_plan_declares_workday_stop_summary_contract_coverage`.

## MCP Contract Coverage Metadata

The JSON command plan also includes a `contract_coverage` entry named
`mcp_read_only_metadata_contracts`. It points at
`harness/specs/mcp-tool-result.schema.json` and the focused pytest checks that
freeze the read-only MCP tool list, metadata-only behavior, provenance, coverage
confidence meaning, and evidence-policy limitations.

The key checks include:

```powershell
python -m pytest tests/test_compatibility_contracts.py::test_mcp_result_schema_tool_enum_matches_exact_read_only_contract
python -m pytest tests/test_mcp_tools.py::test_mcp_tool_results_include_evidence_policy_matrix
python -m pytest tests/test_mcp_tools.py::test_mcp_metadata_only_mode_omits_observed_text_without_tool_list_change
```

That coverage is still inside the full `pytest -q` gate. It does not add MCP
write tools or new capture behavior. The covered contract keeps MCP read-only,
keeps metadata-only as an exposure-reduction mode, keeps provenance as
`local_winchronicle_state`, keeps confidence meaning
`coverage_quality_not_permission`, and keeps the external sharing requires user
approval limitation visible.

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
release-state validator against `docs/release-evidence.md`, and the
manual-smoke freshness validator against current release docs. The
release-state gate keeps published-release evidence bound to its tag and only
requires a next-release preflight section when `pyproject.toml` moves ahead of
the published package version. The static suite does not call GitHub and does
not inspect observed content.

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
