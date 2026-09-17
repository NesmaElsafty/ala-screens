# -*- coding: utf-8 -*-
"""Build eneagram2.html from eneagram1.html design shell + exact PDF content."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(r"d:\Projects\Ala Screens")
SRC = ROOT / "eneagram1.html"
OUT = ROOT / "eneagram2.html"
IMG_DIR = ROOT / "images" / "eneagram 2"
AR_JSON = ROOT / "_i18n" / "ar.json"

# --- Exact English from eneagram2.pdf ---
EN_TITLE_LINE = "A Deeper Understanding of Personalities, and How to Handle Them with Greater Awareness"
EN_OPEN = (
    'Ever felt like you finally understood someone... and then they did something that '
    'completely caught you off guard, leaving you thinking, "wait, isn\'t that not who they usually are?"'
)
EN_P1 = (
    'The truth is, knowing someone\'s type is only the first door. The 9 types tell you "who" someone is... '
    'but they don\'t tell you why the same person can be quiet and withdrawn one day, and social and open '
    'the very next, while still being exactly the same type. That difference isn\'t random — and that\'s '
    'exactly what Level 2 reveals.'
)
EN_P2 = (
    "Once you understand the basics — that everyone has a core type driving them — it's time to open up "
    "a much deeper layer. At this level, it's not just about knowing someone is a Type 1 or a Type 7. "
    "It's about understanding how that type shifts under stress, how it shows up differently depending "
    "on the situation, and how each personality carries subtypes that significantly shape its behavior."
)
EN_P3 = (
    "Subtypes reveal that the same type can look completely different from one person to the next. "
    "One person might be quiet and introverted, while another with the exact same type is social and "
    "outspoken — yet the inner drive behind both is identical. Without understanding that difference, "
    "you end up judging people by surface behavior instead of what's actually driving them."
)
EN_LEARN_HEAD = "At this level, you'll start to understand:"
EN_BULLETS = [
    "Subtypes and their real influence on behavior",
    "How each type shifts under stress versus in states of security",
    "Reading deeper motivations, not just surface actions",
    "How to approach each personality in the way that genuinely fits them",
    "Improving communication and reducing conflict in relationships",
    "Understanding personality dynamics at work and in everyday life",
]
EN_GOAL_HEAD = "The goal here isn't to label people even more..."
EN_GOAL_BODY = (
    "It's to reach a deeper understanding that lets you respond with flexibility and awareness, "
    "instead of the quick reactions or surface-level judgments we all fall into without even realizing it."
)
EN_CLOSE = (
    'Once you reach Level 2, you\'re no longer just "understanding personalities." You now have the '
    "ability to read beyond behavior, and engage with the actual person — not just their actions."
)
EN_GALLERY = "Watch photos and videos from past batches and see the difference for yourself."
EN_CTA_HEAD = "What you see on the surface never tells the whole story."
EN_CTA_BODY = "Book your seat in Level 2 and start seeing what's behind it."
EN_CTA = f"{EN_CTA_HEAD} {EN_CTA_BODY}"

# --- Exact Arabic from eneagram2.pdf (orthography normalized from presentation forms) ---
AR_TITLE_LINE = "فهم أعمق للشخصيات والتعامل معها بوعي أعلى"
AR_OPEN = (
    'جربت قبل كده إنك تحس إنك فاهم حد... وبعدين يتصرف بطريقة مفاجئة تماماً، وتقولها لنفسك '
    '"طب ده مش كان النمط بتاعه كده؟"'
)
AR_P1 = (
    'الحقيقة إن معرفة نمط حد هي بس أول باب. الأنماط التسعة بتقولك "مين هو"... بس مش بتقولك ليه في يوم '
    "بيبقى هادي ومنسحب، وفي يوم تاني نفسه بالظبط بيبان اجتماعي ومنفتح. الفرق ده مش صدفة، وده بالظبط اللي "
    "Level 2 هيوريهولك."
)
AR_P2 = (
    "بعد ما فهمت الأساسيات وإن كل شخص له نمط أساسي بيحركه، جه وقت تفتح طبقة أعمق بكتير. الفكرة هنا مش إنك "
    "تعرف إن الشخص Type 1 أو Type 7... الفكرة إنك تفهم إزاي النمط ده بيتغير تحت الضغط، وإزاي بيظهر بشكل "
    "مختلف حسب الموقف، وإزاي كل شخصية جواها دوافع فرعية (Subtypes) بتأثر على سلوكها بشكل كبير."
)
AR_P3 = (
    "الـ Subtypes بتوضح إن نفس النمط ممكن يبان بأشكال مختلفة جداً... شخص بيكون هادي ومنطوي، وشخص تاني "
    "من نفس النمط بيكون اجتماعي وواضح، بس الدافع الداخلي واحد بالظبط. لو ماتعرفش الفرق ده، هتفضل تحكم على "
    "الناس من الشكل الظاهري، مش من اللي بيحركها فعلاً."
)
AR_LEARN_HEAD = "في المستوى ده هتبدأ تفهم:"
AR_BULLETS = [
    "الـ Subtypes وتأثيرها الحقيقي على السلوك",
    "إزاي كل نمط بيتغير تحت الضغط أو تحت الراحة",
    "قراءة أعمق للدوافع، مش بس الأفعال الظاهرة",
    "إزاي تتعامل مع كل شخصية بالطريقة اللي تناسبها هي بالظبط",
    "تحسين التواصل وتقليل الصدام في العلاقات",
    "فهم ديناميكية الشخصيات في الشغل والحياة اليومية",
]
AR_GOAL_HEAD = "الهدف هنا مش تصنّف الناس أكتر..."
AR_GOAL_BODY = (
    "لكن إنك توصل لفهم أعمق يخليك تتعامل بمرونة ووعي، بدل ردود الفعل السريعة أو الأحكام السطحية اللي "
    "بنقع فيها كلنا من غير ما نحس."
)
AR_CLOSE = (
    'لما توصل لـ Level 2، إنت مش بس "بتفهم الشخصيات"... إنت بقى عندك قدرة تقرأ ما وراء السلوك، '
    "وتتعامل مع الإنسان نفسه، مش مجرد تصرفاته."
)
AR_GALLERY = "اتفرج على صور وفيديوهات الدفعات اللي فاتت وشوف بنفسك الفرق اللي حصل معاهم."
AR_CTA_HEAD = "السلوك اللي بتشوفه مش دايماً بيحكي القصة كلها..."
AR_CTA_BODY = "احجز مكانك في Level 2 وابدأ تشوف اللي وراه."
AR_CTA = f"{AR_CTA_HEAD} {AR_CTA_BODY}"

META_EN = (
    "Enneagram Level 2 | A Deeper Understanding of Personalities, and How to Handle Them with "
    "Greater Awareness — Live, 44 Hours | Ahmed Latif Academy"
)
META_AR = (
    "Enneagram المستوى 2 | فهم أعمق للشخصيات والتعامل معها بوعي أعلى — مباشر، 44 ساعة | Ahmed Latif Academy"
)

WA_INTEREST_EN = (
    "Hello ALA, I'm interested in the Enneagram | Level 2 program. Please share the next available "
    "dates, fees, and current offers."
)
WA_INTEREST_AR = (
    "مرحباً ALA، أنا مهتم/ة ببرنامج Enneagram | المستوى 2. يرجى مشاركة أقرب المواعيد المتاحة والرسوم والعروض الحالية."
)
WA_GENERIC = (
    "You're just one step away from joining ALA! Contact us today, and one of our team members will "
    "be happy to assist you with the next available course date, course fees, current offers, answer "
    "all your questions, and help you complete your registration with ease."
)


def gallery_files() -> list[str]:
    files = sorted(
        p.name
        for p in IMG_DIR.iterdir()
        if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}
    )
    if not files:
        raise SystemExit(f"No images in {IMG_DIR}")
    return files


def hero_image(files: list[str]) -> str:
    # Prefer an Opening shot for hero; fall back to first image
    for name in files:
        if "Opening" in name:
            return name
    return files[0]


def main() -> None:
    html = SRC.read_text(encoding="utf-8")
    files = gallery_files()
    hero = hero_image(files)
    hero_src = "images/eneagram%202/" + quote(hero)

    # Meta
    html = html.replace(
        "Enneagram | Level 1 | Ahmed Latif Academy",
        "Enneagram | Level 2 | Ahmed Latif Academy",
    )
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{META_EN}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{META_EN}">',
        html,
        count=1,
    )

    # Extra CSS for story + 2-col quick facts + contain-friendly gallery stage
    extra_css = """
    .quick-facts-grid.facts-2 {
      grid-template-columns: repeat(2, minmax(0, 1fr));
      max-width: 640px;
      margin-inline: auto;
    }
    .program-story {
      background: var(--white);
      padding: 88px 0;
    }
    .program-story .story-stack {
      max-width: 760px;
      margin: 0 auto;
      display: grid;
      gap: 20px;
    }
    .program-story .story-stack p {
      font-size: 16px;
      line-height: 1.8;
      color: var(--muted-text);
    }
    .program-story .section-header {
      text-align: center;
      margin-bottom: 36px;
    }
    .program-story .section-heading {
      max-width: 820px;
      margin-left: auto;
      margin-right: auto;
    }
    .goal-section {
      background: var(--white);
      padding: 88px 0;
    }
    .goal-section .goal-stack {
      max-width: 760px;
      margin: 0 auto;
      display: grid;
      gap: 18px;
    }
    .goal-section .goal-stack p {
      font-size: 16px;
      line-height: 1.8;
      color: var(--muted-text);
    }
    .goal-section .section-heading {
      max-width: 820px;
    }
    .gallery-stage-btn img {
      object-fit: contain;
      background: #111;
    }
    .gallery-thumb img {
      object-fit: cover;
    }
    html[dir="rtl"] .program-story .story-stack p,
    html[dir="rtl"] .goal-section .goal-stack p {
      font-family: "Cairo", "Raleway", sans-serif;
    }
