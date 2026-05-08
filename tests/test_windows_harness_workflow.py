from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "windows-harness.yml"


def test_windows_harness_uses_current_windows_runner_without_gate_drift():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert 'FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: "true"' in text
    assert "runs-on: windows-2025-vs2026" in text
    assert "runs-on: windows-latest" not in text

    expected_steps = (
        "Check out repository",
        "Set up Python",
        "Set up .NET",
        "Install Python package",
        "Run unit tests",
        "Build UIA helper",
        "Build UIA watcher",
        "Run deterministic harness",
        "Check whitespace",
    )
    positions = [text.index(f"- name: {step}") for step in expected_steps]

    assert positions == sorted(positions)
    assert 'run: python -m pytest -q' in text
    assert (
        "run: dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo"
        in text
    )
    assert (
        "run: dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo"
        in text
    )
    assert "run: python harness/scripts/run_harness.py" in text
    assert "run: git diff --check" in text
