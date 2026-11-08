import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { aligner, ecrireWav, segments } from "../kit-voix/aligner.mjs";

const here = dirname(fileURLToPath(import.meta.url));

test("un écart dans 12 % donne atempo, au-delà le repère bouge", () => {
  const phrases = [
    { id: "a", cue: "start", duration: 1 },
    { id: "b", cue: "show", duration: 2 },
  ];
  const prises = [
    { start: 0.2, duration: 1.1 },
    { start: 1.6, duration: 1 },
  ];
  const plan = aligner(phrases, prises);
  assert.equal(plan[0].action, "atempo");
  assert.equal(plan[0].atempo, 1.1);
  assert.ok(plan[0].atempo <= 1.12);
  assert.equal(plan[1].action, "reminutage");
  assert.equal(plan[1].at, 1.6);
  assert.equal(plan[1].cue, "show");
  assert.equal("speed" in plan[1], false);
});

test("les silences découpent la prise", () => {
  const rate = 8000;
  const samples = signal(rate);
  const found = segments(samples, rate);
  assert.equal(found.length, 2);
  assert.ok(Math.abs(found[0].duration - 1) < 0.05);
  assert.ok(found[1].start > 1.2);
});

test("la commande de changement n'ouvre pas le réseau", async () => {
  const dir = await mkdtemp(join(tmpdir(), "kit-"));
  const manifest = join(dir, "manifeste.json");
  const sortie = join(dir, "nouveau.json");
  await writeFile(
    manifest,
    JSON.stringify({
      reference_id: "536d3a5e000945adb7038665781a4aca",
      paragraphs: [{ id: "ouverture", text: "The field flips.", cues: ["start"] }],
    }),
  );
  const result = spawnSync(
    process.execPath,
    [
      "--import",
      join(here, "bloquer-reseau.mjs"),
      join(here, "../kit-voix/changer.mjs"),
      "--manifest",
      manifest,
      "--vers",
      "0123456789abcdef0123456789abcdef",
      "--cache",
      dir,
      "--ecrire",
      sortie,
    ],
    { encoding: "utf8" },
  );
  assert.equal(result.status, 0, result.stderr);
  const plan = JSON.parse(result.stdout);
  assert.equal(plan.requests, 0);
  assert.equal(plan.paragraphs[0].stale, true);
  const written = JSON.parse(await readFile(sortie, "utf8"));
  assert.deepEqual(written.paragraphs[0].cues, ["start"]);
  assert.equal(written.reference_id, "0123456789abcdef0123456789abcdef");
});

test("l'aligneur lit un wav", async () => {
  const dir = await mkdtemp(join(tmpdir(), "wav-"));
  const wav = join(dir, "prise.wav");
  const phrases = join(dir, "phrases.json");
  const rate = 8000;
  await ecrireWav(wav, signal(rate), rate);
  await writeFile(
    phrases,
    JSON.stringify([
      { id: "a", cue: "start", duration: 1 },
      { id: "b", cue: "show", duration: 1 },
    ]),
  );
  const result = spawnSync(
    process.execPath,
    [join(here, "../kit-voix/aligner.mjs"), "--wav", wav, "--phrases", phrases],
    { encoding: "utf8" },
  );
  assert.equal(result.status, 0, result.stderr);
  const plan = JSON.parse(result.stdout);
  assert.equal(plan.length, 2);
  assert.equal(plan[0].action, "atempo");
  assert.equal(plan[1].cue, "show");
});

function signal(rate) {
  const samples = new Float64Array(rate * 2.4);
  fill(samples, rate, 0, 1, 220);
  fill(samples, rate, 1.4, 2.4, 330);
  return samples;
}

function fill(samples, rate, start, end, freq) {
  for (let index = Math.round(start * rate); index < Math.round(end * rate); index += 1) {
    samples[index] = 0.25 * Math.sin((2 * Math.PI * freq * index) / rate);
  }
}
