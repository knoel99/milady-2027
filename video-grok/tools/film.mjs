import { spawn, spawnSync } from "node:child_process";
import { copyFile, mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { capturer } from "./capture.mjs";
import { preparer } from "./parole.mjs";
import { lireScenes } from "./pilote.mjs";
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

export function dureeTableau(lignes) {
  return lignes.reduce((somme, ligne) => somme + ligne.slot, 0);
}

export function argumentsMontage({ lignes, clips, pistes, sortie }) {
  if (clips.length !== lignes.length) {
    throw Object.assign(new Error("clips"), { code: "clips" });
  }
  const args = ["-y"];
  for (const clip of clips) args.push("-i", clip);
  args.push("-i", pistes);
  const audio = clips.length;
  const filtres = lignes.map((ligne, index) => {
    const duree = ligne.slot;
    return `[${index}:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=${duree},trim=duration=${duree},setpts=PTS-STARTPTS[v${index}]`;
  });
  filtres.push(`${lignes.map((_, index) => `[v${index}]`).join("")}concat=n=${lignes.length}:v=1:a=0[v]`);
  args.push(
    "-filter_complex",
    filtres.join(";"),
    "-map",
    "[v]",
    "-map",
    `${audio}:a:0`,
    "-map",
    `${audio}:a:1`,
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
    "language=eng",
    "-metadata:s:a:1",
    "language=fra",
    "-movflags",
    "+faststart",
    "-t",
    String(dureeTableau(lignes)),
    sortie,
  );
  return args;
}

export async function monter({ lignes, clips, pistes, sortie }) {
  await executer("ffmpeg", argumentsMontage({ lignes, clips, pistes, sortie }));
  return { sortie, duree: dureeTableau(lignes) };
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
    const clips = opts.clips
      ? lignes.map((ligne) => join(opts.clips, `${ligne.nom}.mp4`))
      : await capturerBeats({ root, chapter: opts.chapter, lignes, scenes, dossier });
    const resultat = await monter({ lignes, clips, pistes, sortie: opts.sortie });
    io.stdout.write(
      garderCle(
        `chapitre: ${opts.chapter}\nsortie: ${opts.sortie}\nvideo: ${resultat.duree}\naudio: eng fra\n`,
        env.FISH_API_KEY,
      ),
    );
    return resultat;
  } finally {
    await rm(dossier, { recursive: true, force: true });
  }
}

async function capturerBeats({ root, chapter, lignes, scenes, dossier }) {
  const server = await servir(root);
  const clips = [];
  try {
    for (const ligne of lignes) {
      const scene = scenes.find((item) => item.id === ligne.id);
      const ouverture = [...scene.cues].sort((a, b) => a.at - b.at)[0];
      const sortie = join(dossier, `${ligne.nom}.mp4`);
      await capturer({
        url: `http://127.0.0.1:${server.port}/scenes/${chapter}/${ligne.nom}.html`,
        repere: ouverture.id,
        secondes: Math.min(scene.duration, ligne.slot),
        sortie,
      });
      clips.push(sortie);
    }
  } finally {
    await server.close();
  }
  return clips;
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
      if (code === 0) resolve();
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
