import json
import subprocess
from pathlib import Path

import pytest

from winchronicle.cli import main
from winchronicle.projects import add_project, load_project_registry


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


def test_projects_snapshot_redacts_secret_like_metadata(tmp_path, monkeypatch, capsys):
    if not _git_available():
        pytest.skip("git is not available")
    home = tmp_path / "state"
    monkeypatch.setenv("WINCHRONICLE_HOME", str(home))
    secret = "ghp_winchroniclecanary1234567890ABCD"
    branch_secret = "winchronicle_plain_canary_token"
    repo = tmp_path / f"customer-{secret}-repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "config", "user.email", "winchronicle@example.invalid"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "WinChronicle Test"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    (repo / "README.md").write_text("safe fixture", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(
        ["git", "commit", "-m", f"Initial {branch_secret}"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        ["git", "checkout", "-b", f"feature/{branch_secret}"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    (repo / "src").mkdir()
    (repo / "src" / f"{secret}.py").write_text("print('safe')", encoding="utf-8")

    assert main(["projects", "add", str(repo), "--name", f"Client {secret}"]) == 0
    capsys.readouterr()

    assert main(["projects", "snapshot"]) == 0
    snapshot = json.loads(capsys.readouterr().out)
    project = snapshot["projects"][0]
    serialized = json.dumps(snapshot, ensure_ascii=False)

    assert snapshot["privacy"]["metadata_redaction_enabled"] is True
    assert snapshot["privacy"]["project_paths_are_display_only"] is True
    assert project["path"] != str(repo.resolve())
    assert project["metadata_redacted"] is True
    assert project["redactions"]
    assert secret not in serialized
    assert branch_secret not in serialized
    assert "[REDACTED:" in serialized


def test_project_registry_preserves_existing_file_when_atomic_replace_fails(
    tmp_path, monkeypatch
):
    home = tmp_path / "state"
    add_project(tmp_path / "alpha", name="Alpha", home=home)
    projects_path = home / "projects.json"
    before_text = projects_path.read_text(encoding="utf-8")
    original_replace = Path.replace

    def fail_project_registry_replace(self: Path, target_path: Path) -> Path:
        if target_path == projects_path:
            raise OSError("simulated project registry replace failure")
        return original_replace(self, target_path)

    monkeypatch.setattr(Path, "replace", fail_project_registry_replace)

    try:
        add_project(tmp_path / "beta", name="Beta", home=home)
    except OSError:
        pass
    else:
        raise AssertionError("expected simulated project registry replace failure")

    assert projects_path.read_text(encoding="utf-8") == before_text
    assert list(home.glob("*.tmp")) == []
    registry = load_project_registry(home)
    assert [project["name"] for project in registry["projects"]] == ["Alpha"]


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
