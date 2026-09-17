# -*- coding: utf-8 -*-
import json, re
from pathlib import Path

ROOT = Path(r"d:\Projects\Ala Screens")
html = (ROOT / "shiftCamp.html").read_text(encoding="utf-8")
D = json.loads(re.search(r"window\.ALA_I18N_DICT = (\{.*?\});", html).group(1))
# extract a few visible strings from body
for needle in [
    "Ask About This Program",
    "Stuck. Restless. Running on Empty.",
    "You'll Achieve:",
    "Shift Camp isn't a relaxing getaway",
    "Breaking free from that recurring state",
]:
    hits = [k for k in D if needle in k]
    line = f"{needle!r}: {len(hits)} keys"
    print(line.encode("ascii", "backslashreplace").decode())

# ensure main pages untouched by mtime? just check Academy still absent and brand on programs
for p in ["programs.html", "camps.html", "portfolio.html", "index.html"]:
    h = (ROOT / p).read_text(encoding="utf-8")
    assert "ALA_I18N_BOOT" in h
print("main pages still have i18n")
