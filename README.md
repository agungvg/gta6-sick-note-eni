# gta6-sick-note-eni

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/agungvg/gta6-sick-note-eni/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/agungvg/gta6-sick-note-eni/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

An entry for make.fun's **"Post a GTA 6 meme on X"** bounty ($500 in USDC, top 50 places).

The joke: an official sick note from Leonida General Hospital, excusing every gamer in Leonida from work on GTA VI launch day — diagnosis: acute GTA VI launch fever, 13 years in the making; symptoms: called in sick and a 212 GB download; return date: when Lucia says so. The attending physician is Dr. Ghost, the make.fun ghost. The picture is `meme.png`, drawn by the agent with `make_meme.py` (PIL) from make.fun's official ghost mark (`makefun-mark.png`, press kit). The exact words to post with it are in `POST_TEXT.md` — copy them verbatim, with the image attached as the first (only) picture, from a public X account, and keep the post up until the results are out.

`POST.json` names the post once it is live; `main.ts` copies it to `/output` for the gate. Post it, then point `POST.json` at `https://x.com/<handle>/status/<id>` before the entry is submitted.

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=p9r33tb4&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
