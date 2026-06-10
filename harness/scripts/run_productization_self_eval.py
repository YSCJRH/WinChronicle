from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_THRESHOLD = 90


@dataclass(frozen=True)
class Check:
    category: str
    name: str
    path: str
    needle: str
    mode: str = "contains"


CHECKS = [
    Check("first_screen", "English promise", "README.md", "Local-first memory for Windows AI agents"),
    Check("first_screen", "Chinese promise", "README.zh-CN.md", "面向 Windows AI Agent 的本地优先工作上下文记忆层"),
    Check("first_screen", "README hero", "README.md", "docs/assets/winchronicle-hero.png"),
    Check("first_screen", "Three paths", "README.md", "## Choose A Path"),
    Check("first_screen", "Demo path", "README.md", "python harness/scripts/run_quick_demo.py"),
    Check("first_screen", "Workday path", "README.md", "winchronicle codex setup --dry-run --format text"),
    Check("first_screen", "MCP path", "README.md", "winchronicle codex install --dry-run"),
    Check("privacy_boundary", "Independent project", "README.md", "not affiliated with OpenAI"),
    Check("privacy_boundary", "Trust label", "README.md", 'trust = "untrusted_observed_content"'),
    Check("privacy_boundary", "Redaction first", "docs/privacy-architecture.md", "redaction"),
    Check("privacy_boundary", "No screenshots", "docs/privacy-architecture.md", "screenshots"),
    Check("privacy_boundary", "No desktop control", "docs/privacy-architecture.md", "desktop control"),
    Check("privacy_boundary", "No MCP write tools", "docs/privacy-architecture.md", "MCP write tools"),
    Check("fixture_demo", "Demo doc", "docs/quick-demo.md", "5-Minute Demo"),
    Check("fixture_demo", "Fixture-only shape", "docs/quick-demo.md", "without reading the live desktop"),
    Check("fixture_demo", "Quick demo script", "docs/quick-demo.md", "python harness/scripts/run_quick_demo.py"),
    Check("fixture_demo", "Fake helper boundary", "docs/quick-demo.md", "does not read the real desktop"),
    Check("fixture_demo", "Promotion kit", "docs/demo-promotion-kit.md", "English launch blurb"),
    Check("codex_entry", "Codex workday guide", "docs/codex-app-workday-guide.md", "Codex App Workday Guide"),
    Check("codex_entry", "Plugin doc", "docs/codex-workday-plugin.md", "Fastest Codex App Setup"),
    Check("codex_entry", "Record-only boundary", "docs/codex-workday-plugin.md", "Record-only"),
    Check("codex_entry", "Plugin source command", "docs/codex-workday-plugin.md", "winchronicle codex plugin --dry-run --format text"),
    Check("codex_entry", "MCP remains read-only", "docs/mcp-client-setup.md", "through six fixed tools"),
    Check("contributor_entry", "Contributing guide", "CONTRIBUTING.md", "Good First Contributions"),
    Check("contributor_entry", "Growth tasks", "CONTRIBUTING.md", "Growth And Trust Starter Tasks"),
    Check("contributor_entry", "Self-eval command", "CONTRIBUTING.md", "python harness/scripts/run_productization_self_eval.py"),
    Check("contributor_entry", "No observed content", "CONTRIBUTING.md", "do not commit observed content"),
    Check("contributor_entry", "Project presentation", "docs/project-presentation.md", "Good First Issue Themes"),
    Check("overclaim_risk", "No official-project claim", "README.md", "official openai project", "absent"),
    Check("overclaim_risk", "No records-everything claim", "README.md", "records everything", "absent"),
    Check("overclaim_risk", "No desktop-control claim", "README.md", "controls your desktop", "absent"),
    Check("overclaim_risk", "No screenshot-default claim", "README.md", "uses screenshots by default", "absent"),
    Check("overclaim_risk", "No cloud-memory claim", "README.md", "uploads your desktop", "absent"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Run deterministic productization self-eval.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD)
    args = parser.parse_args()

    payload = evaluate(args.threshold)

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(_format_text(payload))

    return 0 if payload["passed"] else 1


def evaluate(threshold: int = DEFAULT_THRESHOLD) -> dict[str, object]:
    files: dict[str, str] = {}
    failed: list[dict[str, str]] = []
    categories = sorted({check.category for check in CHECKS})
    category_totals = {category: 0 for category in categories}
    category_passed = {category: 0 for category in categories}

    for check in CHECKS:
        category_totals[check.category] += 1
        text = files.get(check.path)
        if text is None:
            path = ROOT / check.path
            if not path.exists():
                failed.append(_failure(check, "missing file"))
                continue
            text = path.read_text(encoding="utf-8")
            files[check.path] = text

        haystack = _normalize(text)
        needle = _normalize(check.needle)
        ok = needle not in haystack if check.mode == "absent" else needle in haystack
        if ok:
            category_passed[check.category] += 1
        else:
            reason = "forbidden phrase present" if check.mode == "absent" else "required phrase missing"
            failed.append(_failure(check, reason))

    score = round(100 * (len(CHECKS) - len(failed)) / len(CHECKS))
    category_scores = {
        category: round(100 * category_passed[category] / category_totals[category])
        for category in categories
    }
    failed_items = [
        f"{item['category']}: {item['name']} ({item['path']}: {item['reason']})"
        for item in failed
    ]

    return {
        "name": "WinChronicle productization self-eval",
        "score": score,
        "threshold": threshold,
        "passed": score >= threshold and not failed_items,
        "categories": category_scores,
        "failed_items": failed_items,
        "next_actions": _next_actions(failed_items),
        "boundary": {
            "does_not_run_live_uia": True,
            "does_not_read_desktop": True,
            "does_not_capture_observed_content": True,
            "checks_public_docs_and_static_metadata_only": True,
        },
    }


def _failure(check: Check, reason: str) -> dict[str, str]:
    return {
        "category": check.category,
        "name": check.name,
        "path": check.path,
        "reason": reason,
    }


def _normalize(text: str) -> str:
    return " ".join(text.lower().split())


def _next_actions(failed_items: list[str]) -> list[str]:
    if not failed_items:
        return [
            "Keep README first-screen copy compact.",
            "Refresh demo and social copy when user-facing behavior changes.",
            "Add new growth/trust checks only when they protect a real onboarding promise.",
        ]
    return [
        "Fix the listed missing or overclaiming items.",
        "Run python harness/scripts/run_productization_self_eval.py again.",
    ]


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
    for category, score in categories.items():
        lines.append(f"- {category}: {score}")

    failed = payload["failed_items"]
    if failed:
        lines.append("Failed items:")
        for item in failed:
            lines.append(f"- {item}")
    else:
        lines.append("Failed items: none")

    lines.append("Next:")
    for item in payload["next_actions"]:
        lines.append(f"- {item}")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
