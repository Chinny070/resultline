# RESULTLINE Stage 1 Test Report

## Stage 1 fresh candidate

`contracts/resultline.py` — SHA-256:
`34b9f9fcc34d9622ae7675a833ea485193fe26470865ee1d7e613ae64ae94617`

The abandoned pre-rebuild source is archived at
`archive/abandoned_resultline_pre_rebuild.py` (SHA-256:
`e2fb16ccd33ab6f58e4ff7758f7e9651f69a1b2c7440f554e271b0a93426a10d`).
The hashes differ. The rebuilt source explicitly persists
`counterparty_position` after matching.

Stable `genvm-lint 0.11.0 lint` and `check` pass. The local suite collected
25 tests: 23 passed and 2 direct-runtime tests are blocked before contract
execution by the documented Windows `WinError 5` cache-permission failure
(the count includes the static tests; the two blocked tests are not contract
failures). No tests were weakened or deleted.

Hosted web retrieval, deployment, Explorer verification, and real two-wallet
payout remain release gates and were not attempted.
