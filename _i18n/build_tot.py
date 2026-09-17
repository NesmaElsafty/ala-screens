# -*- coding: utf-8 -*-
"""Rebuild tot.html from eneagram2.html design shell + exact tot.pdf content."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(r"d:\Projects\Ala Screens")
SRC = ROOT / "eneagram2.html"
OUT = ROOT / "tot.html"
IMG_DIR = ROOT / "images" / "tot"
AR_JSON = ROOT / "_i18n" / "ar.json"

# --- Exact English from tot.pdf ---
EN_TITLE = "Professional TOT - Training of Trainers"
EN_OPEN = (
    "Some people speak beautifully in casual conversation... but the moment they stand "
    "in front of a room of 50 or 100 people, what once felt effortless suddenly feels heavy, "
    "and the idea that was so clear in their head turns into scattered words in front of the crowd."
)
EN_P1 = (
    "Not everyone who can speak well is capable of being an impactful trainer. Many "
    "people have strong knowledge and real experience... but don't know how to deliver it "
    "professionally enough to make people understand, engage, and actually change."
)
EN_P2 = (
    "The truth is, training isn't just talking in front of an audience. It's science + skill + impact."
)
EN_P3 = (
    'Professional TOT is built to move you from "I know how to explain things" to '
    "becoming a professional Trainer capable of training, influencing, and creating real change."
)
EN_LEARN_HEAD = "What you'll learn:"
EN_BULLETS = [
    "Speaking with confidence in front of an audience, and controlling your tone of voice effectively",
    "Using pauses professionally, and understanding body language, gestures, and their impact",
    "Commanding the room and engaging with the audience, and understanding trainee personality types",
    "Managing discussions and creating effective spaces for participation, and handling awkward situations or hostile questions",
    "Advanced persuasion techniques, and breaking down psychological barriers in trainees",
    "Using humor professionally to increase engagement",
    "Improvisation at different levels, and controlling your thoughts while on stage",
    "Releasing nervous tension and turning it into positive energy",
    "Preparing and structuring a speech professionally, and designing training materials",
    "The art of theatrical delivery and storytelling",
    "Powerful opening and closing techniques, and reading audience engagement to address lost attention",
    "Building a professional presentation even under time pressure (3 minutes), and using color theory within presentations",
]
EN_OUTCOMES_HEAD = "By the end of the program, you'll be able to:"
EN_OUTCOMES = [
    "Stand confidently in front of any audience",
    "Design and deliver a complete training program from scratch",
    "Genuinely influence trainees and create real change in them",
    "Build a strong presence as a professional Trainer",
]
EN_TRANSFORM = (
    "And this isn't just skill development. It's a complete transformation in your "
    "personality, your presence, and the way you communicate."
)
EN_WHY_HEAD = "Why is this program different?"
EN_WHY = (
    'Because you won\'t just learn "how to train"... you\'ll learn how to design a complete '
    "training program, command a room professionally, genuinely influence people, "
    "and build your name as a Trainer in the market. The program is built on a blend of "
    "world-class training methodologies, psychology, and intensive hands-on application."
)
EN_AFTER_HEAD = "After the course, we don't leave you on your own:"
EN_AFTER = [
    "A TOT Community for continuous skill practice",
    "Hands-on training opportunities before major events, in front of real audiences",
    "A supportive community that helps you grow and advance in the training field",
]
EN_LEADER_HEAD = "Program led by: Dr. Ahmed Latif"
EN_BIO = (
    "An internationally ICF-certified coach with over 17 years of experience in training "
    "and consulting, having trained over 600,000 people in Egypt and abroad, across "
    "more than 50 different nationalities. He has delivered this Professional TOT "
    "program to over 100 batches, and is the Founder and CEO of ALA Academy. He "
    "holds a PCC certification with over 5,000 coaching hours, a diploma in Positive "
    "Psychology, and internationally certified TOT credentials. He has trained across "
    "more than 56 faculties in 18 universities, and has worked with universities, major "
    "corporations, government and private entities, and leading companies such as "
    "Vodafone and BMW (Ezz El Arab)."
)
EN_DURATION = "Duration: 32 training hours"
EN_GALLERY = "Watch photos and videos from past batches and see the difference for yourself."
EN_CTA_HEAD = "Start your journey as a professional trainer."
EN_CTA_BODY = "Book your seat now."

# --- Exact Arabic from tot.pdf (orthography normalized from presentation forms) ---
AR_TITLE = "Professional TOT - Training of Trainers"
AR_OPEN = (
    "فيه ناس بتتكلم كويس أوي في جلسة عادية... وساعة ما تقف قدام قاعة فيها 50 أو 100 حد، تحس إن الكلام اللي كان "
    "سهل بقى ثقيل، والفكرة اللي كانت واضحة في دماغهم بقت مبعثرة قدام الجمهور."
)
AR_P1 = (
    "مش كل حد بيعرف يتكلم كويس يقدر يكون Trainer مؤثر. كتير من الناس عندهم معرفة قوية وخبرة كبيرة... لكن "
    "مش عارفين ينقلوها بشكل احترافي يخلي الناس تفهم، تتفاعل، وتتغير فعلاً."
)
AR_P2 = "الحقيقة إن التدريب مش مجرد كلام قدام جمهور... هو علم + مهارة + تأثير."
AR_P3 = (
    'Professional TOT معمول عشان ينقلك من مرحلة "بعرف أشرح" لمستوى Trainer محترف قادر يدرّب، يؤثر، ويصنع تغيير حقيقي.'
)
AR_LEARN_HEAD = "هتتعلم فيه:"
AR_BULLETS = [
    "التحدث بثقة أمام الجمهور، والتحكم في نبرة الصوت واستخدامها بفعالية",
    "استخدام الوقفات (Pauses) بشكل احترافي، ولغة الجسد وإيماءاته وتأثيرها",
    "السيطرة على القاعة والتفاعل مع الجمهور، وفهم أنماط المتدربين والتعامل مع كل شخصية",
    "إدارة النقاش وفتح مساحات مشاركة فعالة، والتعامل مع المواقف المحرجة والأسئلة الصعبة أو العدائية",
    "تقنيات الإقناع المتقدمة، وإزالة العوائق النفسية لدى المتدربين",
    "استخدام الـ Humor بشكل احترافي لزيادة التفاعل",
    "الارتجال بمستوياته المختلفة، والتحكم في الأفكار أثناء التواجد على الـ Stage",
    "التخلص من التوتر وتحويله لطاقة إيجابية",
    "إعداد وتجهيز الـ Speech بطريقة احترافية، وتصميم الحقائب التدريبية (Training Materials)",
    "فن الإلقاء المسرحي وسرد القصص (Storytelling)",
    "أساليب افتتاح وختام الجلسات بشكل قوي، وقراءة تفاعل الجمهور ومعالجة فقدان الانتباه",
    "إعداد Presentation احترافي حتى في وقت قصير (3 دقائق)، واستخدام الألوان وتقنياتها داخل العروض",
]
AR_OUTCOMES_HEAD = "بنهاية البرنامج هتكون قادر على:"
AR_OUTCOMES = [
    "الوقوف بثقة أمام أي جمهور",
    "تصميم وتقديم برنامج تدريبي كامل من الصفر",
    "التأثير في المتدربين وإحداث تغيير فعلي فيهم",
    "بناء حضور قوي كـ Trainer محترف",
]
AR_TRANSFORM = "وده مش بس تطوير مهارة... ده تحوّل كامل في شخصيتك، حضورك، وطريقة تواصلك."
AR_WHY_HEAD = "ليه البرنامج ده مختلف؟"
AR_WHY = (
    'لأنك مش بس هتتعلم "إزاي تدرب"... هتتعلم إزاي تصمم تدريب كامل، تدير قاعة باحتراف، تأثر في الناس فعلياً، '
    "وتبني اسمك كـ Trainer في السوق. البرنامج مبني على مزيج من مدارس تدريب عالمية، علم النفس، والتطبيق العملي المكثف."
)
AR_AFTER_HEAD = "وبعد الكورس، مش هنسيبك لوحدك:"
AR_AFTER = [
    "TOT Community لممارسة المهارات باستمرار",
    "فرص تدريب عملي قبل الأحداث المهمة أمام جمهور حقيقي",
    "مجتمع داعم يساعدك تكمل وتكبر في مجال التدريب",
]
AR_LEADER_HEAD = "مقدم البرنامج: د. أحمد لطيف"
AR_BIO = (
    "كوتش دولي معتمد من ICF، بخبرة أكتر من 17 سنة في التدريب والاستشارات، ودرّب أكتر من 600,000 شخص "
    "داخل مصر وخارجها من أكتر من 50 جنسية مختلفة. قدّم برنامج Professional TOT ده لأكتر من 100 دفعة، "
    "وهو المؤسس والمدير التنفيذي لأكاديمية ALA. حاصل على PCC بأكتر من 6000 ساعة كوتشينج، دبلوم علم النفس "
    "الإيجابي، و TOT معتمد من جهات دولية. درّب في أكتر من 56 كلية في 18 جامعة، وعمل مع جامعات، شركات "
    "كبرى، وهيئات حكومية وخاصة، وكبرى الشركات زي Vodafone و BMW (عز العرب)."
)
AR_DURATION = "مدة البرنامج: 32 ساعة تدريبية"
AR_GALLERY = "اتفرج على صور وفيديوهات الدفعات اللي فاتت وشوف بنفسك الفرق اللي حصل معاهم."
AR_CTA_HEAD = "أبدأ رحلتك كمدرب محترف."
AR_CTA_BODY = "احجز مكانك دلوقتي."

META_EN = (
    "Professional TOT - Training of Trainers — Live, 32 Hours | Ahmed Latif Academy"
)
META_AR = (
    "Professional TOT - Training of Trainers — مباشر، 32 ساعة | Ahmed Latif Academy"
)

WA_INTEREST_EN = (
    "Hello ALA, I'm interested in the Professional TOT - Training of Trainers program. "
    "Please share the next available dates, fees, and current offers."
)
WA_INTEREST_AR = (
    "مرحباً ALA، أنا مهتم/ة ببرنامج Professional TOT - Training of Trainers. "
    "يرجى مشاركة أقرب المواعيد المتاحة والرسوم والعروض الحالية."
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
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}
    )
    if not files:
        raise SystemExit(f"No images in {IMG_DIR}")
    return files


def hero_image(files: list[str]) -> str:
    return files[0]


def main() -> None:
    html = SRC.read_text(encoding="utf-8")
    files = gallery_files()
    hero = hero_image(files)
    hero_src = "images/tot/" + quote(hero)

    # Meta
    html = re.sub(
        r"<title>.*?</title>",
        "<title>Professional TOT - Training of Trainers | Ahmed Latif Academy</title>",
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
        '<meta property="og:title" content="Professional TOT - Training of Trainers | Ahmed Latif Academy">',
        html,
        count=1,
    )
    html = re.sub(
        r'<meta property="og:description" content="[^"]*">',
        f'<meta property="og:description" content="{META_EN}">',
        html,
        count=1,
    )

    # Extra CSS for after-course + leader sections
    extra_css = """
    .after-section {
      background: var(--program-warm);
      padding: 88px 0;
    }
    .after-section .section-header {
      text-align: left;
      margin-bottom: 28px;
    }
    html[dir="rtl"] .after-section .section-header {
      text-align: right;
    }
    .leader-section {
      background: var(--white);
      padding: 88px 0;
    }
    .leader-card {
      max-width: 820px;
      margin: 0 auto;
      border: 1px solid #EFEDE8;
      border-radius: 10px;
      padding: 28px 26px;
      background: var(--program-warm);
    }
    .leader-card h2 {
      font-size: clamp(22px, 2.6vw, 30px);
      margin-bottom: 14px;
      color: var(--charcoal);
    }
    .leader-card p {
      font-size: 15px;
      line-height: 1.8;
      color: var(--muted-text);
    }
    html[dir="rtl"] .leader-card,
    html[dir="rtl"] .leader-card p {
      font-family: "Cairo", "Raleway", sans-serif;
    }
    .duration-note {
      text-align: center;
      margin-top: 28px;
      font-size: 15px;
      color: var(--muted-text);
      font-weight: 600;
    }
