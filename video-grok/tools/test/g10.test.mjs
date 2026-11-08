import assert from "node:assert/strict";
import { copyFile, mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { loadScene, viewAt, cueTime } from "../../engine/scene.js";
import { ouvrir } from "../navigateur.mjs";
import { servir } from "../servir.mjs";
import classesRaw from "../../scenes/g10/classes.json" with { type: "json" };
import sampleRaw from "../../scenes/g10/sample.json" with { type: "json" };
import cardRaw from "../../scenes/g10/card.json" with { type: "json" };
import slots from "../../scenes/g10/cues.json" with { type: "json" };

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "../..");
const repo = join(root, "..");
const classes = loadScene(classesRaw);
const sample = loadScene(sampleRaw);
const card = loadScene(cardRaw);
const narration = await readFile(join(root, "narration/en/g10.md"), "utf8");
const digest = (await readFile(join(repo, "experiences/resultats/digest.md"), "utf8")).split("\n");

const CARD_SENTENCE = "Must stationarity fine-tuning be anchored first?";
const DIVERGENCE_ORDER = ["V0", "V1", "V2", "V3", "V4", "V5", "witness", "subsample"];

function line(number) {
  return digest[number - 1];
}

function tokens(text) {
  return new Set(text.match(/\d+(?:\.\d+)?(?:e[+-]?\d+)?/gi) ?? []);
}

const figureTokens = new Set([
  ...tokens([14, 19, ...Array.from({ length: 11 }, (_, index) => 134 + index)].map(line).join("\n")),
]);

test("les durées, la pause et la formule suivent le pilote", () => {
  assert.equal(classes.duration, 45);
  assert.equal(sample.duration, 40);
  assert.equal(card.duration, 8);
  assert.equal(cueTime(card, "cue.g10.card.end") - cueTime(card, "cue.g10.card"), 8);

  const pause = cueTime(sample, "cue.g10.sample.e1") - cueTime(sample, "cue.g10.sample.predict");
  assert.ok(pause >= 2 && pause <= 3, `pause ${pause}`);
  const predict = viewAt(sample, cueTime(sample, "cue.g10.sample.predict") + pause / 2);
  assert.equal(predict.bars, null);
  assert.equal(predict.subtitle.text, "Does the crushed bar help?");
  assert.equal(JSON.stringify(predict).includes("4.17e-17"), false);

  const crushedAt = cueTime(sample, "cue.g10.sample.e1.spread");
  assert.ok(crushedAt > cueTime(sample, "cue.g10.sample.predict"));
  const crushed = viewAt(sample, crushedAt);
  assert.deepEqual(crushed.bars.rows.map((row) => row.name), ["C", "E"]);
  assert.equal(crushed.bars.rows[1].label, "4.17e-17");
  assert.ok(crushed.bars.rows[1].value < crushed.bars.rows[0].value);
  assert.equal(crushed.badges.some((badge) => badge.kind === "MEASURED" && badge.primary), true);

  const formula = viewAt(sample, cueTime(sample, "cue.g10.sample.formula"));
  assert.equal(formula.subtitle, null);
  assert.equal(formula.bars, null);
  assert.equal(formula.matter, "paper");
  assert.equal(formula.transition, null);
  assert.equal(formula.badges.length, 0);
  assert.equal(formula.formula.terms[0].lit, true);
  assert.match(formula.formula.terms[0].tex, /Hypothesis: no mass at 0/);
  assert.equal(/KL|infty|∞/.test(formula.formula.terms[0].tex), false);
  assert.equal(/4\.17e-17|8\.64e-04|8\.27e-06/.test(formula.formula.terms[0].tex), false);
});

