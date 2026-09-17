# -*- coding: utf-8 -*-
"""Fix corrupted i18n CSS injection on portfolio/programs/camps."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"d:\Projects\Ala Screens")
AR = json.loads((ROOT / "_i18n" / "ar.json").read_text(encoding="utf-8"))
AR.pop("Academy", None)

PAGES = ("portfolio.html", "programs.html", "camps.html")

BOOT = """<!-- ALA_I18N_BOOT -->
<script>
(function () {
  try {
    var k = "ala-language";
    var q = (location.search.match(/[?&]lang=(en|ar)(?:&|#|$)/) || [])[1];
    var s = null;
    try { s = localStorage.getItem(k); } catch (e) {}
    var lang = (q === "en" || q === "ar") ? q : (s === "en" || s === "ar") ? s : "en";
    if (q) { try { localStorage.setItem(k, lang); } catch (e) {} }
    var d = document.documentElement;
    d.lang = lang;
    d.dir = lang === "ar" ? "rtl" : "ltr";
    d.setAttribute("lang", lang);
    d.setAttribute("dir", d.dir);
    if (lang === "ar") d.classList.add("ala-i18n-pending");
  } catch (e) {}
})();
</script>
<noscript><style>html.ala-i18n-pending body { visibility: visible !important; }</style></noscript>
<!-- /ALA_I18N_BOOT -->
"""

SHARED_CSS = r"""/* ALA_I18N_CSS_START */
html.ala-i18n-pending body {
  visibility: hidden;
}

.lang-switcher {
  display: inline-flex;
  align-items: center;
  gap: 0.1rem;
  flex-shrink: 0;
}

.lang-switcher button {
  font-family: inherit;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.06em;
  color: #888;
  padding: 0.3rem 0.4rem;
  border-radius: 0.25rem;
  line-height: 1;
  min-width: 1.75rem;
}

.lang-switcher button:hover {
  color: #b8922f;
}

.lang-switcher button.is-active,
.lang-switcher button[aria-current="true"] {
  color: #b8922f;
}

.lang-sep {
  color: #c8c8c8;
  font-size: 0.75rem;
  font-weight: 500;
  user-select: none;
}

html[lang="ar"] body,
html[lang="ar"] button,
html[lang="ar"] input,
html[lang="ar"] select,
html[lang="ar"] textarea {
  font-family: "Cairo", "Tahoma", sans-serif;
}

html[lang="ar"] h1,
html[lang="ar"] h2,
html[lang="ar"] h3,
html[lang="ar"] h4 {
  font-family: "Cairo", "Tahoma", sans-serif;
  letter-spacing: 0;
}

html[lang="ar"] .logo-text strong,
html[lang="ar"] .signature-text,
html[lang="ar"] .hero-name {
  font-family: "Playfair Display", Georgia, serif;
}

html[lang="ar"] .eyebrow,
html[lang="ar"] .header-cta,
html[lang="ar"] .mobile-nav .header-cta,
html[lang="ar"] .nav-contact,
html[lang="ar"] .block-title,
html[lang="ar"] .featured-badge {
  text-transform: none;
  letter-spacing: 0.04em;
}

html[dir="rtl"] input,
html[dir="rtl"] textarea,
html[dir="rtl"] select {
  direction: rtl;
  text-align: start;
}

html[dir="rtl"] input[type="tel"],
html[dir="rtl"] input[type="email"] {
  direction: ltr;
  unicode-bidi: plaintext;
  text-align: start;
}

html[dir="rtl"] .fa-arrow-right,
html[dir="rtl"] .fa-arrow-left,
html[dir="rtl"] .fa-chevron-right,
html[dir="rtl"] .fa-chevron-left {
  transform: scaleX(-1);
}

html[dir="rtl"] .program-card:hover .program-card-link i.fa-arrow-right,
html[dir="rtl"] .program-card:hover .program-card-link i.fa-arrow-left {
  transform: scaleX(-1) translateX(-4px);
}

html[dir="rtl"] .anim-left:not(.visible) {
  transform: translateX(50px);
}

html[dir="rtl"] .anim-right:not(.visible) {
  transform: translateX(-50px);
}

html[dir="rtl"] .main-nav a::after,
html[dir="rtl"] .nav-links a::after {
  transform-origin: right;
}

html[dir="rtl"] .whatsapp-float {
  right: auto;
  left: 20px;
}

html[dir="rtl"] .program-card-content,
html[dir="rtl"] .program-card-body,
html[dir="rtl"] .about-p,
html[dir="rtl"] .page-header .section-intro {
  text-align: start;
}

html[dir="rtl"] .stat-value,
html[dir="rtl"] .stat-counter,
html[dir="rtl"] .stat-number {
  direction: ltr;
  unicode-bidi: isolate;
}

@media (max-width: 768px) {
  html[dir="rtl"] .whatsapp-float {
    left: 14px;
    right: auto;
  }
}
"""

PORTFOLIO_CSS_EXTRA = r"""
/* Portfolio-specific RTL (do not reuse Home hero composition) */
html[lang="ar"] .font-display:not(.hero-name):not(.stat-value) {
  font-family: "Cairo", "Tahoma", sans-serif;
  letter-spacing: 0;
}

html[lang="ar"] .hero-name,
html[lang="ar"] .stat-value {
  font-family: "Playfair Display", Georgia, serif;
}

html[dir="rtl"] .about-p,
html[dir="rtl"] .philo-p,
html[dir="rtl"] .hero-sub,
html[dir="rtl"] .hero-sub2,
html[dir="rtl"] .muted,
html[dir="rtl"] .muted-2,
html[dir="rtl"] .muted-3,
html[dir="rtl"] .muted-4,
html[dir="rtl"] .achieve-detail {
  text-align: start;
}

html[dir="rtl"] .journey-item {
  text-align: start;
}

/* Keep photo | text physical composition; only text direction flips */
html[dir="rtl"] .about-grid {
  direction: ltr;
}

html[dir="rtl"] .about-grid > .anim-right {
  direction: rtl;
}

html[dir="rtl"] .hero-inner {
  text-align: center;
}

html[dir="rtl"] .hero-tags {
  justify-content: center;
}

html[dir="rtl"] .hero-ctas {
  justify-content: center;
}
"""

LISTING_CSS_EXTRA = r"""
html[dir="rtl"] .program-card-content {
  text-align: start;
}

html[dir="rtl"] .program-card-link {
  justify-content: flex-start;
}

html[dir="rtl"] .page-header {
  text-align: center;
}

html[dir="rtl"] .page-header .section-intro {
  margin-inline: auto;
  text-align: center;
}
"""

ALWAYS_KEYS = (
    "Language",
    "English",
    "Home",
    "About",
    "Programs",
    "Events",
    "News",
    "Contact",
    "Find Your Program",
    "See More",
    "Open menu",
    "Close menu",
    "Main navigation",
    "Mobile navigation",
    "Toggle menu",
    "© Ahmed Latif Academy. All rights reserved.",
    "You're just one step away from joining ALA! Contact us today, and one of our team members will be happy to assist you with the next available course date, course fees, current offers, answer all your questions, and help you complete your registration with ease.",
)

SKIP_PORTFOLIO = (
    'if (el.closest("script, style, noscript, .lang-switcher")) return true;\n'
    "    /* Brand lockup stays English */\n"
    '    if (el.closest(".site-header .logo, .site-header .logo-text, .site-header .logo-academy, .nav-logo")) return true;'
)

SKIP_LISTING = (
    'if (el.closest("script, style, noscript, .lang-switcher")) return true;\n'
    "    /* Brand lockup stays English: Ahmed Latif Academy */\n"
    '    if (el.closest(".site-header .logo, .site-header .logo-text, .site-header .logo-academy")) return true;'
)


def extract_engine_from_index() -> str:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(
        r"<!-- ALA_I18N_START -->\s*<script>\s*window\.ALA_I18N_DICT = \{.*?\};\s*</script>\s*<script>([\s\S]*?)</script>\s*<!-- ALA_I18N_END -->",
        html,
    )
    if not m:
        raise RuntimeError("Could not extract engine from index.html")
    return m.group(1).strip()


def patch_should_skip(engine: str, page: str) -> str:
    skip = SKIP_PORTFOLIO if page == "portfolio.html" else SKIP_LISTING
    pattern = (
        r'if \(el\.closest\("script, style, noscript, \.lang-switcher"\)\) return true;[\s\S]*?'
        r"if \(el\.isContentEditable\) return true;"
    )
    replacement = skip + "\n    if (el.isContentEditable) return true;"
    out, n = re.subn(pattern, replacement, engine, count=1)
    if n != 1:
        raise RuntimeError(f"shouldSkip patch failed for {page} (n={n})")
    return out


def build_dict(html: str) -> dict:
    subset = {}
    for en, ar in AR.items():
        escaped = en.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if en in html or escaped in html:
            subset[en] = ar
    for key in ALWAYS_KEYS:
        if key in AR:
            subset[key] = AR[key]
    return subset


def insert_css_into_main_style(html: str, css: str) -> str:
    """Insert CSS before the last </style> that precedes </head>."""
    head_end = re.search(r"</head>", html, flags=re.I)
    if not head_end:
        raise RuntimeError("no </head>")
    head = html[: head_end.start()]
    rest = html[head_end.start() :]
    # find last </style> in head that is NOT inside noscript boot (already cleaned)
    matches = list(re.finditer(r"</style>", head, flags=re.I))
    if not matches:
        raise RuntimeError("no </style> in head")
    m = matches[-1]
    return head[: m.start()] + css + "\n  </style>" + head[m.end() :] + rest


def process(page: str, engine_src: str) -> None:
    path = ROOT / page
    html = path.read_text(encoding="utf-8")

    # Fix / replace boot block
    if "ALA_I18N_BOOT" in html:
        html = re.sub(
            r"<!-- ALA_I18N_BOOT -->[\s\S]*?<!-- /ALA_I18N_BOOT -->\s*",
            BOOT,
            html,
            count=1,
        )
    else:
        html = re.sub(r"(<head[^>]*>)", r"\1\n" + BOOT, html, count=1, flags=re.I)

    # Strip any i18n CSS remnants (including broken ones inside noscript)
    html = re.sub(r"/\* ALA_I18N_CSS_START \*/[\s\S]*?/\* ALA_I18N_CSS_END \*/\s*", "", html)

    # Ensure html dir
    def dir_repl(m: re.Match) -> str:
        attrs = m.group(1)
        if "dir=" not in attrs:
            attrs += ' dir="ltr"'
        return "<html" + attrs + ">"

    html = re.sub(r"<html\b([^>]*)>", dir_repl, html, count=1, flags=re.I)

    # Cairo font
    def font_repl(m: re.Match) -> str:
        href = m.group(1)
        if "Cairo" in href:
            return m.group(0)
        href2 = href.replace("family=", "family=Cairo:wght@400;500;600;700&family=", 1)
        return m.group(0).replace(href, href2)

    html = re.sub(
        r'<link href="(https://fonts\.googleapis\.com/css2\?[^"]+)" rel="stylesheet"\s*/?>',
        font_repl,
        html,
        count=1,
    )

    # Ensure switcher
    if 'class="lang-switcher"' not in html:
        switcher = """
        <div class="lang-switcher" role="group" aria-label="Language">
          <button type="button" data-lang-switch="en" lang="en" aria-label="English">EN</button>
          <span class="lang-sep" aria-hidden="true">/</span>
          <button type="button" data-lang-switch="ar" lang="ar" aria-label="العربية">AR</button>
        </div>
"""
        html, _ = re.subn(
            r'(<div class="nav-actions">[\s\S]*?)(\n\s*<button type="button" class="(?:menu-toggle|nav-toggle)")',
            r"\1" + switcher + r"\2",
            html,
            count=1,
        )

    extra = PORTFOLIO_CSS_EXTRA if page == "portfolio.html" else LISTING_CSS_EXTRA
    css_block = SHARED_CSS + extra + "\n/* ALA_I18N_CSS_END */\n"
    html = insert_css_into_main_style(html, css_block)

    # Replace engine block
    html = re.sub(r"<!-- ALA_I18N_START -->[\s\S]*?<!-- ALA_I18N_END -->\s*", "", html)
    subset = build_dict(html)
    engine = patch_should_skip(engine_src, page)
    payload = (
        "<!-- ALA_I18N_START -->\n<script>\nwindow.ALA_I18N_DICT = "
        + json.dumps(subset, ensure_ascii=False)
        + ";\n</script>\n<script>\n"
        + engine
        + "\n</script>\n<!-- ALA_I18N_END -->\n"
    )
    html = re.sub(r"</body>", lambda m: payload + m.group(0), html, count=1, flags=re.I)

    path.write_text(html, encoding="utf-8", newline="\n")

    # Sanity
    boot_ok = (
        '<noscript><style>html.ala-i18n-pending body { visibility: visible !important; }</style></noscript>'
        in html
    )
    css_in_main = bool(
        re.search(
            r"<style>[\s\S]*ALA_I18N_CSS_START[\s\S]*ALA_I18N_CSS_END[\s\S]*</style>\s*</head>",
            html,
            flags=re.I,
        )
    )
    print(
        f"{page}: dict={len(subset)} boot_ok={boot_ok} css_in_main={css_in_main} "
        f"Academy={'Academy' in subset}"
    )


def main() -> None:
    engine = extract_engine_from_index()
    for page in PAGES:
        process(page, engine)


if __name__ == "__main__":
    main()
