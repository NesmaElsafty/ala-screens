# -*- coding: utf-8 -*-
"""Audit program-detail pages for i18n readiness."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"d:\Projects\Ala Screens")

MAIN = {"index.html", "portfolio.html", "programs.html", "camps.html"}
CANDIDATES = sorted(p.name for p in ROOT.glob("*.html") if p.name not in MAIN)

checks = [
    ("boot", r"ALA_I18N_BOOT"),
    ("engine", r"ALA_I18N_START"),
    ("storage", r'ala-language'),
    ("switcher", r'lang-switcher'),
    ("cairo", r"Cairo"),
    ("css", r"ALA_I18N_CSS_START"),
    ("academy_dict", r'"Academy"\s*:'),
    ("logo_skip", r"logo-academy"),
    ("gallery", r"gallery|lightbox|swiper|carousel", re.I),
]


def dict_size(html: str) -> int:
    m = re.search(r"window\.ALA_I18N_DICT = (\{.*?\});", html)
    if not m:
        return 0
    try:
        return len(json.loads(m.group(1)))
    except Exception:
        return -1


def hero_abs(html: str) -> bool:
    # rough: absolute positioning near hero
    return bool(re.search(r"\.hero[^{]*\{[^}]*position:\s*absolute|\.hero-[\w-]+\s*\{[^}]*left:", html))


report = []
for name in CANDIDATES:
    html = (ROOT / name).read_text(encoding="utf-8")
    row = {"file": name, "dict": dict_size(html), "bytes": len(html)}
    for item in checks:
        key, pat = item[0], item[1]
        flags = item[2] if len(item) > 2 else 0
        row[key] = bool(re.search(pat, html, flags))
    row["hero_abs"] = hero_abs(html)
    # corrupted boot?
    row["boot_corrupt"] = "ALA_I18N_CSS_START" in html.split("<!-- /ALA_I18N_BOOT -->")[0] if "ALA_I18N_BOOT" in html else False
    # shouldSkip brand
    skip = re.search(r"function shouldSkip[\s\S]{0,400}", html)
    row["skip_snippet"] = " ".join(skip.group(0).split())[:160] if skip else "NONE"
    report.append(row)

out = ROOT / "_i18n" / "_audit_detail.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

for r in report:
    print(
        f"{r['file']:24} dict={r['dict']:4} boot={r['boot']} eng={r['engine']} "
        f"sw={r['switcher']} acad={r['academy_dict']} gal={r['gallery']} "
        f"corrupt={r['boot_corrupt']}"
    )
