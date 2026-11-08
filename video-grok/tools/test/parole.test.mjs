import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { REGLAGES } from "../cache.mjs";
import {
  INDICATION,
  PAUSE_LONGUE,
  TERMES,
  VOIX,
  corps,
  epingler,
  estimer,
  filtreAtempo,
  preparer,
} from "../parole.mjs";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");

test("le corps suit FISH.md et ne baisse pas speed", () => {
  const charge = corps("Une phrase.");
  assert.equal(charge.text, "Une phrase.");
  assert.equal(charge.reference_id, VOIX);
  assert.equal(charge.reference_id, "536d3a5e000945adb7038665781a4aca");
  assert.equal(charge.temperature, 0.1);
  assert.equal(charge.format, "mp3");
  assert.equal(charge.mp3_bitrate, 192);
  assert.equal(charge.sample_rate, 44100);
  assert.equal(charge.latency, "normal");
  assert.equal(charge.normalize, true);
  assert.equal(charge.condition_on_previous_chunks, true);
  assert.deepEqual(charge.prosody, { speed: 1, normalize_loudness: true });
  assert.equal("model" in charge, false);
  assert.equal("references" in charge, false);
  assert.equal(REGLAGES.prosody.speed >= 1, true);
  assert.throws(() => corps("a", { ...REGLAGES, prosody: { speed: 0.5, normalize_loudness: true } }), { code: "speed" });
  assert.equal(filtreAtempo(0.8), "atempo=0.8");
  assert.equal(corps("a").prosody.speed, 1);
});

test("les termes sont ceux de FISH.md, et une chaîne absente est signalée", async () => {
  const ligne = (await readFile(join(root, "FISH.md"), "utf8")).split("\n").find((row) => row.startsWith("MilaDy"));
  const attendus = ligne
    .replace("(prononciation française)", "")
    .replace(/ seulement si.*/, "")
    .split(",")
    .map((terme) => terme.trim())
    .filter(Boolean);
  assert.deepEqual(new Set(TERMES), new Set(attendus));
  const vide = epingler("The field flips.", "en");
  assert.deepEqual(vide.manquantes, []);
  assert.equal(vide.texte, "The field flips.");
  const rm = epingler("The Rm grows.", "en");
  assert.deepEqual(rm.manquantes, [{ terme: "Rm", raison: "non sourcée" }]);
  assert.equal(rm.texte.includes("<|phoneme_start|>"), false);
  const gissinger = epingler("le modèle de Gissinger tient.", "fr", { fr: { Gissinger: "ZH IY0" } });
  assert.equal(gissinger.texte, "le modèle de <|phoneme_start|>ZH IY0<|phoneme_end|> tient.");
  const bloque = epingler("Glatzmaier reste hors champ.", "en", { en: { Glatzmaier: "AA1" } });
  assert.deepEqual(bloque.manquantes, [{ terme: "Glatzmaier", raison: "revue science" }]);
  assert.equal(bloque.texte.includes("phoneme"), false);
});

test("g10 envoie un paragraphe par repère parlé, avec une seule indication", async () => {
  for (const lang of ["en", "fr"]) {
    const markdown = await readFile(join(root, "narration", lang, "g10.md"), "utf8");
    const chapitre = preparer(markdown, lang);
    const estimation = estimer(chapitre);
    const parles = markdown.split("\n").filter((ligne) => ligne.trim() === "role: spoken").length;
    assert.equal(estimation.requetes, parles);
    assert.equal(estimation.requetes, 11);
    assert.deepEqual(estimation.manquantes, []);
    assert.equal(chapitre.paragraphes.some((paragraphe) => paragraphe.id === "cue.g10.sample.formula"), false);
    assert.equal(chapitre.paragraphes.some((paragraphe) => paragraphe.texte.includes("Hypothesis:")), false);
    assert.equal(chapitre.paragraphes.some((paragraphe) => /<emphasis>|<stress>/.test(paragraphe.texte)), false);
    const pauses = chapitre.paragraphes.filter((paragraphe) => paragraphe.texte.startsWith(PAUSE_LONGUE));
    const indications = chapitre.paragraphes.filter((paragraphe) => paragraphe.texte.startsWith(INDICATION));
    assert.equal(indications.length, 1);
    assert.equal(pauses.length, chapitre.beats.filter((beat) => beat.paragraphes.length > 0).length - 1);
    const caveat = chapitre.paragraphes.find((paragraphe) => paragraphe.id === "cue.g10.law.caveat");
    const question = chapitre.paragraphes.find((paragraphe) => paragraphe.id === "cue.g10.sample.predict");
    assert.equal(caveat.texte.startsWith(PAUSE_LONGUE), false);
    assert.equal(caveat.texte.includes(INDICATION), false);
    assert.equal(question.texte.includes(PAUSE_LONGUE), false);
    assert.equal(question.texte.includes("pause:"), false);
    const brut = chapitre.paragraphes.reduce((somme, paragraphe) => somme + paragraphe.brut.length, 0);
    const extra = INDICATION.length + 1 + pauses.length * (PAUSE_LONGUE.length + 1);
    assert.equal(estimation.caracteres, brut + extra);
  }
  const anglais = preparer(await readFile(join(root, "narration/en/g10.md"), "utf8"), "en");
  const francais = preparer(await readFile(join(root, "narration/fr/g10.md"), "utf8"), "fr");
  assert.equal(anglais.paragraphes[0].texte.includes("A constraint can sit in four places."), true);
  assert.equal(francais.paragraphes[0].texte.includes("Une contrainte peut occuper quatre places."), true);
  const carte = francais.paragraphes.find((paragraphe) => paragraphe.id === "cue.g10.card");
  assert.equal(carte.texte.includes("Faut-il ancrer"), true);
  assert.equal(carte.texte.includes("Must stationarity"), false);
  assert.deepEqual(
    anglais.paragraphes.map((paragraphe) => paragraphe.id),
    francais.paragraphes.map((paragraphe) => paragraphe.id),
  );
});
