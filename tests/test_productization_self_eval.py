import json
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


def _load_productization_self_eval_module():
    script = ROOT / "harness" / "scripts" / "run_productization_self_eval.py"
    spec = importlib.util.spec_from_file_location("run_productization_self_eval", script)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _copy_self_eval_check_files(module, target_root):
    for relative_path in {check.path for check in module.CHECKS}:
        source = ROOT / relative_path
        target = target_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


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


def test_productization_self_eval_json_payload_contract_is_versioned():
    module = _load_productization_self_eval_module()

    payload = module.evaluate()

    assert list(payload) == [
        "schema_version",
        "name",
        "score",
        "threshold",
        "passed",
        "categories",
        "failed_items",
        "next_actions",
        "provenance",
        "boundary",
    ]
    assert payload["schema_version"] == 1
    assert set(payload["provenance"]) == {"checked_root", "checked_paths"}
    assert payload["provenance"]["checked_root"] == str(ROOT)
    assert payload["provenance"]["checked_paths"] == sorted(
        {check.path for check in module.CHECKS}
    )
    assert payload["provenance"]["checked_paths"] == sorted(
        payload["provenance"]["checked_paths"]
    )
    assert set(payload["boundary"]) == {
        "does_not_run_live_uia",
        "does_not_read_desktop",
        "does_not_capture_observed_content",
        "checks_public_docs_and_static_metadata_only",
    }
    assert all(value is True for value in payload["boundary"].values())


def test_productization_self_eval_score_contract_is_explicit():
    module = _load_productization_self_eval_module()

    assert module.SCORE_FORMULA == "round(100 * passed / total)"
    assert module._percentage_score(0, 4) == 0
    assert module._percentage_score(1, 2) == 50
    assert module._percentage_score(2, 3) == 67
    assert module._percentage_score(3, 3) == 100


def test_productization_self_eval_score_contract_applies_to_overall_and_categories(
    tmp_path,
):
    module = _load_productization_self_eval_module()
    _copy_self_eval_check_files(module, tmp_path)

    doc = tmp_path / "docs" / "productization-self-eval.md"
    doc.write_text(
        doc.read_text(encoding="utf-8").replace(
            "## Stable Text Output",
            "## Output Notes",
        ),
        encoding="utf-8",
    )

    payload = module.evaluate(root=tmp_path)
    expected_score = module._percentage_score(len(module.CHECKS) - 1, len(module.CHECKS))
    contributor_checks = [
        check for check in module.CHECKS if check.category == "contributor_entry"
    ]
    expected_contributor_score = module._percentage_score(
        len(contributor_checks) - 1,
        len(contributor_checks),
    )

    assert payload["score"] == expected_score
    assert payload["categories"]["contributor_entry"] == expected_contributor_score


def test_productization_self_eval_pass_contract_is_explicit():
    module = _load_productization_self_eval_module()

    assert module.PASS_CONDITION == "score >= threshold and failed_items is empty"
    assert module._passes_gate(score=90, threshold=90, failed_items=[]) is True
    assert module._passes_gate(score=89, threshold=90, failed_items=[]) is False
    assert (
        module._passes_gate(
            score=100,
            threshold=90,
            failed_items=["contributor_entry: Example (docs/example.md: missing file)"],
        )
        is False
    )


def test_productization_self_eval_pass_contract_applies_to_evaluate(tmp_path):
    module = _load_productization_self_eval_module()
    _copy_self_eval_check_files(module, tmp_path)

    doc = tmp_path / "docs" / "productization-self-eval.md"
    doc.write_text(
        doc.read_text(encoding="utf-8").replace(
            "## Stable Text Output",
            "## Output Notes",
        ),
        encoding="utf-8",
    )

    payload = module.evaluate(threshold=0, root=tmp_path)

    assert payload["score"] >= payload["threshold"]
    assert payload["failed_items"]
    assert payload["passed"] is False


def test_productization_self_eval_threshold_contract_is_explicit():
    module = _load_productization_self_eval_module()

    assert module.DEFAULT_THRESHOLD == 90
    assert module.THRESHOLD_RANGE == "integer percentage from 0 to 100"
    assert module._validate_threshold(0) == 0
    assert module._validate_threshold(90) == 90
    assert module._validate_threshold(100) == 100

    for threshold in (-1, 101):
        with pytest.raises(ValueError, match="threshold must be between 0 and 100"):
            module._validate_threshold(threshold)

    for threshold in (True, 90.0, "90", None):
        with pytest.raises(TypeError, match="threshold must be an integer"):
            module._validate_threshold(threshold)


def test_productization_self_eval_cli_error_contract_is_explicit():
    module = _load_productization_self_eval_module()

    assert module.CLI_ERROR_EXIT_CODE == 2
    assert module.CLI_ERROR_NO_JSON_PAYLOAD is True
    assert module.CLI_ERROR_NO_TRACEBACK is True
    assert module.CLI_THRESHOLD_RANGE_ERROR == "threshold must be between 0 and 100"
    assert (
        module.CLI_THRESHOLD_INTEGER_ERROR
        == "threshold must be an integer between 0 and 100"
    )


def test_productization_self_eval_cli_rejects_threshold_outside_percentage_range():
    module = _load_productization_self_eval_module()
    script = ROOT / "harness" / "scripts" / "run_productization_self_eval.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--threshold", "101", "--format", "json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    assert completed.returncode == module.CLI_ERROR_EXIT_CODE, completed.stdout
    assert module.CLI_THRESHOLD_RANGE_ERROR in completed.stdout
    assert not completed.stdout.lstrip().startswith("{")
    assert '"schema_version"' not in completed.stdout
    assert "Traceback" not in completed.stdout


def test_productization_self_eval_cli_rejects_non_integer_threshold_without_json_payload():
    module = _load_productization_self_eval_module()
    script = ROOT / "harness" / "scripts" / "run_productization_self_eval.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--threshold", "true", "--format", "json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    assert completed.returncode == module.CLI_ERROR_EXIT_CODE, completed.stdout
    assert module.CLI_THRESHOLD_INTEGER_ERROR in completed.stdout
    assert not completed.stdout.lstrip().startswith("{")
    assert '"schema_version"' not in completed.stdout
    assert "Traceback" not in completed.stdout


def test_productization_self_eval_root_argument_contract_is_explicit(tmp_path):
    module = _load_productization_self_eval_module()

    assert (
        module.ROOT_ARGUMENT_CONTRACT
        == "existing directory used as local self-eval root"
    )
    assert module.CLI_ROOT_PATH_ERROR == "--root must be an existing directory"
    assert module._parse_root(str(ROOT)) == ROOT

    missing_root = tmp_path / "missing-root"
    file_root = tmp_path / "not-a-directory.txt"
    file_root.write_text("not a directory", encoding="utf-8")

    for invalid_root in (missing_root, file_root):
        with pytest.raises(
            module.argparse.ArgumentTypeError,
            match="--root must be an existing directory",
        ):
            module._parse_root(str(invalid_root))


def test_productization_self_eval_cli_rejects_invalid_root_without_json_payload(
    tmp_path,
):
    module = _load_productization_self_eval_module()
    script = ROOT / "harness" / "scripts" / "run_productization_self_eval.py"
    missing_root = tmp_path / "missing-root"
    file_root = tmp_path / "not-a-directory.txt"
    file_root.write_text("not a directory", encoding="utf-8")

    for invalid_root in (missing_root, file_root):
        completed = subprocess.run(
            [
                sys.executable,
                str(script),
                "--root",
                str(invalid_root),
                "--format",
                "json",
            ],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )

        assert completed.returncode == module.CLI_ERROR_EXIT_CODE, completed.stdout
        assert module.CLI_ROOT_PATH_ERROR in completed.stdout
        assert not completed.stdout.lstrip().startswith("{")
        assert '"schema_version"' not in completed.stdout
        assert "Traceback" not in completed.stdout


def test_productization_self_eval_cli_json_reports_existing_root_missing_checked_files(
    tmp_path,
):
    module = _load_productization_self_eval_module()
    _copy_self_eval_check_files(module, tmp_path)
    missing_doc = tmp_path / "docs" / "quick-demo.md"
    missing_doc.unlink()

    script = ROOT / "harness" / "scripts" / "run_productization_self_eval.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--root", str(tmp_path), "--format", "json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    assert completed.returncode == 1, completed.stdout
    payload = json.loads(completed.stdout)

    assert payload["passed"] is False
    assert "fixture_demo: Demo doc (docs/quick-demo.md: missing file)" in payload[
        "failed_items"
    ]
    assert payload["provenance"] == {
        "checked_root": str(tmp_path),
        "checked_paths": sorted({check.path for check in module.CHECKS}),
    }
    assert all(payload["boundary"].values())
    assert module.CLI_ROOT_PATH_ERROR not in completed.stdout
    assert "Traceback" not in completed.stdout


def test_productization_self_eval_failed_items_format_contract_is_explicit():
    module = _load_productization_self_eval_module()
    failure = {
        "category": "fixture_demo",
        "name": "Demo doc",
        "path": "docs/quick-demo.md",
        "reason": "missing file",
    }

    assert module.FAILED_ITEM_FORMAT == "category: name (path: reason)"
    assert (
        module._format_failed_item(failure)
        == "fixture_demo: Demo doc (docs/quick-demo.md: missing file)"
    )


def test_productization_self_eval_next_actions_contract_is_explicit():
    module = _load_productization_self_eval_module()

    assert module.PASSING_NEXT_ACTIONS == (
        "Keep README first-screen copy compact.",
        "Refresh demo and social copy when user-facing behavior changes.",
        "Add new growth/trust checks only when they protect a real onboarding promise.",
    )
    assert (
        module.MISSING_FILE_NEXT_ACTION
        == "Restore or create the missing checked files before rerunning."
    )
    assert module.GENERIC_FAILURE_NEXT_ACTIONS == (
        "Fix the listed missing or overclaiming items.",
        "Run python harness/scripts/run_productization_self_eval.py again.",
    )

    missing_file_failure = "fixture_demo: Demo doc (docs/quick-demo.md: missing file)"
    phrase_failure = (
        "contributor_entry: Self-eval JSON contract heading "
        "(docs/productization-self-eval.md: required phrase missing)"
    )

    assert module._next_actions([]) == list(module.PASSING_NEXT_ACTIONS)
    assert module._next_actions([missing_file_failure]) == [
        module.MISSING_FILE_NEXT_ACTION,
        *module.GENERIC_FAILURE_NEXT_ACTIONS,
    ]
    assert module._next_actions([phrase_failure]) == list(
        module.GENERIC_FAILURE_NEXT_ACTIONS
    )


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
    category_lines = completed.stdout.split("Categories:\n", 1)[1].split(
        "\nFailed items:", 1
    )[0].splitlines()
    boundary_lines = completed.stdout.split("Boundary:\n", 1)[1].split(
        "\nNext:", 1
    )[0].splitlines()

    assert category_lines == [
        "- codex_entry: 100",
        "- contributor_entry: 100",
        "- first_screen: 100",
        "- fixture_demo: 100",
        "- overclaim_risk: 100",
        "- privacy_boundary: 100",
    ]
    assert boundary_lines == [
        "- does_not_run_live_uia: true",
        "- does_not_read_desktop: true",
        "- does_not_capture_observed_content: true",
        "- checks_public_docs_and_static_metadata_only: true",
    ]


