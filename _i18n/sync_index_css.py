from pathlib import Path
import re

root = Path(r"d:\Projects\Ala Screens")
css = (root / "_i18n" / "i18n.css").read_text(encoding="utf-8")
path = root / "index.html"
html = path.read_text(encoding="utf-8")
new, n = re.subn(
    r"/\* ALA_I18N_CSS_START \*/[\s\S]*?/\* ALA_I18N_CSS_END \*/",
    css.strip(),
    html,
    count=1,
)
print("replaced", n)
path.write_text(new, encoding="utf-8", newline="\n")
print("rtl visual", 'html[dir="rtl"] #hero .hero-visual' in new)
print("en left40", "left: 40%;" in new)
print("grid 1.1fr", "minmax(0, 1.1fr) minmax(0, 0.9fr)" in new)
