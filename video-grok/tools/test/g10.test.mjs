import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { copyFile, mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { loadScene, viewAt, cueTime } from "../../engine/scene.js";
import { ouvrir } from "../navigateur.mjs";
import { servir } from "../servir.mjs";
import classesRaw from "../../scenes/g10/classes.json" with { type: "json" };
import hardRaw from "../../scenes/g10/hard.json" with { type: "json" };
import symRaw from "../../scenes/g10/sym.json" with { type: "json" };
import lawRaw from "../../scenes/g10/law.json" with { type: "json" };
import sampleRaw from "../../scenes/g10/sample.json" with { type: "json" };
import biasRaw from "../../scenes/g10/bias.json" with { type: "json" };
import closeRaw from "../../scenes/g10/close.json" with { type: "json" };
import cardRaw from "../../scenes/g10/card.json" with { type: "json" };
import slots from "../../scenes/g10/cues.json" with { type: "json" };

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "../..");
const repo = join(root, "..");
const classes = loadScene(classesRaw);
const hard = loadScene(hardRaw);
const sym = loadScene(symRaw);
const law = loadScene(lawRaw);
const sample = loadScene(sampleRaw);
const bias = loadScene(biasRaw);
const close = loadScene(closeRaw);
const card = loadScene(cardRaw);
const scenes = [classes, hard, sym, law, sample, bias, close, card];
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

test("la clôture montre les deux propositions l'une après l'autre", () => {
  const zero = viewAt(close, 0);
  const ancrage = viewAt(close, cueTime(close, "cue.g10.close.anchor"));
  assert.equal(zero.subtitle.text, "The constraint has zero probability of being exactly zero");
  assert.equal(zero.axis, null);
  assert.equal(ancrage.subtitle.text, "Anchoring limits how far fine-tuning can move from the starting model.");
  assert.equal(ancrage.subtitle.text === zero.subtitle.text, false);
  assert.equal(ancrage.axis.ticks.some((tick) => tick.value === "witness"), true);
  assert.equal(ancrage.axis.param, "second run, same anchor, weight 0");
});

test("la loi sépare le test de la référence d'entraînement", () => {
  const essai = viewAt(law, 0);
  assert.equal(essai.bars.scaleLabel, "log scale");
  assert.ok(essai.bars.ticks.length >= 2);
  assert.deepEqual(
    essai.bars.rows.map((row) => row.label),
    ["0.699", "2.52"],
  );
  assert.match(essai.bars.title, /test parameters/);
  const entrainement = viewAt(law, cueTime(law, "cue.g10.law.floor"));
  assert.deepEqual(
    entrainement.bars.rows.map((row) => row.label),
    ["0.0304"],
  );
  assert.match(entrainement.bars.title, /Subsampling reference/);
  assert.match(entrainement.bars.title, /training parameters/);
  assert.equal(entrainement.bars.scaleLabel, "log scale");
  const dur = viewAt(hard, cueTime(hard, "cue.g10.hard.flow"));
  assert.equal(dur.bars.scaleLabel, "log scale");
  assert.ok(dur.bars.ticks.length >= 2);
  const dissipation = sample.layers.find((layer) => layer.title === "Ratio of dissipation standard deviations");
  assert.equal(dissipation.log, true);
  assert.equal(dissipation.rows.some((row) => row.label === "8.64e-04"), true);
});

test("les cinq scènes du pilote durent leur créneau", () => {
  assert.deepEqual(
    [hard, sym, law, bias, close].map((scene) => [scene.id, scene.duration]),
    [
      ["g10.hard", 43],
      ["g10.sym", 30],
      ["g10.law", 39],
      ["g10.bias", 25],
      ["g10.close", 17],
    ],
  );
  assert.equal(cueTime(law, "cue.g10.law.caveat"), 19.5);
  assert.equal(viewAt(hard, cueTime(hard, "cue.g10.hard.flow")).bars.rows.map((row) => row.name).join(","), "V0,V1 u,V1 B,V2,V4,V3");
  assert.equal(viewAt(law, 0).badges.some((badge) => badge.kind === "MEASURED" && badge.primary), true);
  assert.equal(viewAt(sym, 0).badges.some((badge) => badge.kind === "PROVED" && badge.primary), true);
  assert.equal(viewAt(bias, 0).bars.schematic, true);
  assert.equal(viewAt(close, 0).badges.length, 0);
  assert.equal(viewAt(close, 0).questionCard, null);
});

