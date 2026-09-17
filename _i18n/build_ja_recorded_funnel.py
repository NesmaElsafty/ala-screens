# -*- coding: utf-8 -*-
"""Rebuild ja-recorded-funnel.html with EN translations + responsive fixes."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"D:/Projects/Ala Screens")
SRC = ROOT / "ps-recorded-funnel.html"
OUT = ROOT / "ja-recorded-funnel.html"

# --- Arabic (source) + English (translated from Arabic) ---
COURSE_NAME = ("رحلة وعي", "Journey of Awareness")
COURSE_TAGLINE = (
    "من اللي شكّل تفكيرك... للي تختار إنت تبقاه",
    "From what shaped your thinking... to who you choose to become",
)

SHORT = (
    'فيه ناس بتعيش حياتها كلها بأفكار وقناعات مش هي اللي اختارتها .. أفكار اتحطت جواها من غير ما تاخد إذنها: خوف مش عارفة مصدره، إحساس بالفشل مش مبني على حقيقة، حدود حطتها العادات والتقاليد من غير ما تسأل ليه. رحلة وعي مش كورس هيديك "نصايح تحفيزية" وينتهي. ده رحلة حقيقية بحلقات متتالية، هتاخدك خطوة بخطوة جوه عقلك ووعيك، تفهم فيها إزاي اتشكّلت، وتاخد بعدها قرار واعٍ تكمل بيه حياتك — مش بردود أفعال قديمة بقت "عادي" لمجرد إنك متعود عليها.',
    'Some people live their whole lives with thoughts and beliefs they never chose — ideas placed inside them without permission: a fear they can\'t trace, a sense of failure with no real basis, limits set by habits and traditions without ever asking why. Journey of Awareness isn\'t a course that gives you "motivational tips" and ends there. It\'s a real journey through successive episodes that takes you step by step into your mind and awareness, so you understand how you were shaped — then make a conscious decision to continue your life, not through old reactions that only feel "normal" because you got used to them.',
)

PROMISE = (
    "إنت مش هتتغير من بره... هتوعى للي بيحصل جواك، وبعدين تختار إنت مين تبقى.",
    "You won't change from the outside... you'll become aware of what's happening inside you, then choose who you become.",
)

TRANSFORMS = [
    (
        ('من "بعيش بردود فعل مش فاهم مصدرها"', 'From "I live by reactions I don\'t understand"'),
        ('لـ "بفهم عقلي وبقدر أوجهه إزاي أنا عايز."', 'To "I understand my mind and can direct it the way I want."'),
    ),
    (
        ('من "بخاف من أشياء مش عارف ليه"', 'From "I fear things without knowing why"'),
        ('لـ "بقدر أفهم مصدر الخوف وأتعامل معاه."', 'To "I can understand the source of fear and deal with it."'),
    ),
    (
        ('من "أنا فاشل / مش قادر"', 'From "I\'m a failure / I can\'t"'),
        ('لـ "أنا المسؤول عن حياتي، وقادر أغيّرها."', 'To "I\'m responsible for my life, and I can change it."'),
    ),
    (
        ('من "بعيش حياة على مقاس اللي حواليّا"', 'From "I live a life sized to everyone around me"'),
        ('لـ "مستقبلي أنا اللي بحدده، مش العادات والتقاليد."', 'To "I decide my future — not habits and traditions."'),
    ),
]

AUDIENCE = [
    (
        "أي حد حاسس إنه بيعيش بردود أفعال قديمة مش فاهم مصدرها، وعايز يفهم نفسه أكتر.",
        "Anyone who feels they're living by old reactions they don't understand, and wants to understand themselves more.",
    ),
    (
        "أي حد بيصارع قلق وهموم مستمرة ومحتاج يفهم إزاي عقله بيشتغل عشان يتعامل معاها صح.",
        "Anyone struggling with ongoing anxiety and worries who needs to understand how their mind works to handle them properly.",
    ),
    (
        "أي حد عنده إحساس بالفشل أو عدم الكفاية مش مبني على حقيقة، وعايز يكسره.",
        "Anyone carrying a sense of failure or inadequacy that isn't based on reality, and wants to break it.",
    ),
    (
        "أي حد بيحس إن حياته أصغر من طموحه، وعايز يفهم إيه اللي واقف بينه وبين اللي هو عايزه.",
        "Anyone who feels their life is smaller than their ambition, and wants to understand what's standing between them and what they want.",
    ),
    (
        "أي حد عايز يفهم قانون الجذب بشكل علمي وعملي، مش شعارات بس.",
        "Anyone who wants to understand the Law of Attraction in a scientific and practical way — not just slogans.",
    ),
    (
        "أي حد تعب من إنه بيعيش قرارات مبنية على خجل، خوف، أو قناعات مش بتاعته أصلاً.",
        "Anyone tired of living by decisions built on shame, fear, or beliefs that were never really theirs.",
    ),
]

PROBLEMS = [
    ("بعيش بأفكار وقناعات مش فاهم منين جت.", "I live with thoughts and beliefs I don't know where they came from."),
    ("مش عارف أتعامل مع همومي، فبتراكم وتأثر على حياتي كلها.", "I don't know how to deal with my worries, so they pile up and affect my whole life."),
    ("عندي خوف من أشياء وأحداث معينة مش عارف مصدره الحقيقي.", "I have fear of certain things and events, and I don't know its real source."),
    ("آخر تجربة سيئة لسه بتأثر على قراراتي دلوقتي من غير ما أحس.", "My last bad experience still affects my decisions now without me realizing it."),
    ("حاسس إني فاشل أو مش كفاية، حتى لو مفيش سبب حقيقي.", "I feel like a failure or not enough, even when there's no real reason."),
    ("بحمّل الظروف أو الناس مسؤولية حياتي، بدل ما أمسك زمامها.", "I blame circumstances or other people for my life instead of taking ownership of it."),
    ("بتصرف حسب عادات وتقاليد اتربيت عليها، من غير ما أسأل نفسي هل دي فعلاً قناعتي.", "I act according to habits and traditions I was raised with, without asking myself if these are really my beliefs."),
    ("الخجل بيوقفني عن حاجات كتير كنت أقدر أعملها.", "Shame stops me from doing many things I could have done."),
    ("بحس إن مستقبلي أصغر من طموحي، ومش عارف إزاي أوسّعه.", "I feel my future is smaller than my ambition, and I don't know how to expand it."),
]

FEATURES = [
    ("حلقات مرتبة في رحلة متكاملة، مش معلومات متفرقة.", "Episodes arranged as one complete journey — not scattered information."),
    ("يجمع بين الفهم النفسي العميق و التطبيق العملي لقوانين زي قانون الجذب.", "It combines deep psychological understanding with practical application of principles like the Law of Attraction."),
    ("كل حلقة بتاخدك خطوة أعمق في فهم نفسك، مش بس معلومة تسمعها وتنساها.", "Every episode takes you one step deeper into understanding yourself — not just information you hear and forget."),
    ("مناسب لأي حد يبدأ رحلته من الصفر، حتى لو أول مرة يتعرض لمفاهيم زي الوعي والقناعات.", "Suitable for anyone starting from zero — even if it's their first time with concepts like awareness and beliefs."),
    ("محتوى مسجّل .. تتفرج عليه في ترتيبه الطبيعي، وترجع لأي حلقة وقت ما تحتاجها.", "Recorded content… watch it in its natural order, and return to any episode whenever you need it."),
]

CURRICULUM = (
    'الكورس مبني على رحلة متكاملة من الحلقات، تبدأ بفهم إزاي عقلك بيشتغل والوعي بمصادر خوفك وقلقك، وتاخدك بعدين لكسر القناعات المحدودة زي "أنا فاشل" أو "مسؤولية حياتي على حد تاني"، وتوريك إزاي تقرأ أحداث حياتك وتطبق قانون الجذب بشكل علمي، لحد ما توصل لمرحلة التحرر من الأحكام والخجل، وأخيرًا بناء مستقبل أكبر بقرارات واعية إنت اللي اخترتها.',
    'The course is built as a complete journey of episodes. It starts with understanding how your mind works and becoming aware of the sources of your fear and anxiety, then takes you into breaking limiting beliefs like "I\'m a failure" or "someone else is responsible for my life," shows you how to read the events of your life and apply the Law of Attraction scientifically, until you reach freedom from judgments and shame — and finally build a bigger future through conscious decisions you chose yourself.',
)

FAQS = [
    (
        ("الكورس ده نظري ولا فيه تطبيق عملي؟", "Is this course theoretical, or does it include practical application?"),
        ("الكورس بيجمع بين الفهم العميق لعقلك وقناعاتك، وبين تطبيقات عملية زي قانون الجذب، عشان الوعي ده يتحول لتغيير حقيقي في حياتك، مش معلومة تسمعها وتنساها.", "The course combines a deep understanding of your mind and beliefs with practical applications like the Law of Attraction, so that awareness turns into real change in your life — not information you hear and forget."),
    ),
    (
        ("لازم أبدأ من الحلقة الأولى ولا ممكن أدخل من أي مكان؟", "Do I have to start from the first episode, or can I jump in anywhere?"),
        ("الأفضل تبدأ بالترتيب، لأن كل حلقة بتبني على اللي قبلها — من فهم عقلك، لكسر القناعات المحدودة، لحد بناء مستقبلك بوعي.", "It's best to start in order, because every episode builds on the one before it — from understanding your mind, to breaking limiting beliefs, to building your future with awareness."),
    ),
    (
        ('الكورس ده مناسب لو أول مرة أسمع عن حاجات زي "الوعي" أو "قانون الجذب"؟', 'Is this course suitable if it\'s my first time hearing about things like "awareness" or the "Law of Attraction"?'),
        ("أكيد، الكورس مبني يبدأ معاك من الصفر، وبيشرح كل مفهوم بشكل مبسط قبل ما يتعمق فيه.", "Absolutely. The course is built to start with you from zero, and explains every concept simply before going deeper."),
    ),
    (
        ("الكورس ده لايف يعني هستنى معاد كل حلقة؟", "Is this course live — meaning I have to wait for each episode's schedule?"),
        ("لا.. الكورس مسجل عشان تقدر تسمعه فى أى وقت يناسبك", "No… the course is recorded so you can watch it whenever it suits you."),
    ),
    (
        ("طرق الدفع المتاحة إيه؟", "What payment methods are available?"),
        ("لينك الدفع", "Payment link"),
    ),
]

CTA_P1 = (
    "إنت مش عايز تتغير من بره... إنت عايز تفهم إيه اللي شكّلك من جواك، وبعدين تختار إنت مين تبقى.",
    "You don't want to change from the outside... you want to understand what shaped you from within, then choose who you become.",
)
CTA_P2 = (
    "رحلة وعي مش هتديك نصايح تسمعها وتنساها، هتاخدك في رحلة حقيقية جوه عقلك، لحد ما توصل لنسخة منك بتاخد قراراتها بوعي، مش برد فعل قديم اتعودت عليه.",
    "Journey of Awareness won't give you tips you hear and forget. It will take you on a real journey inside your mind, until you reach a version of yourself that makes decisions with awareness — not an old reaction you've gotten used to.",
)
CTA_BTN = (
    "احجز مكانك في رحلة وعي الآن — 5000 جنيه بدل 9800",
    "Book your seat in Journey of Awareness now — 5000 EGP instead of 9800",
)
CTA_BTN_SHORT = (
    "من قناعات مش بتاعتك... لحياة إنت اخترتها.. 5000 بدل 9800",
    "From beliefs that aren't yours... to a life you chose.. 5000 instead of 9800",
)
CTA_POPUP = (
    "احجز مكانك الآن فى رحلة وعي",
    "Book your seat now in Journey of Awareness",
)
PRICE_SAVE = (
    "خصم يوفرلك 4800 جنيه — العرض متاح لفترة محدودة",
    "A discount that saves you 4800 EGP — offer available for a limited time",
)
PRICE_BADGE = (
    "5000 جنيه بدل 9800",
    "5000 EGP instead of 9800",
)

RESPONSIVE_CSS = """
    /* =========================================================
       JA FUNNEL — RESPONSIVE HARDENING
       ========================================================= */

    #ala-page {
      max-width: 100%;
    }

    .ala-hero-description,
    .ala-learning-text,
    .ala-before-text,
    .ala-after-text,
    .ala-audience-text,
    .ala-pain-text,
    .ala-feature-title,
    .ala-faq-answer,
    .ala-price-save {
      overflow-wrap: anywhere;
      word-break: break-word;
    }

    .ala-hero-badges {
      flex-wrap: wrap;
    }

    .ala-hero-badge {
      max-width: 100%;
      white-space: normal;
      text-align: center;
      line-height: 1.35;
    }

    .ala-learning-item[style*="grid-column"] {
      align-items: flex-start;
    }

    .ala-learning-item[style*="grid-column"] .ala-learning-text {
      max-width: 100%;
    }

    #ala-final-cta .ala-price-card,
    #ala-final-cta .ala-price-main {
      width: 100%;
      max-width: 100%;
    }

    #ala-final-cta .ala-btn {
      max-width: 100%;
      white-space: normal;
      height: auto;
      min-height: 48px;
      padding: 12px 18px;
      line-height: 1.45;
    }

    .ala-price-cta {
      white-space: normal !important;
      height: auto !important;
      min-height: 48px;
      line-height: 1.45;
      text-align: center;
    }

    @media (max-width: 980px) {
      .ala-hero-description {
        font-size: 15px;
        line-height: 1.75;
      }

      .ala-transform-item {
        align-items: stretch;
      }

      .ala-features-grid {
        grid-template-columns: 1fr;
      }

      .ala-feature-title {
        font-size: 16px;
        line-height: 1.55;
      }
    }

    @media (max-width: 760px) {
      .ala-hero-title {
        font-size: clamp(26px, 7vw, 40px) !important;
        line-height: 1.25 !important;
      }

      .ala-hero-description {
        font-size: 14px;
        line-height: 1.7;
      }

      .ala-hero-actions {
        width: 100%;
      }

      .ala-hero-actions .ala-btn {
        width: 100%;
        justify-content: center;
      }

      .ala-pain-grid {
        grid-template-columns: 1fr !important;
      }

      .ala-transform-before,
      .ala-after-box {
        width: 100%;
      }

      .ala-price-card {
        flex-direction: column;
      }

      .ala-price-main,
      .ala-price-details {
        width: 100%;
        max-width: 100%;
      }

      .ala-footer-inner {
        flex-direction: column;
        text-align: center;
      }
    }

    @media (max-width: 560px) {
      .ala-course-name {
        font-size: 14px;
      }

      .ala-section-title {
        font-size: clamp(24px, 7vw, 34px) !important;
        line-height: 1.3 !important;
      }

      .ala-hero-badge {
        font-size: 11px;
        padding: 8px 10px;
      }

      .ala-audience-item {
        align-items: flex-start;
      }

      .ala-audience-text,
      .ala-pain-text,
      .ala-learning-text {
        font-size: 14px;
        line-height: 1.65;
      }

      .ala-transform-item {
        grid-template-columns: 1fr !important;
      }

      .ala-transform-arrow-wrap {
        transform: rotate(90deg);
        margin: 4px 0;
      }

      #ala-final-cta .ala-section-title {
        font-size: clamp(22px, 6.5vw, 30px) !important;
      }
    }

    @media (max-width: 380px) {
      .ala-container {
        width: calc(100% - 20px);
      }

      .ala-header .ala-header-cta {
        padding: 8px 8px;
        font-size: 9px;
      }
    }
