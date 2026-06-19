from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


RELEASE_URL_RE = re.compile(
    r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/releases/tag/[^\s)>]+"
)
ACTIONS_RUN_URL_RE = re.compile(
    r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/actions/runs/\d+"
)
WINDOWS_HARNESS_RE = re.compile(r"\bWindows Harness\b", re.IGNORECASE)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check release evidence for publish and post-push URLs."
    )
    parser.add_argument(
        "evidence",
        nargs="+",
        type=Path,
        help="Release notes or release evidence Markdown file to check.",
    )
    args = parser.parse_args(argv)

    failures: list[str] = []
    for path in args.evidence:
        failures.extend(_validate_path(path))

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    checked = ", ".join(str(path) for path in args.evidence)
    print(f"PASS: release evidence has GitHub release URL and Windows Harness Actions run URL: {checked}")
    return 0


def _validate_path(path: Path) -> list[str]:
    if not path.is_file():
        return [f"{path}: missing file"]

    text = path.read_text(encoding="utf-8")
    failures: list[str] = []
    if not RELEASE_URL_RE.search(text):
        failures.append(f"{path}: missing GitHub release URL")
    if not ACTIONS_RUN_URL_RE.search(text):
        failures.append(f"{path}: missing GitHub Actions run URL")
    if not WINDOWS_HARNESS_RE.search(text):
        failures.append(f"{path}: missing Windows Harness label")
    return failures


if __name__ == "__main__":
    sys.exit(main())
