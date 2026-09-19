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

The contract exposes `resolve(agreement_id)`. It builds a structured result from frozen constitution/evidence through the verified comparative API, then validates outcome enums and evidence IDs before mutation. No caller-supplied verdict, LLM prose, or stake amount controls transfers.

## Economics and security invariants

Payable stake value is separate from protocol fees. Matching requires exact equal value and a different caller. Confirmed outcomes credit the complete pot to the corresponding position; unresolved/invalid outcomes credit original stakes. Pull withdrawal prevents one recipient from blocking the other. State guards prevent self-match, double-match, post-close match, duplicate settlement, withdrawal replay, evidence without time/source authorization, and resolution without owned evidence.

## Lint and deterministic tests

- `genvm-lint lint contracts/resultline.py --json`: passed (3 checks).
- `genvm-lint check contracts/resultline.py --json`: passed; `Resultline`, 11 methods, 4 views, 7 writes.
- Read-only Studio Devnet `gen_getContractSchemaForCode`: passed; all public signatures and payable flags resolved.
- `pytest -q tests/contracts/test_resultline_contract.py`: **14 passed**.
- The existing `gltest` direct runner remains affected by the documented Windows temporary-stdin cleanup `PermissionError [WinError 32]`; no contract semantics were weakened.

The deterministic suite verifies source form, V1 scope, lifecycle method coverage, source allowlisting, evidence/resolve separation, enum/evidence ownership guards, settlement terminality, and absence of external services. It is not a substitute for consensus integration.

## Integration and temporary deployments

No Stage 2 RESULTLINE deployment was made. Stage 1 test-only web probes remain historical evidence:

- corrected runtime probe: `0xf0Ed635D8dE7Af93C4061d10caa587E3da3EAbf6`
- failure-path probe: `0x4573555cec78F641526fa15154E4372c526Cdcd7`

Neither is a RESULTLINE deployment. A representative end-to-end agreement/freeze/resolve/settle integration requires a second funded participant and an explicit bounded semantic adjudication integration pass; it remains the exact Stage 2 blocker.

## Known limitations

The contract is intentionally contract-first and has not been canonically deployed. The source stores bounded rendered text directly, while redirect/status/header metadata remain unavailable. Comparative semantic resolution, correction-window re-resolution, and real two-account payable integration still require a subsequent test-only pass. The Windows `gltest` cleanup defect remains local tooling, not a contract failure.

## Stage 2.1 Consensus Adjudication

### Previous boundary: unsafe placeholder

The previous public signature was `resolve(agreement_id, outcome, evidence_id)`. Any caller could supply a settlement enum; the contract did not invoke an LLM or comparative validator. This was an **UNSAFE PLACEHOLDER — NOT PRODUCTION ADJUDICATION**.

### Verified comparative API

The installed v0.6 RC library exposes `gl.eq_principle.prompt_comparative(fn, principle)`. The zero-argument callback produces the leader result; validators independently execute it and the runtime's `EqComparative` template compares leader and validator answers under the supplied principle. `prompt_non_comparative(fn, task=..., criteria=...)` is also verified and is now used for bounded evidence transcription.

### New resolution flow

`resolve(agreement_id)` is caller-triggered but caller cannot supply an outcome, reasoning, evidence ID, or replacement evidence. The contract builds context from frozen constitution/evidence only, invokes `gl.nondet.exec_prompt(..., response_format="json")` inside `prompt_comparative`, and validates the result before mutation.

Required keys are `outcome`, `source_authority`, `event_status`, `temporal_validity`, `subject_match`, `category_match`, `evidence_sufficiency`, and `evidence_ids_relied_on`. Outcomes are exactly `CONFIRMED_TRUE`, `CONFIRMED_FALSE`, `UNRESOLVED`, or `INVALID_EVENT`. Unknown/malformed/duplicate/cross-agreement evidence IDs fail closed.

The fixed instructions treat rendered material as untrusted data, ignore embedded prompts, forbid browsing/following links, odds, popularity, nominations, predictions, leaks, and invented facts, and distinguish insufficient evidence from false.

### Evidence-freeze equivalence audit

The previous raw-page `strict_eq` comparison was unsafe. `freeze_evidence` now uses verified `prompt_non_comparative` to produce a bounded factual transcription under fixed criteria. The stored value is capped at 512 characters; raw mutable page text is not strict-compared.

