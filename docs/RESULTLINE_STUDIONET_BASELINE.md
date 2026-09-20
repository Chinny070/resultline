# RESULTLINE Studionet Baseline

- Network: `studionet`
- Chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- Frontend SDK: `genlayer-js@1.1.8`
- Contract toolchain: `genvm-lint 0.11.0`, `genlayer-py 0.16.3`, `genlayer-test 0.29.2`

The stable linter accepts `gl.Contract`, public view/write/payable methods,
`gl.Address`, `gl.u256`, `gl.storage.DynArray`, and `gl.storage.TreeMap`.

```python
owed: gl.storage.TreeMap[gl.Address, gl.u256]
self.owed[account] = self.owed.get(account, gl.u256(0)) + amount
```

Deterministic transaction time:

```python
from datetime import datetime, timezone
timestamp = int(datetime.now(timezone.utc).timestamp())
```

Evidence uses `gl.nondet.web.render(url, mode="text")` in an equivalence-
controlled nondeterministic operation. Structured adjudication uses
`gl.nondet.exec_prompt(..., response_format="json")` with comparative
equivalence.

Native EOA payout:

```python
@gl.evm.contract_interface
class _Recipient:
    class View: pass
    class Write: pass

_Recipient(gl.Address(recipient)).emit_transfer(value=gl.u256(amount))
```

The `genlayer-js@1.1.8` lifecycle uses `getTransaction`,
`waitForTransactionReceipt`, round APIs, `finalizeTransaction`, and
`getTriggeredTransactionIds`; newer decision/finalization helpers are absent.

Release gates: live hosted web retrieval; real EOA payout and balance proof;
deployment-address recovery; and Explorer verification.

