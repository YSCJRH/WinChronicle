from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_THRESHOLD = 90
THRESHOLD_RANGE = "integer percentage from 0 to 100"
CLI_ERROR_EXIT_CODE = 2
CLI_ERROR_NO_JSON_PAYLOAD = True
CLI_ERROR_NO_TRACEBACK = True
CLI_THRESHOLD_RANGE_ERROR = "threshold must be between 0 and 100"
CLI_THRESHOLD_INTEGER_ERROR = "threshold must be an integer between 0 and 100"
ROOT_ARGUMENT_CONTRACT = "existing directory used as local self-eval root"
CLI_ROOT_PATH_ERROR = "--root must be an existing directory"
SCORE_FORMULA = "round(100 * passed / total)"
PASS_CONDITION = "score >= threshold and failed_items is empty"
FAILED_ITEM_FORMAT = "category: name (path: reason)"
PASSING_NEXT_ACTIONS = (
    "Keep README first-screen copy compact.",
    "Refresh demo and social copy when user-facing behavior changes.",
    "Add new growth/trust checks only when they protect a real onboarding promise.",
)
MISSING_FILE_NEXT_ACTION = "Restore or create the missing checked files before rerunning."
GENERIC_FAILURE_NEXT_ACTIONS = (
    "Fix the listed missing or overclaiming items.",
    "Run python harness/scripts/run_productization_self_eval.py again.",
)
CATEGORY_TEXT_ORDER = (
    "codex_entry",
    "contributor_entry",
    "first_screen",
    "fixture_demo",
    "overclaim_risk",
    "privacy_boundary",
)
BOUNDARY_TEXT_ORDER = (
    "does_not_run_live_uia",
    "does_not_read_desktop",
    "does_not_capture_observed_content",
    "checks_public_docs_and_static_metadata_only",
)


@dataclass(frozen=True)
class Check:
    category: str
    name: str
    path: str
    needle: str
    mode: str = "contains"


WORKDAY_RECORD_ONLY_TEXT = "record-only"
WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT = "summary-level evidence"
WORKDAY_NO_RAW_OBSERVED_TEXT = "does not send raw observed text"
WORKDAY_SUMMARY_BOUNDARY_FIELD_TEXT = "`summary_boundary`"
WORKDAY_NOT_TELEMETRY_REPORT_TEXT = "not a telemetry or log-counter report"
WORKDAY_README_DAILY_WORKFLOW_VALIDATION_TEXT = "tests/test_readme_daily_workflow.py -q"
WORKDAY_PRODUCTIZATION_SELF_EVAL_VALIDATION_TEXT = (
    "run_productization_self_eval.py --format json"
)
WORKDAY_SHARED_VALIDATION_TEXTS = (
    WORKDAY_README_DAILY_WORKFLOW_VALIDATION_TEXT,
    WORKDAY_PRODUCTIZATION_SELF_EVAL_VALIDATION_TEXT,
)
WORKDAY_CONTRIBUTING_SHARED_BOUNDARY_TEXTS = (
    WORKDAY_RECORD_ONLY_TEXT,
    WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT,
    WORKDAY_NO_RAW_OBSERVED_TEXT,
)


