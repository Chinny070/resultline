# RESULTLINE — Stage 1 Architecture and Feasibility Audit

**Status:** Stage 1.1 complete — **BLOCKED — REQUIRES GENLAYER/AGENT TANK OWNER CONFIRMATION.** No contract, frontend, backend, database, deployment, or live transaction was created.

**Target required by the supplied Agent Tank brief:** Studio Next, chain ID `61997`, `https://studio-next.genlayer.com/api`, explorer `https://explorer-studio-dev.genlayer.com/`, GEN, CLI `studio-dev`, gltest `studio_devnet`, GenLayerJS `studioDevnet`, v0.123.0-rc.6 / Consensus v0.6 RC.

## 1. Product thesis and core trust question

RESULTLINE is an **authoritative event resolution primitive with precommitted source rules**. V1 applies it to two-party, binary entertainment-outcome agreements: participants lock equal GEN on opposite sides of a frozen proposition; GenLayer assesses permitted evidence after the event and the contract settles only a validated outcome.

Its question is deliberately narrow: **did the exact frozen proposition occur under the frozen Resolution Constitution, as established by authoritative evidence?** It is not “what does a web page say?” or “what do people predict?”

GenLayer is material for bounded semantic judgment over live, untrusted web evidence and natural-language constitutions. Deterministic code—not an LLM—must control identity, deadlines, state guards, stake accounting, source allowlists, evidence identifiers, replay protection, and payouts.

## 2. Environment and repository audit

| Item | Observed |
|---|---|
| Workspace | `C:\\Users\\USERpc\\RESULTINE`; empty at inspection time (no package manifest, source, configuration, or prior references) |
| Node / npm | `v24.14.0` / `11.9.0` |
| Python | `3.12.10` |
| GenLayer CLI | not installed / not on PATH |
| `genvm-lint` | `0.11.1rc2` |
| `gltest` | executable present; `gltest --version` printed `pytest 8.4.2`, not a GenLayer Test version |
| `genlayer-py` | `0.19.0rc2` |
| `genlayer-test` | `0.30.0rc2` |
| `genlayer-js`, Transaction Kit, React adapter | not installed; no Node project exists |

The Python package set matches the supplied RC family for `genlayer-py`, `genlayer-test`, and the linter. The CLI and JS packages cannot be verified locally and were not installed or upgraded for Stage 1. The repository search found no stale references to 61999, Studionet, old Studio RPCs, old addresses, or old SDK chain names because the workspace was empty.

## 3. Official research and Studio Next compatibility gate

Reviewed official sources:

