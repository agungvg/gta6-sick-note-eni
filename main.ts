// gta6-meme-x-01 entry (Node 22, standard library only).
// The entry is the X post itself: an agent-made GTA 6 meme, posted from a
// public X account with make.fun / @makefunai and the entrant's play code in
// its text. This program's only job is to copy POST.json from the repository
// root to /output, where the gate reads the post's address and the house
// reads the post from X. Nothing this program writes is judged.
//
// Local check:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// Fail loudly on a malformed POST.json instead of copying a broken file:
// the gate refuses an entry whose POST.json does not read.
const post = JSON.parse(readFileSync(join(BOT_DIR, 'POST.json'), 'utf8'));
if (typeof post !== 'object' || post === null || typeof post.url !== 'string') {
  console.error('POST.json must be a JSON object with a string "url" field');
  process.exit(1);
}

mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(join(BOT_DIR, 'POST.json'), join(OUTPUT_DIR, 'POST.json'));
