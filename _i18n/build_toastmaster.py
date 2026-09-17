# -*- coding: utf-8 -*-
"""Build toastmaster.html from eneagram2.html design shell + exact toastmaster.pdf content."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(r"d:\Projects\Ala Screens")
SRC = ROOT / "eneagram2.html"
OUT = ROOT / "toastmaster.html"
IMG_DIR = ROOT / "images" / "toastmaster"
AR_JSON = ROOT / "_i18n" / "ar.json"

# --- Exact English from Docs/toastmaster.pdf ---
EN_SUBTITLE = "Where Leaders Are Made"
EN_OPEN = (
    "In collaboration with Toastmasters International, one of the world’s leading "
    "organizations for communication and leadership development, ALA Academy is "
    "proud to host the ALA Toastmasters Club, a practical and supportive community "
    "designed for individuals who want to strengthen their public speaking, "
    "communication, leadership, and confidence."
)
EN_P1 = (
    "Founded in 1924, Toastmasters International has grown into a global community of "
    "more than 260,000 members across 13,800+ clubs worldwide. Its unique approach "
    "is built around learning by doing: members practice, participate, take on leadership "
    "roles, and receive constructive feedback in a supportive environment."
)
EN_P2 = (
    "Through the Toastmasters Pathways learning experience, members follow a flexible "
    "and structured development journey designed to strengthen skills across Public "
    "Speaking, Interpersonal Communication, Strategic Leadership, Management, and "
    "Confidence. Pathways combines practical projects, presentations, feedback, and "
    "real-life application to support continuous personal and professional growth."
)
EN_HAPPENS_HEAD = "What Happens at ALA Toastmasters Club?"
EN_HAPPENS_INTRO = (
    "ALA Toastmasters Club meetings are more than traditional training sessions. They "
    "are an interactive learning experience built around practice, participation, feedback, "
    "and continuous improvement."
)
EN_OPP_INTRO = "Members get the opportunity to:"
EN_BULLETS = [
    "Practice and deliver prepared speeches and presentations.",
    "Develop their impromptu speaking skills.",
    "Receive constructive feedback to accelerate their growth.",
    "Take on different roles and responsibilities during meetings.",
    "Develop leadership and teamwork skills.",
    "Progress through the Toastmasters Pathways learning experience.",
    "Build confidence and connect with a community of like-minded individuals.",
]
EN_GATHER_HEAD = "ALA Toastmasters Club Gatherings"
EN_GATHER_BODY = (
    "ALA Toastmasters Club meetings take place on the second and fourth Wednesday "
    "of every month at ALA Academy."
)
EN_SCHEDULE = "2nd and 4th Wednesday of each month"
EN_CTA = "Come practice, speak, learn, lead, and grow,one meeting at a time."

# --- Exact Arabic from toastmaster.pdf (orthography normalized) ---
AR_SUBTITLE = "حيث تُصنع القيادات"
AR_OPEN = (
    "نادي ALA Toastmasters حيث تُصنع القيادات بالتعاون مع منظمة توستماسترز العالمية "
    "(Toastmasters International)، إحدى أكبر وأشهر المنظمات العالمية المتخصصة في تطوير مهارات التواصل والقيادة، "
    "تقدم أكاديمية ALA نادي ALA Toastmasters؛ ليكون مجتمعًا عمليًا وداعمًا لكل من يرغب في تطوير قدراته في التحدث أمام الجمهور، "
    "والتواصل، والقيادة، وبناء الثقة بالنفس."
)
AR_P1 = (
    "تأسست منظمة توستماسترز العالمية عام 1924، وأصبحت اليوم مجتمعًا عالميًا يضم أكثر من 260,000 عضو وأكثر "
    "من 13,800 نادٍ حول العالم. وتعتمد تجربة توستماسترز على التعلم من خلال الممارسة والتجربة المستمرة، "
    "والمشاركة، والتقييم البنّاء، وتولي الأعضاء أدوارًا مختلفة تساعدهم على تطوير مهاراتهم الشخصية والمهنية والقيادية."
)
AR_P2 = (
    "ومن خلال نظام المسارات التعليمية، يخوض كل عضو رحلة تعلم مرنة ومتدرجة، تساعده على تطوير مجموعة متنوعة "
    "من المهارات، مثل التحدث أمام الجمهور، التواصل الفعّال، القيادة، الإدارة، والعمل الجماعي وبناء الثقة بالنفس، من "
    "خلال مشروعات وتطبيقات عملية يتم تنفيذها وممارستها داخل اجتماعات النادي."
)
AR_HAPPENS_HEAD = "ماذا يحدث في نادي ALA Toastmasters؟"
AR_HAPPENS_INTRO = (
    "اجتماعات النادي ليست مجرد محاضرات أو تدريبات تقليدية، وإنما هي تجربة تفاعلية قائمة على الممارسة، والمشاركة، "
    "والتقييم، والتطور المستمر."
)
AR_OPP_INTRO = "خلال الاجتماعات، يحصل الأعضاء على فرص لـ:"
AR_BULLETS = [
    "تقديم خطابات وعروض أمام الجمهور.",
    "التدريب على التحدث الارتجالي والتعبير عن الأفكار بسرعة ووضوح.",
    "الحصول على تقييم وملاحظات بنّاءة تساعدهم على التطور.",
    "ممارسة أدوار ومسؤوليات مختلفة داخل الاجتماع.",
    "تطوير مهارات القيادة والعمل الجماعي.",
    "متابعة تقدمهم من خلال نظام المسارات التعليمية.",
    "بناء الثقة بالنفس والتغلب على رهبة التحدث أمام الجمهور، والتواصل مع مجتمع من الأشخاص المهتمين بالتطور الشخصي والمهني.",
]
AR_GATHER_HEAD = "لقاءات نادي ALA Toastmasters"
AR_GATHER_BODY = (
    "تُعقد لقاءات ALA Toastmasters يومي الأربعاء الثاني والرابع من كل شهر في مقر أكاديمية ALA."
)
AR_SCHEDULE = "الأربعاء الثاني والرابع من كل شهر"
AR_TAGLINE = "ALA Toastmasters — مساحتك للتحدث، والتطور، والقيادة."
AR_CTA = "انضم إلينا، مارس، تكلّم، تعلّم، وقد نفسك نحو تواصل أكثر تأثيرًا وقيادة أكثر فاعلية."

META_EN = (
    "ALA Toastmasters Club — Where Leaders Are Made. Live club meetings on the "
    "2nd and 4th Wednesday of each month | Ahmed Latif Academy"
)
META_AR = (
    "نادي ALA Toastmasters حيث تُصنع القيادات. لقاءات مباشرة يومي الأربعاء الثاني والرابع من كل شهر | Ahmed Latif Academy"
)

WA_INTEREST_EN = (
    "Hello ALA, I'm interested in the ALA Toastmasters Club. Please share the next "
    "available meeting details and how to join."
)
WA_INTEREST_AR = (
    "مرحباً ALA، أنا مهتم/ة بنادي ALA Toastmasters. يرجى مشاركة تفاصيل أقرب اللقاءات وكيفية الانضمام."
)
WA_GENERIC = (
    "You're just one step away from joining ALA! Contact us today, and one of our team members will "
    "be happy to assist you with the next available course date, course fees, current offers, answer "
    "all your questions, and help you complete your registration with ease."
)


def gallery_files() -> list[str]:
    skip = {"chatgpt image sep 17, 2026, 11_45_05 am.png"}
    files = sorted(
        p.name
        for p in IMG_DIR.iterdir()
        if p.is_file()
        and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}
        and p.name.lower() not in skip
    )
    if not files:
        raise SystemExit(f"No images in {IMG_DIR}")
    return files


def hero_image(files: list[str]) -> str:
    for name in files:
        low = name.lower()
        if low.startswith("copy of") or low.startswith("img_"):
            return name
    return files[0]


def main() -> None:
    html = SRC.read_text(encoding="utf-8")
    files = gallery_files()
    hero = hero_image(files)
    hero_src = "images/toastmaster/" + quote(hero)

    html = re.sub(
        r"<title>.*?</title>",
        "<title>ALA Toastmasters Club | Ahmed Latif Academy</title>",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{META_EN}">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:title" content="[^"]*">',
        '<meta property="og:title" content="ALA Toastmasters Club | Ahmed Latif Academy">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{META_EN}">',
        html,
        count=1,
    )

    extra_css = """
    .gather-section {
      background: var(--program-warm);
      padding: 88px 0;
    }
    .gather-section .gather-stack {
      max-width: 760px;
      margin: 0 auto;
      text-align: center;
    }
    .gather-section .gather-stack p {
      font-size: 16px;
      line-height: 1.8;
      color: var(--muted-text);
    }
    html[dir="rtl"] .gather-section .gather-stack p {
      font-family: "Cairo", "Raleway", sans-serif;
    }
    .quick-facts-grid.facts-2 {
      grid-template-columns: repeat(2, minmax(0, 1fr));
      max-width: 720px;
      margin-inline: auto;
    }
