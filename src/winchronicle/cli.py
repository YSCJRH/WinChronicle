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
from .privacy import DISABLED_SURFACE_STATUS, privacy_contract_payload
from .session import monitor_events, read_session, run_monitor_watcher_command, session_count
from .storage import capture_count, init_db, memory_entry_count, search_captures, search_memory_entries
from .workday import (
    DEFAULT_CHECKPOINT_SECONDS,
    DEFAULT_DURATION_SECONDS,
    MAX_DURATION_SECONDS,
    WorkdayError,
    default_helper_command,
    default_watcher_command,
    doctor_workday,
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

    workday = subparsers.add_parser(
        "workday",
        help="Manage an explicit finite local workday recording session.",
    )
    workday_subparsers = workday.add_subparsers(
        dest="workday_command",
        required=True,
        metavar="{start,status,doctor,stop,summarize}",
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

    workday_subparsers.add_parser("status", help="Print active workday session state as JSON.")

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

    workday_summarize = workday_subparsers.add_parser(
        "summarize",
        help="Print a saved workday session summary as JSON.",
    )
    workday_summarize.add_argument("session")

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

    codex = subparsers.add_parser(
        "codex",
        help="Print Codex integration helpers without modifying user config.",
    )
    codex_subparsers = codex.add_subparsers(dest="codex_command", required=True)
    codex_install = codex_subparsers.add_parser(
        "install",
        help="Print a read-only Codex MCP config snippet.",
    )
    codex_install.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the suggested config.toml snippet without writing files.",
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

    if args.command == "workday":
        return _handle_workday(parser, args)

    if args.command == "codex":
        if args.codex_command == "install":
            if not args.dry_run:
                parser.error("codex install currently supports only --dry-run")
            print(_codex_mcp_config_snippet(), end="")
            return 0

    parser.error(f"unknown command: {args.command}")
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
            )
        except WorkdayError as exc:
            print(json.dumps({"active": False, "error": str(exc)}, indent=2, sort_keys=True))
            return 1
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 1 if payload.get("error") else 0

    if args.workday_command == "status":
        print(json.dumps(status_workday(), indent=2, sort_keys=True))
        return 0

    if args.workday_command == "doctor":
        payload = doctor_workday(checkpoint_stale_seconds=args.checkpoint_stale_seconds)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if args.workday_command == "stop":
        payload = stop_workday(wait_seconds=args.wait_seconds)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if args.workday_command == "summarize":
        try:
            payload = summarize_workday(args.session)
        except Exception:
            print("ERROR: session summary could not be read safely")
            return 1
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

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
            )
        except Exception:
            print("ERROR: workday runner could not write a safe session summary")
            return 1
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    parser.error(f"unknown workday command: {args.workday_command}")
    return 2