test("les sous-titres sont des extraits du script, et la carte est q.g10", () => {
  for (const scene of scenes) {
    for (const layer of scene.layers) {
      if (layer.kind !== "subtitle") continue;
      if (layer.text === "The constraint has zero probability of being exactly zero") continue;
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
  "E2 est bidimensionnel et forcé. Une seule graine aléatoire testée. Valeurs intermédiaires dans la plage d’entraînement. Pas une dynamo.";

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
  const chapitre = await readFile(join(root, "narration/fr/g10.md"), "utf8");
  assert.equal(parole(chapitre, "cue.g10.law.caveat"), CAVEAT_FR);
  const tree = await readFile(join(root, "scenes/g10/cues.json"), "utf8");
  assert.equal(tree.includes("One seed"), false);
  assert.equal(tree.includes("dynamo"), false);
});

test("les deux créneaux du caveat disent les trois limites", async () => {
  const points = {
    en: [/One seed/, /interpolation/, /not a dynamo/],
    fr: [/Une seule graine aléatoire/, /[Vv]aleurs intermédiaires dans la plage d’entraînement/, /[Pp]as une dynamo/],
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

test("le beat g10.law avec le caveat français reste à 156 mots par minute", async () => {
  const show = parole(narration, "cue.g10.law.show");
  const caveat = parole(
    await readFile(join(root, "narration/fr/g10.law.caveat.md"), "utf8"),
    "cue.g10.law.caveat",
  );
  const duration = duree(narration, "g10.law");
  const { count, rate } = motsDits(`${show}\n${caveat}`, duration);
  assert.equal(duration, 39);
  assert.ok(count <= 91, `${count} mots dits`);
  assert.ok(rate <= 156, `${rate} mots/min`);
});

test("chaque beat g10 en français entier reste à 156 mots par minute", async () => {
  const chapter = await readFile(join(root, "narration/fr/g10.md"), "utf8");
  const beats = beatsOraux(chapter);
  assert.deepEqual(
    beats.map((beat) => beat.id),
    ["g10.classes", "g10.hard", "g10.sym", "g10.law", "g10.sample", "g10.bias", "g10.close", "g10.card"],
  );
  const law = beats.find((beat) => beat.id === "g10.law");
  const show = law.cues.find((cue) => cue.id === "cue.g10.law.show");
  const caveat = law.cues.find((cue) => cue.id === "cue.g10.law.caveat");
  assert.equal(show.role, "spoken");
  assert.equal(caveat.role, "spoken");
  assert.equal(caveat.text.join(" "), CAVEAT_FR);
  assert.equal(show.text.join(" ").includes("energy distance"), false);
  for (const beat of beats) {
    const spoken = beat.cues.filter((cue) => cue.role === "spoken");
    const text = spoken.map((cue) => cue.text.join(" ")).join("\n");
    const pause = spoken.reduce((sum, cue) => sum + cue.pause, 0);
    if (beat.id === "g10.law") {
      assert.equal(text.includes(show.text.join(" ")), true);
      assert.equal(text.includes(CAVEAT_FR), true);
      assert.equal(text.includes(parole(narration, "cue.g10.law.show")), false);
    }
    const result = debitFrancais(text, beat.duration, pause);
    assert.ok(result.rate <= 156, `${beat.id}: ${result.count} mots, ${result.rate} mots/min`);
  }
  const spelled = debitFrancais("divergence de 0,408.", 40, 0);
  assert.ok(spelled.count >= 5, `${spelled.count} mots pour 0,408`);
  const tooFast = debitFrancais(Array.from({ length: 100 }, () => "mot").join(" "), 30, 0);
  assert.ok(tooFast.rate > 156, `${tooFast.rate} mots/min`);
  const report = execFileSync("python3", [join(root, "narration/fr/g10-verify.py")], { encoding: "utf8" });
  assert.match(report, /g10\.law:/);
  assert.match(report, /débit ≤ 156/);
});

function beatsOraux(markdown) {
  const beats = [];
  let beat = null;
  let cue = null;
  for (const line of markdown.split(/\r?\n/)) {
    if (line.startsWith("## ")) {
      beat = { id: line.slice(3).trim(), duration: 0, cues: [] };
      beats.push(beat);
      cue = null;
      continue;
    }
    if (line.startsWith("### ")) {
      cue = { id: line.slice(4).trim(), role: "", pause: 0, text: [] };
      beat.cues.push(cue);
      continue;
    }
    if (beat && line.startsWith("duration:")) {
      const [minutes, seconds] = line.slice("duration:".length).trim().split(":");
      beat.duration = Number(minutes) * 60 + Number(seconds);
      continue;
    }
    if (!cue) continue;
    if (line.startsWith("role:")) {
      cue.role = line.slice("role:".length).trim();
      continue;
    }
    if (line.startsWith("pause:")) {
      cue.pause = Number(line.slice("pause:".length).trim().replace(/s$/, ""));
      continue;
    }
    if (line.startsWith("screen:") || line.trim() === "") continue;
    cue.text.push(line.trim());
  }
  return beats;
}

function debitFrancais(text, duration, pause) {
  const out = execFileSync("python3", [join(root, "narration/fr/g10-verify.py"), "--rate"], {
    input: JSON.stringify({ text, duration, pause }),
    encoding: "utf8",
  });
  return JSON.parse(out);
}

function duree(markdown, beatId) {
  const lines = markdown.split(/\r?\n/);
  const start = lines.findIndex((line) => line.trim() === `## ${beatId}`);
  const row = lines.slice(start + 1).find((line) => line.startsWith("duration:"));
  const [minutes, seconds] = row.slice("duration:".length).trim().split(":");
  return Number(minutes) * 60 + Number(seconds);
}

function motsDits(text, duration) {
  const checker = join(root, "narration/en/g07-g11-verify.py");
  const script = `
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("chk", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
payload = json.loads(sys.stdin.read())
said = payload["text"]
count = len(mod.words(mod.expand_spoken(said)))
rate = mod.speech_rate(said, payload["duration"], 0)
print(json.dumps({"count": count, "rate": rate}))
`;
  const out = execFileSync("python3", ["-c", script, checker], {
    input: JSON.stringify({ text, duration }),
    encoding: "utf8",
  });
  return JSON.parse(out);
}

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
    ["hard.html", ["cue.g10.hard.show", "cue.g10.hard.flow", "cue.g10.hard.winner"]],
    ["sym.html", ["cue.g10.sym.show", "cue.g10.sym.weights"]],
    ["law.html", ["cue.g10.law.show", "cue.g10.law.caveat", "cue.g10.law.dynamo"]],
    ["bias.html", ["cue.g10.bias.show", "cue.g10.bias.model"]],
    ["close.html", ["cue.g10.close.show", "cue.g10.close.anchor"]],
    ["card.html", ["cue.g10.card"]],
  ];
  const { browser, page } = await ouvrir(`http://127.0.0.1:${server.port}/scenes/g10/${pages[0][0]}`);
  try {
    for (const [file, cues] of pages) {
      await page.goto(`http://127.0.0.1:${server.port}/scenes/g10/${file}`, { waitUntil: "load" });
      await page.waitForFunction(() => window.__scene);
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
        const minimum = await page.evaluate(() =>
          Number.parseFloat(getComputedStyle(document.documentElement).getPropertyValue("--label-size")),
        );
        const tailles = await page.evaluate(() =>
          [...document.querySelectorAll(".bar-name, .bar-value, .bars-title, .bars-scale, .bars-tick-label, .subtitle, .axis-param, .tick-value")]
            .filter((node) => node.textContent.trim())
            .map((node) => ({
              text: node.textContent.trim(),
              size: Number.parseFloat(getComputedStyle(node).fontSize),
              overflow: node.scrollWidth - node.clientWidth,
            })),
        );
        for (const item of tailles) {
          assert.ok(item.size + 0.5 >= minimum, `${cue} ${item.text} ${item.size}`);
          assert.ok(item.overflow <= 1, `${cue} ${item.text} déborde`);
        }
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
        await page.waitForFunction(() => window.__scene);
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
