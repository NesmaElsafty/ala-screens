# -*- coding: utf-8 -*-
"""Patch eneagram2 i18n CTA split keys + AR period without rebuilding whole page."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"d:\Projects\Ala Screens")
HTML = ROOT / "eneagram2.html"
AR = ROOT / "_i18n" / "ar.json"

UPDATES = {
    "What you see on the surface never tells the whole story.": "السلوك اللي بتشوفه مش دايماً بيحكي القصة كلها...",
    "Book your seat in Level 2 and start seeing what's behind it.": "احجز مكانك في Level 2 وابدأ تشوف اللي وراه.",
    "What you see on the surface never tells the whole story. Book your seat in Level 2 and start seeing what's behind it.": "السلوك اللي بتشوفه مش دايماً بيحكي القصة كلها... احجز مكانك في Level 2 وابدأ تشوف اللي وراه.",
}

P1_EN = (
    "The truth is, knowing someone's type is only the first door. The 9 types tell you \"who\" someone is... "
    "but they don't tell you why the same person can be quiet and withdrawn one day, and social and open "
    "the very next, while still being exactly the same type. That difference isn't random — and that's "
    "exactly what Level 2 reveals."
)
P1_AR = (
    'الحقيقة إن معرفة نمط حد هي بس أول باب. الأنماط التسعة بتقولك "مين هو"... بس مش بتقولك ليه في يوم '
    "بيبقى هادي ومنسحب، وفي يوم تاني نفسه بالظبط بيبان اجتماعي ومنفتح. الفرق ده مش صدفة، وده بالظبط اللي "
    "Level 2 هيوريهولك."
)
UPDATES[P1_EN] = P1_AR


def patch_html() -> None:
    text = HTML.read_text(encoding="utf-8")
    m = re.search(r"window\.ALA_I18N_DICT = (\{.*?\});", text, re.S)
    if not m:
        raise SystemExit("dict missing")
    d = json.loads(m.group(1))
    d.update(UPDATES)
    new = "window.ALA_I18N_DICT = " + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + ";"
    text = text[: m.start()] + new + text[m.end() :]
    HTML.write_text(text, encoding="utf-8", newline="\n")
    print("patched html dict")


def patch_ar() -> None:
    data = json.loads(AR.read_text(encoding="utf-8"))
    data.update(UPDATES)
    AR.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("patched ar.json")


if __name__ == "__main__":
    patch_html()
    patch_ar()
    # verify
    html = HTML.read_text(encoding="utf-8")
    d = json.loads(re.search(r"window\.ALA_I18N_DICT = (\{.*?\});", html, re.S).group(1))
    for k in UPDATES:
        assert d.get(k) == UPDATES[k], k
    assert 'galleryFolder = "images/eneagram%202/"' in html
    assert "Book your seat in Level 2 and start seeing what's behind it." in html
    print("verify ok")
