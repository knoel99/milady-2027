import { spawn } from "node:child_process";
import { mkdtemp, readFile, readdir, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { filtreAtempo } from "./parole.mjs";

export function horloges(scenes) {
  const table = new Map();
  for (const scene of scenes) {
    for (const cue of scene.cues ?? []) table.set(cue.id, cue.at);
  }
  return table;
}

export function calendrier(chapitre, temps) {
  let origine = 0;
  const beats = chapitre.beats.map((beat) => {
    const locaux = instants(beat, temps);
    const debut = origine;
    origine += beat.slot;
    return {
      id: beat.id,
      slot: beat.slot,
      debut,
      paragraphes: beat.paragraphes.map((paragraphe, index) => ({
        ...paragraphe,
        at: debut + locaux[index],
      })),
    };
  });
  return { duree: origine, beats };
}

export function ajuster(audio, fenetre) {
  if (!(fenetre > 0)) throw Object.assign(new Error("creneau"), { code: "creneau" });
  const speed = 1;
  if (audio <= fenetre + 1e-6) return { action: "tient", atempo: null, speed };
  const ratio = audio / fenetre;
  if (ratio <= 1.12 + 1e-9) {
    return { action: "atempo", atempo: Number(ratio.toFixed(4)), speed };
  }
  return { action: "reminutage", atempo: null, speed };
}

export function rapport(cal, durees) {
  return cal.beats.map((beat) => {
    const cues = beat.paragraphes.map((paragraphe, index) => {
      const suivant = beat.paragraphes[index + 1];
      const fin = suivant ? suivant.at : beat.debut + beat.slot;
      const audio = durees.get(paragraphe.id) ?? 0;
      return { id: paragraphe.id, at: paragraphe.at, audio, fenetre: fin - paragraphe.at, ...ajuster(audio, fin - paragraphe.at) };
    });
    const audio = cues.reduce((somme, cue) => somme + cue.audio, 0);
    return { id: beat.id, audio, slot: beat.slot, ...ajuster(audio, beat.slot), cues };
  });
}

export function brancher(document, fichiers, rapports) {
  return {
    slots: document.slots.map((slot) => {
      const cue = (rapports[slot.lang] ?? []).flatMap((beat) => beat.cues).find((item) => item.id === slot.id);
      const fichier = fichiers[slot.lang]?.[slot.id];
      if (!cue || !fichier) return { ...slot, audio: null, status: "PENDING" };
      const tient = cue.action === "tient" || cue.action === "atempo";
      if (!tient) return { ...slot, audio: null, status: "PENDING", reason: "la durée dépasse le créneau" };
      return { ...slot, audio: fichier, status: "READY", reason: "" };
    }),
  };
}

export function argumentsPiste(clips, duree) {
  const args = ["-y"];
  for (const clip of clips) args.push("-i", clip.fichier);
  const filtres = clips.map((clip, index) => {
    const delai = Math.round(clip.at * 1000);
    const tempo = clip.atempo ? `${filtreAtempo(clip.atempo)},` : "";
    return `[${index}]${tempo}adelay=${delai}:all=1[c${index}]`;
  });
  if (clips.length === 1) {
    filtres.push(`[c0]atrim=0:${duree},apad=whole_dur=${duree}[out]`);
  } else {
    const melange = clips.map((_, index) => `[c${index}]`).join("");
    filtres.push(
      `${melange}amix=inputs=${clips.length}:duration=longest:dropout_transition=0:normalize=0,atrim=0:${duree},apad=whole_dur=${duree}[out]`,
    );
  }
  args.push("-filter_complex", filtres.join(";"), "-map", "[out]", "-c:a", "pcm_s16le", "-ar", "44100");
  return args;
}

export async function rendre({ en, fr, horloges: temps, sortie }) {
  const calEn = calendrier(en.chapitre, temps);
  const calFr = calendrier(fr.chapitre, temps);
  if (calEn.duree !== calFr.duree) throw Object.assign(new Error("durees"), { code: "durees" });
  for (const beat of calEn.beats) {
    const autre = calFr.beats.find((item) => item.id === beat.id);
    for (const paragraphe of beat.paragraphes) {
      const jumeau = autre?.paragraphes.find((item) => item.id === paragraphe.id);
      if (!jumeau || jumeau.at !== paragraphe.at) {
        throw Object.assign(new Error(`decalage ${paragraphe.id}`), { code: "decalage" });
      }
    }
  }
  const dureesEn = await sonder(en.fichiers);
  const dureesFr = await sonder(fr.fichiers);
  const rapportEn = rapport(calEn, dureesEn);
  const rapportFr = rapport(calFr, dureesFr);
  const dossier = await mkdtemp(join(tmpdir(), "pilote-"));
  const pisteEn = join(dossier, "en.wav");
  const pisteFr = join(dossier, "fr.wav");
  await executer("ffmpeg", [...argumentsPiste(clips(calEn, en.fichiers, rapportEn), calEn.duree), pisteEn]);
  await executer("ffmpeg", [...argumentsPiste(clips(calFr, fr.fichiers, rapportFr), calFr.duree), pisteFr]);
  await executer("ffmpeg", [
    "-y",
    "-i",
    pisteEn,
    "-i",
    pisteFr,
    "-map",
    "0:a",
    "-map",
    "1:a",
    "-c:a",
    "aac",
    "-b:a",
    "192k",
    sortie,
  ]);
  return { en: rapportEn, fr: rapportFr, sortie, duree: calEn.duree };
}

export function dureeFichier(path) {
  return new Promise((resolve, reject) => {
    const enfant = spawn("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "json", path], {
      stdio: ["ignore", "pipe", "pipe"],
    });
    let sortie = "";
    let erreur = "";
    enfant.stdout.on("data", (chunk) => {
      sortie += chunk.toString();
    });
    enfant.stderr.on("data", (chunk) => {
      erreur += chunk.toString();
    });
    enfant.on("error", reject);
    enfant.on("close", (code) => {
      if (code !== 0) reject(new Error(erreur.slice(-500)));
      else resolve(Number(JSON.parse(sortie).format.duration));
    });
  });
}