WORKDAY_ENTRYPOINT_BOUNDARY_CHECKS = [
    Check("first_screen", "README Workday record-only", "README.md", WORKDAY_RECORD_ONLY_TEXT),
    Check("first_screen", "README Workday summary-level evidence", "README.md", WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT),
    Check("first_screen", "README Workday no raw observed text", "README.md", WORKDAY_NO_RAW_OBSERVED_TEXT),
    Check("first_screen", "README Workday summary boundary field", "README.md", WORKDAY_SUMMARY_BOUNDARY_FIELD_TEXT),
    Check("first_screen", "README Workday not telemetry report", "README.md", WORKDAY_NOT_TELEMETRY_REPORT_TEXT),
    Check("first_screen", "README zh-CN Workday record-only", "README.zh-CN.md", WORKDAY_RECORD_ONLY_TEXT),
    Check("first_screen", "README zh-CN Workday summary-level evidence", "README.zh-CN.md", WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT),
    Check("first_screen", "README zh-CN Workday no raw observed text", "README.zh-CN.md", WORKDAY_NO_RAW_OBSERVED_TEXT),
    Check("first_screen", "README zh-CN Workday summary boundary field", "README.zh-CN.md", WORKDAY_SUMMARY_BOUNDARY_FIELD_TEXT),
    Check("first_screen", "README zh-CN Workday localized telemetry boundary", "README.zh-CN.md", "不是遥测或日志计数报告"),
    Check("first_screen", "First-run Workday record-only", "docs/windows-first-run.md", WORKDAY_RECORD_ONLY_TEXT),
    Check("first_screen", "First-run Workday summary-level evidence", "docs/windows-first-run.md", WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT),
    Check("first_screen", "First-run Workday no raw observed text", "docs/windows-first-run.md", WORKDAY_NO_RAW_OBSERVED_TEXT),
    Check("first_screen", "First-run Workday summary boundary field", "docs/windows-first-run.md", WORKDAY_SUMMARY_BOUNDARY_FIELD_TEXT),
    Check("first_screen", "First-run Workday not telemetry report", "docs/windows-first-run.md", WORKDAY_NOT_TELEMETRY_REPORT_TEXT),
    Check("codex_entry", "Plugin install record-only", "docs/codex-app-plugin-install.md", WORKDAY_RECORD_ONLY_TEXT),
    Check("codex_entry", "Plugin install summary-level evidence", "docs/codex-app-plugin-install.md", WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT),
    Check("codex_entry", "Plugin install no raw observed text", "docs/codex-app-plugin-install.md", WORKDAY_NO_RAW_OBSERVED_TEXT),
    Check("codex_entry", "Plugin install summary boundary output", "docs/codex-app-plugin-install.md", "Summary boundary:"),
    Check("codex_entry", "Plugin install not telemetry report", "docs/codex-app-plugin-install.md", WORKDAY_NOT_TELEMETRY_REPORT_TEXT),
    Check("codex_entry", "Workday guide record-only", "docs/codex-app-workday-guide.md", WORKDAY_RECORD_ONLY_TEXT),
    Check("codex_entry", "Workday summary-level evidence", "docs/codex-app-workday-guide.md", WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT),
    Check("codex_entry", "Workday no raw observed text", "docs/codex-app-workday-guide.md", WORKDAY_NO_RAW_OBSERVED_TEXT),
    Check("codex_entry", "Workday guide summary boundary field", "docs/codex-app-workday-guide.md", WORKDAY_SUMMARY_BOUNDARY_FIELD_TEXT),
    Check("codex_entry", "Workday guide not telemetry report", "docs/codex-app-workday-guide.md", WORKDAY_NOT_TELEMETRY_REPORT_TEXT),
    Check("codex_entry", "Workday plugin record-only", "docs/codex-workday-plugin.md", WORKDAY_RECORD_ONLY_TEXT),
    Check("codex_entry", "Workday plugin summary-level evidence", "docs/codex-workday-plugin.md", WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT),
    Check("codex_entry", "Workday plugin no raw observed text", "docs/codex-workday-plugin.md", WORKDAY_NO_RAW_OBSERVED_TEXT),
    Check("codex_entry", "Workday plugin summary boundary field", "docs/codex-workday-plugin.md", WORKDAY_SUMMARY_BOUNDARY_FIELD_TEXT),
    Check("codex_entry", "Workday plugin not telemetry report", "docs/codex-workday-plugin.md", WORKDAY_NOT_TELEMETRY_REPORT_TEXT),
]


