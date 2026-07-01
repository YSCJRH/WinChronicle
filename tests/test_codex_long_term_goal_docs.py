from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_codex_long_term_goal_preserves_project_boundaries():
    doc = (ROOT / "docs" / "codex-long-term-goal.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    required = [
        "# Codex Long-Term Optimization Goal",
        "not a release plan",
        "not a maintenance loop",
        "not approval for new capture surfaces",
        "AGENTS.md",
        "docs/roadmap.md",
        "README.md",
        "local-first",
        "UIA-first",
        "harness-first",
        "redaction before storage, search, memory generation, reports, or MCP output",
        "read-only MCP",
        "untrusted_observed_content",
        "explicit human product decision",
        "privacy-boundary review",
    ]

    for text in required:
        assert text in normalized


def test_codex_long_term_goal_declares_direction_not_authorization():
    doc = (ROOT / "docs" / "codex-long-term-goal.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    for expected in (
        "direction only",
        "not release authorization",
        "not automatic maintenance authorization",
        "does not authorize broad evidence sweeps",
        "does not authorize release or publish actions",
        "does not authorize capture-surface expansion",
    ):
        assert expected in normalized


def test_codex_long_term_goal_lists_forbidden_surfaces_as_boundaries():
    doc = (ROOT / "docs" / "codex-long-term-goal.md").read_text(encoding="utf-8")

    forbidden_surface_terms = [
        "screenshots",
        "OCR",
        "audio recording",
        "keylogging",
        "clipboard capture",
        "cloud or network upload",
        "desktop control",
        "background daemons or services",
        "infinite polling loops",
        "MCP write tools",
        "arbitrary file reads",
        "LLM reducers or classifiers",
        "product-targeted capture",
        "release, upload, publish, or retag actions",
    ]

    hard_boundaries = doc.split("## Hard Boundaries", 1)[1].split("## Operating Loop", 1)[0]
    assert "This goal does not authorize:" in hard_boundaries
    for term in forbidden_surface_terms:
        assert term in hard_boundaries


def test_codex_long_term_goal_is_discoverable_from_navigation_docs():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    maintenance_index = (ROOT / "docs" / "maintenance-index.md").read_text(encoding="utf-8")

    assert "[Codex long-term optimization goal](docs/codex-long-term-goal.md)" in readme
    assert "[Codex 长期优化目标](docs/codex-long-term-goal.md)" in readme_zh
    assert "[Codex long-term optimization goal](codex-long-term-goal.md)" in maintenance_index


def test_codex_long_term_goal_navigation_text_is_not_authorization():
    surfaces = {
        "README.md": (
            (ROOT / "README.md").read_text(encoding="utf-8"),
            "[Codex long-term optimization goal](docs/codex-long-term-goal.md)",
            ("direction only", "not release", "not automatic maintenance authorization"),
        ),
        "README.zh-CN.md": (
            (ROOT / "README.zh-CN.md").read_text(encoding="utf-8"),
            "[Codex 长期优化目标](docs/codex-long-term-goal.md)",
            ("仅作方向参考", "不是发布授权", "不是自动维护循环"),
        ),
        "docs/maintenance-index.md": (
            (ROOT / "docs" / "maintenance-index.md").read_text(encoding="utf-8"),
            "[Codex long-term optimization goal](codex-long-term-goal.md)",
            ("direction only", "not release", "not automatic maintenance authorization"),
        ),
    }

    for surface, (text, link, required_phrases) in surfaces.items():
        matching_lines = [line for line in text.splitlines() if link in line]
        assert matching_lines, surface
        for line in matching_lines:
            for phrase in required_phrases:
                assert phrase in line, surface


