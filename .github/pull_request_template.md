## Summary

-

## Validation

- Before implementation, read `AGENTS.md`, `docs/roadmap.md`, `README.md`,
  `docs/codex-long-term-goal.md`, and the files, tests, fixtures, schemas,
  scorecards, or docs affected by the task.
- Reading `docs/codex-long-term-goal.md` gives direction only; it is not
  release authorization, not automatic maintenance authorization, and not
  approval for broad evidence sweeps, release or publish actions, or
  capture-surface expansion.
-
- If this changes `README.md` or `README.zh-CN.md` Workday guidance, include `python -m pytest tests/test_readme_daily_workflow.py -q` and `python harness/scripts/run_productization_self_eval.py --format json` in validation.
- If this changes `contract_coverage`, cite `CONTRIBUTING.md` `Command Plan Contract Coverage` instead of copying its commands here; that shared paragraph owns the command plan JSON check plus the workflow test that runs the schema, pytest-node, and artifact-path gates.
- New `contract_coverage` entries must update the README navigation, the Current coverage examples table, the JSON command plan, and at least one focused pytest node in the same change.

## Privacy and scope

- Product CLI/MCP shape unchanged unless explicitly called out.
- If this changes MCP result examples, metadata, or schema, `mcp-tool-result.schema.json` still preserves trust, metadata-only, and evidence-policy guardrails.
- No new screenshot/OCR/audio/keyboard/clipboard/network/LLM/desktop-control surface unless explicitly called out.
- No observed-content artifact, local state, raw helper JSON, raw watcher JSONL, generated capture, generated memory, secret, or password committed.