WORKDAY_CONTRIBUTING_ENTRYPOINT_TARGETS = (
    ("README entrypoint", "`README.md`"),
    ("first-run entrypoint", "`docs/windows-first-run.md`"),
    ("plugin install entrypoint", "`docs/codex-app-plugin-install.md`"),
    ("guide entrypoint", "`docs/codex-app-workday-guide.md`"),
    ("plugin doc entrypoint", "`docs/codex-workday-plugin.md`"),
)
WORKDAY_CONTRIBUTING_ENTRYPOINT_CHECKS = [
    Check("contributor_entry", f"Contributing Workday {target_name}", "CONTRIBUTING.md", target_text)
    for target_name, target_text in WORKDAY_CONTRIBUTING_ENTRYPOINT_TARGETS
]
WORKDAY_CONTRIBUTING_META_TARGETS = (
    ("consistency rule", "five-entrypoint consistency"),
    ("self-eval link", "`docs/productization-self-eval.md`"),
)
WORKDAY_CONTRIBUTING_META_CHECKS = [
    Check("contributor_entry", f"Contributing Workday {meta_name}", "CONTRIBUTING.md", meta_text)
    for meta_name, meta_text in WORKDAY_CONTRIBUTING_META_TARGETS
]
WORKDAY_CONTRIBUTING_BOUNDARY_TARGETS = (
    ("record-only boundary", WORKDAY_RECORD_ONLY_TEXT),
    ("summary evidence boundary", WORKDAY_SUMMARY_LEVEL_EVIDENCE_TEXT),
    ("raw text boundary", WORKDAY_NO_RAW_OBSERVED_TEXT),
)
WORKDAY_CONTRIBUTING_BOUNDARY_CHECKS = [
    Check("contributor_entry", f"Contributing Workday {boundary_name}", "CONTRIBUTING.md", boundary_text)
    for boundary_name, boundary_text in WORKDAY_CONTRIBUTING_BOUNDARY_TARGETS
]
WORKDAY_CONTRIBUTING_VALIDATION_TARGETS = (
    ("README daily workflow validation", WORKDAY_README_DAILY_WORKFLOW_VALIDATION_TEXT),
    ("self-eval JSON validation", WORKDAY_PRODUCTIZATION_SELF_EVAL_VALIDATION_TEXT),
    (
        "Chinese README validation note",
        "若修改 `README.md` 或 `README.zh-CN.md` 的 Workday guidance",
    ),
)
WORKDAY_CONTRIBUTING_VALIDATION_CHECKS = [
    Check("contributor_entry", f"Contributing Workday {validation_name}", "CONTRIBUTING.md", validation_text)
    for validation_name, validation_text in WORKDAY_CONTRIBUTING_VALIDATION_TARGETS
]
WORKDAY_CONTRIBUTING_CONSISTENCY_CHECKS = [
    *WORKDAY_CONTRIBUTING_META_CHECKS,
    *WORKDAY_CONTRIBUTING_ENTRYPOINT_CHECKS,
    *WORKDAY_CONTRIBUTING_BOUNDARY_CHECKS,
    *WORKDAY_CONTRIBUTING_VALIDATION_CHECKS,
]


WORKDAY_CONTRIBUTOR_CHECKLIST_TARGETS = (
    ("PR", ".github/pull_request_template.md"),
    ("Harness issue", ".github/ISSUE_TEMPLATE/harness_first_task.yml"),
)
WORKDAY_CONTRIBUTOR_CHECKLIST_VALIDATIONS = (
    ("README daily workflow validation", WORKDAY_README_DAILY_WORKFLOW_VALIDATION_TEXT),
    ("self-eval JSON validation", WORKDAY_PRODUCTIZATION_SELF_EVAL_VALIDATION_TEXT),
)
WORKDAY_CONTRIBUTOR_CHECKLIST_CHECKS = [
    Check("contributor_entry", f"{target_name} Workday {validation_name}", path, validation_text)
    for target_name, path in WORKDAY_CONTRIBUTOR_CHECKLIST_TARGETS
    for validation_name, validation_text in WORKDAY_CONTRIBUTOR_CHECKLIST_VALIDATIONS
]