"""


def span(ar: str, en: str) -> str:
    return f"""            <span class="ala-ar">
              {ar}
            </span>

            <span
              class="ala-en"
              hidden
            >
              {en}
            </span>"""


def dual(ar: str, en: str) -> str:
    return span(ar, en)


def pain_cards(items):
    parts = []
    for i, (ar, en) in enumerate(items, 1):
        delay = "" if i % 4 == 1 else f'\n            style="--ala-delay:{(i % 4) * 60}ms;"'
        parts.append(
            f"""          <article class="ala-pain-card ala-reveal"{delay}>
            <div class="ala-pain-number">{i:02d}</div>
            <p class="ala-pain-text">
{span(ar, en)}
            </p>
          </article>"""
        )
    return "\n".join(parts)


def audience_items(items):
    parts = []
    for i, (ar, en) in enumerate(items, 1):
        parts.append(
            f"""            <div class="ala-audience-item ala-reveal">
              <span class="ala-audience-index">{i:02d}</span>
              <p class="ala-audience-text">
{span(ar, en)}
              </p>
            </div>"""
        )
    return "\n".join(parts)


def feature_cards(items):
    parts = []
    for i, (ar, en) in enumerate(items, 1):
        delay = "" if i == 1 else f'\n            style="--ala-delay:{(i - 1) * 60}ms;"'
        parts.append(
            f"""          <article class="ala-feature ala-reveal"{delay}>
            <div class="ala-feature-number">{i:02d}</div>
            <h3 class="ala-feature-title">
{span(ar, en)}
            </h3>
          </article>"""
        )
    return "\n".join(parts)


def transform_cards(pairs):
    parts = []
    for i, ((ar_b, en_b), (ar_a, en_a)) in enumerate(pairs, 1):
        delay = "" if i == 1 else f'\n            style="--ala-delay:{(i - 1) * 60}ms;"'
        parts.append(
            f"""          <div class="ala-transform-item ala-reveal"{delay}>
            <span class="ala-transform-index">{i:02d}</span>
            <div class="ala-transform-before">
              <span class="ala-before-label">
{dual("قبل", "BEFORE")}
              </span>
              <p class="ala-before-text">
{span(ar_b, en_b)}
              </p>
            </div>
            <div class="ala-transform-arrow-wrap">
              <div class="ala-transform-arrow">→</div>
            </div>
            <div class="ala-after-box">
              <span class="ala-after-label">
{dual("بعد", "AFTER")}
              </span>
              <p class="ala-after-text">
{span(ar_a, en_a)}
              </p>
            </div>
          </div>"""
        )
    return "\n".join(parts)


def faq_items(faqs):
    parts = []
    for (ar_q, en_q), (ar_a, en_a) in faqs:
        parts.append(
            f"""            <details class="ala-faq-item ala-reveal">
              <summary>
{span(ar_q, en_q)}
              </summary>
              <div class="ala-faq-answer">
{span(ar_a, en_a)}
              </div>
            </details>"""
        )
    return "\n".join(parts)


def build_main_sections() -> str:
    return f"""
    <section id="ala-hero" class="ala-hero">
      <div class="ala-container ala-hero-inner">
        <div class="ala-hero-visual ala-reveal" style="--ala-delay:180ms;">
          <div class="ala-hero-frame">
            <img
              class="ala-hero-image"
              src="https://assets.cdn.filesafe.space/x2KOxD9uXD3EImAPNXfQ/media/6a7a651e888087201921caae.png"
              alt="Ahmed Latif"
            >
          </div>
        </div>

        <div class="ala-hero-content ala-reveal" style="--ala-delay:80ms;">
          <div class="ala-course-pill">
{dual("كورس مسجل", "Recorded Course")}
          </div>

          <p class="ala-course-name">
{span(*COURSE_NAME)}
          </p>

          <h1 class="ala-hero-title">
{span(*COURSE_TAGLINE)}
          </h1>

          <p class="ala-hero-description">
{span(*SHORT)}
          </p>

          <div class="ala-hero-badges">
            <span class="ala-hero-badge">
{dual("كورس مسجل", "Recorded")}
            </span>
            <span class="ala-hero-badge">
{span(*PRICE_BADGE)}
            </span>
          </div>

          <div class="ala-hero-actions">
            <a href="#lead-form" class="ala-btn ala-btn-primary">
{dual("احجز مكانك الآن", "Book Your Seat Now")}
            </a>
            <a href="#ala-pain" class="ala-btn ala-btn-secondary">
{dual("اعرف أكتر", "Learn More")}
            </a>
          </div>
        </div>
      </div>
    </section>

    <section id="ala-transform" class="ala-transform">
      <div class="ala-container ala-transform-inner">
        <div class="ala-transform-header ala-reveal">
          <h2 class="ala-section-title">
{span("الوعد الرئيسي / التحول", "The Core Promise / Transformation")}
          </h2>
          <p class="ala-section-intro" style="max-width:720px;margin:16px auto 0;color:var(--ala-muted);line-height:1.8;text-align:center;">
{span(*PROMISE)}
          </p>
        </div>
        <div class="ala-transform-list">
{transform_cards(TRANSFORMS)}
        </div>
      </div>
    </section>

    <section id="ala-audience" class="ala-audience">
      <div class="ala-container ala-audience-inner">
        <div class="ala-audience-layout">
          <div class="ala-reveal">
            <h2 class="ala-section-title">
{span("الكورس ده لمين؟", "Who Is This Course For?")}
            </h2>
          </div>
          <div class="ala-audience-list">
{audience_items(AUDIENCE)}
          </div>
        </div>
      </div>
    </section>

    <section id="ala-pain" class="ala-pain">
      <div class="ala-container ala-pain-inner">
        <div class="ala-pain-header ala-reveal">
          <h2 class="ala-section-title">
{span("المشاكل اللي الكورس بيحلّها", "Problems This Course Solves")}
          </h2>
        </div>
        <div class="ala-pain-grid">
{pain_cards(PROBLEMS)}
        </div>
      </div>
    </section>

    <section id="ala-features" class="ala-features">
      <div class="ala-container ala-features-inner">
        <h2 class="ala-section-title ala-reveal">
{span("مميزات الكورس (Key Features)", "Course Features (Key Features)")}
        </h2>
        <div class="ala-features-grid">
{feature_cards(FEATURES)}
        </div>
      </div>
    </section>

    <section id="ala-learn" class="ala-learn">
      <div class="ala-container ala-learn-inner">
        <h2 class="ala-section-title ala-reveal">
{span("تفاصيل الكورس / المنهج", "Course Details / Curriculum")}
        </h2>
        <div class="ala-learning-grid">
          <div class="ala-learning-item ala-reveal" style="grid-column: 1 / -1;">
            <span class="ala-learning-index">01</span>
            <p class="ala-learning-text">
{span(*CURRICULUM)}
            </p>
          </div>
        </div>
      </div>
    </section>

    <section id="ala-pricing" class="ala-pricing">
      <div class="ala-container ala-pricing-inner">
        <h2 class="ala-section-title ala-reveal">
{span("السعر والعرض", "Price & Offer")}
        </h2>
        <div class="ala-price-card ala-reveal">
          <div class="ala-price-main">
            <div class="ala-price-label">
{span("العرض متاح لفترة محدودة", "Offer available for a limited time")}
            </div>
            <div class="ala-price-current">
              5,000
              <small>
{dual("جنيه", "EGP")}
              </small>
            </div>
            <div class="ala-price-old">9,800 EGP</div>
            <br>
            <div class="ala-price-save">
{span(*PRICE_SAVE)}
            </div>
          </div>
          <div class="ala-price-details">
            <div class="ala-price-list">
              <div class="ala-price-item">
{span(*FEATURES[4])}
              </div>
              <div class="ala-price-item">
{span(*FEATURES[0])}
              </div>
            </div>
            <a href="#lead-form" class="ala-btn ala-btn-primary ala-price-cta">
{span(*CTA_BTN_SHORT)}
            </a>
          </div>
        </div>
      </div>
    </section>

    <section id="ala-faq" class="ala-faq">
      <div class="ala-container">
        <div class="ala-faq-inner">
          <h2 class="ala-section-title ala-reveal">
{span("الأسئلة الشائعة (FAQs)", "Frequently Asked Questions (FAQs)")}
          </h2>
          <div class="ala-faq-list">
{faq_items(FAQS)}
          </div>
        </div>
      </div>
    </section>

    <section id="ala-final-cta" class="ala-pricing" style="padding-top: 24px;">
      <div class="ala-container ala-pricing-inner">
        <div class="ala-price-card ala-reveal">
          <div class="ala-price-main" style="flex: 1 1 100%;">
            <h2 class="ala-section-title" style="margin-bottom: 18px;">
{span(*CTA_POPUP)}
            </h2>
            <p style="color: var(--ala-muted); line-height: 1.8; margin: 0 0 16px;">
{span(*CTA_P1)}
            </p>
            <p style="color: var(--ala-muted); line-height: 1.8; margin: 0 0 22px;">
{span(*CTA_P2)}
            </p>
            <a href="#lead-form" class="ala-btn ala-btn-primary">
{span(*CTA_BTN)}
            </a>
          </div>
        </div>
      </div>
    </section>
