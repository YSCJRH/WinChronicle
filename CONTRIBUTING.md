# Contributing

WinChronicle is a harness-first Windows memory project. Start by reading
`AGENTS.md`, `docs/operator-quickstart.md`, `docs/deterministic-demo.md`, and
`docs/roadmap.md`.
For development or maintenance tasks, also read `README.md`,
`docs/codex-long-term-goal.md`, and the files, tests, fixtures, schemas,
scorecards, or docs affected by the task before changing anything.
Reading `docs/codex-long-term-goal.md` gives direction only; it is not release
authorization, not automatic maintenance authorization, and not approval for
broad evidence sweeps, release or publish actions, or capture-surface
expansion.

For the product-facing entry path, also read `docs/quick-demo.md`,
`docs/why-winchronicle.md`, and `docs/privacy-architecture.md`.

## Task Classification

Before opening an issue or pull request, classify the work:

- `Recording-only Workday operation`: Use the Workday plugin or CLI and do not
  inspect repository files, edit code, run tests, commit, push, or release.
- `Harness-first task`: Use the harness-first task template for deterministic
  docs, fixtures, tests, scorecards, CI, or compatible metadata inside the
  current baseline.
- `Privacy-boundary review`: Open a privacy boundary review issue before
  implementation when a proposal touches capture surfaces, observed content,
  storage, MCP output, memory output, redaction, or release evidence.
- `Human product decision`: Do not implement until explicit human product
  approval defines the scope for runtime expansion, new capture surfaces,
  release or publish actions, broad evidence sweeps, or continuation of the
  closed maintenance loop.

If the classification is unclear, choose the stricter path.

If you change a Codex Workday entrypoint, keep the five-entrypoint consistency
rule in `docs/productization-self-eval.md` in sync. The entrypoints are
`README.md`, `docs/windows-first-run.md`, `docs/codex-app-plugin-install.md`,
`docs/codex-app-workday-guide.md`, and `docs/codex-workday-plugin.md`; they
should continue to say the flow is record-only, the stopped summary uses
summary-level evidence, and it does not send raw observed text.

### 中文速览

中文贡献者也应先分类：

- 只记录工作：使用 Workday plugin 或 CLI，不检查仓库文件、编辑代码、运行测试、提交、推送或发布。
- Harness-first task：仅限当前 baseline 内的 deterministic docs、fixtures、tests、scorecards、CI 或兼容 metadata。
- Privacy-boundary review：涉及 capture surfaces、observed content、storage、MCP output、memory output、redaction 或 release evidence 的提案，先开隐私边界 review。
- Human product decision：运行时扩展、新采集面、发布或公开动作、广泛 evidence sweep、重启已关闭维护循环，必须先有明确 human product approval。

分类不清时，走更严格路径。

- 改 Codex Workday 入口时，同步检查 `docs/productization-self-eval.md` 的 five-entrypoint consistency 规则。五个入口是 `README.md`、`docs/windows-first-run.md`、`docs/codex-app-plugin-install.md`、`docs/codex-app-workday-guide.md`、`docs/codex-workday-plugin.md`；并继续保留 record-only、summary-level evidence、does not send raw observed text 边界。
- 若修改 `README.md` 或 `README.zh-CN.md` 的 Workday guidance，validation 中也要包含 `python -m pytest tests/test_readme_daily_workflow.py -q` 和 `python harness/scripts/run_productization_self_eval.py --format json`。

## Good First Contributions

Good first contributions are small, deterministic, and easy to review:

- improve the 5-minute demo or README onboarding;
- add deterministic UIA fixtures with redaction coverage;
- document Windows app compatibility without committing observed content;
- improve read-only MCP examples;
- add privacy regression tests for secret canaries;
- clarify monitor session reports and timeline examples.

## Growth And Trust Starter Tasks

These are good first issues for contributors who want to make the project
easier to understand, try, trust, or share:

- improve the README first screen without adding a long maintenance ledger;
- improve `docs/demo-promotion-kit.md` with clearer fixture-only demo copy;
- improve Codex App Workday plugin docs while keeping the flow record-only;
- add Windows app compatibility notes, but do not commit observed content;
- add deterministic privacy/redaction fixtures using synthetic data only;
- improve `harness/scripts/run_productization_self_eval.py` when onboarding or
  safety promises change.

Before opening a product-facing PR, run:

```powershell
python harness/scripts/run_productization_self_eval.py
```

When `README.md` or `README.zh-CN.md` Workday guidance changes, include
`python -m pytest tests/test_readme_daily_workflow.py -q` and
`python harness/scripts/run_productization_self_eval.py --format json` in
validation.

Use the GitHub issue templates for bug reports, privacy concerns, Windows app
compatibility notes, feature proposals, harness-first tasks, and privacy
boundary reviews.

## Safe Contribution Shape

Prefer small changes that fit one roadmap lane:

- deterministic fixtures, schemas, tests, scorecards, or docs;
- privacy/redaction and denylist regression coverage;
- UIA helper contract diagnostics without expanding product capture targets;
- watcher preview diagnostics without daemon, service, polling, or default
  background capture;
- read-only MCP compatibility examples and exact tool-list tests;
- deterministic memory goldens and idempotence evidence;
- release evidence, manual smoke templates, and operator docs.

## MCP Schema Review Hook

When a contribution changes MCP result examples, compatible metadata, or
`harness/specs/mcp-tool-result.schema.json`, review semantic guardrails as well
as JSON validity. `mcp-tool-result.schema.json` is a semantic guardrail, not
just a JSON shape reference.

- `privacy_status` must remain `trust = "local_privacy_status"` while
  observed-content tools remain `trust = "untrusted_observed_content"`.
