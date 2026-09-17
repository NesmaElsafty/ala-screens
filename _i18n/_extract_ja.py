# -*- coding: utf-8 -*-
from pathlib import Path
from pypdf import PdfReader
import unicodedata
import re

docs = Path(r"D:/Projects/Ala Screens/Docs")
pdf = None
for p in docs.glob("*.pdf"):
    if "رحلة" in p.name or "وعى" in p.name or "وعي" in p.name:
        pdf = p
        break
if pdf is None:
    # size match from earlier listing
    for p in docs.glob("*.pdf"):
        if abs(p.stat().st_size - 433159) < 50:
            pdf = p
            break
assert pdf, "PDF not found"
(Path(r"D:/Projects/Ala Screens/Docs/_ja_pdf_path.txt")).write_text(str(pdf), encoding="utf-8")

r = PdfReader(str(pdf))


def is_ar(t):
    return any(
        ("\u0600" <= c <= "\u06FF")
        or ("\uFB50" <= c <= "\uFDFF")
        or ("\uFE70" <= c <= "\uFEFF")
        for c in t
    )


def tokens(page):
    toks = []

    def v(text, cm, tm, fontDict, fontSize):
        if text and text.strip():
            toks.append({"x": float(tm[4]), "y": float(tm[5]), "t": text})

    page.extract_text(visitor_text=v)
    return toks


def reconstruct(toks):
    if not toks:
        return ""
    lines = []
    buf = [toks[0]["t"]]
    prev = toks[0]
    ar_mode = is_ar(prev["t"])
    for tok in toks[1:]:
        t = tok["t"]
        dx = tok["x"] - prev["x"]
        new_line = False
        if ar_mode or is_ar(t):
            if dx > 120:
                new_line = True
        else:
            if dx < -120:
                new_line = True
        if t.strip() in {"●", "✨", "🎯", "📸", "🧬", "🎙", "🔑", "🤝", "⏳", "✅"} and buf:
            new_line = True
        if new_line:
            lines.append(" ".join(buf))
            buf = [t]
            ar_mode = is_ar(t)
        else:
            buf.append(t)
            if is_ar(t):
                ar_mode = True
        prev = tok
    if buf:
        lines.append(" ".join(buf))
    cleaned = []
    for line in lines:
        line = unicodedata.normalize("NFKC", line)
        line = re.sub(r"[ \t]+", " ", line).strip()
        if line:
            cleaned.append(line)
    return "\n".join(cleaned)


out = Path(r"D:/Projects/Ala Screens/Docs/_ja_clean.txt")
parts = [f"pages {len(r.pages)}", f"source={pdf.name}"]
for i, page in enumerate(r.pages, 1):
    parts.append(f"\n===== PAGE {i} STREAM =====")
    parts.append(reconstruct(tokens(page)))
    parts.append(f"\n===== PAGE {i} LAYOUT =====")
    layout = page.extract_text(extraction_mode="layout") or ""
    parts.append(unicodedata.normalize("NFKC", layout))
out.write_text("\n".join(parts), encoding="utf-8")
print("ok pages", len(r.pages), "bytes", out.stat().st_size)