"""
    html = html.replace("    /* Learning */", extra_css + "\n    /* Learning */", 1)

    # Replace main content from breadcrumb current through end of CTA
    main_content = f"""    <nav class="breadcrumb" aria-label="Breadcrumb">
      <div class="container">
        <ol class="breadcrumb-list">
          <li><a href="https://link.cashprocess.io/preview/LFFNtiNpdGcVJBl4zV8u" target="_top">Home</a></li>
          <li><a href="https://link.cashprocess.io/preview/fRaRY5RMY05VbnLSxGoO" target="_top">Programs</a></li>
          <li class="breadcrumb-current" aria-current="page">Enneagram | Level 2</li>
        </ol>
      </div>
    </nav>

    <section class="program-hero" id="program-hero">
      <div class="container program-hero-grid">
        <div class="program-hero-content">
          <p class="eyebrow anim-item">Live Program</p>
          <h1 class="program-hero-title anim-item">
            <span class="line-dark">Enneagram</span>
            <span class="line-gold">Level 2</span>
          </h1>
          <p class="program-hero-desc anim-item">{EN_OPEN}</p>
          <div class="program-meta anim-item" aria-label="Program facts">
            <span class="program-meta-badge"><i class="fa-regular fa-circle-dot" aria-hidden="true"></i> Live Program</span>
            <span class="program-meta-badge"><i class="fa-regular fa-clock" aria-hidden="true"></i> 44 Hours</span>
          </div>
          <div class="program-hero-actions">
            <a href="#program-cta" class="btn-primary anim-scale">Ask About This Program</a>
            <a class="btn-secondary anim-scale" id="heroWhatsApp" href="https://wa.me/201010002231?text={quote(WA_GENERIC)}" target="_blank" rel="noopener noreferrer">
              <i class="fa-brands fa-whatsapp" aria-hidden="true"></i> Ask on WhatsApp
            </a>
          </div>
        </div>

        <div class="program-hero-visual anim-right">
          <div class="hero-deco" aria-hidden="true">
            <div class="hero-circle hero-circle--lg"></div>
            <div class="hero-circle hero-circle--sm"></div>
            <span class="hero-dot-detail"></span>
          </div>
          <div class="program-hero-frame">
            <img
              id="programHeroImage"
              src="{hero_src}"
              alt="Participants during a live Enneagram Level 2 training with Ahmed Latif Academy"
              width="960"
              height="1200"
              loading="eager"
              fetchpriority="high"
              decoding="async"
            >
          </div>
        </div>
      </div>
    </section>

    <section class="quick-facts" id="quick-facts" aria-label="Program quick facts">
      <div class="container">
        <div class="quick-facts-grid facts-2">
          <div class="quick-fact anim-scale">
            <i class="fa-regular fa-circle-dot" aria-hidden="true"></i>
            <strong>Live</strong>
            <span>Program</span>
          </div>
          <div class="quick-fact anim-scale">
            <i class="fa-regular fa-clock" aria-hidden="true"></i>
            <strong>44 Hours</strong>
            <span>Training</span>
          </div>
        </div>
      </div>
    </section>

    <section class="program-story" id="program-story">
      <div class="container">
        <div class="section-header">
          <p class="eyebrow anim-item">Enneagram Level 2</p>
          <h2 class="section-heading anim-item">{EN_TITLE_LINE}</h2>
        </div>
        <div class="story-stack">
          <p class="anim-item">{EN_P1}</p>
          <p class="anim-item">{EN_P2}</p>
          <p class="anim-item">{EN_P3}</p>
        </div>
      </div>
    </section>

    <section class="outcomes-section" id="learning">
      <div class="container">
        <div class="section-header">
          <h2 class="section-heading anim-item">{EN_LEARN_HEAD}</h2>
        </div>
        <ul class="outcomes-list">
{chr(10).join(
    f'          <li class="anim-item"><i class="fa-solid fa-check" aria-hidden="true"></i><span>{b}</span></li>'
    for b in EN_BULLETS
)}
        </ul>
      </div>
    </section>

    <section class="goal-section" id="program-goal">
      <div class="container">
        <div class="section-header">
          <h2 class="section-heading anim-item">{EN_GOAL_HEAD}</h2>
        </div>
        <div class="goal-stack">
          <p class="anim-item">{EN_GOAL_BODY}</p>
          <p class="anim-item">{EN_CLOSE}</p>
        </div>
      </div>
    </section>

    <section class="program-gallery" id="program-gallery">
      <div class="container">
        <div class="section-header">
          <p class="eyebrow anim-item">Program Experience</p>
          <h2 class="section-heading anim-item">{EN_GALLERY}</h2>
        </div>
        <div class="gallery-slider" id="galleryRoot" aria-roledescription="carousel" aria-label="Enneagram Level 2 program photo gallery"></div>
      </div>
    </section>

    <section class="program-cta" id="program-cta">
      <div class="container">
        <div class="program-cta-card anim-item">
          <h2>{EN_CTA_HEAD}</h2>
          <p>{EN_CTA_BODY}</p>
          <div class="program-cta-actions">
            <a class="btn-primary" id="ctaAskProgram" href="https://wa.me/201010002231?text={quote(WA_INTEREST_EN)}" target="_blank" rel="noopener noreferrer">Ask About This Program</a>
            <a class="btn-secondary" href="https://wa.me/201010002231?text={quote(WA_GENERIC)}" target="_blank" rel="noopener noreferrer">
              <i class="fa-brands fa-whatsapp" aria-hidden="true"></i> Ask on WhatsApp
            </a>
          </div>
        </div>
      </div>
    </section>
