import { REGLAGES } from "./cache.mjs";

export const VOIX = "536d3a5e000945adb7038665781a4aca";
export const INDICATION = "[calm, natural narrator voice]";
export const PAUSE_LONGUE = "[long pause]";
export const URL_FISH = "https://api.fish.audio/v1/tts";

export const TERMES = [
  "Fokker–Planck",
  "Zel'dovich",
  "Jean Zay",
  "Glatzmaier",
  "Ponomarenko",
  "Wasserstein",
  "Kazantsev",
  "Gissinger",
  "Karlsruhe",
  "Cadarache",
  "Liouville",
  "Poincaré",
  "SFEMaNS",
  "DRESDYN",
  "PySINDy",
  "TorchDA",
  "FunDiff",
  "Pétrélis",
  "Reynolds",
  "MilaDy",
  "Cowling",
  "GENCI",
  "CEREA",
  "Heun",
  "Leray",
  "LATU",
  "MHD",
  "ABC",
  "VKS",
  "ENPC",
  "LISN",
  "DQVU",
  "Cheng",
  "Lucor",
  "Nore",
  "Ponty",
  "Rice",
  "Rm",
  "Re",
  "Pm",
];

const BLOQUES = new Set(["Glatzmaier"]);

export function lireMarkdown(markdown) {
  const beats = [];
  let beat = null;
  let cue = null;
  for (const line of markdown.split(/\r?\n/)) {
    if (line.startsWith("## ")) {
      beat = { id: line.slice(3).trim(), slot: 0, cues: [] };
      beats.push(beat);
      cue = null;
      continue;
    }
    if (line.startsWith("### ")) {
      if (!beat) throw Object.assign(new Error("beat"), { code: "beat" });
      cue = { id: line.slice(4).trim(), role: "", pause: 0, lignes: [] };
      beat.cues.push(cue);
      continue;
    }
    if (beat && line.startsWith("duration:")) {
      const [minutes, seconds] = line.slice("duration:".length).trim().split(":");
      beat.slot = Number(minutes) * 60 + Number(seconds);
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
    if (line.startsWith("screen:") || line.startsWith("badge:") || line.startsWith("class:")) continue;
    if (line.trim() === "") continue;
    cue.lignes.push(line.trim());
  }
  return beats;
}

export function epingler(texte, lang, sources = { en: {}, fr: {} }) {
  const table = sources[lang] ?? {};
  const ordre = [...TERMES].sort((gauche, droite) => droite.length - gauche.length);
  const occupes = [];
  for (const terme of ordre) {
    for (const match of texte.matchAll(limite(terme))) {
      const debut = match.index;
      const fin = debut + terme.length;
      if (occupes.some((span) => debut < span.fin && fin > span.debut)) continue;
      occupes.push({ debut, fin, terme });
    }
  }
  occupes.sort((gauche, droite) => gauche.debut - droite.debut);
  const manquantes = [];
  const vus = new Set();
  let sortie = "";
  let index = 0;
  for (const span of occupes) {
    sortie += texte.slice(index, span.debut);
    const phonemes = BLOQUES.has(span.terme) ? null : table[span.terme];
    if (!phonemes) {
      if (!vus.has(span.terme)) {
        vus.add(span.terme);
        manquantes.push({ terme: span.terme, raison: BLOQUES.has(span.terme) ? "revue science" : "non sourcée" });
      }
      sortie += texte.slice(span.debut, span.fin);
    } else {
      sortie += `<|phoneme_start|>${phonemes}<|phoneme_end|>`;
    }
    index = span.fin;
  }
  return { texte: sortie + texte.slice(index), manquantes };
}

export function preparer(markdown, lang, sources) {
  const beats = lireMarkdown(markdown);
  const paragraphes = [];
  let premier = true;
  for (const beat of beats) {
    let principal = true;
    const parles = [];
    for (const cue of beat.cues) {
      if (cue.role !== "spoken") continue;
      const brut = cue.lignes.join(" ");
      if (!brut) throw Object.assign(new Error(`paragraphe vide ${cue.id}`), { code: "paragraphe" });
      const epingle = epingler(brut, lang, sources);
      let texte = epingle.texte;
      if (premier) {
        texte = `${INDICATION} ${texte}`;
        premier = false;
        principal = false;
      } else if (principal) {
        texte = `${PAUSE_LONGUE} ${texte}`;
        principal = false;
      }
      if (/<emphasis>|<stress>/i.test(texte)) {
        throw Object.assign(new Error("balise"), { code: "balise" });
      }
      const item = {
        id: cue.id,
        beat: beat.id,
        brut,
        texte,
        pause: cue.pause,
        manquantes: epingle.manquantes,
      };
      parles.push(item);
      paragraphes.push(item);
    }
    beat.paragraphes = parles;
  }
  return { lang, beats, paragraphes };
}

export function estimer(chapitre) {
  const vus = new Map();
  for (const paragraphe of chapitre.paragraphes) {
    for (const manque of paragraphe.manquantes) vus.set(manque.terme, manque);
  }
  return {
    requetes: chapitre.paragraphes.length,
    caracteres: chapitre.paragraphes.reduce((somme, paragraphe) => somme + paragraphe.texte.length, 0),
    manquantes: [...vus.values()],
  };
}

export function filtreAtempo(facteur) {
  if (!(facteur > 0)) throw Object.assign(new Error("atempo"), { code: "atempo" });
  return `atempo=${facteur}`;
}

export function corps(texte, reglages = REGLAGES) {
  if (reglages.prosody.speed < 1) {
    throw Object.assign(new Error("speed"), { code: "speed" });
  }
  return {
    text: texte,
    reference_id: VOIX,
    temperature: reglages.temperature,
    format: reglages.format,
    mp3_bitrate: reglages.mp3_bitrate,
    sample_rate: reglages.sample_rate,
    latency: reglages.latency,
    normalize: reglages.normalize,
    condition_on_previous_chunks: reglages.condition_on_previous_chunks,
    prosody: { speed: reglages.prosody.speed, normalize_loudness: reglages.prosody.normalize_loudness },
  };
}

export function formulerManquantes(manquantes) {
  if (manquantes.length === 0) return "aucune";
  return manquantes.map((manque) => `${manque.terme}: ${manque.raison}`).join(", ");
}

export function formulerEstimation(opts, estimation) {
  return [
    `chapitre: ${opts.chapter}`,
    `langue: ${opts.lang}`,
    `requêtes: ${estimation.requetes}`,
    `caractères: ${estimation.caracteres}`,
    `non sourcées: ${formulerManquantes(estimation.manquantes)}`,
    "",
  ].join("\n");
}

export function formulerSynthese(opts, resultat, estimation) {
  return [
    `chapitre: ${opts.chapter}`,
    `langue: ${opts.lang}`,
    `requêtes: ${resultat.requetes}`,
    `prévues: ${resultat.prevues}`,
    `cache: ${resultat.succesCache}`,
    `caractères: ${estimation.caracteres}`,
    `minutes: ${resultat.minutes == null ? "unavailable" : resultat.minutes}`,
    `non sourcées: ${formulerManquantes(estimation.manquantes)}`,
    "",
  ].join("\n");
}

function limite(terme) {
  return new RegExp(`(?<![\\p{L}\\p{N}])${echapper(terme)}(?![\\p{L}\\p{N}])`, "gu");
}

function echapper(terme) {
  return terme.replace(/[\\^$.*+?()[\]{}|]/g, "\\$&");
}
