#!/usr/bin/env python3
"""Set About (description/homepage/topics) on agungvg/gta6-sick-note-eni."""
import json
import sys
import urllib.request
import urllib.error

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

API = "https://api.github.com"
REPO = "agungvg/gta6-sick-note-eni"
SUMMARY = ("Official sick note from Leonida General Hospital: every gamer in "
           "Leonida is off work for GTA VI launch day, signed by Dr. Ghost.")
ABOUT = (SUMMARY + " Built by an AI agent for make.fun's \u201cPost a GTA 6 meme "
         "on X\u201d bounty, $500 in USDC.")


def api(method, path, payload=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/vnd.github+json")
    add_surrogate_to_request(req, "custom.github",
                             allowed_hosts=["api.github.com", "github.com"])
    try:
        with urllib.request.build_opener().open(req, timeout=30) as resp:
            return resp.status, read_json_response(resp)
    except urllib.error.HTTPError as exc:
        return exc.code, {"error": exc.read(300).decode("utf-8", errors="replace")}


s, r = api("PATCH", f"/repos/{REPO}", {
    "description": ABOUT,
    "homepage": "https://make.fun/bounty/gta6-meme-x-01",
})
print("PATCH repo ->", s, r.get("description"), "|", r.get("homepage"))
assert s == 200

s, r = api("PUT", f"/repos/{REPO}/topics", {
    "names": ["makefun", "ai-agents", "bounties", "growth"],
})
print("PUT topics ->", s, r.get("names"))
assert s == 200
print("About set OK")
