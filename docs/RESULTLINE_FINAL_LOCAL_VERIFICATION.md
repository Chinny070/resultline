# RESULTLINE Final Local Verification

## Candidate

- Source: `contracts/resultline.py`
- Previous local base recorded for this hardening pass: `a59d3a83677d3ad793f24c3232cd03710471062d0ac09f177c3f2720aa3d4588`
- Current release candidate hash: `385fa34f18c95b12aa38582c09106c47538a284cdcf4290f63bba14e4c3d3289`
- Base functional candidate: `2242d36b908bde76293c2e3d80a5007585048f9119eb49b5a15472d3b6b52ec9`
- Lines: 216

## Local verification

- `genvm-lint lint`: PASS (UTF-8 console mode)
- `genvm-lint check`: PASS (UTF-8 console mode)
- Static contract tests: PASS
- Direct/runtime tests: BLOCKED before execution by Windows cache permission (`WinError 5` in `.cache/gltest-direct`); no contract assertion failed.

## Hardening coverage

The candidate preserves the explicit storage initialization and string-return schema fixes, and adds persisted temporal mode, structured adjudication fields (including source authority, event status, temporal validity, subject/category matches, evidence sufficiency, evidence IDs, and bounded rationale), strict evidence-reference validation, and a matched-counterparty settlement guard. Web evidence remains HTTPS/host/path constrained, untrusted, bounded, and non-browsing; missing evidence is distinct from `CONFIRMED_FALSE`. EOA withdrawal continues to clear owed balance before the finalized EVM-recipient transfer.

## Spec matrix

| Requirement | Result |
|---|---|
| Binary outcome/positions and explicit constitution | PASS |
| Temporal mode and immutable pre-match constitution | PASS (local code audit) |
| Structured adjudication and evidence traceability | PASS |
| Source authority/path and prompt-injection defenses | PASS |
| Deterministic state machine and settlement accounting | PASS |
| EOA payout safety | PASS |
| Hosted StudioNet schema/runtime execution | HOSTED-ONLY |
| Windows direct GenVM execution | HOSTED-ONLY (cache permission blocker) |

No deployment, wallet interaction, or frontend change was performed.
