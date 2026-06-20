from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path


DEFAULT_REPO = "YSCJRH/WinChronicle"
CURRENT_RELEASE_HEADING = "## Current Package Release Evidence"
NEXT_RELEASE_PREFLIGHT_HEADING = "## Next Package Release Preflight"
TAG_RE = re.compile(r"\bv\d+\.\d+\.\d+(?:[-.][A-Za-z0-9.]+)?\b")
SHA_RE = re.compile(r"\b[0-9a-f]{40}\b", re.IGNORECASE)
HEAD_SHA_RE = re.compile(r"\bhead(?:\s+SHA)?\s+`?([0-9a-f]{40})`?", re.IGNORECASE)
PUBLISHED_RE = re.compile(r"\bpublished\b", re.IGNORECASE)
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
        "--project",
        type=Path,
        help="pyproject.toml used by strict release evidence checks.",
    )
    parser.add_argument(
        "--require-current-release",
        action="store_true",
        help=(
            "Require a Current Package Release Evidence section binding project.version "
            "to release URL, tag SHA, Windows Harness URL, and run head SHA."
        ),
    )
    parser.add_argument(
        "--require-release-state",
        action="store_true",
        help=(
            "Require published-release evidence, and require a next-release preflight "
            "section only when project.version is ahead of the published release."
        ),
    )
    parser.add_argument(
        "evidence",
        nargs="+",
        type=Path,
        help="Release notes or release evidence Markdown file to check.",
    )
    args = parser.parse_args(argv)

    failures: list[str] = []
    current_version = None
    if args.require_current_release or args.require_release_state:
        if args.project is None:
            parser.error(
                "--project is required with --require-current-release or --require-release-state"
            )
        try:
            current_version = _read_project_version(args.project)
        except ValueError as exc:
            failures.append(str(exc))

    for path in args.evidence:
        failures.extend(
            _validate_path(
                path,
                repo=args.repo,
                current_version=current_version if args.require_current_release else None,
                release_state_version=current_version if args.require_release_state else None,
            )
        )

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


def _validate_path(
    path: Path,
    repo: str,
    current_version: str | None = None,
    release_state_version: str | None = None,
) -> list[str]:
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

    if current_version is not None:
        failures.extend(
            _current_release_failures(
                path,
                text,
                repo=repo,
                version=current_version,
                actions_run_url_re=actions_run_url_re,
            )
        )

    if release_state_version is not None:
        failures.extend(
            _release_state_failures(
                path,
                text,
                repo=repo,
                project_version=release_state_version,
                actions_run_url_re=actions_run_url_re,
            )
        )

    return failures


def _release_state_failures(
    path: Path,
    text: str,
    *,
    repo: str,
    project_version: str,
    actions_run_url_re: re.Pattern[str],
) -> list[str]:
    failures: list[str] = []
    section = _markdown_section(text, CURRENT_RELEASE_HEADING)
    if section is None:
        return [f"{path}: missing {CURRENT_RELEASE_HEADING} section"]

    published_tag = _release_tag(section)
    if published_tag is None:
        failures.append(f"{path}: missing current release tag")
    else:
        published_version = published_tag.removeprefix("v")
        failures.extend(
            _current_release_failures(
                path,
                text,
                repo=repo,
                version=published_version,
                actions_run_url_re=actions_run_url_re,
            )
        )
        if published_version != project_version:
            failures.extend(
                _next_release_preflight_failures(
                    path,
                    text,
                    repo=repo,
                    version=project_version,
                )
            )
        elif _markdown_section(text, NEXT_RELEASE_PREFLIGHT_HEADING) is not None:
            failures.append(
                f"{path}: unexpected next release preflight section when project version already matches `{published_tag}`"
            )

    return failures


def _current_release_failures(
    path: Path,
    text: str,
    *,
    repo: str,
    version: str,
    actions_run_url_re: re.Pattern[str],
) -> list[str]:
    failures: list[str] = []
    section = _markdown_section(text, CURRENT_RELEASE_HEADING)
    if section is None:
        return [f"{path}: missing {CURRENT_RELEASE_HEADING} section"]

    tag = f"v{version}"
    release_url = f"https://github.com/{repo}/releases/tag/{tag}"
    if f"`{tag}`" not in section:
        failures.append(f"{path}: missing current release tag `{tag}`")
    if release_url not in section:
        failures.append(f"{path}: missing current release URL {release_url}")

    tag_line = _first_matching_line(section, "Tag target SHA")
    tag_sha = _first_sha(tag_line or "")
    if tag_sha is None:
        failures.append(f"{path}: missing current release tag target SHA")

    status_line = _first_matching_line(section, "Publication status")
    if status_line is None:
        failures.append(f"{path}: missing current release publication status")
    elif not _has_publication_status(status_line):
        failures.append(
            f"{path}: current release status must say published, not a draft, and not a prerelease"
        )

    harness_line = next(
        (
            line
            for line in section.splitlines()
            if WINDOWS_HARNESS_RE.search(line) and actions_run_url_re.search(line)
        ),
        None,
    )
    if harness_line is None:
        failures.append(f"{path}: missing current Windows Harness Actions run URL for {repo}")
    else:
        harness_sha = _explicit_head_sha(harness_line)
        if harness_sha is None:
            failures.append(f"{path}: missing current Windows Harness head SHA")
        elif tag_sha is not None and harness_sha.lower() != tag_sha.lower():
            failures.append(f"{path}: Windows Harness head SHA does not match tag target SHA")

    roadmap_line = _first_matching_line(section, "Current roadmap")
    if roadmap_line is None or not _table_value(roadmap_line):
        failures.append(f"{path}: missing current roadmap")

    return failures