test("les chiffres affichés sont ceux du digest, dans l'ordre fixe", () => {
  const shown = [];
  for (const cue of sample.cues) {
    const view = viewAt(sample, cue.at);
    if (!view.bars || view.bars.schematic) continue;
    for (const row of view.bars.rows) {
      assert.equal(figureTokens.has(row.label), true, `${cue.id} ${row.name} ${row.label}`);
      shown.push(row.label);
    }
  }
  for (const label of ["0.408", "0.34", "5.05e-17", "2.03e-08", "8.27e-06", "8.64e-04", "0.00257", "0.0231", "4.17e-17"]) {
    assert.equal(shown.includes(label), true, label);
  }

  const divergence = viewAt(sample, cueTime(sample, "cue.g10.sample.div"));
  assert.equal(divergence.bars.log, true);
  assert.equal(divergence.bars.title, "Divergence, log scale");
  assert.equal(divergence.bars.seedLabel, "one seed");
  assert.deepEqual(divergence.bars.rows.map((row) => row.name), DIVERGENCE_ORDER);
  const byValue = [...divergence.bars.rows].sort((a, b) => a.value - b.value).map((row) => row.name);
  assert.notDeepEqual(divergence.bars.rows.map((row) => row.name), byValue);
  assert.equal(divergence.bars.rows.at(-1).role, "infra");
  assert.equal(divergence.bars.rows[5].role, "model");

  const distance = viewAt(sample, cueTime(sample, "cue.g10.sample.e1"));
  assert.equal(distance.bars.seedLabel, "two seeds");
  assert.equal(distance.bars.floor.label, "noise floor");
  assert.equal(distance.bars.floor.n, 10000);
  assert.match(line(5), /10000/);
  const floor = sample.layers.find((layer) => layer.kind === "bars" && layer.floor != null);
  assert.equal(line(48).includes(String(floor.floor)), true);

  const proved = viewAt(classes, cueTime(classes, "cue.g10.classes.c4"));
  assert.deepEqual(proved.bars.rows.map((row) => row.name), ["C1", "C2", "C3", "C4"]);
  assert.equal(new Set(proved.bars.rows.map((row) => row.value)).size, 1);
  assert.equal(proved.bars.schematic, true);
  assert.deepEqual(proved.bars.rows.map((row) => row.role), ["velocity", "field", "model", "parameter"]);
  assert.equal(proved.badges.some((badge) => badge.kind === "PROVED" && badge.primary), true);
});

test("les sous-titres sont des extraits du script, et la carte est q.g10", () => {
  for (const scene of [classes, sample]) {
    for (const layer of scene.layers) {
      if (layer.kind !== "subtitle") continue;
      assert.equal(narration.includes(layer.text), true, layer.text);
      assert.equal(/KL|infty|∞|Hypothesis/.test(layer.text), false, layer.text);
    }
  }
  const opening = viewAt(card, cueTime(card, "cue.g10.card"));
  assert.equal(opening.questionCard.sentence, CARD_SENTENCE);
  assert.equal(opening.questionCard.class, "A");
  assert.equal(opening.questionCard.badge, "PLANNED");
  assert.equal(narration.includes(CARD_SENTENCE), true);
  assert.equal(viewAt(card, 7.9).questionCard.sentence, CARD_SENTENCE);
  assert.equal(viewAt(card, 8).questionCard, null);
});

const CAVEAT_EN =
  "E2 is two-dimensional and forced. One seed. The tests are interpolation. This is not a dynamo.";
const CAVEAT_FR =
  "E2 est bidimensionnel et forcé. Une seule graine aléatoire a été testée. Les tests portent sur des valeurs intermédiaires dans la plage d’entraînement. Ce n’est pas une dynamo.";

test("le caveat de g10.law reste sans voix", async () => {
  assert.equal(slots.slots.length, 2);
  for (const slot of slots.slots) {
    assert.equal(slot.id, "cue.g10.law.caveat");
    assert.equal(slot.audio, null);
    assert.equal(slot.status, "PENDING");
  }
  const english = slots.slots.find((slot) => slot.lang === "en");
  const french = slots.slots.find((slot) => slot.lang === "fr");
  assert.equal(english.source, "narration/en/g10.md");
  assert.equal(french.source, "narration/fr/g10.law.caveat.md");
  assert.match(narration, /cue\.g10\.law\.caveat/);
  assert.equal(parole(narration, "cue.g10.law.caveat"), CAVEAT_EN);
  await assert.rejects(readFile(join(root, "narration/fr/g10.md"), "utf8"));
  const tree = await readFile(join(root, "scenes/g10/cues.json"), "utf8");
  assert.equal(tree.includes("One seed"), false);
  assert.equal(tree.includes("dynamo"), false);
});

