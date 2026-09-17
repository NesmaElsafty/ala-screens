# -*- coding: utf-8 -*-
"""Reconstruct EN/AR from PDF using stream order + x-jump line breaks."""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(r"D:/Projects/Ala Screens/Docs/live courses")
PDF = ROOT / "eneagram2.pdf"
OUT = ROOT / "_eneagram2_clean.txt"


def tokens_in_stream_order(page):
    toks = []

    def v(text, cm, tm, fontDict, fontSize):
        if text and text.strip():
            toks.append({"x": float(tm[4]), "y": float(tm[5]), "t": text})

    page.extract_text(visitor_text=v)
    return toks


def is_ar(t: str) -> bool:
    return any(
        ("\u0600" <= c <= "\u06FF")
        or ("\uFB50" <= c <= "\uFDFF")
        or ("\uFE70" <= c <= "\uFEFF")
        for c in t
    )


def reconstruct(toks):
    if not toks:
        return ""
    # Prefer layout extraction as secondary — also build from stream.
    lines = []
    buf = [toks[0]["t"]]
    prev = toks[0]
    ar_mode = is_ar(prev["t"])
    for tok in toks[1:]:
        t = tok["t"]
        # New line heuristics:
        # RTL: next token jumps back to the right (x much larger)
        # LTR: next token jumps back to the left (x much smaller)
        dx = tok["x"] - prev["x"]
        new_line = False
        if ar_mode or is_ar(t):
            if dx > 120:  # jumped rightward a lot -> new RTL line
                new_line = True
        else:
            if dx < -120:  # jumped leftward -> new LTR line
                new_line = True
        # Bullet or emoji often starts a block
        if t in {"●", "✨", "🎯", "📸", "🧬"} and buf:
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


def main():
    r = PdfReader(str(PDF))
    parts = []
    for i, page in enumerate(r.pages, 1):
        # Also dump layout mode
        layout = page.extract_text(extraction_mode="layout") or ""
        layout = unicodedata.normalize("NFKC", layout)
        stream = reconstruct(tokens_in_stream_order(page))
        parts.append(f"===== PAGE {i} STREAM =====")
        parts.append(stream)
        parts.append(f"\n===== PAGE {i} LAYOUT =====")
        parts.append(layout)
        parts.append("")
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print("wrote", OUT, "chars", OUT.stat().st_size)


if __name__ == "__main__":
    main()
