import assert from "node:assert/strict";
import test from "node:test";
import { createClock, randomAt } from "./clock.js";
import { loadScene, viewAt, SceneError, cueTime } from "./scene.js";
import demo from "./demo/scene.json" with { type: "json" };

const scene = loadScene(demo);

test("deux lectures du même instant donnent la même vue", () => {
  const left = viewAt(scene, cueTime(scene, "show"));
  const right = viewAt(scene, cueTime(scene, "show"));
  assert.deepEqual(left, right);
  assert.notDeepEqual(viewAt(scene, cueTime(scene, "predict")), left);
});

function tirage(frame, count) {
  const random = randomAt(scene.seed, frame);
  return Array.from({ length: count }, () => random());
}

test("la graine et l'image fixent le hasard", () => {
  const frame = viewAt(scene, 1).frame;
  assert.deepEqual(tirage(frame, 4), tirage(frame, 4));
  assert.notDeepEqual(tirage(frame, 4), tirage(frame + 1, 4));
});

test("l'horloge virtuelle ne dépend pas du mur", () => {
  const clock = createClock(30);
  const first = clock.seek(2.5);
  const second = clock.seek(2.5);
  assert.deepEqual(first, second);
  assert.equal(first.millis, 2500);
  assert.equal(first.performanceMillis, 2500);
  assert.equal(first.frame, 75);
  const step = clock.seek(1 / 30);
  assert.equal(step.millis, 33);
  assert.equal(step.performanceMillis, 1000 / 30);
  assert.equal(step.frame, 1);
});

test("la carte question dure 8 s et disparaît au close", () => {
  const card = viewAt(scene, cueTime(scene, "card"));
  const close = viewAt(scene, cueTime(scene, "close"));
  assert.equal(cueTime(scene, "card-end") - cueTime(scene, "card"), 8);
  assert.equal(card.questionCard.sentence, "What should a shared stage prove first?");
  assert.equal(card.questionCard.badge, "PLANNED");
  assert.equal(card.chapterCard, null);
  assert.equal(close.questionCard, null);
  assert.equal(close.chapterCard, null);
  assert.equal(close.transition.frames, 8);
  assert.equal(close.transition.to, "blueprint");
  assert.notEqual(close.transition.from, close.transition.to);
});

test("la carte de chapitre dure 4 s et n'est pas la transition", () => {
  const start = viewAt(scene, cueTime(scene, "start"));
  const end = viewAt(scene, cueTime(scene, "chapter-end"));
  assert.equal(cueTime(scene, "chapter-end") - cueTime(scene, "start"), 4);
  assert.equal(start.chapterCard.title, "Shared stage");
  assert.equal(start.transition, null);
  assert.equal(end.chapterCard, null);
});

test("PROVED et MEASURED sont deux pastilles", () => {
  const show = viewAt(scene, cueTime(scene, "show"));
  const kinds = show.badges.map((badge) => badge.kind);
  assert.deepEqual(kinds, ["PROVED", "MEASURED"]);
  assert.equal(show.badges.filter((badge) => badge.primary).length, 1);
  assert.deepEqual(show.bars.rows.map((row) => row.name), ["A", "B", "C"]);
  assert.equal(show.bars.seedLabel, "two seeds");
  assert.equal(show.bars.floor.label, "noise floor");
  assert.equal(show.bars.log, true);
});

test("le calque allume le terme du repère", () => {
  const formula = viewAt(scene, cueTime(scene, "formula"));
  const caveat = viewAt(scene, cueTime(scene, "caveat"));
  assert.deepEqual(formula.formula.terms.map((term) => term.lit), [true, false]);
  assert.deepEqual(caveat.formula.terms.map((term) => term.lit), [false, true]);
  assert.equal(formula.subtitle.text.includes("\\"), false);
  assert.equal(formula.chapterCard, null);
});

test("l'emplacement en attente ne dessine pas une mesure", () => {
  const waiting = viewAt(scene, cueTime(scene, "waiting"));
  assert.equal(waiting.waiting.label, "not yet run");
  assert.equal(waiting.bars, null);
  assert.equal(waiting.matter, "blueprint");
  assert.equal(waiting.badges[0].kind, "PLANNED");
});

test("une carte question de 20 s est refusée", () => {
  const raw = structuredClone(demo);
  raw.cues.push({ id: "too-late", at: 20 });
  raw.layers.push({
    kind: "question-card",
    from: "start",
    until: "too-late",
    sentence: "Too long for a card.",
    class: "A",
    badge: "PLANNED",
  });
  assert.throws(() => loadScene(raw), (error) => error instanceof SceneError && error.code === "carte-question");
});

test("une transition qui n'a pas 8 images est refusée", () => {
  const raw = structuredClone(demo);
  raw.layers.find((layer) => layer.kind === "transition").frames = 20;
  assert.throws(() => loadScene(raw), (error) => error instanceof SceneError && error.code === "transition");
});

test("l'attente ne peut pas annoncer un résultat", () => {
  const raw = structuredClone(demo);
  raw.layers.find((layer) => layer.kind === "waiting").label = "we obtained";
  const loaded = loadScene(raw);
  assert.equal(viewAt(loaded, cueTime(loaded, "waiting")).waiting.label, "not yet run");
});

test("une pastille mixte est refusée", () => {
  const raw = structuredClone(demo);
  raw.layers.find((layer) => layer.badge === "PROVED").badge = "MEASURED+CONTEXT";
  assert.throws(() => loadScene(raw), (error) => error instanceof SceneError && error.code === "pastille");
});

test("un sous-titre TeX est refusé", () => {
  const raw = structuredClone(demo);
  raw.layers.find((layer) => layer.kind === "subtitle").text = "KL = \\infty";
  assert.throws(() => loadScene(raw), (error) => error instanceof SceneError && error.code === "sous-titre");
});
