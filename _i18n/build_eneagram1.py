# -*- coding: utf-8 -*-
"""Build eneagram1.html content + CDN gallery from template copy."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(r"d:\Projects\Ala Screens")
path = ROOT / "eneagram1.html"
html = path.read_text(encoding="utf-8")

urls = [
    u.strip()
    for u in (ROOT / "images" / "eneagram1Images.html").read_text(encoding="utf-8").splitlines()
    if u.strip().startswith("http")
]
hero_src = urls[2] if len(urls) > 2 else urls[0]

gallery_js = ",\n        ".join(
    f'{{ src: "{u}", alt: "Enneagram program photo {i}" }}'
    for i, u in enumerate(urls, 1)
)

wa_interest = quote(
    "Hello ALA, I'm interested in the Enneagram | Level 1 program. Please share the next available dates, fees, and current offers."
)
wa_generic = "You%27re%20just%20one%20step%20away%20from%20joining%20ALA%21%20Contact%20us%20today%2C%20and%20one%20of%20our%20team%20members%20will%20be%20happy%20to%20assist%20you%20with%20the%20next%20available%20course%20date%2C%20course%20fees%2C%20current%20offers%2C%20answer%20all%20your%20questions%2C%20and%20help%20you%20complete%20your%20registration%20with%20ease."

# --- Meta ---
html = html.replace(
    """  <title>Life Coaching Program | PCC Level | Ahmed Latif Academy</title>
  <meta name="description" content="Explore Ahmed Latif Academy's Life Coaching Program at PCC Level — 50 hours of training, mentoring, Relation Coaching, Positive Psychology, and one year of follow-up support.">
  <meta property="og:title" content="Life Coaching Program | PCC Level | Ahmed Latif Academy">
  <meta property="og:description" content="Explore Ahmed Latif Academy's Life Coaching Program at PCC Level — 50 hours of training, mentoring, Relation Coaching, Positive Psychology, and one year of follow-up support.">""",
    """  <title>Enneagram | Level 1 | Ahmed Latif Academy</title>
  <meta name="description" content="Explore Ahmed Latif Academy's Enneagram Level 1 — 44 hours live training to understand people from the inside: 9 personality types, 3 intelligence centers, hiring, teamwork, and deeper relationships.">
  <meta property="og:title" content="Enneagram | Level 1 | Ahmed Latif Academy">
  <meta property="og:description" content="Explore Ahmed Latif Academy's Enneagram Level 1 — 44 hours live training to understand people from the inside: 9 personality types, 3 intelligence centers, hiring, teamwork, and deeper relationships.">""",
)

# --- Breadcrumb ---
html = html.replace(
    '<li class="breadcrumb-current" aria-current="page">Life Coaching Program | PCC Level</li>',
    '<li class="breadcrumb-current" aria-current="page">Enneagram | Level 1</li>',
)

# --- Hero ---
html = html.replace(
    """          <p class="eyebrow anim-item">Live Program</p>
          <h1 class="program-hero-title anim-item">
            <span class="line-dark">Life Coaching Program</span>
            <span class="line-gold">PCC Level</span>
          </h1>
          <p class="program-hero-desc anim-item">You finished your ACC. You're officially a coach. But there's a real gap between doing coaching and being the coach your clients walk away from with a different level of awareness. That gap has a name: PCC — a real shift in your presence, not another line on your resume.</p>
          <div class="program-meta anim-item" aria-label="Program facts">
            <span class="program-meta-badge"><i class="fa-regular fa-circle-dot" aria-hidden="true"></i> Live Program</span>
            <span class="program-meta-badge"><i class="fa-regular fa-clock" aria-hidden="true"></i> 50 Hours</span>
            <span class="program-meta-badge"><i class="fa-regular fa-calendar" aria-hidden="true"></i> 1 Year Follow-up</span>
          </div>""",
    """          <p class="eyebrow anim-item">Live Program</p>
          <h1 class="program-hero-title anim-item">
            <span class="line-dark">Enneagram</span>
            <span class="line-gold">Level 1</span>
          </h1>
          <p class="program-hero-desc anim-item">Why do certain colleagues drain you at work for no clear reason? Why does your partner react a certain way in specific situations — and you just can't figure out why? Why does a candidate look perfect in the interview, only for you to discover later they're completely wrong for the role? The truth is, everyone is driven by an inner need that's invisible to the outside world. The Enneagram is the science that reveals exactly that need — not a typical personality label, but a framework that shows you the reason behind any behavior at home, at work, or when you're hiring someone new.</p>
          <div class="program-meta anim-item" aria-label="Program facts">
            <span class="program-meta-badge"><i class="fa-regular fa-circle-dot" aria-hidden="true"></i> Live Program</span>
            <span class="program-meta-badge"><i class="fa-regular fa-clock" aria-hidden="true"></i> 44 Hours</span>
            <span class="program-meta-badge"><i class="fa-solid fa-users" aria-hidden="true"></i> 9 Personality Types</span>
          </div>""",
)

html = re.sub(
    r'(id="programHeroImage"\s*\n\s*src=")[^"]+(")',
    rf'\1{hero_src}\2',
    html,
    count=1,
)
html = html.replace(
    'alt="Ahmed Latif mentoring a participant during a PCC coaching session"',
    'alt="Participants during a live Enneagram training with Ahmed Latif Academy"',
)

# --- Quick facts ---
html = re.sub(
    r'<section class="quick-facts"[\s\S]*?</section>\s*\n\s*<section class="audience-section"',
    """<section class="quick-facts" id="quick-facts" aria-label="Program quick facts">
      <div class="container">
        <div class="quick-facts-grid">
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
          <div class="quick-fact anim-scale">
            <i class="fa-solid fa-users" aria-hidden="true"></i>
            <strong>9 Types</strong>
            <span>Personality Map</span>
          </div>
          <div class="quick-fact anim-scale">
            <i class="fa-regular fa-lightbulb" aria-hidden="true"></i>
            <strong>3 Centers</strong>
            <span>Head · Heart · Body</span>
          </div>
        </div>
      </div>
    </section>

    <section class="audience-section""",
    html,
    count=1,
)

