import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { cleCache, ecrire, lire } from "./cache.mjs";
import { ecrireJournal } from "./journal.mjs";
import { brancher, ecrireManifeste, horloges, lireScenes, relier, rendre } from "./pilote.mjs";
import {
  URL_FISH,
  VOIX,
  corps,
  estimer,
  formulerEstimation,
  formulerSynthese,
  preparer,
} from "./parole.mjs";

const ici = dirname(fileURLToPath(import.meta.url));

export function analyser(argv) {
  const opts = {
    chapter: "g10",
    lang: "en",
    dryRun: false,
    estimate: false,
    rendre: false,
    cache: null,
    sortie: null,
    stats: null,
    creneaux: null,
    scenes: null,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === "--dry-run") opts.dryRun = true;
    else if (arg === "--estimate") opts.estimate = true;
    else if (arg === "--rendre") opts.rendre = true;
    else if (arg === "--chapter") opts.chapter = lireValeur(argv, (index += 1), arg);
    else if (arg === "--lang") opts.lang = lireValeur(argv, (index += 1), arg);
    else if (arg === "--cache") opts.cache = lireValeur(argv, (index += 1), arg);
    else if (arg === "--sortie") opts.sortie = lireValeur(argv, (index += 1), arg);
    else if (arg === "--stats") opts.stats = lireValeur(argv, (index += 1), arg);
    else if (arg === "--creneaux") opts.creneaux = lireValeur(argv, (index += 1), arg);
    else if (arg === "--scenes") opts.scenes = lireValeur(argv, (index += 1), arg);
    else throw Object.assign(new Error(`argument ${arg}`), { code: "argument" });
  }
  if (!["en", "fr"].includes(opts.lang)) throw Object.assign(new Error("langue"), { code: "langue" });
  return opts;
}

export function exigerCle(env) {
  const cle = env.FISH_API_KEY;
  if (typeof cle !== "string" || cle.trim() === "") {
    throw Object.assign(new Error("FISH_API_KEY manquante"), { code: "FISH_API_KEY" });
  }
  return cle;
}

export function garderCle(texte, cle) {
  if (cle && texte.includes(cle)) throw Object.assign(new Error("la clé ne sort pas"), { code: "cle" });
  return texte;
}

export function minutesReponse(headers) {
  for (const nom of ["x-billed-minutes", "x-fish-billed-minutes"]) {
    const valeur = headers.get(nom);
    if (valeur == null || valeur === "") continue;
    const nombre = Number(valeur);
    if (Number.isFinite(nombre)) return nombre;
  }
  return null;
}

