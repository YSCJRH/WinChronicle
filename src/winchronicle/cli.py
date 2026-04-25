from __future__ import annotations

import argparse
import json
from pathlib import Path

from .capture import capture_once_from_fixture, privacy_check_path
from .paths import ensure_state, state_paths
from .storage import capture_count, init_db, search_captures


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="winchronicle")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialize the local WinChronicle state directory.")
    subparsers.add_parser("status", help="Print local state and privacy feature status as JSON.")

    capture = subparsers.add_parser("capture-once", help="Capture a deterministic fixture once.")
    capture.add_argument("--fixture", required=True, type=Path)

    privacy = subparsers.add_parser("privacy-check", help="Dry-run redaction and privacy gates.")
    privacy.add_argument("path", type=Path)

    search = subparsers.add_parser("search-captures", help="Search locally indexed captures.")
    search.add_argument("query")

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
            "screenshots_enabled": False,
            "ocr_enabled": False,
            "audio_enabled": False,
            "keyboard_capture_enabled": False,
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

    parser.error(f"unknown command: {args.command}")
    return 2
