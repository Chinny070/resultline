# Studio Next EIP-1193 harness (test-only)

This is preparation only. It does not deploy or submit transactions by itself.

Use a browser wallet that the user authorizes normally. The harness checks `eth_chainId == 0xf1cd` (61997) before any write, estimates protocol fees with `estimateTransactionFeesForWrite`, and passes payable stake as `value` separately from `fees`. It waits for `waitUntil: "finalized"` and requires a distinct second authorized account before matching.

Install only the pinned `genlayer-js@2.0.0-rc.1` package in an external test runner. Do not import or inspect CLI keystores. The first interactive action is `eth_requestAccounts`; stop if the browser wallet is absent or connected to another network.
