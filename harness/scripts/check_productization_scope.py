from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


PHASE_FILES = {
    "p0": {
        "AGENTS.md",
        ".github/release.yml",
        ".github/workflows/productization.yml",
        ".github/workflows/windows-harness.yml",
        "docs/productization-blueprint.md",
        "harness/scripts/check_productization_scope.py",
        "harness/scripts/run_install_cli_smoke.py",
        "src/winchronicle/cli.py",
        "tests/test_cli.py",
    },
    "p1": {
        "README.md",
        "README.zh-CN.md",
        "docs/assets/winchronicle-hero.png",
        "docs/assets/winchronicle-social-preview.png",
        "docs/assets/winchronicle-hero.prompt.md",
        "docs/project-presentation.md",
    },
    "p2": {
        "README.md",
        "README.zh-CN.md",
        "docs/windows-first-run.md",
        "docs/codex-app-workday-guide.md",
        "docs/mcp-client-setup.md",
    },
    "p3": {
        "README.md",
        "README.zh-CN.md",
        "docs/workday-session.md",
        "docs/examples/workday-summary.zh-CN.md",
        "docs/examples/workday-summary.en.md",
    },
    "p4": {
        "README.md",
        "README.zh-CN.md",
        "docs/codex-app-workday-guide.md",
        "docs/codex-workday-plugin.md",
        "docs/mcp-client-setup.md",
    },
    "p5": {
        "README.md",
        "README.zh-CN.md",
        "docs/maintenance-index.md",
        "docs/project-presentation.md",
    },
}

RELEASE_METADATA_FILES = {
    "pyproject.toml",
    "plugins/winchronicle-workday/.codex-plugin/plugin.json",
    "src/winchronicle/codex_plugins/winchronicle-workday/.codex-plugin/plugin.json",
    "src/winchronicle/_version.py",
    "tests/test_version_identity.py",
}

CLOSEOUT_BRANCHES = {
    "codex/winchronicle-closeout",
}

CLOSEOUT_FILES = set().union(*PHASE_FILES.values(), RELEASE_METADATA_FILES) | {
    ".github/ISSUE_TEMPLATE/feature_proposal.yml",
    ".github/ISSUE_TEMPLATE/harness_first_task.yml",
    ".github/ISSUE_TEMPLATE/privacy_boundary_review.yml",
    ".github/pull_request_template.md",
    "CONTRIBUTING.md",
    "docs/codex-app-plugin-install.md",
    "docs/codex-app-workday-guide.md",
    "docs/codex-long-term-goal.md",
    "docs/codex-workday-plugin.md",
    "docs/demo-promotion-kit.md",
    "docs/deterministic-demo.md",
    "docs/mcp-readonly-examples.md",
    "docs/mcp-result-metadata.md",
    "docs/operator-quickstart.md",
    "docs/productization-self-eval.md",
    "docs/quick-demo.md",
    "docs/release-checklist.md",
    "docs/release-evidence.md",
    "docs/windows-first-run.md",
    "docs/workday-session.md",
    "harness/README.md",
    "harness/fixtures/workday/daily_dry_run_text_contract.json",
    "harness/fixtures/workday/plugin_dry_run_text_contract.json",
    "harness/fixtures/workday/plugin_entrypoint_contract.json",
    "harness/fixtures/workday/setup_dry_run_text_contract.json",
    "harness/fixtures/workday/status_text_contract.json",
    "harness/fixtures/workday/stop_human_summary_contract.json",
    "harness/scorecards/mcp-quality.md",
    "harness/scorecards/memory-quality.md",
    "harness/scripts/run_harness.py",
    "harness/scripts/run_install_cli_smoke.py",
    "harness/scripts/run_productization_self_eval.py",
    "harness/scripts/run_watcher_slow_helper_smoke.py",
    "harness/specs/harness-command-plan.schema.json",
    "harness/specs/mcp-tool-result.schema.json",
    "harness/specs/workday-dry-run-text-contract.schema.json",
    "harness/specs/workday-stop-summary-contract.schema.json",
    "plugins/winchronicle-workday/skills/workday-recorder/SKILL.md",
    "src/winchronicle/cli.py",
    "src/winchronicle/codex_plugins/winchronicle-workday/skills/workday-recorder/SKILL.md",
    "src/winchronicle/mcp/server.py",
    "src/winchronicle/workday.py",
    "tests/test_cli.py",
    "tests/test_codex_long_term_goal_docs.py",
    "tests/test_codex_workday_plugin.py",
    "tests/test_compatibility_contracts.py",
    "tests/test_compatibility_evidence_docs.py",
    "tests/test_mcp_result_metadata_docs.py",
    "tests/test_mcp_tools.py",
    "tests/test_operator_diagnostics_docs.py",
    "tests/test_productization_scope.py",
    "tests/test_productization_self_eval.py",
    "tests/test_readme_daily_workflow.py",
    "tests/test_watcher_events.py",
    "tests/test_windows_first_run_docs.py",
    "tests/test_windows_harness_workflow.py",
    "tests/test_workday.py",
    "tests/test_workday_docs.py",
}

