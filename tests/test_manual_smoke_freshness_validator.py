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
    assert "missing next release preflight for project version `v9.9.9`" in completed.stdout


def test_manual_smoke_freshness_validator_rejects_preflight_without_manual_smoke_relationship(tmp_path):
    project = tmp_path / "pyproject.toml"
    project.write_text("[project]\nversion = \"9.9.9\"\n", encoding="utf-8")
    ledger = tmp_path / "manual-smoke-evidence-ledger.md"
    guide = tmp_path / "release-evidence.md"
    checklist = tmp_path / "release-checklist.md"
    ledger.write_text(
        "\n".join(
            [
                "| Field | Value |",
                "| --- | --- |",
                "| Latest package/tag release | `v9.9.8` ([GitHub release](https://github.com/YSCJRH/WinChronicle/releases/tag/v9.9.8)) |",
                "| Manual smoke relationship for latest package/tag | `v9.9.8` does not refresh manual UIA smoke; it is separate from the latest full manual UIA smoke source. |",
                "| Latest full manual UIA smoke source | [v0.2.0 release record](release-v0.2.0.md) |",
            ]
        ),
        encoding="utf-8",
    )
    guide.write_text(
        "\n".join(
            [
                "- the latest package/tag release is `v9.9.8`, recorded in the release.",
                "- the latest full manual UIA smoke source remains [v0.2.0 release record](release-v0.2.0.md);",
                "## Next Package Release Preflight",
                "| Field | Value |",
                "| --- | --- |",
                "| Release | `v9.9.9` |",
                "| Publication status | Not published; pending post-publication reconciliation |",
            ]
        ),
        encoding="utf-8",
    )
    checklist.write_text(guide.read_text(encoding="utf-8"), encoding="utf-8")

    completed = _run_validator(project=project, ledger=ledger, guide=guide, checklist=checklist)

    assert completed.returncode == 1
    assert "next release preflight must state `v9.9.9` does not refresh manual UIA smoke" in completed.stdout


def _run_validator(
    project: Path | None = None,
    ledger: Path | None = None,
    guide: Path | None = None,
    checklist: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    args = [
        sys.executable,
        str(SCRIPT),
        "--project",
        str(project or ROOT / "pyproject.toml"),
        "--ledger",
        str(ledger or ROOT / "docs" / "manual-smoke-evidence-ledger.md"),
        "--guide",
        str(guide or ROOT / "docs" / "release-evidence.md"),
        "--checklist",
        str(checklist or ROOT / "docs" / "release-checklist.md"),
    ]
    return subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
