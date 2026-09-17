# -*- coding: utf-8 -*-
"""Extract unique user-facing strings from ALA HTML pages."""
import html as htmlmod
import json
import os
import re
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_TAGS = {"script", "style", "noscript"}
ATTRS = ("alt", "placeholder", "aria-label", "title", "content")
SKIP_FILES = {"ps-recorded-funnel.html"}  # already bilingual; handled separately

TEXT_RE = re.compile(r"[A-Za-z]")


class Extractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.buf = []
        self.texts = []
        self.attrs_found = []

    def handle_starttag(self, tag, attrs):
        if tag in SKIP_TAGS:
            self.skip += 1
        ad = dict(attrs)
        for a in ATTRS:
            if a in ad and ad[a] and TEXT_RE.search(ad[a]):
                val = ad[a].strip()
                if a == "content" and tag not in ("meta",):
                    continue
                self.attrs_found.append((tag, a, val))
        if tag in ("title",) and self.skip == 0:
            self.buf = []

    def handle_endtag(self, tag):
        if tag in SKIP_TAGS and self.skip:
            self.skip -= 1
        if self.skip:
            return
        if tag in {
            "p", "h1", "h2", "h3", "h4", "h5", "label", "option", "button",
            "a", "span", "li", "strong", "small", "div", "td", "th", "figcaption",
            "blockquote", "dt", "dd", "legend", "title"
        }:
            text = " ".join("".join(self.buf).split())
            self.buf = []
            if text and TEXT_RE.search(text) and len(text) > 1:
                self.texts.append((tag, text))
        else:
            # keep buffer for parent
            pass

    def handle_data(self, data):
        if self.skip:
            return
        self.buf.append(data)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


# Simpler: collect all text nodes and attributes with regex from body
def extract_file(path):
    raw = open(path, encoding="utf-8").read()
    # strip scripts/styles
    stripped = re.sub(r"<script[\s\S]*?</script>", " ", raw, flags=re.I)
    stripped = re.sub(r"<style[\s\S]*?</style>", " ", stripped, flags=re.I)
    # title
    titles = re.findall(r"<title[^>]*>(.*?)</title>", stripped, flags=re.I | re.S)
    metas = re.findall(
        r'<meta[^>]*(?:name|property)=["\'](?:description|og:title|og:description)["\'][^>]*content=["\']([^"\']+)["\']',
        raw,
        flags=re.I,
    )
    metas += re.findall(
        r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*(?:name|property)=["\'](?:description|og:title|og:description)["\']',
        raw,
        flags=re.I,
    )
    alts = re.findall(r'\balt=["\']([^"\']+)["\']', stripped, flags=re.I)
    placeholders = re.findall(r'\bplaceholder=["\']([^"\']+)["\']', stripped, flags=re.I)
    arias = re.findall(r'\baria-label=["\']([^"\']+)["\']', stripped, flags=re.I)
    titles_attr = re.findall(r'\btitle=["\']([^"\']+)["\']', stripped, flags=re.I)
    options = re.findall(r"<option[^>]*>(.*?)</option>", stripped, flags=re.I | re.S)

    # visible text: tags that typically hold copy
    chunks = re.findall(
        r"<(p|h1|h2|h3|h4|h5|label|button|a|span|li|strong|small|legend|blockquote|figcaption|th|td)[^>]*>(.*?)</\1>",
        stripped,
        flags=re.I | re.S,
    )
    texts = []
    for tag, inner in chunks:
        inner_no_tags = re.sub(r"<[^>]+>", " ", inner)
        inner_no_tags = htmlmod.unescape(inner_no_tags)
        t = " ".join(inner_no_tags.split())
        if t and TEXT_RE.search(t):
            texts.append(t)

    extras = []
    for lst in (titles, metas, alts, placeholders, arias, titles_attr):
        extras.extend(htmlmod.unescape(x).strip() for x in lst if x and TEXT_RE.search(x))
    extras.extend(" ".join(htmlmod.unescape(re.sub(r"<[^>]+>", " ", o)).split()) for o in options)

    # JS-generated English strings
    js_blocks = re.findall(r"<script[\s\S]*?</script>", raw, flags=re.I)
    js_strings = []
    for block in js_blocks:
        js_strings += re.findall(r'"(Previous photo|Next photo|Scroll thumbnails left|Scroll thumbnails right|Gallery thumbnails|Use the arrows to browse all photos\. Click the image to view it larger\.|View larger: |Show photo |Close gallery|Previous image|Next image|All rights reserved\.)"', block)
        js_strings += re.findall(r"'(Hello ALA, I.m interested in: |Name: |Phone: |Email: |Message: |Please share the next available course date, fees, and current offers\.)'", block)

    all_texts = texts + extras + js_strings
    # unique preserve order
    seen = set()
    unique = []
    for t in all_texts:
        t = t.strip()
        if not t or t in seen:
            continue
        # skip urls, classes, mostly numeric
        if t.startswith("http") or t.startswith("www."):
            continue
        if re.fullmatch(r"[\d+\-.,/%KMh]+", t):
            continue
        if len(t) < 2:
            continue
        seen.add(t)
        unique.append(t)
    return unique


def main():
    files = [f for f in os.listdir(ROOT) if f.endswith(".html") and f not in SKIP_FILES]
    report = {}
    all_unique = []
    seen = set()
    for f in sorted(files):
        strings = extract_file(os.path.join(ROOT, f))
        report[f] = strings
        for s in strings:
            if s not in seen:
                seen.add(s)
                all_unique.append(s)
    out = os.path.join(os.path.dirname(__file__), "extracted.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"all": all_unique, "by_file": report}, fh, ensure_ascii=False, indent=2)
    print("files", len(files))
    print("unique strings", len(all_unique))
    print("wrote", out)


if __name__ == "__main__":
    main()