def test_productization_self_eval_groups_workday_entrypoint_guards_by_category():
    module = _load_productization_self_eval_module()

    entrypoint_guards = {
        (check.category, check.path, check.needle)
        for check in module.WORKDAY_ENTRYPOINT_BOUNDARY_CHECKS
    }
    expected_entrypoint_guards = {
        ("first_screen", "README.md", "record-only"),
        ("first_screen", "README.md", "summary-level evidence"),
        ("first_screen", "README.md", "does not send raw observed text"),
        ("first_screen", "README.md", "`summary_boundary`"),
        ("first_screen", "README.md", "not a telemetry or log-counter report"),
        ("first_screen", "README.zh-CN.md", "record-only"),
        ("first_screen", "README.zh-CN.md", "summary-level evidence"),
        ("first_screen", "README.zh-CN.md", "does not send raw observed text"),
        ("first_screen", "README.zh-CN.md", "`summary_boundary`"),
        ("first_screen", "README.zh-CN.md", "不是遥测或日志计数报告"),
        ("first_screen", "docs/windows-first-run.md", "record-only"),
        ("first_screen", "docs/windows-first-run.md", "summary-level evidence"),
        ("first_screen", "docs/windows-first-run.md", "does not send raw observed text"),
        ("first_screen", "docs/windows-first-run.md", "`summary_boundary`"),
        ("first_screen", "docs/windows-first-run.md", "not a telemetry or log-counter report"),
        ("codex_entry", "docs/codex-app-plugin-install.md", "record-only"),
        ("codex_entry", "docs/codex-app-plugin-install.md", "summary-level evidence"),
        ("codex_entry", "docs/codex-app-plugin-install.md", "does not send raw observed text"),
        ("codex_entry", "docs/codex-app-plugin-install.md", "Summary boundary:"),
        ("codex_entry", "docs/codex-app-plugin-install.md", "not a telemetry or log-counter report"),
        ("codex_entry", "docs/codex-app-workday-guide.md", "record-only"),
        ("codex_entry", "docs/codex-app-workday-guide.md", "summary-level evidence"),
        ("codex_entry", "docs/codex-app-workday-guide.md", "does not send raw observed text"),
        ("codex_entry", "docs/codex-app-workday-guide.md", "`summary_boundary`"),
        ("codex_entry", "docs/codex-app-workday-guide.md", "not a telemetry or log-counter report"),
        ("codex_entry", "docs/codex-workday-plugin.md", "record-only"),
        ("codex_entry", "docs/codex-workday-plugin.md", "summary-level evidence"),
        ("codex_entry", "docs/codex-workday-plugin.md", "does not send raw observed text"),
        ("codex_entry", "docs/codex-workday-plugin.md", "`summary_boundary`"),
        ("codex_entry", "docs/codex-workday-plugin.md", "not a telemetry or log-counter report"),
    }

    contributing_guards = {
        (check.category, check.path, check.needle)
        for check in module.WORKDAY_CONTRIBUTING_CONSISTENCY_CHECKS
    }
    expected_contributing_guards = {
        ("contributor_entry", "CONTRIBUTING.md", "five-entrypoint consistency"),
        ("contributor_entry", "CONTRIBUTING.md", "`docs/productization-self-eval.md`"),
        ("contributor_entry", "CONTRIBUTING.md", "`README.md`"),
        ("contributor_entry", "CONTRIBUTING.md", "`docs/windows-first-run.md`"),
        ("contributor_entry", "CONTRIBUTING.md", "`docs/codex-app-plugin-install.md`"),
        ("contributor_entry", "CONTRIBUTING.md", "`docs/codex-app-workday-guide.md`"),
        ("contributor_entry", "CONTRIBUTING.md", "`docs/codex-workday-plugin.md`"),
        ("contributor_entry", "CONTRIBUTING.md", "record-only"),
        ("contributor_entry", "CONTRIBUTING.md", "summary-level evidence"),
        ("contributor_entry", "CONTRIBUTING.md", "does not send raw observed text"),
        ("contributor_entry", "CONTRIBUTING.md", "tests/test_readme_daily_workflow.py -q"),
        ("contributor_entry", "CONTRIBUTING.md", "run_productization_self_eval.py --format json"),
        ("contributor_entry", "CONTRIBUTING.md", "若修改 `README.md` 或 `README.zh-CN.md` 的 Workday guidance"),
    }

    all_checks = {(check.category, check.path, check.needle) for check in module.CHECKS}

    assert entrypoint_guards == expected_entrypoint_guards
    assert contributing_guards == expected_contributing_guards
    assert entrypoint_guards <= all_checks
    assert contributing_guards <= all_checks


def test_workday_entrypoint_boundary_checks_reuse_shared_text_constants():
    module = _load_productization_self_eval_module()
    needles = [check.needle for check in module.WORKDAY_ENTRYPOINT_BOUNDARY_CHECKS]

    assert module.WORKDAY_RECORD_ONLY_TEXT == "record-only"
    assert module.WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT == "summary-level evidence"
    assert module.WORKDAY_NO_RAW_OBSERVED_TEXT == "does not send raw observed text"
    assert module.WORKDAY_SUMMARY_BOUNDARY_FIELD_TEXT == "`summary_boundary`"
    assert module.WORKDAY_NOT_TELEMETRY_REPORT_TEXT == (
        "not a telemetry or log-counter report"
    )
    assert needles.count(module.WORKDAY_RECORD_ONLY_TEXT) == 6
    assert needles.count(module.WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT) == 6
    assert needles.count(module.WORKDAY_NO_RAW_OBSERVED_TEXT) == 6
    assert needles.count(module.WORKDAY_SUMMARY_BOUNDARY_FIELD_TEXT) == 5
    assert needles.count(module.WORKDAY_NOT_TELEMETRY_REPORT_TEXT) == 5


def test_workday_contributing_shared_boundary_texts_are_runtime_contract():
    module = _load_productization_self_eval_module()
    contributing_needles = {
        check.needle for check in module.WORKDAY_CONTRIBUTING_CONSISTENCY_CHECKS
    }

    assert module.WORKDAY_CONTRIBUTING_SHARED_BOUNDARY_TEXTS == (
        module.WORKDAY_RECORD_ONLY_TEXT,
        module.WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT,
        module.WORKDAY_NO_RAW_OBSERVED_TEXT,
    )
    assert set(module.WORKDAY_CONTRIBUTING_SHARED_BOUNDARY_TEXTS) <= contributing_needles


def test_workday_contributing_meta_targets_are_runtime_contract():
    module = _load_productization_self_eval_module()

    assert module.WORKDAY_CONTRIBUTING_META_TARGETS == (
        ("consistency rule", "five-entrypoint consistency"),
        ("self-eval link", "`docs/productization-self-eval.md`"),
    )
    assert tuple(
        (check.name, check.path, check.needle)
        for check in module.WORKDAY_CONTRIBUTING_META_CHECKS
    ) == tuple(
        (f"Contributing Workday {meta_name}", "CONTRIBUTING.md", meta_text)
        for meta_name, meta_text in module.WORKDAY_CONTRIBUTING_META_TARGETS
    )
    assert set(module.WORKDAY_CONTRIBUTING_META_CHECKS) <= set(
        module.WORKDAY_CONTRIBUTING_CONSISTENCY_CHECKS
    )


def test_workday_contributing_boundary_targets_are_runtime_contract():
    module = _load_productization_self_eval_module()

    assert module.WORKDAY_CONTRIBUTING_BOUNDARY_TARGETS == (
        ("record-only boundary", module.WORKDAY_RECORD_ONLY_TEXT),
        ("summary evidence boundary", module.WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT),
        ("raw text boundary", module.WORKDAY_NO_RAW_OBSERVED_TEXT),
    )
    assert tuple(
        (check.name, check.path, check.needle)
        for check in module.WORKDAY_CONTRIBUTING_BOUNDARY_CHECKS
    ) == tuple(
        (f"Contributing Workday {boundary_name}", "CONTRIBUTING.md", boundary_text)
        for boundary_name, boundary_text in module.WORKDAY_CONTRIBUTING_BOUNDARY_TARGETS
    )
    assert set(module.WORKDAY_CONTRIBUTING_BOUNDARY_CHECKS) <= set(
        module.WORKDAY_CONTRIBUTING_CONSISTENCY_CHECKS
    )


def test_workday_contributing_consistency_checks_reuse_shared_text_constants():
    module = _load_productization_self_eval_module()
    checks = {
        (check.name, check.path, check.needle)
        for check in module.WORKDAY_CONTRIBUTING_CONSISTENCY_CHECKS
    }

    assert module.WORKDAY_CONTRIBUTING_SHARED_BOUNDARY_TEXTS == (
        module.WORKDAY_RECORD_ONLY_TEXT,
        module.WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT,
        module.WORKDAY_NO_RAW_OBSERVED_TEXT,
    )
    assert {
        ("Contributing Workday record-only boundary", "CONTRIBUTING.md", module.WORKDAY_RECORD_ONLY_TEXT),
        (
            "Contributing Workday summary evidence boundary",
            "CONTRIBUTING.md",
            module.WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT,
        ),
        (
            "Contributing Workday raw text boundary",
            "CONTRIBUTING.md",
            module.WORKDAY_NO_RAW_OBSERVED_TEXT,
        ),
    } <= checks


def test_workday_contributing_entrypoint_targets_are_runtime_contract():
    module = _load_productization_self_eval_module()

    assert module.WORKDAY_CONTRIBUTING_ENTRYPOINT_TARGETS == (
        ("README entrypoint", "`README.md`"),
        ("first-run entrypoint", "`docs/windows-first-run.md`"),
        ("plugin install entrypoint", "`docs/codex-app-plugin-install.md`"),
        ("guide entrypoint", "`docs/codex-app-workday-guide.md`"),
        ("plugin doc entrypoint", "`docs/codex-workday-plugin.md`"),
    )
    assert tuple(
        (check.name, check.path, check.needle)
        for check in module.WORKDAY_CONTRIBUTING_ENTRYPOINT_CHECKS
    ) == tuple(
        (f"Contributing Workday {target_name}", "CONTRIBUTING.md", target_text)
        for target_name, target_text in module.WORKDAY_CONTRIBUTING_ENTRYPOINT_TARGETS
    )
    assert set(module.WORKDAY_CONTRIBUTING_ENTRYPOINT_CHECKS) <= set(
        module.WORKDAY_CONTRIBUTING_CONSISTENCY_CHECKS
    )


def test_workday_contributing_validation_targets_are_runtime_contract():
    module = _load_productization_self_eval_module()

    assert module.WORKDAY_CONTRIBUTING_VALIDATION_TARGETS == (
        (
            "README daily workflow validation",
            module.WORKDAY_README_DAILY_WORKFLOW_VALIDATION_TEXT,
        ),
        (
            "self-eval JSON validation",
            module.WORKDAY_PRODUCTIZATION_SELF_EVAL_VALIDATION_TEXT,
        ),
        (
            "Chinese README validation note",
            "若修改 `README.md` 或 `README.zh-CN.md` 的 Workday guidance",
        ),
    )
    assert tuple(
        (check.name, check.path, check.needle)
        for check in module.WORKDAY_CONTRIBUTING_VALIDATION_CHECKS
    ) == tuple(
        (f"Contributing Workday {validation_name}", "CONTRIBUTING.md", validation_text)
        for validation_name, validation_text in module.WORKDAY_CONTRIBUTING_VALIDATION_TARGETS
    )
    assert set(module.WORKDAY_CONTRIBUTING_VALIDATION_CHECKS) <= set(
        module.WORKDAY_CONTRIBUTING_CONSISTENCY_CHECKS
    )


def test_workday_validation_gate_checks_reuse_shared_command_constants():
    module = _load_productization_self_eval_module()

    assert (
        module.WORKDAY_README_DAILY_WORKFLOW_VALIDATION_TEXT
        == "tests/test_readme_daily_workflow.py -q"
    )
    assert (
        module.WORKDAY_PRODUCTIZATION_SELF_EVAL_VALIDATION_TEXT
        == "run_productization_self_eval.py --format json"
    )
    assert module.WORKDAY_SHARED_VALIDATION_TEXTS == (
        module.WORKDAY_README_DAILY_WORKFLOW_VALIDATION_TEXT,
        module.WORKDAY_PRODUCTIZATION_SELF_EVAL_VALIDATION_TEXT,
    )

    contributing_needles = [
        check.needle for check in module.WORKDAY_CONTRIBUTING_CONSISTENCY_CHECKS
    ]
    checklist_needles = [
        check.needle for check in module.WORKDAY_CONTRIBUTOR_CHECKLIST_CHECKS
    ]

    for validation_text in module.WORKDAY_SHARED_VALIDATION_TEXTS:
        assert contributing_needles.count(validation_text) == 1
        assert checklist_needles.count(validation_text) == 2


