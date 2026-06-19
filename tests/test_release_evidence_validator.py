import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "harness" / "scripts" / "check_release_evidence.py"


def test_release_evidence_validator_accepts_release_and_actions_urls(tmp_path):
    evidence = tmp_path / "release-notes.md"
    evidence.write_text(
        "\n".join(
            [
                "# v0.2.46",
                "",
                "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.46",
                "Remote Windows Harness: https://github.com/YSCJRH/WinChronicle/actions/runs/27824449915",
            ]
        ),
        encoding="utf-8",
    )

    completed = _run_validator(evidence)

    assert completed.returncode == 0, completed.stdout
    assert "PASS" in completed.stdout


def test_release_evidence_validator_fails_without_release_url(tmp_path):
    evidence = tmp_path / "release-notes.md"
    evidence.write_text(
        "Remote Windows Harness: https://github.com/YSCJRH/WinChronicle/actions/runs/27824449915",
        encoding="utf-8",
    )

    completed = _run_validator(evidence)

    assert completed.returncode == 1
    assert "missing GitHub release URL" in completed.stdout


def test_release_evidence_validator_fails_without_windows_harness_run_url(tmp_path):
    evidence = tmp_path / "release-notes.md"
    evidence.write_text(
        "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.46",
        encoding="utf-8",
    )

    completed = _run_validator(evidence)

    assert completed.returncode == 1
    assert "missing GitHub Actions run URL" in completed.stdout
    assert "missing Windows Harness label" in completed.stdout


def test_v020_release_record_passes_release_evidence_validator():
    completed = _run_validator(ROOT / "docs" / "release-v0.2.0.md")

    assert completed.returncode == 0, completed.stdout


def _run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(path)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