CONTRIBUTOR_TEMPLATE_INTAKE_TEXT = (
    "Before implementation, read `AGENTS.md`, `docs/roadmap.md`, "
    "`README.md`, `docs/codex-long-term-goal.md`, and the files, tests, "
    "fixtures, schemas, scorecards, or docs affected by the task."
)
CONTRIBUTOR_TEMPLATE_INTAKE_TARGETS = (
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


CONTRIBUTOR_TEMPLATE_INTAKE_CHECKS = [
    Check("contributor_entry", name, path, CONTRIBUTOR_TEMPLATE_INTAKE_TEXT)
    for name, path in CONTRIBUTOR_TEMPLATE_INTAKE_TARGETS
]


CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_TEXT = (
    "Reading `docs/codex-long-term-goal.md` gives direction only; it is not "
    "release authorization, not automatic maintenance authorization, and "
    "not approval for broad evidence sweeps, release or publish actions, "
    "or capture-surface expansion."
)
CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_TARGETS = (
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


CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_CHECKS = [
    Check("contributor_entry", name, path, CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_TEXT)
    for name, path in CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_TARGETS
]


SELF_EVAL_STABLE_TEXT_OUTPUT_CHECKS = [
    Check("contributor_entry", "Self-eval stable text output heading", "docs/productization-self-eval.md", "## Stable Text Output"),
    Check("contributor_entry", "Self-eval stable text output category order", "docs/productization-self-eval.md", "`Categories:` uses this canonical order", "canonical_category_order"),
    Check("contributor_entry", "Self-eval stable text output boundary order", "docs/productization-self-eval.md", "`Boundary:` uses this canonical order", "canonical_boundary_order"),
    Check("contributor_entry", "Self-eval stable text output update rule", "docs/productization-self-eval.md", "update the canonical order constants"),
]


SELF_EVAL_JSON_CONTRACT_CHECKS = [
    Check("contributor_entry", "Self-eval JSON contract heading", "docs/productization-self-eval.md", "## JSON Contract"),
    Check("contributor_entry", "Self-eval JSON contract schema version", "docs/productization-self-eval.md", "`schema_version = 1`"),
    Check("contributor_entry", "Self-eval JSON contract top-level keys", "docs/productization-self-eval.md", "`schema_version`, `name`, `score`, `threshold`, `passed`, `categories`, `failed_items`, `next_actions`, `provenance`, and `boundary`"),
    Check("contributor_entry", "Self-eval JSON contract update rule", "docs/productization-self-eval.md", "change the schema version and focused JSON contract tests before renaming or removing fields"),
]


SELF_EVAL_JSON_FAILURE_CONTRACT_CHECKS = [
    Check("contributor_entry", "Self-eval JSON failure contract heading", "docs/productization-self-eval.md", "## JSON Failure Contract"),
    Check("contributor_entry", "Self-eval JSON failure contract stable shape", "docs/productization-self-eval.md", "Failure JSON keeps the same `schema_version`, `provenance`, and `boundary` fields"),
    Check("contributor_entry", "Self-eval JSON failure contract failed items", "docs/productization-self-eval.md", "`failed_items` identifies the missing or overclaiming check"),
    Check("contributor_entry", "Self-eval JSON failure contract no path snapshots", "docs/productization-self-eval.md", "Do not snapshot absolute `checked_root` paths"),
]


SELF_EVAL_FAILED_ITEM_FORMAT_CHECKS = [
    Check("contributor_entry", "Self-eval failed item format heading", "docs/productization-self-eval.md", "## Failed Item Format"),
    Check("contributor_entry", "Self-eval failed item format contract", "docs/productization-self-eval.md", "`failed_items` entries use `category: name (path: reason)`"),
    Check("contributor_entry", "Self-eval failed item format update rule", "docs/productization-self-eval.md", "update `FAILED_ITEM_FORMAT` and focused failed-item format tests"),
]


SELF_EVAL_NEXT_ACTIONS_CONTRACT_CHECKS = [
    Check("contributor_entry", "Self-eval next actions contract heading", "docs/productization-self-eval.md", "## Next Actions Contract"),
    Check("contributor_entry", "Self-eval next actions stable vocabulary", "docs/productization-self-eval.md", "`next_actions` is a small stable action vocabulary for local automation."),
    Check("contributor_entry", "Self-eval next actions passing entries", "docs/productization-self-eval.md", "Passing runs use the three `PASSING_NEXT_ACTIONS` entries"),
    Check("contributor_entry", "Self-eval next actions missing-file entries", "docs/productization-self-eval.md", "Missing-file failures prepend `MISSING_FILE_NEXT_ACTION` before `GENERIC_FAILURE_NEXT_ACTIONS`."),
    Check("contributor_entry", "Self-eval next actions generic failure entries", "docs/productization-self-eval.md", "Other failures return only `GENERIC_FAILURE_NEXT_ACTIONS`."),
    Check("contributor_entry", "Self-eval next actions update rule", "docs/productization-self-eval.md", "update `PASSING_NEXT_ACTIONS`, `MISSING_FILE_NEXT_ACTION`, `GENERIC_FAILURE_NEXT_ACTIONS`, and focused next-actions tests"),
]


SELF_EVAL_SCORE_CONTRACT_CHECKS = [
    Check("contributor_entry", "Self-eval score contract heading", "docs/productization-self-eval.md", "## Score Contract"),
    Check("contributor_entry", "Self-eval score formula", "docs/productization-self-eval.md", "`score` and category scores use `round(100 * passed / total)`."),
    Check("contributor_entry", "Self-eval score helper update rule", "docs/productization-self-eval.md", "update `SCORE_FORMULA`, `_percentage_score`, and focused score contract tests"),
]


SELF_EVAL_PASS_CONTRACT_CHECKS = [
    Check("contributor_entry", "Self-eval pass contract heading", "docs/productization-self-eval.md", "## Pass Contract"),
    Check("contributor_entry", "Self-eval pass condition", "docs/productization-self-eval.md", "`passed` is true only when `score >= threshold` and `failed_items` is empty."),
    Check("contributor_entry", "Self-eval pass helper update rule", "docs/productization-self-eval.md", "update `PASS_CONDITION`, `_passes_gate`, and focused pass contract tests"),
]


SELF_EVAL_THRESHOLD_CONTRACT_CHECKS = [
    Check("contributor_entry", "Self-eval threshold contract heading", "docs/productization-self-eval.md", "## Threshold Contract"),
    Check("contributor_entry", "Self-eval default threshold", "docs/productization-self-eval.md", "`DEFAULT_THRESHOLD` is 90."),
    Check("contributor_entry", "Self-eval threshold range", "docs/productization-self-eval.md", "`threshold` is an integer percentage from 0 to 100."),
    Check("contributor_entry", "Self-eval CLI error exit code", "docs/productization-self-eval.md", "`CLI_ERROR_EXIT_CODE` is 2."),
    Check("contributor_entry", "Self-eval CLI threshold error text", "docs/productization-self-eval.md", "CLI threshold errors use `CLI_THRESHOLD_RANGE_ERROR` or `CLI_THRESHOLD_INTEGER_ERROR`."),
    Check("contributor_entry", "Self-eval CLI error output boundary", "docs/productization-self-eval.md", "CLI threshold errors do not emit a JSON payload or traceback."),
    Check("contributor_entry", "Self-eval threshold helper update rule", "docs/productization-self-eval.md", "update `THRESHOLD_RANGE`, `CLI_ERROR_EXIT_CODE`, `CLI_THRESHOLD_RANGE_ERROR`, `CLI_THRESHOLD_INTEGER_ERROR`, `_validate_threshold`, `_parse_threshold`, and focused threshold contract tests"),
]


SELF_EVAL_ROOT_ARGUMENT_CONTRACT_CHECKS = [
    Check("contributor_entry", "Self-eval root argument contract heading", "docs/productization-self-eval.md", "## Root Argument Contract"),
    Check("contributor_entry", "Self-eval root argument purpose", "docs/productization-self-eval.md", "`--root` is a hidden local test override."),
    Check("contributor_entry", "Self-eval root argument existing directory", "docs/productization-self-eval.md", "`ROOT_ARGUMENT_CONTRACT` is `existing directory used as local self-eval root`."),
    Check("contributor_entry", "Self-eval root argument CLI error text", "docs/productization-self-eval.md", "CLI root errors use `CLI_ROOT_PATH_ERROR`."),
    Check("contributor_entry", "Self-eval root argument no payload", "docs/productization-self-eval.md", "Invalid root paths do not emit a JSON payload or traceback."),
    Check("contributor_entry", "Self-eval root argument missing checked paths", "docs/productization-self-eval.md", "Existing roots with missing checked paths are self-eval failures, not CLI argument errors."),
    Check("contributor_entry", "Self-eval root argument helper update rule", "docs/productization-self-eval.md", "update `ROOT_ARGUMENT_CONTRACT`, `CLI_ROOT_PATH_ERROR`, `_parse_root`, and focused root argument tests"),
]


SELF_EVAL_JSON_PROVENANCE_CHECKS = [
    Check("contributor_entry", "Self-eval JSON provenance heading", "docs/productization-self-eval.md", "## JSON Provenance"),
    Check("contributor_entry", "Self-eval JSON provenance checked root", "docs/productization-self-eval.md", "`provenance.checked_root`"),
    Check("contributor_entry", "Self-eval JSON provenance checked paths", "docs/productization-self-eval.md", "`provenance.checked_paths`"),
    Check("contributor_entry", "Self-eval JSON provenance sharing boundary", "docs/productization-self-eval.md", "do not treat JSON output as permission to publish"),
    Check("contributor_entry", "Self-eval JSON provenance fixed path boundary", "docs/productization-self-eval.md", "fixed repository-relative docs and static metadata paths"),
]


FIRST_RUN_SAFE_BOUNDARY_CHECKS = [
    Check("first_screen", "First-run fixture-only demo", "docs/windows-first-run.md", "fixture-only"),
    Check("first_screen", "First-run no live desktop read", "docs/windows-first-run.md", "does not read the live desktop"),
    Check("first_screen", "First-run no content upload", "docs/windows-first-run.md", "does not upload content"),
    Check("first_screen", "First-run dry-run print-only", "docs/windows-first-run.md", "The dry-runs only print instructions or config snippets."),
]


DEMO_OUTPUT_SHARING_BOUNDARY_CHECKS = [
    Check("fixture_demo", "Deterministic demo sharing boundary", "docs/deterministic-demo.md", "Demo and MCP output are local evidence"),
    Check("fixture_demo", "Promotion kit sharing boundary", "docs/demo-promotion-kit.md", "Demo and MCP output are local evidence"),
    Check("fixture_demo", "Promotion kit external sharing approval", "docs/demo-promotion-kit.md", "External sharing still requires explicit user approval"),
]


DEMO_PROMOTION_FEATURE_PROPOSAL_BOUNDARY_CHECKS = [
    Check("fixture_demo", "Promotion kit feature proposal boundary", "docs/demo-promotion-kit.md", "feature proposal"),
    Check("fixture_demo", "Promotion kit implementation approval boundary", "docs/demo-promotion-kit.md", "approval to implement runtime behavior"),
    Check("fixture_demo", "Promotion kit contributing route", "docs/demo-promotion-kit.md", "`CONTRIBUTING.md`"),
    Check("fixture_demo", "Promotion kit self-eval route", "docs/demo-promotion-kit.md", "`docs/productization-self-eval.md`"),
]


MCP_METADATA_ONLY_PUBLIC_SHARING_BOUNDARY_CHECKS = [
    Check("codex_entry", "MCP metadata-only public sharing boundary", "docs/mcp-client-setup.md", "Metadata-only mode is not permission to publish MCP results"),
    Check("codex_entry", "MCP external sharing approval boundary", "docs/mcp-client-setup.md", "External sharing still requires explicit user approval"),
]


CONTRIBUTOR_README_CLASSIFICATION_CHECKS = [
    Check("contributor_entry", "English README task classification entry", "README.md", "classify the task with `CONTRIBUTING.md`"),
    Check("contributor_entry", "English README self-eval entry", "README.md", "`docs/productization-self-eval.md`"),
    Check("contributor_entry", "Chinese README contributing link", "README.zh-CN.md", "[CONTRIBUTING.md](CONTRIBUTING.md)"),
    Check("contributor_entry", "Chinese README summary entrypoint", "README.zh-CN.md", "`Task Classification` / `中文速览`"),
]


PROJECT_PRESENTATION_CLASSIFICATION_CHECKS = [
    Check("contributor_entry", "Project presentation classification link", "docs/project-presentation.md", "classify it with `CONTRIBUTING.md`"),
    Check("contributor_entry", "Project presentation self-eval link", "docs/project-presentation.md", "`docs/productization-self-eval.md`"),
    Check("contributor_entry", "Project presentation stricter path", "docs/project-presentation.md", "Use the stricter path when work touches privacy"),
]


CHECKS = [
    Check("first_screen", "English promise", "README.md", "Local-first memory for Windows AI agents"),
    Check("first_screen", "Chinese promise", "README.zh-CN.md", "面向 Windows AI Agent 的本地优先工作上下文记忆层"),
    Check("first_screen", "README hero", "README.md", "docs/assets/winchronicle-hero.png"),
    Check("first_screen", "Three paths", "README.md", "## Choose A Path"),
    Check("first_screen", "Demo path", "README.md", "python harness/scripts/run_quick_demo.py"),
    Check("first_screen", "Workday path", "README.md", "winchronicle codex setup --dry-run --format text"),
    Check("first_screen", "MCP path", "README.md", "winchronicle codex install --dry-run"),
    *FIRST_RUN_SAFE_BOUNDARY_CHECKS,
    *WORKDAY_ENTRYPOINT_BOUNDARY_CHECKS,
    Check("privacy_boundary", "Independent project", "README.md", "not affiliated with OpenAI"),
    Check("privacy_boundary", "Trust label", "README.md", 'trust = "untrusted_observed_content"'),
    Check("privacy_boundary", "Redaction first", "docs/privacy-architecture.md", "redaction"),
    Check("privacy_boundary", "No screenshots", "docs/privacy-architecture.md", "screenshots"),
    Check("privacy_boundary", "No desktop control", "docs/privacy-architecture.md", "desktop control"),
    Check("privacy_boundary", "No MCP write tools", "docs/privacy-architecture.md", "MCP write tools"),
    Check("fixture_demo", "Demo doc", "docs/quick-demo.md", "5-Minute Demo"),
    Check("fixture_demo", "Fixture-only shape", "docs/quick-demo.md", "fixture-only"),
    Check("fixture_demo", "No live desktop read", "docs/quick-demo.md", "does not read the live desktop"),
    Check("fixture_demo", "No content upload", "docs/quick-demo.md", "does not upload content"),
    Check("fixture_demo", "Quick demo script", "docs/quick-demo.md", "python harness/scripts/run_quick_demo.py"),
    Check("fixture_demo", "Fake helper boundary", "docs/quick-demo.md", "does not read the real desktop"),
    Check("fixture_demo", "Promotion kit", "docs/demo-promotion-kit.md", "English launch blurb"),
    *DEMO_OUTPUT_SHARING_BOUNDARY_CHECKS,
    *DEMO_PROMOTION_FEATURE_PROPOSAL_BOUNDARY_CHECKS,
    Check("codex_entry", "Codex workday guide", "docs/codex-app-workday-guide.md", "Codex App Workday Guide"),
    Check("codex_entry", "Plugin doc", "docs/codex-workday-plugin.md", "Fastest Codex App Setup"),
    Check("codex_entry", "Record-only boundary", "docs/codex-workday-plugin.md", "Record-only"),
    Check("codex_entry", "Plugin source command", "docs/codex-workday-plugin.md", "winchronicle codex plugin --dry-run --format text"),
    Check("codex_entry", "MCP remains read-only", "docs/mcp-client-setup.md", "through six fixed tools"),
    *MCP_METADATA_ONLY_PUBLIC_SHARING_BOUNDARY_CHECKS,
    Check("contributor_entry", "Contributing guide", "CONTRIBUTING.md", "Good First Contributions"),
    Check("contributor_entry", "Growth tasks", "CONTRIBUTING.md", "Growth And Trust Starter Tasks"),
    Check("contributor_entry", "Self-eval command", "CONTRIBUTING.md", "python harness/scripts/run_productization_self_eval.py"),
    Check("contributor_entry", "No observed content", "CONTRIBUTING.md", "do not commit observed content"),
    *CONTRIBUTOR_README_CLASSIFICATION_CHECKS,
    *WORKDAY_CONTRIBUTING_CONSISTENCY_CHECKS,
    *WORKDAY_CONTRIBUTOR_CHECKLIST_CHECKS,
    *CONTRIBUTOR_TEMPLATE_INTAKE_CHECKS,
    *CONTRIBUTOR_LONG_TERM_GOAL_BOUNDARY_CHECKS,
    Check("contributor_entry", "Project presentation", "docs/project-presentation.md", "Good First Issue Themes"),
    *PROJECT_PRESENTATION_CLASSIFICATION_CHECKS,
    *SELF_EVAL_STABLE_TEXT_OUTPUT_CHECKS,
    *SELF_EVAL_JSON_CONTRACT_CHECKS,
    *SELF_EVAL_JSON_FAILURE_CONTRACT_CHECKS,
    *SELF_EVAL_FAILED_ITEM_FORMAT_CHECKS,
    *SELF_EVAL_NEXT_ACTIONS_CONTRACT_CHECKS,
    *SELF_EVAL_SCORE_CONTRACT_CHECKS,
    *SELF_EVAL_PASS_CONTRACT_CHECKS,
    *SELF_EVAL_THRESHOLD_CONTRACT_CHECKS,
    *SELF_EVAL_ROOT_ARGUMENT_CONTRACT_CHECKS,
    *SELF_EVAL_JSON_PROVENANCE_CHECKS,
    Check("overclaim_risk", "No official-project claim", "README.md", "official openai project", "absent"),
    Check("overclaim_risk", "No records-everything claim", "README.md", "records everything", "absent"),
    Check("overclaim_risk", "No desktop-control claim", "README.md", "controls your desktop", "absent"),
    Check("overclaim_risk", "No screenshot-default claim", "README.md", "uses screenshots by default", "absent"),
    Check("overclaim_risk", "No cloud-memory claim", "README.md", "uploads your desktop", "absent"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic productization self-eval.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--threshold", type=_parse_threshold, default=DEFAULT_THRESHOLD)
    parser.add_argument("--root", type=_parse_root, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args()

    payload = evaluate(args.threshold, root=args.root)

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(_format_text(payload))

    return 0 if payload["passed"] else 1


def evaluate(threshold: int = DEFAULT_THRESHOLD, root: Path | None = None) -> dict[str, object]:
    threshold = _validate_threshold(threshold)
    base = ROOT if root is None else root
    files: dict[str, str] = {}
    failed: list[dict[str, str]] = []
    categories = sorted({check.category for check in CHECKS})
    category_totals = {category: 0 for category in categories}
    category_passed = {category: 0 for category in categories}

    for check in CHECKS:
        category_totals[check.category] += 1
        text = files.get(check.path)
        if text is None:
            path = base / check.path
            if not path.exists():
                failed.append(_failure(check, "missing file"))
                continue
            text = path.read_text(encoding="utf-8")
            files[check.path] = text

        ok = _check_matches(check, text)
        if ok:
            category_passed[check.category] += 1
        else:
            failed.append(_failure(check, _failure_reason(check)))

    score = _percentage_score(len(CHECKS) - len(failed), len(CHECKS))
    category_scores = {
        category: _percentage_score(category_passed[category], category_totals[category])
        for category in categories
    }
    failed_items = [_format_failed_item(item) for item in failed]

    return {
        "schema_version": 1,
        "name": "WinChronicle productization self-eval",
        "score": score,
        "threshold": threshold,
        "passed": _passes_gate(score, threshold, failed_items),
        "categories": category_scores,
        "failed_items": failed_items,
        "next_actions": _next_actions(failed_items),
        "provenance": {
            "checked_root": str(base),
            "checked_paths": sorted({check.path for check in CHECKS}),
        },
        "boundary": {
            "does_not_run_live_uia": True,
            "does_not_read_desktop": True,
            "does_not_capture_observed_content": True,
            "checks_public_docs_and_static_metadata_only": True,
        },
    }


def _percentage_score(passed: int, total: int) -> int:
    return round(100 * passed / total)


def _passes_gate(score: int, threshold: int, failed_items: list[str]) -> bool:
    return score >= threshold and not failed_items


def _validate_threshold(threshold: int) -> int:
    if type(threshold) is not int:
        raise TypeError(CLI_THRESHOLD_INTEGER_ERROR)
    if threshold < 0 or threshold > 100:
        raise ValueError(CLI_THRESHOLD_RANGE_ERROR)
    return threshold


def _parse_threshold(value: str) -> int:
    try:
        threshold = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(CLI_THRESHOLD_INTEGER_ERROR) from exc
    try:
        return _validate_threshold(threshold)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def _parse_root(value: str) -> Path:
    root = Path(value)
    if not root.is_dir():
        raise argparse.ArgumentTypeError(CLI_ROOT_PATH_ERROR)
    return root


def _failure(check: Check, reason: str) -> dict[str, str]:
    return {
        "category": check.category,
        "name": check.name,
        "path": check.path,
        "reason": reason,
    }


def _format_failed_item(item: dict[str, str]) -> str:
    return f"{item['category']}: {item['name']} ({item['path']}: {item['reason']})"


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _check_matches(check: Check, text: str) -> bool:
    if check.mode == "contains":
        return _normalize(check.needle) in _normalize(text)
    if check.mode == "absent":
        return _normalize(check.needle) not in _normalize(text)
    if check.mode == "canonical_category_order":
        return _canonical_order_matches(text, "Categories", CATEGORY_TEXT_ORDER)
    if check.mode == "canonical_boundary_order":
        return _canonical_order_matches(text, "Boundary", BOUNDARY_TEXT_ORDER)
    raise ValueError(f"unknown check mode: {check.mode}")


def _canonical_order_matches(text: str, label: str, expected: tuple[str, ...]) -> bool:
    pattern = rf"`{re.escape(label)}:` uses this canonical order:\s*(.*?)\."
    match = re.search(pattern, text, flags=re.DOTALL)
    if match is None:
        return False
    return tuple(re.findall(r"`([^`]+)`", match.group(1))) == expected


def _failure_reason(check: Check) -> str:
    if check.mode == "absent":
        return "forbidden phrase present"
    if check.mode in {"canonical_category_order", "canonical_boundary_order"}:
        return "canonical order mismatch"
    return "required phrase missing"


def _next_actions(failed_items: list[str]) -> list[str]:
    if not failed_items:
        return list(PASSING_NEXT_ACTIONS)
    actions = []
    if any("missing file" in item for item in failed_items):
        actions.append(MISSING_FILE_NEXT_ACTION)
    actions.extend(GENERIC_FAILURE_NEXT_ACTIONS)
    return actions


def _format_text(payload: dict[str, object]) -> str:
    status = "PASS" if payload["passed"] else "FAIL"
    lines = [
        "Productization self-eval",
        f"Status: {status}",
        f"Score: {payload['score']}/{payload['threshold']} threshold",
        "Categories:",
    ]
    categories = payload["categories"]
    assert isinstance(categories, dict)
    ordered_category_keys = [
        *[key for key in CATEGORY_TEXT_ORDER if key in categories],
        *[key for key in sorted(categories) if key not in CATEGORY_TEXT_ORDER],
    ]
    for category in ordered_category_keys:
        score = categories[category]
        lines.append(f"- {category}: {score}")

    failed = payload["failed_items"]
    if failed:
        lines.append("Failed items:")
        for item in failed:
            lines.append(f"- {item}")
    else:
        lines.append("Failed items: none")

    boundary = payload["boundary"]
    assert isinstance(boundary, dict)
    lines.append("Boundary:")
    ordered_boundary_keys = [
        *[key for key in BOUNDARY_TEXT_ORDER if key in boundary],
        *[key for key in boundary if key not in BOUNDARY_TEXT_ORDER],
    ]
    for key in ordered_boundary_keys:
        value = boundary[key]
        display_value = str(value).lower() if isinstance(value, bool) else value
        lines.append(f"- {key}: {display_value}")

    lines.append("Next:")
    for item in payload["next_actions"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
