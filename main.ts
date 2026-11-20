// Entry for make.fun's gta6-meme-x-01 ("Post a GTA 6 meme on X").
// The entry itself is the X post: a GTA 6 meme posted from a public account,
// carrying make.fun / @makefunai and the entrant's play code. This program
// does the only mechanical job the harness needs: it copies POST.json, the
// file at the repository root that names the post's address, into the output
// directory, where the gate reads it and the house reads the post from X.
// It writes nothing else and judges nothing.
//
// Run locally:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const raw = readFileSync(join(botDir, 'POST.json'), 'utf8');
const parsed = JSON.parse(raw);
if (parsed === null || typeof parsed !== 'object' || typeof parsed.url !== 'string') {
  console.error('POST.json must hold a JSON object with a string "url" field');
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
copyFileSync(join(botDir, 'POST.json'), join(outputDir, 'POST.json'));
console.log('copied POST.json ->', join(outputDir, 'POST.json'));
