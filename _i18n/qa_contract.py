# -*- coding: utf-8 -*-
"""Verify shared i18n contract across index + three nav pages."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"d:\Projects\Ala Screens")
PAGES = ["index.html", "portfolio.html", "programs.html", "camps.html"]


def extract(html: str, pattern: str) -> str | None:
    m = re.search(pattern, html)
    return m.group(1) if m else None


def main() -> None:
    for page in PAGES:
        html = (ROOT / page).read_text(encoding="utf-8")
        has_boot = "ala-language" in html and "ALA_I18N_BOOT" in html
        has_engine = "ALA_I18N_START" in html and "STORAGE_KEY = \"ala-language\"" in html
        has_switcher = 'data-lang-switch="ar"' in html
        academy_key = '"Academy"' in (extract(html, r"window\.ALA_I18N_DICT = (\{.*?\});") or "")
        print(
            f"{page}: boot={has_boot} engine={has_engine} switcher={has_switcher} "
            f"AcademyDict={academy_key}"
        )

    # Link rewrite contract samples
    samples = [
        ("programs.html#programs", "ar", "programs.html?lang=ar#programs"),
        ("silentCamp.html", "ar", "silentCamp.html?lang=ar"),
        ("shiftcamp.html", "en", "shiftcamp.html?lang=en"),
        ("https://link.cashprocess.io/preview/abc", "ar", "lang=ar"),
    ]

    def with_lang(href: str, lang: str) -> str:
        hash_ = ""
        if "#" in href:
            href, hash_ = href.split("#", 1)
            hash_ = "#" + hash_
        if href.startswith("http"):
            from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

            u = urlparse(href)
            q = parse_qs(u.query)
            q["lang"] = [lang]
            # flatten
            pairs = []
            for k, vals in q.items():
                for v in vals:
                    pairs.append((k, v))
            return urlunparse((u.scheme, u.netloc, u.path, u.params, urlencode(pairs), "")) + hash_
        base = href.split("?")[0]
        return f"{base}?lang={lang}{hash_}"

    print("--- link rewrite samples ---")
    for href, lang, expect in samples:
        out = with_lang(href, lang)
        ok = expect in out if expect.startswith("lang=") else out == expect
        print(("OK" if ok else "FAIL"), out)

    # Ensure index untouched marker: hero-signature skip only on index
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    assert ".hero-signature" in idx
    for page in ("portfolio.html", "programs.html", "camps.html"):
        html = (ROOT / page).read_text(encoding="utf-8")
        # listing skip should not require hero-signature
        eng = re.search(
            r"function shouldSkip\(el\) \{[\s\S]*?return false;\n  \}",
            html,
        ).group(0)
        print(page, "shouldSkip:", " ".join(eng.split())[:180], "...")


if __name__ == "__main__":
    main()
