import assert from "node:assert/strict";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { appliquer, cleCache, ecrire, lire, planifier, REGLAGES } from "../cache.mjs";
import { changer } from "../kit-voix/changer.mjs";

const manifest = {
  reference_id: "536d3a5e000945adb7038665781a4aca",
  paragraphs: [{ id: "ouverture", text: "The field flips.", cues: ["start", "show"] }],
};

test("le cache distingue le texte, la voix et les réglages", () => {
  const base = { text: manifest.paragraphs[0].text, referenceId: manifest.reference_id };
  const key = cleCache(base);
  assert.equal(cleCache(base), key);
  assert.notEqual(cleCache({ ...base, referenceId: "0123456789abcdef0123456789abcdef" }), key);
  assert.notEqual(cleCache({ ...base, settings: { ...REGLAGES, temperature: 0.2 } }), key);
});

test("une clé écrite deux fois garde le premier fichier", async () => {
  const dir = await mkdtemp(join(tmpdir(), "cache-"));
  const key = cleCache({ text: "a", referenceId: manifest.reference_id });
  assert.equal(await lire(dir, key), null);
  await ecrire(dir, key, Buffer.from("premier"));
  const second = await ecrire(dir, key, Buffer.from("second"));
  assert.equal(second.toString(), "premier");
  assert.equal((await lire(dir, key)).toString(), "premier");
});

test("changer de voix n'appelle pas le réseau et garde les repères", async () => {
  const dir = await mkdtemp(join(tmpdir(), "cache-"));
  const next = "0123456789abcdef0123456789abcdef";
  const plan = await changer({ manifest, referenceId: next, cacheDir: dir });
  assert.equal(plan.requests, 0);
  assert.equal(plan.paragraphs[0].stale, true);
  assert.deepEqual(plan.paragraphs[0].cues, ["start", "show"]);
  const rewritten = appliquer(manifest, plan);
  assert.equal(rewritten.reference_id, next);
  assert.deepEqual(rewritten.paragraphs[0].cues, manifest.paragraphs[0].cues);
  assert.equal(rewritten.paragraphs[0].text, manifest.paragraphs[0].text);

  await ecrire(dir, plan.paragraphs[0].after, Buffer.from("audio"));
  const again = planifier(manifest, next, new Set([plan.paragraphs[0].after]));
  assert.equal(again.paragraphs[0].stale, false);
  assert.equal(again.requests, 0);
});
