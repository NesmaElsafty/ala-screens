# -*- coding: utf-8 -*-
import json, re
from pathlib import Path

html = Path(r"d:\Projects\Ala Screens\eneagram1.html").read_text(encoding="utf-8")
D = json.loads(re.search(r"window\.ALA_I18N_DICT = (\{.*?\});", html).group(1))
urls = re.findall(r'src: "(https://[^"]+)"', html)
hero = re.search(r'id="programHeroImage"\s*\n\s*src="([^"]+)"', html)
lines = [
    f"gallery={len(urls)}",
    f"hero={hero.group(1) if hero else None}",
    f"Ask About={'Ask About This Program' in D}",
    f"44 Hours={'44 Hours' in D}",
    f"Leaders={'Leaders & Teams' in D}",
    f"AcademyKey={'Academy' in D}",
    f"title has Enneagram={'Enneagram | Level 1' in html}",
    f"PCC leftover body={('PCC Level' in html.split('ALA_I18N_DICT')[0])}",
]
Path(r"d:\Projects\Ala Screens\_i18n\_eneagram_qa.txt").write_text("\n".join(lines), encoding="utf-8")
print("ok")
