# -*- coding: utf-8 -*-
"""Inject standalone EN/AR localization into every ALA HTML page."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(__file__)

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

SWITCHER = """
        <div class="lang-switcher" role="group" aria-label="Language">
          <button type="button" data-lang-switch="en" lang="en" aria-label="English">EN</button>
          <span class="lang-sep" aria-hidden="true">/</span>
          <button type="button" data-lang-switch="ar" lang="ar" aria-label="العربية">AR</button>
        </div>
"""

FUNNEL_BOOT = """
<script>
(function () {
  try {
    var k = "ala-language";
    var q = (location.search.match(/[?&]lang=(en|ar)(?:&|#|$)/) || [])[1];
    var s = null;
    try { s = localStorage.getItem(k); } catch (e) {}
    var lang = (q === "en" || q === "ar") ? q : (s === "en" || s === "ar") ? s : "en";
    if (q) { try { localStorage.setItem(k, lang); } catch (e) {} }
    window.__ALA_BOOT_LANG = lang;
    var d = document.documentElement;
    if (d) {
      d.lang = lang;
      d.dir = lang === "ar" ? "rtl" : "ltr";
      d.setAttribute("lang", lang);
      d.setAttribute("dir", d.dir);
    }
  } catch (e) {}
})();
</script>
"""


def strip_existing(html):
    html = re.sub(r"<!-- ALA_I18N_BOOT -->[\s\S]*?<!-- /ALA_I18N_BOOT -->\s*", "", html)
    html = re.sub(r"/\* ALA_I18N_CSS_START \*/[\s\S]*?/\* ALA_I18N_CSS_END \*/\s*", "", html)
    html = re.sub(r"<!-- ALA_I18N_START -->[\s\S]*?<!-- ALA_I18N_END -->\s*", "", html)
    html = re.sub(r"\n\s*<div class=\"lang-switcher\"[\s\S]*?</div>\n", "\n", html, count=4)
    return html


def add_dir_lang(html):
    def repl(m):
        attrs = m.group(1)
        if "dir=" not in attrs:
            attrs += ' dir="ltr"'
        return "<html" + attrs + ">"
    return re.sub(r"<html\b([^>]*)>", repl, html, count=1, flags=re.I)


def add_cairo(html):
    def repl(m):
        href = m.group(1)
        if "Cairo" in href:
            return m.group(0)
        href = href.replace("family=", "family=Cairo:wght@400;500;600;700&family=", 1)
        return m.group(0).replace(m.group(1), href)
    return re.sub(
        r'<link href="(https://fonts\.googleapis\.com/css2\?[^"]+)" rel="stylesheet"\s*/?>',
        repl,
        html,
        count=1,
    )


def insert_boot(html):
    if re.search(r"<head[^>]*>", html, flags=re.I):
        return re.sub(r"(<head[^>]*>)", r"\1\n" + BOOT, html, count=1, flags=re.I)
    return BOOT + html


def insert_css(html, css):
    if "</style>" in html:
        # last style close in head-ish: replace first </style> after fonts
        return html.replace("</style>", css + "\n  </style>", 1)
    return html


def insert_switcher_academy(html):
    if 'class="lang-switcher"' in html:
        return html
    # before hamburger
    html, n = re.subn(
        r'(<div class="nav-actions">[\s\S]*?)(\n\s*<button type="button" class="menu-toggle")',
        r"\1" + SWITCHER + r"\2",
        html,
        count=1,
    )
    if n:
        return html
    html, n = re.subn(
        r'(<div class="nav-actions">[\s\S]*?)(\n\s*<button type="button" class="nav-toggle")',
        r"\1" + SWITCHER + r"\2",
        html,
        count=1,
    )
    return html


def page_dict(html, all_ar):
    subset = {}
    for en, ar in all_ar.items():
        escaped = (
            en.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        if en in html or escaped in html:
            subset[en] = ar
    # always include a few runtime/constructed keys
    for key in (
        "Language", "English", "Close menu", "Previous photo", "Next photo",
        "Scroll thumbnails left", "Scroll thumbnails right", "Gallery thumbnails",
        "Use the arrows to browse all photos. Click the image to view it larger.",
        "View larger: ", "Show photo ", "Close gallery", "Previous image", "Next image",
        "© Ahmed Latif Academy. All rights reserved.",
        "Hello ALA, I'm interested in: ",
        "Name: ", "Phone: ", "Email: ", "Message: ",
        "Please share the next available course date, fees, and current offers.",
        "You're just one step away from joining ALA! Contact us today, and one of our team members will be happy to assist you with the next available course date, course fees, current offers, answer all your questions, and help you complete your registration with ease.",
        "— Find the learning experience that best fits your goals.",
        "— Get the latest verified schedule, pricing, and available offers.",
        "— Our team will help you complete your registration with ease.",
        "UPCOMING EVENTS", "LATEST NEWS",
    ):
        if key in all_ar:
            subset[key] = all_ar[key]
    return subset


def insert_engine(html, subset, engine_js):
    payload = (
        "<!-- ALA_I18N_START -->\n<script>\nwindow.ALA_I18N_DICT = "
        + json.dumps(subset, ensure_ascii=False)
        + ";\n</script>\n<script>\n"
        + engine_js
        + "\n</script>\n<!-- ALA_I18N_END -->\n"
    )
    if re.search(r"</body>", html, flags=re.I):
        return re.sub(r"</body>", lambda m: payload + m.group(0), html, count=1, flags=re.I)
    return html + payload


def patch_gallery_scroll(html):
    html = html.replace(
        'thumbsEl.scrollBy({ left: -280, behavior: "smooth" });',
        'thumbsEl.scrollBy({ left: (document.documentElement.dir === "rtl" ? 280 : -280), behavior: "smooth" });',
    )
    html = html.replace(
        'thumbsEl.scrollBy({ left: 280, behavior: "smooth" });',
        'thumbsEl.scrollBy({ left: (document.documentElement.dir === "rtl" ? -280 : 280), behavior: "smooth" });',
    )
    return html


def patch_form_messages(html):
    old = '''          var composed =
            "Hello ALA, I'm interested in: " + interest +
            "\\nName: " + name +
            "\\nPhone: " + phone +
            "\\nEmail: " + email +
            (message ? ("\\nMessage: " + message) : "") +
            "\\n\\nPlease share the next available course date, fees, and current offers.";'''
    new = '''          var i18n = window.ALA_I18N;
          var t = function (s) { return i18n && i18n.tText ? i18n.tText(s) : s; };
          var composed =
            t("Hello ALA, I'm interested in: ") + interest +
            "\\n" + t("Name: ") + name +
            "\\n" + t("Phone: ") + phone +
            "\\n" + t("Email: ") + email +
            (message ? ("\\n" + t("Message: ") + message) : "") +
            "\\n\\n" + t("Please share the next available course date, fees, and current offers.");'''
    return html.replace(old, new)


def process_standard(path, css, engine_js, all_ar):
    html = open(path, encoding="utf-8").read()
    html = strip_existing(html)
    html = add_dir_lang(html)
    html = add_cairo(html)
    html = insert_css(html, css)
    html = insert_boot(html)
    html = insert_switcher_academy(html)
    html = patch_gallery_scroll(html)
    html = patch_form_messages(html)
    subset = page_dict(html, all_ar)
    html = insert_engine(html, subset, engine_js)
    open(path, "w", encoding="utf-8", newline="\n").write(html)
    return len(subset)


def process_funnel(path):
    html = open(path, encoding="utf-8").read()
    if "ALA_I18N_FUNNEL_BOOT" not in html:
        html = "<!-- ALA_I18N_FUNNEL_BOOT -->" + FUNNEL_BOOT + "<!-- /ALA_I18N_FUNNEL_BOOT -->\n" + html
    else:
        html = re.sub(
            r"<!-- ALA_I18N_FUNNEL_BOOT -->[\s\S]*?<!-- /ALA_I18N_FUNNEL_BOOT -->\n",
            "<!-- ALA_I18N_FUNNEL_BOOT -->" + FUNNEL_BOOT + "<!-- /ALA_I18N_FUNNEL_BOOT -->\n",
            html,
            count=1,
        )

    html = html.replace('      dir="rtl"', '      dir="ltr"', 1)
    html = html.replace('      data-lang="ar"', '      data-lang="en"', 1)
    html = html.replace(
        '              class="ala-lang-btn is-active"\n              data-ala-lang="ar"',
        '              class="ala-lang-btn"\n              data-ala-lang="ar"',
        1,
    )
    html = html.replace(
        '              class="ala-lang-btn"\n              data-ala-lang="en"',
        '              class="ala-lang-btn is-active"\n              data-ala-lang="en"',
        1,
    )

    html = html.replace("sessionStorage.setItem(", "localStorage.setItem(")
    html = html.replace("sessionStorage.getItem(", "localStorage.getItem(")

    html = html.replace(
        '''        let savedLanguage = "ar";


        try {

          savedLanguage =
            localStorage.getItem(
              "ala-language"
            ) || "ar";

        } catch (error) {}


        setLanguage(
          savedLanguage === "en"
            ? "en"
            : "ar"
        );''',
        '''        let savedLanguage = window.__ALA_BOOT_LANG || "en";


        try {

          var queryLang = (location.search.match(/[?&]lang=(en|ar)(?:&|#|$)/) || [])[1];
          var storedLang = localStorage.getItem("ala-language");
          savedLanguage = queryLang || storedLang || window.__ALA_BOOT_LANG || "en";

        } catch (error) {}


        setLanguage(
          savedLanguage === "ar"
            ? "ar"
            : "en"
        );'''
    )

    # persist URL + documentElement inside existing setLanguage
    if "searchParams.set" not in html:
        html = html.replace(
            '''          try {

            localStorage.setItem(
              "ala-language",
              lang
            );

          } catch (error) {}

        }''',
            '''          try {

            localStorage.setItem(
              "ala-language",
              lang
            );

          } catch (error) {}

          try {
            var nextUrl = new URL(window.location.href);
            nextUrl.searchParams.set("lang", lang);
            window.history.replaceState({}, "", nextUrl.toString());
            document.documentElement.lang = lang;
            document.documentElement.dir = isArabic ? "rtl" : "ltr";
            document.documentElement.setAttribute("lang", lang);
            document.documentElement.setAttribute("dir", document.documentElement.dir);
          } catch (error) {}

        }''',
            1,
        )

    open(path, "w", encoding="utf-8", newline="\n").write(html)


def main():
    css = open(os.path.join(HERE, "i18n.css"), encoding="utf-8").read()
    engine_js = open(os.path.join(HERE, "engine.js"), encoding="utf-8").read()
    all_ar = json.load(open(os.path.join(HERE, "ar.json"), encoding="utf-8"))

    for name in sorted(os.listdir(ROOT)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(ROOT, name)
        if name == "ps-recorded-funnel.html":
            process_funnel(path)
            print("funnel patched", name)
            continue
        n = process_standard(path, css, engine_js, all_ar)
        print("%s  dict=%s  switcher=%s" % (
            name.ljust(24),
            n,
            "yes" if 'class="lang-switcher"' in open(path, encoding="utf-8").read() else "NO",
        ))


if __name__ == "__main__":
    main()