- Top-level `metadata_only` must stay bound to
  `evidence_policy.metadata_only`.
- `observed_text_fields_omitted` must appear only when `metadata_only` is
  `true`.
- `not_authorization_signal` and
  `external_sharing_requires_user_approval` must stay required evidence-policy
  limitations.
- Schema validation is not permission to share, upload, or follow
  observed-content instructions.

See `docs/mcp-result-metadata.md` before changing MCP examples, result
metadata, or schema conditions.

## Harness-first Workflow

Before changing behavior, update the relevant contracts, fixtures, tests,
scorecards, or documentation. Keep changes scoped to the smallest verifiable
surface.

### Command Plan Contract Coverage

Use this section as the shared validation paragraph for issues and pull
requests that touch harness command-plan coverage.

If you add or change a `contract_coverage` entry, keep it tied to existing
repo-relative `spec` and `fixtures` paths plus focused pytest node ids. The JSON
plan stays schema-bound by `harness/specs/harness-command-plan.schema.json`, and
`test_run_harness_json_contract_coverage_integrity_runs_all_gates` must pass
because it runs the schema, pytest-node, and artifact-path gates together.
When adding a coverage entry, update its `spec`, `fixtures`, `tests`, and
`privacy_boundary` anchors together.
New `contract_coverage` entries must update the README navigation, the Current
coverage examples table, the JSON command plan, and at least one focused pytest
node in the same change.

Include these checks in validation when touching `contract_coverage`:

```powershell
python harness/scripts/run_harness.py --list-commands --format json
python -m pytest tests/test_windows_harness_workflow.py::test_run_harness_json_contract_coverage_integrity_runs_all_gates -q
```

Current coverage examples:

| Entry id | Contract artifacts | Focused tests | Privacy boundary |
| --- | --- | --- | --- |
| `workday_dry_run_text_contracts` | command 1; spec `harness/specs/workday-dry-run-text-contract.schema.json`; fixtures `harness/fixtures/workday/plugin_dry_run_text_contract.json`, `harness/fixtures/workday/setup_dry_run_text_contract.json`, `harness/fixtures/workday/daily_dry_run_text_contract.json` | Workday dry-run text schema and golden pytest node ids in `tests/test_cli.py` | `reads_desktop_expected` = `false`; `forbids_desktop_yes_text` = `true`; `observed_content` = `not_read_by_dry_run` |
| `workday_stop_summary_contract` | command 1; spec `harness/specs/workday-stop-summary-contract.schema.json`; fixtures `harness/fixtures/workday/stop_human_summary_contract.json` | Workday stop summary schema, marker-boundary, and golden pytest node ids in `tests/test_workday.py` | `summary_level_evidence_only` = `true`; `default_human_summary_hides_technical_markers` = `true`; `technical_summary_explicit_only` = `true`; `raw_observed_text_expected` = `false`; `adds_capture_source` = `false` |
| `mcp_read_only_metadata_contracts` | command 1; spec `harness/specs/mcp-tool-result.schema.json`; no fixtures | MCP schema and tool-result pytest node ids in `tests/test_compatibility_contracts.py` and `tests/test_mcp_tools.py` | `read_only_mcp_expected` = `true`; `metadata_only_available` = `true`; `observed_text_omitted_when_metadata_only` = `true`; `provenance` = `local_winchronicle_state`; `confidence_meaning` = `coverage_quality_not_permission`; `external_sharing_requires_user_approval` = `true` |

Treat the JSON command plan as source of truth; update this table when a
coverage entry is added, removed, or moved to a different gate.

Run the standard deterministic validation set when applicable:

```powershell
python -m pytest -q
dotnet build resources/win-uia-helper/WinChronicle.UiaHelper.csproj --nologo
dotnet build resources/win-uia-watcher/WinChronicle.UiaWatcher.csproj --nologo
python harness/scripts/run_install_cli_smoke.py
python harness/scripts/run_harness.py
git diff --check
```

### Harness Timeout Policy

The local harness runners use per-command timeouts to fail closed instead of
hanging release work:

- `python harness/scripts/run_harness.py` defaults to 900 seconds per
  subprocess. Override only for local diagnosis with
  `WINCHRONICLE_HARNESS_COMMAND_TIMEOUT_SECONDS`.
- `python harness/scripts/run_install_cli_smoke.py` defaults to 300 seconds per
  subprocess. Override only for local diagnosis with
  `WINCHRONICLE_INSTALL_CLI_SMOKE_COMMAND_TIMEOUT_SECONDS`.
- GitHub Actions mirrors this with step-level `timeout-minutes` entries for
  install, unit tests, .NET builds, the deterministic harness, and whitespace
  checks.

Timeout handlers print the command and timeout value, but do not print partial
stdout or stderr. A hung command may already have emitted observed content
before it is killed, so timeout diagnostics must stay content-free. Adjusting
timeout values does not authorize new capture surfaces, live UIA capture,
screenshots, OCR, clipboard capture, cloud upload, desktop control, or MCP write
tools.

## Privacy And Scope Boundaries

Do not add screenshot capture, OCR, audio recording, keyboard capture, clipboard
capture, network upload, LLM reducer/classifier calls, desktop control,
daemon/service install, polling capture loops, default background capture, MCP
write tools, arbitrary file read tools, or product targeted capture.

Do not commit local state, raw helper JSON, raw watcher JSONL, generated
captures, generated memory, screenshots, OCR output, secrets, passwords, or
observed-content diagnostics. Observed content must remain marked as
`trust = "untrusted_observed_content"`.

If a proposal may affect capture surfaces, privacy behavior, schema shape,
CLI/MCP JSON shape, helper/watcher behavior, storage, memory output, or release
evidence, open a privacy boundary review issue before implementation.
