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
import { argumentsPiste, ecrireManifeste } from "../pilote.mjs";
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

test("chaque sous-titre suit la voix mesurée sur la piste mélangée", async () => {
  const dir = await mkdtemp(join(tmpdir(), "sync-"));
  const rate = 44100;
  for (const lang of ["en", "fr"]) {
    const markdown = await readFile(join(root, "narration", lang, "g10.md"), "utf8");
    const chapitre = preparer(markdown, lang);
    const lignes = tableau(chapitre);
    const durees = new Map();
    const fichiers = new Map();
    let raccourci = false;
    for (const paragraphe of chapitre.paragraphes) {
      const parties = [];
      const dites = phrases(paragraphe.brut);
      dites.forEach((phrase, index) => {
        const court = !raccourci && index > 0;
        if (court) raccourci = true;
        if (index > 0) parties.push(new Float64Array(Math.round(0.4 * rate)));
        parties.push(ton(court ? 0.45 : 1.25, rate));
      });
      parties.push(new Float64Array(Math.round(0.25 * rate)));
      const samples = coller(parties);
      const chemin = join(dir, `${lang}-${paragraphe.id.replaceAll(".", "-")}.wav`);
      await ecrireWav(chemin, samples, rate);
      durees.set(paragraphe.id, samples.length / rate);
      fichiers.set(paragraphe.id, chemin);
    }
    let origine = 0;
    const clips = [];
    for (const ligne of lignes) {
      const beat = chapitre.beats.find((item) => item.id === ligne.id);
      const place = placer(beat.paragraphes, durees);
      for (const pose of place.poses) clips.push({ fichier: fichiers.get(pose.id), at: origine + pose.at, atempo: null });
      origine += ligne.slot;
    }
    const mix = join(dir, `${lang}-mix.wav`);
    const melange = spawnSync("ffmpeg", [...argumentsPiste(clips, origine), mix], { encoding: "utf8" });
    assert.equal(melange.status, 0, melange.stderr);
    const voix = voixMesuree(mix);
    const dites = chapitre.paragraphes.flatMap((paragraphe) => phrases(paragraphe.brut));
    assert.equal(voix.length, dites.length, `${lang} ${voix.length} voix, ${dites.length} phrases`);
    const cues = await sousTitresNarration(lignes, chapitre, durees, fichiers);
    let curseur = 0;
    let pireDepart = 0;
    let pireFin = 0;
    for (const cue of cues) {
      const debut = voix[curseur].debut;
      let fin = voix[curseur].fin;
      let reste = contrat(cue.text);
      const premiere = contrat(dites[curseur]);
      assert.equal(reste.includes(premiere), true, `${lang} ${premiere}`);
      reste = reste.slice(reste.indexOf(premiere) + premiere.length).trim();
      curseur += 1;
      while (curseur < dites.length && reste.startsWith(contrat(dites[curseur]))) {
        fin = voix[curseur].fin;
        const suivante = contrat(dites[curseur]);
        reste = reste.slice(suivante.length).trim();
        curseur += 1;
      }
      const depart = Math.abs(cue.debut - debut);
      const anticipe = fin - cue.fin;
      pireDepart = Math.max(pireDepart, depart);
      pireFin = Math.max(pireFin, anticipe);
      assert.ok(depart <= 0.15, `${lang} départ ${depart.toFixed(3)} ${cue.text}`);
      assert.ok(anticipe <= 0.03, `${lang} fin ${anticipe.toFixed(3)} ${cue.text}`);
    }
    assert.equal(curseur, dites.length, lang);
    console.log(`écart ${lang}: départ ${pireDepart.toFixed(3)} s, fin anticipée ${pireFin.toFixed(3)} s`);
  }
});

function ton(secondes, rate) {
  const samples = new Float64Array(Math.round(secondes * rate));
  for (let index = 0; index < samples.length; index += 1) {
    samples[index] = 0.4 * Math.sin((2 * Math.PI * 440 * index) / rate);
  }
  return samples;
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

function voixMesuree(fichier) {
  const probe = spawnSync(
    "ffprobe",
    ["-v", "error", "-show_entries", "format=duration", "-of", "json", fichier],
    { encoding: "utf8" },
  );
  assert.equal(probe.status, 0, probe.stderr);
  const duree = Number(JSON.parse(probe.stdout).format.duration);
  const detecte = spawnSync(
    "ffmpeg",
    ["-i", fichier, "-af", "silencedetect=noise=-40dB:d=0.15", "-f", "null", "-"],
    { encoding: "utf8" },
  );
  const silences = [];
  const debuts = [...detecte.stderr.matchAll(/silence_start: ([0-9.]+)/g)].map((match) => Number(match[1]));
  const fins = [...detecte.stderr.matchAll(/silence_end: ([0-9.]+)/g)].map((match) => Number(match[1]));
  debuts.forEach((start, index) => silences.push({ start, end: fins[index] ?? duree }));
  const voix = [];
  let curseur = 0;
  for (const silence of silences) {
    if (silence.start - curseur > 0.05) voix.push({ debut: curseur, fin: silence.start });
    curseur = silence.end;
  }
  if (duree - curseur > 0.05) voix.push({ debut: curseur, fin: duree });
  return voix;
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