# --- Audience ---
html = re.sub(
    r'(<section class="audience-section"[\s\S]*?<div class="audience-grid">)[\s\S]*?(</div>\s*</div>\s*</section>\s*\n\s*<section class="learning-section")',
    r"""\1
          <article class="audience-card anim-scale">
            <div class="icon-wrap" aria-hidden="true"><i class="fa-regular fa-briefcase"></i></div>
            <h3>Leaders &amp; Teams</h3>
            <p>For managers and professionals who want to stop guessing with colleagues and start reading people with real clarity.</p>
          </article>
          <article class="audience-card anim-scale">
            <div class="icon-wrap" aria-hidden="true"><i class="fa-regular fa-id-badge"></i></div>
            <h3>Hiring &amp; Interviews</h3>
            <p>For anyone involved in hiring who wants to place the right person in the right role — beyond the CV and interview talk.</p>
          </article>
          <article class="audience-card anim-scale">
            <div class="icon-wrap" aria-hidden="true"><i class="fa-regular fa-heart"></i></div>
            <h3>Relationships &amp; Family</h3>
            <p>For people who want deeper understanding with a partner, children, and family — instead of blame without a clear reason.</p>
          </article>
        \2""",
    html,
    count=1,
)

# --- Learning ---
html = re.sub(
    r'(<section class="learning-section"[\s\S]*?<div class="section-header">[\s\S]*?</div>\s*<div class="learning-grid">)[\s\S]*?(</div>\s*</div>\s*</section>\s*\n\s*<section class="outcomes-section")',
    r"""\1
          <article class="learning-card anim-scale">
            <div class="icon-wrap" aria-hidden="true"><i class="fa-solid fa-9"></i></div>
            <h3>The 9 Personality Types</h3>
            <p>The 9 personality types, and how to read anyone from your very first interaction with them.</p>
          </article>
          <article class="learning-card anim-scale">
            <div class="icon-wrap" aria-hidden="true"><i class="fa-regular fa-brain"></i></div>
            <h3>3 Intelligence Centers</h3>
            <p>Head, Heart, and Body — and how each center drives a completely different kind of reaction.</p>
          </article>
          <article class="learning-card anim-scale">
            <div class="icon-wrap" aria-hidden="true"><i class="fa-regular fa-eye"></i></div>
            <h3>Real Motives</h3>
            <p>How to understand the real motive behind someone's behavior — not just the behavior itself.</p>
          </article>
          <article class="learning-card anim-scale">
            <div class="icon-wrap" aria-hidden="true"><i class="fa-regular fa-handshake"></i></div>
            <h3>Interviews &amp; Hiring</h3>
            <p>Use the Enneagram in interviews and hiring to uncover what a candidate truly needs and what drives them.</p>
          </article>
          <article class="learning-card anim-scale">
            <div class="icon-wrap" aria-hidden="true"><i class="fa-regular fa-comments"></i></div>
            <h3>Work Relationships</h3>
            <p>Deal with your manager, colleagues, and business partners by genuinely understanding how they think.</p>
          </article>
          <article class="learning-card anim-scale">
            <div class="icon-wrap" aria-hidden="true"><i class="fa-regular fa-house"></i></div>
            <h3>Family Understanding</h3>
            <p>Build real understanding with your partner, children, and family — instead of blaming each other for unclear reasons.</p>
          </article>
        \2""".replace(
        '<p class="eyebrow anim-item">What You\'ll Learn</p>\n          <h2 class="section-heading anim-item">Presence. Depth. Specialization.</h2>',
        '<p class="eyebrow anim-item">What You\'ll Learn</p>\n          <h2 class="section-heading anim-item">Understand People from the Inside.</h2>',
    ),
    html,
    count=1,
)

