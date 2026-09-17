# -*- coding: utf-8 -*-
from pathlib import Path
import re
import json

html = Path(r"d:/Projects/Ala Screens/eneagram2.html").read_text(encoding="utf-8")
m = re.search(r"window\.ALA_I18N_DICT = (\{.*?\});", html, re.S)
d = json.loads(m.group(1))
out = []

checks = [
    "Ever felt like you finally understood someone",
    "At this level, you'll start to understand:",
    "Subtypes and their real influence on behavior",
    "The goal here isn't to label people even more...",
    "Watch photos and videos from past batches",
    "What you see on the surface never tells the whole story",
    "A Deeper Understanding of Personalities",
    "The truth is, knowing someone's type",
    "Once you understand the basics",
    "Subtypes reveal that the same type",
    "Once you reach Level 2",
]
for frag in checks:
    key = next((k for k in d if frag in k), None)
    out.append(f"OK i18n={bool(key)} :: {frag[:60]}")
    if key:
        out.append(f"  AR: {d[key][:90]}")

l1 = [k for k in d if "Level 1" in k or "Why do certain colleagues" in k]
out.append(f"L1 leftover: {len(l1)}")

files = re.search(r"var galleryFiles = \[(.*?)\];", html, re.S)
n = len(re.findall(r'"([^"]+)"', files.group(1))) if files else 0
out.append(f"gallery entries: {n}")

secs = re.findall(r'<section class="([^"]+)"', html)
out.append("sections: " + ", ".join(secs))

hm = re.search(r'id="programHeroImage"\s*\n\s*src="([^"]+)"', html)
out.append("hero=" + (hm.group(1) if hm else "MISSING"))

# visible EN program strings in body that lack dict keys
body = html.split("<main>", 1)[1].split("</main>", 1)[0]
# crude: find text in tags
for frag in checks:
    in_body = frag in body
    in_dict = any(frag in k for k in d)
    out.append(f"body={in_body} dict={in_dict} :: {frag[:50]}")

Path(r"d:/Projects/Ala Screens/_i18n/_eneagram2_qa.txt").write_text("\n".join(out), encoding="utf-8")
print("done")
