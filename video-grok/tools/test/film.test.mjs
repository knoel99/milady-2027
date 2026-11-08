import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdir, mkdtemp, readFile, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { cleCache, ecrire } from "../cache.mjs";
import { ecrireWav } from "../kit-voix/aligner.mjs";
import { VOIX, preparer } from "../parole.mjs";
import { ecrireManifeste } from "../pilote.mjs";
import { dureeTableau, empreinteAac, lireParole, monter, poserCues, sousTitresNarration, tableau, texteSousTitre, texteSrt, verifierEmpreinte } from "../film.mjs";
import { lireScenes } from "../pilote.mjs";

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

test("chaque sous-titre couvre la parole mesurée", async () => {
  const ref = await lireParole("g10");
  assert.equal(ref.sha256.en, "6c96dca1ae84f6a3ff20468ec5f6b52920f3e130d1b25f65e69a684026656d12");
  assert.equal(ref.sha256.fr, "af074e982c45ead963bfea5332f8d392e939d32a7044a8eb6dc1650d3981fb62");
  assert.equal(ref.en.length, 52);
  assert.equal(ref.fr.length, 51);
  for (const lang of ["en", "fr"]) {
    const markdown = await readFile(join(root, "narration", lang, "g10.md"), "utf8");
    const chapitre = preparer(markdown, lang);
    const dites = chapitre.paragraphes.flatMap((paragraphe) => phrases(paragraphe.brut));
    assert.equal(dites.length, ref[lang].length, lang);
    const cues = await sousTitresNarration(chapitre);
    let indice = 0;
    let pireTot = 0;
    let pireTard = 0;
    let pireFin = 0;
    const lignesCue = [];
    for (const [numero, cue] of cues.entries()) {
      const texte = contrat(cue.text);
      const couvertes = [];
      while (indice < dites.length && texte.includes(contrat(dites[indice]))) {
        couvertes.push({ phrase: dites[indice], ...ref[lang][indice] });
        indice += 1;
      }
      assert.ok(couvertes.length > 0, `${lang} ${cue.text}`);
      const parole = couvertes[0];
      const finParole = couvertes[couvertes.length - 1].fin;
      const suivant = cues[numero + 1];
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
      assert.ok(anticipe <= 1e-6, `${lang} fin ${anticipe.toFixed(3)} ${couvertes.at(-1).phrase}`);
      assert.ok(cue.fin <= finParole + 0.3 + 1e-6, `${lang} tenue ${couvertes.at(-1).phrase}`);
      for (const phrase of couvertes) {
        assert.ok(cue.debut <= phrase.debut + 1e-6, phrase.phrase);
        assert.ok(cue.fin + 1e-6 >= phrase.fin, phrase.phrase);
      }
      if (suivant) assert.ok(cue.fin <= suivant.debut + 1e-6, `${lang} ${numero + 1}`);
    }
    assert.equal(indice, dites.length, lang);
    for (let index = 1; index < cues.length; index += 1) {
      assert.ok(cues[index].debut + 1e-6 >= cues[index - 1].fin, `${lang} ${index}`);
      assert.ok(cues[index].fin - cues[index].debut >= 1 - 1e-6, `${lang} ${index}`);
    }
    console.log(`cue\tdebut\tfin\tvoixDebut\tvoixFin\ttot\ttard\tfinAnticipee\tduree\ttexte`);
    console.log(lignesCue.join("\n"));
    console.log(`écart ${lang}: tôt ${pireTot.toFixed(3)} s, tard ${pireTard.toFixed(3)} s, fin anticipée ${pireFin.toFixed(3)} s`);
  }
});

test("un cue s'arrête avant le suivant, quitte à fusionner", () => {
  const ranges = poserCues([
    { debut: 0, fin: 0.4, text: "The field flips.", phrase: "The field flips.", beat: "a" },
    { debut: 0.5, fin: 1.2, text: "The flow falls.", phrase: "The flow falls.", beat: "a" },
  ]);
  assert.equal(ranges.length, 1);
  assert.match(ranges[0].text, /field flips/);
  assert.match(ranges[0].text, /flow falls/);
  assert.ok(ranges[0].fin - ranges[0].debut >= 1 - 1e-6);
  const bornes = poserCues([
    { debut: 0, fin: 2, text: "The field flips.", phrase: "The field flips.", beat: "a" },
    { debut: 2.1, fin: 4, text: "The flow falls.", phrase: "The flow falls.", beat: "a" },
  ]);
  assert.equal(bornes.length, 2);
  assert.equal(bornes[0].text, "The field flips.");
  assert.ok(bornes[0].fin <= bornes[1].debut + 1e-9);
  assert.ok(bornes[0].fin <= 2.3 + 1e-9);
  assert.ok(bornes[0].fin + 1e-9 >= 2);
  assert.ok(bornes[1].fin - bornes[1].debut >= 1 - 1e-6);
});

