#!/usr/bin/env python3
"""Set the About box (description, homepage, topics) on
agungvg/gta6-sick-note-eni: homepage is the bounty page, topics are the
make.fun set. Uses the custom.github connector credential helper."""

import json
import sys
import urllib.error
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

API = "https://api.github.com"
REPO = "agungvg/gta6-sick-note-eni"
DESCRIPTION = (
    "Official sick note from Leonida General Hospital: every gamer in Leonida "
    "is off work for GTA VI launch day, signed by Dr. Ghost. Built by an AI "
    "agent for make.fun's \u201cPost a GTA 6 meme on X\u201d bounty, $500 in USDC."
)
HOMEPAGE = "https://make.fun/bounty/gta6-meme-x-01"
TOPICS = ["makefun", "ai-agents", "bounties", "growth"]


def call(method, path, payload=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(API + path, data=body, method=method)
    if body is not None:
        req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/vnd.github+json")
    add_surrogate_to_request(
        req, "custom.github", allowed_hosts=["api.github.com", "github.com"]
    )
    try:
        with urllib.request.build_opener().open(req, timeout=30) as resp:
            return resp.status, read_json_response(resp)
    except urllib.error.HTTPError as exc:
        return exc.code, {"error": exc.read(300).decode("utf-8", "replace")}


status, repo = call("PATCH", f"/repos/{REPO}", {
    "description": DESCRIPTION,
    "homepage": HOMEPAGE,
})
print("PATCH repo ->", status, "|", repo.get("description"), "|", repo.get("homepage"))
assert status == 200, repo

status, topics = call("PUT", f"/repos/{REPO}/topics", {"names": TOPICS})
print("PUT topics ->", status, "|", topics.get("names"))
assert status == 200, topics
print("About set OK")
