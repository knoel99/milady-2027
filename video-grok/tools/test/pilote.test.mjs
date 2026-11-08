import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { cleCache } from "../cache.mjs";
import { ecrireWav } from "../kit-voix/aligner.mjs";
import { VOIX, preparer } from "../parole.mjs";
import {
  ajuster,
  argumentsPiste,
  brancher,
  calendrier,
  dureeFichier,
  ecrireManifeste,
  horloges,
  lireScenes,
  rapport,
  rendre,
} from "../pilote.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "../..");
const tts = join(here, "../tts.mjs");

test("un audio plus court que le créneau tient, et un audio plus long échoue", () => {
  assert.equal(ajuster(4, 8).action, "tient");
  assert.equal(ajuster(4, 8).atempo, null);
  assert.equal(ajuster(4, 8).speed, 1);
  assert.throws(() => ajuster(8.5, 8), { code: "atempo" });
  assert.throws(() => ajuster(10, 8), { code: "atempo" });
  const args = argumentsPiste([{ fichier: "a.wav", at: 1.5, atempo: null }], 2);
  assert.equal(args.join(" ").includes("atempo"), false);
  assert.equal(args.join(" ").includes("adelay=1500"), true);
});

test("chaque beat de g10 compare sa durée audio à son créneau, sur le même repère", async () => {
  const scenes = await lireScenes(join(root, "scenes/g10"));
  const temps = horloges(scenes);
  const anglais = preparer(await readFile(join(root, "narration/en/g10.md"), "utf8"), "en");
  const francais = preparer(await readFile(join(root, "narration/fr/g10.md"), "utf8"), "fr");
  const calEn = calendrier(anglais, temps);
  const calFr = calendrier(francais, temps);
  assert.deepEqual(
    calEn.beats.map((beat) => [beat.id, beat.slot]),
    [
      ["g10.classes", 45],
      ["g10.hard", 43],
      ["g10.sym", 30],
      ["g10.law", 39],
      ["g10.sample", 41],
      ["g10.bias", 25],
      ["g10.close", 17],
      ["g10.card", 8],
    ],
  );
  const sample = JSON.parse(await readFile(join(root, "scenes/g10/sample.json"), "utf8"));
  const predict = sample.cues.find((cue) => cue.id === "cue.g10.sample.predict").at;
  for (const [gauche, droite] of calEn.beats.map((beat, index) => [beat, calFr.beats[index]])) {
    assert.equal(gauche.debut, droite.debut);
    for (const paragraphe of gauche.paragraphes) {
      const jumeau = droite.paragraphes.find((item) => item.id === paragraphe.id);
      assert.equal(jumeau.at, paragraphe.at, paragraphe.id);
    }
  }
  const echantillon = calEn.beats.find((beat) => beat.id === "g10.sample");
  const question = echantillon.paragraphes.find((paragraphe) => paragraphe.id === "cue.g10.sample.predict");
  assert.equal(question.at, echantillon.debut + predict);
  const loi = calEn.beats.find((beat) => beat.id === "g10.law");
  assert.equal(loi.paragraphes[1].id, "cue.g10.law.caveat");
  assert.equal(loi.paragraphes[1].at, loi.debut + loi.slot / 2);

  const dir = await mkdtemp(join(tmpdir(), "duree-"));
  const wav = join(dir, "note.wav");
  await ecrireWav(wav, note(8000, 0.4), 8000);
  const mesure = await dureeFichier(wav);
  assert.ok(Math.abs(mesure - 0.4) < 0.05, `${mesure}`);
  const durees = new Map(anglais.paragraphes.map((paragraphe) => [paragraphe.id, mesure]));
  for (const beat of rapport(calEn, durees)) {
    assert.ok(beat.audio <= beat.slot, `${beat.id} ${beat.audio} ${beat.slot}`);
    assert.equal(beat.action, "tient");
    assert.equal(beat.speed, 1);
    for (const cue of beat.cues) {
      assert.ok(cue.audio <= cue.fenetre + 1e-6, `${cue.id} ${cue.audio} ${cue.fenetre}`);
      assert.equal(cue.speed, 1);
    }
  }
});

