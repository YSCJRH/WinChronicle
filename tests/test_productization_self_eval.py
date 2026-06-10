import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_productization_self_eval_script_outputs_passing_json():
    script = ROOT / "harness" / "scripts" / "run_productization_self_eval.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--format", "json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout
    payload = json.loads(completed.stdout)

    assert payload["score"] >= 90
    assert payload["threshold"] >= 90
    assert payload["passed"] is True
    assert not payload["failed_items"]
    assert {
        "first_screen",
        "privacy_boundary",
        "fixture_demo",
        "codex_entry",
        "contributor_entry",
        "overclaim_risk",
    }.issubset(payload["categories"])


def test_productization_self_eval_script_outputs_plain_text_summary():
    script = ROOT / "harness" / "scripts" / "run_productization_self_eval.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--format", "text"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    assert completed.returncode == 0, completed.stdout
    assert "Productization self-eval" in completed.stdout
    assert "PASS" in completed.stdout
    assert "Score:" in completed.stdout
    assert "Next:" in completed.stdout


def test_demo_promotion_kit_is_safe_and_copyable():
    doc = (ROOT / "docs" / "demo-promotion-kit.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    required = [
        "# Demo Promotion Kit",
        "python harness/scripts/run_quick_demo.py",
        "fixture-only",
        "does not read the live desktop",
        "untrusted_observed_content",
        "No screenshots",
        "No OCR",
        "No clipboard",
        "No keylogging",
        "No cloud upload",
        "English launch blurb",
        "中文发布文案",
        "What to show in a demo",
        "What not to claim",
    ]
    for text in required:
        assert text in normalized

    for forbidden in [
        "official OpenAI project",
        "full Chronicle clone",
        "records everything",
        "controls your desktop",
    ]:
        assert forbidden not in doc.lower()


def test_readme_and_contributing_link_productization_self_eval():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert "[Demo promotion kit](docs/demo-promotion-kit.md)" in readme
    assert "[Productization self-eval](docs/productization-self-eval.md)" in readme
    assert "[Demo promotion kit](docs/demo-promotion-kit.md)" in readme_zh
    assert "[Productization self-eval](docs/productization-self-eval.md)" in readme_zh
    assert "Growth And Trust Starter Tasks" in contributing
    assert "python harness/scripts/run_productization_self_eval.py" in contributing
    assert "do not commit observed content" in contributing.lower()