# Fix learning header separately if still PCC text
html = html.replace(
    """          <p class="eyebrow anim-item">What You'll Learn</p>
          <h2 class="section-heading anim-item">Presence. Depth. Specialization.</h2>""",
    """          <p class="eyebrow anim-item">What You'll Learn</p>
          <h2 class="section-heading anim-item">Understand People from the Inside.</h2>""",
)

# --- Outcomes ---
html = re.sub(
    r'(<section class="outcomes-section"[\s\S]*?<ul class="outcomes-list">)[\s\S]*?(</ul>)',
    r"""\1
          <li class="anim-item"><i class="fa-solid fa-check" aria-hidden="true"></i><span>Understand why people behave the way they do at work, and adapt your approach to fit each personality</span></li>
          <li class="anim-item"><i class="fa-solid fa-check" aria-hidden="true"></i><span>Hire smarter — uncover a candidate's real needs and motivations, not just what's on their CV or what they say in the interview</span></li>
          <li class="anim-item"><i class="fa-solid fa-check" aria-hidden="true"></i><span>Build a well-rounded team, with everyone in the role that truly fits their nature</span></li>
          <li class="anim-item"><i class="fa-solid fa-check" aria-hidden="true"></i><span>Communicate better with your manager and business partners, and negotiate with real insight</span></li>
          <li class="anim-item"><i class="fa-solid fa-check" aria-hidden="true"></i><span>Understand your partner and children on a deeper level, and close the distance that used to have no clear explanation</span></li>
          <li class="anim-item"><i class="fa-solid fa-check" aria-hidden="true"></i><span>Discover why certain people drain you while others feel effortless — and use that to your advantage in every relationship</span></li>
        \2""",
    html,
    count=1,
)
html = html.replace(
    """          <p class="eyebrow anim-item">By the End of the Program</p>
          <h2 class="section-heading anim-item">You'll Become:</h2>""",
    """          <p class="eyebrow anim-item">By the End of the Program</p>
          <h2 class="section-heading anim-item">You'll Be Able To:</h2>""",
)

# --- Why ---
html = re.sub(
    r'(<section class="why-program"[\s\S]*?<div class="why-grid">)[\s\S]*?(</div>\s*</div>\s*</section>\s*\n\s*<section class="program-proof")',
    r"""\1
          <article class="why-card anim-scale">
            <div class="icon-wrap" aria-hidden="true"><i class="fa-regular fa-compass"></i></div>
            <h3>Beyond Labels</h3>
            <p>This isn't typical personality science that just labels you. It's a framework that reveals the real need driving every behavior.</p>
          </article>
          <article class="why-card anim-scale">
            <div class="icon-wrap" aria-hidden="true"><i class="fa-regular fa-hand"></i></div>
            <h3>Applied, Not Passive</h3>
            <p>Training includes hands-on workshops, role-play, interactive games, and visual tools — so you apply the framework, not just hear it.</p>
          </article>
          <article class="why-card anim-scale">
            <div class="icon-wrap" aria-hidden="true"><i class="fa-regular fa-users"></i></div>
            <h3>Work, Hiring &amp; Home</h3>
            <p>Use the same map with colleagues, candidates, partners, and family — stop guessing and start understanding from day one.</p>
          </article>
        \2""",
    html,
    count=1,
)
html = html.replace(
    """          <p class="eyebrow anim-item">Why This Program?</p>
          <h2 class="section-heading anim-item">More Than Another Program. A Real Shift.</h2>""",
    """          <p class="eyebrow anim-item">Why This Program?</p>
          <h2 class="section-heading anim-item">Stop Guessing. Start Understanding.</h2>""",
)