def test_workday_shared_validation_texts_are_runtime_contract():
    module = _load_productization_self_eval_module()
    contributing_needles = {
        check.needle for check in module.WORKDAY_CONTRIBUTING_CONSISTENCY_CHECKS
    }
    checklist_needles = {
        check.needle for check in module.WORKDAY_CONTRIBUTOR_CHECKLIST_CHECKS
    }

    assert module.WORKDAY_SHARED_VALIDATION_TEXTS == (
        module.WORKDAY_README_DAILY_WORKFLOW_VALIDATION_TEXT,
        module.WORKDAY_PRODUCTIZATION_SELF_EVAL_VALIDATION_TEXT,
    )
    assert set(module.WORKDAY_SHARED_VALIDATION_TEXTS) <= contributing_needles
    assert set(module.WORKDAY_SHARED_VALIDATION_TEXTS) <= checklist_needles


def test_productization_self_eval_groups_stable_text_output_checks_by_category():
    module = _load_productization_self_eval_module()

    stable_output_checks = {
        (check.category, check.name, check.path, check.needle, check.mode)
        for check in module.SELF_EVAL_STABLE_TEXT_OUTPUT_CHECKS
    }
    expected_stable_output_checks = {
        (
            "contributor_entry",
            "Self-eval stable text output heading",
            "docs/productization-self-eval.md",
            "## Stable Text Output",
            "contains",
        ),
        (
            "contributor_entry",
            "Self-eval stable text output category order",
            "docs/productization-self-eval.md",
            "`Categories:` uses this canonical order",
            "canonical_category_order",
        ),
        (
            "contributor_entry",
            "Self-eval stable text output boundary order",
            "docs/productization-self-eval.md",
            "`Boundary:` uses this canonical order",
            "canonical_boundary_order",
        ),
        (
            "contributor_entry",
            "Self-eval stable text output update rule",
            "docs/productization-self-eval.md",
            "update the canonical order constants",
            "contains",
        ),
    }
    all_checks = {
        (check.category, check.name, check.path, check.needle, check.mode)
        for check in module.CHECKS
    }

    assert stable_output_checks == expected_stable_output_checks
    assert stable_output_checks <= all_checks


def test_productization_self_eval_groups_json_provenance_checks_by_category():
    module = _load_productization_self_eval_module()

    json_provenance_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.SELF_EVAL_JSON_PROVENANCE_CHECKS
    }
    expected_json_provenance_checks = {
        (
            "contributor_entry",
            "Self-eval JSON provenance heading",
            "docs/productization-self-eval.md",
            "## JSON Provenance",
        ),
        (
            "contributor_entry",
            "Self-eval JSON provenance checked root",
            "docs/productization-self-eval.md",
            "`provenance.checked_root`",
        ),
        (
            "contributor_entry",
            "Self-eval JSON provenance checked paths",
            "docs/productization-self-eval.md",
            "`provenance.checked_paths`",
        ),
        (
            "contributor_entry",
            "Self-eval JSON provenance sharing boundary",
            "docs/productization-self-eval.md",
            "do not treat JSON output as permission to publish",
        ),
        (
            "contributor_entry",
            "Self-eval JSON provenance fixed path boundary",
            "docs/productization-self-eval.md",
            "fixed repository-relative docs and static metadata paths",
        ),
    }
    all_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.CHECKS
    }

    assert json_provenance_checks == expected_json_provenance_checks
    assert json_provenance_checks <= all_checks


def test_productization_self_eval_groups_json_contract_checks_by_category():
    module = _load_productization_self_eval_module()

    json_contract_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.SELF_EVAL_JSON_CONTRACT_CHECKS
    }
    expected_json_contract_checks = {
        (
            "contributor_entry",
            "Self-eval JSON contract heading",
            "docs/productization-self-eval.md",
            "## JSON Contract",
        ),
        (
            "contributor_entry",
            "Self-eval JSON contract schema version",
            "docs/productization-self-eval.md",
            "`schema_version = 1`",
        ),
        (
            "contributor_entry",
            "Self-eval JSON contract top-level keys",
            "docs/productization-self-eval.md",
            "`schema_version`, `name`, `score`, `threshold`, `passed`, `categories`, `failed_items`, `next_actions`, `provenance`, and `boundary`",
        ),
        (
            "contributor_entry",
            "Self-eval JSON contract update rule",
            "docs/productization-self-eval.md",
            "change the schema version and focused JSON contract tests before renaming or removing fields",
        ),
    }
    all_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.CHECKS
    }

    assert json_contract_checks == expected_json_contract_checks
    assert json_contract_checks <= all_checks


def test_productization_self_eval_groups_json_failure_contract_checks_by_category():
    module = _load_productization_self_eval_module()

    json_failure_contract_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.SELF_EVAL_JSON_FAILURE_CONTRACT_CHECKS
    }
    expected_json_failure_contract_checks = {
        (
            "contributor_entry",
            "Self-eval JSON failure contract heading",
            "docs/productization-self-eval.md",
            "## JSON Failure Contract",
        ),
        (
            "contributor_entry",
            "Self-eval JSON failure contract stable shape",
            "docs/productization-self-eval.md",
            "Failure JSON keeps the same `schema_version`, `provenance`, and `boundary` fields",
        ),
        (
            "contributor_entry",
            "Self-eval JSON failure contract failed items",
            "docs/productization-self-eval.md",
            "`failed_items` identifies the missing or overclaiming check",
        ),
        (
            "contributor_entry",
            "Self-eval JSON failure contract no path snapshots",
            "docs/productization-self-eval.md",
            "Do not snapshot absolute `checked_root` paths",
        ),
    }
    all_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.CHECKS
    }

    assert json_failure_contract_checks == expected_json_failure_contract_checks
    assert json_failure_contract_checks <= all_checks


def test_productization_self_eval_groups_failed_item_format_checks_by_category():
    module = _load_productization_self_eval_module()

    failed_item_format_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.SELF_EVAL_FAILED_ITEM_FORMAT_CHECKS
    }
    expected_failed_item_format_checks = {
        (
            "contributor_entry",
            "Self-eval failed item format heading",
            "docs/productization-self-eval.md",
            "## Failed Item Format",
        ),
        (
            "contributor_entry",
            "Self-eval failed item format contract",
            "docs/productization-self-eval.md",
            "`failed_items` entries use `category: name (path: reason)`",
        ),
        (
            "contributor_entry",
            "Self-eval failed item format update rule",
            "docs/productization-self-eval.md",
            "update `FAILED_ITEM_FORMAT` and focused failed-item format tests",
        ),
    }
    all_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.CHECKS
    }

    assert failed_item_format_checks == expected_failed_item_format_checks
    assert failed_item_format_checks <= all_checks


def test_productization_self_eval_groups_next_actions_contract_checks_by_category():
    module = _load_productization_self_eval_module()

    next_actions_contract_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.SELF_EVAL_NEXT_ACTIONS_CONTRACT_CHECKS
    }
    expected_next_actions_contract_checks = {
        (
            "contributor_entry",
            "Self-eval next actions contract heading",
            "docs/productization-self-eval.md",
            "## Next Actions Contract",
        ),
        (
            "contributor_entry",
            "Self-eval next actions stable vocabulary",
            "docs/productization-self-eval.md",
            "`next_actions` is a small stable action vocabulary for local automation.",
        ),
        (
            "contributor_entry",
            "Self-eval next actions passing entries",
            "docs/productization-self-eval.md",
            "Passing runs use the three `PASSING_NEXT_ACTIONS` entries",
        ),
        (
            "contributor_entry",
            "Self-eval next actions missing-file entries",
            "docs/productization-self-eval.md",
            "Missing-file failures prepend `MISSING_FILE_NEXT_ACTION` before `GENERIC_FAILURE_NEXT_ACTIONS`.",
        ),
        (
            "contributor_entry",
            "Self-eval next actions generic failure entries",
            "docs/productization-self-eval.md",
            "Other failures return only `GENERIC_FAILURE_NEXT_ACTIONS`.",
        ),
        (
            "contributor_entry",
            "Self-eval next actions update rule",
            "docs/productization-self-eval.md",
            "update `PASSING_NEXT_ACTIONS`, `MISSING_FILE_NEXT_ACTION`, `GENERIC_FAILURE_NEXT_ACTIONS`, and focused next-actions tests",
        ),
    }
    all_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.CHECKS
    }

    assert next_actions_contract_checks == expected_next_actions_contract_checks
    assert next_actions_contract_checks <= all_checks


def test_productization_self_eval_groups_score_contract_checks_by_category():
    module = _load_productization_self_eval_module()

    score_contract_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.SELF_EVAL_SCORE_CONTRACT_CHECKS
    }
    expected_score_contract_checks = {
        (
            "contributor_entry",
            "Self-eval score contract heading",
            "docs/productization-self-eval.md",
            "## Score Contract",
        ),
        (
            "contributor_entry",
            "Self-eval score formula",
            "docs/productization-self-eval.md",
            "`score` and category scores use `round(100 * passed / total)`.",
        ),
        (
            "contributor_entry",
            "Self-eval score helper update rule",
            "docs/productization-self-eval.md",
            "update `SCORE_FORMULA`, `_percentage_score`, and focused score contract tests",
        ),
    }
    all_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.CHECKS
    }

    assert score_contract_checks == expected_score_contract_checks
    assert score_contract_checks <= all_checks


def test_productization_self_eval_groups_pass_contract_checks_by_category():
    module = _load_productization_self_eval_module()

    pass_contract_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.SELF_EVAL_PASS_CONTRACT_CHECKS
    }
    expected_pass_contract_checks = {
        (
            "contributor_entry",
            "Self-eval pass contract heading",
            "docs/productization-self-eval.md",
            "## Pass Contract",
        ),
        (
            "contributor_entry",
            "Self-eval pass condition",
            "docs/productization-self-eval.md",
            "`passed` is true only when `score >= threshold` and `failed_items` is empty.",
        ),
        (
            "contributor_entry",
            "Self-eval pass helper update rule",
            "docs/productization-self-eval.md",
            "update `PASS_CONDITION`, `_passes_gate`, and focused pass contract tests",
        ),
    }
    all_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.CHECKS
    }

    assert pass_contract_checks == expected_pass_contract_checks
    assert pass_contract_checks <= all_checks


def test_productization_self_eval_groups_threshold_contract_checks_by_category():
    module = _load_productization_self_eval_module()

    threshold_contract_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.SELF_EVAL_THRESHOLD_CONTRACT_CHECKS
    }
    expected_threshold_contract_checks = {
        (
            "contributor_entry",
            "Self-eval threshold contract heading",
            "docs/productization-self-eval.md",
            "## Threshold Contract",
        ),
        (
            "contributor_entry",
            "Self-eval default threshold",
            "docs/productization-self-eval.md",
            "`DEFAULT_THRESHOLD` is 90.",
        ),
        (
            "contributor_entry",
            "Self-eval threshold range",
            "docs/productization-self-eval.md",
            "`threshold` is an integer percentage from 0 to 100.",
        ),
        (
            "contributor_entry",
            "Self-eval CLI error exit code",
            "docs/productization-self-eval.md",
            "`CLI_ERROR_EXIT_CODE` is 2.",
        ),
        (
            "contributor_entry",
            "Self-eval CLI threshold error text",
            "docs/productization-self-eval.md",
            "CLI threshold errors use `CLI_THRESHOLD_RANGE_ERROR` or `CLI_THRESHOLD_INTEGER_ERROR`.",
        ),
        (
            "contributor_entry",
            "Self-eval CLI error output boundary",
            "docs/productization-self-eval.md",
            "CLI threshold errors do not emit a JSON payload or traceback.",
        ),
        (
            "contributor_entry",
            "Self-eval threshold helper update rule",
            "docs/productization-self-eval.md",
            "update `THRESHOLD_RANGE`, `CLI_ERROR_EXIT_CODE`, `CLI_THRESHOLD_RANGE_ERROR`, `CLI_THRESHOLD_INTEGER_ERROR`, `_validate_threshold`, `_parse_threshold`, and focused threshold contract tests",
        ),
    }
    all_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.CHECKS
    }

    assert threshold_contract_checks == expected_threshold_contract_checks
    assert threshold_contract_checks <= all_checks