test("le rendu aligne les deux langues et branche le caveat qui tient", async () => {
  const dir = await mkdtemp(join(tmpdir(), "pilote-"));
  const wav = join(dir, "note.wav");
  await ecrireWav(wav, note(8000, 0.3), 8000);
  const scenes = await lireScenes(join(root, "scenes/g10"));
  const temps = horloges(scenes);
  const fichiers = {};
  for (const lang of ["en", "fr"]) {
    const markdown = await readFile(join(root, "narration", lang, "g10.md"), "utf8");
    const chapitre = preparer(markdown, lang);
    const paragraphes = chapitre.paragraphes.map((paragraphe) => ({
      id: paragraphe.id,
      cle: cleCache({ text: paragraphe.texte, referenceId: VOIX }),
      fichier: wav,
    }));
    await ecrireManifeste(join(dir, `g10-${lang}.json`), { chapter: "g10", lang, paragraphes });
    fichiers[lang] = chapitre;
  }
  const creneaux = join(dir, "cues.json");
  await writeFile(creneaux, await readFile(join(root, "scenes/g10/cues.json")));
  const sortie = join(dir, "pilote.m4a");
  const resultat = spawnSync(
    process.execPath,
    [
      "--import",
      join(here, "bloquer-reseau.mjs"),
      tts,
      "--chapter",
      "g10",
      "--rendre",
      "--cache",
      dir,
      "--sortie",
      sortie,
      "--creneaux",
      creneaux,
      "--scenes",
      join(root, "scenes/g10"),
    ],
    { encoding: "utf8" },
  );
  assert.equal(resultat.status, 0, resultat.stderr);
  for (const beat of ["g10.classes", "g10.hard", "g10.sym", "g10.law", "g10.sample", "g10.bias", "g10.close", "g10.card"]) {
    assert.match(resultat.stdout, new RegExp(`en ${beat}: audio .+ slot .+ tient`));
    assert.match(resultat.stdout, new RegExp(`fr ${beat}: audio .+ slot .+ tient`));
  }
  const probe = spawnSync(
    "ffprobe",
    ["-v", "error", "-show_entries", "stream=codec_type", "-of", "json", sortie],
    { encoding: "utf8" },
  );
  assert.equal(probe.status, 0, probe.stderr);
  const streams = JSON.parse(probe.stdout).streams;
  assert.deepEqual(
    streams.map((stream) => stream.codec_type),
    ["audio", "audio"],
  );
  const document = JSON.parse(await readFile(creneaux, "utf8"));
  assert.equal(document.slots.length, 2);
  for (const slot of document.slots) {
    assert.equal(slot.id, "cue.g10.law.caveat");
    assert.equal(slot.status, "READY");
    assert.equal(slot.audio, wav);
  }
  const direct = await rendre({
    en: { chapitre: fichiers.en, fichiers: Object.fromEntries(fichiers.en.paragraphes.map((item) => [item.id, wav])) },
    fr: { chapitre: fichiers.fr, fichiers: Object.fromEntries(fichiers.fr.paragraphes.map((item) => [item.id, wav])) },
    horloges: temps,
    sortie: join(dir, "direct.m4a"),
  });
  const depart = direct.en.find((beat) => beat.id === "g10.law").cues.find((cue) => cue.id === "cue.g10.law.caveat").at;
  const autre = direct.fr.find((beat) => beat.id === "g10.law").cues.find((cue) => cue.id === "cue.g10.law.caveat").at;
  assert.equal(depart, autre);
  const etroit = brancher(
    { slots: [{ id: "cue.g10.card", lang: "en", audio: null, status: "PENDING" }] },
    { en: { "cue.g10.card": wav } },
    { en: [{ cues: [{ id: "cue.g10.card", action: "reminutage" }] }] },
  );
  assert.equal(etroit.slots[0].status, "PENDING");
  assert.equal(etroit.slots[0].audio, null);
});

function note(rate, seconds) {
  const samples = new Float64Array(Math.round(rate * seconds));
  for (let index = 0; index < samples.length; index += 1) {
    samples[index] = 0.2 * Math.sin((2 * Math.PI * 440 * index) / rate);
  }
  return samples;
}