# --- Proof ---
html = re.sub(
    r'(<section class="program-proof"[\s\S]*?<div class="proof-stats">)[\s\S]*?(</div>\s*<p class="section-intro)',
    r"""\1
          <div class="proof-stat anim-scale">
            <div class="number">44h</div>
            <div class="label">Live Training</div>
          </div>
          <div class="proof-stat anim-scale">
            <div class="number">9</div>
            <div class="label">Personality Types</div>
          </div>
          <div class="proof-stat anim-scale">
            <div class="number">3</div>
            <div class="label">Intelligence Centers</div>
          </div>
        \2""",
    html,
    count=1,
)
html = html.replace(
    """          <p class="eyebrow anim-item">Proven Track Record</p>
          <h2 class="section-heading anim-item">Already Delivered. Already Making a Difference.</h2>""",
    """          <p class="eyebrow anim-item">Proven Track Record</p>
          <h2 class="section-heading anim-item">A Map You Can Use Immediately.</h2>""",
)
html = html.replace(
    "This isn't a first-time program. Explore photos from past batches in the gallery and see the difference for yourself.",
    "Explore photos from live Enneagram sessions in the gallery and see the energy of the room for yourself.",
)

# --- Timeline ---
html = re.sub(
    r'(<section class="program-timeline"[\s\S]*?<div class="timeline-track">)[\s\S]*?(</div>\s*</div>\s*</section>\s*\n\s*<section class="program-gallery")',
    r"""\1
          <article class="timeline-step anim-item">
            <div class="timeline-num">01</div>
            <h3>Learn</h3>
            <p>The 9 types and 3 intelligence centers</p>
          </article>
          <article class="timeline-step anim-item">
            <div class="timeline-num">02</div>
            <h3>Practice</h3>
            <p>Workshops, role-play, and interactive games</p>
          </article>
          <article class="timeline-step anim-item">
            <div class="timeline-num">03</div>
            <h3>Apply</h3>
            <p>Hiring, teams, and everyday relationships</p>
          </article>
          <article class="timeline-step anim-item">
            <div class="timeline-num">04</div>
            <h3>Read People</h3>
            <p>Understand motives from the first interaction</p>
          </article>
        \2""",
    html,
    count=1,
)
html = html.replace(
    """          <p class="eyebrow anim-item">How the Program Works</p>
          <h2 class="section-heading anim-item">A Journey Designed for Practice and Growth</h2>""",
    """          <p class="eyebrow anim-item">How You'll Learn</p>
          <h2 class="section-heading anim-item">Not a Passive Lecture. Real Practice.</h2>""",
)

# --- Gallery header ---
html = html.replace(
    """          <p class="eyebrow anim-item">Program Experience</p>
          <h2 class="section-heading anim-item">Inside the PCC Experience</h2>
          <p class="section-intro anim-item">Explore highlights from training sessions, mentoring, and previous PCC batches.</p>""",
    """          <p class="eyebrow anim-item">Program Experience</p>
          <h2 class="section-heading anim-item">Inside the Enneagram Experience</h2>
          <p class="section-intro anim-item">Explore highlights from live Enneagram sessions and previous groups.</p>""",
)
html = html.replace(
    'aria-label="PCC program photo gallery"',
    'aria-label="Enneagram program photo gallery"',
)

# --- CTA ---
html = html.replace(
    """          <h2>Ready to Step Into PCC?</h2>
          <p>There's a difference between being a coach, and being the coach no one forgets. Take the next step in your professional coaching path.</p>""",
    """          <h2>Ready to Understand People from Day One?</h2>
          <p>Stop guessing with people. Start understanding them from the inside. Book your seat now.</p>""",
)

# WhatsApp CTAs that mention PCC
html = re.sub(
    r"https://wa\.me/201010002231\?text=Hello%20ALA%2C%20I%27m%20interested%20in%20the%20Life%20Coaching%20Program%20%7C%20PCC%20Level\.[^\"']*",
    f"https://wa.me/201010002231?text={wa_interest}",
    html,
)

# --- Gallery images array ---
html = re.sub(
    r"var galleryImages = \[[\s\S]*?\];",
    f"var galleryImages = [\n        {gallery_js}\n      ];",
    html,
    count=1,
)

path.write_text(html, encoding="utf-8", newline="\n")
print(f"updated eneagram1.html urls={len(urls)} hero={hero_src[-40:]}")
