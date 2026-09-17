# -*- coding: utf-8 -*-
"""Extract leaf-level user-facing strings."""
import html as htmlmod
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_FILES = {"ps-recorded-funnel.html"}
TEXT_RE = re.compile(r"[A-Za-z]")
ICON_OR_EMPTY = re.compile(r"^\s*(?:<i\b[^>]*>.*?</i>|<br\s*/?>|&nbsp;|\s)*\s*$", re.I | re.S)

LEAF_TAGS = (
    "p", "h1", "h2", "h3", "h4", "h5", "label", "option", "button", "a",
    "span", "li", "strong", "small", "legend", "blockquote", "figcaption",
    "th", "td", "div", "title"
)


def leaf_text(inner):
    # remove icons
    inner = re.sub(r"<i\b[^>]*>.*?</i>", " ", inner, flags=re.I | re.S)
    inner = re.sub(r"<br\s*/?>", " ", inner, flags=re.I)
    if re.search(r"<[a-zA-Z]", inner):
        return None  # has nested tags
    t = " ".join(htmlmod.unescape(inner).split())
    return t if t and TEXT_RE.search(t) else None


def extract_file(path):
    raw = open(path, encoding="utf-8").read()
    stripped = re.sub(r"<script[\s\S]*?</script>", " ", raw, flags=re.I)
    stripped = re.sub(r"<style[\s\S]*?</style>", " ", stripped, flags=re.I)
    found = []
    for tag in LEAF_TAGS:
        for m in re.finditer(rf"<{tag}\b([^>]*)>(.*?)</{tag}>", stripped, flags=re.I | re.S):
            t = leaf_text(m.group(2))
            if t:
                found.append(t)
    for attr in ("alt", "placeholder", "aria-label", "title"):
        for m in re.finditer(rf'\b{attr}=["\']([^"\']+)["\']', stripped, flags=re.I):
            t = htmlmod.unescape(m.group(1)).strip()
            if t and TEXT_RE.search(t):
                found.append(t)
    for m in re.finditer(
        r'<meta[^>]+(?:name|property)=["\'](?:description|og:title|og:description)["\'][^>]*content=["\']([^"\']+)["\']',
        raw, flags=re.I):
        found.append(htmlmod.unescape(m.group(1)).strip())
    for m in re.finditer(
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*(?:name|property)=["\'](?:description|og:title|og:description)["\']',
        raw, flags=re.I):
        found.append(htmlmod.unescape(m.group(1)).strip())
    # JS strings of interest
    for block in re.findall(r"<script[\s\S]*?</script>", raw, flags=re.I):
        for s in re.findall(r'"([^"\n]{8,160})"', block):
            if TEXT_RE.search(s) and not s.startswith("http") and "fa-" not in s and "function" not in s:
                if any(k in s.lower() for k in (
                    "photo", "gallery", "scroll", "previous", "next", "close",
                    "hello ala", "all rights", "view larger", "show photo",
                    "interested in", "please share", "use the arrows"
                )):
                    found.append(s)
    seen = set()
    unique = []
    for t in found:
        if t in seen:
            continue
        if t.startswith("http") or t.startswith("www."):
            continue
        if re.fullmatch(r"[\d+\-.,/%KMh:]+", t):
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
    out = os.path.join(os.path.dirname(__file__), "leaves.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"all": all_unique, "by_file": {k: v for k, v in report.items()}}, fh, ensure_ascii=False, indent=2)
    print("unique leaf strings", len(all_unique))
    for f, s in report.items():
        print(f"{f:30s} {len(s)}")


if __name__ == "__main__":
    main()
