from pathlib import Path

path = Path(r"d:\Projects\Ala Screens\index.html")
text = path.read_text(encoding="utf-8")

start = "/* Desktop RTL hero — visual left; signature as caption BELOW portrait */"
end = 'html[dir="rtl"] .gallery-nav-prev,'

i = text.find(start)
j = text.find(end)
if i < 0 or j < 0 or j <= i:
    raise SystemExit(f"markers not found i={i} j={j}")

replacement = r'''/* Desktop RTL hero — PERSON toward center/RIGHT; SIGNATURE to LEFT */
@media (min-width: 1100px) {
  html[dir="rtl"] #hero {
    overflow: visible;
  }

  html[dir="rtl"] #hero .hero-grid {
    padding-bottom: 8px;
  }

  html[dir="rtl"] #hero .hero-content {
    width: 52%;
    max-width: 520px;
    margin-inline-start: 0;
    margin-inline-end: auto;
    padding-inline-start: 16px;
    z-index: 4;
  }

  html[dir="rtl"] #hero .hero-desc {
    max-width: 100%;
  }

  /*
    Visual zone stays LEFT half, but composition sits toward CENTER
    (person moves RIGHT relative to previous far-left placement).
  */
  html[dir="rtl"] #hero .hero-visual {
    left: 0;
    right: 48%;
  }

  /* Person + circle toward the right side of the visual zone (toward center) */
  html[dir="rtl"] #hero .hero-instructor {
    left: 64%;
    transform: translateX(-50%) translateY(-16px) scale(1.06);
    transform-origin: bottom center;
  }

  html[dir="rtl"] #hero .hero-circle--lg {
    left: 60%;
    right: auto;
    transform: translateX(-50%);
  }

  html[dir="rtl"] #hero .hero-circle--sm {
    left: 66%;
    right: auto;
    transform: translateX(-50%);
  }

  /*
    Signature in LEFT negative space of the portrait — NOT between
    person and Arabic content.
  */
  html[dir="rtl"] #hero .hero-signature {
    left: 2%;
    right: auto;
    bottom: 56px;
    text-align: left;
    z-index: 3;
    max-width: 38%;
    pointer-events: none;
  }

  html[dir="rtl"] #hero .hero-dots {
    left: 2%;
    right: auto;
    top: 6px;
  }

  html[dir="rtl"] #hero .hero-waves {
    left: auto;
    right: 4%;
  }
}

@media (min-width: 1200px) {
  html[dir="rtl"] #hero .hero-visual {
    left: 1%;
    right: 47%;
  }

  html[dir="rtl"] #hero .hero-instructor {
    left: 66%;
  }

  html[dir="rtl"] #hero .hero-circle--lg {
    left: 62%;
  }

  html[dir="rtl"] #hero .hero-circle--sm {
    left: 68%;
  }

  html[dir="rtl"] #hero .hero-signature {
    left: 3%;
    bottom: 60px;
  }
}

@media (min-width: 1400px) {
  html[dir="rtl"] #hero .hero-visual {
    left: 2%;
    right: 46%;
  }

  html[dir="rtl"] #hero .hero-instructor {
    left: 68%;
  }

  html[dir="rtl"] #hero .hero-circle--lg {
    left: 64%;
  }

  html[dir="rtl"] #hero .hero-circle--sm {
    left: 70%;
  }

  html[dir="rtl"] #hero .hero-signature {
    left: 4%;
    bottom: 64px;
  }
}

/* Tablet: no desktop absolute offsets */
@media (min-width: 769px) and (max-width: 1099px) {
  html[dir="rtl"] #hero .hero-grid {
    grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
    align-items: center;
    padding-bottom: 28px;
  }

  html[dir="rtl"] #hero .hero-content {
    max-width: none;
    width: auto;
  }

  html[dir="rtl"] #hero .hero-visual {
    overflow: visible;
    position: relative;
    left: auto;
    right: auto;
  }

  html[dir="rtl"] #hero .hero-instructor {
    left: 55%;
    transform: translateX(-50%);
    max-width: 100%;
  }

  html[dir="rtl"] #hero .hero-signature {
    left: 4%;
    right: auto;
    bottom: 20px;
    text-align: left;
    max-width: 42%;
  }

  html[dir="rtl"] #hero .hero-dots {
    left: 0;
    right: auto;
  }
}

@media (max-width: 768px) {
  html[dir="rtl"] #hero .hero-stats {
    flex-wrap: wrap;
    gap: 20px;
  }

  html[dir="rtl"] #hero .hero-stats .stat-item {
    flex: 1 1 calc(50% - 12px);
    min-width: 140px;
    padding-inline: 0;
  }

  html[dir="rtl"] #hero .hero-stats .stat-item:not(:last-child)::after {
    display: none;
  }

  html[dir="rtl"] #hero .hero-visual {
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: visible;
    padding-bottom: 8px;
  }

  html[dir="rtl"] #hero .hero-signature {
    position: relative;
    right: auto;
    left: auto;
    bottom: auto;
    margin: 10px auto 0;
    text-align: center;
    max-width: none;
    z-index: 3;
  }

  html[dir="rtl"] #hero .hero-dots {
    left: 0;
    right: auto;
  }
}

'''

path.write_text(text[:i] + replacement + text[j:], encoding="utf-8", newline="\n")
print("ok", i, j)
