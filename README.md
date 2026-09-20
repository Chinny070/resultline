# RESULTLINE

RESULTLINE is a constitution-bound entertainment-result settlement protocol. It freezes a precise proposition and authoritative source before matching, records bounded evidence, uses GenLayer semantic consensus for adjudication, and settles deterministically.

## Deployed test contract

- Network: StudioNet (`studionet`)
- Chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- Contract: `0x9877d9af48565797F71dA4492f5e4C8e44c944Cb`
- Locked local source hash: `385fa34f18c95b12aa38582c09106c47538a284cdcf4290f63bba14e4c3d3289`

Hosted deployment was accepted with successful GenVM execution and consensus. Hosted lifecycle, web adjudication, settlement, and EOA payout behavior remain unverified and are not claimed as complete.

## Local development

```powershell
cd frontend
npm install
npm run typecheck
npm run build
npm run dev
```

The frontend uses injected EIP-1193 wallets only for actions. It performs authoritative reads where available and labels examples instead of fabricating live markets.

## Architecture

Agreements encode outcome type, proposition, subject, category, organizer, event, source host/path, positions, stake, temporal windows, and persisted adjudication traceability. Evidence is HTTPS/host/path constrained, rendered as bounded untrusted text, and semantic resolution is fail-closed. Settlement is deterministic; withdrawal clears owed balance before scheduling transfer.
