import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdir, mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { cleCache, ecrire } from "../cache.mjs";
import { ecrireWav } from "../kit-voix/aligner.mjs";
import { VOIX, preparer } from "../parole.mjs";
import { ecrireManifeste } from "../pilote.mjs";
import { ecouter, syntheseMot } from "../calage.mjs";
import { dureeTableau, sousTitresNarration, tableau, texteSousTitre } from "../film.mjs";
import { lireScenes, placer } from "../pilote.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "../..");
const film = join(here, "../film.mjs");

test("le tableau du film suit les créneaux de g10", async () => {
  const chapitre = preparer(await readFile(join(root, "narration/en/g10.md"), "utf8"), "en");
  const lignes = tableau(chapitre);
  assert.deepEqual(
    lignes.map((ligne) => [ligne.id, ligne.slot, ligne.nom]),
    [
      ["g10.classes", 45, "classes"],
      ["g10.hard", 43, "hard"],
      ["g10.sym", 30, "sym"],
      ["g10.law", 39, "law"],
      ["g10.sample", 45, "sample"],
      ["g10.bias", 25, "bias"],
      ["g10.close", 17, "close"],
      ["g10.card", 8, "card"],
    ],
  );
  assert.equal(dureeTableau(lignes), 252);
});

test("chaque sous-titre français vient du script français", async () => {
  const anglais = await readFile(join(root, "narration/en/g10.md"), "utf8");
  const francais = await readFile(join(root, "narration/fr/g10.md"), "utf8");
  const scenes = await lireScenes(join(root, "scenes/g10"));
  const couches = scenes.flatMap((scene) => (scene.layers ?? []).filter((layer) => layer.kind === "subtitle"));
  assert.equal(couches.length, 47);
  for (const layer of couches) {
    const en = texteSousTitre(layer, "en");
    const fr = texteSousTitre(layer, "fr");
    assert.equal(francais.includes(fr), true, fr);
    if (fr === en) assert.equal(anglais.includes(fr), true, fr);
  }
});

const PUISSANCE = "⁰¹²³⁴⁵⁶⁷⁸⁹";

function puissance(chiffres) {
  return `⁻${[...String(chiffres)].map((chiffre) => PUISSANCE[Number(chiffre)]).join("")}`;
}

