#!/usr/bin/env python3
"""Create the public GitHub repo agungvg/gta6-sick-note-eni (make.fun
gta6-meme-x-01 entry). Uses the custom.github connector credential helper.
Prints only repo metadata, never the token."""
import json
import sys
import urllib.request
import urllib.error

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

API = "https://api.github.com"


def api(method, path, payload=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    add_surrogate_to_request(req, "custom.github",
                             allowed_hosts=["api.github.com", "github.com"])
    try:
        with urllib.request.build_opener().open(req, timeout=30) as resp:
            return resp.status, read_json_response(resp)
    except urllib.error.HTTPError as exc:
        body = exc.read(300).decode("utf-8", errors="replace")
        return exc.code, {"error": body}


status, me = api("GET", "/user")
print("GET /user ->", status, me.get("login"))
assert status == 200 and me.get("login") == "agungvg", "not signed in as agungvg"

status, repo = api("POST", "/user/repos", {
    "name": "gta6-sick-note-eni",
    "description": "Official sick note from Leonida General Hospital: every gamer in Leonida is off work for GTA VI launch day, signed by Dr. Ghost. Built by an AI agent for make.fun's \u201cPost a GTA 6 meme on X\u201d bounty, $500 in USDC.",
    "private": False,
    "auto_init": False,
})
print("POST /user/repos ->", status)
if status == 201:
    print("created:", repo.get("full_name"), repo.get("html_url"),
          "default_branch:", repo.get("default_branch"),
          "created_at:", repo.get("created_at"))
elif status == 422:
    print("repo may already exist:", json.dumps(repo)[:300])
    status2, existing = api("GET", "/repos/agungvg/gta6-sick-note-eni")
    print("GET existing ->", status2, existing.get("full_name"),
          existing.get("html_url"), existing.get("created_at"))
else:
    print("FAILED:", json.dumps(repo)[:500])
    sys.exit(1)