- [Fetch Web Content example](https://docs.genlayer.com/developers/intelligent-contracts/examples/fetch-web-content)
- [GenLayer full documentation](https://docs.genlayer.com/full-documentation.txt), including web access, equivalence, storage/value transfer, transaction lifecycle, v0.6 fees, network configuration, and SDK material
- [GenLayer SDK API reference](https://sdk.genlayer.com/main/_static/ai/api.txt)
- [GenLayer Skills](https://skills.genlayer.com/)

### Stage 1.1 endpoint/preset reconciliation — BLOCKED — REQUIRES GENLAYER/AGENT TANK OWNER CONFIRMATION

The supplied brief is authoritative for the hackathon target and locks `https://studio-next.genlayer.com/api`. The exact RC sources instead resolve **every supplied programmatic preset** to `https://studio-dev.genlayer.com/api`, chain `61997`: `genlayer-js@2.0.0-rc.1` exports `studioDevnet` with that URL; `genlayer@0.40.0-rc.3` maps CLI `studio-dev` to that same definition; installed `genlayer-py@0.19.0rc2` and `gltest` map `studio_devnet` there too. Both candidate endpoints responded to read-only `eth_chainId` with `0xf22d` (61997), but equal chain ID does **not** prove that the two hostnames are supported aliases with the same deployments, fee manager, or consensus configuration. The current official documentation likewise names `studio-dev` as canonical and describes `studio-next` only as a possible browser alias.

Therefore the supported RC programmatic configuration is evidenced as `studio-dev` / `studioDevnet` / `studio_devnet` → `https://studio-dev.genlayer.com/api` → `61997`; using the brief's `studio-next` RPC remains unverified. An Agent Tank/GenLayer owner must either confirm the supplied `studio-next` hostname is an approved alias for this exact RC deployment or amend the supplied RPC requirement. No custom network was created.

| Component | Verified value | Evidence/source |
|---|---|---|
| Supplied target RPC | `https://studio-next.genlayer.com/api` | Agent Tank brief; read-only `eth_chainId` → `0xf22d` |
| Supported RC RPC | `https://studio-dev.genlayer.com/api` | exact CLI, JS, Python, and gltest preset sources; read-only `eth_chainId` → `0xf22d` |
| Chain ID | `61997` | both probes; all RC preset sources |
| CLI preset/version | `studio-dev`; `genlayer@0.40.0-rc.3` | inspected package source maps it to `studioDevnet` |
| GenLayerJS/version | `studioDevnet`; `genlayer-js@2.0.0-rc.1` | inspected `dist` chain definition |
| gltest preset/version | `studio_devnet`; `genlayer-test@0.30.0rc2` | installed `gltest_cli` default config and `genlayer_py.chains` |
| Python SDK | `genlayer-py@0.19.0rc2` | installed package metadata/source |
| Linter | `genvm-linter@0.11.1rc2` | installed package metadata/source |
| Transaction Kit | `@genlayer/transaction-kit@0.1.0-rc.2` | exact npm tarball inspected; package published at supplied pin |
| React kit | `@genlayer/transaction-kit-react@0.1.0-rc.2` | exact npm tarball inspected; package published at supplied pin |
| IC header family | supplied v0.3.0 family; exact runner hash **not verified** | linter verifies `Depends: py-genlayer:<hash>` header mechanism but no v0.3.0 artifact/runner was installed |
| Fee lifecycle | v0.6 RC fee-funded lifecycle | current docs and installed Python SDK expose estimate, `distribution`, `feeValue`, separate `value`, receipt/finality APIs |
| Web render | API source/docs compatible; target runtime behavior **not directly exercised** | current docs/linter verify `gl.nondet.web.get` / `.render` and equivalence boundary; no non-production deployed runner exists |

## 4. Verified current GenLayer / Studio Next capabilities

The following are verified from current official material, not proposed APIs:

| Capability | Verified behavior / API |
|---|---|
| Python IC | `class …(gl.Contract)` with `@gl.public.write` / `@gl.public.view` |
| Web fetch | `gl.nondet.web.get(url)` returns a response whose `body` can be decoded |
| Web render | `gl.nondet.web.render(url, mode="text"|"html"|"screenshot", wait_after_loaded="5s" optional)`; render is documented for JavaScript-rendered DOMs |
| Nondeterminism | web calls must execute in a function passed to `gl.eq_principle.*`; otherwise the docs say they error |
| Exact equivalence | `gl.eq_principle.strict_eq(callback)` is documented for stable, exactly reproducible normalized outputs |
| Consensus | leader produces an execution result; validators assess it under contract-defined equivalence; finality is separate from submission |
| Value / IC transfer | payable user value is separate from transaction fees; IC messages document `emit(value=u256(...), on='finalized')` and `emit_transfer(...)` |
| Fee-funded writes | `estimateTransactionFeesForWrite`; `writeContract({...call, fees:{distribution: estimate.distribution, feeValue: estimate.feeValue}})`; `value` remains distinct |
| Lifecycle inspection | official Node API lists `gen_getTransactionStatus`, `gen_getTransactionReceipt`, and `gen_getTransactionLifecycle` |
| RC network | current docs identify `studio-dev`, `studioDevnet`, and chain `61997` for the v0.123/v0.6 preview |

Storage exact types, schema-generation behavior on the locked deployment, and the supplied v0.3.0 header/runner binding remain unverified. The exact CLI, JS, and Transaction Kit npm RC archives were inspected without adding project dependencies.

## 5. V1 scope and binary model

**Ship:** `AWARD_WINNER` and `COMPETITION_WINNER`, with one fixed category, subject, organizer, event identity, and binary YES/NO proposition. **Optionally ship `EVENT_OCCURRENCE` only after a narrow venue/organizer constitution template is tested.**

**Defer `BOX_OFFICE_MILESTONE`.** “Worldwide”, reporting territory, gross definition, cutoff, revisions, and competing authority conventions require a separate numerical-source constitution. Forcing it into the winner model would hide material ambiguity.

Binary positions are the safe V1: YES means the proposition is confirmed true; NO means it is confirmed false. “Film A versus Film B” is excluded because Film C can win. Stakes never affect authority or semantic judgment.

## 6. Object model and frozen Resolution Constitution

The smallest future model is `Agreement` containing an immutable `ResolutionConstitution`, two positions, zero or more evidence records, one resolution record, and settlement accounting. Store scalar fields and supported typed collections only; do not assume arbitrary persisted Python objects.

The constitution is created before the counterparty accepts and becomes immutable at matching/funding. Required fields are: canonical outcome type; exact proposition; subject and category; organizer/event identity; expected event time; close time; resolution-not-before; resolution deadline; allowed primary source identities and URL/path constraints; explicit fallback rules; cancellation, postponement, correction and settlement rules; and a versioned constitution hash. It must state whether “occur” means occurrence on the named local calendar date and timezone.

## 7. Authority and source precommitment

Authority is relation-specific, not cosmetic. Tier 1 is the named organizer/event authority. Tier 2 is a named first-party party only when the constitution permits it (for example, the official broadcaster for the exact ceremony). Tier 3 is a named reputable secondary publisher only when an explicit fallback condition is met. Fan polls, odds, nominations, predictions, leaks, snippets, unsourced social posts, and commentary are never authority.

Precommit a **source-identity record plus constrained URL policy**, rather than only an exact URL or an entire domain. Each rule includes source ID, role/tier, approved HTTPS host(s), optional path prefix/pattern, redirect policy, relation to event, and whether it is primary or fallback. Exact pages may be unknown before results; a whole domain is too broad. Candidate URLs may be submitted only if they deterministically satisfy a frozen rule. Redirects are accepted only when every hop and final URL satisfy the same frozen approved-host/path policy; otherwise evidence is rejected.

Use one Tier-1 source as normal minimum. Permit a second Tier-1 source or a specifically named Tier-2 fallback only after an objective condition (unavailable, no result by deadline, or specified contradiction policy). Do not use broad “search for sources” fallback.

## 8. Valid Web Render Architecture — verified gate

**Verified: API/source compatibility yes; live target runtime proof no.** The current official example documents `gl.nondet.web.get` for static content and `gl.nondet.web.render` for browser-rendered content. It explicitly documents `render(..., mode="text")`, `render(..., mode="html")`, screenshot mode, and short `wait_after_loaded`; it says render is for JavaScript execution/DOM rendering and that nondeterministic web operations must be invoked inside `gl.eq_principle.*`. No minimal direct test was available that can invoke GenVM render on the target without a deployed runner/contract; none was fabricated.

Proposed RESULTLINE flow:

`frozen source rule → permitted candidate URL → GenLayer render(text by default; html only when needed) → bounded untrusted evidence → deterministic eligibility checks → equivalence-protected freeze → committed evidence metadata/fingerprint → semantic adjudication → deterministic validation → settlement`.

Use `get` only for a stable, allowed static endpoint; use `render(mode="text")` for result pages that need a browser. Rendered HTML is reserved for a documented extraction need. The render result is evidence, not settlement authority by itself. Preserve original and final URL, redirect-chain summary if exposed by the verified API, host, source ID/tier, retrieval/render mode, attempt time, status/error category, bounded canonical evidence text, byte/character lengths, and a deterministic fingerprint of the stored bounded representation. Do not claim headers, redirect metadata, or hashing helpers are available until the RC source confirms them.

Bound before storage and adjudication with fixed maximum characters, deterministic truncation marker, and content-type/size policy. Oversized, malformed, unavailable, unauthorized-redirect, retrieval, and render failures create a failed attempt record or revert without changing prior frozen evidence; they do not become FALSE. Duplicates are fingerprint-deduplicated. A successful freeze never overwrites prior evidence. The frozen record, its constitution hash, source rule ID, URL trace, mode, timestamps, bounded representation and fingerprint are the audit trail. Actual on-chain capacity determines whether the bounded text is stored or only a supported immutable representation/reference; no off-chain database is allowed as settlement authority.

This follows the official pattern by executing the supported web operation in GenLayer’s nondeterministic/equivalence boundary rather than backend or frontend scraping. The linter also rejects strict equality over *raw* nondeterministic web output; future code must normalize/extract a bounded state-relevant result or use a comparative principle. Before implementation, run a direct test against the owner-approved 61997 endpoint and exact v0.3.0 runner to verify returned representation, failure and redirect/URL metadata fields. No such metadata has been claimed as runtime-observed.

## 9. Evidence and prompt-injection controls

Rendered material is untrusted data delimited as evidence. The adjudication instruction is static contract-owned text: it tells the model to extract only stated facts, ignore every instruction in evidence, never follow links or requests in evidence, never use sources outside the frozen rules, and return `UNRESOLVED` if facts are missing or conflicting. It forbids votes, stakes, popularity, odds, nominations, predictions, leaks and result-like commentary as proof. It supplies only frozen fields and bounded frozen evidence IDs; it does not permit arbitrary browsing.

Separate `freeze_evidence` from `resolve`. Both are permissionless after deterministic guards. Resolution references frozen IDs only; a malformed/failed/undetermined resolution leaves frozen evidence and financial state intact. Limit attempts per agreement and require a new bounded attempt after an objective retry interval; callers fund their own protocol fee, with no automatic reimbursement in V1. This prevents a disappearing loser from blocking settlement while limiting fee griefing.

## 10. Temporal model and result states

Persist `created_at`, `accepted_at`, `betting_closes_at`, `expected_event_at`, `resolution_not_before`, `resolution_deadline`, and each evidence `retrieved_at`/`frozen_at`. Use chain time only for guards. Expected time is informational; it does not by itself make the result false.

| State | Meaning / settlement |
|---|---|
| `CONFIRMED_TRUE` | authoritative frozen evidence establishes the precise proposition; YES receives stake pot |
| `CONFIRMED_FALSE` | authoritative frozen evidence establishes the negation under the constitution; NO receives pot |
| `UNRESOLVED` | by deadline evidence is insufficient, unavailable, contradictory without a rule, delayed, or consensus is inconclusive; refund both matched stakes |
| `INVALID_EVENT` | a constitution-defined cancellation/void condition occurred; refund both matched stakes |

Postponement and publication delay remain `UNRESOLVED` until deadline unless the constitution explicitly makes a stated date proposition false. A concert moved from September 20 to 22 is false only if the frozen proposition and local-date semantics say September 20; delayed award publication is not false. Corrections before finality supersede earlier evidence under the correction policy.

## 11. Structured adjudication and equivalence

Future semantic output is a bounded enum-only record: `outcome`, `source_authority`, `event_status`, `temporal_validity`, `subject_match`, `category_match`, `evidence_sufficiency`, and sorted `evidence_ids_relied_on`; optional reasoning is display-only and cannot change money. Deterministic code validates enum membership, IDs, ordering, allowed source tiers, constitution linkage, state/time guards, and legal outcome-to-settlement mapping before mutation.

Do not use strict equality over live page text or rich model prose. Use a documented comparative/leader-validator equivalence strategy for semantic resolution: leader proposes the normalized state-relevant enum record from frozen evidence; validators independently determine whether that record is supported by the same frozen constitution/evidence and reject unsupported, malformed, missing-ID, or contradictory proposals. Semantic wording may vary; the validated outcome and relied-on IDs may not. Strict equality is appropriate only for a small, stable normalized retrieval/fingerprint result if direct testing demonstrates reproducibility. An undetermined or failed consensus causes no settlement and leaves the agreement retryable until the deadline, then `UNRESOLVED`.

## 12. Agreement lifecycle and caller model

`DRAFT → OPEN → MATCHED/LOCKED → AWAITING_EVENT → EVIDENCE_FROZEN (repeatable evidence append) → RESOLVING → RESOLVED`.

Exceptional terminals: `CANCELLED` only before matching or under a constitution-defined pre-event cancellation; `UNRESOLVED` and `INVALID_EVENT` after deadline/void conditions. `RESOLVING` must not persist as a financial intermediate after a failed consensus; it returns to evidence-frozen/awaiting resolution. Creator creates and funds the YES or NO position; counterparty must fund the exact opposite position and equal stake before lock. Any caller may freeze permitted evidence after not-before and resolve after evidence and time guards; any caller may finalize a validated result. Replay is rejected by state and one-time settlement flags.

## 13. GEN economics and fee architecture

V1 uses equal integer base-unit GEN stakes, held by the contract; no floats, odds, treasury cut, or semantic influence. On confirmed true/false, the complete stake pot pays the winning position. On `UNRESOLVED`, `INVALID_EVENT`, cancellation after matched funding, evidence unavailability, render failure, and undetermined consensus at deadline, each participant receives their original stake. Contract payout logic must use a pull-withdrawal or a finalization-safe transfer pattern verified against the pinned IC API, so an external payout failure cannot create a partial settlement.

Protocol fees are separate from stake value. Current docs show user-side fee estimation and submission carrying `fees.distribution` and `fees.feeValue` while payable `value` remains independent. The future UI must estimate immediately before each write, show **stake** and **protocol fee deposit** separately, handle fee/wallet/policy failure before submission, then inspect lifecycle/receipt and re-read contract state after finality. Do not select stake size, fee subsidy, or relayer economics in Stage 1. Permissionless evidence/resolution callers pay their own execution fee in V1; reimbursement or bonded incentives require a separate approved economic design.

## 14. Correction and finality policy

Use a short, constitution-defined correction window only for award/competition sources where organizers may issue a correction. Resolution is provisional during that window; approved sources may be refreshed/frozen under the same rule, then a permissionless finalization settles once. No appeals system in V1. If correction handling is not meaningful for an event template, set the window to zero and settle after consensus finality. Settlement is irreversible only after that finalization. A correction after payment is a disclosed product limitation, not a reason to rewrite history.

## 15. Threat model

| Threat | Impact | Mitigation | Remaining limitation |
|---|---|---|---|
| Ambiguous/malicious wording | wrong settlement | typed template + frozen constitution | templates need governance/review |
| Source shopping/fake authority | fabricated proof | identity + host/path precommitment | genuine source compromise remains possible |
| Prompt injection | model manipulation | evidence-as-data prompt, no tool/link following, enums | model/validator risk remains |
| Stale nomination/prediction/poll/leak | false result | exact outcome/event checks and authority tiers | source may be unclear |
| Delay/postponement/cancellation | premature false | time rules and `UNRESOLVED`/`INVALID_EVENT` | real events can remain uncertain |
| Correction/contradiction | wrong finality | correction window, source hierarchy, unresolved fallback | correction after finality |
| Unavailable/malformed/oversized page | lost or bad evidence | bounded failures; retry; never infer false | source may never recover |
| Redirect/duplicate | source-rule bypass | final and hop policy; fingerprint dedupe | API redirect metadata must be verified |
| Early freeze/repeated calls | griefing | time/source guards, append-only records, caps/retry interval | callers can spend own fees |
| Disappearance/replay/payout failure | hostage or double payment | permissionless calls, state guards, one-time settlement, safe payout pattern | exact transfer semantics need RC test |
| Fee failure/undetermined consensus | stranded action | no mutation until final decision; lifecycle re-read; deadline refund | protocol availability |
| Validator disagreement | inconsistent judgment | equivalence validates meaningful enums/IDs | consensus latency/cost |

## 16. Stage 2 test strategy

Test deterministic creation, matching, immutable constitutions, equal stakes, time guards, invalid transitions, accounting and replay prevention. Test valid official retrieval and render, unavailable/malformed/oversized pages, duplicate evidence, redirects and unauthorized redirects, retrieval/render failure, and evidence freeze persistence. Test official winner, nomination/prediction/poll/leak, delay, cancellation, correction, contradiction, insufficiency, prompt injection, fake authority, malformed semantic records and invalid evidence IDs. Test undetermined consensus, failed resolution after freeze, atomic no-settlement on invalid output, payout behavior, fees versus value, unresolved/invalid refunds and lifecycle finality re-read.

## 17. Live Studio Next verification plan (later only)

After the endpoint blocker is resolved, pin the confirmed RC artifacts, configure only the confirmed Studio Next/chain-61997 preset, and run a direct render proof on an approved official page. Then deploy, verify schema/reads, create and match a small real-GEN agreement, freeze rendered evidence, resolve, inspect consensus/receipt/lifecycle, wait through finalization/correction policy, settle, and re-read balances and contract state. Each action is accepted only after authoritative state re-read—not merely a returned transaction ID. No action in this plan was executed in Stage 1.

## 18. Future frontend and public read model

The later frontend uses the confirmed RC `genlayer-js`/Transaction Kit family and a real EIP-1193 wallet; it never holds private keys. It is read-only without a wallet and exposes agreements, constitutions, source rules, frozen evidence metadata, outcomes, reasoning, settlement, and status. Writes visibly progress through preparing, fee estimate, wallet approval, submitted, pending consensus, decided, finalization (if applicable), finalized, and authoritative state re-read. Design should be an entertainment-resolution product, not a generic market dashboard.

## 19. Differentiation and reusable primitive

Unlike prediction markets, RESULTLINE does not use prices or crowd probability as truth. Unlike deterministic oracles, it resolves a frozen natural-language proposition from bounded evidence. Unlike centralized settlement, the rule/evidence/decision trail is public and consensus-governed. Unlike generic AI search or an “LLM decides” contract, both allowable evidence and the deterministic money path are constrained. GenLayer is not needed for matching, accounting, timestamps, authorization, or UI reads; ordinary deterministic contract logic should do those jobs.

The reusable technical name is **Constitution-Bound Authoritative Event Resolution**: a frozen proposition plus precommitted source policy, immutable evidence record, and consensus-validated semantic outcome.

## 20. Open decisions and recommendations

1. V1: award and competition winners; narrow event occurrence only after template testing.
2. Defer box office: yes.
3. Precommit source identity plus constrained host/path policy, not URL-only/domain-only.
4. One Tier-1 source minimum; optional second permitted source for contradiction/correction.
5. Fallback: only explicit, objective-condition fallback.
6. Authority: source’s documented relationship to this exact event/category.
7. `UNRESOLVED`: equal-stake refund.
8. `INVALID_EVENT`: equal-stake refund.
9. Resolution: permissionless after guards.
10. Correction window: template-specific, short; zero only where correction is implausible.
11. Irreversibility: after consensus finality plus correction window.
12. Consensus fields: normalized outcome and evidence IDs plus authority/event/temporal/subject/category/sufficiency enums.
13. Freeze and resolution: always separate in V1.
14. Failed attempts: deterministic cap and retry interval; deadline resolves to refund state.
15. Protocol fees: caller-funded V1; no unapproved subsidy.
16. Value representation: separate `value` stake and estimated `fees` object in every client call.
17. Strongest demo: a completed awards outcome with a stable organizer result page and a controlled correction-window demonstration.

## 21. Known limitations and Stage 2 recommendation

The system cannot eliminate compromised official sources, post-finality corrections, availability failures, semantic disagreement, or the legal/regulatory implications of financial prediction agreements. It must not describe refunds as legal advice or assume all jurisdictions permit the product.

## STAGE 2 REMAINS BLOCKED

Do not start Stage 2. The pinned CLI/JS/Transaction Kit artifacts are now inspected, but the supplied `studio-next` RPC has not been proven to be the supported alias of the RC preset's `studio-dev` RPC. Obtain explicit Agent Tank/GenLayer confirmation or an amended requirement. Then run a direct, non-production proof using the approved endpoint and exact v0.3.0 runner to verify the render representation, failures, and redirect/URL metadata. If that proof differs materially from this audit, revise this document before implementation.