"""
    if ".gather-section" not in html:
        html = html.replace("    /* Learning */", extra_css + "\n    /* Learning */", 1)

    learn_items = "\n".join(
        f'          <li class="anim-item"><i class="fa-solid fa-check" aria-hidden="true"></i><span>{b}</span></li>'
        for b in EN_BULLETS
    )

    main_content = f"""    <nav class="breadcrumb" aria-label="Breadcrumb">
      <div class="container">
        <ol class="breadcrumb-list">
          <li><a href="https://link.cashprocess.io/preview/LFFNtiNpdGcVJBl4zV8u" target="_top">Home</a></li>
          <li><a href="https://link.cashprocess.io/preview/fRaRY5RMY05VbnLSxGoO" target="_top">Programs</a></li>
          <li class="breadcrumb-current" aria-current="page">ALA Toastmasters Club</li>
        </ol>
      </div>
    </nav>

    <section class="program-hero" id="program-hero">
      <div class="container program-hero-grid">
        <div class="program-hero-content">
          <p class="eyebrow anim-item">Live Program</p>
          <h1 class="program-hero-title anim-item">
            <span class="line-dark">ALA Toastmasters Club</span>
            <span class="line-gold">{EN_SUBTITLE}</span>
          </h1>
          <p class="program-hero-desc anim-item">{EN_OPEN}</p>
          <div class="program-meta anim-item" aria-label="Program facts">
            <span class="program-meta-badge"><i class="fa-regular fa-circle-dot" aria-hidden="true"></i> Live Program</span>
            <span class="program-meta-badge"><i class="fa-regular fa-calendar" aria-hidden="true"></i> {EN_SCHEDULE}</span>
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
              alt="Members during an ALA Toastmasters Club meeting with Ahmed Latif Academy"
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
            <i class="fa-regular fa-calendar" aria-hidden="true"></i>
            <strong>{EN_SCHEDULE}</strong>
            <span>Course Duration</span>
          </div>
        </div>
      </div>
    </section>

    <section class="program-story" id="program-story">
      <div class="container">
        <div class="section-header">
          <p class="eyebrow anim-item">ALA Toastmasters Club</p>
          <h2 class="section-heading anim-item">{EN_SUBTITLE}</h2>
        </div>
        <div class="story-stack">
          <p class="anim-item">{EN_P1}</p>
          <p class="anim-item">{EN_P2}</p>
        </div>
      </div>
    </section>

    <section class="outcomes-section" id="learning">
      <div class="container">
        <div class="section-header">
          <h2 class="section-heading anim-item">{EN_HAPPENS_HEAD}</h2>
          <p class="section-intro anim-item" style="color: rgba(255,255,255,0.82); max-width: 720px;">{EN_HAPPENS_INTRO}</p>
          <p class="section-intro anim-item" style="color: rgba(255,255,255,0.82); margin-top: 12px;">{EN_OPP_INTRO}</p>
        </div>
        <ul class="outcomes-list">
{learn_items}
        </ul>
      </div>
    </section>

    <section class="gather-section" id="gatherings">
      <div class="container">
        <div class="section-header">
          <h2 class="section-heading anim-item">{EN_GATHER_HEAD}</h2>
        </div>
        <div class="gather-stack">
          <p class="anim-item">{EN_GATHER_BODY}</p>
        </div>
      </div>
    </section>

    <section class="program-gallery" id="program-gallery">
      <div class="container">
        <div class="section-header">
          <p class="eyebrow anim-item">Program Experience</p>
          <h2 class="section-heading anim-item">ALA Toastmasters Club</h2>
        </div>
        <div class="gallery-slider" id="galleryRoot" aria-roledescription="carousel" aria-label="ALA Toastmasters Club photo gallery"></div>
      </div>
    </section>

    <section class="program-cta" id="program-cta">
      <div class="container">
        <div class="program-cta-card anim-item">
          <h2>{EN_CTA}</h2>
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

    files_js = ",\n        ".join(f'"{f}"' for f in files)
    gallery_block = f"""      var galleryFolder = "images/toastmaster/";
      var galleryFiles = [
        {files_js}
      ];
      var galleryImages = galleryFiles.map(function (file, index) {{
        return {{
          src: galleryFolder + encodeURIComponent(file),
          alt: "ALA Toastmasters Club photo " + (index + 1)
        }};
      }});"""

    html = re.sub(
        r"      var galleryFolder = [\s\S]*?var galleryImages = galleryFiles\.map\(function \(file, index\) \{[\s\S]*?\}\);",
        gallery_block,
        html,
        count=1,
    )
    # eneagram2 may still use galleryImages = [ array ] form if replace failed — handle both
    if "images/toastmaster/" not in html:
        html = re.sub(
            r"      var galleryImages = \[[\s\S]*?\];",
            gallery_block,
            html,
            count=1,
        )

    program_i18n = {
        "ALA Toastmasters Club": "نادي ALA Toastmasters",
        "ALA Toastmasters Club | Ahmed Latif Academy": "نادي ALA Toastmasters | Ahmed Latif Academy",
        META_EN: META_AR,
        EN_SUBTITLE: AR_SUBTITLE,
        EN_OPEN: AR_OPEN,
        EN_P1: AR_P1,
        EN_P2: AR_P2,
        EN_HAPPENS_HEAD: AR_HAPPENS_HEAD,
        EN_HAPPENS_INTRO: AR_HAPPENS_INTRO,
        EN_OPP_INTRO: AR_OPP_INTRO,
        EN_GATHER_HEAD: AR_GATHER_HEAD,
        EN_GATHER_BODY: AR_GATHER_BODY,
        EN_SCHEDULE: AR_SCHEDULE,
        "Course Duration": "مدة البرنامج",
        EN_CTA: AR_CTA,
        "Members during an ALA Toastmasters Club meeting with Ahmed Latif Academy": (
            "أعضاء خلال لقاء نادي ALA Toastmasters مع Ahmed Latif Academy"
        ),
        "ALA Toastmasters Club photo gallery": "معرض صور نادي ALA Toastmasters",
        "ALA Toastmasters Club photo ": "صورة نادي ALA Toastmasters ",
        WA_INTEREST_EN: WA_INTEREST_AR,
        AR_TAGLINE: AR_TAGLINE,  # keep available if referenced
    }
    for en_b, ar_b in zip(EN_BULLETS, AR_BULLETS):
        program_i18n[en_b] = ar_b

    m = re.search(r"window\.ALA_I18N_DICT = (\{.*?\});", html, re.S)
    if not m:
        raise SystemExit("ALA_I18N_DICT not found")
    old_dict = json.loads(m.group(1))

    drop_frags = (
        "Level 2",
        "Enneagram",
        "Subtypes",
        "Ever felt like you finally",
        "The truth is, knowing someone's type",
        "Once you understand the basics",
        "At this level, you'll start",
        "The goal here isn't to label",
        "Once you reach Level 2",
        "What you see on the surface",
        "Book your seat in Level 2",
        "A Deeper Understanding",
        "Professional TOT",
        "Training of Trainers",
    )
    for k in list(old_dict):
        if any(frag in k for frag in drop_frags):
            old_dict.pop(k, None)

    old_dict.update(program_i18n)
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

    ar = json.loads(AR_JSON.read_text(encoding="utf-8"))
    ar.update(program_i18n)
    AR_JSON.write_text(json.dumps(ar, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("updated ar.json")

    sync = ROOT / "_i18n" / "sync_detail_pages.py"
    sync_txt = sync.read_text(encoding="utf-8")
    if '"toastmaster.html"' not in sync_txt:
        sync_txt = sync_txt.replace(
            '    "tot.html",\n',
            '    "tot.html",\n    "toastmaster.html",\n',
            1,
        )
        if '"toastmaster.html"' not in sync_txt:
            sync_txt = sync_txt.replace(
                '    "eneagram2.html",\n)',
                '    "eneagram2.html",\n    "toastmaster.html",\n)',
                1,
            )
        sync.write_text(sync_txt, encoding="utf-8", newline="\n")
        print("registered toastmaster.html")
    else:
        print("toastmaster.html already registered")


if __name__ == "__main__":
    main()
