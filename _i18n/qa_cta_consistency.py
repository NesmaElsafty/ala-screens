# -*- coding: utf-8 -*-
import json, re
from pathlib import Path

ROOT = Path(r"d:\Projects\Ala Screens")
keys = [
    "Ask About This Program",
    "Ask on WhatsApp",
    "See More",
    "Explore Programs",
    "Home",
    "Programs",
    "Contact",
    "Find Your Program",
    "Camps",
]
pages = list(Path(r"d:\Projects\Ala Screens").glob("*.html"))
detail = [
    "shiftCamp.html",
    "silentCamp.html",
    "poc.html",
    "acc.html",
    "pcc.html",
    "nlp.html",
    "nlpKids.html",
    "ps.html",
    "psKids.html",
    "leadershipKids.html",
    "pg.html",
    "ots.html",
    "tot.html",
    "ps-recorded.html",
]
rows = {k: set() for k in keys}
for p in detail:
    D = json.loads(
        re.search(
            r"window\.ALA_I18N_DICT = (\{.*?\});",
            (ROOT / p).read_text(encoding="utf-8"),
        ).group(1)
    )
    for k in keys:
        if k in D:
            rows[k].add(D[k])

lines = []
for k, v in rows.items():
    status = "OK" if len(v) <= 1 else "DRIFT"
    lines.append(f"{k}: variants={len(v)} {status}")
(ROOT / "_i18n" / "_cta_consistency.txt").write_text("\n".join(lines), encoding="utf-8")
print("wrote")
