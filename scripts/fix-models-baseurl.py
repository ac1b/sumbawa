#!/usr/bin/env python3
"""Fix MiniMax baseUrl in auto-generated models.json files.
OpenClaw generates baseUrl as https://api.minimax.io/v1 but correct is /anthropic.
"""
import json, glob, os

for f in glob.glob("/root/.openclaw/agents/*/agent/models.json"):
    try:
        with open(f) as fh:
            d = json.load(fh)
        p = d.get("providers", d)
        mm = p.get("minimax", {})
        if mm.get("baseUrl") == "https://api.minimax.io/v1":
            mm["baseUrl"] = "https://api.minimax.io/anthropic"
            with open(f, "w") as fh:
                json.dump(d, fh, indent=2)
            print(f"Fixed minimax baseUrl in {f}")
    except Exception as e:
        print(f"Skip {f}: {e}")