function contrat(texte) {
  return texte
    .replace(/(\d+(?:\.\d+)?) times 10 to the minus (\d+)/gi, (_, nombre, exposant) => `${nombre} × 10${puissance(exposant)}`)
    .replace(/about 10 to the minus (\d+)/gi, (_, exposant) => `about 10${puissance(exposant)}`)
    .replace(/(\d+(?:,\d+)?) fois 10 à la puissance moins (\d+)/gi, (_, nombre, exposant) => `${nombre} × 10${puissance(exposant)}`)
    .replace(/environ 10 à la puissance moins (\d+)/gi, (_, exposant) => `environ 10${puissance(exposant)}`)
    .replace(/\u00a0/g, " ")
    .replace(/\s+/g, " ")
    .trim();
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

function estNombreSeul(texte) {
  const nu = texte.replaceAll("\n", " ").replaceAll("\u00a0", " ").replace(/[.!?]+$/g, "").trim();
  return /^(?:\d+(?:[.,]\d+)?|\d+(?:[.,]\d+)?\s*×\s*10[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+|10[⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)$/.test(nu);
}

test("chaque sous-titre couvre le premier et le dernier mot dit", async () => {
  const dir = await mkdtemp(join(tmpdir(), "sync-"));
  const preuves = [
    ["en", "V0 leaves a divergence of 0.408."],
    ["en", "A soft penalty leaves 0.34 on the velocity and 0.162 on the magnetic field, and the magnetic energy is too high."],
    ["en", "Potentials and the final projection fall to about 10 to the minus 17."],
    ["en", "The projected flow falls to 2.03 times 10 to the minus 8."],
    ["en", "Those constructions force the rule in the architecture or at the last step."],
    ["en", "The honest floor, on the training values of eta, the magnetic diffusivity, is 0.0304."],
    ["en", "Dissipation spread divided by reference spread is 8.64 times 10 to the minus 4."],
    ["fr", "V0 laisse une divergence de 0,408."],
    ["fr", "Une pénalité souple laisse 0,34 sur la vitesse et 0,162 sur le champ magnétique, et l’énergie magnétique est trop haute."],
    ["fr", "Les potentiels et la projection finale tombent à environ 10 à la puissance moins 17."],
    ["fr", "Le flot projeté tombe à 2,03 fois 10 à la puissance moins 8."],
    ["fr", "E2, résidu de 8,27 fois 10 à la puissance moins 6."],
    ["fr", "L’écart-type de dissipation sur l’écart-type de référence vaut 8,64 fois 10 à la puissance moins 4."],
  ];
  for (const lang of ["en", "fr"]) {
    const markdown = await readFile(join(root, "narration", lang, "g10.md"), "utf8");
    const chapitre = preparer(markdown, lang);
    const lignes = tableau(chapitre);
    const durees = new Map();
    const fichiers = new Map();
    for (const paragraphe of chapitre.paragraphes) {
      const dites = phrases(paragraphe.brut);
      const parties = [];
      for (let index = 0; index < dites.length; index += 1) {
        if (index > 0) {
          const pause = /\d/.test(dites[index]) ? 0.9 : 0.35 + (index % 4) * 0.22;
          parties.push(silence(pause, 22050));
        }
        const rendu = await syntheseMot(dites[index], lang);
        parties.push(rendu.samples);
      }
      parties.push(silence(0.25, 22050));
      const samples = coller(parties);
      const chemin = join(dir, `${lang}-${paragraphe.id.replaceAll(".", "-")}.wav`);
      await ecrireWav(chemin, samples, 22050);
      durees.set(paragraphe.id, samples.length / 22050);
      fichiers.set(paragraphe.id, chemin);
    }
    let origine = 0;
    const posesMix = [];
    for (const ligne of lignes) {
      const beat = chapitre.beats.find((item) => item.id === ligne.id);
      const place = placer(beat.paragraphes, durees);
      ligne.slot = place.fin + 0.5;
      beat.slot = ligne.slot;
      for (const pose of place.poses) posesMix.push({ id: pose.id, at: origine + pose.at });
      origine += ligne.slot;
    }
    const mix = new Float64Array(Math.ceil((origine + 1) * 22050));
    for (const pose of posesMix) {
      const samples = await readWav(fichiers.get(pose.id));
      mix.set(samples, Math.round(pose.at * 22050));
    }
    const cheminMix = join(dir, `${lang}-mix.wav`);
    await ecrireWav(cheminMix, mix, 22050);
    const oreille = ecouter([{ id: "mix", audio: cheminMix, langue: lang }]).mix;
    const dites = chapitre.paragraphes.flatMap((paragraphe) => phrases(paragraphe.brut));
    const fenetres = placerSegments(dites, oreille.segments ?? []);
    const paroles = fenetres.map((fenetre) => borneRms(fenetre, oreille.regions ?? []));
    const cues = await sousTitresNarration(lignes, chapitre, durees, fichiers);
    let pireTot = 0;
    let pireTard = 0;
    let pireFin = 0;
    let indice = 0;
    const lignesCue = [];
    for (const [numero, cue] of cues.entries()) {
      const texte = contrat(cue.text);
      const couvertes = [];
      while (indice < paroles.length && texte.includes(contrat(paroles[indice].phrase))) {
        couvertes.push(paroles[indice]);
        indice += 1;
      }
      assert.ok(couvertes.length > 0, `${lang} ${cue.text}`);
      const parole = couvertes[0];
      const finParole = couvertes[couvertes.length - 1].fin;
      const tot = parole.debut - cue.debut;
      const tard = cue.debut - parole.debut;
      const anticipe = finParole - cue.fin;
      const duree = cue.fin - cue.debut;
      pireTot = Math.max(pireTot, tot);
      pireTard = Math.max(pireTard, tard);
      pireFin = Math.max(pireFin, anticipe);
      lignesCue.push(
        `${lang}\t${numero + 1}\t${cue.debut.toFixed(3)}\t${cue.fin.toFixed(3)}\t${parole.debut.toFixed(3)}\t${finParole.toFixed(3)}\t${tot.toFixed(3)}\t${tard.toFixed(3)}\t${anticipe.toFixed(3)}\t${duree.toFixed(3)}\t${couvertes[0].phrase.slice(0, 72)}`,
      );
      assert.ok(duree >= 1 - 1e-6, `${lang} ${duree.toFixed(3)} ${couvertes[0].phrase}`);
      assert.ok(tot <= 0.35, `${lang} tôt ${tot.toFixed(3)} ${couvertes[0].phrase}`);
      assert.ok(tard <= 0.2, `${lang} tard ${tard.toFixed(3)} ${couvertes[0].phrase}`);
      assert.ok(anticipe <= 0, `${lang} fin ${anticipe.toFixed(3)} ${couvertes.at(-1).phrase}`);
    }
    assert.equal(indice, paroles.length, lang);
    for (const [langue, extrait] of preuves) {
      if (langue !== lang) continue;
      const cle = contrat(extrait).slice(0, 24);
      const parole = paroles.find((item) => contrat(item.phrase).includes(cle));
      const cue = cues.find((item) => contrat(item.text).includes(cle));
      assert.ok(parole && cue, extrait);
      const tot = parole.debut - cue.debut;
      const tard = cue.debut - parole.debut;
      assert.ok(tot <= 0.35 && tard <= 0.2, extrait);
      assert.ok(cue.fin >= parole.fin, extrait);
      assert.ok(cue.fin - cue.debut >= 1 - 1e-6, extrait);
    }
    console.log(`cue\tdebut\tfin\tvoixDebut\tvoixFin\ttot\ttard\tfinAnticipee\tduree\ttexte`);
    console.log(lignesCue.join("\n"));
    console.log(`écart ${lang}: tôt ${pireTot.toFixed(3)} s, tard ${pireTard.toFixed(3)} s, fin anticipée ${pireFin.toFixed(3)} s`);
  }
});

function jetonsOreille(texte) {
  return texte
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{Diacritic}/gu, "")
    .replace(/[^a-z0-9]+/g, " ")
    .trim()
    .split(/\s+/)
    .filter((mot) => mot.length > 2);
}

function scoreOreille(phrase, texte) {
  const attendus = jetonsOreille(phrase);
  const entendus = new Set(jetonsOreille(texte));
  const mots = attendus.length === 0 || entendus.size === 0
    ? 0
    : attendus.filter((mot) => entendus.has(mot)).length / attendus.length;
  const chiffresPhrase = (phrase.match(/\d/g) ?? []).join("");
  const chiffresTexte = (texte.match(/\d/g) ?? []).join("");
  const nombres = chiffresPhrase && chiffresTexte && (chiffresTexte.includes(chiffresPhrase) || chiffresPhrase.includes(chiffresTexte)) ? 0.45 : 0;
  return Math.min(1, mots + nombres);
}

function placerSegments(phrases, segments) {
  if (phrases.length === 0) return [];
  if (segments.length === 0) return phrases.map((phrase) => ({ phrase, debut: 0, fin: 0 }));
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
        const prix = 1 - scoreOreille(phrases[i], segments[j].texte);
        if (cout[i][j] + prix < cout[i + 1][j + 1]) {
          cout[i + 1][j + 1] = cout[i][j] + prix;
          choix[i + 1][j + 1] = [i, j, 1];
        }
      }
      if (i < n && j + 1 < m) {
        const prix = 1 - scoreOreille(phrases[i], `${segments[j].texte} ${segments[j + 1].texte}`) + 0.05;
        if (cout[i][j] + prix < cout[i + 1][j + 2]) {
          cout[i + 1][j + 2] = cout[i][j] + prix;
          choix[i + 1][j + 2] = [i, j, 2];
        }
      }
      if (i + 1 < n && j < m) {
        const prix = 1 - Math.max(scoreOreille(phrases[i], segments[j].texte), scoreOreille(phrases[i + 1], segments[j].texte)) + 0.08;
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
    if (mode === 1) fenetres[pi] = { phrase: phrases[pi], debut: segments[pj].debut, fin: segments[pj].fin };
    else if (mode === 2) fenetres[pi] = { phrase: phrases[pi], debut: segments[pj].debut, fin: segments[pj + 1].fin };
    else {
      const milieu = (segments[pj].debut + segments[pj].fin) / 2;
      fenetres[pi] = { phrase: phrases[pi], debut: segments[pj].debut, fin: milieu };
      fenetres[pi + 1] = { phrase: phrases[pi + 1], debut: milieu, fin: segments[pj].fin };
    }
  }
  return fenetres;
}

function borneRms(fenetre, regions) {
  let debut = fenetre.debut;
  let fin = fenetre.fin;
  let vu = false;
  for (const region of regions) {
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
  return { phrase: fenetre.phrase, debut, fin };
}

async function readWav(chemin) {
  const { samples } = await import("../kit-voix/aligner.mjs").then((module) => module.lireWav(chemin));
  return samples;
}

function silence(secondes, rate) {
  return new Float64Array(Math.round(secondes * rate));
}

function coller(parties) {
  const total = parties.reduce((somme, partie) => somme + partie.length, 0);
  const samples = new Float64Array(total);
  let curseur = 0;
  for (const partie of parties) {
    samples.set(partie, curseur);
    curseur += partie.length;
  }
  return samples;
}

test("aucun sous-titre n'est trop court pour se lire", async () => {
  for (const lang of ["en", "fr"]) {
    const markdown = await readFile(join(root, "narration", lang, "g10.md"), "utf8");
    const chapitre = preparer(markdown, lang);
    const durees = new Map(chapitre.paragraphes.map((paragraphe) => [paragraphe.id, 8]));
    const cues = await sousTitresNarration(tableau(chapitre), chapitre, durees);
    const lignes = new Set(
      phrases(contrat(chapitre.paragraphes.map((paragraphe) => paragraphe.brut).join(" "))).filter(
        (phrase) => phrase.replace(/[.!?]+$/g, "").trim().split(/\s+/).length <= 1,
      ),
    );
    for (const cue of cues) {
      const duree = cue.fin - cue.debut;
      assert.ok(duree >= 1 - 1e-6, `${lang} ${duree.toFixed(3)} ${cue.text}`);
      const plat = contrat(cue.text);
      const mots = plat.replace(/[.!?]+$/g, "").trim().split(/\s+/).filter(Boolean);
      if (mots.length > 1 && !estNombreSeul(plat)) continue;
      assert.equal(lignes.has(plat), true, `${lang} ${plat}`);
    }
  }
});

test("la piste entière égale le script parlé", async () => {
  for (const lang of ["en", "fr"]) {
    const markdown = await readFile(join(root, "narration", lang, "g10.md"), "utf8");
    const chapitre = preparer(markdown, lang);
    const durees = new Map(chapitre.paragraphes.map((paragraphe) => [paragraphe.id, 8]));
    const cues = await sousTitresNarration(tableau(chapitre), chapitre, durees);
    const lu = contrat(cues.map((cue) => cue.text).join(" "));
    const voulu = contrat(chapitre.paragraphes.map((paragraphe) => paragraphe.brut).join(" "));
    assert.equal(lu, voulu, lang);
    assert.equal(chapitre.paragraphes.some((paragraphe) => paragraphe.id === "cue.g10.sample.formula"), false);
  }
});

test("chaque beat porte le texte parlé, l'exposant et la conclusion", async () => {
  for (const lang of ["en", "fr"]) {
    const markdown = await readFile(join(root, "narration", lang, "g10.md"), "utf8");
    const chapitre = preparer(markdown, lang);
    const durees = new Map(chapitre.paragraphes.map((paragraphe) => [paragraphe.id, 8]));
    const lignes = tableau(chapitre);
    const cues = await sousTitresNarration(lignes, chapitre, durees);
    let origine = 0;
    for (const ligne of lignes) {
      const beat = chapitre.beats.find((item) => item.id === ligne.id);
      const duBeat = cues.filter((cue) => cue.beat === beat.id);
      const lu = contrat(duBeat.map((cue) => cue.text).join(" "));
      const voulu = contrat(beat.paragraphes.map((paragraphe) => paragraphe.brut).join(" "));
      assert.equal(lu, voulu, `${lang} ${beat.id}`);
      const place = placer(beat.paragraphes, durees);
      const debutAudio = origine + place.poses[0].at;
      const finAudio = origine + place.poses.at(-1).fin;
      for (const cue of duBeat) {
        assert.ok(cue.debut >= debutAudio - 1e-6 && cue.fin <= finAudio + 1e-6, `${cue.text} hors voix`);
        assert.ok(cue.fin > cue.debut, cue.text);
        const lignesBloc = cue.text.split("\n");
        assert.ok(lignesBloc.every((item) => item.length <= 42 || !item.includes(" ")), cue.text);
      }
      for (let index = 1; index < duBeat.length; index += 1) {
        assert.ok(duBeat[index].debut >= duBeat[index - 1].fin - 1e-9, beat.id);
      }
      const textes = duBeat.map((cue) => contrat(cue.text));
      for (const phrase of phrases(voulu)) {
        const tient = textes.some((texte, index) => [texte, textes[index + 1]].filter(Boolean).join(" ").includes(phrase));
        assert.equal(tient, true, `${lang} ${phrase}`);
      }
      origine += ligne.slot;
    }
    const tout = contrat(cues.map((cue) => cue.text).join(" "));
    for (const match of markdown.matchAll(/(\d+(?:[.,]\d+)?) (?:times 10 to the minus|fois 10 à la puissance moins) (\d+)/gi)) {
      assert.equal(tout.includes(`${match[1]} × 10${puissance(match[2])}`), true, match[0]);
    }
    for (const match of markdown.matchAll(/(?:about 10 to the minus|environ 10 à la puissance moins) (\d+)/gi)) {
      assert.equal(tout.includes(`10${puissance(match[1])}`), true, match[0]);
    }
  }
  const anglais = preparer(await readFile(join(root, "narration/en/g10.md"), "utf8"), "en");
  const francais = preparer(await readFile(join(root, "narration/fr/g10.md"), "utf8"), "fr");
  const cuesAnglais = await sousTitresNarration(tableau(anglais), anglais, new Map(anglais.paragraphes.map((item) => [item.id, 8])));
  const cuesFrancais = await sousTitresNarration(tableau(francais), francais, new Map(francais.paragraphes.map((item) => [item.id, 8])));
  const ligneFlot = (cues, nombre) =>
    cues.flatMap((cue) => cue.text.split("\n")).find((ligne) => ligne.replaceAll("\u00a0", " ").includes(nombre));
  assert.match(ligneFlot(cuesAnglais, "2.03").replaceAll("\u00a0", " "), /2\.03 × 10⁻⁸/);
  assert.match(ligneFlot(cuesFrancais, "2,03").replaceAll("\u00a0", " "), /2,03 × 10⁻⁸/);
  for (const [cues, amorce, conclusion] of [
    [cuesAnglais, "A positive variance does not prove", "there is no mass at 0"],
    [cuesFrancais, "Une variance positive ne prouve pas", "absence de masse en 0"],
  ]) {
    const index = cues.findIndex((cue) => contrat(cue.text).includes(amorce));
    assert.ok(index >= 0, amorce);
    const voisin = [cues[index], cues[index + 1]].filter(Boolean).map((cue) => contrat(cue.text)).join(" ");
    assert.equal(voisin.includes(conclusion), true, amorce);
  }
});

test("le film tient 248 s et marque les pistes eng et fra", async () => {
  const dir = await mkdtemp(join(tmpdir(), "film-"));
  const cache = join(dir, "cache");
  const wav = join(dir, "note.wav");
  await ecrireWav(wav, note(8000, 0.2), 8000);
  const octets = await readFile(wav);
  for (const lang of ["en", "fr"]) {
    const markdown = await readFile(join(root, "narration", lang, "g10.md"), "utf8");
    const chapitre = preparer(markdown, lang);
    const paragraphes = chapitre.paragraphes.map((paragraphe) => ({
      id: paragraphe.id,
      cle: cleCache({ text: paragraphe.texte, referenceId: VOIX }),
      fichier: wav,
    }));
    for (const paragraphe of paragraphes) await ecrire(cache, paragraphe.cle, octets);
    await ecrireManifeste(join(cache, `g10-${lang}.json`), { chapter: "g10", lang, paragraphes });
  }
  const clips = join(dir, "clips");
  await mkdir(clips);
  for (const nom of ["classes", "hard", "sym", "law", "sample", "bias", "close", "card"]) {
    const image = spawnSync(
      "ffmpeg",
      ["-y", "-f", "lavfi", "-i", "color=c=black:s=320x240:r=30:d=0.2", "-c:v", "libx264", "-pix_fmt", "yuv420p", join(clips, `${nom}.mp4`)],
      { encoding: "utf8" },
    );
    assert.equal(image.status, 0, image.stderr);
  }
  const cuesAvant = await readFile(join(root, "scenes/g10/cues.json"), "utf8");
  const sortie = join(dir, "pilote");
  const resultat = spawnSync(
    process.execPath,
    ["--import", join(here, "bloquer-reseau.mjs"), film, "--chapter", "g10", "--cache", cache, "--clips", clips, "--sortie", sortie],
    { encoding: "utf8", env: { ...process.env, FISH_API_KEY: "poisson-cle-film" } },
  );
  assert.equal(resultat.status, 0, resultat.stderr);
  assert.equal(resultat.stdout.includes("poisson-cle-film"), false);
  assert.match(resultat.stdout, /video: 252/);
  assert.equal(await readFile(join(root, "scenes/g10/cues.json"), "utf8"), cuesAvant);
  for (const [fichier, langue] of [
    [`${sortie}-en.mp4`, "eng"],
    [`${sortie}-fr.mp4`, "fra"],
  ]) {
    const probe = spawnSync(
      "ffprobe",
      ["-v", "error", "-count_frames", "-show_entries", "stream=codec_type,duration,nb_read_frames:stream_tags=language", "-of", "json", fichier],
      { encoding: "utf8" },
    );
    assert.equal(probe.status, 0, probe.stderr);
    const streams = JSON.parse(probe.stdout).streams;
    const video = streams.filter((stream) => stream.codec_type === "video");
    const audio = streams.filter((stream) => stream.codec_type === "audio");
    const sous = streams.filter((stream) => stream.codec_type === "subtitle");
    assert.equal(video.length, 1, langue);
    assert.equal(audio.length, 1, langue);
    assert.equal(sous.length, 1, langue);
    assert.equal(Number(video[0].duration), 252, langue);
    assert.equal(Number(video[0].nb_read_frames), 7560, langue);
    assert.equal(audio[0].tags.language, langue);
    assert.equal(sous[0].tags.language, langue);
    const piste = spawnSync("ffmpeg", ["-y", "-i", fichier, "-map", "0:s:0", "-f", "srt", "-"], { encoding: "utf8" });
    assert.equal(piste.status, 0, piste.stderr);
    const texte = piste.stdout.replaceAll("\u00a0", " ").replace(/\s+/g, " ");
    if (langue === "eng") {
      assert.match(texte, /2\.03 × 10⁻⁸/);
      assert.match(texte, /there is no mass at 0/);
    } else {
      assert.match(texte, /2,03 × 10⁻⁸/);
      assert.match(texte, /absence de masse en 0/);
    }
  }
});

function note(rate, seconds) {
  const samples = new Float64Array(Math.round(rate * seconds));
  for (let index = 0; index < samples.length; index += 1) {
    samples[index] = 0.2 * Math.sin((2 * Math.PI * 440 * index) / rate);
  }
  return samples;
}
