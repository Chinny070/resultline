# RESULTLINE V1 Contract Specification

RESULTLINE supports only `AWARD_WINNER` and `COMPETITION_WINNER`, with YES/NO
positions and outcomes `CONFIRMED_TRUE`, `CONFIRMED_FALSE`, `UNRESOLVED`, and
`INVALID_EVENT`.

State machine: `OPEN → MATCHED → EVIDENCE_FROZEN → RESOLVED → SETTLED`, with
creator-only pre-match cancellation. Constitution fields, source policy,
temporal bounds, stake, and participants become immutable once matched.

Evidence is frozen separately through the official rendered web flow, bounded,
and treated as untrusted data. Adjudication consumes only frozen evidence and
validates structured output; missing evidence is never FALSE.

Settlement is deterministic pull accounting. The winner receives the pot;
UNRESOLVED/INVALID_EVENT refund original stakes. Withdrawal clears owed storage
before emitting a finalized EOA transfer.

