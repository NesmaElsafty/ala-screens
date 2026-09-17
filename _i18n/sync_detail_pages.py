# -*- coding: utf-8 -*-
"""Sync approved index.html i18n architecture onto program-detail pages."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(r"d:\Projects\Ala Screens")
AR = json.loads((ROOT / "_i18n" / "ar.json").read_text(encoding="utf-8"))
AR.pop("Academy", None)

# Approved main pages — never touch
FORBIDDEN = {"index.html", "portfolio.html", "programs.html", "camps.html"}

DETAIL_PAGES = (
    "shiftCamp.html",
    "silentCamp.html",
    "poc.html",  # camp detail linked from camps.html
    "acc.html",
    "leadershipKids.html",
    "nlp.html",
    "nlpKids.html",
    "ots.html",
    "pcc.html",
    "pg.html",
    "ps.html",
    "psKids.html",
    "tot.html",
    "ps-recorded.html",
    "eneagram1.html",
)

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
    "Ask About This Program",
    "Ask on WhatsApp",
    "Explore Programs",
    "Open menu",
    "Close menu",
    "Main navigation",
    "Mobile navigation",
    "Toggle menu",
    "Breadcrumb",
    "Program facts",
    "Program quick facts",
    "© Ahmed Latif Academy. All rights reserved.",
    "You're just one step away from joining ALA! Contact us today, and one of our team members will be happy to assist you with the next available course date, course fees, current offers, answer all your questions, and help you complete your registration with ease.",
)

SKIP = (
    'if (el.closest("script, style, noscript, .lang-switcher")) return true;\n'
    "    /* Brand lockup stays English: Ahmed Latif Academy */\n"
    '    if (el.closest(".site-header .logo, .site-header .logo-text, .site-header .logo-academy")) return true;'
)

# Shared + detail-page RTL. Intentionally excludes Home #hero composition rules.
DETAIL_CSS = r"""/* ALA_I18N_CSS_START */
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
html[lang="ar"] .signature-text {
  font-family: "Playfair Display", Georgia, serif;
}

