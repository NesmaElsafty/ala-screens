# -*- coding: utf-8 -*-
from pypdf import PdfReader
from pathlib import Path

pdf = Path(r"D:/Projects/Ala Screens/Docs/live courses/eneagram2.pdf")
out = Path(r"D:/Projects/Ala Screens/Docs/live courses/_eneagram2_visitor2.txt")
r = PdfReader(str(pdf))
lines = []
for pi, page in enumerate(r.pages):
    lines.append(f"\n===== PAGE {pi + 1} =====")
    def v(text, cm, tm, fontDict, fontSize, _lines=lines):
        if text and text.strip():
            _lines.append(f"{tm[4]:7.1f},{tm[5]:7.1f} sz={fontSize:.1f} | {text!r}")
    page.extract_text(visitor_text=v)

# Also write a cleaned-ish continuous extract by joining words carefully
raw = []
for pi, page in enumerate(r.pages):
    raw.append(f"\n===== PAGE {pi + 1} RAW =====\n")
    raw.append(page.extract_text() or "")

out.write_text("\n".join(lines) + "\n\n" + "".join(raw), encoding="utf-8")
print("wrote", out, "bytes", out.stat().st_size)
