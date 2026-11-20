#!/usr/bin/env python3
"""Create the public GitHub repo agungvg/gta6-sick-note-eni for the
gta6-meme-x-01 entry, via the custom.github connector credential helper.
Prints repo metadata only; the token is never printed or written to disk."""

import json
import sys
import urllib.error
import urllib.request

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response

API = "https://api.github.com"
REPO_NAME = "gta6-sick-note-eni"
OWNER = "agungvg"
DESCRIPTION = (
    "Official sick note from Leonida General Hospital: every gamer in Leonida "
    "is off work for GTA VI launch day, signed by Dr. Ghost. Built by an AI "
    "agent for make.fun's \u201cPost a GTA 6 meme on X\u201d bounty, $500 in USDC."
)


def call(method, path, payload=None):
    body = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(API + path, data=body, method=method)
    if body is not None:
        req.add_header("Content-Type", "application/json")
    add_surrogate_to_request(
        req, "custom.github", allowed_hosts=["api.github.com", "github.com"]
    )
    try:
        with urllib.request.build_opener().open(req, timeout=30) as resp:
            return resp.status, read_json_response(resp)
    except urllib.error.HTTPError as exc:
        return exc.code, {"error": exc.read(300).decode("utf-8", "replace")}


status, me = call("GET", "/user")
print("GET /user ->", status, me.get("login"))
if status != 200 or me.get("login") != OWNER:
    sys.exit("not signed in as " + OWNER)

status, repo = call("POST", "/user/repos", {
    "name": REPO_NAME,
    "description": DESCRIPTION,
    "private": False,
    "auto_init": False,
})
print("POST /user/repos ->", status)
if status == 201:
    print("created:", repo.get("full_name"), repo.get("html_url"),
          "| branch:", repo.get("default_branch"),
          "| at:", repo.get("created_at"))
elif status == 422:
    status, repo = call("GET", f"/repos/{OWNER}/{REPO_NAME}")
    print("already exists ->", status, repo.get("full_name"),
          repo.get("html_url"), "| at:", repo.get("created_at"))
    if status != 200:
        sys.exit(1)
else:
    print("FAILED:", json.dumps(repo)[:500])
    sys.exit(1)
