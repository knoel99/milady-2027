import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { copyFile, mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { ajuster } from "../pilote.mjs";
import { preparer } from "../parole.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "../..");
const tts = join(here, "../tts.mjs");
const fictif = join(here, "../doubles/fish-langue.mjs");
const cle = "poisson-cle-9f3a";

const EXTRA = `    {
      "id": "cue.g10.classes.bar",
      "lang": "en",
      "audio": null,
      "status": "HOLD",
      "reason": "NE-PAS-TOUCHER"
    }`;

test("un beat plus long que son créneau échoue au lieu d'accélérer", () => {
  assert.throws(() => ajuster(36.86, 35), { code: "atempo" });
  assert.throws(() => ajuster(38.45, 35), { code: "atempo" });
  assert.throws(() => ajuster(42.48, 42), { code: "atempo" });
  assert.throws(() => ajuster(40.07, 40), { code: "atempo" });
});

test("les horloges en et fr couvrent les beats trop longs", async () => {
  for (const lang of ["en", "fr"]) {
    const chapitre = preparer(await readFile(join(root, "narration", lang, "g10.md"), "utf8"), lang);
    const slots = Object.fromEntries(chapitre.beats.map((beat) => [beat.id, beat.slot]));
    assert.equal(slots["g10.law"], 39);
    assert.equal(slots["g10.hard"], 43);
    assert.equal(slots["g10.sample"], 41);
  }
});

test("le rendu garde la langue de chaque piste et les créneaux qu'il ne possède pas", async () => {
  const dir = await mkdtemp(join(tmpdir(), "langue-"));
  const cache = join(dir, "cache");
  const stats = join(dir, "STATS.md");
  const creneaux = join(dir, "cues.json");
  const sortie = join(dir, "pilote.m4a");
  const original = await readFile(join(root, "scenes/g10/cues.json"), "utf8");
  const avecExtra = original.replace(
    "\n  ]\n}",
    `,\n${EXTRA}\n  ],\n  "garde": "oui"\n}`,
  );
  assert.equal(avecExtra.includes(EXTRA), true);
  await writeFile(creneaux, avecExtra);
  const env = { FISH_API_KEY: cle };
  const anglais = lancer(["--chapter", "g10", "--lang", "en", "--cache", cache, "--stats", stats], env);
  assert.equal(anglais.status, 0, anglais.stderr);
  const cheminEn = (await manifeste(cache, "en")).find((item) => item.id === "cue.g10.classes.show").fichier;
  const copieEn = join(dir, "en-ouverture.wav");
  await copyFile(cheminEn, copieEn);
  const freqEn = await frequenceFichier(copieEn);
  const francais = lancer(["--chapter", "g10", "--lang", "fr", "--cache", cache, "--stats", stats], env);
  assert.equal(francais.status, 0, francais.stderr);
  const cheminFr = (await manifeste(cache, "fr")).find((item) => item.id === "cue.g10.classes.show").fichier;
  const copieFr = join(dir, "fr-ouverture.wav");
  await copyFile(cheminFr, copieFr);
  const freqFr = await frequenceFichier(copieFr);
  const partage = join(dir, "partage.mp3");
  await copyFile(copieFr, partage);
  for (const lang of ["en", "fr"]) {
    const document = JSON.parse(await readFile(join(cache, `g10-${lang}.json`), "utf8"));
    for (const item of document.paragraphes) item.fichier = partage;
    await writeFile(join(cache, `g10-${lang}.json`), `${JSON.stringify(document)}\n`);
  }
  const rendu = lancer(
    ["--chapter", "g10", "--rendre", "--cache", cache, "--sortie", sortie, "--creneaux", creneaux],
    {},
  );
  assert.equal(rendu.status, 0, rendu.stderr);
  const freq0 = await frequencePiste(sortie, "0:a:0");
  const freq1 = await frequencePiste(sortie, "0:a:1");
  const apres = await readFile(creneaux, "utf8");
  const problemes = [];
  if (Math.abs(freq0 - freqEn) > 40) problemes.push(`en ${freq0} != ${freqEn}`);
  if (Math.abs(freq1 - freqFr) > 40) problemes.push(`fr ${freq1} != ${freqFr}`);
  if (Math.abs(freq0 - freq1) < 100) problemes.push(`pistes ${freq0} et ${freq1}`);
  if (!apres.includes(EXTRA)) problemes.push("creneau efface");
  if (!apres.includes('"garde": "oui"')) problemes.push("cle effacee");
  assert.equal(anglais.stdout.includes(cle), false);
  assert.equal(problemes.length, 0, problemes.join("; "));
});

async function manifeste(cache, lang) {
  const document = JSON.parse(await readFile(join(cache, `g10-${lang}.json`), "utf8"));
  return document.paragraphes;
}

function lancer(args, env) {
  return spawnSync(process.execPath, ["--import", fictif, tts, ...args], {
    encoding: "utf8",
    env: { ...process.env, ...env },
  });
}

async function frequenceFichier(path) {
  const buffer = await readFile(path);
  const samples = [];
  for (let offset = 44; offset + 1 < buffer.length; offset += 2) {
    samples.push(buffer.readInt16LE(offset) / 32768);
  }
  return mesurer(samples, 8000);
}

async function frequencePiste(path, map) {
  const result = spawnSync(
    "ffmpeg",
    ["-v", "error", "-i", path, "-map", map, "-ac", "1", "-ar", "8000", "-t", "0.2", "-f", "f32le", "pipe:1"],
    { maxBuffer: 1_000_000 },
  );
  assert.equal(result.status, 0, result.stderr.toString());
  const samples = [];
  for (let offset = 0; offset + 3 < result.stdout.length; offset += 4) {
    samples.push(result.stdout.readFloatLE(offset));
  }
  return mesurer(samples, 8000);
}

function mesurer(samples, rate) {
  let passages = 0;
  for (let index = 1; index < samples.length; index += 1) {
    const avant = samples[index - 1];
    const courant = samples[index];
    if ((avant <= 0 && courant > 0) || (avant >= 0 && courant < 0)) passages += 1;
  }
  return (passages / 2) / (samples.length / rate);
}
