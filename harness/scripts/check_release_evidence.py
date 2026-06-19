from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DEFAULT_REPO = "YSCJRH/WinChronicle"
ANY_RELEASE_URL_RE = re.compile(
    r"https://github\.com/(?P<repo>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/releases/tag/[^\s)>|]+"
)
ANY_ACTIONS_RUN_URL_RE = re.compile(
    r"https://github\.com/(?P<repo>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/actions/runs/\d+"
)
WINDOWS_HARNESS_RE = re.compile(r"\bWindows Harness\b", re.IGNORECASE)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check release evidence for publish and post-push URLs."
    )
    parser.add_argument(
        "--repo",
        default=DEFAULT_REPO,
        help=f"Expected GitHub owner/repository. Defaults to {DEFAULT_REPO}.",
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
        failures.extend(_validate_path(path, repo=args.repo))

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    checked = ", ".join(str(path) for path in args.evidence)
    print(
        "PASS: release evidence has expected-repo GitHub release URL "
        f"and Windows Harness Actions run URL: {checked}"
    )
    return 0


def _validate_path(path: Path, repo: str) -> list[str]:
    if not path.is_file():
        return [f"{path}: missing file"]

    text = path.read_text(encoding="utf-8")
    release_url_re, actions_run_url_re = _repo_patterns(repo)
    failures: list[str] = []

    failures.extend(_unexpected_repo_failures(path, text, ANY_RELEASE_URL_RE, repo, "release"))
    failures.extend(
        _unexpected_repo_failures(path, text, ANY_ACTIONS_RUN_URL_RE, repo, "Actions run")
    )

    if not release_url_re.search(text):
        failures.append(f"{path}: missing GitHub release URL for {repo}")

    has_expected_actions_url = bool(actions_run_url_re.search(text))
    has_windows_harness_label = bool(WINDOWS_HARNESS_RE.search(text))
    has_bound_windows_harness_run = any(
        WINDOWS_HARNESS_RE.search(line) and actions_run_url_re.search(line)
        for line in text.splitlines()
    )

    if not has_expected_actions_url:
        failures.append(f"{path}: missing GitHub Actions run URL for {repo}")
    if not has_windows_harness_label:
        failures.append(f"{path}: missing Windows Harness label")
    elif not has_bound_windows_harness_run:
        failures.append(
            f"{path}: missing Windows Harness GitHub Actions run URL for {repo}"
        )

    return failures


def _unexpected_repo_failures(
    path: Path,
    text: str,
    pattern: re.Pattern[str],
    expected_repo: str,
    url_kind: str,
) -> list[str]:
    failures: list[str] = []
    for match in pattern.finditer(text):
        actual_repo = match.group("repo")
        if actual_repo != expected_repo:
            failures.append(f"{path}: unexpected GitHub {url_kind} URL repo {actual_repo}")
    return failures


def _repo_patterns(repo: str) -> tuple[re.Pattern[str], re.Pattern[str]]:
    escaped_repo = re.escape(repo.strip("/"))
    return (
        re.compile(rf"https://github\.com/{escaped_repo}/releases/tag/[^\s)>|]+"),
        re.compile(rf"https://github\.com/{escaped_repo}/actions/runs/\d+"),
    )


if __name__ == "__main__":
    sys.exit(main())
