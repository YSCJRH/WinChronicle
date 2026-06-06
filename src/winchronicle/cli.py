from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from ._version import __version__
from .capture import capture_frontmost_with_helper, capture_once_from_fixture, privacy_check_path
from .events import dispatch_watcher_events, run_watcher_command
from .memory import generate_memory_entries
from .mcp.server import TOOL_NAMES, run_stdio
from .paths import ensure_state, state_paths
from .privacy import DISABLED_SURFACE_STATUS, TRUST, privacy_contract_payload
from .projects import add_project, load_project_registry, remove_project, snapshot_projects
from .session import monitor_events, read_session, run_monitor_watcher_command, session_count
from .storage import capture_count, init_db, memory_entry_count, search_captures, search_memory_entries
from .workday import (
    CAPTURE_SURFACE,
    DEFAULT_CHECKPOINT_SECONDS,
    DEFAULT_DURATION_SECONDS,
    MAX_DURATION_SECONDS,
    WorkdayError,
    default_helper_command,
    default_watcher_command,
    doctor_workday,
    format_workday_status_text,
    format_workday_text_summary,
    recover_workday_runner_failure,
    run_workday,
    start_workday,
    status_workday,
    stop_workday,
    summarize_workday,
)


FORBIDDEN_PASSTHROUGH_FLAGS = (
    "--hwnd",
    "--pid",
    "--window-title",
    "--window-title-regex",
    "--process-name",
    "--screenshot",
    "--ocr",
    "--audio",
    "--keyboard",
    "--clipboard",
    "--control",
)

CODEX_MCP_ENABLED_TOOLS = [
    "privacy_status",
    "current_context",
    "recent_activity",
    "search_memory",
    "search_captures",
    "read_recent_capture",
]
CODEX_WORKDAY_ACCEPTED_PHRASES = [
    "开始工作",
    "开始记录工作",
    "结束工作并总结",
    "停止工作并总结",
    "查看工作记录状态",
]
CODEX_WORKDAY_DEFAULT_PROMPTS = [
    "开始记录工作",
    "停止工作并总结",
    "查看工作记录状态",
]
CODEX_WORKDAY_NEXT_PROMPTS = [
    "开始记录工作",
    "查看工作记录状态",
    "停止工作并总结",
]
CODEX_RECORD_ONLY_PROMPT_COMMAND = "winchronicle codex daily --dry-run --format text"
CODEX_PLUGIN_POST_INSTALL_SELF_CHECK = [
    "After adding the plugin source, open a new Codex App thread in the folder you want to record.",
    "Say: 查看工作记录状态",
    "Expected local command: winchronicle workday status --format text --language zh-CN",
]
CODEX_RECORD_ONLY_THREAD_PROMPT = (
    "Only call WinChronicle workday commands for this thread.\n"
    "Do not inspect, scan, review, edit, test, commit, push, or release repository files.\n"
    'When I say "开始工作" or "开始记录工作", run:\n'
    'winchronicle workday intent "开始工作" --execute\n'
    'When I say "结束工作并总结" or "停止工作并总结", run:\n'
    'winchronicle workday intent "结束工作并总结" --execute --wait-seconds 60\n'
    'When I say "查看工作记录状态", run:\n'
    "winchronicle workday status --format text --language zh-CN\n"
    "Only paste a summary into chat after the user explicitly asks for chat output.\n"
)
CODEX_RECORDING_MODE_BOUNDARY = (
    "Recording phrases are not development requests. Execute the matching "
    "WinChronicle workday command first; do not run repository preflight "
    "commands such as git status, rg, Get-ChildItem, Get-Content, or ls "
    "unless the user explicitly asks for project development work."
)

