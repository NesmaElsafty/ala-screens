(function (window, document) {
  "use strict";

  var STORAGE_KEY = "ala-language";
  var SUPPORTED = { en: true, ar: true };

  function dict() {
    return window.ALA_I18N_DICT || {};
  }

  function getQueryLang() {
    try {
      var match = window.location.search.match(/[?&]lang=(en|ar)(?:&|#|$)/);
      return match ? match[1] : null;
    } catch (e) {
      return null;
    }
  }

  function getStoredLang() {
    try {
      var value = window.localStorage.getItem(STORAGE_KEY);
      return SUPPORTED[value] ? value : null;
    } catch (e) {
      return null;
    }
  }

  function saveLang(lang) {
    try {
      window.localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {}
  }

  function resolveLang() {
    return getQueryLang() || getStoredLang() || "en";
  }

  function getLanguage() {
    var lang = document.documentElement.getAttribute("lang");
    return SUPPORTED[lang] ? lang : resolveLang();
  }

  var originalText = typeof WeakMap === "function" ? new WeakMap() : null;
  var originalAttrs = typeof WeakMap === "function" ? new WeakMap() : null;

  function rememberText(node, value) {
    if (originalText) {
      if (!originalText.has(node)) originalText.set(node, value);
      return originalText.get(node);
    }
    if (!node.alaOrigText) node.alaOrigText = value;
    return node.alaOrigText;
  }

  function rememberAttr(el, name, value) {
    var bag = null;
    if (originalAttrs) {
      bag = originalAttrs.get(el);
      if (!bag) {
        bag = {};
        originalAttrs.set(el, bag);
      }
    } else {
      el.alaOrigAttrs = el.alaOrigAttrs || {};
      bag = el.alaOrigAttrs;
    }
    if (!(name in bag)) bag[name] = value;
    return bag[name];
  }

  function translateString(text, lang) {
    if (text == null) return text;
    if (lang === "en") return text;

    var map = dict();
    if (map[text]) return map[text];

    var trimmed = String(text).trim();
    if (map[trimmed]) {
      if (trimmed === String(text)) return map[trimmed];
      return String(text).replace(trimmed, map[trimmed]);
    }

    var copy = trimmed.match(/^©\s+(\d{4})\s+Ahmed Latif Academy\.\s+All rights reserved\.$/);
    if (copy) {
      return "© " + copy[1] + " Ahmed Latif Academy. جميع الحقوق محفوظة.";
    }

    var photo = trimmed.match(/^(.*?)(?: program| coaching program)? photo (\d+)$/i);
    if (photo) {
      var label = photo[1].replace(/\s+$/, "");
      var translatedLabel = map[label] || label;
      return "صورة " + photo[2] + " — " + translatedLabel;
    }

    var viewLarger = trimmed.match(/^View larger:\s*(.*)$/);
    if (viewLarger) {
      var rest = viewLarger[1];
      return "عرض أكبر: " + translateString(rest, lang);
    }

    var showPhoto = trimmed.match(/^Show photo (\d+):\s*(.*)$/);
    if (showPhoto) {
      return "عرض الصورة " + showPhoto[1] + ": " + translateString(showPhoto[2], lang);
    }

    return text;
  }

  function shouldSkip(el) {
    if (!el || !el.closest) return true;
    if (el.closest("script, style, noscript, .lang-switcher")) return true;
    if (el.isContentEditable) return true;
    return false;
  }

  function translateTextNodes(root, lang) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    var node;
    while ((node = walker.nextNode())) {
      var parent = node.parentNode;
      if (!parent || parent.nodeType !== 1) continue;
      var tag = parent.tagName;
      if (tag === "SCRIPT" || tag === "STYLE" || tag === "NOSCRIPT") continue;
      if (shouldSkip(parent)) continue;
      var raw = node.nodeValue;
      if (!raw || !raw.trim()) continue;
      if (!/[A-Za-z]/.test(raw) && lang === "ar") continue;
      var orig = rememberText(node, raw);
      var next = lang === "en" ? orig : translateString(orig, lang);
      if (next !== node.nodeValue) node.nodeValue = next;
    }
  }

  var ATTRS = ["placeholder", "aria-label", "alt", "title"];

  function translateAttrs(root, lang) {
    var selector = ATTRS.map(function (name) { return "[" + name + "]"; }).join(",");
    var els = root.querySelectorAll(selector);
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (shouldSkip(el)) continue;
      for (var a = 0; a < ATTRS.length; a++) {
        var name = ATTRS[a];
        if (!el.hasAttribute(name)) continue;
        var current = el.getAttribute(name);
        var orig = rememberAttr(el, name, current);
        var next = lang === "en" ? orig : translateString(orig, lang);
        if (next !== current) el.setAttribute(name, next);
      }
    }
  }

  function translateMeta(lang) {
    var titleEl = document.querySelector("title");
    if (titleEl) {
      var origTitle = rememberAttr(titleEl, "text", titleEl.textContent);
      document.title = lang === "en" ? origTitle : translateString(origTitle, lang);
    }

    var metas = document.querySelectorAll('meta[name="description"], meta[property="og:title"], meta[property="og:description"]');
    for (var i = 0; i < metas.length; i++) {
      var meta = metas[i];
      if (!meta.hasAttribute("content")) continue;
      var orig = rememberAttr(meta, "content", meta.getAttribute("content"));
      meta.setAttribute("content", lang === "en" ? orig : translateString(orig, lang));
    }
  }

  function isExternalHref(href) {
    if (!href) return true;
    var lower = href.trim().toLowerCase();
    if (lower.indexOf("mailto:") === 0 || lower.indexOf("tel:") === 0 || lower.indexOf("javascript:") === 0) return true;
    if (href.charAt(0) === "#") return true;

    var url;
    try {
      url = new URL(href, window.location.href);
    } catch (e) {
      return false;
    }

    if (url.protocol !== "http:" && url.protocol !== "https:") return false;

    var host = url.hostname.replace(/^www\./, "");
    var external = [
      "wa.me",
      "whatsapp.com",
      "api.whatsapp.com",
      "facebook.com",
      "instagram.com",
      "youtube.com",
      "youtu.be",
      "ala-eg.com",
      "unsplash.com",
      "images.unsplash.com",
      "cdnjs.cloudflare.com",
      "fonts.googleapis.com",
      "fonts.gstatic.com",
      "filesafe.space",
      "cashprocess.io"
    ];
    for (var i = 0; i < external.length; i++) {
      if (host === external[i] || host.slice(-(external[i].length + 1)) === "." + external[i]) return true;
    }
    return false;
  }

  function withLangParam(href, lang) {
    var hash = "";
    var hashIndex = href.indexOf("#");
    if (hashIndex >= 0) {
      hash = href.slice(hashIndex);
      href = href.slice(0, hashIndex);
    }
    if (!href) {
      var file = (window.location.pathname.split("/").pop() || "index.html");
      return file + "?lang=" + lang + hash;
    }

    var isAbs = /^(https?:)?\/\//i.test(href);
    try {
      var url = new URL(href, window.location.href);
      url.searchParams.set("lang", lang);
      if (isAbs) return url.origin + url.pathname + url.search + hash;
      return href.split("?")[0] + url.search + hash;
    } catch (e) {
      var qIndex = href.indexOf("?");
      if (qIndex === -1) return href + "?lang=" + lang + hash;
      var params = href.slice(qIndex + 1).split("&").filter(function (part) {
        return part && part.indexOf("lang=") !== 0;
      });
      params.push("lang=" + lang);
      return href.slice(0, qIndex) + "?" + params.join("&") + hash;
    }
  }

  function updateInternalLinks(lang) {
    var links = document.querySelectorAll("a[href]");
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      if (shouldSkip(a)) continue;
      var href = rememberAttr(a, "href", a.getAttribute("href"));
      if (isExternalHref(href)) {
        if (a.getAttribute("href") !== href) a.setAttribute("href", href);
        continue;
      }
      a.setAttribute("href", withLangParam(href, lang));
    }
  }

  var WA_GENERIC_EN = "You're just one step away from joining ALA! Contact us today, and one of our team members will be happy to assist you with the next available course date, course fees, current offers, answer all your questions, and help you complete your registration with ease.";
  var WA_GENERIC_AR = "أنت على بُعد خطوة واحدة من الانضمام إلى ALA! تواصل معنا اليوم، وسيسعد أحد أعضاء فريقنا بمساعدتك بموعد الدورة المتاح التالي، والرسوم، والعروض الحالية، والإجابة عن كل أسئلتك، وإتمام تسجيلك بسهولة.";

  function translateWhatsAppHrefs(lang) {
    var links = document.querySelectorAll('a[href*="wa.me"], a[href*="whatsapp.com"]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var href = rememberAttr(a, "href", a.getAttribute("href"));
      try {
        var url = new URL(href, window.location.href);
        var text = url.searchParams.get("text");
        if (!text) continue;
        var next = text;
        if (lang === "ar") {
          if (text === WA_GENERIC_EN) next = WA_GENERIC_AR;
          else next = translateString(text, lang);
          if (next === text) {
            next = text
              .replace(/^Hello ALA, I'm interested in:\s*/i, "مرحباً ALA، أنا مهتم/ة بـ: ")
              .replace(/^Hello ALA, I'm interested in /i, "مرحباً ALA، أنا مهتم/ة بـ ")
              .replace(/\nName:\s*/g, "\nالاسم: ")
              .replace(/\nPhone:\s*/g, "\nالهاتف: ")
              .replace(/\nEmail:\s*/g, "\nالبريد: ")
              .replace(/\nMessage:\s*/g, "\nالرسالة: ")
              .replace(/Please share the next available (?:course )?dates?, fees, and current offers\.?/i, "يرجى مشاركة أقرب المواعيد المتاحة والرسوم والعروض الحالية.")
              .replace(/Please share the next available course date, fees, and current offers\.?/i, "يرجى مشاركة أقرب موعد متاح للدورة والرسوم والعروض الحالية.");
          }
        }
        url.searchParams.set("text", next);
        a.setAttribute("href", url.toString());
      } catch (e) {}
    }
  }

  function updateDocumentLanguage(lang) {
    var root = document.documentElement;
    root.lang = lang;
    root.dir = lang === "ar" ? "rtl" : "ltr";
    root.setAttribute("lang", lang);
    root.setAttribute("dir", root.dir);
  }

  function updateSwitcher(lang) {
    var buttons = document.querySelectorAll("[data-lang-switch]");
    for (var i = 0; i < buttons.length; i++) {
      var btn = buttons[i];
      var value = btn.getAttribute("data-lang-switch");
      var active = value === lang;
      btn.classList.toggle("is-active", active);
      if (active) btn.setAttribute("aria-current", "true");
      else btn.removeAttribute("aria-current");
    }
  }

  function apply(lang) {
    lang = SUPPORTED[lang] ? lang : "en";
    updateDocumentLanguage(lang);
    translateMeta(lang);
    translateTextNodes(document.body || document.documentElement, lang);
    translateAttrs(document, lang);
    updateInternalLinks(lang);
    translateWhatsAppHrefs(lang);
    updateSwitcher(lang);
    document.documentElement.classList.remove("ala-i18n-pending");
    try {
      document.dispatchEvent(new CustomEvent("ala:languagechange", { detail: { lang: lang } }));
    } catch (e) {}
  }

  function setUrlLang(lang) {
    try {
      var url = new URL(window.location.href);
      url.searchParams.set("lang", lang);
      window.history.replaceState({}, "", url.toString());
    } catch (e) {}
  }

  function setLanguage(lang) {
    lang = SUPPORTED[lang] ? lang : "en";
    saveLang(lang);
    setUrlLang(lang);
    apply(lang);
    return lang;
  }

  function bindSwitcher() {
    document.addEventListener("click", function (event) {
      var btn = event.target.closest && event.target.closest("[data-lang-switch]");
      if (!btn) return;
      event.preventDefault();
      setLanguage(btn.getAttribute("data-lang-switch"));
    });
  }

  function init() {
    var lang = resolveLang();
    saveLang(lang);
    apply(lang);
    bindSwitcher();
    window.setTimeout(function () {
      document.documentElement.classList.remove("ala-i18n-pending");
    }, 2000);
  }

  window.ALA_I18N = {
    setLanguage: setLanguage,
    getLanguage: getLanguage,
    apply: apply,
    tText: function (text) {
      return translateString(text, getLanguage());
    },
    t: function (text) {
      return translateString(text, getLanguage());
    }
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})(window, document);