def test_productization_self_eval_groups_root_argument_contract_checks_by_category():
    module = _load_productization_self_eval_module()

    root_argument_contract_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.SELF_EVAL_ROOT_ARGUMENT_CONTRACT_CHECKS
    }
    expected_root_argument_contract_checks = {
        (
            "contributor_entry",
            "Self-eval root argument contract heading",
            "docs/productization-self-eval.md",
            "## Root Argument Contract",
        ),
        (
            "contributor_entry",
            "Self-eval root argument purpose",
            "docs/productization-self-eval.md",
            "`--root` is a hidden local test override.",
        ),
        (
            "contributor_entry",
            "Self-eval root argument existing directory",
            "docs/productization-self-eval.md",
            "`ROOT_ARGUMENT_CONTRACT` is `existing directory used as local self-eval root`.",
        ),
        (
            "contributor_entry",
            "Self-eval root argument CLI error text",
            "docs/productization-self-eval.md",
            "CLI root errors use `CLI_ROOT_PATH_ERROR`.",
        ),
        (
            "contributor_entry",
            "Self-eval root argument no payload",
            "docs/productization-self-eval.md",
            "Invalid root paths do not emit a JSON payload or traceback.",
        ),
        (
            "contributor_entry",
            "Self-eval root argument missing checked paths",
            "docs/productization-self-eval.md",
            "Existing roots with missing checked paths are self-eval failures, not CLI argument errors.",
        ),
        (
            "contributor_entry",
            "Self-eval root argument helper update rule",
            "docs/productization-self-eval.md",
            "update `ROOT_ARGUMENT_CONTRACT`, `CLI_ROOT_PATH_ERROR`, `_parse_root`, and focused root argument tests",
        ),
    }
    all_checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.CHECKS
    }

    assert root_argument_contract_checks == expected_root_argument_contract_checks
    assert root_argument_contract_checks <= all_checks


def test_productization_self_eval_reports_missing_workday_summary_boundary(tmp_path):
    module = _load_productization_self_eval_module()
    _copy_self_eval_check_files(module, tmp_path)

    readme = tmp_path / "README.md"
    readme.write_text(
        readme.read_text(encoding="utf-8").replace("`summary_boundary`", "`removed_boundary`"),
        encoding="utf-8",
    )

    payload = module.evaluate(root=tmp_path)

    assert payload["passed"] is False
    assert (
        "first_screen: README Workday summary boundary field "
        "(README.md: required phrase missing)"
    ) in payload["failed_items"]
    assert payload["categories"]["first_screen"] < 100
    assert "Fix the listed missing or overclaiming items." in payload["next_actions"]


def test_productization_self_eval_reports_missing_chinese_workday_telemetry_boundary(
    tmp_path,
):
    module = _load_productization_self_eval_module()
    _copy_self_eval_check_files(module, tmp_path)

    readme_zh = tmp_path / "README.zh-CN.md"
    readme_zh.write_text(
        readme_zh.read_text(encoding="utf-8").replace(
            "不是遥测或日志计数报告",
            "不是普通日志报告",
        ),
        encoding="utf-8",
    )

    payload = module.evaluate(root=tmp_path)

    assert payload["passed"] is False
    assert (
        "first_screen: README zh-CN Workday localized telemetry boundary "
        "(README.zh-CN.md: required phrase missing)"
    ) in payload["failed_items"]
    assert payload["categories"]["first_screen"] < 100


def test_productization_self_eval_reports_missing_checked_file_with_restore_action(tmp_path):
    module = _load_productization_self_eval_module()
    _copy_self_eval_check_files(module, tmp_path)

    missing_doc = tmp_path / "docs" / "quick-demo.md"
    missing_doc.unlink()

    payload = module.evaluate(root=tmp_path)

    assert payload["passed"] is False
    assert "fixture_demo: Demo doc (docs/quick-demo.md: missing file)" in payload[
        "failed_items"
    ]
    assert payload["categories"]["fixture_demo"] < 100
    assert payload["schema_version"] == 1
    assert payload["provenance"] == {
        "checked_root": str(tmp_path),
        "checked_paths": sorted({check.path for check in module.CHECKS}),
    }
    assert payload["boundary"] == {
        "does_not_run_live_uia": True,
        "does_not_read_desktop": True,
        "does_not_capture_observed_content": True,
        "checks_public_docs_and_static_metadata_only": True,
    }
    assert "Restore or create the missing checked files before rerunning." in payload[
        "next_actions"
    ]


def test_productization_self_eval_text_output_includes_restore_action_and_boundary(tmp_path):
    module = _load_productization_self_eval_module()
    _copy_self_eval_check_files(module, tmp_path)

    missing_doc = tmp_path / "docs" / "quick-demo.md"
    missing_doc.unlink()

    output = module._format_text(module.evaluate(root=tmp_path))

    assert "Status: FAIL" in output
    assert "- fixture_demo: Demo doc (docs/quick-demo.md: missing file)" in output
    assert "- Restore or create the missing checked files before rerunning." in output
    assert "Boundary:" in output
    assert "- does_not_read_desktop: true" in output
    assert "- does_not_capture_observed_content: true" in output
    assert "- checks_public_docs_and_static_metadata_only: true" in output
    assert "- does_not_read_desktop: True" not in output


def test_productization_self_eval_text_output_uses_canonical_boundary_order():
    module = _load_productization_self_eval_module()
    payload = module.evaluate()
    payload["boundary"] = {
        "checks_public_docs_and_static_metadata_only": True,
        "does_not_capture_observed_content": True,
        "does_not_read_desktop": True,
        "does_not_run_live_uia": True,
    }

    output = module._format_text(payload)
    boundary_lines = output.split("Boundary:\n", 1)[1].split("\nNext:", 1)[0].splitlines()

    assert boundary_lines == [
        "- does_not_run_live_uia: true",
        "- does_not_read_desktop: true",
        "- does_not_capture_observed_content: true",
        "- checks_public_docs_and_static_metadata_only: true",
    ]


def test_productization_self_eval_text_output_uses_canonical_category_order():
    module = _load_productization_self_eval_module()
    payload = module.evaluate()
    payload["categories"] = {
        "privacy_boundary": 100,
        "overclaim_risk": 100,
        "fixture_demo": 100,
        "first_screen": 100,
        "contributor_entry": 100,
        "codex_entry": 100,
    }

    output = module._format_text(payload)
    category_lines = output.split("Categories:\n", 1)[1].split(
        "\nFailed items:", 1
    )[0].splitlines()

    assert category_lines == [
        "- codex_entry: 100",
        "- contributor_entry: 100",
        "- first_screen: 100",
        "- fixture_demo: 100",
        "- overclaim_risk: 100",
        "- privacy_boundary: 100",
    ]


def test_productization_self_eval_text_output_appends_unknown_categories_after_known_order():
    module = _load_productization_self_eval_module()
    payload = module.evaluate()
    payload["categories"] = {
        "privacy_boundary": 100,
        "accessibility": 100,
        "overclaim_risk": 100,
        "fixture_demo": 100,
        "first_screen": 100,
        "contributor_entry": 100,
        "codex_entry": 100,
    }

    output = module._format_text(payload)
    category_lines = output.split("Categories:\n", 1)[1].split(
        "\nFailed items:", 1
    )[0].splitlines()

    assert category_lines == [
        "- codex_entry: 100",
        "- contributor_entry: 100",
        "- first_screen: 100",
        "- fixture_demo: 100",
        "- overclaim_risk: 100",
        "- privacy_boundary: 100",
        "- accessibility: 100",
    ]


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


def test_demo_promotion_kit_warns_feature_proposals_do_not_authorize_implementation():
    doc = (ROOT / "docs" / "demo-promotion-kit.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "Do not treat a feature proposal, launch request, or shareable idea as approval to implement runtime behavior.",
        "Route product-facing ideas through `CONTRIBUTING.md` and `docs/productization-self-eval.md` before changing behavior.",
    ):
        assert expected in normalized


def test_demo_promotion_feature_proposal_boundary_checks_are_grouped():
    module = _load_productization_self_eval_module()
    checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.DEMO_PROMOTION_FEATURE_PROPOSAL_BOUNDARY_CHECKS
    }

    assert checks == {
        (
            "fixture_demo",
            "Promotion kit feature proposal boundary",
            "docs/demo-promotion-kit.md",
            "feature proposal",
        ),
        (
            "fixture_demo",
            "Promotion kit implementation approval boundary",
            "docs/demo-promotion-kit.md",
            "approval to implement runtime behavior",
        ),
        (
            "fixture_demo",
            "Promotion kit contributing route",
            "docs/demo-promotion-kit.md",
            "`CONTRIBUTING.md`",
        ),
        (
            "fixture_demo",
            "Promotion kit self-eval route",
            "docs/demo-promotion-kit.md",
            "`docs/productization-self-eval.md`",
        ),
    }
    assert checks <= {
        (check.category, check.name, check.path, check.needle)
        for check in module.CHECKS
    }


def test_demo_output_sharing_boundary_checks_are_grouped():
    module = _load_productization_self_eval_module()
    checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.DEMO_OUTPUT_SHARING_BOUNDARY_CHECKS
    }

    assert checks == {
        (
            "fixture_demo",
            "Deterministic demo sharing boundary",
            "docs/deterministic-demo.md",
            "Demo and MCP output are local evidence",
        ),
        (
            "fixture_demo",
            "Promotion kit sharing boundary",
            "docs/demo-promotion-kit.md",
            "Demo and MCP output are local evidence",
        ),
        (
            "fixture_demo",
            "Promotion kit external sharing approval",
            "docs/demo-promotion-kit.md",
            "External sharing still requires explicit user approval",
        ),
    }
    assert checks <= {
        (check.category, check.name, check.path, check.needle)
        for check in module.CHECKS
    }


def test_productization_self_eval_checks_demo_promotion_feature_proposal_boundary():
    module = _load_productization_self_eval_module()
    checks = {
        (check.path, check.needle)
        for check in module.DEMO_PROMOTION_FEATURE_PROPOSAL_BOUNDARY_CHECKS
    }

    assert checks == {
        ("docs/demo-promotion-kit.md", "feature proposal"),
        ("docs/demo-promotion-kit.md", "approval to implement runtime behavior"),
        ("docs/demo-promotion-kit.md", "`CONTRIBUTING.md`"),
        ("docs/demo-promotion-kit.md", "`docs/productization-self-eval.md`"),
    }
    assert checks <= {(check.path, check.needle) for check in module.CHECKS}


def test_demo_docs_clarify_output_is_not_external_sharing_authorization():
    for relative_path in ("docs/deterministic-demo.md", "docs/demo-promotion-kit.md"):
        doc = " ".join((ROOT / relative_path).read_text(encoding="utf-8").split())

        for expected in (
            "Demo and MCP output are local evidence, not permission to publish or share results.",
            "External sharing still requires explicit user approval.",
        ):
            assert expected in doc, f"{relative_path} missing {expected!r}"


def test_productization_self_eval_checks_demo_output_sharing_boundary():
    module = _load_productization_self_eval_module()
    checks = {
        (check.path, check.needle)
        for check in module.DEMO_OUTPUT_SHARING_BOUNDARY_CHECKS
    }

    assert checks == {
        ("docs/deterministic-demo.md", "Demo and MCP output are local evidence"),
        ("docs/demo-promotion-kit.md", "Demo and MCP output are local evidence"),
        ("docs/demo-promotion-kit.md", "External sharing still requires explicit user approval"),
    }
    assert checks <= {(check.path, check.needle) for check in module.CHECKS}


def test_demo_docs_open_with_fixture_only_no_live_desktop_no_upload_boundary():
    for relative_path in ("docs/quick-demo.md", "docs/deterministic-demo.md"):
        doc = (ROOT / relative_path).read_text(encoding="utf-8")
        intro = doc.split("\n## ", 1)[0]
        normalized = " ".join(intro.split())

        for expected in (
            "fixture-only",
            "does not read the live desktop",
            "does not upload content",
        ):
            assert expected in normalized, f"{relative_path} missing {expected!r}"


def test_windows_first_run_opens_with_safe_demo_and_dry_run_boundaries():
    doc = (ROOT / "docs" / "windows-first-run.md").read_text(encoding="utf-8")
    intro = doc.split("\n## Install And Check", 1)[0]
    normalized = " ".join(intro.split())

    for expected in (
        "fixture-only",
        "does not read the live desktop",
        "does not upload content",
        "The dry-runs only print instructions or config snippets.",
    ):
        assert expected in normalized


