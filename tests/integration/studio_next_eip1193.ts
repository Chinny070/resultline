/**
 * TEST-ONLY Studio Next payable integration harness.
 *
 * This file deliberately requires a browser EIP-1193 provider (window.ethereum).
 * It never reads CLI keystores, private keys, mnemonics, or seed phrases.
 */
import { createClient } from "genlayer-js";
import { studioDevnet } from "genlayer-js/chains";

type Eip1193 = { request(args: { method: string; params?: unknown[] }): Promise<unknown> };

const RPC = "https://studio-dev.genlayer.com/api";
const CHAIN_ID = 61997n;

declare global { interface Window { ethereum?: Eip1193 } }

function provider(): Eip1193 {
  if (!window.ethereum) throw new Error("No EIP-1193 wallet provider; connect an authorized browser wallet.");
  return window.ethereum;
}

export async function connectParticipant(): Promise<{ address: `0x${string}`; chainId: bigint }> {
  const p = provider();
  const accounts = await p.request({ method: "eth_requestAccounts" }) as string[];
  const chainHex = await p.request({ method: "eth_chainId" }) as string;
  const chainId = BigInt(chainHex);
  if (chainId !== CHAIN_ID) throw new Error(`Wrong network: ${chainId}; expected 61997 (studio-dev).`);
  if (!accounts[0]) throw new Error("Wallet returned no authorized account.");
  return { address: accounts[0] as `0x${string}`, chainId };
}

export async function estimatePayableWrite(client: ReturnType<typeof createClient>, account: `0x${string}`, address: `0x${string}`, functionName: string, args: unknown[], stake: bigint) {
  const estimate = await client.estimateTransactionFeesForWrite({ account, address, functionName, args });
  return { stake, protocolFee: estimate.feeValue, fees: estimate };
}

export async function submitPayableWrite(client: ReturnType<typeof createClient>, account: `0x${string}`, address: `0x${string}`, functionName: string, args: unknown[], stake: bigint) {
  const estimate = await client.estimateTransactionFeesForWrite({ account, address, functionName, args });
  const hash = await client.writeContract({
    account, address, functionName, args, value: stake,
    fees: { distribution: estimate.distribution, messageAllocations: estimate.messageAllocations, feeValue: estimate.feeValue },
  });
  const receipt = await client.waitForTransactionReceipt({ hash, waitUntil: "finalized" });
  return { hash, receipt };
}

export function makeStudioClient() {
  const p = provider();
  return createClient({ chain: studioDevnet, provider: p });
}

export function assertDistinct(a: string, b: string) {
  if (a.toLowerCase() === b.toLowerCase()) throw new Error("Participant B must be a different wallet account.");
}
