from __future__ import annotations

import json
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

from .paths import ensure_state, state_paths
from .redaction import redact_text, redactions_from_counts


PROJECT_REGISTRY_TRUST = "local_project_allowlist"
PROJECT_METADATA_TRUST = "local_project_metadata"
PROJECT_SCHEMA_VERSION = 1
GIT_TIMEOUT_SECONDS = 5


def load_project_registry(home: Path | str | None = None) -> dict[str, Any]:
    path = state_paths(home)["projects"]
    if not path.exists():
        return _empty_registry()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _empty_registry()
    projects = payload.get("projects")
    if not isinstance(projects, list):
        projects = []
    return {
        "schema_version": PROJECT_SCHEMA_VERSION,
        "trust": PROJECT_REGISTRY_TRUST,
        "projects": [project for project in projects if isinstance(project, dict)],
    }


def save_project_registry(payload: dict[str, Any], home: Path | str | None = None) -> dict[str, Any]:
    paths = ensure_state(home)
    registry = {
        "schema_version": PROJECT_SCHEMA_VERSION,
        "trust": PROJECT_REGISTRY_TRUST,
        "projects": payload.get("projects", []),
    }
    paths["projects"].write_text(
        json.dumps(registry, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return registry


def add_project(
    path: Path | str,
    *,
    name: str | None = None,
    home: Path | str | None = None,
) -> dict[str, Any]:
    registry = load_project_registry(home)
    resolved = str(Path(path).expanduser().resolve())
    display_name = name or Path(resolved).name or resolved
    projects = [
        project
        for project in registry["projects"]
        if str(project.get("path", "")).casefold() != resolved.casefold()
        and str(project.get("name", "")).casefold() != display_name.casefold()
    ]
    projects.append(
        {
            "name": _clip(display_name, 80),
            "path": resolved,
            "added_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        }
    )
    return save_project_registry({"projects": projects}, home)


def remove_project(identifier: str, home: Path | str | None = None) -> dict[str, Any]:
    registry = load_project_registry(home)
    normalized = str(identifier).casefold()
    removed: list[dict[str, Any]] = []
    kept: list[dict[str, Any]] = []
    for project in registry["projects"]:
        name = str(project.get("name", "")).casefold()
        path = str(project.get("path", "")).casefold()
        if normalized in {name, path}:
            removed.append(project)
        else:
            kept.append(project)
    updated = save_project_registry({"projects": kept}, home)
    return {
        **updated,
        "removed": removed,
    }


def snapshot_projects(home: Path | str | None = None) -> dict[str, Any]:
    registry = load_project_registry(home)
    return {
        "schema_version": PROJECT_SCHEMA_VERSION,
        "trust": PROJECT_METADATA_TRUST,
        "privacy": {
            "explicit_allowlist_only": True,
            "metadata_redaction_enabled": True,
            "project_paths_are_display_only": True,
            "reads_file_contents": False,
            "reads_full_diff": False,
            "reads_git_status": True,
            "reads_recent_commit_subjects": True,
        },
        "projects": [_snapshot_project(project) for project in registry["projects"]],
    }


def _snapshot_project(project: dict[str, Any]) -> dict[str, Any]:
    path = Path(str(project.get("path", "")))
    redaction_counts: Counter[str] = Counter()
    result: dict[str, Any] = {
        "name": _redact_metadata_text(project.get("name", path.name), 80, redaction_counts),
        "path": _project_path_display(path, redaction_counts),
        "path_kind": "basename_only",
        "exists": path.exists(),
        "is_git_repo": False,
        "branch": "",
        "changed_files": [],
        "changed_file_count": 0,
        "status_counts": {
            "modified": 0,
            "added": 0,
            "deleted": 0,
            "renamed": 0,
            "untracked": 0,
            "other": 0,
        },
        "diff_stat": {
            "files_changed": 0,
            "insertions": 0,
            "deletions": 0,
            "raw": "",
        },
        "recent_commits": [],
        "errors": [],
        "metadata_redacted": False,
        "redactions": [],
    }
    if not path.exists():
        result["errors"].append("project_path_missing")
        return _finalize_project_metadata(result, redaction_counts)
    if not path.is_dir():
        result["errors"].append("project_path_not_directory")
        return _finalize_project_metadata(result, redaction_counts)

    inside = _git(path, "rev-parse", "--is-inside-work-tree")
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        result["errors"].append("not_a_git_work_tree")
        if inside.stderr:
            result["errors"].append(_redact_metadata_text(inside.stderr, 120, redaction_counts))
        return _finalize_project_metadata(result, redaction_counts)

    result["is_git_repo"] = True
    branch = _git(path, "branch", "--show-current")
    if branch.returncode == 0:
        result["branch"] = _redact_metadata_text(branch.stdout.strip(), 80, redaction_counts)

    status = _git(path, "status", "--porcelain=v1")
    if status.returncode == 0:
        changed_files, status_counts = _parse_status(status.stdout)
        result["changed_files"] = [
            _redact_metadata_text(filename, 160, redaction_counts)
            for filename in changed_files
        ]
        result["changed_file_count"] = len(changed_files)
        result["status_counts"] = status_counts
    elif status.stderr:
        result["errors"].append(_redact_metadata_text(status.stderr, 120, redaction_counts))

    shortstat = _git(path, "diff", "--shortstat")
    if shortstat.returncode == 0:
        result["diff_stat"] = _redact_shortstat(
            _parse_shortstat(shortstat.stdout.strip()),
            redaction_counts,
        )
    elif shortstat.stderr:
        result["errors"].append(_redact_metadata_text(shortstat.stderr, 120, redaction_counts))

    commits = _git(path, "log", "-3", "--pretty=format:%h%x09%s")
    if commits.returncode == 0:
        result["recent_commits"] = _redact_commits(
            _parse_commits(commits.stdout),
            redaction_counts,
        )
    elif commits.stderr and "does not have any commits" not in commits.stderr:
        result["errors"].append(_redact_metadata_text(commits.stderr, 120, redaction_counts))
    return _finalize_project_metadata(result, redaction_counts)


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            text=True,
            capture_output=True,
            timeout=GIT_TIMEOUT_SECONDS,
            check=False,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        return subprocess.CompletedProcess(
            ["git", *args],
            1,
            "",
            exc.__class__.__name__,
        )


def _parse_status(stdout: str) -> tuple[list[str], dict[str, int]]:
    files: list[str] = []
    counts = {
        "modified": 0,
        "added": 0,
        "deleted": 0,
        "renamed": 0,
        "untracked": 0,
        "other": 0,
    }
    for line in stdout.splitlines():
        if len(line) < 4:
            continue
        status = line[:2]
        filename = line[3:]
        if " -> " in filename:
            filename = filename.split(" -> ", 1)[1]
        files.append(_clip(filename.strip('"'), 160))
        if status == "??":
            counts["untracked"] += 1
        elif "R" in status:
            counts["renamed"] += 1
        elif "D" in status:
            counts["deleted"] += 1
        elif "A" in status:
            counts["added"] += 1
        elif "M" in status:
            counts["modified"] += 1
        else:
            counts["other"] += 1
    return files[:50], counts


def _parse_shortstat(raw: str) -> dict[str, Any]:
    result = {"files_changed": 0, "insertions": 0, "deletions": 0, "raw": _clip(raw, 160)}
    parts = [part.strip() for part in raw.split(",") if part.strip()]
    for part in parts:
        tokens = part.split()
        if not tokens:
            continue
        try:
            count = int(tokens[0])
        except ValueError:
            continue
        if "file" in part:
            result["files_changed"] = count
        elif "insertion" in part:
            result["insertions"] = count
        elif "deletion" in part:
            result["deletions"] = count
    return result


def _parse_commits(stdout: str) -> list[dict[str, str]]:
    commits: list[dict[str, str]] = []
    for line in stdout.splitlines():
        if "\t" in line:
            commit_hash, subject = line.split("\t", 1)
        else:
            commit_hash, subject = line[:12], line[12:].strip()
        commits.append(
            {
                "hash": _clip(commit_hash, 16),
                "subject": _clip(subject, 120),
            }
        )
    return commits[:3]


def _redact_shortstat(raw: dict[str, Any], counts: Counter[str]) -> dict[str, Any]:
    return {
        **raw,
        "raw": _redact_metadata_text(raw.get("raw", ""), 160, counts),
    }


def _redact_commits(commits: list[dict[str, str]], counts: Counter[str]) -> list[dict[str, str]]:
    return [
        {
            "hash": _redact_metadata_text(commit.get("hash", ""), 16, counts),
            "subject": _redact_metadata_text(commit.get("subject", ""), 120, counts),
        }
        for commit in commits
    ]


def _project_path_display(path: Path, counts: Counter[str]) -> str:
    return _redact_metadata_text(path.name or "project", 80, counts)


def _redact_metadata_text(value: Any, limit: int, counts: Counter[str]) -> str:
    text = _clip(value, limit)
    redacted, field_counts = redact_text(text)
    counts.update(field_counts)
    return redacted or ""


def _finalize_project_metadata(
    result: dict[str, Any],
    counts: Counter[str],
) -> dict[str, Any]:
    result["metadata_redacted"] = bool(counts)
    result["redactions"] = redactions_from_counts(counts)
    return result


def _empty_registry() -> dict[str, Any]:
    return {
        "schema_version": PROJECT_SCHEMA_VERSION,
        "trust": PROJECT_REGISTRY_TRUST,
        "projects": [],
    }


def _clip(value: Any, limit: int) -> str:
    text = str(value or "").replace("\r", " ").replace("\n", " ").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."
