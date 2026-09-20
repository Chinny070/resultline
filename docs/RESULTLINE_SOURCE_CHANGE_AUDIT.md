# RESULTLINE Source Change Audit

## Exact source change

The old `b436...` blob was recovered from the repository's unreachable Git
objects and compared byte-for-byte with the current source.

1. Constructor initialization changed from dynamic `setattr` assignment to
   explicit assignments for every persistent field. This was a schema-
   compatibility change; it does not alter public methods, parameters,
   payable behavior, storage field names/types, settlement arithmetic, or web
   and adjudication rules.
2. `get_agreement` changed from `dict[str, typing.Any]` to a schema-safe `str`
   serialization. `get_evidence` changed the same way. This changes only the
   read return representation; it does not change writes, storage, settlement,
   source policy, evidence retrieval, or adjudication.

The Studio error was an actual `gen_getContractSchemaForCode` execution failure
shown in the Studio RPC log. The first correction (explicit constructor fields)
was therefore evidence-backed. The later string-return correction was also
made in response to the same schema-generation failure after the constructor
fix alone did not resolve it.

## Current source audit

| Requirement | Result | Location |
|---|---|---|
| Immutable constitution | PARTIAL | `create_agreement`; no explicit temporal-mode field |
| Binary YES/NO | PASS | `create_agreement`, `match_agreement` |
| Explicit creator position | PASS | `creator_position` |
| Explicit counterparty position | PASS | `counterparty_position` |
| Equal-stake matching | PASS | `match_agreement` |
| Host/path identity | PASS | `_source`, `freeze_evidence` |
| Source shopping prevention | PASS | exact frozen URL comparison |
| Official rendered retrieval | PASS | `freeze_evidence` |
| Bounded evidence | PASS | `MAX_TEXT` check |
| Evidence freeze state | PASS | `freeze_evidence` |
| Failed evidence fail-closed | PARTIAL | runtime failure atomicity not live-tested |
| UNRESOLVED distinct from FALSE | PASS | adjudication enum validation/prompt |
| Structured adjudication | PARTIAL | fields are required but retained inside serialized resolution |
| Evidence IDs relied upon | PARTIAL | not stored as a dedicated field |
| Comparative equivalence | PASS | `prompt_comparative` |
| Deterministic settlement | PASS | `settle` |
| TRUE/FALSE/refunds | PASS | `settle` branches |
| Settlement once only | PASS | resolved-state guard |
| Address→u256 owed accounting | PASS | `owed` TreeMap |
| Checks-effects-interactions | PASS | `withdraw` |
| Double withdrawal prevention | PASS | owed zeroing + zero guard |
| Permissionless resolution | PASS | no caller restriction in `resolve` |
| Stake excluded from adjudication | PASS | stake is not included as a decision input |
| Atomicity | PARTIAL | requires runtime/consensus tests |

## Local verification

- SHA-256: `a59d3a83677d3ad793f24c3232cd03710471062d0ac09f177c3f2720aa3d4588`
- `genvm-lint lint`: PASS
- `genvm-lint check`: PASS
- Tests: 10 collected, 8 passed, 0 failed, 2 blocked, 0 skipped
- Blocked tests fail before contract execution with Windows `WinError 5` in
  the gltest direct-SDK cache.

## Decision

The current source is a justified schema-compatibility candidate relative to
`b436...`, but it is not yet ready for deployment because the audit identifies
partial requirements and the CLI/hosted proof is incomplete.

OLD HASH:
b43692674e3522afbca016d748d0af5b384ba35a55570625201e5b914f875026

CURRENT HASH:
a59d3a83677d3ad793f24c3232cd03710471062d0ac09f177c3f2720aa3d4588

SCHEMA FIX VERIFIED NECESSARY:
YES

CURRENT CONTRACT SPEC AUDIT:
FAIL

MISSING OR PARTIAL REQUIREMENTS:
5

RECOMMENDED CANDIDATE:
a59d...

READY FOR HOSTED STUDIONET DEPLOYMENT:
NO
