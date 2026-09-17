from pathlib import Path
import re

p = Path(r"d:\Projects\Ala Screens\index.html")
t = p.read_text(encoding="utf-8")
t2, n = re.subn(r'"Academy":\s*"الأكاديمية",?\s*', "", t, count=1)
print("removed Academy keys:", n)
p.write_text(t2, encoding="utf-8", newline="\n")
print("Academy key remains:", '"Academy":' in p.read_text(encoding="utf-8"))