test("les deux créneaux du caveat disent les trois limites", async () => {
  const points = {
    en: [/One seed/, /interpolation/, /not a dynamo/],
    fr: [/Une seule graine aléatoire/, /valeurs intermédiaires dans la plage d’entraînement/, /pas une dynamo/],
  };
  const expected = { en: CAVEAT_EN, fr: CAVEAT_FR };
  for (const lang of ["en", "fr"]) {
    const slot = slots.slots.find((item) => item.lang === lang);
    assert.equal(typeof slot.source, "string", lang);
    const text = parole(await readFile(join(root, slot.source), "utf8"), slot.id);
    assert.equal(text.length > 0, true, lang);
    assert.equal(text, expected[lang], lang);
    for (const point of points[lang]) assert.match(text, point, `${lang} ${point}`);
  }
});

function parole(markdown, cueId) {
  const lines = markdown.split(/\r?\n/);
  const start = lines.findIndex((line) => line.trim() === `### ${cueId}`);
  if (start < 0) return "";
  const body = [];
  for (const line of lines.slice(start + 1)) {
    if (line.startsWith("## ") || line.startsWith("### ")) break;
    const trimmed = line.trim();
    if (trimmed === "" || trimmed.startsWith("role:")) continue;
    body.push(trimmed);
  }
  return body.join(" ");
}

test("le texte reste à 28 px, hors marge, et ne coupe pas les barres", async () => {
  const server = await servir(root);
  const pages = [
    ["classes.html", ["cue.g10.classes.show", "cue.g10.classes.c1", "cue.g10.classes.c4", "cue.g10.classes.bar"]],
    [
      "sample.html",
      [
        "cue.g10.sample.div",
        "cue.g10.sample.e2",
        "cue.g10.sample.predict",
        "cue.g10.sample.e1",
        "cue.g10.sample.e1.spread",
        "cue.g10.sample.formula",
      ],
    ],
    ["card.html", ["cue.g10.card"]],
  ];
  const { browser, page } = await ouvrir(`http://127.0.0.1:${server.port}/scenes/g10/${pages[0][0]}`);
  try {
    for (const [file, cues] of pages) {
      await page.goto(`http://127.0.0.1:${server.port}/scenes/g10/${file}`, { waitUntil: "load" });
      await page.evaluate(() => document.fonts.ready);
      for (const cue of cues) {
        const report = await page.evaluate((id) => {
          window.seek(window.__scene.cue(id));
          const rectsOf = (selector) =>
            [...document.querySelectorAll(selector)].flatMap((node) =>
              [...node.getClientRects()]
                .filter((rect) => rect.width > 0.5 && rect.height > 0.5)
                .map((rect) => ({ x: rect.x, y: rect.y, right: rect.right, bottom: rect.bottom })),
            );
          const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
          const items = [];
          while (walker.nextNode()) {
            const node = walker.currentNode;
            const text = node.textContent.replace(/\s+/g, " ").trim();
            if (!text) continue;
            const parent = node.parentElement;
            const style = getComputedStyle(parent);
            if (style.display === "none" || style.visibility === "hidden" || Number(style.opacity) === 0) continue;
            const size = Number.parseFloat(style.fontSize);
            const range = document.createRange();
            range.selectNodeContents(node);
            items.push({
              text,
              size,
              katex: parent.closest(".katex") != null,
              rects: [...range.getClientRects()]
                .filter((rect) => rect.width > 0.5 && rect.height > 0.5)
                .map((rect) => ({ x: rect.x, y: rect.y, right: rect.right, bottom: rect.bottom })),
            });
          }
          return {
            items,
            bars: rectsOf(".bar-fill, .floor-line"),
            formula: rectsOf(".formula"),
            cue: document.querySelector(".stage").dataset.cue,
          };
        }, cue);
        assert.equal(report.cue, cue, file);
        assert.ok(report.items.length > 0, cue);
        for (const item of report.items) {
          assert.ok(item.size >= 28, `${cue} ${item.text} ${item.size}`);
          for (const rect of item.rects) {
            assert.ok(rect.x >= 80, `${cue} ${item.text} x ${rect.x}`);
            assert.ok(rect.y >= 80, `${cue} ${item.text} y ${rect.y}`);
            assert.ok(rect.right <= 1840, `${cue} ${item.text} right ${rect.right}`);
            assert.ok(rect.bottom <= 1000, `${cue} ${item.text} bottom ${rect.bottom}`);
            for (const bar of report.bars) {
              const hit =
                rect.x < bar.right - 0.5 &&
                rect.right > bar.x + 0.5 &&
                rect.y < bar.bottom - 0.5 &&
                rect.bottom > bar.y + 0.5;
              assert.equal(hit, false, `${cue} ${item.text} coupe une barre`);
            }
          }
        }
        for (let i = 0; i < report.items.length; i += 1) {
          for (let j = i + 1; j < report.items.length; j += 1) {
            if (report.items[i].katex && report.items[j].katex) continue;
            for (const a of report.items[i].rects) {
              for (const b of report.items[j].rects) {
                const hit = a.x < b.right - 0.5 && a.right > b.x + 0.5 && a.y < b.bottom - 0.5 && a.bottom > b.y + 0.5;
                assert.equal(hit, false, `${cue} ${report.items[i].text} / ${report.items[j].text}`);
              }
            }
          }
        }
        if (cue === "cue.g10.sample.formula") {
          assert.ok(report.formula.length > 0);
          for (const box of report.formula) {
            for (const item of report.items) {
              if (item.katex) continue;
              for (const rect of item.rects) {
                const hit =
                  rect.x < box.right - 0.5 &&
                  rect.right > box.x + 0.5 &&
                  rect.y < box.bottom - 0.5 &&
                  rect.bottom > box.y + 0.5;
                assert.equal(hit, false, `${item.text} coupe la formule`);
              }
            }
          }
        }
      }
    }
  } finally {
    await browser.close();
    await server.close();
  }
});

