from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path


PACKAGE_RELEASE_RE = re.compile(
    r"\|\s*Latest package/tag release\s*\|\s*`v(?P<version>[^`]+)`"
)
MANUAL_SMOKE_SOURCE_RE = re.compile(
    r"\|\s*Latest full manual UIA smoke source\s*\|\s*\[v(?P<version>[^\]]+?) release record\]"
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check that release docs separate package release identity from manual smoke evidence."
    )
    parser.add_argument("--project", type=Path, required=True, help="pyproject.toml path.")
    parser.add_argument("--ledger", type=Path, required=True, help="Manual smoke evidence ledger.")
    parser.add_argument("--guide", type=Path, required=True, help="Release evidence guide.")
    parser.add_argument("--checklist", type=Path, required=True, help="Release checklist.")
    args = parser.parse_args(argv)

    failures = _validate(args.project, args.ledger, args.guide, args.checklist)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("PASS: package/tag release and manual UIA smoke source are explicitly separated")
    return 0


def _validate(project: Path, ledger: Path, guide: Path, checklist: Path) -> list[str]:
    failures: list[str] = []
    version = _project_version(project, failures)
    ledger_text = _read_text(ledger, failures)
    guide_text = _read_text(guide, failures)
    checklist_text = _read_text(checklist, failures)

    if not version or ledger_text is None or guide_text is None or checklist_text is None:
        return failures

    package_match = PACKAGE_RELEASE_RE.search(ledger_text)
    if not package_match:
        failures.append(f"{ledger}: missing Latest package/tag release row")
        package_version = None
    else:
        package_version = package_match.group("version")
        if package_version != version:
            failures.append(
                f"{ledger}: Latest package/tag release must be `v{version}`, found `v{package_version}`"
            )

    smoke_match = MANUAL_SMOKE_SOURCE_RE.search(ledger_text)
    if not smoke_match:
        failures.append(f"{ledger}: missing Latest full manual UIA smoke source row")
        return failures

    smoke_version = smoke_match.group("version")
    if smoke_version == version:
        return failures

    package_phrase = f"latest package/tag release is `v{version}`"
    smoke_phrase = f"latest full manual UIA smoke source remains [v{smoke_version} release record]"
    stale_claim = f"`v{smoke_version}` is the latest published release"

    for path, text in ((guide, guide_text), (checklist, checklist_text)):
        if package_phrase not in text:
            failures.append(f"{path}: missing phrase: {package_phrase}")
        if smoke_phrase not in text:
            failures.append(f"{path}: missing phrase: {smoke_phrase}")
        if stale_claim in text:
            failures.append(f"{path}: stale package-release claim remains: {stale_claim}")

    ledger_phrase = f"`v{version}` does not refresh manual UIA smoke"
    if ledger_phrase not in ledger_text:
        failures.append(f"{ledger}: missing phrase: {ledger_phrase}")

    return failures


def _project_version(path: Path, failures: list[str]) -> str | None:
    if not path.is_file():
        failures.append(f"{path}: missing file")
        return None
    with path.open("rb") as handle:
        data = tomllib.load(handle)
    version = data.get("project", {}).get("version")
    if not isinstance(version, str) or not version:
        failures.append(f"{path}: missing [project].version")
        return None
    return version


def _read_text(path: Path, failures: list[str]) -> str | None:
    if not path.is_file():
        failures.append(f"{path}: missing file")
        return None
    return path.read_text(encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
