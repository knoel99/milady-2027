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
  if (audio <= fenetre + 1e-2) return { action: "tient", atempo: null, speed: 1 };
  throw Object.assign(new Error(`atempo refusé: ${audio} s dans un créneau de ${fenetre} s`), {
    code: "atempo",
    audio,
    fenetre,
  });
}

export function rapport(cal, durees) {
  return cal.beats.map((beat) => {
    const cues = beat.paragraphes.map((paragraphe, index) => {
      const suivant = beat.paragraphes[index + 1];
      const fin = suivant ? suivant.at : beat.debut + beat.slot;
      const audio = durees.get(paragraphe.id) ?? 0;
      return { id: paragraphe.id, at: paragraphe.at, audio, fenetre: fin - paragraphe.at, action: "tient", atempo: null, speed: 1 };
    });
    const audio = cues.reduce((somme, cue) => somme + cue.audio, 0);
    return { id: beat.id, audio, slot: beat.slot, ...ajuster(audio, beat.slot), cues };
  });
}

export function relier(texte, mises) {
  const voulu = new Map(mises.map((mise) => [`${mise.lang}\0${mise.id}`, mise]));
  let sortie = "";
  let index = 0;
  for (const span of objetsFeuilles(texte)) {
    sortie += texte.slice(index, span.debut);
    const brut = texte.slice(span.debut, span.fin);
    let valeur = null;
    try {
      valeur = JSON.parse(brut);
    } catch {
      valeur = null;
    }
    const mise = valeur && typeof valeur.id === "string" ? voulu.get(`${valeur.lang}\0${valeur.id}`) : null;
    sortie += mise ? remplacerCreneau(brut, mise) : brut;
    index = span.fin;
  }
  return sortie + texte.slice(index);
}

export function brancher(document, fichiers, rapports) {
  return {
    slots: document.slots.map((slot) => {
      const cue = (rapports[slot.lang] ?? []).flatMap((beat) => beat.cues).find((item) => item.id === slot.id);
      const fichier = fichiers[slot.lang]?.[slot.id];
      if (!cue || !fichier) return slot;
      if (cue.atempo) {
        throw Object.assign(new Error(`atempo refusé: ${slot.id}`), { code: "atempo" });
      }
      const tient = cue.action === "tient";
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
      const atempo = parCue.get(paragraphe.id)?.atempo ?? null;
      if (atempo) throw Object.assign(new Error(`atempo refusé: ${paragraphe.id}`), { code: "atempo" });
      liste.push({ fichier, at: paragraphe.at, atempo: null });
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

function objetsFeuilles(texte) {
  const pile = [];
  const spans = [];
  let chaine = false;
  let echappe = false;
  for (let index = 0; index < texte.length; index += 1) {
    const caractere = texte[index];
    if (chaine) {
      if (echappe) echappe = false;
      else if (caractere === "\\") echappe = true;
      else if (caractere === '"') chaine = false;
      continue;
    }
    if (caractere === '"') {
      chaine = true;
      continue;
    }
    if (caractere === "{") pile.push({ debut: index, enfants: 0 });
    else if (caractere === "}" && pile.length > 0) {
      const courant = pile.pop();
      if (pile.length > 0) pile[pile.length - 1].enfants += 1;
      if (courant.enfants === 0) spans.push({ debut: courant.debut, fin: index + 1 });
    }
  }
  return spans;
}

function remplacerCreneau(brut, mise) {
  let sortie = remplacerChamp(brut, "audio", mise.audio);
  sortie = remplacerChamp(sortie, "status", mise.status);
  return remplacerChamp(sortie, "reason", mise.reason);
}

function remplacerChamp(brut, nom, valeur) {
  const motif = new RegExp(`("${nom}"\\s*:\\s*)(?:"(?:\\\\.|[^"\\\\])*"|null|true|false|-?\\d+(?:\\.\\d+)?)`);
  if (!motif.test(brut)) throw Object.assign(new Error(`champ ${nom}`), { code: "champ" });
  return brut.replace(motif, `$1${JSON.stringify(valeur)}`);
}

export async function ecrireManifeste(path, { chapter, lang, paragraphes }) {
  await writeFile(path, `${JSON.stringify({ chapter, lang, paragraphes }, null, 2)}\n`);
}