def _next_release_preflight_failures(
    path: Path,
    text: str,
    *,
    repo: str,
    version: str,
) -> list[str]:
    failures: list[str] = []
    section = _markdown_section(text, NEXT_RELEASE_PREFLIGHT_HEADING)
    tag = f"v{version}"
    if section is None:
        return [
            f"{path}: missing {NEXT_RELEASE_PREFLIGHT_HEADING} section for project version `{tag}`"
        ]

    release_value = _table_row_value(section, "Release")
    if release_value is None or f"`{tag}`" not in release_value:
        failures.append(f"{path}: missing next release preflight tag `{tag}`")

    expected_release_url = f"https://github.com/{repo}/releases/tag/{tag}"
    expected_url_value = _table_row_value(section, "Expected release URL")
    if expected_url_value is None or expected_release_url not in expected_url_value:
        failures.append(f"{path}: missing expected next release URL {expected_release_url}")

    status_value = _table_row_value(section, "Publication status")
    if status_value is None:
        failures.append(f"{path}: missing next release preflight publication status")
    elif "not published" not in status_value.lower():
        failures.append(f"{path}: next release preflight must say not published")

    gate_value = _table_row_value(section, "Required deterministic gate")
    if gate_value is None or "harness/scripts/run_harness.py" not in gate_value:
        failures.append(f"{path}: missing next release deterministic harness gate")

    reconciliation_value = _table_row_value(section, "Post-publication reconciliation")
    lowered_reconciliation_line = (reconciliation_value or "").lower()
    if (
        reconciliation_value is None
        or "current package release evidence" not in lowered_reconciliation_line
        or "tag target sha" not in lowered_reconciliation_line
        or "windows harness head sha" not in lowered_reconciliation_line
    ):
        failures.append(f"{path}: missing next release post-publication reconciliation plan")

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


def _read_project_version(path: Path) -> str:
    if not path.is_file():
        raise ValueError(f"{path}: missing project file")
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    version = data.get("project", {}).get("version")
    if not isinstance(version, str) or not version:
        raise ValueError(f"{path}: missing [project].version")
    return version


def _markdown_section(text: str, heading: str) -> str | None:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index
            break
    if start is None:
        return None

    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.startswith("## ") and line.strip() != heading:
            end = index
            break
    return "\n".join(lines[start:end])


def _first_matching_line(text: str, pattern: str) -> str | None:
    lowered_pattern = pattern.lower()
    return next(
        (line for line in text.splitlines() if lowered_pattern in line.lower()),
        None,
    )


def _first_sha(text: str) -> str | None:
    match = SHA_RE.search(text)
    return match.group(0) if match else None


def _release_tag(text: str) -> str | None:
    release_value = _table_row_value(text, "Release")
    if release_value is None:
        return None
    match = TAG_RE.search(release_value)
    return match.group(0) if match else None


def _explicit_head_sha(text: str) -> str | None:
    match = HEAD_SHA_RE.search(text)
    return match.group(1) if match else None


def _has_publication_status(line: str) -> bool:
    lowered = line.lower()
    return bool(PUBLISHED_RE.search(line)) and "not a draft" in lowered and "not a prerelease" in lowered


def _table_value(line: str) -> str:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return cells[1] if len(cells) > 1 else ""


def _table_row_value(text: str, field: str) -> str | None:
    expected = field.lower()
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[0].lower() == expected:
            return cells[1]
    return None


def _repo_patterns(repo: str) -> tuple[re.Pattern[str], re.Pattern[str]]:
    escaped_repo = re.escape(repo.strip("/"))
    return (
        re.compile(rf"https://github\.com/{escaped_repo}/releases/tag/[^\s)>|]+"),
        re.compile(rf"https://github\.com/{escaped_repo}/actions/runs/\d+"),
    )


if __name__ == "__main__":
    sys.exit(main())