export async function synthetiser({ chapitre, cacheDir, cle, dryRun = false, fetchImpl = globalThis.fetch }) {
  if (chapitre.lang !== "en" && chapitre.lang !== "fr") {
    throw Object.assign(new Error("langue"), { code: "langue" });
  }
  if (!dryRun) exigerCle({ FISH_API_KEY: cle });
  let requetes = 0;
  let succesCache = 0;
  let prevues = 0;
  let minutes = 0;
  let minutesConnues = true;
  const fichiers = {};
  try {
    for (const paragraphe of chapitre.paragraphes) {
      const key = cleCache({ text: paragraphe.texte, referenceId: VOIX });
      const chemin = join(cacheDir, chapitre.lang, `${paragraphe.id}.mp3`);
      const deja = await lire(cacheDir, key);
      if (deja) {
        succesCache += 1;
        if (!dryRun) {
          await ecrireNomme(chemin, deja);
          fichiers[paragraphe.id] = chemin;
        }
        continue;
      }
      if (dryRun) {
        prevues += 1;
        continue;
      }
      const charge = corps(paragraphe.texte);
      let reponse;
      try {
        reponse = await fetchImpl(URL_FISH, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${cle}`,
            "Content-Type": "application/json",
            model: "drama-3",
          },
          body: JSON.stringify(charge),
        });
      } catch {
        throw Object.assign(new Error("Fish injoignable"), { code: "fish", requetes, succesCache });
      }
      requetes += 1;
      if (!reponse.ok) {
        throw Object.assign(new Error(`Fish ${reponse.status}`), { code: "fish", requetes, succesCache });
      }
      const lu = minutesReponse(reponse.headers);
      if (lu == null) minutesConnues = false;
      else minutes += lu;
      const octets = Buffer.from(await reponse.arrayBuffer());
      await ecrire(cacheDir, key, octets);
      await ecrireNomme(chemin, octets);
      fichiers[paragraphe.id] = chemin;
    }
  } catch (error) {
    error.requetes ??= requetes;
    error.succesCache ??= succesCache;
    throw error;
  }
  if (requetes === 0 || !minutesConnues) minutes = null;
  return { requetes, succesCache, prevues, minutes, fichiers };
}

export async function principal(argv, env, io) {
  const opts = analyser(argv);
  const root = io.root;
  const cache = opts.cache ?? join(root, "tools/.cache/fish");
  if (opts.rendre) {
    const texte = await rendreChapitre({ opts, root, cache });
    io.stdout.write(garderCle(texte, env.FISH_API_KEY));
    return;
  }
  const markdown = await readFile(join(root, "narration", opts.lang, `${opts.chapter}.md`), "utf8");
  const chapitre = preparer(markdown, opts.lang);
  const estimation = estimer(chapitre);
  if (opts.estimate) {
    io.stdout.write(garderCle(formulerEstimation(opts, estimation), env.FISH_API_KEY));
    return;
  }
  const resultat = await synthetiser({
    chapitre,
    cacheDir: cache,
    cle: opts.dryRun ? "" : env.FISH_API_KEY,
    dryRun: opts.dryRun,
    fetchImpl: io.fetchImpl,
  });
  const texte = formulerSynthese(opts, resultat, estimation);
  io.stdout.write(garderCle(texte, env.FISH_API_KEY));
  if (!opts.dryRun) {
    await ecrireManifeste(join(cache, `${opts.chapter}-${opts.lang}.json`), {
      chapter: opts.chapter,
      lang: opts.lang,
      paragraphes: chapitre.paragraphes.map((paragraphe) => ({
        id: paragraphe.id,
        cle: cleCache({ text: paragraphe.texte, referenceId: VOIX }),
        fichier: resultat.fichiers[paragraphe.id],
      })),
    });
    await ecrireJournal(opts.stats ?? join(root, "STATS.md"), resultat);
  }
}

async function rendreChapitre({ opts, root, cache }) {
  const prepares = {};
  for (const lang of ["en", "fr"]) {
    const markdown = await readFile(join(root, "narration", lang, `${opts.chapter}.md`), "utf8");
    const chapitre = preparer(markdown, lang);
    const chemin = join(cache, `${opts.chapter}-${lang}.json`);
    let manifeste;
    try {
      manifeste = JSON.parse(await readFile(chemin, "utf8"));
    } catch (error) {
      if (error.code !== "ENOENT") throw error;
      throw Object.assign(new Error(`audio manquant: ${opts.chapter} ${lang}`), { code: "audio" });
    }
    const fichiers = {};
    for (const paragraphe of chapitre.paragraphes) {
      const ligne = manifeste.paragraphes.find((item) => item.id === paragraphe.id);
      const cle = cleCache({ text: paragraphe.texte, referenceId: VOIX });
      const octets = ligne && ligne.cle === cle ? await lire(cache, ligne.cle) : null;
      if (!octets) throw Object.assign(new Error(`audio manquant: ${paragraphe.id}`), { code: "audio" });
      const chemin = join(cache, lang, `${paragraphe.id}.mp3`);
      await ecrireNomme(chemin, octets);
      fichiers[paragraphe.id] = chemin;
    }
    prepares[lang] = { chapitre, fichiers };
  }
  const scenes = await lireScenes(opts.scenes ?? join(root, "scenes", opts.chapter));
  const sortie = opts.sortie ?? join(cache, `${opts.chapter}-pilote.m4a`);
  const resultat = await rendre({
    en: prepares.en,
    fr: prepares.fr,
    horloges: horloges(scenes),
    sortie,
  });
  const creneaux = opts.creneaux ?? join(root, "scenes", opts.chapter, "cues.json");
  const texte = await readFile(creneaux, "utf8");
  const document = JSON.parse(texte);
  const branche = brancher(document, { en: prepares.en.fichiers, fr: prepares.fr.fichiers }, resultat);
  const mises = [];
  for (let index = 0; index < document.slots.length; index += 1) {
    const avant = document.slots[index];
    const apres = branche.slots[index];
    if (avant === apres) continue;
    mises.push({
      id: apres.id,
      lang: apres.lang,
      audio: apres.audio,
      status: apres.status,
      reason: apres.reason,
    });
  }
  await writeFile(creneaux, relier(texte, mises));
  const lignes = [
    `chapitre: ${opts.chapter}`,
    `sortie: ${sortie}`,
    ...resultat.en.map((beat) => `en ${beat.id}: audio ${beat.audio.toFixed(3)} slot ${beat.slot} ${beat.action}`),
    ...resultat.fr.map((beat) => `fr ${beat.id}: audio ${beat.audio.toFixed(3)} slot ${beat.slot} ${beat.action}`),
    "",
  ];
  return lignes.join("\n");
}

async function ecrireNomme(chemin, octets) {
  await mkdir(dirname(chemin), { recursive: true });
  await writeFile(chemin, octets);
}

function lireValeur(argv, index, arg) {
  const valeur = argv[index];
  if (!valeur || valeur.startsWith("--")) throw Object.assign(new Error(`argument ${arg}`), { code: "argument" });
  return valeur;
}

if (process.argv[1] && process.argv[1].endsWith("tts.mjs")) {
  principal(process.argv.slice(2), process.env, {
    root: join(ici, ".."),
    stdout: process.stdout,
    fetchImpl: globalThis.fetch,
  }).catch((error) => {
    const cle = process.env.FISH_API_KEY;
    const message = error.code === "FISH_API_KEY" ? "FISH_API_KEY manquante" : error.message;
    const sur = cle && message.includes(cle) ? "Fish a échoué" : message;
    process.stderr.write(`${sur}\n`);
    const depense = error.requetes > 0 ? error : null;
    const stats = process.argv.includes("--stats") ? process.argv[process.argv.indexOf("--stats") + 1] : join(ici, "..", "STATS.md");
    const ecrit = depense && !process.argv.includes("--dry-run")
      ? ecrireJournal(stats, { requetes: depense.requetes, succesCache: depense.succesCache ?? 0, minutes: null })
      : Promise.resolve();
    ecrit.then(
      () => {
        process.exitCode = 1;
      },
      () => {
        process.exitCode = 1;
      },
    );
  });
}