"""

    html = re.sub(
        r"    <nav class=\"breadcrumb\"[\s\S]*?</section>\s*\n  </main>",
        main_content + "  </main>",
        html,
        count=1,
    )

    # Gallery local files (tot.html pattern)
    files_js = ",\n        ".join(f'"{f}"' for f in files)
    gallery_block = f"""      var galleryFolder = "images/eneagram%202/";
      var galleryFiles = [
        {files_js}
      ];
      var galleryImages = galleryFiles.map(function (file, index) {{
        return {{
          src: galleryFolder + encodeURIComponent(file),
          alt: "Enneagram Level 2 program photo " + (index + 1)
        }};
      }});"""

    html = re.sub(
        r"      var galleryImages = \[[\s\S]*?\];",
        gallery_block,
        html,
        count=1,
    )

    # Build i18n program keys
    program_i18n = {
        "Enneagram | Level 2": "Enneagram | المستوى 2",
        "Enneagram | Level 2 | Ahmed Latif Academy": "Enneagram | المستوى 2 | Ahmed Latif Academy",
        META_EN: META_AR,
        "Level 2": "المستوى 2",
        "Enneagram Level 2": "Enneagram المستوى 2",
        EN_TITLE_LINE: AR_TITLE_LINE,
        EN_OPEN: AR_OPEN,
        EN_P1: AR_P1,
        EN_P2: AR_P2,
        EN_P3: AR_P3,
        EN_LEARN_HEAD: AR_LEARN_HEAD,
        EN_GOAL_HEAD: AR_GOAL_HEAD,
        EN_GOAL_BODY: AR_GOAL_BODY,
        EN_CLOSE: AR_CLOSE,
        EN_GALLERY: AR_GALLERY,
        EN_CTA_HEAD: AR_CTA_HEAD,
        EN_CTA_BODY: AR_CTA_BODY,
        EN_CTA: AR_CTA,
        "44 Hours": "44 ساعة",
        "Participants during a live Enneagram Level 2 training with Ahmed Latif Academy": (
            "مشاركون خلال تدريب Enneagram المستوى 2 مباشر مع Ahmed Latif Academy"
        ),
        "Enneagram Level 2 program photo gallery": "معرض صور برنامج Enneagram المستوى 2",
        WA_INTEREST_EN: WA_INTEREST_AR,
    }
    for en_b, ar_b in zip(EN_BULLETS, AR_BULLETS):
        program_i18n[en_b] = ar_b

    # Merge into existing page dict: keep shared UI keys, drop Level-1-only keys by rebuilding from ALWAYS + program
    m = re.search(r"window\.ALA_I18N_DICT = (\{.*?\});", html, re.S)
    if not m:
        raise SystemExit("ALA_I18N_DICT not found")
    old_dict = json.loads(m.group(1))

    # Keep shared UI keys that are not clearly Level-1 specific
    drop_prefixes = ()
    level1_keys = [
        k
        for k in list(old_dict)
        if (
            "Level 1" in k
            or "9 Personality" in k
            or "9 Types" in k
            or "3 Centers" in k
            or "Head · Heart" in k
            or "Work. Hiring" in k
            or "Leaders & Teams" in k
            or "Hiring & Interviews" in k
            or "Relationships & Family" in k
            or "Understand People from the Inside" in k
            or "The 9 Personality" in k
            or "3 Intelligence" in k
            or "Real Motives" in k
            or "Interviews & Hiring" in k
            or "Work Relationships" in k
            or "Family Understanding" in k
            or "Stop Guessing" in k
            or "Beyond Labels" in k
            or "Applied, Not Passive" in k
            or "Work, Hiring" in k
            or "A Map You Can Use" in k
            or "Personality Map" in k
            or "Personality Types" in k
            or "Intelligence Centers" in k
            or "How You'll Learn" in k
            or "Not a Passive Lecture" in k
            or "Read People" in k
            or "Inside the Enneagram Experience" in k
            or "Ready to Understand People" in k
            or "Stop guessing with people" in k
            or "Explore photos from live Enneagram" in k
            or "Explore highlights from live Enneagram" in k
            or "Why do certain colleagues" in k
            or "Hire smarter" in k
            or "Build a well-rounded" in k
            or "Communicate better with your manager" in k
            or "Understand your partner and children" in k
            or "Discover why certain people drain" in k
            or "Understand why people behave" in k
            or "For managers and professionals" in k
            or "For anyone involved in hiring" in k
            or "For people who want deeper understanding with a partner" in k
            or "The 9 personality types, and how" in k
            or "Head, Heart, and Body" in k
            or "How to understand the real motive" in k
            or "Use the Enneagram in interviews" in k
            or "Deal with your manager" in k
            or "Build real understanding with your partner" in k
            or "This isn't typical personality" in k
            or "Training includes hands-on" in k
            or "Use the same map with colleagues" in k
            or "The 9 types and 3 intelligence" in k
            or "Workshops, role-play" in k
            or "Hiring, teams, and everyday" in k
            or "Understand motives from the first" in k
            or "Who Is This Program For?" in k
            or "What You'll Learn" in k
            or "By the End of the Program" in k
            or "Why This Program?" in k
            or "Proven Track Record" in k
            or "You'll Be Able To:" in k
            or k.startswith("Enneagram program photo ")
        )
    ]
    for k in level1_keys:
        old_dict.pop(k, None)

    old_dict.update(program_i18n)
    # photo alt pattern used dynamically
    old_dict["Enneagram Level 2 program photo "] = "صورة برنامج Enneagram المستوى 2 "

    dict_json = json.dumps(old_dict, ensure_ascii=False, separators=(",", ":"))
    html = re.sub(
        r"window\.ALA_I18N_DICT = \{.*?\};",
        "window.ALA_I18N_DICT = " + dict_json + ";",
        html,
        count=1,
        flags=re.S,
    )

    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes)")
    print(f"gallery images: {len(files)}")
    print(f"hero: {hero}")

    # Merge into ar.json
    ar = json.loads(AR_JSON.read_text(encoding="utf-8"))
    ar.update(program_i18n)
    ar["Enneagram Level 2 program photo "] = "صورة برنامج Enneagram المستوى 2 "
    AR_JSON.write_text(json.dumps(ar, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated ar.json")

    # Register in sync_detail_pages
    sync = ROOT / "_i18n" / "sync_detail_pages.py"
    sync_txt = sync.read_text(encoding="utf-8")
    if '"eneagram2.html"' not in sync_txt:
        sync_txt = sync_txt.replace(
            '    "eneagram1.html",\n)',
            '    "eneagram1.html",\n    "eneagram2.html",\n)',
            1,
        )
        sync.write_text(sync_txt, encoding="utf-8", newline="\n")
        print("registered eneagram2.html in sync_detail_pages.py")


if __name__ == "__main__":
    main()