def test_first_run_safe_boundary_checks_are_grouped():
    module = _load_productization_self_eval_module()
    checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.FIRST_RUN_SAFE_BOUNDARY_CHECKS
    }

    assert checks == {
        (
            "first_screen",
            "First-run fixture-only demo",
            "docs/windows-first-run.md",
            "fixture-only",
        ),
        (
            "first_screen",
            "First-run no live desktop read",
            "docs/windows-first-run.md",
            "does not read the live desktop",
        ),
        (
            "first_screen",
            "First-run no content upload",
            "docs/windows-first-run.md",
            "does not upload content",
        ),
        (
            "first_screen",
            "First-run dry-run print-only",
            "docs/windows-first-run.md",
            "The dry-runs only print instructions or config snippets.",
        ),
    }
    assert checks <= {
        (check.category, check.name, check.path, check.needle)
        for check in module.CHECKS
    }


def test_productization_self_eval_checks_windows_first_run_boundaries():
    module = _load_productization_self_eval_module()
    checks = {
        (check.path, check.needle)
        for check in module.FIRST_RUN_SAFE_BOUNDARY_CHECKS
    }

    assert checks == {
        ("docs/windows-first-run.md", "fixture-only"),
        ("docs/windows-first-run.md", "does not read the live desktop"),
        ("docs/windows-first-run.md", "does not upload content"),
        (
            "docs/windows-first-run.md",
            "The dry-runs only print instructions or config snippets.",
        ),
    }
    assert checks <= {(check.path, check.needle) for check in module.CHECKS}


def test_productization_self_eval_checks_windows_first_run_workday_boundaries():
    module = _load_productization_self_eval_module()
    checks = {
        (check.path, check.needle)
        for check in module.WORKDAY_ENTRYPOINT_BOUNDARY_CHECKS
    }

    for expected in (
        ("docs/windows-first-run.md", module.WORKDAY_RECORD_ONLY_TEXT),
        ("docs/windows-first-run.md", module.WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT),
        ("docs/windows-first-run.md", module.WORKDAY_NO_RAW_OBSERVED_TEXT),
    ):
        assert expected in checks


def test_workday_guide_opens_with_record_only_summary_level_boundary():
    doc = (ROOT / "docs" / "codex-app-workday-guide.md").read_text(encoding="utf-8")
    intro = doc.split("\n## Setup", 1)[0]
    normalized = " ".join(intro.split())

    for expected in (
        "record-only",
        "summary-level evidence",
        "does not send raw observed text",
    ):
        assert expected in normalized


def test_workday_plugin_doc_opens_with_record_only_summary_level_boundary():
    doc = (ROOT / "docs" / "codex-workday-plugin.md").read_text(encoding="utf-8")
    intro = doc.split("\n## Workday Plugin, MCP, Or Development Thread?", 1)[0]
    normalized = " ".join(intro.split())

    for expected in (
        "record-only",
        "summary-level evidence",
        "does not send raw observed text",
    ):
        assert expected in normalized


def test_productization_self_eval_checks_workday_guide_boundaries():
    module = _load_productization_self_eval_module()
    checks = {
        (check.path, check.needle)
        for check in module.WORKDAY_ENTRYPOINT_BOUNDARY_CHECKS
    }

    for expected in (
        ("docs/codex-app-workday-guide.md", module.WORKDAY_RECORD_ONLY_TEXT),
        ("docs/codex-app-workday-guide.md", module.WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT),
        ("docs/codex-app-workday-guide.md", module.WORKDAY_NO_RAW_OBSERVED_TEXT),
    ):
        assert expected in checks


def test_productization_self_eval_checks_workday_plugin_boundaries():
    module = _load_productization_self_eval_module()
    checks = {
        (check.path, check.needle)
        for check in module.WORKDAY_ENTRYPOINT_BOUNDARY_CHECKS
    }

    for expected in (
        ("docs/codex-workday-plugin.md", module.WORKDAY_RECORD_ONLY_TEXT),
        ("docs/codex-workday-plugin.md", module.WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT),
        ("docs/codex-workday-plugin.md", module.WORKDAY_NO_RAW_OBSERVED_TEXT),
    ):
        assert expected in checks


def test_productization_self_eval_checks_plugin_install_boundaries():
    module = _load_productization_self_eval_module()
    checks = {
        (check.path, check.needle)
        for check in module.WORKDAY_ENTRYPOINT_BOUNDARY_CHECKS
    }

    for expected in (
        ("docs/codex-app-plugin-install.md", module.WORKDAY_RECORD_ONLY_TEXT),
        ("docs/codex-app-plugin-install.md", module.WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT),
        ("docs/codex-app-plugin-install.md", module.WORKDAY_NO_RAW_OBSERVED_TEXT),
    ):
        assert expected in checks


def test_mcp_metadata_only_public_sharing_boundary_checks_are_grouped():
    module = _load_productization_self_eval_module()
    checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.MCP_METADATA_ONLY_PUBLIC_SHARING_BOUNDARY_CHECKS
    }

    assert checks == {
        (
            "codex_entry",
            "MCP metadata-only public sharing boundary",
            "docs/mcp-client-setup.md",
            "Metadata-only mode is not permission to publish MCP results",
        ),
        (
            "codex_entry",
            "MCP external sharing approval boundary",
            "docs/mcp-client-setup.md",
            "External sharing still requires explicit user approval",
        ),
    }
    assert checks <= {
        (check.category, check.name, check.path, check.needle)
        for check in module.CHECKS
    }


def test_productization_self_eval_checks_mcp_metadata_only_public_sharing_boundary():
    module = _load_productization_self_eval_module()
    checks = {
        (check.path, check.needle)
        for check in module.MCP_METADATA_ONLY_PUBLIC_SHARING_BOUNDARY_CHECKS
    }

    assert checks == {
        (
            "docs/mcp-client-setup.md",
            "Metadata-only mode is not permission to publish MCP results",
        ),
        (
            "docs/mcp-client-setup.md",
            "External sharing still requires explicit user approval",
        ),
    }
    assert checks <= {(check.path, check.needle) for check in module.CHECKS}


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


def test_readme_points_contributors_to_task_classification_before_changes():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    normalized = " ".join(readme.split())

    for expected in (
        "Before opening a contribution, classify the task with `CONTRIBUTING.md` and the review entry checks in `docs/productization-self-eval.md`.",
        "Use the stricter path when the work touches privacy, MCP output, release evidence, runtime behavior, or capture surfaces.",
    ):
        assert expected in normalized


def test_readme_zh_points_contributors_to_task_classification_before_changes():
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    normalized = " ".join(readme_zh.split())

    for expected in (
        "提交贡献前，先用 `CONTRIBUTING.md` 和 `docs/productization-self-eval.md` 的 review entry checks 给任务分类。",
        "如果工作涉及隐私、MCP 输出、发布证据、运行时行为或采集面，走更严格路径。",
    ):
        assert expected in normalized


def test_readme_zh_links_to_contributing_task_classification_rules():
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    normalized = " ".join(readme_zh.split())

    assert (
        "完整分类规则见 [CONTRIBUTING.md](CONTRIBUTING.md) 的 `Task Classification` / `中文速览`。"
        in normalized
    )


def test_contributor_readme_classification_checks_are_grouped():
    module = _load_productization_self_eval_module()
    checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.CONTRIBUTOR_README_CLASSIFICATION_CHECKS
    }

    assert checks == {
        (
            "contributor_entry",
            "English README task classification entry",
            "README.md",
            "classify the task with `CONTRIBUTING.md`",
        ),
        (
            "contributor_entry",
            "English README self-eval entry",
            "README.md",
            "`docs/productization-self-eval.md`",
        ),
        (
            "contributor_entry",
            "Chinese README contributing link",
            "README.zh-CN.md",
            "[CONTRIBUTING.md](CONTRIBUTING.md)",
        ),
        (
            "contributor_entry",
            "Chinese README summary entrypoint",
            "README.zh-CN.md",
            "`Task Classification` / `中文速览`",
        ),
    }
    assert checks <= {
        (check.category, check.name, check.path, check.needle)
        for check in module.CHECKS
    }


def test_productization_self_eval_checks_readme_zh_contributing_summary_link():
    module = _load_productization_self_eval_module()
    checks = {
        (check.path, check.needle)
        for check in module.CONTRIBUTOR_README_CLASSIFICATION_CHECKS
    }

    assert {
        ("README.zh-CN.md", "`Task Classification` / `中文速览`"),
        ("README.zh-CN.md", "[CONTRIBUTING.md](CONTRIBUTING.md)"),
    } <= checks
    assert checks <= {(check.path, check.needle) for check in module.CHECKS}


def test_productization_self_eval_checks_readme_contributor_classification_entry():
    module = _load_productization_self_eval_module()
    checks = {
        (check.path, check.needle)
        for check in module.CONTRIBUTOR_README_CLASSIFICATION_CHECKS
    }

    assert {
        ("README.md", "classify the task with `CONTRIBUTING.md`"),
        ("README.md", "`docs/productization-self-eval.md`"),
    } <= checks
    assert checks <= {(check.path, check.needle) for check in module.CHECKS}


def test_productization_self_eval_docs_explain_review_entry_checks():
    doc = (ROOT / "docs" / "productization-self-eval.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "## Review Entry Checks",
        "Use this section when README, demo, Codex entry, contribution path, or safety claims change.",
        "Feature proposal: use for product-facing ideas or developer-experience ideas before implementation; it classifies the idea but does not approve implementation.",
        "Harness-first task: use for deterministic docs, fixtures, tests, scorecards, CI, or compatible metadata inside the current baseline; include expected validation commands.",
        "Privacy-boundary review: use before implementation when work touches capture surfaces, observed content, storage, MCP output, memory output, redaction, or release evidence; include MCP output impact when relevant.",
        "Pull request template: use at PR time to confirm validation, Product CLI/MCP shape changes, prohibited surfaces, observed-content artifacts, and MCP schema guardrails.",
        "If the correct entry is unclear, choose the stricter review path before changing runtime behavior.",
    ):
        assert expected in normalized


def test_productization_self_eval_docs_explain_stable_text_output_contract():
    doc = (ROOT / "docs" / "productization-self-eval.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "## Stable Text Output",
        "The text output is a reader-facing contract for contributors and release notes.",
        "`Categories:` uses this canonical order: `codex_entry`, `contributor_entry`, `first_screen`, `fixture_demo`, `overclaim_risk`, `privacy_boundary`.",
        "Unknown future categories append after the known order so new checks do not reorder existing report lines.",
        "`Boundary:` uses this canonical order: `does_not_run_live_uia`, `does_not_read_desktop`, `does_not_capture_observed_content`, `checks_public_docs_and_static_metadata_only`.",
        "When adding a category or boundary flag, update the canonical order constants and focused text-output tests before changing report wording.",
    ):
        assert expected in normalized


def test_productization_self_eval_docs_explain_json_provenance_contract():
    doc = (ROOT / "docs" / "productization-self-eval.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "## JSON Provenance",
        "`--format json` includes `provenance.checked_root` and `provenance.checked_paths`",
        "`provenance.checked_root` is a local audit pointer to the repository root passed to the self-eval.",
        "do not treat JSON output as permission to publish or externally share local evidence.",
        "`provenance.checked_paths` lists the fixed repository-relative docs and static metadata paths checked by the scorecard.",
        "It is not an arbitrary file inventory",
        "it does not authorize live UIA, desktop reads, observed content capture, LLM calls, upload, or local state changes.",
    ):
        assert expected in normalized


def test_productization_self_eval_docs_explain_json_payload_contract():
    doc = (ROOT / "docs" / "productization-self-eval.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "## JSON Contract",
        "`--format json` is a local automation contract for the self-eval scorecard.",
        "The current payload uses `schema_version = 1`.",
        "Keep these top-level keys stable: `schema_version`, `name`, `score`, `threshold`, `passed`, `categories`, `failed_items`, `next_actions`, `provenance`, and `boundary`.",
        "change the schema version and focused JSON contract tests before renaming or removing fields",
    ):
        assert expected in normalized


def test_productization_self_eval_docs_explain_json_failure_contract():
    doc = (ROOT / "docs" / "productization-self-eval.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "## JSON Failure Contract",
        "Failure JSON keeps the same `schema_version`, `provenance`, and `boundary` fields as passing JSON.",
        "`failed_items` identifies the missing or overclaiming check",
        "`next_actions` keeps the next local repair step machine-readable.",
        "Do not snapshot absolute `checked_root` paths in tests or docs",
    ):
        assert expected in normalized


