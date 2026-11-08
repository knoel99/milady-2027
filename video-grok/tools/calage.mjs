import { spawnSync } from "node:child_process";
import { mkdtemp, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { lireWav } from "./kit-voix/aligner.mjs";

const VOIX = { en: "en-us", fr: "fr-fr" };
const memoire = new Map();
const SAUT = 0.01;
const FENETRE = 0.025;
const BANDES = [200, 400, 700, 1100, 1600, 2300, 3200, 4500];

export function motsTexte(texte) {
  return texte.replaceAll("\n", " ").trim().split(/\s+/).filter(Boolean);
}

export async function syntheseMot(mot, lang) {
  const cle = `${lang}\0${mot}`;
  const garde = memoire.get(cle);
  if (garde) return garde;
  const voix = VOIX[lang] ?? "en-us";
  const resultat = spawnSync("espeak-ng", ["-v", voix, "-s", "150", "--stdout", mot], {
    maxBuffer: 8_000_000,
  });
  if (resultat.status !== 0) {
    throw new Error(resultat.stderr?.toString() || "espeak-ng");
  }
  const lu = lireTampon(resultat.stdout);
  memoire.set(cle, lu);
  return lu;
}

export async function decoder(fichier) {
  const dir = await mkdtemp(join(tmpdir(), "calage-"));
  const wav = join(dir, "clip.wav");
  try {
    const resultat = spawnSync(
      "ffmpeg",
      ["-y", "-i", fichier, "-ac", "1", "-ar", "22050", "-c:a", "pcm_s16le", wav],
      { encoding: "utf8" },
    );
    if (resultat.status !== 0) throw new Error(resultat.stderr?.slice(-500) || "ffmpeg");
    return await lireWav(wav);
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
}

export function trames(samples, rate) {
  const taille = Math.max(1, Math.round(rate * FENETRE));
  const saut = Math.max(1, Math.round(rate * SAUT));
  const sortie = [];
  for (let depart = 0; depart + taille <= samples.length; depart += saut) {
    const fenetre = samples.subarray(depart, depart + taille);
    sortie.push(BANDES.map((freq) => goertzel(fenetre, rate, freq)));
  }
  return sortie;
}

export async function calerMots(fichier, texte, lang) {
  const clip = await decoder(fichier);
  return alignerMots(clip, motsTexte(texte), lang, 0, clip.samples.length / clip.sampleRate);
}

async function alignerMots(clip, mots, lang, debut, fin, couvrir = false) {
  const rate = clip.sampleRate;
  const gauche = Math.max(0, Math.floor(debut * rate));
  const droite = Math.min(clip.samples.length, Math.ceil(fin * rate));
  const extrait = clip.samples.subarray(gauche, droite);
  const trameClip = trames(extrait, rate);
  const energie = energieTrames(extrait, rate);
  const gabarits = [];
  for (const mot of mots) {
    const reference = await syntheseMot(mot, lang);
    const parole = rogner(reference.samples, reference.sampleRate);
    let trameMot = trames(parole.length > 0 ? parole : reference.samples, reference.sampleRate);
    if (trameMot.length === 0) trameMot = [new Array(trameClip[0]?.length ?? 8).fill(0)];
    gabarits.push(trameMot);
  }
  if (trameClip.length === 0 || gabarits.length === 0) {
    return mots.map((mot) => ({ mot, debut, fin: debut }));
  }
  const places = alignerSuite(trameClip, gabarits, energie, couvrir);
  const origine = gauche / rate;
  return mots.map((mot, index) => ({
    mot,
    debut: origine + places[index].debut * SAUT,
    fin: origine + places[index].fin * SAUT,
  }));
}

export async function calerPhrases(fichier, brut, lang, decouper) {
  const clip = await decoder(fichier);
  const phrases = decouper(brut);
  const plan = [];
  for (const phrase of phrases) {
    const mots = motsTexte(phrase);
    let corps = 0;
    for (const mot of mots) {
      const reference = await syntheseMot(mot, lang);
      corps += reference.samples.length / reference.sampleRate + 0.06;
      if (/\d/.test(mot)) corps += 0.55;
      if (/[.!?]$/.test(mot)) corps += 0.24;
    }
    plan.push({ phrase, mots, corps });
  }
  const total = plan.reduce((somme, item) => somme + item.corps, 0) || 1;
  const duree = clip.samples.length / clip.sampleRate;
  const echelle = duree / total;
  const cues = [];
  let origine = 0;
  for (const item of plan) {
    if (item.mots.length === 0) continue;
    const corps = item.corps * echelle;
    const debut = Math.max(0, origine - 0.3);
    const horizon = Math.min(duree, origine + corps + 0.4);
    const bornes = await alignerMots(clip, item.mots, lang, debut, horizon, true);
    if (bornes.length === 0) continue;
    cues.push({
      phrase: item.phrase,
      debut: bornes[0].debut,
      fin: bornes[bornes.length - 1].fin,
    });
    origine += corps;
  }
  return cues;
}

function rogner(samples, rate) {
  const hop = Math.max(1, Math.round(rate * 0.01));
  const actif = (index) => {
    if (index < 0 || index >= samples.length) return false;
    let energie = 0;
    const nombre = Math.min(hop, samples.length - index);
    for (let offset = 0; offset < nombre; offset += 1) energie += samples[index + offset] ** 2;
    return Math.sqrt(energie / nombre) > 0.04;
  };
  let debut = 0;
  let fin = samples.length;
  while (debut < samples.length && !actif(debut)) debut += hop;
  while (fin > debut + hop && !actif(fin - hop)) fin -= hop;
  return samples.subarray(debut, Math.max(debut + hop, fin));
}

function energieTrames(samples, rate) {
  const taille = Math.max(1, Math.round(rate * FENETRE));
  const saut = Math.max(1, Math.round(rate * SAUT));
  const sortie = [];
  for (let depart = 0; depart + taille <= samples.length; depart += saut) {
    let energie = 0;
    const fenetre = samples.subarray(depart, depart + taille);
    for (let index = 0; index < fenetre.length; index += 1) energie += fenetre[index] ** 2;
    sortie.push(Math.sqrt(energie / fenetre.length));
  }
  return sortie;
}

function alignerSuite(clip, gabarits, energie, couvrir) {
  const owner = [];
  const frames = [];
  for (let mot = 0; mot < gabarits.length; mot += 1) {
    for (const trame of gabarits[mot]) {
      frames.push(trame);
      owner.push(mot);
    }
  }
  const n = frames.length;
  const m = clip.length;
  const pred = new Uint8Array(n * m);
  const inf = 1e15;
  let precedent = new Float64Array(m).fill(inf);
  let courant = new Float64Array(m);
  const sautSilence = new Float64Array(m);
  let somme = 0;
  for (let j = 0; j < m; j += 1) {
    sautSilence[j] = somme;
    somme += energie[j] < 0.02 ? 0.0001 : 0.85;
  }
  for (let i = 0; i < n; i += 1) {
    courant.fill(inf);
    for (let j = 0; j < m; j += 1) {
      const cout = distance(frames[i], clip[j]);
      let meilleur = inf;
      let choix = 0;
      if (i === 0) {
        const depart = cout + (j > 0 ? sautSilence[j] : 0);
        if (depart < meilleur) {
          meilleur = depart;
          choix = 0;
        }
      }
      if (i > 0 && j > 0 && precedent[j - 1] + cout < meilleur) {
        meilleur = precedent[j - 1] + cout;
        choix = 0;
      }
      if (i > 0 && precedent[j] + cout + 0.15 < meilleur) {
        meilleur = precedent[j] + cout + 0.15;
        choix = 1;
      }
      if (j > 0 && courant[j - 1] + (energie[j] < 0.02 ? 0.0001 : 0.85) < meilleur) {
        meilleur = courant[j - 1] + (energie[j] < 0.02 ? 0.0001 : 0.85);
        choix = 2;
      }
      courant[j] = meilleur;
      pred[i * m + j] = choix;
    }
    const ancien = precedent;
    precedent = courant;
    courant = ancien;
  }
  const abandon = new Float64Array(m);
  if (couvrir) {
    let reste = 0;
    for (let j = m - 1; j >= 0; j -= 1) {
      abandon[j] = reste;
      reste += energie[j] < 0.02 ? 0.0001 : 0.85;
    }
  }
  let fin = 0;
  for (let j = 1; j < m; j += 1) {
    if (precedent[j] + abandon[j] < precedent[fin] + abandon[fin]) fin = j;
  }
  const positions = gabarits.map(() => []);
  let i = n - 1;
  let j = fin;
  while (i >= 0 && j >= 0) {
    const mot = owner[i];
    const choix = pred[i * m + j];
    if (choix !== 2) positions[mot].push(j);
    if (choix === 1) i -= 1;
    else if (choix === 2) j -= 1;
    else {
      i -= 1;
      j -= 1;
    }
  }
  return positions.map((liste) => ilot(liste));
}

function ilot(liste) {
  if (liste.length === 0) return { debut: 0, fin: 1 };
  const tri = liste.sort((a, b) => a - b);
  let meilleur = { debut: tri[0], fin: tri[0] + 1, n: 0, duree: 0 };
  let debut = tri[0];
  let nombre = 0;
  let precedent = tri[0] - 1;
  const fermer = (fin) => {
    const duree = fin - debut;
    if (nombre > meilleur.n || (nombre === meilleur.n && duree > meilleur.duree)) {
      meilleur = { debut, fin: fin + 1, n: nombre, duree };
    }
  };
  for (const point of tri) {
    if (point - precedent > 20) {
      fermer(precedent);
      debut = point;
      nombre = 0;
    }
    nombre += 1;
    precedent = point;
  }
  fermer(precedent);
  return { debut: meilleur.debut, fin: Math.max(meilleur.fin, meilleur.debut + 1) };
}

function distance(gauche, droite) {
  let produit = 0;
  let normeG = 0;
  let normeD = 0;
  for (let index = 0; index < gauche.length; index += 1) {
    produit += gauche[index] * droite[index];
    normeG += gauche[index] * gauche[index];
    normeD += droite[index] * droite[index];
  }
  const denom = Math.sqrt(normeG * normeD) || 1;
  return 1 - produit / denom;
}

function goertzel(fenetre, rate, freq) {
  const k = Math.round((freq * fenetre.length) / rate);
  const omega = (2 * Math.PI * k) / fenetre.length;
  const coeff = 2 * Math.cos(omega);
  let s0 = 0;
  let s1 = 0;
  let s2 = 0;
  for (let index = 0; index < fenetre.length; index += 1) {
    s0 = fenetre[index] + coeff * s1 - s2;
    s2 = s1;
    s1 = s0;
  }
  return Math.log(1 + s1 * s1 + s2 * s2 - coeff * s1 * s2);
}

function lireTampon(buffer) {
  if (buffer.toString("ascii", 0, 4) !== "RIFF") throw new Error("wav");
  let offset = 12;
  let sampleRate = 0;
  let data = null;
  while (offset + 8 <= buffer.length) {
    const id = buffer.toString("ascii", offset, offset + 4);
    const size = buffer.readUInt32LE(offset + 4);
    const body = offset + 8;
    if (id === "fmt ") sampleRate = buffer.readUInt32LE(body + 4);
    if (id === "data") data = buffer.subarray(body, body + size);
    offset = body + size + (size % 2);
  }
  const samples = new Float64Array(data.length / 2);
  for (let index = 0; index < samples.length; index += 1) {
    samples[index] = data.readInt16LE(index * 2) / 32768;
  }
  return { samples, sampleRate };
}