REQUIRED_BY_PHASE = {
    "p0": {
        "docs/productization-blueprint.md",
        ".github/workflows/productization.yml",
        "harness/scripts/check_productization_scope.py",
    },
    "p1": {
        "docs/assets/winchronicle-hero.png",
        "docs/assets/winchronicle-social-preview.png",
        "docs/assets/winchronicle-hero.prompt.md",
    },
    "p3": {
        "docs/examples/workday-summary.zh-CN.md",
        "docs/examples/workday-summary.en.md",
    },
}

PRODUCTIZATION_SURFACES = (
    "README.md",
    "README.zh-CN.md",
    "AGENTS.md",
    ".github/",
    "docs/",
    "harness/scripts/check_productization_scope.py",
)

GENERATED_PREFIXES = (
    "capture-buffer/",
    "diagnostics/",
    "harness/artifacts/",
    "harness/diagnostics/",
    "logs/",
    "memory/",
    "ocr-cache/",
    "screenshot-cache/",
    "smoke-artifacts/",
    "uia-smoke-artifacts/",
)

GENERATED_SUFFIXES = (
    ".db",
    ".db-shm",
    ".db-wal",
    ".sqlite",
    ".sqlite3",
    ".tmp",
    ".temp",
)


def main() -> int:
    branch = os.environ.get("GITHUB_HEAD_REF") or os.environ.get("GITHUB_REF_NAME", "")
    phase = _phase_from_branch(branch)
    changed = _changed_files()

    generated = [
        path
        for path in changed
        if path.startswith(GENERATED_PREFIXES) or path.endswith(GENERATED_SUFFIXES)
    ]
    if generated:
        _print_list("Generated or local-state artifacts must not be committed:", generated)
        return 1

    if _is_closeout_branch(branch):
        forbidden = [path for path in changed if path not in CLOSEOUT_FILES]
        if forbidden:
            _print_list("Closeout integration changed files outside scope:", forbidden)
            return 1
        print(f"Closeout integration scope check passed for {len(changed)} changed file(s).")
        return 0

    if phase is None:
        touched_productization = [
            path
            for path in changed
            if path in RELEASE_METADATA_FILES or _starts_with_any(path, PRODUCTIZATION_SURFACES)
        ]
        if touched_productization:
            print(f"Productization files changed on unrecognized branch {branch!r}.")
            print(
                "Use a branch named codex/p0-*, codex/p1-*, ..., codex/p5-*, "
                "or codex/winchronicle-closeout for the approved integration closeout."
            )
            _print_list("Changed productization files:", touched_productization)
            return 1
        print(f"No productization scope check required for branch {branch!r}.")
        return 0

    allowed = PHASE_FILES[phase] | RELEASE_METADATA_FILES
    forbidden = [path for path in changed if path not in allowed]
    if forbidden:
        _print_list(f"Phase {phase} changed files outside scope:", forbidden)
        return 1

    missing = [path for path in sorted(REQUIRED_BY_PHASE.get(phase, set())) if not Path(path).exists()]
    if missing:
        _print_list(f"Phase {phase} is missing required paths:", missing)
        return 1

    print(f"Phase {phase} scope check passed for {len(changed)} changed file(s).")
    return 0


def _phase_from_branch(branch: str) -> str | None:
    for candidate in PHASE_FILES:
        if f"/{candidate}-" in branch or branch.startswith(f"codex/{candidate}-"):
            return candidate
    return None


def _is_closeout_branch(branch: str) -> bool:
    return branch in CLOSEOUT_BRANCHES


def _changed_files() -> list[str]:
    subprocess.run(["git", "fetch", "origin", "main", "--quiet"], check=True)
    if os.environ.get("GITHUB_ACTIONS") == "true":
        diff_command = ["git", "diff", "--name-only", "origin/main...HEAD"]
    else:
        diff_command = ["git", "diff", "--name-only", "origin/main"]
    diff = subprocess.check_output(diff_command, text=True)
    changed = {line.strip().replace("\\", "/") for line in diff.splitlines() if line.strip()}
    if os.environ.get("GITHUB_ACTIONS") != "true":
        untracked = subprocess.check_output(
            ["git", "ls-files", "--others", "--exclude-standard"],
            text=True,
        )
        changed.update(line.strip().replace("\\", "/") for line in untracked.splitlines() if line.strip())
    return sorted(changed)


def _starts_with_any(path: str, prefixes: tuple[str, ...]) -> bool:
    return any(path == prefix.rstrip("/") or path.startswith(prefix) for prefix in prefixes)


def _print_list(title: str, paths: list[str]) -> None:
    print(title)
    for path in paths:
        print(f"  - {path}")


if __name__ == "__main__":
    sys.exit(main())
