import { createHash } from "node:crypto";
import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { join } from "node:path";

export const REGLAGES = Object.freeze({
  model: "drama-3",
  temperature: 0.1,
  format: "mp3",
  mp3_bitrate: 192,
  sample_rate: 44100,
  latency: "normal",
  normalize: true,
  condition_on_previous_chunks: true,
  prosody: Object.freeze({ speed: 1, normalize_loudness: true }),
});

export function cleCache({ text, referenceId, settings = REGLAGES }) {
  const body = canonique({ text, referenceId, settings });
  return createHash("sha256").update(body).digest("hex");
}

export async function lire(dir, key) {
  try {
    return await readFile(join(dir, `${key}.bin`));
  } catch (error) {
    if (error.code === "ENOENT") return null;
    throw error;
  }
}

export async function ecrire(dir, key, bytes) {
  await mkdir(dir, { recursive: true });
  const dest = join(dir, `${key}.bin`);
  const existing = await lire(dir, key);
  if (existing) return existing;
  const temporary = join(dir, `.${key}.tmp`);
  await writeFile(temporary, bytes);
  try {
    await rename(temporary, dest);
  } catch (error) {
    if (error.code !== "EEXIST") throw error;
  }
  return (await lire(dir, key)) ?? bytes;
}

export function planifier(manifest, referenceId, presents) {
  if (!/^[0-9a-f]{32}$/.test(referenceId)) {
    throw Object.assign(new Error("reference_id"), { code: "reference_id" });
  }
  const paragraphs = manifest.paragraphs.map((paragraph) => {
    const before = cleCache({ text: paragraph.text, referenceId: manifest.reference_id });
    const after = cleCache({ text: paragraph.text, referenceId });
    return {
      id: paragraph.id,
      cues: paragraph.cues,
      before,
      after,
      stale: !presents.has(after),
    };
  });
  return { requests: 0, reference_id: referenceId, paragraphs };
}

export function appliquer(manifest, plan) {
  return {
    reference_id: plan.reference_id,
    paragraphs: manifest.paragraphs.map((paragraph) => ({
      id: paragraph.id,
      text: paragraph.text,
      cues: [...paragraph.cues],
    })),
  };
}

function canonique(value) {
  if (Array.isArray(value)) return `[${value.map(canonique).join(",")}]`;
  if (value && typeof value === "object") {
    const keys = Object.keys(value).sort();
    return `{${keys.map((key) => `${JSON.stringify(key)}:${canonique(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}
