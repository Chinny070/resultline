# RESULTLINE Stage 2 Contract Verification

Status: contract-first implementation complete; no frontend, backend, database, indexer, or canonical deployment was created.

## Implemented V1 scope

`contracts/resultline.py` implements a narrow two-party binary agreement for `AWARD_WINNER` and `COMPETITION_WINNER`. `BOX_OFFICE_MILESTONE` is excluded. Positions are `YES` and `NO`; the counterparty is fixed to the opposite side.

## Storage model

The contract uses scalar fields plus typed `DynArray` collections for agreements and append-only evidence, and a typed `TreeMap[Address, u256]` withdrawal ledger. Stored data is bounded: 512-character text/URL fields, four evidence records per agreement, and no floats, runtime response objects, model objects, or arbitrary persisted dictionaries.

The constitution stores outcome type, proposition, subject, category, organizer, event ID, approved HTTPS host/path, position, stake, temporal bounds, and correction window. A cryptographic constitution fingerprint is not fabricated because the verified RC helper was not established; the source fields are stored directly and remain immutable after creation/matching.

## Lifecycle

`OPEN → MATCHED → EVIDENCE_FROZEN → RESOLVED → SETTLED`; unmatched creators may `CANCELLED`. Every write validates prior state, time ordering, caller identity, equal stake, evidence ownership, and terminal replay guards.

## Evidence architecture

`freeze_evidence` is separate from `resolve` and `settle`. It deterministically requires an HTTPS URL under the frozen host/path rule, retrieves with `gl.nondet.web.render(url, mode="text")` inside `strict_eq`, bounds the representation, appends URL/text/length/fingerprint/timestamp, and never overwrites earlier evidence. Retrieval failure occurs before evidence arrays are mutated and therefore fails closed.

The contract does not depend on final URL, redirect chain, status, headers, or content type, which Stage 1 did not expose. Raw HTML is not required for V1.

## Semantic adjudication

The current contract exposes a defensive `resolve(agreement_id, outcome, evidence_id)` boundary for the structured result that a later comparative leader/validator flow must supply. It accepts only `CONFIRMED_TRUE`, `CONFIRMED_FALSE`, `UNRESOLVED`, or `INVALID_EVENT`, and verifies that the evidence ID belongs to the agreement. No LLM prose or stake amount controls transfers. Comparative equivalence and prompt construction remain the next integration increment; no arbitrary model API was invented.

## Economics and security invariants

Payable stake value is separate from protocol fees. Matching requires exact equal value and a different caller. Confirmed outcomes credit the complete pot to the corresponding position; unresolved/invalid outcomes credit original stakes. Pull withdrawal prevents one recipient from blocking the other. State guards prevent self-match, double-match, post-close match, duplicate settlement, withdrawal replay, evidence without time/source authorization, and resolution without owned evidence.

## Lint and deterministic tests

- `genvm-lint lint contracts/resultline.py --json`: passed (3 checks).
- `genvm-lint check contracts/resultline.py --json`: passed; `Resultline`, 11 methods, 4 views, 7 writes.
- Read-only Studio Devnet `gen_getContractSchemaForCode`: passed; all public signatures and payable flags resolved.
- `pytest -q tests/contracts/test_resultline_contract.py`: **11 passed**.
- The existing `gltest` direct runner remains affected by the documented Windows temporary-stdin cleanup `PermissionError [WinError 32]`; no contract semantics were weakened.

The deterministic suite verifies source form, V1 scope, lifecycle method coverage, source allowlisting, evidence/resolve separation, enum/evidence ownership guards, settlement terminality, and absence of external services. It is not a substitute for consensus integration.

## Integration and temporary deployments

No Stage 2 RESULTLINE deployment was made. Stage 1 test-only web probes remain historical evidence:

- corrected runtime probe: `0xf0Ed635D8dE7Af93C4061d10caa587E3da3EAbf6`
- failure-path probe: `0x4573555cec78F641526fa15154E4372c526Cdcd7`

Neither is a RESULTLINE deployment. A representative end-to-end agreement/freeze/resolve/settle integration requires a second funded participant and an explicit bounded semantic adjudication integration pass; it remains the exact Stage 2 blocker.

## Known limitations

The contract is intentionally contract-first and has not been canonically deployed. The source stores bounded rendered text directly, while redirect/status/header metadata remain unavailable. Comparative semantic resolution, correction-window re-resolution, and real two-account payable integration still require a subsequent test-only pass. The Windows `gltest` cleanup defect remains local tooling, not a contract failure.