def test_codex_long_term_goal_preserves_authority_and_report_format():
    doc = (ROOT / "docs" / "codex-long-term-goal.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    assert "does not replace `AGENTS.md` or `docs/roadmap.md`" in normalized
    assert "If this document and those files differ, follow the stricter boundary." in normalized
    assert (
        "It also does not replace GitHub issue templates, the pull request template, "
        "or the review entry checks in `docs/productization-self-eval.md`."
    ) in normalized
    assert (
        "Use those entry points before treating a long-term-goal turn as authorization "
        "for implementation."
    ) in normalized
    assert "## Required Closeout" in doc
    for heading in (
        "- What changed",
        "- Tests run",
        "- Tests not run and why",
        "- Privacy/security implications",
        "- Next smallest implementation task",
    ):
        assert heading in doc


def test_codex_long_term_goal_defines_task_selection_checklist():
    doc = (ROOT / "docs" / "codex-long-term-goal.md").read_text(encoding="utf-8")
    normalized = " ".join(doc.split())

    assert "## Task Selection Checklist" in doc
    for expected in (
        "Classify the request before choosing files or commands.",
        "`recording-only Workday operation`",
        "`harness-first task`",
        "`privacy-boundary review`",
        "`human product decision`",
        "If the request only starts, checks, stops, or summarizes a Workday session",
        "If the work stays inside deterministic docs, tests, fixtures, schemas, scorecards, CI, or compatible metadata",
        "If the work touches capture surfaces, observed content, storage, MCP output, memory output, redaction, or release evidence",
        "If the work asks for runtime expansion, a new capture surface, release or publish action, broad evidence sweep, or continuation of the closed maintenance loop",
        "When unsure, choose the stricter classification and stop before changing runtime behavior.",
    ):
        assert expected in normalized


def test_codex_long_term_goal_matches_roadmap_and_readme_expansion_boundaries():
    doc = (ROOT / "docs" / "codex-long-term-goal.md").read_text(encoding="utf-8")
    roadmap = (ROOT / "docs" / "roadmap.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    normalized_doc = " ".join(doc.split())
    normalized_roadmap = " ".join(roadmap.split())
    normalized_readme = " ".join(readme.split())

    assert "This roadmap does not start a new maintenance cursor." in normalized_roadmap
    assert "These are options for human review, not an automatically authorized backlog." in normalized_roadmap
    assert "manual smoke refresh" in normalized_roadmap
    assert "release path" in normalized_roadmap
    assert "default background capture" in normalized_readme

    for expected in (
        "does not start a new maintenance cursor",
        "not an automatically authorized backlog",
        "runtime behavior",
        "capture-surface expansion",
        "release path",
        "manual smoke refresh",
        "broad evidence sweep",
        "explicit human product approval",
        "default background capture",
    ):
        assert expected in normalized_doc


def test_readmes_codex_development_entrypoints_include_required_intake():
    surfaces = {
        "README.md": (
            (ROOT / "README.md").read_text(encoding="utf-8"),
            "When using Codex app or Codex CLI to develop WinChronicle:",
            "the files, tests, fixtures, schemas, scorecards, or docs affected by the task",
        ),
        "README.zh-CN.md": (
            (ROOT / "README.zh-CN.md").read_text(encoding="utf-8"),
            "使用 Codex app 或 Codex CLI 协助开发 WinChronicle 时：",
            "本次任务影响的 files、tests、fixtures、schemas、scorecards 或 docs",
        ),
    }

    for surface, (text, heading, affected_files_phrase) in surfaces.items():
        start = text.index(heading)
        end = text.index("\n## ", start + len(heading))
        section = text[start:end]
        normalized = " ".join(section.split())

        for expected in (
            "AGENTS.md",
            "docs/roadmap.md",
            "README.md",
            affected_files_phrase,
        ):
            assert expected in normalized, surface


def test_maintenance_index_exposes_required_intake_for_codex_maintenance_tasks():
    maintenance_index = (ROOT / "docs" / "maintenance-index.md").read_text(encoding="utf-8")
    normalized = " ".join(maintenance_index.split())

    assert "## Codex Maintenance Task Intake" in maintenance_index
    for expected in (
        "This index is historical reference, not a task queue.",
        "AGENTS.md",
        "docs/roadmap.md",
        "README.md",
        "docs/codex-long-term-goal.md",
        "the files, tests, fixtures, schemas, scorecards, or docs affected by the task",
        "Do not treat historical release records as authorization for release, upload, publish, broad evidence sweeps, or automatic maintenance loops.",
    ):
        assert expected in normalized


def test_maintenance_index_links_required_intake_to_self_eval_template_guard():
    maintenance_index = (ROOT / "docs" / "maintenance-index.md").read_text(encoding="utf-8")
    section = maintenance_index.split("## Codex Maintenance Task Intake", 1)[1].split(
        "\n## ",
        1,
    )[0]
    normalized = " ".join(section.split())

    for expected in (
        "[Contributor Required Intake Checks](productization-self-eval.md#contributor-required-intake-checks)",
        "PR and harness issue template Required Intake guard",
        "CONTRIBUTOR_TEMPLATE_INTAKE_CHECKS",
    ):
        assert expected in normalized


def test_contributing_exposes_required_intake_before_task_classification():
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    intro = contributing.split("## Task Classification", 1)[0]
    normalized = " ".join(intro.split())

    for expected in (
        "AGENTS.md",
        "docs/roadmap.md",
        "README.md",
        "docs/codex-long-term-goal.md",
        "the files, tests, fixtures, schemas, scorecards, or docs affected by the task",
    ):
        assert expected in normalized


def test_contributor_templates_expose_required_intake_before_work_starts():
    surfaces = {
        ".github/pull_request_template.md": (
            ROOT / ".github" / "pull_request_template.md"
        ).read_text(encoding="utf-8"),
        ".github/ISSUE_TEMPLATE/harness_first_task.yml": (
            ROOT / ".github" / "ISSUE_TEMPLATE" / "harness_first_task.yml"
        ).read_text(encoding="utf-8"),
        ".github/ISSUE_TEMPLATE/feature_proposal.yml": (
            ROOT / ".github" / "ISSUE_TEMPLATE" / "feature_proposal.yml"
        ).read_text(encoding="utf-8"),
        ".github/ISSUE_TEMPLATE/privacy_boundary_review.yml": (
            ROOT / ".github" / "ISSUE_TEMPLATE" / "privacy_boundary_review.yml"
        ).read_text(encoding="utf-8"),
    }

    required = (
        "Before implementation, read `AGENTS.md`, `docs/roadmap.md`, "
        "`README.md`, `docs/codex-long-term-goal.md`, and the files, tests, "
        "fixtures, schemas, scorecards, or docs affected by the task."
    )

    for surface, text in surfaces.items():
        assert required in " ".join(text.split()), surface


def test_contributor_entrypoints_explain_long_term_goal_is_not_authorization():
    surfaces = {
        "CONTRIBUTING.md": (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8"),
        ".github/pull_request_template.md": (
            ROOT / ".github" / "pull_request_template.md"
        ).read_text(encoding="utf-8"),
        ".github/ISSUE_TEMPLATE/harness_first_task.yml": (
            ROOT / ".github" / "ISSUE_TEMPLATE" / "harness_first_task.yml"
        ).read_text(encoding="utf-8"),
    }
    required = (
        "Reading `docs/codex-long-term-goal.md` gives direction only; it is not "
        "release authorization, not automatic maintenance authorization, and "
        "not approval for broad evidence sweeps, release or publish actions, "
        "or capture-surface expansion."
    )

    for surface, text in surfaces.items():
        assert required in " ".join(text.split()), surface
