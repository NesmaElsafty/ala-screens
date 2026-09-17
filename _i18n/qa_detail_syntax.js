const fs = require("fs");
const pages = [
  "shiftCamp.html","silentCamp.html","poc.html","acc.html","pcc.html",
  "nlp.html","nlpKids.html","ps.html","psKids.html","leadershipKids.html",
  "pg.html","ots.html","tot.html","ps-recorded.html"
];
let bad = 0;
for (const p of pages) {
  const html = fs.readFileSync("d:/Projects/Ala Screens/" + p, "utf8");
  const re =
    /<!-- ALA_I18N_START -->[\s\S]*?<script>\s*window\.ALA_I18N_DICT[\s\S]*?<\/script>\s*<script>([\s\S]*?)<\/script>\s*<!-- ALA_I18N_END -->/;
  const m = html.match(re);
  if (!m) { console.log(p, "NO ENGINE"); bad++; continue; }
  try { new Function(m[1]); } catch (e) { console.log(p, "SYNTAX", e.message); bad++; continue; }
  const academy = /"Academy"\s*:/.test(html.match(/window\.ALA_I18N_DICT = (\{.*?\});/)[1]);
  const skip = m[1].includes("logo-academy");
  const boot = html.includes("ala-language") && html.includes("ALA_I18N_BOOT");
  if (academy || !skip || !boot) {
    console.log(p, { academy, skip, boot });
    bad++;
  } else {
    console.log(p, "OK");
  }
}
console.log("failures", bad);