"""


def main() -> None:
    html = SRC.read_text(encoding="utf-8")
    html = html.replace(
        "ALA PUBLIC SPEAKING LANDING PAGE",
        "ALA JOURNEY OF AWARENESS (رحلة وعي) RECORDED FUNNEL",
        1,
    )

    # Inject responsive CSS before first tablet media query
    if "JA FUNNEL — RESPONSIVE HARDENING" not in html:
        html = html.replace(
            "    /* =========================================================\n       LARGE TABLET / SMALL DESKTOP",
            RESPONSIVE_CSS
            + "\n    /* =========================================================\n       LARGE TABLET / SMALL DESKTOP",
            1,
        )

    start = html.find('<section\n      id="ala-hero"')
    if start < 0:
        start = html.find('id="ala-hero"')
        start = html.rfind("<section", 0, start)

    form_start = html.find('id="lead-form"')
    if form_start < 0:
        form_start = html.find('id="ala-form-modal"')
    form_start = html.rfind("<section", 0, form_start)
    if start < 0 or form_start < 0:
        raise SystemExit(f"markers not found start={start} form={form_start}")

    html = html[:start] + build_main_sections() + "\n\n    " + html[form_start:]

    # Final CTA / form labels from source
    html = html.replace(
        """            <span class="ala-ar">
              احجز مكانك في التدريب اللي غير حياة
              <strong>
                600 ألف شخص
              </strong>
            </span>


            <span
              class="ala-en"
              hidden
            >
              Reserve Your Place in the Training That Has Impacted
              <strong>
                600,000 People
              </strong>
            </span>""",
        f"""{span(*CTA_POPUP)}""",
        1,
    )
    html = html.replace('aria-label="Recorded - Public Speaking Course"', 'aria-label="Recorded - Journey of Awareness"')
    html = html.replace('data-form-name="Recorded - Public Speaking Course"', 'data-form-name="Recorded - Journey of Awareness"')
    html = html.replace('title="Recorded - Public Speaking Course"', 'title="Recorded - Journey of Awareness"')

    OUT.write_text(html, encoding="utf-8", newline="\n")
    text = OUT.read_text(encoding="utf-8")
    assert "Journey of Awareness" in text
    assert "Who Is This Course For?" in text
    assert "Problems This Course Solves" in text
    assert 'id="ala-trust"' not in text
    assert "JA FUNNEL — RESPONSIVE HARDENING" in text
    print("wrote", OUT, OUT.stat().st_size)
    print("ok")


if __name__ == "__main__":
    main()