### Atomicity and deadline

Resolution, settlement, and withdrawal state are untouched until comparative adjudication and deterministic parsing succeed. Failed execution, malformed output, invalid evidence, or undetermined consensus leave frozen evidence and financial state unchanged. After the resolution deadline, `resolve(agreement_id)` records `UNRESOLVED` deterministically, enabling the refund branch.

### Tests and remaining blocker

The deterministic suite now reports **14 passing tests**. Read-only Studio Devnet schema compilation passes and exposes `resolve(agreement_id)` only. No real Studio Next semantic adjudication transaction has been submitted. The Windows direct runner still has `PermissionError [WinError 32]`; a second funded participant and real comparative/settlement integration remain before economic integration.

## Stage 2.2 Integration boundary (2026-09-19)

The pinned `genlayer@0.40.0-rc.3` CLI was audited before any deployment. Its `write` implementation constructs the transaction with `value: 0n` and exposes only protocol fee options (`--fees` / `--fee-value`); it has no payable-value option. RESULTLINE `create(...)` requires a non-zero payable stake, so the official CLI cannot submit the first agreement without bypassing the pinned path or exposing a private signing implementation. No Stage 2.2 deployment or transaction was made.

Non-mutating checks remain green: 14 deterministic tests, `genvm-lint lint`, and `genvm-lint check`. The configured Studio-dev account audit found funded named keystores, but the payable-value limitation is the first integration blocker. No frontend, backend, database, indexer, oracle, canonical deployment, or production RESULTLINE contract was created.

## Stage 2.2A Payable SDK Integration

The explicitly pinned packages were inspected from temporary tarballs: `genlayer-js@2.0.0-rc.1` and `@genlayer/transaction-kit@0.1.0-rc.2`. The official GenLayerJS type surface supports the required separation:

```ts
const fees = await client.estimateTransactionFeesForWrite({
  account, address, functionName, args,
});
const txHash = await client.writeContract({
  account, address, functionName, args,
  value: stake,
  fees: { distribution: fees.distribution, messageAllocations: fees.messageAllocations, feeValue: fees.feeValue },
});
```

`value` is payable contract value; `fees` is protocol/consensus funding. The write client uses an EIP-1193 provider and an authorized public account, then `waitForTransactionReceipt` awaits the requested decision/finalization status. Transaction Kit `0.1.0-rc.2` likewise submits `value: quote.userValue` separately from `fees` through its provider-backed flow.

The repository has no installed pinned SDK, no EIP-1193 provider for either configured keystore, and no safe official adapter that exposes those CLI-managed accounts to GenLayerJS. The CLI itself hardcodes `value: 0n`. Consequently no harness, deployment, payable create, or payable match was run, and Stage 2 remains blocked at account authorization/provider setup—not at RESULTLINE economics.

## Stage 2.2B EIP-1193 Integration Preparation

The `.git` directory has an explicit Windows deny ACL for the repository SID, including write/delete rights on `.git/index` and its children. No stale lock or active Git process exists. A harmless write inside `.git` is denied; the smallest safe repair is for the repository owner/administrator to remove only that explicit deny ACE (or grant the current user Modify on `.git`), then re-run Git. No ACL was changed by this task. `.pytest_cache` is likewise inaccessible and was left untouched.

Added the test-only harness `tests/integration/studio_next_eip1193.ts` and instructions in `tests/integration/README.md`. It requires a browser EIP-1193 provider, checks chain 61997 before writes, estimates fees with `estimateTransactionFeesForWrite`, submits `value` separately from `fees`, waits for finalization, and rejects identical participant accounts. It contains no secrets and does not execute transactions by itself.

Interactive user action remains required: connect an authorized browser wallet on Studio-dev (chain 61997), then authorize Participant A and later a distinct Participant B. No deployment, create, match, evidence, resolution, settlement, or withdrawal has been attempted.

## Stage 2.2C deployment postflight boundary

The user-approved browser flow reported that the deployment request returned, but the runner did not preserve the returned transaction identifier. Read-only standard RPC inspection confirmed chain `61997` and the canonical Studio endpoint, but `eth_getBlockByNumber` exposes empty transaction lists on Studio Dev and therefore cannot identify this GenLayer deployment by sender alone. No transaction hash, receipt, execution status, consensus decision, finalization, deployed address, schema, or deployed-code identity is asserted here. No follow-up transaction was submitted.
