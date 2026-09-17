# -*- coding: utf-8 -*-
import json, re
from pathlib import Path

ROOT = Path(r"d:\Projects\Ala Screens")

for page in ["programs.html", "camps.html", "portfolio.html"]:
    html = (ROOT / page).read_text(encoding="utf-8")
    D = json.loads(re.search(r"window\.ALA_I18N_DICT = (\{.*?\});", html).group(1))
    cards = re.findall(r'<a class="program-card[\s\S]*?</a>', html)
    print("===", page, "cards", len(cards), "===")
    for c in cards:
        href = re.search(r'href="([^"]+)"', c).group(1)
        title = re.search(r"<h3[^>]*>([\s\S]*?)</h3>", c)
        desc = re.search(r"<p[^>]*>([\s\S]*?)</p>", c)
        t = re.sub(r"<[^>]+>", "", title.group(1)).strip() if title else "?"
        d = re.sub(r"<[^>]+>", "", desc.group(1)).strip() if desc else "?"
        print(" href:", href)
        print(" title:", t[:90], "| in dict:", t in D)
        print(" desc in dict:", d in D)
        if d not in D:
            print("  MISS:", d[:120])
    # page header
    for key in ["Our Programs", "Explore ALA Programs", "Our Camps", "Explore ALA Camps"]:
        if key in html:
            print(" header key", key, "in dict:", key in D)