def test_productization_self_eval_docs_explain_failed_item_format_contract():
    doc = (ROOT / "docs" / "productization-self-eval.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "## Failed Item Format",
        "`failed_items` entries use `category: name (path: reason)`.",
        "The format is intentionally compact so automation can split the category, check name, source path, and reason without reading free-form prose.",
        "When changing this string, update `FAILED_ITEM_FORMAT` and focused failed-item format tests before changing output code.",
    ):
        assert expected in normalized


def test_productization_self_eval_docs_explain_next_actions_contract():
    doc = (ROOT / "docs" / "productization-self-eval.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "## Next Actions Contract",
        "`next_actions` is a small stable action vocabulary for local automation.",
        "Passing runs use the three `PASSING_NEXT_ACTIONS` entries.",
        "Missing-file failures prepend `MISSING_FILE_NEXT_ACTION` before `GENERIC_FAILURE_NEXT_ACTIONS`.",
        "Other failures return only `GENERIC_FAILURE_NEXT_ACTIONS`.",
        "When changing this vocabulary, update `PASSING_NEXT_ACTIONS`, `MISSING_FILE_NEXT_ACTION`, `GENERIC_FAILURE_NEXT_ACTIONS`, and focused next-actions tests before changing output code.",
    ):
        assert expected in normalized


def test_productization_self_eval_docs_explain_score_contract():
    doc = (ROOT / "docs" / "productization-self-eval.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "## Score Contract",
        "`score` and category scores use `round(100 * passed / total)`.",
        "The numerator is passed checks and the denominator is total checks at the same scope.",
        "When changing score semantics, update `SCORE_FORMULA`, `_percentage_score`, and focused score contract tests before changing output code.",
    ):
        assert expected in normalized


def test_productization_self_eval_docs_explain_pass_contract():
    doc = (ROOT / "docs" / "productization-self-eval.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "## Pass Contract",
        "`passed` is true only when `score >= threshold` and `failed_items` is empty.",
        "A high score with any failed item still fails the gate, and a clean run below threshold also fails.",
        "When changing pass semantics, update `PASS_CONDITION`, `_passes_gate`, and focused pass contract tests before changing output code.",
    ):
        assert expected in normalized


def test_productization_self_eval_docs_explain_threshold_contract():
    doc = (ROOT / "docs" / "productization-self-eval.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "## Threshold Contract",
        "`DEFAULT_THRESHOLD` is 90.",
        "`threshold` is an integer percentage from 0 to 100.",
        "Programmatic callers must pass a real `int`; `bool`, `float`, `str`, and `None` are rejected.",
        "CLI `--threshold` rejects values outside this range before evaluation.",
        "`CLI_ERROR_EXIT_CODE` is 2.",
        "CLI threshold errors use `CLI_THRESHOLD_RANGE_ERROR` or `CLI_THRESHOLD_INTEGER_ERROR`.",
        "CLI threshold errors do not emit a JSON payload or traceback.",
        "When changing threshold semantics, update `THRESHOLD_RANGE`, `CLI_ERROR_EXIT_CODE`, `CLI_THRESHOLD_RANGE_ERROR`, `CLI_THRESHOLD_INTEGER_ERROR`, `_validate_threshold`, `_parse_threshold`, and focused threshold contract tests before changing output code.",
    ):
        assert expected in normalized


def test_productization_self_eval_docs_explain_root_argument_contract():
    doc = (ROOT / "docs" / "productization-self-eval.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "## Root Argument Contract",
        "`--root` is a hidden local test override.",
        "`ROOT_ARGUMENT_CONTRACT` is `existing directory used as local self-eval root`.",
        "CLI root errors use `CLI_ROOT_PATH_ERROR`.",
        "Invalid root paths do not emit a JSON payload or traceback.",
        "Existing roots with missing checked paths are self-eval failures, not CLI argument errors.",
        "When changing root semantics, update `ROOT_ARGUMENT_CONTRACT`, `CLI_ROOT_PATH_ERROR`, `_parse_root`, and focused root argument tests before changing output code.",
    ):
        assert expected in normalized


