const fs = require("fs");
const pages = ["portfolio.html", "programs.html", "camps.html"];
for (const p of pages) {
  const html = fs.readFileSync("d:/Projects/Ala Screens/" + p, "utf8");
  const re =
    /<!-- ALA_I18N_START -->[\s\S]*?<script>\s*window\.ALA_I18N_DICT[\s\S]*?<\/script>\s*<script>([\s\S]*?)<\/script>\s*<!-- ALA_I18N_END -->/;
  const m = html.match(re);
  if (!m) {
    console.log(p, "NO ENGINE");
    continue;
  }
  try {
    new Function(m[1]);
    console.log(p, "syntax OK", "dict keys", (html.match(/window\.ALA_I18N_DICT = (\{.*?\});/) || [])[0] ? "yes" : "no");
  } catch (e) {
    console.log(p, "SYNTAX ERROR", e.message);
  }
  // boot + css checks
  const bootOk = html.includes(
    '<noscript><style>html.ala-i18n-pending body { visibility: visible !important; }</style></noscript>'
  );
  const cssOk = /ALA_I18N_CSS_START[\s\S]*ALA_I18N_CSS_END[\s\S]*<\/style>\s*<\/head>/i.test(html);
  const academyInDict = /"Academy"\s*:/.test(html.match(/window\.ALA_I18N_DICT = (\{.*?\});/)[1]);
  console.log(" ", { bootOk, cssOk, academyInDict });
}
