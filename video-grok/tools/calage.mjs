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

export function ecouter(taches) {
  if (taches.length === 0) return {};
  const resultat = spawnSync("python3", [join(ici, "oreille.py")], {
    input: JSON.stringify({ taches }),
    maxBuffer: 64_000_000,
    encoding: "utf8",
    env: { ...process.env, TOKENIZERS_PARALLELISM: "false" },
  });
  if (resultat.status !== 0) {
    throw new Error(resultat.stderr?.slice(-800) || "oreille");
  }
  return JSON.parse(resultat.stdout);
}

function jetons(texte) {
  return texte
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim()
    .split(/\s+/)
    .filter((mot) => mot.length > 2);
}

function recouvre(phrase, texte) {
  const attendus = jetons(phrase);
  const entendus = new Set(jetons(texte));
  const mots = attendus.length === 0 || entendus.size === 0
    ? 0
    : attendus.filter((mot) => entendus.has(mot)).length / attendus.length;
  const chiffresPhrase = (phrase.match(/\d/g) ?? []).join("");
  const chiffresTexte = (texte.match(/\d/g) ?? []).join("");
  const nombres = chiffresPhrase && chiffresTexte && (chiffresTexte.includes(chiffresPhrase) || chiffresPhrase.includes(chiffresTexte)) ? 0.45 : 0;
  return Math.min(1, mots + nombres);
}

export function repartir(phrases, segments) {
  if (phrases.length === 0) return [];
  if (!segments?.length) {
    return phrases.map((phrase) => ({ phrase, debut: 0, fin: 0 }));
  }
  const n = phrases.length;
  const m = segments.length;
  const inf = 1e9;
  const cout = Array.from({ length: n + 1 }, () => Array(m + 1).fill(inf));
  const choix = Array.from({ length: n + 1 }, () => Array(m + 1).fill(null));
  cout[0][0] = 0;
  for (let i = 0; i <= n; i += 1) {
    for (let j = 0; j <= m; j += 1) {
      if (cout[i][j] >= inf / 2) continue;
      if (i < n && j < m) {
        const prix = 1 - recouvre(phrases[i], segments[j].texte);
        if (cout[i][j] + prix < cout[i + 1][j + 1]) {
          cout[i + 1][j + 1] = cout[i][j] + prix;
          choix[i + 1][j + 1] = [i, j, 1];
        }
      }
      if (i < n && j + 1 < m) {
        const prix = 1 - recouvre(phrases[i], `${segments[j].texte} ${segments[j + 1].texte}`) + 0.05;
        if (cout[i][j] + prix < cout[i + 1][j + 2]) {
          cout[i + 1][j + 2] = cout[i][j] + prix;
          choix[i + 1][j + 2] = [i, j, 2];
        }
      }
      if (i + 1 < n && j < m) {
        const prix =
          1 -
          Math.max(recouvre(phrases[i], segments[j].texte), recouvre(phrases[i + 1], segments[j].texte)) +
          0.08;
        if (cout[i][j] + prix < cout[i + 2][j + 1]) {
          cout[i + 2][j + 1] = cout[i][j] + prix;
          choix[i + 2][j + 1] = [i, j, "partage"];
        }
      }
    }
  }
  if (!choix[n][m]) {
    const fin = segments.at(-1).fin;
    const pas = fin / n || 0;
    return phrases.map((phrase, index) => ({ phrase, debut: index * pas, fin: (index + 1) * pas }));
  }
  const etapes = [];
  let i = n;
  let j = m;
  while (i > 0 || j > 0) {
    const pas = choix[i][j];
    if (!pas) break;
    etapes.push(pas);
    i = pas[0];
    j = pas[1];
  }
  etapes.reverse();
  const fenetres = phrases.map((phrase) => ({ phrase, debut: 0, fin: 0 }));
  for (const [pi, pj, mode] of etapes) {
    if (mode === 1) {
      fenetres[pi] = { phrase: phrases[pi], debut: segments[pj].debut, fin: segments[pj].fin };
    } else if (mode === 2) {
      fenetres[pi] = { phrase: phrases[pi], debut: segments[pj].debut, fin: segments[pj + 1].fin };
    } else {
      const milieu = (segments[pj].debut + segments[pj].fin) / 2;
      fenetres[pi] = { phrase: phrases[pi], debut: segments[pj].debut, fin: milieu };
      fenetres[pi + 1] = { phrase: phrases[pi + 1], debut: milieu, fin: segments[pj].fin };
    }
  }
  return fenetres;
}

export function paroleRms(fenetre, regions) {
  let debut = fenetre.debut;
  let fin = fenetre.fin;
  let vu = false;
  for (const region of regions ?? []) {
    if (region.fin <= fenetre.debut || region.debut >= fenetre.fin) continue;
    const gauche = region.debut >= fenetre.debut - 0.45 ? region.debut : fenetre.debut;
    const droite = Math.min(region.fin, fenetre.fin);
    if (!vu) {
      debut = gauche;
      fin = droite;
      vu = true;
    } else {
      debut = Math.min(debut, gauche);
      fin = Math.max(fin, droite);
    }
  }
  if (fin < debut) fin = debut;
  return { debut, fin };
}

export function calerPhrasesDepuisOreille(oreille, brut, decouper) {
  const phrases = decouper(brut);
  return repartir(phrases, oreille?.segments ?? []).map((fenetre) => {
    const parole = paroleRms(fenetre, oreille?.regions ?? []);
    return { phrase: fenetre.phrase, debut: parole.debut, fin: Math.max(parole.fin, parole.debut) };
  });
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