"""
    if ".after-section" not in html:
        html = html.replace("    /* Learning */", extra_css + "\n    /* Learning */", 1)

    learn_items = "\n".join(
        f'          <li class="anim-item"><i class="fa-solid fa-check" aria-hidden="true"></i><span>{b}</span></li>'
        for b in EN_BULLETS
    )
    outcome_items = "\n".join(
        f'          <li class="anim-item"><i class="fa-solid fa-check" aria-hidden="true"></i><span>{b}</span></li>'
        for b in EN_OUTCOMES
    )
    after_items = "\n".join(
        f'          <li class="anim-item"><i class="fa-solid fa-check" aria-hidden="true"></i><span>{b}</span></li>'
        for b in EN_AFTER
    )

    main_content = f"""    <nav class="breadcrumb" aria-label="Breadcrumb">
      <div class="container">
        <ol class="breadcrumb-list">
          <li><a href="https://link.cashprocess.io/preview/LFFNtiNpdGcVJBl4zV8u" target="_top">Home</a></li>
          <li><a href="https://link.cashprocess.io/preview/fRaRY5RMY05VbnLSxGoO" target="_top">Programs</a></li>
          <li class="breadcrumb-current" aria-current="page">Professional TOT - Training of Trainers</li>
        </ol>
      </div>
    </nav>

    <section class="program-hero" id="program-hero">
      <div class="container program-hero-grid">
        <div class="program-hero-content">
          <p class="eyebrow anim-item">Live Program</p>
          <h1 class="program-hero-title anim-item">
            <span class="line-dark">Professional TOT</span>
            <span class="line-gold">Training of Trainers</span>
          </h1>
          <p class="program-hero-desc anim-item">{EN_OPEN}</p>
          <div class="program-meta anim-item" aria-label="Program facts">
            <span class="program-meta-badge"><i class="fa-regular fa-circle-dot" aria-hidden="true"></i> Live Program</span>
            <span class="program-meta-badge"><i class="fa-regular fa-clock" aria-hidden="true"></i> 32 Hours</span>
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
              alt="Participants during a live Professional TOT training with Ahmed Latif Academy"
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
            <strong>32 Hours</strong>
            <span>Training</span>
          </div>
        </div>
        <p class="duration-note anim-item">{EN_DURATION}</p>
      </div>
    </section>

    <section class="program-story" id="program-story">
      <div class="container">
        <div class="section-header">
          <p class="eyebrow anim-item">Professional ToT</p>
          <h2 class="section-heading anim-item">{EN_TITLE}</h2>
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
{learn_items}
        </ul>
      </div>
    </section>

    <section class="goal-section" id="outcomes">
      <div class="container">
        <div class="section-header">
          <h2 class="section-heading anim-item">{EN_OUTCOMES_HEAD}</h2>
        </div>
        <ul class="outcomes-list" style="color: inherit;">
{outcome_items}
        </ul>
        <div class="goal-stack" style="margin-top: 36px;">
          <p class="anim-item">{EN_TRANSFORM}</p>
        </div>
      </div>
    </section>

    <section class="program-story" id="why-program">
      <div class="container">
        <div class="section-header">
          <h2 class="section-heading anim-item">{EN_WHY_HEAD}</h2>
        </div>
        <div class="story-stack">
          <p class="anim-item">{EN_WHY}</p>
        </div>
      </div>
    </section>

    <section class="after-section" id="after-course">
      <div class="container">
        <div class="section-header">
          <h2 class="section-heading anim-item">{EN_AFTER_HEAD}</h2>
        </div>
        <ul class="outcomes-list" style="grid-template-columns: 1fr; max-width: 760px;">
{after_items}
        </ul>
      </div>
    </section>

    <section class="leader-section" id="program-leader">
      <div class="container">
        <article class="leader-card anim-item">
          <h2>{EN_LEADER_HEAD}</h2>
          <p>{EN_BIO}</p>
        </article>
      </div>
    </section>

    <section class="program-gallery" id="program-gallery">
      <div class="container">
        <div class="section-header">
          <p class="eyebrow anim-item">Program Experience</p>
          <h2 class="section-heading anim-item">{EN_GALLERY}</h2>
        </div>
        <div class="gallery-slider" id="galleryRoot" aria-roledescription="carousel" aria-label="Professional TOT program photo gallery"></div>
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

    # Fix outcomes list colors on light goal section
    if ".goal-section .outcomes-list" not in html:
        html = html.replace(
            "    .goal-section .section-heading {\n      max-width: 820px;\n    }",
            """    .goal-section .section-heading {
      max-width: 820px;
    }
    .goal-section .outcomes-list li,
    .after-section .outcomes-list li {
      color: var(--charcoal);
    }
    .goal-section .outcomes-list i,
    .after-section .outcomes-list i {
      color: var(--gold);
    }""",
            1,
        )

    files_js = ",\n        ".join(f'"{f}"' for f in files)
    gallery_block = f"""      var galleryFolder = "images/tot/";
      var galleryFiles = [
        {files_js}
      ];
      var galleryImages = galleryFiles.map(function (file, index) {{
        return {{
          src: galleryFolder + encodeURIComponent(file),
          alt: "Professional TOT program photo " + (index + 1)
        }};
      }});"""

    html = re.sub(
        r"      var galleryFolder = [\s\S]*?var galleryImages = galleryFiles\.map\(function \(file, index\) \{[\s\S]*?\}\);",
        gallery_block,
        html,
        count=1,
    )

    program_i18n = {
        "Professional TOT - Training of Trainers": AR_TITLE,
        "Professional TOT - Training of Trainers | Ahmed Latif Academy": (
            "Professional TOT - Training of Trainers | Ahmed Latif Academy"
        ),
        META_EN: META_AR,
        "Professional TOT": "Professional TOT",
        "Training of Trainers": "Training of Trainers",
        "Professional ToT": "Professional ToT",
        EN_OPEN: AR_OPEN,
        EN_P1: AR_P1,
        EN_P2: AR_P2,
        EN_P3: AR_P3,
        EN_LEARN_HEAD: AR_LEARN_HEAD,
        EN_OUTCOMES_HEAD: AR_OUTCOMES_HEAD,
        EN_TRANSFORM: AR_TRANSFORM,
        EN_WHY_HEAD: AR_WHY_HEAD,
        EN_WHY: AR_WHY,
        EN_AFTER_HEAD: AR_AFTER_HEAD,
        EN_LEADER_HEAD: AR_LEADER_HEAD,
        EN_BIO: AR_BIO,
        EN_DURATION: AR_DURATION,
        EN_GALLERY: AR_GALLERY,
        EN_CTA_HEAD: AR_CTA_HEAD,
        EN_CTA_BODY: AR_CTA_BODY,
        "32 Hours": "32 ساعة",
        "Participants during a live Professional TOT training with Ahmed Latif Academy": (
            "مشاركون خلال تدريب Professional TOT مباشر مع Ahmed Latif Academy"
        ),
        "Professional TOT program photo gallery": "معرض صور برنامج Professional TOT",
        "Professional TOT program photo ": "صورة برنامج Professional TOT ",
        WA_INTEREST_EN: WA_INTEREST_AR,
    }
    for en_b, ar_b in zip(EN_BULLETS, AR_BULLETS):
        program_i18n[en_b] = ar_b
    for en_b, ar_b in zip(EN_OUTCOMES, AR_OUTCOMES):
        program_i18n[en_b] = ar_b
    for en_b, ar_b in zip(EN_AFTER, AR_AFTER):
        program_i18n[en_b] = ar_b

    m = re.search(r"window\.ALA_I18N_DICT = (\{.*?\});", html, re.S)
    if not m:
        raise SystemExit("ALA_I18N_DICT not found")
    old_dict = json.loads(m.group(1))

    # Drop Enneagram-2-specific keys
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
    if '"tot.html"' not in sync_txt:
        sync_txt = sync_txt.replace(
            '    "pg.html",\n',
            '    "pg.html",\n    "tot.html",\n',
            1,
        )
        sync.write_text(sync_txt, encoding="utf-8", newline="\n")
        print("registered tot.html")
    else:
        print("tot.html already in sync list")


if __name__ == "__main__":
    main()
