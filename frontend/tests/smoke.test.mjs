import assert from 'node:assert/strict';
import fs from 'node:fs';

const html = fs.readFileSync(new URL('../index.html', import.meta.url), 'utf8');
const source = fs.readFileSync(new URL('../src/main.ts', import.meta.url), 'utf8');
assert.match(html, /id="app"/);
for (const method of ['create_agreement','match_agreement','cancel_agreement','freeze_evidence','resolve','settle','withdraw']) assert.match(source, new RegExp(method));
for (const method of ['get_agreement','get_agreement_count','get_evidence','get_withdrawable']) assert.match(source, new RegExp(method));
assert.match(source, /chainId: 61999/);
assert.match(source, /studionet|studio\.genlayer\.com/);
assert.doesNotMatch(source, /61997|studio-dev\.genlayer\.com|studioDevnet/);
console.log('frontend smoke tests passed');
