import { spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const VOIX = { en: "en-us", fr: "fr-fr" };
const memoire = new Map();
const ici = dirname(fileURLToPath(import.meta.url));

export function motsTexte(texte) {
  return texte.replaceAll("\n", " ").trim().split(/\s+/).filter(Boolean);
}

export async function syntheseMot(mot, lang) {
  const cle = `${lang}\0${mot}`;
  const garde = memoire.get(cle);
  if (garde) return garde;
  const voix = VOIX[lang] ?? "en-us";
  const resultat = spawnSync("espeak-ng", ["-v", voix, "-s", "150", "--stdout", mot], {
    maxBuffer: 8_000_000,
  });
  if (resultat.status !== 0) {
    throw new Error(resultat.stderr?.toString() || "espeak-ng");
  }
  const lu = lireTampon(resultat.stdout);
  memoire.set(cle, lu);
  return lu;
}

export function alignerTextes(taches) {
  if (taches.length === 0) return {};
  const resultat = spawnSync("python3", [join(ici, "acoustique.py")], {
    input: JSON.stringify({ taches }),
    maxBuffer: 64_000_000,
    encoding: "utf8",
    env: { ...process.env, TRANSFORMERS_VERBOSITY: "error", TOKENIZERS_PARALLELISM: "false" },
  });
  if (resultat.status !== 0) {
    throw new Error(resultat.stderr?.slice(-800) || "alignement acoustique");
  }
  return JSON.parse(resultat.stdout);
}

export function calerPhrasesDepuisMots(mots, brut, decouper) {
  const phrases = decouper(brut);
  const cues = [];
  let index = 0;
  for (const phrase of phrases) {
    const nombre = motsTexte(phrase).length;
    const groupe = mots.slice(index, index + nombre);
    index += nombre;
    if (groupe.length === 0) continue;
    cues.push({
      phrase,
      debut: groupe[0].debut,
      fin: groupe[groupe.length - 1].fin,
    });
  }
  return cues;
}

export async function calerPhrases(fichier, brut, lang, decouper) {
  const aligne = alignerTextes([{ id: "clip", audio: fichier, texte: brut, langue: lang }]);
  return calerPhrasesDepuisMots(aligne.clip ?? [], brut, decouper);
}

function lireTampon(buffer) {
  if (buffer.toString("ascii", 0, 4) !== "RIFF") throw new Error("wav");
  let offset = 12;
  let sampleRate = 0;
  let data = null;
  while (offset + 8 <= buffer.length) {
    const id = buffer.toString("ascii", offset, offset + 4);
    const size = buffer.readUInt32LE(offset + 4);
    const body = offset + 8;
    if (id === "fmt ") sampleRate = buffer.readUInt32LE(body + 4);
    if (id === "data") data = buffer.subarray(body, body + size);
    offset = body + size + (size % 2);
  }
  const samples = new Float64Array(data.length / 2);
  for (let index = 0; index < samples.length; index += 1) {
    samples[index] = data.readInt16LE(index * 2) / 32768;
  }
  return { samples, sampleRate };
}