html[lang="ar"] .eyebrow,
html[lang="ar"] .header-cta,
html[lang="ar"] .mobile-nav .header-cta,
html[lang="ar"] .nav-contact,
html[lang="ar"] .block-title,
html[lang="ar"] .featured-badge,
html[lang="ar"] .program-meta-badge {
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

html[dir="rtl"] .program-icon-badge {
  left: auto;
  inset-inline-end: 20px;
}

/* Program detail content — logical alignment (not Home hero) */
html[dir="rtl"] .program-hero-content,
html[dir="rtl"] .program-hero-desc,
html[dir="rtl"] .section-header,
html[dir="rtl"] .outcomes-section .section-header,
html[dir="rtl"] .case-block .eyebrow,
html[dir="rtl"] .case-block,
html[dir="rtl"] .program-card-body,
html[dir="rtl"] .program-card-content,
html[dir="rtl"] .instructor-content,
html[dir="rtl"] .contact-content,
html[dir="rtl"] .lead-form,
html[dir="rtl"] .about-p,
html[dir="rtl"] .audience-card,
html[dir="rtl"] .learning-card,
html[dir="rtl"] .why-card,
html[dir="rtl"] .delivery-card,
html[dir="rtl"] .timeline-step,
html[dir="rtl"] .program-cta-card,
html[dir="rtl"] .quick-fact {
  text-align: start;
}

html[dir="rtl"] .program-hero-actions,
html[dir="rtl"] .program-meta {
  justify-content: flex-start;
}

html[dir="rtl"] .outcomes-list li,
html[dir="rtl"] .feature-list li,
html[dir="rtl"] .checklist li,
html[dir="rtl"] .audience-list li {
  text-align: start;
}

/* Numeric / code-like values stay LTR visually */
html[dir="rtl"] .timeline-num,
html[dir="rtl"] .stat-value,
html[dir="rtl"] .stat-number,
html[dir="rtl"] .stat-counter,
html[dir="rtl"] .gallery-counter,
html[dir="rtl"] .proof-stat strong,
html[dir="rtl"] .quick-fact strong {
  direction: ltr;
  unicode-bidi: isolate;
}

html[dir="rtl"] .stat-item:first-child {
  padding-inline-end: 30px;
  padding-inline-start: 0;
  padding-left: 0;
  padding-right: 0;
}

html[dir="rtl"] .stat-item:last-child {
  padding-inline-start: 30px;
  padding-inline-end: 0;
  padding-left: 0;
  padding-right: 0;
}

html[dir="rtl"] .stat-item:not(:last-child)::after {
  right: auto;
  left: 0;
}

html[dir="rtl"] .gallery-nav-prev,
html[dir="rtl"] .lightbox-prev {
  left: auto;
  right: 14px;
}

html[dir="rtl"] .gallery-nav-next,
html[dir="rtl"] .lightbox-next {
  right: auto;
  left: 14px;
}

html[dir="rtl"] .lightbox-close {
  right: auto;
  left: 0;
}

html[dir="rtl"] .breadcrumb-list {
  flex-direction: row;
}

html[dir="rtl"] .breadcrumb-list li:not(:last-child)::after {
  content: "‹";
}

/* Mobile timeline: keep number on inline-start without physical left lock */
@media (max-width: 900px) {
  html[dir="rtl"] .timeline-track {
    padding-inline-start: 8px;
    padding-left: 0;
  }

  html[dir="rtl"] .timeline-track::before {
    left: auto;
    inset-inline-start: 26px;
  }

  html[dir="rtl"] .timeline-step {
    text-align: start;
  }
}

@media (max-width: 768px) {
  html[dir="rtl"] .whatsapp-float {
    left: 14px;
    right: auto;
  }

  html[dir="rtl"] .gallery-nav-prev,
  html[dir="rtl"] .lightbox-prev {
    right: 8px;
  }

  html[dir="rtl"] .gallery-nav-next,
  html[dir="rtl"] .lightbox-next {
    left: 8px;
  }
}

/* ALA_I18N_CSS_END */
"""


def extract_engine_from_index() -> str:
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(
        r"<!-- ALA_I18N_START -->\s*<script>\s*window\.ALA_I18N_DICT = \{.*?\};\s*</script>\s*<script>([\s\S]*?)</script>\s*<!-- ALA_I18N_END -->",
        html,
    )
    if not m:
        raise RuntimeError("Could not extract engine from index.html")
    return m.group(1).strip()


def patch_should_skip(engine: str) -> str:
    pattern = (
        r'if \(el\.closest\("script, style, noscript, \.lang-switcher"\)\) return true;[\s\S]*?'
        r"if \(el\.isContentEditable\) return true;"
    )
    replacement = SKIP + "\n    if (el.isContentEditable) return true;"
    out, n = re.subn(pattern, replacement, engine, count=1)
    if n != 1:
        raise RuntimeError(f"shouldSkip patch failed (n={n})")
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
    head_end = re.search(r"</head>", html, flags=re.I)
    if not head_end:
        raise RuntimeError("no </head>")
    head = html[: head_end.start()]
    rest = html[head_end.start() :]
    matches = list(re.finditer(r"</style>", head, flags=re.I))
    if not matches:
        raise RuntimeError("no </style> in head")
    m = matches[-1]
    return head[: m.start()] + css + "\n  </style>" + head[m.end() :] + rest


def ensure_cairo(html: str) -> str:
    def repl(m: re.Match) -> str:
        href = m.group(1)
        if "Cairo" in href:
            return m.group(0)
        href2 = href.replace("family=", "family=Cairo:wght@400;500;600;700&family=", 1)
        return m.group(0).replace(href, href2)

    return re.sub(
        r'<link href="(https://fonts\.googleapis\.com/css2\?[^"]+)" rel="stylesheet"\s*/?>',
        repl,
        html,
        count=1,
    )


def ensure_dir(html: str) -> str:
    def repl(m: re.Match) -> str:
        attrs = m.group(1)
        if "dir=" not in attrs:
            attrs += ' dir="ltr"'
        return "<html" + attrs + ">"

    return re.sub(r"<html\b([^>]*)>", repl, html, count=1, flags=re.I)


def ensure_switcher(html: str) -> str:
    if 'class="lang-switcher"' in html:
        return html
    switcher = """
        <div class="lang-switcher" role="group" aria-label="Language">
          <button type="button" data-lang-switch="en" lang="en" aria-label="English">EN</button>
          <span class="lang-sep" aria-hidden="true">/</span>
          <button type="button" data-lang-switch="ar" lang="ar" aria-label="العربية">AR</button>
        </div>
"""
    html2, n = re.subn(
        r'(<div class="header-actions">[\s\S]*?)(\n\s*<button type="button" class="menu-toggle")',
        r"\1" + switcher + r"\2",
        html,
        count=1,
    )
    if n:
        return html2
    html2, n = re.subn(
        r'(<div class="nav-actions">[\s\S]*?)(\n\s*<button type="button" class="(?:menu-toggle|nav-toggle)")',
        r"\1" + switcher + r"\2",
        html,
        count=1,
    )
    return html2 if n else html


def process(page: str, engine_src: str) -> None:
    if page in FORBIDDEN:
        raise RuntimeError(f"Refusing to modify approved page: {page}")
    path = ROOT / page
    if not path.exists():
        raise FileNotFoundError(page)

    html = path.read_text(encoding="utf-8")
    html = ensure_dir(html)
    html = ensure_cairo(html)

    if "ALA_I18N_BOOT" in html:
        html = re.sub(
            r"<!-- ALA_I18N_BOOT -->[\s\S]*?<!-- /ALA_I18N_BOOT -->\s*",
            BOOT,
            html,
            count=1,
        )
    else:
        html = re.sub(r"(<head[^>]*>)", r"\1\n" + BOOT, html, count=1, flags=re.I)

    html = ensure_switcher(html)

    html = re.sub(r"/\* ALA_I18N_CSS_START \*/[\s\S]*?/\* ALA_I18N_CSS_END \*/\s*", "", html)
    html = re.sub(r"<!-- ALA_I18N_START -->[\s\S]*?<!-- ALA_I18N_END -->\s*", "", html)

    html = insert_css_into_main_style(html, DETAIL_CSS)

    subset = build_dict(html)
    engine = patch_should_skip(engine_src)

    payload = (
        "<!-- ALA_I18N_START -->\n<script>\nwindow.ALA_I18N_DICT = "
        + json.dumps(subset, ensure_ascii=False)
        + ";\n</script>\n<script>\n"
        + engine
        + "\n</script>\n<!-- ALA_I18N_END -->\n"
    )
    html = re.sub(r"</body>", lambda m: payload + m.group(0), html, count=1, flags=re.I)

    path.write_text(html, encoding="utf-8", newline="\n")

    boot_ok = (
        '<noscript><style>html.ala-i18n-pending body { visibility: visible !important; }</style></noscript>'
        in html
    )
    css_ok = bool(
        re.search(
            r"ALA_I18N_CSS_START[\s\S]*ALA_I18N_CSS_END[\s\S]*</style>\s*</head>",
            html,
            flags=re.I,
        )
    )
    academy = '"Academy"' in json.dumps(subset)
    brand_skip = "logo-academy" in engine
    print(
        f"{page}: dict={len(subset)} boot={boot_ok} css={css_ok} "
        f"AcademyKey={academy} brandSkip={brand_skip}"
    )


def main() -> None:
    engine = extract_engine_from_index()
    for page in DETAIL_PAGES:
        process(page, engine)


if __name__ == "__main__":
    main()
