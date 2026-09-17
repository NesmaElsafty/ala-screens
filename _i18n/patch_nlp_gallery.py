# -*- coding: utf-8 -*-
import re
from pathlib import Path

ROOT = Path(r"d:\Projects\Ala Screens")
urls = [
    u.strip()
    for u in (ROOT / "images" / "nlpImages.html").read_text(encoding="utf-8").splitlines()
    if u.strip().startswith("http")
]
gallery_js = ",\n        ".join(
    f'{{ src: "{u}", alt: "NLP program photo {i}" }}' for i, u in enumerate(urls, 1)
)
path = ROOT / "nlp.html"
html = path.read_text(encoding="utf-8")
new_block = f"""      var galleryImages = [
        {gallery_js}
      ];"""
html2, n = re.subn(
    r"      var galleryFolder = [\s\S]*?var galleryImages = galleryFiles\.map\(function \(file, index\) \{\s*"
    r"return \{\s*src: galleryFolder \+ encodeURIComponent\(file\),\s*"
    r'alt: "NLP program photo " \+ \(index \+ 1\)\s*\};\s*\}\);',
    new_block,
    html,
    count=1,
)
if n != 1:
    raise SystemExit(f"replace failed n={n}")
path.write_text(html2, encoding="utf-8", newline="\n")
print(f"replaced gallery with {len(urls)} CDN urls")
