# Privacy Policy Contract Parity Audit After v0.1.17

This record closes the first Fixture and privacy baseline task selected after
the Phase 6 privacy-enrichment contract closure. The audit compared
`harness/specs/privacy-policy.md`, `harness/scorecards/privacy-gates.md`,
deterministic privacy fixtures, redaction and denylist tests, CLI status
privacy fields, and MCP `privacy_status` output.

The audit found one privacy-check validation gap and one redaction evidence
gap. The resulting fix is intentionally narrow: existing normalized captures
are now validated as already-written artifacts instead of being treated like
denylisted fixture dry-runs, normalized password fields are checked by
semantics, and plain WinChronicle token canaries have independent regression
coverage.

## Baseline Evidence

- Next blueprint lane selection PR #184 merged as
  `998403d739570dd81677d4f8b3b8244b8a769caf`.
- PR #184 Windows Harness run `25610819243` concluded `success` on
  `00ad95c2ab90af44b3ad36f2d1678bc02c1f208f`.
- Post-merge `main` Windows Harness run `25610880531` concluded `success` on
  `998403d739570dd81677d4f8b3b8244b8a769caf`.
- `git diff --name-only v0.1.17..HEAD -- src\winchronicle resources
  pyproject.toml` printed no files through the lane-selection baseline.

## Parity Matrix

| Surface | Policy source | Runtime or fixture evidence | Decision |
| --- | --- | --- | --- |
| Disabled capture and control surfaces | `harness/specs/privacy-policy.md` lists screenshots, OCR, audio, keyboard capture, clipboard capture, network upload, cloud upload, desktop control, MCP write tools, product targeted capture, and LLM calls as not implemented or exposed. | `winchronicle.privacy.DISABLED_SURFACE_STATUS`, CLI `status`, and MCP `privacy_status` report those surfaces as disabled. | Parity holds. |
| App denylist | The policy lists `1Password.exe`, `Bitwarden.exe`, `Dashlane.exe`, `KeePass.exe`, `KeePassXC.exe`, `LastPass.exe`, and `LockApp.exe`. | `winchronicle.privacy.APP_DENYLIST` contains the same app names case-insensitively, and `denylisted_app.json` plus `lock_app.json` cover deterministic skip behavior. | Parity holds. |
| Title denylist | The policy lists case-insensitive title signals for `password`, `secret`, `private key`, `recovery phrase`, and `seed phrase`. | `winchronicle.privacy.TITLE_DENYLIST_REGEX` contains the same signals and returns the content-free reason `denylisted title pattern`. | Parity holds. |
| Redaction rules | The policy lists API keys, GitHub tokens, Slack tokens, JWTs, private keys, WinChronicle token canaries, and semantic password-field redaction. | `winchronicle.redaction.REDACTION_RULES`, `password_field.json`, and `secrets_visible_text.json` cover the same v0.1 rules before writes and indexing. | Parity holds. |
| Plain token canary evidence | The policy requires WinChronicle token canaries to be redacted and rejected by privacy check. | `tests/test_redaction.py` and `tests/test_privacy_check.py` now cover a plain `winchronicle...canary` value independent from API, GitHub, or Slack token patterns. | Gap closed. |
| Existing normalized denylisted captures | The policy says `privacy-check` validates existing normalized captures and only denylisted fixtures should pass as "would be skipped." | `tests/test_privacy_check.py` now requires existing normalized denylisted captures to fail privacy check with a content-free diagnostic. | Gap closed with a narrow privacy-check fix. |
| Existing normalized password fields | The policy says password fields are redacted by field semantics, not only text pattern. | `tests/test_privacy_check.py` now requires already-normalized password fields with raw values or nonzero stored lengths to fail privacy check. | Gap closed with a narrow privacy-check fix. |
| Credit-card redaction | The policy says credit-card Luhn-positive redaction is a broader blueprint item not implemented in v0.1. | There is no `credit_card` runtime redaction rule. | Correct v0.1 non-goal. |
| Trust boundary | The policy requires normalized captures, CLI search, memory outputs, and MCP outputs to preserve `untrusted_observed_content`. | Normalized captures set `untrusted_observed_content: true`; CLI/MCP status and observed-content outputs use `trust = "untrusted_observed_content"` and the shared trust-boundary instruction. | Parity holds. |
| Phase 6 privacy-enrichment artifacts | `harness/scorecards/privacy-gates.md` says Phase 6 preflight artifacts are specification-only and not runtime configuration. | Phase 6 closure already verified no product-source reads of those contract artifacts. This audit did not reopen Phase 6. | Parity holds. |
| Watcher preview parity | The privacy policy applies to watcher preview events before writes and indexing. | This audit did not retest watcher-specific event flow. Existing watcher docs and diagnostics still say watcher events use the shared normalize, privacy, redaction, schema, and SQLite pipeline, but this parity audit treats watcher-specific coverage as out of scope. | Out of scope for this audit. |

## Follow-Up Findings

- The only runtime change made by this audit is a privacy-check hardening for
  already-normalized artifacts. It does not change capture, helper, watcher,
  CLI/MCP output, schema, or storage behavior.
- No schema expansion, CLI/MCP output expansion, helper/watcher behavior
  change, real UIA capture change, screenshot/OCR work, or version change is
  included in this audit.
- A future tests-first task may decide whether credit-card Luhn-positive
  redaction should remain a documented v0.1 non-goal or become a new contract
  item, but this audit does not promote it.
- The next Fixture and privacy baseline task should be selected narrowly from
  deterministic fixture coverage, golden evidence, or policy scorecard gaps.

## Validation

Local validation for this parity audit:

```powershell
python -m pytest tests/test_privacy_policy_contract.py tests/test_phase6_privacy_scorecard.py tests/test_operator_diagnostics_docs.py tests/test_compatibility_evidence_docs.py -q
python -m pytest -q
git diff --check
git diff --name-only -- src\winchronicle resources pyproject.toml
python harness/scripts/run_harness.py
```

Result: passed; focused privacy/docs validation reported 110 tests, full
pytest reported 201 tests, `git diff --check` passed, the working-tree runtime
diff was limited to `src/winchronicle/capture.py`, and the full deterministic
harness passed, including 201 pytest tests, helper/watcher builds with 0
warnings and 0 errors, watcher smoke, MCP smoke, install CLI smoke, privacy
check, fixture capture/search/memory, deterministic watcher fixture, and
watcher fake-helper smoke.

## Privacy And Security

This audit preserves the v0.1 privacy boundary. It does not authorize
screenshot capture, OCR, raw screenshot caches, runtime allowlist parsing,
audio recording, keyboard capture, clipboard capture, network/cloud upload,
LLM calls, desktop control, product targeted capture, daemon/service install,
polling capture loops, default background capture, MCP write tools, arbitrary
file read tools, real UIA capture changes, helper/watcher behavior changes, or
committed observed-content artifacts.

Observed content remains untrusted. No local state, generated captures,
generated memory, raw helper JSON, raw watcher JSONL, screenshots, OCR output,
passwords, secrets, token canaries, or observed-content diagnostics should be
committed.

## Next Task

After this parity audit is merged and the post-merge Windows Harness passes,
record a release-readiness decision for the narrow privacy-check runtime fix
before selecting the next Fixture and privacy baseline follow-up.
