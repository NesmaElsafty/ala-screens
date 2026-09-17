# -*- coding: utf-8 -*-
"""Find visible text nodes not covered by ar.json."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {"ps-recorded-funnel.html"}
ar = json.load(open(os.path.join(os.path.dirname(__file__), "ar.json"), encoding="utf-8"))

def texts(html):
    html = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
    html = re.sub(r"<style[\s\S]*?</style>", " ", html, flags=re.I)
    html = re.sub(r"<i\b[^>]*>.*?</i>", " ", html, flags=re.I | re.S)
    parts = re.split(r"<[^>]+>", html)
    out = []
    for p in parts:
        t = " ".join(p.split())
        if t and re.search(r"[A-Za-z]", t):
            out.append(t)
    return out

missing = []
seen = set()
for f in sorted(os.listdir(ROOT)):
    if not f.endswith(".html") or f in SKIP:
        continue
    raw = open(os.path.join(ROOT, f), encoding="utf-8").read()
    for t in texts(raw):
        if t in ar or t in seen:
            continue
        if t.startswith("http") or "Copy of" in t or t.startswith("images/"):
            continue
        if re.fullmatch(r"[\d+\-.,/%KMh:]+", t):
            continue
        seen.add(t)
        missing.append(t)

print("missing", len(missing))
open(os.path.join(os.path.dirname(__file__), "missing.txt"), "w", encoding="utf-8").write("\n".join(missing))
for t in missing[:80]:
    print(repr(t)[:160])
