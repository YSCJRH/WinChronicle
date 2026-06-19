import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "harness" / "scripts" / "check_manual_smoke_freshness.py"


def test_manual_smoke_freshness_validator_accepts_repository_docs():
    completed = _run_validator()

    assert completed.returncode == 0, completed.stdout
    assert "PASS" in completed.stdout


def test_manual_smoke_freshness_validator_fails_when_package_release_row_lags_project_version(tmp_path):
    project = tmp_path / "pyproject.toml"
    project.write_text(
        "\n".join(
            [
                "[project]",
                'version = "9.9.9"',
            ]
        ),
        encoding="utf-8",
    )

    completed = _run_validator(project=project)

    assert completed.returncode == 1
    assert "Latest package/tag release must be `v9.9.9`" in completed.stdout


def _run_validator(project: Path | None = None) -> subprocess.CompletedProcess[str]:
    args = [
        sys.executable,
        str(SCRIPT),
        "--project",
        str(project or ROOT / "pyproject.toml"),
        "--ledger",
        str(ROOT / "docs" / "manual-smoke-evidence-ledger.md"),
        "--guide",
        str(ROOT / "docs" / "release-evidence.md"),
        "--checklist",
        str(ROOT / "docs" / "release-checklist.md"),
    ]
    return subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
