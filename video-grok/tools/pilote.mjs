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

export function placer(paragraphes, durees) {
  let curseur = 0;
  const poses = [];
  for (const paragraphe of paragraphes) {
    const audio = durees.get(paragraphe.id) ?? 0;
    const pause = Number(paragraphe.pause) || 0;
    const at = curseur;
    const fin = at + audio;
    poses.push({ id: paragraphe.id, at, audio, pause, fin });
    curseur = fin + pause;
  }
  return { poses, fin: curseur };
}

export function chevauchements(poses) {
  const problèmes = [];
  for (let index = 1; index < poses.length; index += 1) {
    if (poses[index].at + 1e-3 < poses[index - 1].fin) {
      problèmes.push(`${poses[index - 1].id} → ${poses[index].id}`);
    }
  }
  return problèmes;
}

export function deborde(poses, slot) {
  return poses.filter((pose) => pose.fin > slot + 1e-2).map((pose) => pose.id);
}

export function calendrier(chapitre, temps, durees) {
  let origine = 0;
  const beats = chapitre.beats.map((beat) => {
    const locaux = durees ? locauxMesures(beat, durees) : instants(beat, temps);
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

function locauxMesures(beat, durees) {
  const place = placer(beat.paragraphes, durees);
  if (place.fin > beat.slot + 1e-2) {
    throw Object.assign(
      new Error(`creneau ${beat.id}: ${place.fin.toFixed(3)} s dans ${beat.slot} s`),
      { code: "creneau", beat: beat.id, fin: place.fin, slot: beat.slot },
    );
  }
  if (chevauchements(place.poses).length > 0) {
    throw Object.assign(new Error(`chevauche ${beat.id}`), { code: "chevauche" });
  }
  const parId = new Map(place.poses.map((pose) => [pose.id, pose.at]));
  return beat.paragraphes.map((paragraphe) => parId.get(paragraphe.id));
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

export function bords(scene, poses, slot) {
  const ancien = [0];
  const nouveau = [poses[0] ? poses[0].at : 0];
  for (let index = 1; index < poses.length; index += 1) {
    const cue = (scene.cues ?? []).find((item) => item.id === poses[index].id);
    const marque = cue ? cue.at : (index * scene.duration) / poses.length;
    if (marque > ancien[ancien.length - 1] + 1e-6) {
      ancien.push(marque);
      nouveau.push(poses[index].at);
    }
  }
  ancien.push(scene.duration);
  nouveau.push(slot);
  return { ancien, nouveau };
}

export function projeter(temps, bordsScene) {
  const { ancien, nouveau } = bordsScene;
  for (let index = 0; index < ancien.length - 1; index += 1) {
    if (temps <= ancien[index + 1] + 1e-9) {
      const largeur = ancien[index + 1] - ancien[index] || 1;
      const part = (temps - ancien[index]) / largeur;
      return nouveau[index] + part * (nouveau[index + 1] - nouveau[index]);
    }
  }
  return nouveau[nouveau.length - 1];
}

export function sousTitresDans(scene, poses, slot) {
  const carte = bords(scene, poses, slot);
  const instant = new Map((scene.cues ?? []).map((cue) => [cue.id, projeter(cue.at, carte)]));
  const hors = [];
  for (const layer of (scene.layers ?? []).filter((item) => item.kind === "subtitle")) {
    const debut = instant.get(layer.from);
    const fin = instant.get(layer.until);
    const contient = poses.some((pose, index) => {
      const borne = index + 1 < poses.length ? poses[index + 1].at : slot;
      return debut >= pose.at - 1e-6 && fin <= borne + 1e-6;
    });
    if (!contient) hors.push(layer.from);
  }
  return hors;
}

export async function rendre({ en, fr, sortie }) {
  const dureesEn = await sonder(en.fichiers);
  const dureesFr = await sonder(fr.fichiers);
  const calEn = calendrier(en.chapitre, new Map(), dureesEn);
  const calFr = calendrier(fr.chapitre, new Map(), dureesFr);
  if (calEn.duree !== calFr.duree) throw Object.assign(new Error("durees"), { code: "durees" });
  for (const beat of calEn.beats) {
    if (!calFr.beats.some((item) => item.id === beat.id)) {
      throw Object.assign(new Error(`decalage ${beat.id}`), { code: "decalage" });
    }
  }
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
