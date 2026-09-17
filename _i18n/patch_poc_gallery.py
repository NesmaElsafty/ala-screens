# -*- coding: utf-8 -*-
"""Add CDN gallery to poc.html from images/pocImages.html."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"d:\Projects\Ala Screens")
poc_path = ROOT / "poc.html"
pg_path = ROOT / "pg.html"

urls = [
    u.strip()
    for u in (ROOT / "images" / "pocImages.html").read_text(encoding="utf-8").splitlines()
    if u.strip().startswith("http")
]

poc = poc_path.read_text(encoding="utf-8")
pg = pg_path.read_text(encoding="utf-8")

if 'id="galleryRoot"' in poc:
    raise SystemExit("poc.html already has a gallery")

# CSS from pg: gallery + lightbox block
css_m = re.search(
    r"(    /\* Gallery slider \*/[\s\S]*?\.lightbox-status \{[\s\S]*?\n    \}\n\n)",
    pg,
)
if not css_m:
    raise SystemExit("gallery CSS not found in pg.html")
gallery_css = css_m.group(1)

# Gallery JS from pg (from galleryRoot through keydown handler, before menuToggle)
js_m = re.search(
    r"(      var galleryRoot = document\.getElementById\(\"galleryRoot\"\);[\s\S]*?"
    r"document\.addEventListener\(\"keydown\", function \(e\) \{[\s\S]*?\}\);\n\n)"
    r"      var menuToggle",
    pg,
)
if not js_m:
    raise SystemExit("gallery JS not found in pg.html")
gallery_js_body = js_m.group(1)

gallery_js_items = ",\n        ".join(
    f'{{ src: "{u}", alt: "POC camp photo {i}" }}' for i, u in enumerate(urls, 1)
)
gallery_config = f"""      /* ============================================================
         PROGRAM MEDIA CONFIG
         ============================================================ */
      var galleryImages = [
        {gallery_js_items}
      ];

"""

# 1) body.lightbox-open
if "body.lightbox-open" not in poc:
    poc = poc.replace(
        """    body {
      font-family: "Raleway", system-ui, sans-serif;
      font-size: 16px;
      line-height: 1.6;
      color: var(--charcoal);
      background: var(--warm-white);
      overflow-x: hidden;
      padding-top: 4.75rem;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    img {""",
        """    body {
      font-family: "Raleway", system-ui, sans-serif;
      font-size: 16px;
      line-height: 1.6;
      color: var(--charcoal);
      background: var(--warm-white);
      overflow-x: hidden;
      padding-top: 4.75rem;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    body.lightbox-open {
      overflow: hidden;
    }

    img {""",
        1,
    )

# 2) inject gallery CSS before Final CTA
if "/* Gallery slider */" not in poc:
    if "/* Final CTA */" not in poc:
        raise SystemExit("Final CTA marker missing")
    poc = poc.replace("    /* Final CTA */", gallery_css + "    /* Final CTA */", 1)

# 3) include program-gallery in mobile padding list if present
poc = poc.replace(
    """      .why-program,
      .program-timeline,
      .delivery-options {
        padding: 64px 0;
      }""",
    """      .why-program,
      .program-timeline,
      .delivery-options,
      .program-gallery {
        padding: 64px 0;
      }""",
    1,
)

# 4) gallery HTML section before CTA
gallery_html = """
    <section class="program-gallery" id="program-gallery">
      <div class="container">
        <div class="section-header">
          <p class="eyebrow anim-item">Camp Experience</p>
          <h2 class="section-heading anim-item">Inside the POC Experience</h2>
          <p class="section-intro anim-item">Explore highlights from previous Power of Change camps.</p>
        </div>
        <div class="gallery-slider" id="galleryRoot" aria-roledescription="carousel" aria-label="POC camp photo gallery"></div>
      </div>
    </section>

"""
poc = poc.replace(
    '    <section class="program-cta" id="program-cta">',
    gallery_html + '    <section class="program-cta" id="program-cta">',
    1,
)

# 5) lightbox markup before first page script after whatsapp
lightbox_html = """
  <div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-labelledby="lightboxStatus" hidden>
    <div class="lightbox-inner">
      <button type="button" class="lightbox-close" id="lightboxClose" aria-label="Close gallery">
        <i class="fa-solid fa-xmark" aria-hidden="true"></i>
      </button>
      <button type="button" class="lightbox-prev" id="lightboxPrev" aria-label="Previous image">
        <i class="fa-solid fa-chevron-left" aria-hidden="true"></i>
      </button>
      <img id="lightboxImage" src="" alt="">
      <button type="button" class="lightbox-next" id="lightboxNext" aria-label="Next image">
        <i class="fa-solid fa-chevron-right" aria-hidden="true"></i>
      </button>
      <p class="lightbox-status" id="lightboxStatus"></p>
    </div>
  </div>

"""
poc = poc.replace(
    """  <script>
    (function () {
      var menuToggle = document.getElementById("menuToggle");""",
    lightbox_html
    + """  <script>
    (function () {
"""
    + gallery_config
    + gallery_js_body
    + """      var menuToggle = document.getElementById("menuToggle");""",
    1,
)

poc_path.write_text(poc, encoding="utf-8", newline="\n")
print(f"poc.html: added gallery with {len(urls)} CDN urls")