test("deux captures du même repère donnent la même image, carte comprise", async () => {
  const server = await servir(root);
  let browser;
  let dir;
  try {
    dir = await mkdtemp(join(tmpdir(), "g10-captures-"));
    const opened = await ouvrir(`http://127.0.0.1:${server.port}/scenes/g10/card.html`);
    browser = opened.browser;
    const page = opened.page;
    const shots = [
      ["classes.html", "cue.g10.classes.c4", "g10-classes-c4.png"],
      ["sample.html", "cue.g10.sample.div", "g10-sample-divergence.png"],
      ["sample.html", "cue.g10.sample.predict", "g10-sample-predict.png"],
      ["sample.html", "cue.g10.sample.e1", "g10-sample-distance.png"],
      ["sample.html", "cue.g10.sample.e1.spread", "g10-sample-crushed.png"],
      ["sample.html", "cue.g10.sample.formula", "g10-sample-formula.png"],
      ["card.html", "cue.g10.card", "g10-card.png"],
    ];
    let previous = "";
    for (const [file, cue, name] of shots) {
      if (file !== previous) {
        await page.goto(`http://127.0.0.1:${server.port}/scenes/g10/${file}`, { waitUntil: "load" });
        await page.evaluate(() => document.fonts.ready);
        previous = file;
      }
      const first = await capture(page, cue);
      await page.evaluate((id) => window.seek(window.__scene.cue(id) + 1), cue);
      const second = await capture(page, cue);
      assert.equal(first.equals(second), true, cue);
      assert.equal(pngSize(first).width, 1920);
      assert.equal(pngSize(first).height, 1080);
      await writeFile(join(dir, name), first);
    }
    if (process.env.G10_ARTIFACTS_DIR) {
      await mkdir(process.env.G10_ARTIFACTS_DIR, { recursive: true });
      for (const [, , name] of shots) {
        await copyFile(join(dir, name), join(process.env.G10_ARTIFACTS_DIR, name));
      }
    }
  } finally {
    const closing = [server.close()];
    if (browser) closing.push(browser.close());
    if (dir) closing.push(rm(dir, { recursive: true, force: true }));
    const results = await Promise.allSettled(closing);
    const rejected = results.find((result) => result.status === "rejected");
    if (rejected?.status === "rejected") throw rejected.reason;
  }
});

async function capture(page, cue) {
  await page.evaluate((id) => window.seek(window.__scene.cue(id)), cue);
  return page.screenshot({ type: "png", animations: "disabled" });
}

function pngSize(buffer) {
  return { width: buffer.readUInt32BE(16), height: buffer.readUInt32BE(20) };
}
