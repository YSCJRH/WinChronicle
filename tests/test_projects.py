import json
import subprocess
from pathlib import Path

import pytest

from winchronicle.cli import main


def test_projects_allowlist_snapshot_reads_metadata_not_file_contents(tmp_path, monkeypatch, capsys):
    if not _git_available():
        pytest.skip("git is not available")
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    repo = tmp_path / "demo-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True, text=True)
    (repo / "notes.txt").write_text(
        "SECRET_CONTENT_SHOULD_NOT_APPEAR ghp_winchroniclecanary1234567890ABCD",
        encoding="utf-8",
    )

    assert main(["projects", "add", str(repo), "--name", "Demo"]) == 0
    added = json.loads(capsys.readouterr().out)
    assert added["trust"] == "local_project_allowlist"
    assert added["projects"][0]["name"] == "Demo"

    assert main(["projects", "list"]) == 0
    listed = json.loads(capsys.readouterr().out)
    assert listed["projects"][0]["path"] == str(repo.resolve())

    assert main(["projects", "snapshot"]) == 0
    snapshot = json.loads(capsys.readouterr().out)
    project = snapshot["projects"][0]
    assert snapshot["trust"] == "local_project_metadata"
    assert snapshot["privacy"]["reads_file_contents"] is False
    assert snapshot["privacy"]["reads_full_diff"] is False
    assert project["is_git_repo"] is True
    assert project["changed_files"] == ["notes.txt"]
    assert project["status_counts"]["untracked"] == 1

    serialized = json.dumps(snapshot, ensure_ascii=False)
    assert "SECRET_CONTENT_SHOULD_NOT_APPEAR" not in serialized
    assert "ghp_winchroniclecanary1234567890ABCD" not in serialized


def _git_available() -> bool:
    try:
        return subprocess.run(
            ["git", "--version"],
            check=False,
            capture_output=True,
            text=True,
        ).returncode == 0
    except FileNotFoundError:
        return False