export async function lireScenes(dir) {
  const noms = (await readdir(dir)).filter((nom) => nom.endsWith(".json") && nom !== "cues.json");
  const scenes = [];
  for (const nom of noms.sort()) scenes.push(JSON.parse(await readFile(join(dir, nom), "utf8")));
  return scenes;
}

function instants(beat, temps) {
  const connus = beat.paragraphes.every((paragraphe) => temps.has(paragraphe.id));
  if (beat.paragraphes.length > 0 && connus) {
    return beat.paragraphes.map((paragraphe) => temps.get(paragraphe.id));
  }
  const part = beat.slot / beat.paragraphes.length;
  return beat.paragraphes.map((_, index) => index * part);
}

function clips(cal, fichiers, lignes) {
  const parCue = new Map(lignes.flatMap((beat) => beat.cues.map((cue) => [cue.id, cue])));
  const liste = [];
  for (const beat of cal.beats) {
    for (const paragraphe of beat.paragraphes) {
      const fichier = fichiers[paragraphe.id];
      if (!fichier) throw Object.assign(new Error(`audio manquant: ${paragraphe.id}`), { code: "audio" });
      liste.push({ fichier, at: paragraphe.at, atempo: parCue.get(paragraphe.id)?.atempo ?? null });
    }
  }
  if (liste.length === 0) throw Object.assign(new Error("audio manquant"), { code: "audio" });
  return liste;
}

async function sonder(fichiers) {
  const durees = new Map();
  for (const [id, fichier] of Object.entries(fichiers)) durees.set(id, await dureeFichier(fichier));
  return durees;
}

function executer(commande, args) {
  return new Promise((resolve, reject) => {
    const enfant = spawn(commande, args, { stdio: ["ignore", "ignore", "pipe"] });
    let erreur = "";
    enfant.stderr.on("data", (chunk) => {
      erreur += chunk.toString();
    });
    enfant.on("error", reject);
    enfant.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error(erreur.slice(-2000)));
    });
  });
}

export async function ecrireManifeste(path, { chapter, lang, paragraphes }) {
  await writeFile(path, `${JSON.stringify({ chapter, lang, paragraphes }, null, 2)}\n`);
}
