# -*- coding: utf-8 -*-
"""Find visible English still missing from page dicts / ar.json."""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(r"d:\Projects\Ala Screens")
AR = json.loads((ROOT / "_i18n" / "ar.json").read_text(encoding="utf-8"))
PAGES = [
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

KEEP = re.compile(
    r"^(EN|AR|/|Facebook|Instagram|WhatsApp|LinkedIn|YouTube|ALA|"
    r"Ahmed Latif|Academy|ICF|PCC|ACC|NLP|OTS|TOT|POC|PG|"
    r"Silent Camp|Shift Camp|Dynamo Camp|Psychological Genius|Enneagram|"
    r"Power of Change|Orbit Training School|Relation Coaching|"
    r"Journey Of Awareness|CashProcess|Dynamo).*$",
    re.I,
)


class H(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip = 0
        self.texts = []
        self.attrs = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip += 1
        d = dict(attrs)
        for k in ("alt", "title", "aria-label", "placeholder"):
            if k in d and d[k] and re.search(r"[A-Za-z]", d[k]):
                self.attrs.append(d[k])

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if self.skip:
            return
        t = " ".join(data.split())
        if t and re.search(r"[A-Za-z]", t):
            self.texts.append(t)


report = {}
for page in PAGES:
    html = (ROOT / page).read_text(encoding="utf-8")
    D = json.loads(re.search(r"window\.ALA_I18N_DICT = (\{.*?\});", html).group(1))
    body = re.sub(
        r"<!-- ALA_I18N_(START|BOOT) -->[\s\S]*?<!-- (/ALA_I18N_BOOT|ALA_I18N_END) -->",
        "",
        html,
    )
    body = re.sub(r"<style[\s\S]*?</style>", "", body, flags=re.I)
    p = H()
    p.feed(body)
    miss = []
    seen = set()
    for t in p.texts + p.attrs:
        if t in seen:
            continue
        seen.add(t)
        if t in D or KEEP.match(t) or t.startswith("http"):
            continue
        if not re.search(r"[A-Za-z]{3,}", t):
            continue
        miss.append({"t": t, "inAR": t in AR})
    report[page] = miss
    print(f"{page}: missing {len(miss)} (inAR {sum(1 for m in miss if m['inAR'])})")

(ROOT / "_i18n" / "_missing_detail.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
)
