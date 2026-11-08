import { spawn, spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { copyFile, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { capturer } from "./capture.mjs";
import { preparer } from "./parole.mjs";
import { bords, dureeFichier, lireScenes, placer, projeter } from "./pilote.mjs";
import { servir } from "./servir.mjs";
import { garderCle } from "./tts.mjs";

const ici = dirname(fileURLToPath(import.meta.url));

export function analyser(argv) {
  const opts = {
    chapter: "g10",
    cache: null,
    sortie: null,
    clips: null,
    scenes: null,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--chapter") opts.chapter = lireValeur(argv, (index += 1), arg);
    else if (arg === "--cache") opts.cache = lireValeur(argv, (index += 1), arg);
    else if (arg === "--sortie") opts.sortie = lireValeur(argv, (index += 1), arg);
    else if (arg === "--clips") opts.clips = lireValeur(argv, (index += 1), arg);
    else if (arg === "--scenes") opts.scenes = lireValeur(argv, (index += 1), arg);
    else throw Object.assign(new Error(`argument ${arg}`), { code: "argument" });
  }
  if (!opts.cache) throw Object.assign(new Error("cache"), { code: "cache" });
  if (!opts.sortie) throw Object.assign(new Error("sortie"), { code: "sortie" });
  return opts;
}

export function tableau(chapitre) {
  return chapitre.beats.map((beat) => ({
    id: beat.id,
    slot: beat.slot,
    nom: beat.id.slice(beat.id.indexOf(".") + 1),
  }));
}

const IMAGES = 30;

export function dureeTableau(lignes) {
  return lignes.reduce((somme, ligne) => somme + ligne.slot, 0);
}

export function images(slot) {
  const n = Math.round(slot * IMAGES);
  if (n < 1) throw Object.assign(new Error("images"), { code: "images" });
  return n;
}

export function fichiersSortie(sortie) {
  const tige = sortie.endsWith(".mp4") ? sortie.slice(0, -4) : sortie;
  return [
    { lang: "en", langue: "eng", piste: 0, fichier: `${tige}-en.mp4` },
    { lang: "fr", langue: "fra", piste: 1, fichier: `${tige}-fr.mp4` },
  ];
}

export function argumentsMontage({ lignes, clips, pistes, sortie, piste = 0, langue = "eng", sousTitres = null }) {
  if (clips.length !== lignes.length) {
    throw Object.assign(new Error("clips"), { code: "clips" });
  }
  const args = ["-y"];
  for (const clip of clips) args.push("-i", clip);
  args.push("-i", pistes);
  if (sousTitres) args.push("-i", sousTitres);
  const audio = clips.length;
  const sous = sousTitres ? clips.length + 1 : null;
  const filtres = lignes.map((ligne, index) => {
    const n = images(ligne.slot);
    return `[${index}:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=${IMAGES},tpad=stop_mode=clone:stop=${n},trim=end_frame=${n},settb=1/${IMAGES},setpts=N[v${index}]`;
  });
  filtres.push(`${lignes.map((_, index) => `[v${index}]`).join("")}concat=n=${lignes.length}:v=1:a=0[v]`);
  args.push(
    "-filter_complex",
    filtres.join(";"),
    "-map",
    "[v]",
    "-map",
    `${audio}:a:${piste}`,
    "-c:v",
    "libx264",
    "-preset",
    "ultrafast",
    "-pix_fmt",
    "yuv420p",
    "-crf",
    "20",
    "-g",
    "60",
    "-color_primaries",
    "bt709",
    "-color_trc",
    "bt709",
    "-colorspace",
    "bt709",
    "-c:a",
    "copy",
    "-metadata:s:a:0",
    `language=${langue}`,
    "-movflags",
    "+faststart",
    "-r",
    String(IMAGES),
    "-video_track_timescale",
    String(IMAGES),
    "-frames:v",
    String(lignes.reduce((somme, ligne) => somme + images(ligne.slot), 0)),
  );
  if (sous != null) {
    args.push("-map", `${sous}:s:0`, "-c:s", "mov_text", "-metadata:s:s:0", `language=${langue}`);
  }
  args.push(sortie);
  return args;
}

export async function monter({ lignes, clips, pistes, sortie, piste = 0, langue = "eng", sousTitres = null }) {
  await executer("ffmpeg", argumentsMontage({ lignes, clips, pistes, sortie, piste, langue, sousTitres }));
  return { sortie, duree: dureeTableau(lignes), images: lignes.reduce((somme, ligne) => somme + images(ligne.slot), 0) };
}

export async function principal(argv, env, io) {
  const opts = analyser(argv);
  const root = io.root;
  const markdown = await readFile(join(root, "narration", "en", `${opts.chapter}.md`), "utf8");
  const lignes = tableau(preparer(markdown, "en"));
  const scenesDir = opts.scenes ?? join(root, "scenes", opts.chapter);
  const scenes = await lireScenes(scenesDir);
  for (const ligne of lignes) {
    if (!scenes.some((scene) => scene.id === ligne.id)) {
      throw Object.assign(new Error(`scène manquante: ${ligne.id}`), { code: "scene" });
    }
  }
  const dossier = await mkdtemp(join(tmpdir(), "film-"));
  try {
    const pistes = join(dossier, "pistes.m4a");
    const creneaux = join(dossier, "cues.json");
    await copyFile(join(scenesDir, "cues.json"), creneaux);
    const rendu = spawnSync(
      process.execPath,
      [
        "--import",
        join(ici, "test/bloquer-reseau.mjs"),
        join(ici, "tts.mjs"),
        "--chapter",
        opts.chapter,
        "--rendre",
        "--cache",
        opts.cache,
        "--sortie",
        pistes,
        "--creneaux",
        creneaux,
        "--scenes",
        scenesDir,
      ],
      { encoding: "utf8", env: { ...env, FISH_API_KEY: "" } },
    );
    if (rendu.status !== 0) {
      throw Object.assign(new Error(garderCle(rendu.stderr || rendu.stdout, env.FISH_API_KEY)), { code: "rendre" });
    }
    verifierEmpreinte(pistes, await lireParole(opts.chapter));
    const films = fichiersSortie(opts.sortie);
    const rendus = [];
    for (const film of films) {
      const chapitre = preparer(
        await readFile(join(root, "narration", film.lang, `${opts.chapter}.md`), "utf8"),
        film.lang,
      );
      const durees = new Map();
      for (const paragraphe of chapitre.paragraphes) {
        const chemin = join(opts.cache, film.lang, `${paragraphe.id}.mp3`);
        durees.set(paragraphe.id, await dureeFichier(chemin));
      }
      const srt = join(dossier, `${film.lang}.srt`);
      await writeFile(srt, texteSrt(await sousTitresNarration(chapitre)));
      const clips = opts.clips
        ? lignes.map((ligne) => join(opts.clips, `${ligne.nom}.mp4`))
        : await capturerBeats({
            root,
            chapter: opts.chapter,
            lignes,
            scenes,
            dossier,
            lang: film.lang,
            chapitre,
            durees,
          });
      rendus.push(
        await monter({
          lignes,
          clips,
          pistes,
          sortie: film.fichier,
          piste: film.piste,
          langue: film.langue,
          sousTitres: srt,
        }),
      );
    }
    io.stdout.write(
      garderCle(
        [
          `chapitre: ${opts.chapter}`,
          `en: ${films[0].fichier}`,
          `fr: ${films[1].fichier}`,
          `video: ${rendus[0].duree}`,
          `images: ${rendus[0].images}`,
          "audio: eng",
          "audio: fra",
          "",
        ].join("\n"),
        env.FISH_API_KEY,
      ),
    );
    return rendus;
  } finally {
    await rm(dossier, { recursive: true, force: true });
  }
}

async function capturerBeats({ root, chapter, lignes, scenes, dossier, lang, chapitre, durees }) {
  const visuel = join(root, "tools/.cache/retiming", lang);
  const { mkdir } = await import("node:fs/promises");
  await mkdir(visuel, { recursive: true });
  for (const ligne of lignes) {
    const scene = scenes.find((item) => item.id === ligne.id);
    const beat = chapitre.beats.find((item) => item.id === ligne.id);
    const place = placer(beat.paragraphes, durees);
    const carte = bords(scene, place.poses, ligne.slot);
    const copie = {
      ...scene,
      duration: ligne.slot,
      cues: scene.cues.map((cue) => ({ ...cue, at: projeter(cue.at, carte) })),
    };
    await writeFile(join(visuel, `${ligne.nom}.json`), JSON.stringify(copie));
  }
  const server = await servir(root);
  const clips = [];
  try {
    for (const ligne of lignes) {
      const scene = scenes.find((item) => item.id === ligne.id);
      const ouverture = [...scene.cues].sort((a, b) => a.at - b.at)[0];
      const sortie = join(dossier, `${lang}-${ligne.nom}.mp4`);
      const document = encodeURIComponent(`/tools/.cache/retiming/${lang}/${ligne.nom}.json`);
      await capturer({
        url: `http://127.0.0.1:${server.port}/scenes/${chapter}/${ligne.nom}.html?lang=${lang}&document=${document}`,
        repere: ouverture.id,
        secondes: ligne.slot,
        sortie,
      });
      clips.push(sortie);
    }
  } finally {
    await server.close();
  }
  return clips;
}

const LARGEUR = 42;
const PUISSANCE = "⁰¹²³⁴⁵⁶⁷⁸⁹";

function puissance(chiffres) {
  return `⁻${[...String(chiffres)].map((chiffre) => PUISSANCE[Number(chiffre)]).join("")}`;
}

function notationNombres(texte) {
  return texte
    .replace(/(\d+(?:\.\d+)?) times 10 to the minus (\d+)/gi, (_, nombre, exposant) => `${nombre}\u00a0×\u00a010${puissance(exposant)}`)
    .replace(/about 10 to the minus (\d+)/gi, (_, exposant) => `about\u00a010${puissance(exposant)}`)
    .replace(/(\d+(?:,\d+)?) fois 10 à la puissance moins (\d+)/gi, (_, nombre, exposant) => `${nombre}\u00a0×\u00a010${puissance(exposant)}`)
    .replace(/environ 10 à la puissance moins (\d+)/gi, (_, exposant) => `environ\u00a010${puissance(exposant)}`);
}

function phrases(texte) {
  const trouvees = [];
  let courant = "";
  for (let index = 0; index < texte.length; index += 1) {
    const char = texte[index];
    courant += char;
    const decimal = char === "." && /\d/.test(texte[index - 1] ?? "") && /\d/.test(texte[index + 1] ?? "");
    if ((char === "." || char === "?" || char === "!") && !decimal) {
      trouvees.push(courant.trim());
      courant = "";
    }
  }
  if (courant.trim()) trouvees.push(courant.trim());
  return trouvees;
}

function lignesDe(texte) {
  const mots = texte.split(/ +/).filter(Boolean);
  const lignes = [];
  let ligne = "";
  for (const mot of mots) {
    const suivant = ligne ? `${ligne} ${mot}` : mot;
    if (suivant.length <= LARGEUR) ligne = suivant;
    else {
      if (ligne) lignes.push(ligne);
      ligne = mot;
    }
  }
  if (ligne) lignes.push(ligne);
  return lignes;
}

function motsDe(texte) {
  return texte
    .replaceAll("\n", " ")
    .replaceAll("\u00a0", " ")
    .replace(/[.!?]+/g, " ")
    .trim()
    .split(/\s+/)
    .filter(Boolean);
}

function estNombreSeul(texte) {
  const nu = texte.replaceAll("\n", " ").replaceAll("\u00a0", " ").replace(/[.!?]+$/g, "").trim();
  return /^(?:\d+(?:[.,]\d+)?|\d+(?:[.,]\d+)?\s*×\s*10[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+|10[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)$/.test(nu);
}

function aEcarter(cue) {
  if (cue.fin - cue.debut < 1 - 1e-6) return true;
  const mots = motsDe(cue.text);
  if (motsDe(cue.phrase).length <= 1 && mots.length <= 1) return false;
  if (mots.length <= 1) return true;
  return estNombreSeul(cue.text);
}

const TENUE = 0.3;

export async function lireParole(chapitre) {
  const chemin = join(ici, "..", "narration", `${chapitre}-speech-ref.json`);
  try {
    return JSON.parse(await readFile(chemin, "utf8"));
  } catch (error) {
    if (error.code === "ENOENT") throw Object.assign(new Error(`parole ${chapitre}`), { code: "parole" });
    throw error;
  }
}

export function empreinteAac(chemin, piste) {
  const resultat = spawnSync(
    "ffmpeg",
    ["-v", "error", "-i", chemin, "-map", `0:a:${piste}`, "-c", "copy", "-f", "adts", "pipe:1"],
    { maxBuffer: 32 * 1024 * 1024 },
  );
  if (resultat.status !== 0) {
    throw Object.assign(new Error(resultat.stderr?.toString().slice(-500) || "empreinte"), { code: "empreinte" });
  }
  return createHash("sha256").update(resultat.stdout).digest("hex");
}

export function verifierEmpreinte(chemin, ref) {
  const en = empreinteAac(chemin, 0);
  const fr = empreinteAac(chemin, 1);
  if (en === ref.sha256.en && fr === ref.sha256.fr) return;
  throw Object.assign(
    new Error(`empreinte\nen ${en}\nattendu ${ref.sha256.en}\nfr ${fr}\nattendu ${ref.sha256.fr}`),
    { code: "empreinte" },
  );
}

export function poserCues(cues) {
  const suite = cues.map((cue) => ({ ...cue, finVoix: cue.finVoix ?? cue.fin }));
  let garde = 0;
  while (garde < suite.length * 4 + 4) {
    garde += 1;
    appliquerTenue(suite);
    const index = suite.findIndex((cue) => aEcarter(cue));
    if (index < 0) return suite;
    let vers = -1;
    if (index > 0 && aEcarter(suite[index - 1])) vers = index - 1;
    else if (index + 1 < suite.length && aEcarter(suite[index + 1])) vers = index + 1;
    else if (index > 0) vers = index - 1;
    else if (index + 1 < suite.length) vers = index + 1;
    if (vers < 0) {
      if (suite[index].fin - suite[index].debut < 1 - 1e-6) suite[index].fin = suite[index].debut + 1;
      return suite;
    }
    const cible = Math.min(index, vers);
    const source = Math.max(index, vers);
    suite[cible] = reunir(suite[cible], suite[source]);
    suite.splice(source, 1);
  }
  appliquerTenue(suite);
  return suite;
}

function appliquerTenue(suite) {
  for (let index = 0; index < suite.length; index += 1) {
    const suivant = suite[index + 1];
    const plafond = suivant ? suivant.debut : Number.POSITIVE_INFINITY;
    suite[index].fin = Math.min(suite[index].finVoix + TENUE, plafond);
  }
}

function reunir(gauche, droite) {
  const finVoix = Math.max(gauche.finVoix, droite.finVoix);
  return {
    debut: Math.min(gauche.debut, droite.debut),
    fin: finVoix,
    finVoix,
    text: `${gauche.text}\n${droite.text}`,
    beat: gauche.beat,
    phrase: `${gauche.phrase} ${droite.phrase}`,
  };
}

export async function sousTitresNarration(chapitre) {
  const id = chapitre.beats[0].id.split(".")[0];
  const ref = await lireParole(id);
  const mesures = ref[chapitre.lang];
  if (!mesures) throw Object.assign(new Error(`parole ${chapitre.lang}`), { code: "parole" });
  const dites = [];
  for (const paragraphe of chapitre.paragraphes) {
    for (const phrase of phrases(paragraphe.brut)) {
      const mesure = mesures[dites.length];
      if (!mesure) throw Object.assign(new Error(`parole ${chapitre.lang} ${dites.length + 1}`), { code: "parole" });
      dites.push({
        debut: mesure.debut,
        fin: mesure.fin,
        text: lignesDe(notationNombres(phrase)).join("\n"),
        beat: paragraphe.beat,
        phrase,
      });
    }
  }
  if (dites.length !== mesures.length) {
    throw Object.assign(new Error(`parole ${chapitre.lang} ${dites.length} ${mesures.length}`), { code: "parole" });
  }
  return poserCues(dites);
}

export function texteSousTitre(layer, lang) {
  if (lang === "fr" && layer.fr) return layer.fr;
  return layer.text;
}

export function texteSrt(cues) {
  return `${cues
    .map((cue, index) => `${index + 1}\n${horlogeSrt(cue.debut)} --> ${horlogeSrt(cue.fin)}\n${cue.text}\n`)
    .join("\n")}\n`;
}

function horlogeSrt(secondes) {
  const total = Math.max(0, Math.round(secondes * 1000));
  const heures = Math.floor(total / 3600000);
  const minutes = Math.floor(total / 60000) % 60;
  const secs = Math.floor(total / 1000) % 60;
  const reste = total % 1000;
  const largeur = (valeur, taille) => String(valeur).padStart(taille, "0");
  return `${largeur(heures, 2)}:${largeur(minutes, 2)}:${largeur(secs, 2)},${largeur(reste, 3)}`;
}

function lireValeur(argv, index, arg) {
  const valeur = argv[index];
  if (!valeur || valeur.startsWith("--")) throw Object.assign(new Error(`argument ${arg}`), { code: "argument" });
  return valeur;
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
    if (code === 0) resolve(erreur);
    else reject(new Error(erreur.slice(-2000)));
    });
  });
}

if (process.argv[1] && process.argv[1].endsWith("film.mjs")) {
  principal(process.argv.slice(2), process.env, {
    root: join(ici, ".."),
    stdout: process.stdout,
  }).catch((error) => {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  });
}