WORKDAY_INTENT_TRUST = "local_workday_intent_mapping"
WORKDAY_START_PHRASES = ("开始记录工作", "开始工作")
WORKDAY_STOP_SUMMARY_PHRASES = ("停止工作并总结", "结束工作并总结")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="winchronicle")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialize the local WinChronicle state directory.")
    subparsers.add_parser("status", help="Print local state and privacy feature status as JSON.")
    subparsers.add_parser(
        "doctor",
        help="Check local install, state, helper build outputs, and disabled privacy surfaces.",
    )

    capture = subparsers.add_parser("capture-once", help="Capture a deterministic fixture once.")
    capture.add_argument("--fixture", required=True, type=Path)

    frontmost = subparsers.add_parser(
        "capture-frontmost",
        help="Capture the foreground window through an explicit UIA helper.",
    )
    frontmost.add_argument("--helper", required=True, help="Path or command for win-uia-helper.")
    frontmost.add_argument(
        "--helper-arg",
        action="append",
        default=[],
        help="Extra argument passed to the helper command before capture-frontmost.",
    )
    frontmost.add_argument("--depth", type=int, default=80)

    privacy = subparsers.add_parser("privacy-check", help="Dry-run redaction and privacy gates.")
    privacy.add_argument("path", type=Path)

    search = subparsers.add_parser("search-captures", help="Search locally indexed captures.")
    search.add_argument("query")

    generate_memory = subparsers.add_parser(
        "generate-memory",
        help="Generate deterministic Markdown memory entries from indexed captures.",
    )
    generate_memory.add_argument("--date", help="Generate memory only for YYYY-MM-DD.")

    search_memory = subparsers.add_parser("search-memory", help="Search durable memory entries.")
    search_memory.add_argument("query")

    watch = subparsers.add_parser("watch", help="Dispatch watcher events from fixtures or a watcher command.")
    watch_source = watch.add_mutually_exclusive_group(required=True)
    watch_source.add_argument("--events", type=Path)
    watch_source.add_argument("--watcher", help="Path or command for win-uia-watcher.")
    watch.add_argument(
        "--watcher-arg",
        action="append",
        default=[],
        help="Extra argument passed to the watcher command before watch.",
    )
    watch.add_argument("--helper", help="Path or command for win-uia-helper.")
    watch.add_argument(
        "--helper-arg",
        action="append",
        default=[],
        help="Extra argument passed to the helper command before capture-frontmost.",
    )
    watch.add_argument("--depth", type=int, default=80)
    watch.add_argument("--duration", type=int, default=30)
    watch.add_argument("--debounce-ms", type=int, default=750)
    watch.add_argument("--heartbeat-ms", type=int, default=5000)
    watch.add_argument("--capture-on-start", action="store_true")

    monitor = subparsers.add_parser(
        "monitor",
        help="Run an explicit finite local UIA monitor session.",
    )
    monitor_source = monitor.add_mutually_exclusive_group(required=True)
    monitor_source.add_argument("--events", type=Path)
    monitor_source.add_argument("--watcher", help="Path or command for win-uia-watcher.")
    monitor.add_argument(
        "--watcher-arg",
        action="append",
        default=[],
        help="Extra argument passed to the watcher command before watch.",
    )
    monitor.add_argument("--helper", help="Path or command for win-uia-helper.")
    monitor.add_argument(
        "--helper-arg",
        action="append",
        default=[],
        help="Extra argument passed to the helper command before capture-frontmost.",
    )
    monitor.add_argument("--depth", type=int, default=80)
    monitor.add_argument("--duration", type=int, default=30)
    monitor.add_argument("--debounce-ms", type=int, default=750)
    monitor.add_argument("--heartbeat-ms", type=int, default=5000)
    monitor.add_argument("--capture-on-start", action="store_true")
    monitor.add_argument("--session-id")
    monitor.add_argument(
        "--exclude-app",
        action="append",
        default=[],
        help="Skip exact app names in this monitor session.",
    )

    summarize_session = subparsers.add_parser(
        "summarize-session",
        help="Print a saved monitor session summary as JSON.",
    )
    summarize_session.add_argument("session")

    subparsers.add_parser("mcp-stdio", help="Run the read-only MCP stdio server.")

    projects = subparsers.add_parser(
        "projects",
        help="Manage the explicit local project allowlist used by workday summaries.",
    )
    project_subparsers = projects.add_subparsers(
        dest="projects_command",
        required=True,
        metavar="{add,list,remove,snapshot}",
    )
    project_add = project_subparsers.add_parser(
        "add",
        help="Add an explicit local project directory to workday summaries.",
    )
    project_add.add_argument("path", type=Path)
    project_add.add_argument("--name", help="Optional display name for the project.")
    project_subparsers.add_parser(
        "list",
        help="Print the registered project allowlist as JSON.",
    )
    project_remove = project_subparsers.add_parser(
        "remove",
        help="Remove a project by exact name or path.",
    )
    project_remove.add_argument("identifier")
    project_subparsers.add_parser(
        "snapshot",
        help="Print lightweight git metadata for registered projects.",
    )

    workday = subparsers.add_parser(
        "workday",
        help="Manage an explicit finite local workday recording session.",
    )
    workday_subparsers = workday.add_subparsers(
        dest="workday_command",
        required=True,
        metavar="{start,status,doctor,stop,summarize,intent}",
    )
    workday_start = workday_subparsers.add_parser(
        "start",
        help="Start an explicit bounded workday monitor session.",
    )
    workday_start.add_argument("--watcher", help="Path or command for win-uia-watcher.")
    workday_start.add_argument(
        "--watcher-arg",
        action="append",
        default=[],
        help="Extra argument passed to the watcher command before watch.",
    )
    workday_start.add_argument("--helper", help="Path or command for win-uia-helper.")
    workday_start.add_argument(
        "--helper-arg",
        action="append",
        default=[],
        help="Extra argument passed to the helper command before capture-frontmost.",
    )
    workday_start.add_argument("--depth", type=int, default=80)
    workday_start.add_argument("--duration", type=int, default=DEFAULT_DURATION_SECONDS)
    workday_start.add_argument("--debounce-ms", type=int, default=750)
    workday_start.add_argument("--heartbeat-ms", type=int, default=5000)
    workday_start.add_argument("--checkpoint-seconds", type=int, default=DEFAULT_CHECKPOINT_SECONDS)
    workday_start.add_argument("--capture-on-start", action="store_true", default=True)
    workday_start.add_argument("--session-id")
    workday_start.add_argument(
        "--exclude-app",
        action="append",
        default=[],
        help="Skip exact app names in this workday session.",
    )
    workday_start.add_argument(
        "--focus",
        action="append",
        default=[],
        help="Optional user-stated focus note for the resulting human workday summary.",
    )

    workday_status = workday_subparsers.add_parser(
        "status",
        help="Print active workday session state.",
    )
    workday_status.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Output JSON by default, or a deterministic operator-facing text status.",
    )
    workday_status.add_argument(
        "--language",
        choices=("zh-CN",),
        default="zh-CN",
        help="Language for --format text output.",
    )

    workday_doctor = workday_subparsers.add_parser(
        "doctor",
        help="Diagnose active workday session health without capturing content.",
    )
    workday_doctor.add_argument(
        "--checkpoint-stale-seconds",
        type=int,
        default=DEFAULT_CHECKPOINT_SECONDS * 2,
        help="Treat an active checkpoint older than this many seconds as stale.",
    )

    workday_stop = workday_subparsers.add_parser(
        "stop",
        help="Stop the active workday session and print a summary when available.",
    )
    workday_stop.add_argument("--wait-seconds", type=int, default=30)
    workday_stop.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Output JSON by default, or a deterministic operator-facing text summary when available.",
    )
    workday_stop.add_argument(
        "--language",
        choices=("zh-CN",),
        default="zh-CN",
        help="Language for --format text output.",
    )
    workday_stop.add_argument(
        "--confirmation",
        "--note",
        action="append",
        dest="confirmation",
        default=[],
        help="Optional user-confirmed note to include in the text summary.",
    )
    workday_stop.add_argument(
        "--summary-style",
        choices=("human", "technical"),
        default="human",
        help="Use human daily-review text by default, or technical evidence text for debugging.",
    )

    workday_summarize = workday_subparsers.add_parser(
        "summarize",
        help="Print a saved workday session summary.",
    )
    workday_summarize.add_argument("session")
    workday_summarize.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Output JSON by default, or a deterministic operator-facing text summary.",
    )
    workday_summarize.add_argument(
        "--language",
        choices=("zh-CN",),
        default="zh-CN",
        help="Language for --format text output.",
    )
    workday_summarize.add_argument(
        "--confirmation",
        "--note",
        action="append",
        dest="confirmation",
        default=[],
        help="Optional user-confirmed note to include in the text summary.",
    )
    workday_summarize.add_argument(
        "--summary-style",
        choices=("human", "technical"),
        default="human",
        help="Use human daily-review text by default, or technical evidence text for debugging.",
    )

    workday_intent = workday_subparsers.add_parser(
        "intent",
        help="Map allowlisted natural-language workday phrases to bounded commands.",
    )
    workday_intent.add_argument("phrase")
    workday_intent.add_argument(
        "--execute",
        action="store_true",
        help="Run the mapped command. Without this flag, only print the JSON plan.",
    )
    workday_intent.add_argument("--watcher", help="Path or command for win-uia-watcher.")
    workday_intent.add_argument(
        "--watcher-arg",
        action="append",
        default=[],
        help="Extra argument passed to the watcher command before watch.",
    )
    workday_intent.add_argument("--helper", help="Path or command for win-uia-helper.")
    workday_intent.add_argument(
        "--helper-arg",
        action="append",
        default=[],
        help="Extra argument passed to the helper command before capture-frontmost.",
    )
    workday_intent.add_argument("--depth", type=int, default=80)
    workday_intent.add_argument("--duration", type=int, default=DEFAULT_DURATION_SECONDS)
    workday_intent.add_argument("--debounce-ms", type=int, default=750)
    workday_intent.add_argument("--heartbeat-ms", type=int, default=5000)
    workday_intent.add_argument("--checkpoint-seconds", type=int, default=DEFAULT_CHECKPOINT_SECONDS)
    workday_intent.add_argument("--capture-on-start", action="store_true", default=True)
    workday_intent.add_argument("--session-id")
    workday_intent.add_argument("--wait-seconds", type=int, default=30)
    workday_intent.add_argument(
        "--exclude-app",
        action="append",
        default=[],
        help="Skip exact app names in a started workday session.",
    )
    workday_intent.add_argument(
        "--focus",
        action="append",
        default=[],
        help="Optional user-stated focus note for the resulting human workday summary.",
    )

    workday_run = workday_subparsers.add_parser("run", help=argparse.SUPPRESS)
    workday_subparsers._choices_actions = [  # type: ignore[attr-defined]
        action for action in workday_subparsers._choices_actions if action.dest != "run"
    ]
    workday_run.add_argument("--session-id", required=True)
    workday_run.add_argument("--stop-file", required=True, type=Path)
    workday_run.add_argument("--result-file", required=True, type=Path)
    workday_run.add_argument("--checkpoint-file", type=Path)
    workday_run.add_argument("--watcher-arg", action="append", default=[])
    workday_run.add_argument("--helper-arg", action="append", default=[])
    workday_run.add_argument("--duration", type=int, required=True)
    workday_run.add_argument("--depth", type=int, default=80)
    workday_run.add_argument("--debounce-ms", type=int, default=750)
    workday_run.add_argument("--heartbeat-ms", type=int, default=5000)
    workday_run.add_argument("--checkpoint-seconds", type=int, default=DEFAULT_CHECKPOINT_SECONDS)
    workday_run.add_argument("--capture-on-start", action="store_true")
    workday_run.add_argument("--exclude-app", action="append", default=[])
    workday_run.add_argument("--focus", action="append", default=[])

    codex = subparsers.add_parser(
        "codex",
        help="Print Codex integration helpers without modifying user config.",
    )
    codex_subparsers = codex.add_subparsers(dest="codex_command", required=True)
    codex_setup = codex_subparsers.add_parser(
        "setup",
        help="Print a combined Codex readiness report without writing files.",
    )
    codex_setup.add_argument(
        "--dry-run",
        action="store_true",
        help="Print local readiness, MCP config, and plugin guidance without writing files.",
    )
    codex_setup.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Print JSON by default, or a compact user-facing readiness guide.",
    )
    codex_install = codex_subparsers.add_parser(
        "install",
        help="Print a read-only Codex MCP config snippet.",
    )
    codex_install.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the suggested config.toml snippet without writing files.",
    )
    codex_plugin = codex_subparsers.add_parser(
        "plugin",
        help="Print local Codex Workday plugin source guidance without writing files.",
    )
    codex_plugin.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the local plugin source path and safety boundary without writing files.",
    )
    codex_plugin.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Print JSON by default, or a compact user-facing plugin guide.",
    )
    codex_daily = codex_subparsers.add_parser(
        "daily",
        help="Print daily workday setup and record-only prompt without writing files.",
    )
    codex_daily.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the daily Workday plugin workflow without writing files.",
    )
    codex_daily.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Print JSON by default, or a compact user-facing text guide.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "init":
        paths = ensure_state()
        init_db(paths["db"])
        print(str(paths["home"]))
        return 0

    if args.command == "status":
        paths = ensure_state()
        init_db(paths["db"])
        payload = {
            "home": str(paths["home"]),
            "capture_buffer": str(paths["capture_buffer"]),
            "db_exists": paths["db"].exists(),
            "capture_count": capture_count(paths["home"]),
            "memory_entry_count": memory_entry_count(paths["home"]),
            "session_count": session_count(paths["home"]),
            **privacy_contract_payload(),
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if args.command == "doctor":
        payload = _doctor_payload()
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if args.command == "capture-once":
        result = capture_once_from_fixture(args.fixture)
        if result.skipped:
            print(f"SKIPPED: {result.reason}")
            return 0
        print(str(result.path))
        return 0

    if args.command == "capture-frontmost":
        _reject_forbidden_passthrough(parser, args.helper_arg, "--helper-arg")
        if not 0 <= args.depth <= 80:
            parser.error("--depth must be between 0 and 80")
        try:
            result = capture_frontmost_with_helper(
                [args.helper, *args.helper_arg],
                depth=args.depth,
            )
        except RuntimeError as exc:
            print(f"ERROR: {exc}")
            return 1
        except Exception:
            print("ERROR: helper output could not be captured safely")
            return 1
        if result.skipped:
            print(f"SKIPPED: {result.reason}")
            return 0
        print(str(result.path))
        return 0

    if args.command == "privacy-check":
        result = privacy_check_path(args.path)
        for message in result.messages:
            print(message)
        return 0 if result.ok else 1

    if args.command == "search-captures":
        paths = state_paths()
        results = search_captures(args.query, paths["home"])
        print(json.dumps(results, indent=2, sort_keys=True))
        return 0

    if args.command == "generate-memory":
        paths = ensure_state()
        results = generate_memory_entries(paths["home"], date=args.date)
        print(json.dumps([result.to_json() for result in results], indent=2, sort_keys=True))
        return 0

    if args.command == "search-memory":
        paths = state_paths()
        results = search_memory_entries(args.query, paths["home"])
        print(json.dumps(results, indent=2, sort_keys=True))
        return 0

    if args.command == "watch":
        if args.events:
            paths = ensure_state()
            try:
                result = dispatch_watcher_events(args.events, paths["home"])
            except ValueError as exc:
                print(f"ERROR: {exc}")
                return 1
            except Exception:
                print("ERROR: watcher output could not be captured safely")
                return 1
        else:
            _reject_forbidden_passthrough(parser, args.watcher_arg, "--watcher-arg")
            _reject_forbidden_passthrough(parser, args.helper_arg, "--helper-arg")
            if not 0 <= args.depth <= 80:
                parser.error("--depth must be between 0 and 80")
            if args.duration < 0:
                parser.error("--duration must be non-negative")
            paths = ensure_state()
            helper_command = [args.helper, *args.helper_arg] if args.helper else None
            try:
                result = run_watcher_command(
                    [args.watcher, *args.watcher_arg],
                    helper_command,
                    depth=args.depth,
                    duration_seconds=args.duration,
                    debounce_ms=args.debounce_ms,
                    heartbeat_ms=args.heartbeat_ms,
                    capture_on_start=args.capture_on_start,
                    home=paths["home"],
                )
            except RuntimeError as exc:
                print(f"ERROR: {exc}")
                return 1
            except Exception:
                print("ERROR: watcher output could not be captured safely")
                return 1
        print(json.dumps(result.to_json(), indent=2, sort_keys=True))
        return 0

    if args.command == "monitor":
        if args.events:
            paths = ensure_state()
            try:
                result = monitor_events(
                    args.events,
                    paths["home"],
                    session_id=args.session_id,
                    exclude_apps=args.exclude_app,
                )
            except ValueError as exc:
                print(f"ERROR: {exc}")
                return 1
            except Exception:
                print("ERROR: monitor output could not be captured safely")
                return 1
        else:
            _reject_forbidden_passthrough(parser, args.watcher_arg, "--watcher-arg")
            _reject_forbidden_passthrough(parser, args.helper_arg, "--helper-arg")
            if not 0 <= args.depth <= 80:
                parser.error("--depth must be between 0 and 80")
            if args.duration < 0:
                parser.error("--duration must be non-negative")
            paths = ensure_state()
            helper_command = [args.helper, *args.helper_arg] if args.helper else None
            try:
                result = run_monitor_watcher_command(
                    [args.watcher, *args.watcher_arg],
                    helper_command,
                    depth=args.depth,
                    duration_seconds=args.duration,
                    debounce_ms=args.debounce_ms,
                    heartbeat_ms=args.heartbeat_ms,
                    capture_on_start=args.capture_on_start,
                    home=paths["home"],
                    session_id=args.session_id,
                    exclude_apps=args.exclude_app,
                )
            except RuntimeError as exc:
                print(f"ERROR: {exc}")
                return 1
            except Exception:
                print("ERROR: monitor output could not be captured safely")
                return 1
        print(json.dumps(result.to_json(), indent=2, sort_keys=True))
        return 0

    if args.command == "summarize-session":
        paths = state_paths()
        try:
            result = read_session(args.session, paths["home"])
        except Exception:
            print("ERROR: session summary could not be read safely")
            return 1
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0

    if args.command == "mcp-stdio":
        paths = state_paths()
        return run_stdio(home=paths["home"])

    if args.command == "projects":
        return _handle_projects(args)

    if args.command == "workday":
        return _handle_workday(parser, args)

    if args.command == "codex":
        if args.codex_command == "setup":
            if not args.dry_run:
                parser.error("codex setup currently supports only --dry-run")
            payload = _codex_setup_dry_run_payload()
            if args.format == "text":
                print(_format_codex_setup_dry_run_text(payload), end="")
            else:
                print(
                    json.dumps(
                        payload,
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    )
                )
            return 0
        if args.codex_command == "install":
            if not args.dry_run:
                parser.error("codex install currently supports only --dry-run")
            print(_codex_mcp_config_snippet(), end="")
            return 0
        if args.codex_command == "plugin":
            if not args.dry_run:
                parser.error("codex plugin currently supports only --dry-run")
            payload = _codex_plugin_dry_run_payload()
            if args.format == "text":
                print(_format_codex_plugin_dry_run_text(payload), end="")
                return 0
            print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
            return 0
        if args.codex_command == "daily":
            if not args.dry_run:
                parser.error("codex daily currently supports only --dry-run")
            payload = _codex_daily_dry_run_payload()
            if args.format == "text":
                print(_format_codex_daily_dry_run_text(payload), end="")
            else:
                print(
                    json.dumps(
                        payload,
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    )
                )
            return 0

    parser.error(f"unknown command: {args.command}")
    return 2


def _handle_projects(args: argparse.Namespace) -> int:
    if args.projects_command == "add":
        payload = add_project(args.path, name=args.name)
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.projects_command == "list":
        payload = load_project_registry()
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.projects_command == "remove":
        payload = remove_project(args.identifier)
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.projects_command == "snapshot":
        payload = snapshot_projects()
        print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    return 2


def _codex_mcp_config_snippet() -> str:
    if set(CODEX_MCP_ENABLED_TOOLS) != set(TOOL_NAMES):
        raise RuntimeError("Codex enabled tool list drifted from MCP tool contract")

    tool_lines = "\n".join(f'  "{tool}",' for tool in CODEX_MCP_ENABLED_TOOLS)
    return (
        "[mcp_servers.winchronicle]\n"
        'command = "winchronicle"\n'
        'args = ["mcp-stdio"]\n'
        "startup_timeout_sec = 20\n"
        "tool_timeout_sec = 30\n"
        "enabled = true\n"
        "enabled_tools = [\n"
        f"{tool_lines}\n"
        "]\n"
    )


def _codex_setup_dry_run_payload() -> dict[str, object]:
    privacy = privacy_contract_payload()
    disabled_ok = all(privacy[key] is False for key in DISABLED_SURFACE_STATUS)
    plugin = _codex_plugin_dry_run_payload()

    checks: list[dict[str, object]] = [
        {
            "name": "python",
            "ok": sys.version_info >= (3, 11),
            "detail": platform.python_version(),
        },
        _dotnet_check(),
        {
            "name": "privacy_surfaces",
            "ok": disabled_ok,
            "detail": "disabled surfaces remain off",
        },
        {
            "name": "mcp_tool_allowlist",
            "ok": set(CODEX_MCP_ENABLED_TOOLS) == set(TOOL_NAMES),
            "detail": CODEX_MCP_ENABLED_TOOLS,
        },
        {
            "name": "workday_plugin",
            "ok": bool(plugin["plugin_available"]),
            "detail": plugin["plugin_path"],
        },
    ]

    return {
        "command": "codex setup",
        "dry_run": True,
        "version": __version__,
        "writes_config": False,
        "writes_state": False,
        "starts_capture": False,
        "observed_content_trust": TRUST,
        "checks": checks,
        "mcp": {
            "config_toml": _codex_mcp_config_snippet(),
            "enabled_tools": CODEX_MCP_ENABLED_TOOLS,
            "writes_config": False,
        },
        "plugin": plugin,
        "disabled_surfaces": _codex_plugin_disabled_surface_names(),
        "next_commands": [
            "winchronicle codex install --dry-run",
            "winchronicle codex plugin --dry-run --format text",
            "winchronicle workday status --format text --language zh-CN",
        ],
        "chat_output_warning": (
            "Only paste local setup output into chat when the user explicitly asks "
            "to share local paths or session metadata."
        ),
    }


def _format_codex_setup_dry_run_text(payload: dict[str, object]) -> str:
    plugin = payload["plugin"]
    if not isinstance(plugin, dict):
        plugin = {}

    lines = [
        "WinChronicle Codex setup dry-run",
        "",
        "Fast path for Codex App:",
        f"1. Add local plugin source: {plugin.get('codex_app_plugin_source_path', '')}",
        "2. In a Codex App thread, say:",
        "   - 开始记录工作",
        "   - 查看工作记录状态",
        "   - 停止工作并总结",
        "3. Keep summaries local unless you explicitly ask Codex to paste them into chat.",
        "",
        "Safety boundary:",
        f"- dry run only: {_yes_no(payload['dry_run'])}",
        f"- writes Codex config: {_yes_no(payload['writes_config'])}",
        f"- writes WinChronicle state: {_yes_no(payload['writes_state'])}",
        f"- starts capture now: {_yes_no(payload['starts_capture'])}",
        f"- Observed content trust: {payload['observed_content_trust']}",
        "- no screenshots, OCR, clipboard, desktop control, or MCP write tools",
        "",
        "For diagnostics: winchronicle doctor",
        "For JSON setup details: winchronicle codex setup --dry-run",
        "For plugin-only path: winchronicle codex plugin --dry-run --format text",
    ]
    return "\n".join(lines) + "\n"


def _format_codex_check_line(check: object) -> str:
    if not isinstance(check, dict):
        return "- unknown: no"
    name = check.get("name", "unknown")
    status = "ok" if check.get("ok") is True else "not ok"
    detail = check.get("detail")
    if detail in (None, "", []):
        return f"- {name}: {status}"
    return f"- {name}: {status} ({detail})"


def _codex_daily_dry_run_payload() -> dict[str, object]:
    return {
        "command": "codex daily",
        "dry_run": True,
        "version": __version__,
        "writes_config": False,
        "writes_state": False,
        "starts_capture": False,
        "adds_mcp_tools": False,
        "observed_content_trust": TRUST,
        "setup_commands": [
            "winchronicle codex setup --dry-run",
            "winchronicle codex plugin --dry-run --format text",
        ],
        "plugin": _codex_plugin_dry_run_payload(),
        "daily_phrases": CODEX_WORKDAY_ACCEPTED_PHRASES,
        "what_to_say_next": CODEX_WORKDAY_NEXT_PROMPTS,
        "first_prompt_to_try": CODEX_WORKDAY_NEXT_PROMPTS[0],
        "after_plugin_setup": (
            "After adding the local plugin source, try these prompts in Codex App."
        ),
        "record_only_thread_prompt": CODEX_RECORD_ONLY_THREAD_PROMPT,
        "recording_mode_boundary": CODEX_RECORDING_MODE_BOUNDARY,
        "chat_output_warning": (
            "Only paste local setup output or work summaries into chat when the "
            "user explicitly asks to share local paths, session metadata, or "
            "summary text."
        ),
    }


def _format_codex_daily_dry_run_text(payload: dict[str, object]) -> str:
    plugin = payload["plugin"]
    if not isinstance(plugin, dict):
        plugin = {}
    what_to_say_next = payload["what_to_say_next"]
    prompts = what_to_say_next if isinstance(what_to_say_next, list) else []
    disabled_surfaces = plugin.get("disabled_surfaces", [])
    disabled_surface_names = disabled_surfaces if isinstance(disabled_surfaces, list) else []

    lines = [
        "WinChronicle Codex daily dry-run",
        "",
        f"Dry run only: {_yes_no(payload['dry_run'])}",
        f"Writes config: {_yes_no(payload['writes_config'])}",
        f"Writes state: {_yes_no(payload['writes_state'])}",
        f"Starts capture: {_yes_no(payload['starts_capture'])}",
        f"Adds MCP tools: {_yes_no(payload['adds_mcp_tools'])}",
        f"Observed content trust: {payload['observed_content_trust']}",
        "",
        f"Add local plugin source: {plugin.get('codex_app_plugin_source_path', '')}",
        f"First prompt to try: {payload['first_prompt_to_try']}",
        "What to say next:",
        *[f"- {prompt}" for prompt in prompts],
        "",
        "Disabled surfaces remain off:",
        *[f"- {surface}" for surface in disabled_surface_names],
        "",
        "Record-only boundary:",
        "Do not inspect, scan, review, edit, test, commit, push, or release repository files.",
        str(payload["recording_mode_boundary"]),
        "",
        "Record-only thread prompt:",
        str(payload["record_only_thread_prompt"]).rstrip(),
        "",
        "No new capture, upload, control, or MCP write surfaces are added.",
    ]
    return "\n".join(lines) + "\n"


def _format_codex_plugin_dry_run_text(payload: dict[str, object]) -> str:
    starter_phrases = payload["starter_phrases"]
    prompts = starter_phrases if isinstance(starter_phrases, list) else []
    disabled_surfaces = payload["disabled_surfaces"]
    disabled_surface_names = disabled_surfaces if isinstance(disabled_surfaces, list) else []

    lines = [
        "WinChronicle Codex plugin dry-run",
        "",
        f"Dry run only: {_yes_no(payload['dry_run'])}",
        f"Writes config: {_yes_no(payload['writes_config'])}",
        f"Adds MCP tools: {_yes_no(payload['adds_mcp_tools'])}",
        f"Observed content trust: {payload['observed_content_trust']}",
        "",
        f"Plugin available: {_yes_no(payload['plugin_available'])}",
        f"Plugin source: {payload['codex_app_plugin_source_path']}",
        str(payload["copyable_plugin_source_instruction"]),
        "",
        "Starter prompts:",
        *[f"- {prompt}" for prompt in prompts],
        "",
        "Post-install self-check:",
        *[
            f"{index}. {step}"
            for index, step in enumerate(
                payload["post_install_self_check"]
                if isinstance(payload.get("post_install_self_check"), list)
                else [],
                start=1,
            )
        ],
        "If Codex starts scanning files instead, paste the record-only prompt from:",
        str(payload["record_only_prompt_command"]),
        "",
        "Disabled surfaces remain off:",
        *[f"- {surface}" for surface in disabled_surface_names],
        "",
        str(payload["install_hint"]),
    ]
    return "\n".join(lines) + "\n"


def _yes_no(value: object) -> str:
    return "yes" if value is True else "no"


def _codex_plugin_dry_run_payload() -> dict[str, object]:
    plugin_path = _codex_workday_plugin_path()
    manifest_path = plugin_path / ".codex-plugin" / "plugin.json"
    skill_path = plugin_path / "skills" / "workday-recorder" / "SKILL.md"
    plugin_available = plugin_path.is_dir() and manifest_path.is_file() and skill_path.is_file()

    return {
        "command": "codex plugin",
        "dry_run": True,
        "writes_config": False,
        "plugin_name": "winchronicle-workday",
        "plugin_available": plugin_available,
        "plugin_path": str(plugin_path),
        "manifest_path": str(manifest_path),
        "skill_path": str(skill_path),
        "codex_app_plugin_source_path": str(plugin_path),
        "copyable_plugin_source_instruction": (
            f"Codex App -> Plugins -> Add local plugin source -> {plugin_path}"
        ),
        "install_hint": (
            "Add this local plugin source path in the Codex app plugin UI or local "
            "plugin source settings; do not paste summaries into chat unless the "
            "user explicitly asks for chat output."
        ),
        "post_install_self_check": CODEX_PLUGIN_POST_INSTALL_SELF_CHECK,
        "record_only_prompt_command": CODEX_RECORD_ONLY_PROMPT_COMMAND,
        "starter_phrases": CODEX_WORKDAY_DEFAULT_PROMPTS,
        "accepted_phrases": CODEX_WORKDAY_ACCEPTED_PHRASES,
        "default_prompts": CODEX_WORKDAY_DEFAULT_PROMPTS,
        "disabled_surfaces": _codex_plugin_disabled_surface_names(),
        "observed_content_trust": TRUST,
        "adds_mcp_tools": False,
        "writes_codex_config": False,
    }


def _codex_workday_plugin_path() -> Path:
    packaged_plugin = Path(__file__).resolve().parent / "codex_plugins" / "winchronicle-workday"
    if packaged_plugin.is_dir():
        return packaged_plugin
    return Path(__file__).resolve().parents[2] / "plugins" / "winchronicle-workday"


def _codex_plugin_disabled_surface_names() -> list[str]:
    names: list[str] = []
    for key in DISABLED_SURFACE_STATUS:
        name = key
        if name in {"keyboard_capture_enabled", "clipboard_capture_enabled"}:
            name = name[: -len("_capture_enabled")]
        elif name.endswith("_enabled"):
            name = name[: -len("_enabled")]
        names.append(name)
    return names


def _doctor_payload() -> dict[str, object]:
    paths = ensure_state()
    checks: list[dict[str, object]] = []

    checks.append(
        {
            "name": "python",
            "ok": sys.version_info >= (3, 11),
            "detail": platform.python_version(),
        }
    )

    try:
        init_db(paths["db"])
        sqlite_ok = paths["db"].exists()
        sqlite_detail = "initialized" if sqlite_ok else "database file missing"
    except Exception:
        sqlite_ok = False
        sqlite_detail = "sqlite initialization failed"
    checks.append({"name": "sqlite", "ok": sqlite_ok, "detail": sqlite_detail})

    checks.append(_dotnet_check())

    root = Path(__file__).resolve().parents[2]
    helper_dll = (
        root
        / "resources"
        / "win-uia-helper"
        / "bin"
        / "Debug"
        / "net8.0-windows"
        / "win-uia-helper.dll"
    )
    watcher_dll = (
        root
        / "resources"
        / "win-uia-watcher"
        / "bin"
        / "Debug"
        / "net8.0-windows"
        / "win-uia-watcher.dll"
    )
    checks.append(
        {
            "name": "uia_helper_dll",
            "ok": helper_dll.exists(),
            "path": str(helper_dll),
        }
    )
    checks.append(
        {
            "name": "uia_watcher_dll",
            "ok": watcher_dll.exists(),
            "path": str(watcher_dll),
        }
    )

    privacy = privacy_contract_payload()
    disabled_ok = all(privacy[key] is False for key in DISABLED_SURFACE_STATUS)
    checks.append(
        {
            "name": "privacy_surfaces",
            "ok": disabled_ok,
            "detail": "disabled surfaces remain off",
        }
    )

    return {
        "command": "doctor",
        "version": __version__,
        "python_version": platform.python_version(),
        "home": str(paths["home"]),
        "capture_buffer": str(paths["capture_buffer"]),
        "db_exists": paths["db"].exists(),
        "checks": checks,
        **privacy,
    }


def _dotnet_check() -> dict[str, object]:
    executable = shutil.which("dotnet")
    if executable is None:
        return {"name": "dotnet", "ok": False, "detail": "dotnet not found"}

    try:
        result = subprocess.run(
            [executable, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except Exception:
        return {"name": "dotnet", "ok": False, "detail": "dotnet --version failed"}

    version = result.stdout.strip().splitlines()[0] if result.stdout.strip() else ""
    return {
        "name": "dotnet",
        "ok": result.returncode == 0,
        "detail": version if result.returncode == 0 and version else "dotnet --version failed",
    }


def _reject_forbidden_passthrough(
    parser: argparse.ArgumentParser,
    values: list[str],
    option_name: str,
) -> None:
    for value in values:
        for forbidden in FORBIDDEN_PASSTHROUGH_FLAGS:
            if value == forbidden or value.startswith(f"{forbidden}="):
                parser.error(
                    f"{option_name} cannot pass disabled WinChronicle surface flag {forbidden}"
                )


def _handle_workday(parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
    if args.workday_command == "start":
        return _execute_workday_start(parser, args)

    if args.workday_command == "status":
        payload = status_workday()
        if args.format == "text":
            print(format_workday_status_text(payload), end="")
            return 0
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if args.workday_command == "doctor":
        payload = doctor_workday(checkpoint_stale_seconds=args.checkpoint_stale_seconds)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if args.workday_command == "stop":
        return _execute_workday_stop(args, output_format=args.format)

    if args.workday_command == "summarize":
        try:
            payload = summarize_workday(
                args.session,
                output_format=args.format,
                language=args.language,
                confirmation_notes=args.confirmation,
                summary_style=args.summary_style,
            )
        except Exception:
            print("ERROR: session summary could not be read safely")
            return 1
        if isinstance(payload, str):
            print(payload, end="")
            return 0
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if args.workday_command == "intent":
        plan = _workday_intent_plan(args.phrase)
        if not plan["matched"]:
            print(json.dumps(plan, indent=2, sort_keys=True, ensure_ascii=False))
            return 1
        if not args.execute:
            print(json.dumps(plan, indent=2, sort_keys=True, ensure_ascii=False))
            return 0
        if plan["intent"] == "start_workday":
            return _execute_workday_start(parser, args)
        if plan["intent"] == "stop_and_summarize_workday":
            return _execute_workday_stop(args, output_format="text")
        print(json.dumps(plan, indent=2, sort_keys=True, ensure_ascii=False))
        return 1

    if args.workday_command == "run":
        _reject_forbidden_passthrough(parser, args.watcher_arg, "--watcher-arg")
        _reject_forbidden_passthrough(parser, args.helper_arg, "--helper-arg")
        if not args.watcher_arg:
            parser.error("workday run requires --watcher-arg")
        if args.duration < 0 or args.duration > MAX_DURATION_SECONDS:
            parser.error(f"--duration must be between 0 and {MAX_DURATION_SECONDS}")
        try:
            payload = run_workday(
                watcher_command=args.watcher_arg,
                helper_command=args.helper_arg or None,
                stop_file=args.stop_file,
                result_file=args.result_file,
                checkpoint_file=args.checkpoint_file,
                session_id=args.session_id,
                duration_seconds=args.duration,
                depth=args.depth,
                debounce_ms=args.debounce_ms,
                heartbeat_ms=args.heartbeat_ms,
                checkpoint_seconds=args.checkpoint_seconds,
                capture_on_start=args.capture_on_start,
                exclude_apps=args.exclude_app,
                operator_focus=args.focus,
            )
        except Exception:
            recovery = recover_workday_runner_failure(
                session_id=args.session_id,
                result_file=args.result_file,
                checkpoint_file=args.checkpoint_file,
                stopped=args.stop_file.exists(),
            )
            if recovery.get("summary_available"):
                print(json.dumps(recovery, indent=2, sort_keys=True))
                return 0
            print("ERROR: workday runner could not write a safe session summary")
            return 1
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    parser.error(f"unknown workday command: {args.workday_command}")
    return 2


def _execute_workday_start(parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
    _reject_forbidden_passthrough(parser, args.watcher_arg, "--watcher-arg")
    _reject_forbidden_passthrough(parser, args.helper_arg, "--helper-arg")
    if not 0 <= args.depth <= 80:
        parser.error("--depth must be between 0 and 80")
    if args.duration < 0 or args.duration > MAX_DURATION_SECONDS:
        parser.error(f"--duration must be between 0 and {MAX_DURATION_SECONDS}")
    watcher_command = [args.watcher, *args.watcher_arg] if args.watcher else default_watcher_command()
    helper_command = [args.helper, *args.helper_arg] if args.helper else None
    if args.helper is None and not args.watcher:
        helper_command = default_helper_command()
    try:
        payload = start_workday(
            watcher_command=watcher_command,
            helper_command=helper_command,
            session_id=args.session_id,
            duration_seconds=args.duration,
            depth=args.depth,
            debounce_ms=args.debounce_ms,
            heartbeat_ms=args.heartbeat_ms,
            checkpoint_seconds=args.checkpoint_seconds,
            capture_on_start=args.capture_on_start,
            exclude_apps=args.exclude_app,
            operator_focus=[*args.focus, *_focus_notes_from_phrase(getattr(args, "phrase", ""))],
        )
    except WorkdayError as exc:
        print(json.dumps({"active": False, "error": str(exc)}, indent=2, sort_keys=True))
        return 1
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if payload.get("error") else 0


def _execute_workday_stop(args: argparse.Namespace, *, output_format: str) -> int:
    payload = stop_workday(wait_seconds=args.wait_seconds)
    if (
        output_format == "text"
        and payload.get("summary_available")
        and isinstance(payload.get("summary"), dict)
    ):
        print(
            format_workday_text_summary(
                payload["summary"],
                confirmation_notes=getattr(args, "confirmation", []),
                summary_style=getattr(args, "summary_style", "human"),
            ),
            end="",
        )
        return 0
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def _workday_intent_plan(phrase: str) -> dict[str, object]:
    normalized = " ".join(str(phrase).split())
    supported_phrases = [*WORKDAY_START_PHRASES, *WORKDAY_STOP_SUMMARY_PHRASES]
    start_matched, focus_notes = _match_start_intent(normalized)
    if start_matched:
        command = ["winchronicle", "workday", "start"]
        for note in focus_notes:
            command.extend(["--focus", note])
        return {
            "matched": True,
            "execute": False,
            "intent": "start_workday",
            "phrase": phrase,
            "command": command,
            "operator_focus": focus_notes,
            "bounded": True,
            "capture_surface": CAPTURE_SURFACE,
            "trust": WORKDAY_INTENT_TRUST,
            "dry_run_by_default": True,
        }
    if normalized in WORKDAY_STOP_SUMMARY_PHRASES:
        return {
            "matched": True,
            "execute": False,
            "intent": "stop_and_summarize_workday",
            "phrase": phrase,
            "command": [
                "winchronicle",
                "workday",
                "stop",
                "--format",
                "text",
                "--language",
                "zh-CN",
            ],
            "bounded": True,
            "capture_surface": CAPTURE_SURFACE,
            "trust": WORKDAY_INTENT_TRUST,
            "dry_run_by_default": True,
        }
    return {
        "matched": False,
        "execute": False,
        "error": "unsupported_workday_intent",
        "phrase": phrase,
        "supported_phrases": supported_phrases,
        "trust": WORKDAY_INTENT_TRUST,
        "dry_run_by_default": True,
    }


def _match_start_intent(normalized: str) -> tuple[bool, list[str]]:
    for start_phrase in WORKDAY_START_PHRASES:
        if normalized == start_phrase:
            return True, []
        for separator in ("：", ":", "，", ",", " "):
            prefix = f"{start_phrase}{separator}"
            if normalized.startswith(prefix):
                note = normalized[len(prefix) :].strip(" ：:,，")
                return True, [note] if note else []
    return False, []


def _focus_notes_from_phrase(phrase: str) -> list[str]:
    matched, notes = _match_start_intent(" ".join(str(phrase).split()))
    return notes if matched else []
