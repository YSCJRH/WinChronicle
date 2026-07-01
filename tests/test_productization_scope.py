from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _load_scope_module():
    script = ROOT / "harness" / "scripts" / "check_productization_scope.py"
    spec = importlib.util.spec_from_file_location("check_productization_scope", script)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_productization_scope_accepts_named_closeout_integration_branch(
    monkeypatch, capsys
):
    module = _load_scope_module()
    monkeypatch.setenv("GITHUB_HEAD_REF", "codex/winchronicle-closeout")
    monkeypatch.setattr(
        module,
        "_changed_files",
        lambda: [
            "README.md",
            "docs/codex-long-term-goal.md",
            "harness/specs/mcp-tool-result.schema.json",
            "src/winchronicle/workday.py",
            "tests/test_workday.py",
        ],
    )

    assert module.main() == 0

    assert "Closeout integration scope check passed" in capsys.readouterr().out


def test_productization_scope_rejects_closeout_files_outside_declared_integration(
    monkeypatch, capsys
):
    module = _load_scope_module()
    monkeypatch.setenv("GITHUB_HEAD_REF", "codex/winchronicle-closeout")
    monkeypatch.setattr(
        module,
        "_changed_files",
        lambda: [
            "README.md",
            "scripts/private_upload.py",
        ],
    )

    assert module.main() == 1

    output = capsys.readouterr().out
    assert "Closeout integration changed files outside scope:" in output
    assert "scripts/private_upload.py" in output
