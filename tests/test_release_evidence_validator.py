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


def test_release_evidence_validator_accepts_run_url_before_windows_harness_label(tmp_path):
    evidence = tmp_path / "release-notes.md"
    evidence.write_text(
        "\n".join(
            [
                "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.47",
                "Remote run: https://github.com/YSCJRH/WinChronicle/actions/runs/27828004902 completed Windows Harness successfully.",
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


def test_release_evidence_validator_rejects_release_url_from_wrong_repo(tmp_path):
    evidence = tmp_path / "release-notes.md"
    evidence.write_text(
        "\n".join(
            [
                "Release URL: https://github.com/someone-else/WinChronicle/releases/tag/v0.2.47",
                "Remote Windows Harness: https://github.com/YSCJRH/WinChronicle/actions/runs/27828004902",
            ]
        ),
        encoding="utf-8",
    )

    completed = _run_validator(evidence)

    assert completed.returncode == 1
    assert "missing GitHub release URL for YSCJRH/WinChronicle" in completed.stdout


def test_release_evidence_validator_rejects_mixed_release_urls_from_wrong_repo(tmp_path):
    evidence = tmp_path / "release-notes.md"
    evidence.write_text(
        "\n".join(
            [
                "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.47",
                "Mirror release URL: https://github.com/someone-else/WinChronicle/releases/tag/v0.2.47",
                "Remote Windows Harness: https://github.com/YSCJRH/WinChronicle/actions/runs/27828004902",
            ]
        ),
        encoding="utf-8",
    )

    completed = _run_validator(evidence)

    assert completed.returncode == 1
    assert "unexpected GitHub release URL repo someone-else/WinChronicle" in completed.stdout


def test_release_evidence_validator_rejects_windows_harness_run_from_wrong_repo(tmp_path):
    evidence = tmp_path / "release-notes.md"
    evidence.write_text(
        "\n".join(
            [
                "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.47",
                "Remote Windows Harness: https://github.com/someone-else/WinChronicle/actions/runs/27828004902",
            ]
        ),
        encoding="utf-8",
    )

    completed = _run_validator(evidence)

    assert completed.returncode == 1
    assert "missing Windows Harness GitHub Actions run URL for YSCJRH/WinChronicle" in completed.stdout


def test_release_evidence_validator_rejects_mixed_actions_urls_from_wrong_repo(tmp_path):
    evidence = tmp_path / "release-notes.md"
    evidence.write_text(
        "\n".join(
            [
                "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.47",
                "Remote Windows Harness: https://github.com/YSCJRH/WinChronicle/actions/runs/27828004902",
                "Foreign Windows Harness: https://github.com/someone-else/WinChronicle/actions/runs/27828004902",
            ]
        ),
        encoding="utf-8",
    )

    completed = _run_validator(evidence)

    assert completed.returncode == 1
    assert "unexpected GitHub Actions run URL repo someone-else/WinChronicle" in completed.stdout


def test_release_evidence_validator_rejects_unbound_windows_harness_label(tmp_path):
    evidence = tmp_path / "release-notes.md"
    evidence.write_text(
        "\n".join(
            [
                "Release URL: https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.47",
                "Remote CI: https://github.com/YSCJRH/WinChronicle/actions/runs/27828004902",
                "Windows Harness completed successfully.",
            ]
        ),
        encoding="utf-8",
    )

    completed = _run_validator(evidence)

    assert completed.returncode == 1
    assert "missing Windows Harness GitHub Actions run URL for YSCJRH/WinChronicle" in completed.stdout


def test_v020_release_record_passes_release_evidence_validator():
    completed = _run_validator(ROOT / "docs" / "release-v0.2.0.md")

    assert completed.returncode == 0, completed.stdout


def test_current_release_validator_accepts_bound_project_release(tmp_path):
    project = tmp_path / "pyproject.toml"
    project.write_text(
        '[project]\nname = "winchronicle"\nversion = "0.2.51"\n',
        encoding="utf-8",
    )
    evidence = tmp_path / "release-evidence.md"
    head_sha = "53ad63a79ec088100999a64cca803ed53f04504d"
    evidence.write_text(
        "\n".join(
            [
                "# Release Evidence",
                "",
                "## Current Package Release Evidence",
                "",
                "| Field | Value |",
                "| --- | --- |",
                "| Release | `v0.2.51` |",
                "| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.51 |",
                f"| Tag target SHA | `{head_sha}` |",
                "| Publication status | Published, not a draft, not a prerelease |",
                f"| Windows Harness | Passed, https://github.com/YSCJRH/WinChronicle/actions/runs/27833755101, head `{head_sha}` |",
                "| Next active execution cursor | Post-v0.1.18 maintenance plan |",
                "",
                "## Other Evidence",
                "",
                "Historical Windows Harness: https://github.com/YSCJRH/WinChronicle/actions/runs/25947270522",
            ]
        ),
        encoding="utf-8",
    )

    completed = _run_validator_args(
        "--project",
        str(project),
        "--require-current-release",
        str(evidence),
    )

    assert completed.returncode == 0, completed.stdout
    assert "PASS" in completed.stdout


def test_current_release_validator_rejects_wrong_current_version_url(tmp_path):
    project = tmp_path / "pyproject.toml"
    project.write_text(
        '[project]\nname = "winchronicle"\nversion = "0.2.51"\n',
        encoding="utf-8",
    )
    evidence = tmp_path / "release-evidence.md"
    head_sha = "53ad63a79ec088100999a64cca803ed53f04504d"
    evidence.write_text(
        "\n".join(
            [
                "## Current Package Release Evidence",
                "| Field | Value |",
                "| --- | --- |",
                "| Release | `v0.2.50` |",
                "| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.50 |",
                f"| Tag target SHA | `{head_sha}` |",
                "| Publication status | Published, not a draft, not a prerelease |",
                f"| Windows Harness | Passed, https://github.com/YSCJRH/WinChronicle/actions/runs/27833755101, head `{head_sha}` |",
                "| Next active execution cursor | Post-v0.1.18 maintenance plan |",
            ]
        ),
        encoding="utf-8",
    )

    completed = _run_validator_args(
        "--project",
        str(project),
        "--require-current-release",
        str(evidence),
    )

    assert completed.returncode == 1
    assert "missing current release URL" in completed.stdout


def test_current_release_validator_rejects_mismatched_tag_and_harness_sha(tmp_path):
    project = tmp_path / "pyproject.toml"
    project.write_text(
        '[project]\nname = "winchronicle"\nversion = "0.2.51"\n',
        encoding="utf-8",
    )
    evidence = tmp_path / "release-evidence.md"
    tag_sha = "53ad63a79ec088100999a64cca803ed53f04504d"
    run_sha = "4c61f81aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    evidence.write_text(
        "\n".join(
            [
                "## Current Package Release Evidence",
                "| Field | Value |",
                "| --- | --- |",
                "| Release | `v0.2.51` |",
                "| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.51 |",
                f"| Tag target SHA | `{tag_sha}` |",
                "| Publication status | Published, not a draft, not a prerelease |",
                f"| Windows Harness | Passed, https://github.com/YSCJRH/WinChronicle/actions/runs/27833755101, head `{run_sha}` |",
                "| Next active execution cursor | Post-v0.1.18 maintenance plan |",
            ]
        ),
        encoding="utf-8",
    )

    completed = _run_validator_args(
        "--project",
        str(project),
        "--require-current-release",
        str(evidence),
    )

    assert completed.returncode == 1
    assert "Windows Harness head SHA does not match tag target SHA" in completed.stdout


def test_current_release_validator_requires_explicit_harness_head_sha(tmp_path):
    project = tmp_path / "pyproject.toml"
    project.write_text(
        '[project]\nname = "winchronicle"\nversion = "0.2.51"\n',
        encoding="utf-8",
    )
    evidence = tmp_path / "release-evidence.md"
    tag_sha = "53ad63a79ec088100999a64cca803ed53f04504d"
    evidence.write_text(
        "\n".join(
            [
                "## Current Package Release Evidence",
                "| Field | Value |",
                "| --- | --- |",
                "| Release | `v0.2.51` |",
                "| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.51 |",
                f"| Tag target SHA | `{tag_sha}` |",
                "| Publication status | Published, not a draft, not a prerelease |",
                f"| Windows Harness | Passed, tag `{tag_sha}`, https://github.com/YSCJRH/WinChronicle/actions/runs/27833755101 |",
                "| Next active execution cursor | Post-v0.1.18 maintenance plan |",
            ]
        ),
        encoding="utf-8",
    )

    completed = _run_validator_args(
        "--project",
        str(project),
        "--require-current-release",
        str(evidence),
    )

    assert completed.returncode == 1
    assert "missing current Windows Harness head SHA" in completed.stdout


def test_current_release_validator_rejects_unpublished_status(tmp_path):
    project = tmp_path / "pyproject.toml"
    project.write_text(
        '[project]\nname = "winchronicle"\nversion = "0.2.51"\n',
        encoding="utf-8",
    )
    evidence = tmp_path / "release-evidence.md"
    head_sha = "53ad63a79ec088100999a64cca803ed53f04504d"
    evidence.write_text(
        "\n".join(
            [
                "## Current Package Release Evidence",
                "| Field | Value |",
                "| --- | --- |",
                "| Release | `v0.2.51` |",
                "| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.51 |",
                f"| Tag target SHA | `{head_sha}` |",
                "| Publication status | Unpublished, not a draft, not a prerelease |",
                f"| Windows Harness | Passed, https://github.com/YSCJRH/WinChronicle/actions/runs/27833755101, head `{head_sha}` |",
                "| Next active execution cursor | Post-v0.1.18 maintenance plan |",
            ]
        ),
        encoding="utf-8",
    )

    completed = _run_validator_args(
        "--project",
        str(project),
        "--require-current-release",
        str(evidence),
    )

    assert completed.returncode == 1
    assert "current release status must say published" in completed.stdout


def test_release_evidence_guide_published_section_passes_current_release_validator(tmp_path):
    project = tmp_path / "pyproject.toml"
    project.write_text(
        '[project]\nname = "winchronicle"\nversion = "0.2.58"\n',
        encoding="utf-8",
    )
    completed = _run_validator_args(
        "--project",
        str(project),
        "--require-current-release",
        str(ROOT / "docs" / "release-evidence.md"),
    )

    assert completed.returncode == 0, completed.stdout


def test_release_state_validator_accepts_published_version_without_preflight(tmp_path):
    project = tmp_path / "pyproject.toml"
    project.write_text(
        '[project]\nname = "winchronicle"\nversion = "0.2.51"\n',
        encoding="utf-8",
    )
    evidence = tmp_path / "release-evidence.md"
    evidence.write_text(_published_release_evidence(), encoding="utf-8")

    completed = _run_validator_args(
        "--project",
        str(project),
        "--require-release-state",
        str(evidence),
    )

    assert completed.returncode == 0, completed.stdout


def test_release_state_validator_requires_next_preflight_when_project_version_ahead(tmp_path):
    project = tmp_path / "pyproject.toml"
    project.write_text(
        '[project]\nname = "winchronicle"\nversion = "0.2.52"\n',
        encoding="utf-8",
    )
    evidence = tmp_path / "release-evidence.md"
    evidence.write_text(_published_release_evidence(), encoding="utf-8")

    completed = _run_validator_args(
        "--project",
        str(project),
        "--require-release-state",
        str(evidence),
    )

    assert completed.returncode == 1
    assert "missing ## Next Package Release Preflight section for project version `v0.2.52`" in completed.stdout


def test_release_state_validator_accepts_project_version_ahead_with_preflight(tmp_path):
    project = tmp_path / "pyproject.toml"
    project.write_text(
        '[project]\nname = "winchronicle"\nversion = "0.2.52"\n',
        encoding="utf-8",
    )
    evidence = tmp_path / "release-evidence.md"
    evidence.write_text(
        "\n".join(
            [
                _published_release_evidence(),
                "",
                "## Next Package Release Preflight",
                "",
                "| Field | Value |",
                "| --- | --- |",
                "| Release | `v0.2.52` |",
                "| Expected release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.52 |",
                "| Publication status | Not published; pending post-publication reconciliation |",
                "| Required deterministic gate | `python harness/scripts/run_harness.py` |",
                "| Post-publication reconciliation | Update Current Package Release Evidence with tag target SHA and Windows Harness head SHA. |",
            ]
        ),
        encoding="utf-8",
    )

    completed = _run_validator_args(
        "--project",
        str(project),
        "--require-release-state",
        str(evidence),
    )

    assert completed.returncode == 0, completed.stdout


def test_release_state_validator_rejects_preflight_marked_published(tmp_path):
    project = tmp_path / "pyproject.toml"
    project.write_text(
        '[project]\nname = "winchronicle"\nversion = "0.2.52"\n',
        encoding="utf-8",
    )
    evidence = tmp_path / "release-evidence.md"
    evidence.write_text(
        "\n".join(
            [
                _published_release_evidence(),
                "",
                "## Next Package Release Preflight",
                "",
                "| Field | Value |",
                "| --- | --- |",
                "| Release | `v0.2.52` |",
                "| Expected release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.52 |",
                "| Publication status | Published, not a draft, not a prerelease |",
                "| Required deterministic gate | `python harness/scripts/run_harness.py` |",
                "| Post-publication reconciliation | Update Current Package Release Evidence with tag target SHA and Windows Harness head SHA. |",
            ]
        ),
        encoding="utf-8",
    )

    completed = _run_validator_args(
        "--project",
        str(project),
        "--require-release-state",
        str(evidence),
    )

    assert completed.returncode == 1
    assert "next release preflight must say not published" in completed.stdout


def test_release_state_validator_rejects_stale_preflight_when_project_version_is_published(tmp_path):
    project = tmp_path / "pyproject.toml"
    project.write_text(
        '[project]\nname = "winchronicle"\nversion = "0.2.51"\n',
        encoding="utf-8",
    )
    evidence = tmp_path / "release-evidence.md"
    evidence.write_text(
        "\n".join(
            [
                _published_release_evidence(),
                "",
                "## Next Package Release Preflight",
                "",
                "| Field | Value |",
                "| --- | --- |",
                "| Release | `v0.2.52` |",
                "| Expected release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.52 |",
                "| Publication status | Not published; pending post-publication reconciliation |",
                "| Required deterministic gate | `python harness/scripts/run_harness.py` |",
                "| Post-publication reconciliation | Update Current Package Release Evidence with tag target SHA and Windows Harness head SHA. |",
            ]
        ),
        encoding="utf-8",
    )

    completed = _run_validator_args(
        "--project",
        str(project),
        "--require-release-state",
        str(evidence),
    )

    assert completed.returncode == 1
    assert "unexpected next release preflight section when project version already matches" in completed.stdout


def test_release_evidence_guide_passes_release_state_validator():
    completed = _run_validator_args(
        "--project",
        str(ROOT / "pyproject.toml"),
        "--require-release-state",
        str(ROOT / "docs" / "release-evidence.md"),
    )

    assert completed.returncode == 0, completed.stdout


def test_release_evidence_guide_records_published_current_release_and_next_preflight():
    evidence = (ROOT / "docs" / "release-evidence.md").read_text(encoding="utf-8")

    assert "## Next Package Release Preflight" in evidence
    assert "| Release | `v0.2.58` |" in evidence
    assert "| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.58 |" in evidence
    assert "| Tag target SHA | `428f6bc6186cec6bc42327496a6a3c1f567a3126` |" in evidence
    assert (
        "| Publication status | Published, not a draft, not a prerelease; published at `2026-06-19T21:03:49Z` |"
        in evidence
    )
    assert (
        "| Windows Harness | Passed, https://github.com/YSCJRH/WinChronicle/actions/runs/27848063345, head `428f6bc6186cec6bc42327496a6a3c1f567a3126` |"
        in evidence
    )
    assert (
        "| Manual smoke relationship | `v0.2.58` does not refresh manual UIA smoke; the latest full manual UIA smoke source remains [v0.2.0 release record](release-v0.2.0.md). |"
        in evidence
    )
    assert "| Release | `v0.2.59` |" in evidence
    assert "| Expected release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.59 |" in evidence
    assert "| Publication status | Not published; pending post-publication reconciliation |" in evidence
    assert (
        "| Manual smoke relationship | `v0.2.59` does not refresh manual UIA smoke; the latest full manual UIA smoke source remains [v0.2.0 release record](release-v0.2.0.md). |"
        in evidence
    )
    assert "| Required deterministic gate | `python harness/scripts/run_harness.py` |" in evidence
    assert (
        "| Post-publication reconciliation | Update Current Package Release Evidence with tag target SHA and Windows Harness head SHA. |"
        in evidence
    )


def _published_release_evidence() -> str:
    head_sha = "53ad63a79ec088100999a64cca803ed53f04504d"
    return "\n".join(
        [
            "# Release Evidence",
            "",
            "## Current Package Release Evidence",
            "",
            "| Field | Value |",
            "| --- | --- |",
            "| Release | `v0.2.51` |",
            "| Release URL | https://github.com/YSCJRH/WinChronicle/releases/tag/v0.2.51 |",
            f"| Tag target SHA | `{head_sha}` |",
            "| Publication status | Published, not a draft, not a prerelease |",
            f"| Windows Harness | Passed, https://github.com/YSCJRH/WinChronicle/actions/runs/27833755101, head `{head_sha}` |",
            "| Next active execution cursor | Post-v0.1.18 maintenance plan |",
        ]
    )


def _run_validator(path: Path) -> subprocess.CompletedProcess[str]:
    return _run_validator_args(str(path))


def _run_validator_args(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