test("une empreinte différente arrête le rendu", async () => {
  const dir = await mkdtemp(join(tmpdir(), "empreinte-"));
  const wav = join(dir, "note.wav");
  const m4a = join(dir, "pistes.m4a");
  await ecrireWav(wav, note(8000, 0.2), 8000);
  const mix = spawnSync("ffmpeg", ["-y", "-i", wav, "-i", wav, "-map", "0:a", "-map", "1:a", "-c:a", "aac", "-b:a", "192k", m4a], { encoding: "utf8" });
  assert.equal(mix.status, 0, mix.stderr);
  const ref = await lireParole("g10");
  assert.notEqual(empreinteAac(m4a, 0), ref.sha256.en);
  assert.throws(() => verifierEmpreinte(m4a, ref), /empreinte/);
  const cache = join(dir, "cache");
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
  const sortie = join(dir, "pilote");
  const resultat = spawnSync(
    process.execPath,
    ["--import", join(here, "bloquer-reseau.mjs"), film, "--chapter", "g10", "--cache", cache, "--sortie", sortie],
    { encoding: "utf8", env: { ...process.env, FISH_API_KEY: "poisson-cle-film" } },
  );
  assert.notEqual(resultat.status, 0);
  assert.match(resultat.stderr, /empreinte/);
  assert.match(resultat.stderr, new RegExp(ref.sha256.en));
  assert.match(resultat.stderr, new RegExp(ref.sha256.fr));
  assert.equal(resultat.stdout.includes("poisson-cle-film"), false);
});

test("aucun sous-titre n'est trop court pour se lire", async () => {
  for (const lang of ["en", "fr"]) {
    const markdown = await readFile(join(root, "narration", lang, "g10.md"), "utf8");
    const chapitre = preparer(markdown, lang);
    const cues = await sousTitresNarration(chapitre);
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
    const cues = await sousTitresNarration(chapitre);
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
    const lignes = tableau(chapitre);
    const cues = await sousTitresNarration(chapitre);
    let origine = 0;
    for (const ligne of lignes) {
      const beat = chapitre.beats.find((item) => item.id === ligne.id);
      const duBeat = cues.filter((cue) => cue.beat === beat.id);
      const lu = contrat(duBeat.map((cue) => cue.text).join(" "));
      const voulu = contrat(beat.paragraphes.map((paragraphe) => paragraphe.brut).join(" "));
      assert.equal(lu, voulu, `${lang} ${beat.id}`);
      for (const cue of duBeat) {
        assert.ok(cue.debut >= origine - 1e-6 && cue.fin <= origine + ligne.slot + 1e-6, `${cue.text} hors voix`);
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
  const cuesAnglais = await sousTitresNarration(anglais);
  const cuesFrancais = await sousTitresNarration(francais);
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

test("le montage tient 252 s et marque les pistes eng et fra", async () => {
  const dir = await mkdtemp(join(tmpdir(), "film-"));
  const wav = join(dir, "note.wav");
  const pistes = join(dir, "pistes.m4a");
  await ecrireWav(wav, note(8000, 0.2), 8000);
  const mix = spawnSync(
    "ffmpeg",
    ["-y", "-i", wav, "-i", wav, "-map", "0:a", "-map", "1:a", "-c:a", "aac", "-b:a", "192k", pistes],
    { encoding: "utf8" },
  );
  assert.equal(mix.status, 0, mix.stderr);
  const clips = join(dir, "clips");
  await mkdir(clips);
  const noms = ["classes", "hard", "sym", "law", "sample", "bias", "close", "card"];
  for (const nom of noms) {
    const image = spawnSync(
      "ffmpeg",
      ["-y", "-f", "lavfi", "-i", "color=c=black:s=320x240:r=30:d=0.2", "-c:v", "libx264", "-pix_fmt", "yuv420p", join(clips, `${nom}.mp4`)],
      { encoding: "utf8" },
    );
    assert.equal(image.status, 0, image.stderr);
  }
  const anglais = preparer(await readFile(join(root, "narration/en/g10.md"), "utf8"), "en");
  const francais = preparer(await readFile(join(root, "narration/fr/g10.md"), "utf8"), "fr");
  const lignes = tableau(anglais);
  for (const [chapitre, piste, langue, fichier] of [
    [anglais, 0, "eng", join(dir, "pilote-en.mp4")],
    [francais, 1, "fra", join(dir, "pilote-fr.mp4")],
  ]) {
    const srt = join(dir, `${langue}.srt`);
    await writeFile(srt, texteSrt(await sousTitresNarration(chapitre)));
    const rendu = await monter({
      lignes,
      clips: noms.map((nom) => join(clips, `${nom}.mp4`)),
      pistes,
      sortie: fichier,
      piste,
      langue,
      sousTitres: srt,
    });
    assert.equal(rendu.duree, 252);
    assert.equal(rendu.images, 7560);
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
    const extrait = spawnSync("ffmpeg", ["-y", "-i", fichier, "-map", "0:s:0", "-f", "srt", "-"], { encoding: "utf8" });
    assert.equal(extrait.status, 0, extrait.stderr);
    const texte = extrait.stdout.replaceAll("\u00a0", " ").replace(/\s+/g, " ");
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
