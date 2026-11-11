// Check that every formula of a rendered page passes KaTeX (throwOnError).
// Usage: NODE_PATH=<node_modules folder> node tools/check_katex.mjs page1/index.html [page2/index.html ...]
// Quarto 1.7 writes formulas in <span class="math inline">...</span> and <span class="math display">...</span> (without \( \)).
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const katex = require("katex");
const decode = (s) => s.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, "&");
let bad = 0, total = 0;
for (const file of process.argv.slice(2)) {
  const html = readFileSync(file, "utf8");
  const re = /<span class="math (inline|display)">(?:\\[\(\[])?([\s\S]*?)(?:\\[\)\]])?<\/span>/g;
  let m;
  while ((m = re.exec(html))) {
    total++;
    const tex = decode(m[2]);
    try { katex.renderToString(tex, { displayMode: m[1] === "display", throwOnError: true, strict: "ignore" }); }
    catch (e) { bad++; console.log(`${file}: ${e.message.split("\n")[0]}\n    ${tex.slice(0, 160)}`); }
  }
}
console.log(`${total} formulas, ${bad} errors`);
process.exit(bad ? 1 : 0);