def test_productization_self_eval_reports_missing_stable_text_output_contract(tmp_path):
    module = _load_productization_self_eval_module()
    _copy_self_eval_check_files(module, tmp_path)

    doc = tmp_path / "docs" / "productization-self-eval.md"
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text(
        (ROOT / "docs" / "productization-self-eval.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    doc.write_text(
        doc.read_text(encoding="utf-8").replace(
            "## Stable Text Output",
            "## Output Notes",
        ),
        encoding="utf-8",
    )

    payload = module.evaluate(root=tmp_path)

    assert payload["passed"] is False
    assert (
        "contributor_entry: Self-eval stable text output heading "
        "(docs/productization-self-eval.md: required phrase missing)"
    ) in payload["failed_items"]
    assert payload["categories"]["contributor_entry"] < 100


def test_productization_self_eval_reports_stable_text_output_order_drift(tmp_path):
    module = _load_productization_self_eval_module()

    cases = (
        (
            "category",
            "`Categories:` uses this canonical order: `codex_entry`, `contributor_entry`,\n`first_screen`, `fixture_demo`, `overclaim_risk`, `privacy_boundary`.",
            "`Categories:` uses this canonical order: `first_screen`, `contributor_entry`,\n`codex_entry`, `fixture_demo`, `overclaim_risk`, `privacy_boundary`.",
            "contributor_entry: Self-eval stable text output category order "
            "(docs/productization-self-eval.md: canonical order mismatch)",
        ),
        (
            "boundary",
            "`Boundary:` uses this canonical order: `does_not_run_live_uia`,\n`does_not_read_desktop`, `does_not_capture_observed_content`,\n`checks_public_docs_and_static_metadata_only`.",
            "`Boundary:` uses this canonical order: `does_not_read_desktop`,\n`does_not_run_live_uia`, `does_not_capture_observed_content`,\n`checks_public_docs_and_static_metadata_only`.",
            "contributor_entry: Self-eval stable text output boundary order "
            "(docs/productization-self-eval.md: canonical order mismatch)",
        ),
    )

    for case_name, original, replacement, expected_failure in cases:
        case_root = tmp_path / case_name
        _copy_self_eval_check_files(module, case_root)
        doc = case_root / "docs" / "productization-self-eval.md"
        text = doc.read_text(encoding="utf-8")
        assert original in text
        doc.write_text(text.replace(original, replacement), encoding="utf-8")

        payload = module.evaluate(root=case_root)

        assert payload["passed"] is False
        assert expected_failure in payload["failed_items"]
        assert payload["categories"]["contributor_entry"] < 100


def test_productization_self_eval_cli_text_reports_order_drift_with_boundary(tmp_path):
    module = _load_productization_self_eval_module()
    case_root = tmp_path / "cli-order-drift"
    _copy_self_eval_check_files(module, case_root)

    doc = case_root / "docs" / "productization-self-eval.md"
    text = doc.read_text(encoding="utf-8")
    doc.write_text(
        text.replace(
            "`Categories:` uses this canonical order: `codex_entry`, `contributor_entry`,\n`first_screen`, `fixture_demo`, `overclaim_risk`, `privacy_boundary`.",
            "`Categories:` uses this canonical order: `first_screen`, `contributor_entry`,\n`codex_entry`, `fixture_demo`, `overclaim_risk`, `privacy_boundary`.",
        ),
        encoding="utf-8",
    )

    script = ROOT / "harness" / "scripts" / "run_productization_self_eval.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--root", str(case_root), "--format", "text"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    assert completed.returncode == 1, completed.stdout
    assert "Status: FAIL" in completed.stdout
    assert (
        "- contributor_entry: Self-eval stable text output category order "
        "(docs/productization-self-eval.md: canonical order mismatch)"
    ) in completed.stdout
    assert "Boundary:" in completed.stdout
    assert "- does_not_run_live_uia: true" in completed.stdout
    assert "- does_not_read_desktop: true" in completed.stdout
    assert "- does_not_capture_observed_content: true" in completed.stdout
    assert "- checks_public_docs_and_static_metadata_only: true" in completed.stdout


def test_productization_self_eval_cli_json_reports_order_drift_with_provenance(
    tmp_path,
):
    module = _load_productization_self_eval_module()
    case_root = tmp_path / "cli-json-order-drift"
    _copy_self_eval_check_files(module, case_root)

    doc = case_root / "docs" / "productization-self-eval.md"
    text = doc.read_text(encoding="utf-8")
    doc.write_text(
        text.replace(
            "`Boundary:` uses this canonical order: `does_not_run_live_uia`,\n`does_not_read_desktop`, `does_not_capture_observed_content`,\n`checks_public_docs_and_static_metadata_only`.",
            "`Boundary:` uses this canonical order: `does_not_read_desktop`,\n`does_not_run_live_uia`, `does_not_capture_observed_content`,\n`checks_public_docs_and_static_metadata_only`.",
        ),
        encoding="utf-8",
    )

    script = ROOT / "harness" / "scripts" / "run_productization_self_eval.py"
    completed = subprocess.run(
        [sys.executable, str(script), "--root", str(case_root), "--format", "json"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    assert completed.returncode == 1, completed.stdout
    payload = json.loads(completed.stdout)

    assert payload["passed"] is False
    assert (
        "contributor_entry: Self-eval stable text output boundary order "
        "(docs/productization-self-eval.md: canonical order mismatch)"
    ) in payload["failed_items"]
    assert payload["categories"]["contributor_entry"] < 100
    assert payload["boundary"] == {
        "does_not_run_live_uia": True,
        "does_not_read_desktop": True,
        "does_not_capture_observed_content": True,
        "checks_public_docs_and_static_metadata_only": True,
    }
    assert payload["provenance"] == {
        "checked_root": str(case_root),
        "checked_paths": sorted({check.path for check in module.CHECKS}),
    }


def test_productization_self_eval_docs_explain_readme_contributor_entry_guards():
    doc = (ROOT / "docs" / "productization-self-eval.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "The `contributor_entry` category also guards both README contributor entrypoints.",
        "`README.md` must point contributors to `CONTRIBUTING.md` and `docs/productization-self-eval.md`.",
        "`README.zh-CN.md` must point contributors to `CONTRIBUTING.md` and the `Task Classification` / `中文速览` labels.",
    ):
        assert expected in normalized


def test_productization_self_eval_docs_explain_contributor_template_required_intake_checks():
    doc = (ROOT / "docs" / "productization-self-eval.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "## Contributor Required Intake Checks",
        "The `contributor_entry` category guards the Required Intake sentence in `.github/pull_request_template.md`, `.github/ISSUE_TEMPLATE/harness_first_task.yml`, `.github/ISSUE_TEMPLATE/feature_proposal.yml`, and `.github/ISSUE_TEMPLATE/privacy_boundary_review.yml`.",
        "Before implementation, read `AGENTS.md`, `docs/roadmap.md`, `README.md`, `docs/codex-long-term-goal.md`, and the files, tests, fixtures, schemas, scorecards, or docs affected by the task.",
        "`CONTRIBUTOR_TEMPLATE_INTAKE_CHECKS`",
        "`PR required intake`",
        "`Harness issue required intake`",
        "`Feature proposal required intake`",
        "`Privacy review required intake`",
        "The same category guards the long-term-goal authorization boundary in `CONTRIBUTING.md`, `.github/pull_request_template.md`, `.github/ISSUE_TEMPLATE/harness_first_task.yml`, `.github/ISSUE_TEMPLATE/feature_proposal.yml`, and `.github/ISSUE_TEMPLATE/privacy_boundary_review.yml`.",
        "Reading `docs/codex-long-term-goal.md` gives direction only; it is not release authorization, not automatic maintenance authorization, and not approval for broad evidence sweeps, release or publish actions, or capture-surface expansion.",
        "`CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_CHECKS`",
        "This is a static docs and metadata check; it does not run live UIA, read the desktop, or capture observed content.",
    ):
        assert expected in normalized


def test_project_presentation_good_first_issue_themes_route_to_task_classification():
    doc = (ROOT / "docs" / "project-presentation.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "Before turning any theme into an issue, classify it with `CONTRIBUTING.md` and `docs/productization-self-eval.md`.",
        "Use the stricter path when work touches privacy, MCP output, release evidence, runtime behavior, or capture surfaces.",
    ):
        assert expected in normalized


def test_project_presentation_classification_checks_are_grouped():
    module = _load_productization_self_eval_module()
    checks = {
        (check.category, check.name, check.path, check.needle)
        for check in module.PROJECT_PRESENTATION_CLASSIFICATION_CHECKS
    }

    assert checks == {
        (
            "contributor_entry",
            "Project presentation classification link",
            "docs/project-presentation.md",
            "classify it with `CONTRIBUTING.md`",
        ),
        (
            "contributor_entry",
            "Project presentation self-eval link",
            "docs/project-presentation.md",
            "`docs/productization-self-eval.md`",
        ),
        (
            "contributor_entry",
            "Project presentation stricter path",
            "docs/project-presentation.md",
            "Use the stricter path when work touches privacy",
        ),
    }
    assert checks <= {
        (check.category, check.name, check.path, check.needle)
        for check in module.CHECKS
    }


def test_productization_self_eval_checks_project_presentation_task_classification():
    module = _load_productization_self_eval_module()
    checks = {
        (check.path, check.needle)
        for check in module.PROJECT_PRESENTATION_CLASSIFICATION_CHECKS
    }

    assert checks == {
        ("docs/project-presentation.md", "classify it with `CONTRIBUTING.md`"),
        ("docs/project-presentation.md", "`docs/productization-self-eval.md`"),
        (
            "docs/project-presentation.md",
            "Use the stricter path when work touches privacy",
        ),
    }
    assert checks <= {(check.path, check.needle) for check in module.CHECKS}


def test_productization_self_eval_docs_explain_workday_entrypoint_consistency():
    doc = (ROOT / "docs" / "productization-self-eval.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "## Codex Workday Entrypoint Consistency",
        "`README.md`",
        "`README.zh-CN.md` is the localized README mirror and shares the same Workday boundary guard.",
        "`docs/windows-first-run.md`",
        "`docs/codex-app-plugin-install.md`",
        "`docs/codex-app-workday-guide.md`",
        "`docs/codex-workday-plugin.md`",
        "record-only",
        "summary-level evidence",
        "does not send raw observed text",
        "`summary_boundary`",
        "not a telemetry or log-counter report",
        "不是遥测或日志计数报告",
        "Do not inspect, scan, review, edit, test, commit, push, or release repository files.",
        "The self-eval also checks `CONTRIBUTING.md` so contributors see this rule before changing a Codex Workday entrypoint.",
        "When `README.md` or `README.zh-CN.md` changes, run `python -m pytest tests/test_readme_daily_workflow.py -q` with the self-eval JSON gate.",
        "python harness/scripts/run_productization_self_eval.py --format json",
    ):
        assert expected in normalized


def test_contributing_routes_tasks_before_implementation():
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    normalized = " ".join(contributing.split())

    assert "## Task Classification" in contributing
    for expected in (
        "Before opening an issue or pull request, classify the work:",
        "`Recording-only Workday operation`",
        "Use the Workday plugin or CLI and do not inspect repository files",
        "`Harness-first task`",
        "Use the harness-first task template",
        "`Privacy-boundary review`",
        "Open a privacy boundary review issue before implementation",
        "`Human product decision`",
        "Do not implement until explicit human product approval defines the scope",
        "If the classification is unclear, choose the stricter path.",
    ):
        assert expected in normalized


def test_contributing_points_codex_workday_entry_changes_to_consistency_check():
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    normalized = " ".join(contributing.split())

    for expected in (
        "If you change a Codex Workday entrypoint, keep the five-entrypoint consistency rule in `docs/productization-self-eval.md` in sync.",
        "`README.md`",
        "`docs/windows-first-run.md`",
        "`docs/codex-app-plugin-install.md`",
        "`docs/codex-app-workday-guide.md`",
        "`docs/codex-workday-plugin.md`",
        "record-only",
        "summary-level evidence",
        "does not send raw observed text",
        "When `README.md` or `README.zh-CN.md` Workday guidance changes, include `python -m pytest tests/test_readme_daily_workflow.py -q` and `python harness/scripts/run_productization_self_eval.py --format json` in validation.",
        "改 Codex Workday 入口时，同步检查 `docs/productization-self-eval.md` 的 five-entrypoint consistency 规则。",
    ):
        assert expected in normalized


def test_productization_self_eval_checks_contributing_workday_consistency_rule():
    module = _load_productization_self_eval_module()
    checks = {
        (check.category, check.path, check.needle)
        for check in module.WORKDAY_CONTRIBUTING_CONSISTENCY_CHECKS
    }
    expected = {
        ("contributor_entry", "CONTRIBUTING.md", "five-entrypoint consistency"),
        ("contributor_entry", "CONTRIBUTING.md", "`docs/productization-self-eval.md`"),
        ("contributor_entry", "CONTRIBUTING.md", "`README.md`"),
        ("contributor_entry", "CONTRIBUTING.md", "`docs/windows-first-run.md`"),
        ("contributor_entry", "CONTRIBUTING.md", "`docs/codex-app-plugin-install.md`"),
        ("contributor_entry", "CONTRIBUTING.md", "`docs/codex-app-workday-guide.md`"),
        ("contributor_entry", "CONTRIBUTING.md", "`docs/codex-workday-plugin.md`"),
        ("contributor_entry", "CONTRIBUTING.md", module.WORKDAY_RECORD_ONLY_TEXT),
        (
            "contributor_entry",
            "CONTRIBUTING.md",
            module.WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT,
        ),
        ("contributor_entry", "CONTRIBUTING.md", module.WORKDAY_NO_RAW_OBSERVED_TEXT),
        ("contributor_entry", "CONTRIBUTING.md", "tests/test_readme_daily_workflow.py -q"),
        ("contributor_entry", "CONTRIBUTING.md", "run_productization_self_eval.py --format json"),
        (
            "contributor_entry",
            "CONTRIBUTING.md",
            "若修改 `README.md` 或 `README.zh-CN.md` 的 Workday guidance",
        ),
    }

    assert checks == expected
    assert checks <= {
        (check.category, check.path, check.needle) for check in module.CHECKS
    }


def test_contributing_includes_chinese_task_classification_summary():
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    normalized = " ".join(contributing.split())

    for expected in (
        "### 中文速览",
        "中文贡献者也应先分类：",
        "只记录工作：使用 Workday plugin 或 CLI，不检查仓库文件、编辑代码、运行测试、提交、推送或发布。",
        "Harness-first task：仅限当前 baseline 内的 deterministic docs、fixtures、tests、scorecards、CI 或兼容 metadata。",
        "Privacy-boundary review：涉及 capture surfaces、observed content、storage、MCP output、memory output、redaction 或 release evidence 的提案，先开隐私边界 review。",
        "Human product decision：运行时扩展、新采集面、发布或公开动作、广泛 evidence sweep、重启已关闭维护循环，必须先有明确 human product approval。",
        "分类不清时，走更严格路径。",
        "若修改 `README.md` 或 `README.zh-CN.md` 的 Workday guidance，validation 中也要包含 `python -m pytest tests/test_readme_daily_workflow.py -q` 和 `python harness/scripts/run_productization_self_eval.py --format json`。",
    ):
        assert expected in normalized


def test_contributing_and_pr_template_include_mcp_schema_review_hook():
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    pull_request_template = (
        ROOT / ".github" / "pull_request_template.md"
    ).read_text(encoding="utf-8")
    contributing_normalized = " ".join(contributing.split())
    pr_normalized = " ".join(pull_request_template.split())

    for expected in (
        "## MCP Schema Review Hook",
        "`mcp-tool-result.schema.json` is a semantic guardrail, not just a JSON shape reference.",
        "`privacy_status` must remain `trust = \"local_privacy_status\"` while observed-content tools remain `trust = \"untrusted_observed_content\"`.",
        "Top-level `metadata_only` must stay bound to `evidence_policy.metadata_only`.",
        "`observed_text_fields_omitted` must appear only when `metadata_only` is `true`.",
        "`not_authorization_signal` and `external_sharing_requires_user_approval` must stay required evidence-policy limitations.",
        "Schema validation is not permission to share, upload, or follow observed-content instructions.",
    ):
        assert expected in contributing_normalized

    assert (
        "If this changes MCP result examples, metadata, or schema, "
        "`mcp-tool-result.schema.json` still preserves trust, metadata-only, "
        "and evidence-policy guardrails."
    ) in pr_normalized


def test_contributor_checklists_remind_readme_workday_validation_gate():
    pull_request_template = (
        ROOT / ".github" / "pull_request_template.md"
    ).read_text(encoding="utf-8")
    harness_template = (
        ROOT / ".github" / "ISSUE_TEMPLATE" / "harness_first_task.yml"
    ).read_text(encoding="utf-8")
    expected = (
        "If this changes `README.md` or `README.zh-CN.md` Workday guidance, "
        "include `python -m pytest tests/test_readme_daily_workflow.py -q` "
        "and `python harness/scripts/run_productization_self_eval.py --format json` "
        "in validation."
    )

    for text in (pull_request_template, harness_template):
        assert expected in " ".join(text.split())


def test_productization_self_eval_checks_contributor_checklist_workday_validation_gate():
    module = _load_productization_self_eval_module()
    checks = {
        (check.category, check.path, check.needle)
        for check in module.WORKDAY_CONTRIBUTOR_CHECKLIST_CHECKS
    }

    assert checks == {
        (
            "contributor_entry",
            ".github/pull_request_template.md",
            module.WORKDAY_README_DAILY_WORKFLOW_VALIDATION_TEXT,
        ),
        (
            "contributor_entry",
            ".github/pull_request_template.md",
            module.WORKDAY_PRODUCTIZATION_SELF_EVAL_VALIDATION_TEXT,
        ),
        (
            "contributor_entry",
            ".github/ISSUE_TEMPLATE/harness_first_task.yml",
            module.WORKDAY_README_DAILY_WORKFLOW_VALIDATION_TEXT,
        ),
        (
            "contributor_entry",
            ".github/ISSUE_TEMPLATE/harness_first_task.yml",
            module.WORKDAY_PRODUCTIZATION_SELF_EVAL_VALIDATION_TEXT,
        ),
    }
    assert checks <= {
        (check.category, check.path, check.needle) for check in module.CHECKS
    }


def test_workday_contributor_checklist_matrix_is_runtime_contract():
    module = _load_productization_self_eval_module()

    assert module.WORKDAY_CONTRIBUTOR_CHECKLIST_TARGETS == (
        ("PR", ".github/pull_request_template.md"),
        ("Harness issue", ".github/ISSUE_TEMPLATE/harness_first_task.yml"),
    )
    assert module.WORKDAY_CONTRIBUTOR_CHECKLIST_VALIDATIONS == (
        (
            "README daily workflow validation",
            module.WORKDAY_README_DAILY_WORKFLOW_VALIDATION_TEXT,
        ),
        (
            "self-eval JSON validation",
            module.WORKDAY_PRODUCTIZATION_SELF_EVAL_VALIDATION_TEXT,
        ),
    )
    assert tuple(
        (check.name, check.path, check.needle)
        for check in module.WORKDAY_CONTRIBUTOR_CHECKLIST_CHECKS
    ) == tuple(
        (f"{target_name} Workday {validation_name}", path, validation_text)
        for target_name, path in module.WORKDAY_CONTRIBUTOR_CHECKLIST_TARGETS
        for validation_name, validation_text in module.WORKDAY_CONTRIBUTOR_CHECKLIST_VALIDATIONS
    )


def test_contributor_template_intake_checks_reuse_single_constant():
    module = _load_productization_self_eval_module()
    required = (
        "Before implementation, read `AGENTS.md`, `docs/roadmap.md`, "
        "`README.md`, `docs/codex-long-term-goal.md`, and the files, tests, "
        "fixtures, schemas, scorecards, or docs affected by the task."
    )

    assert module.CONTRIBUTOR_TEMPLATE_INTAKE_TEXT == required
    assert {
        check.needle for check in module.CONTRIBUTOR_TEMPLATE_INTAKE_CHECKS
    } == {module.CONTRIBUTOR_TEMPLATE_INTAKE_TEXT}


def test_contributor_template_intake_targets_are_runtime_contract():
    module = _load_productization_self_eval_module()

    assert module.CONTRIBUTOR_TEMPLATE_INTAKE_TARGETS == (
        ("PR required intake", ".github/pull_request_template.md"),
        (
            "Harness issue required intake",
            ".github/ISSUE_TEMPLATE/harness_first_task.yml",
        ),
        (
            "Feature proposal required intake",
            ".github/ISSUE_TEMPLATE/feature_proposal.yml",
        ),
        (
            "Privacy review required intake",
            ".github/ISSUE_TEMPLATE/privacy_boundary_review.yml",
        ),
    )
    assert tuple(
        (check.name, check.path)
        for check in module.CONTRIBUTOR_TEMPLATE_INTAKE_CHECKS
    ) == module.CONTRIBUTOR_TEMPLATE_INTAKE_TARGETS


def test_productization_self_eval_checks_contributor_long_term_goal_boundary():
    module = _load_productization_self_eval_module()
    required = (
        "Reading `docs/codex-long-term-goal.md` gives direction only; it is not "
        "release authorization, not automatic maintenance authorization, and "
        "not approval for broad evidence sweeps, release or publish actions, "
        "or capture-surface expansion."
    )
    checks = {
        (check.name, check.path, check.needle)
        for check in module.CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_CHECKS
    }

    assert checks == {
        (name, path, required)
        for name, path in module.CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_TARGETS
    }


def test_contributor_long_term_goal_boundary_checks_reuse_single_constant():
    module = _load_productization_self_eval_module()
    required = (
        "Reading `docs/codex-long-term-goal.md` gives direction only; it is not "
        "release authorization, not automatic maintenance authorization, and "
        "not approval for broad evidence sweeps, release or publish actions, "
        "or capture-surface expansion."
    )

    assert module.CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_TEXT == required
    assert {
        check.needle for check in module.CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_CHECKS
    } == {module.CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_TEXT}


def test_contributor_long_term_goal_boundary_targets_are_runtime_contract():
    module = _load_productization_self_eval_module()

    assert module.CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_TARGETS == (
        ("Contributing long-term goal boundary", "CONTRIBUTING.md"),
        ("PR long-term goal boundary", ".github/pull_request_template.md"),
        (
            "Harness issue long-term goal boundary",
            ".github/ISSUE_TEMPLATE/harness_first_task.yml",
        ),
        (
            "Feature proposal long-term goal boundary",
            ".github/ISSUE_TEMPLATE/feature_proposal.yml",
        ),
        (
            "Privacy review long-term goal boundary",
            ".github/ISSUE_TEMPLATE/privacy_boundary_review.yml",
        ),
    )
    assert tuple(
        (check.name, check.path)
        for check in module.CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_CHECKS
    ) == module.CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_TARGETS


def test_productization_self_eval_fails_when_contributor_template_intake_is_missing(
    tmp_path,
):
    module = _load_productization_self_eval_module()
    required = (
        "Before implementation, read `AGENTS.md`, `docs/roadmap.md`, "
        "`README.md`, `docs/codex-long-term-goal.md`, and the files, tests, "
        "fixtures, schemas, scorecards, or docs affected by the task."
    )
    cases = (
        (
            ".github/pull_request_template.md",
            (
                "Before implementation, read `AGENTS.md`, `docs/roadmap.md`, `README.md`,\n"
                "  `docs/codex-long-term-goal.md`, and the files, tests, fixtures, schemas,\n"
                "  scorecards, or docs affected by the task."
            ),
            "contributor_entry: PR required intake "
            "(.github/pull_request_template.md: required phrase missing)",
        ),
        (
            ".github/ISSUE_TEMPLATE/harness_first_task.yml",
            (
                "Before implementation, read `AGENTS.md`, `docs/roadmap.md`,\n"
                "        `README.md`, `docs/codex-long-term-goal.md`, and the files, tests,\n"
                "        fixtures, schemas, scorecards, or docs affected by the task."
            ),
            "contributor_entry: Harness issue required intake "
            "(.github/ISSUE_TEMPLATE/harness_first_task.yml: required phrase missing)",
        ),
        (
            ".github/ISSUE_TEMPLATE/feature_proposal.yml",
            (
                "Before implementation, read `AGENTS.md`, `docs/roadmap.md`,\n"
                "        `README.md`, `docs/codex-long-term-goal.md`, and the files, tests,\n"
                "        fixtures, schemas, scorecards, or docs affected by the task."
            ),
            "contributor_entry: Feature proposal required intake "
            "(.github/ISSUE_TEMPLATE/feature_proposal.yml: required phrase missing)",
        ),
        (
            ".github/ISSUE_TEMPLATE/privacy_boundary_review.yml",
            (
                "Before implementation, read `AGENTS.md`, `docs/roadmap.md`,\n"
                "        `README.md`, `docs/codex-long-term-goal.md`, and the files, tests,\n"
                "        fixtures, schemas, scorecards, or docs affected by the task."
            ),
            "contributor_entry: Privacy review required intake "
            "(.github/ISSUE_TEMPLATE/privacy_boundary_review.yml: required phrase missing)",
        ),
    )

    for relative_path, wrapped_phrase, expected_failure in cases:
        case_root = tmp_path / relative_path.replace("/", "_").replace(".", "_")
        _copy_self_eval_check_files(module, case_root)
        template = case_root / relative_path
        if not template.exists():
            template.parent.mkdir(parents=True, exist_ok=True)
            template.write_text(
                (ROOT / relative_path).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        text = template.read_text(encoding="utf-8")
        assert required in " ".join(text.split())
        assert wrapped_phrase in text
        template.write_text(text.replace(wrapped_phrase, ""), encoding="utf-8")

        payload = module.evaluate(root=case_root)

        assert payload["passed"] is False
        assert expected_failure in payload["failed_items"]
        assert payload["categories"]["contributor_entry"] < 100


def test_productization_self_eval_fails_when_contributor_long_term_boundary_is_missing(
    tmp_path,
):
    module = _load_productization_self_eval_module()
    required = (
        "Reading `docs/codex-long-term-goal.md` gives direction only; it is not "
        "release authorization, not automatic maintenance authorization, and "
        "not approval for broad evidence sweeps, release or publish actions, "
        "or capture-surface expansion."
    )
    cases = (
        (
            "CONTRIBUTING.md",
            "contributor_entry: Contributing long-term goal boundary "
            "(CONTRIBUTING.md: required phrase missing)",
        ),
        (
            ".github/pull_request_template.md",
            "contributor_entry: PR long-term goal boundary "
            "(.github/pull_request_template.md: required phrase missing)",
        ),
        (
            ".github/ISSUE_TEMPLATE/harness_first_task.yml",
            "contributor_entry: Harness issue long-term goal boundary "
            "(.github/ISSUE_TEMPLATE/harness_first_task.yml: required phrase missing)",
        ),
        (
            ".github/ISSUE_TEMPLATE/feature_proposal.yml",
            "contributor_entry: Feature proposal long-term goal boundary "
            "(.github/ISSUE_TEMPLATE/feature_proposal.yml: required phrase missing)",
        ),
        (
            ".github/ISSUE_TEMPLATE/privacy_boundary_review.yml",
            "contributor_entry: Privacy review long-term goal boundary "
            "(.github/ISSUE_TEMPLATE/privacy_boundary_review.yml: required phrase missing)",
        ),
    )

    for relative_path, expected_failure in cases:
        case_root = tmp_path / relative_path.replace("/", "_").replace(".", "_")
        _copy_self_eval_check_files(module, case_root)
        template = case_root / relative_path
        if not template.exists():
            template.parent.mkdir(parents=True, exist_ok=True)
            template.write_text(
                (ROOT / relative_path).read_text(encoding="utf-8"),
                encoding="utf-8",
            )
        text = template.read_text(encoding="utf-8")
        assert required in " ".join(text.split())
        template.write_text(text.replace("direction only", "direction-only"), encoding="utf-8")

        payload = module.evaluate(root=case_root)

        assert payload["passed"] is False
        assert expected_failure in payload["failed_items"]
        assert payload["categories"]["contributor_entry"] < 100


def test_feature_proposal_template_does_not_authorize_implementation():
    template = (
        ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_proposal.yml"
    ).read_text(encoding="utf-8")
    normalized = " ".join(template.split())

    for expected in (
        "Use this to discuss product-facing ideas before implementation.",
        "A feature proposal is not approval to implement.",
        "Reading `docs/codex-long-term-goal.md` gives direction only; it is not release authorization, not automatic maintenance authorization, and not approval for broad evidence sweeps, release or publish actions, or capture-surface expansion.",
        "If the idea is deterministic docs, tests, fixtures, scorecards, CI, or compatible metadata, use the harness-first task template instead.",
        "If the idea touches capture surfaces, observed content, storage, MCP output, memory output, redaction, or release evidence, open a privacy boundary review before implementation.",
        "Runtime expansion, new capture surfaces, release or publish actions, broad evidence sweeps, or continuation of the closed maintenance loop require explicit human product approval before implementation.",
        "This issue classifies the idea only; implementation starts only after the required harness-first task, privacy-boundary review, or explicit human product decision defines scope.",
    ):
        assert expected in normalized


def test_harness_and_privacy_templates_route_to_stricter_classifications():
    harness_template = (
        ROOT / ".github" / "ISSUE_TEMPLATE" / "harness_first_task.yml"
    ).read_text(encoding="utf-8")
    privacy_template = (
        ROOT / ".github" / "ISSUE_TEMPLATE" / "privacy_boundary_review.yml"
    ).read_text(encoding="utf-8")

    harness_normalized = " ".join(harness_template.split())
    privacy_normalized = " ".join(privacy_template.split())

    for expected in (
        "Use this for `Harness-first task` work.",
        "If the work is a product-facing idea rather than deterministic evidence work, use the feature proposal template.",
        "If the work touches capture surfaces, observed content, storage, MCP output, memory output, redaction, or release evidence, open a privacy boundary review before implementation.",
        "This template does not authorize runtime expansion, new capture surfaces, release or publish actions, broad evidence sweeps, or continuation of the closed maintenance loop.",
    ):
        assert expected in harness_normalized

    for expected in (
        "Use this for `Privacy-boundary review` work before implementation.",
        "This review classifies risk; it is not approval to implement.",
        "Reading `docs/codex-long-term-goal.md` gives direction only; it is not release authorization, not automatic maintenance authorization, and not approval for broad evidence sweeps, release or publish actions, or capture-surface expansion.",
        "If the work is deterministic docs, tests, fixtures, scorecards, CI, or compatible metadata that does not touch privacy surfaces, use the harness-first task template.",
        "If the proposal requires runtime expansion, new capture surfaces, release or publish actions, broad evidence sweeps, or continuation of the closed maintenance loop, stop for explicit human product approval.",
    ):
        assert expected in privacy_normalized


def test_privacy_boundary_template_requires_mcp_output_impact_classification():
    template = (
        ROOT / ".github" / "ISSUE_TEMPLATE" / "privacy_boundary_review.yml"
    ).read_text(encoding="utf-8")
    normalized = " ".join(template.split())

    for expected in (
        "id: mcp_output_impact",
        "label: MCP output impact",
        "If this touches MCP output, name whether it affects result examples, compatible metadata, schema conditions, or the fixed read-only tool list.",
        "State `No MCP output impact` if none.",
        "Result examples:",
        "Compatible metadata:",
        "Schema conditions:",
        "Fixed read-only tool list:",
    ):
        assert expected in normalized


def test_harness_template_suggests_mcp_metadata_validation_for_mcp_docs():
    template = (
        ROOT / ".github" / "ISSUE_TEMPLATE" / "harness_first_task.yml"
    ).read_text(encoding="utf-8")
    normalized = " ".join(template.split())

    for expected in (
        "For MCP examples or compatible metadata, include the focused MCP docs/schema tests in the validation plan.",
        "python -m pytest tests/test_mcp_result_metadata_docs.py tests/test_compatibility_contracts.py::test_mcp_result_schema_tool_enum_matches_exact_read_only_contract -q",
        "python -m pytest tests/test_mcp_tools.py tests/test_mcp_result_metadata_docs.py tests/test_compatibility_contracts.py -q",
        "MCP examples and compatible metadata keep the fixed read-only tool list, trust labels, metadata-only binding, and evidence-policy guardrails.",
    ):
        assert expected in normalized
