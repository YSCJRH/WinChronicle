from __future__ import annotations

import argparse
import json
from pathlib import Path

from .capture import capture_frontmost_with_helper, capture_once_from_fixture, privacy_check_path
from .events import dispatch_watcher_events, run_watcher_command
from .memory import generate_memory_entries
from .mcp.server import run_stdio
from .paths import ensure_state, state_paths
from .privacy import privacy_contract_payload
from .storage import capture_count, init_db, memory_entry_count, search_captures, search_memory_entries


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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="winchronicle")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialize the local WinChronicle state directory.")
    subparsers.add_parser("status", help="Print local state and privacy feature status as JSON.")

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

    subparsers.add_parser("mcp-stdio", help="Run the read-only MCP stdio server.")

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
            **privacy_contract_payload(),
        }
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

    if args.command == "mcp-stdio":
        paths = state_paths()
        return run_stdio(home=paths["home"])

    parser.error(f"unknown command: {args.command}")
    return 2


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
