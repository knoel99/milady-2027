import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { cleCache, ecrire, lire } from "../cache.mjs";
import { noter } from "../journal.mjs";
import { VOIX, preparer } from "../parole.mjs";
import { exigerCle, minutesReponse, synthetiser } from "../tts.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "../..");
const tts = join(here, "../tts.mjs");
const cle = "poisson-cle-9f3a";

function reponse(octets, { status = 200, minutes } = {}) {
  const headers = { "content-type": "audio/mpeg" };
  if (minutes != null) headers["x-billed-minutes"] = String(minutes);
  return new Response(octets, { status, headers });
}

test("la clé absente échoue avant toute requête, et le cache est consulté avant", async () => {
  const dir = await mkdtemp(join(tmpdir(), "tts-"));
  const markdown = await readFile(join(root, "narration/en/g10.md"), "utf8");
  const chapitre = preparer(markdown, "en");
  let appels = 0;
  const fetchImpl = async (url, init) => {
    const body = JSON.parse(init.body);
    assert.equal(url, "https://api.fish.audio/v1/tts");
    assert.equal(init.headers.model, "drama-3");
    assert.equal(init.headers.Authorization, `Bearer ${cle}`);
    assert.equal(JSON.stringify(init).includes(cle), true);
    const key = cleCache({ text: body.text, referenceId: body.reference_id });
    if (await lire(dir, key)) throw new Error("requete apres cache");
    appels += 1;
    return reponse(Buffer.from(`audio-${appels}`), { minutes: 0.25 });
  };
  await assert.rejects(synthetiser({ chapitre, cacheDir: dir, cle: "", fetchImpl }), { code: "FISH_API_KEY" });
  assert.equal(appels, 0);
  const premier = chapitre.paragraphes[0];
  await ecrire(dir, cleCache({ text: premier.texte, referenceId: VOIX }), Buffer.from("deja"));
  const resultat = await synthetiser({ chapitre, cacheDir: dir, cle, fetchImpl });
  assert.equal(appels, 10);
  assert.equal(resultat.succesCache, 1);
  assert.equal(resultat.requetes, 10);
  assert.equal(resultat.minutes, 2.5);
  const encore = await synthetiser({ chapitre, cacheDir: dir, cle, fetchImpl });
  assert.equal(appels, 10);
  assert.equal(encore.requetes, 0);
  assert.equal(encore.succesCache, 11);
  assert.equal(encore.minutes, null);
});

test("le même triplet n'est payé qu'une fois, et l'échec ne révèle pas la clé", async () => {
  const dir = await mkdtemp(join(tmpdir(), "tts-"));
  const chapitre = {
    lang: "en",
    paragraphes: [
      { id: "a", texte: "Hello." },
      { id: "b", texte: "Hello." },
    ],
  };
  let appels = 0;
  const fetchImpl = async () => {
    appels += 1;
    return reponse(Buffer.from("une-fois"));
  };
  const resultat = await synthetiser({ chapitre, cacheDir: dir, cle, fetchImpl });
  assert.equal(appels, 1);
  assert.equal(resultat.requetes, 1);
  assert.equal(resultat.succesCache, 1);
  assert.equal(resultat.minutes, null);
  const echec = {
    lang: "en",
    paragraphes: [{ id: "c", texte: "Autre." }],
  };
  await assert.rejects(
    synthetiser({
      chapitre: echec,
      cacheDir: dir,
      cle,
      fetchImpl: async () => reponse(Buffer.from("non"), { status: 402 }),
    }),
    (error) => {
      assert.equal(error.code, "fish");
      assert.equal(error.message, "Fish 402");
      assert.equal(error.message.includes(cle), false);
      assert.equal(error.requetes, 1);
      return true;
    },
  );
});

test("le journal additionne les envois et laisse les minutes unavailable", () => {
  const premier = noter("", { requetes: 2, succesCache: 1, minutes: null });
  assert.match(premier, /Requêtes envoyées \| 2/);
  assert.match(premier, /Succès de cache \| 1/);
  assert.match(premier, /Minutes facturées \| unavailable/);
  const deuxieme = noter(premier, { requetes: 0, succesCache: 3, minutes: null });
  assert.match(deuxieme, /Requêtes envoyées \| 2/);
  assert.match(deuxieme, /Succès de cache \| 4/);
  assert.match(deuxieme, /Minutes facturées \| unavailable/);
  const connu = noter("", { requetes: 1, succesCache: 0, minutes: 1.5 });
  const suite = noter(connu, { requetes: 1, succesCache: 0, minutes: 0.5 });
  assert.match(suite, /Minutes facturées \| 2/);
  const trou = noter(suite, { requetes: 1, succesCache: 0, minutes: null });
  assert.match(trou, /Minutes facturées \| unavailable/);
});

test("l'estimation et l'essai à blanc ne touchent pas le réseau", async () => {
  const dir = await mkdtemp(join(tmpdir(), "tts-sec-"));
  const anglais = lancer(["--chapter", "g10", "--lang", "en", "--estimate"]);
  const francais = lancer(["--chapter", "g10", "--lang", "fr", "--estimate"]);
  const sec = lancer(["--chapter", "g10", "--lang", "en", "--dry-run", "--cache", dir], { FISH_API_KEY: cle });
  assert.equal(anglais.status, 0, anglais.stderr);
  assert.equal(francais.status, 0, francais.stderr);
  assert.equal(sec.status, 0, sec.stderr);
  assert.match(anglais.stdout, /requêtes: 11/);
  assert.match(anglais.stdout, /caractères: \d+/);
  assert.match(anglais.stdout, /non sourcées: aucune/);
  assert.match(francais.stdout, /requêtes: 11/);
  assert.match(francais.stdout, /langue: fr/);
  assert.match(sec.stdout, /requêtes: 0/);
  assert.match(sec.stdout, /prévues: 11/);
  assert.equal(anglais.stdout.includes(cle), false);
  assert.equal(sec.stdout.includes(cle), false);
  assert.equal(sec.stderr.includes(cle), false);
  const sansCle = lancer(["--chapter", "g10", "--lang", "en"], { FISH_API_KEY: undefined });
  assert.equal(sansCle.status, 1);
  assert.match(sansCle.stderr, /FISH_API_KEY manquante/);
  assert.equal(sansCle.stdout.includes("Bearer"), false);
});

test("la commande envoie le corps drama-3 sans écrire la clé", async () => {
  const dir = await mkdtemp(join(tmpdir(), "tts-cli-"));
  const trace = join(dir, "trace.jsonl");
  const stats = join(dir, "STATS.md");
  const env = { FISH_API_KEY: cle, FISH_TRACE: trace, FISH_MINUTES: "0.5" };
  const premier = lancer(["--chapter", "g10", "--lang", "en", "--cache", dir, "--stats", stats], env, true);
  assert.equal(premier.status, 0, premier.stderr);
  assert.match(premier.stdout, /requêtes: 11/);
  assert.match(premier.stdout, /minutes: 5.5/);
  assert.equal(premier.stdout.includes(cle), false);
  assert.equal(premier.stderr.includes(cle), false);
  const lignes = (await readFile(trace, "utf8")).trim().split("\n").map((ligne) => JSON.parse(ligne));
  assert.equal(lignes.length, 11);
  assert.equal(lignes.every((ligne) => ligne.authorizationOk && ligne.model === "drama-3"), true);
  assert.equal(lignes.every((ligne) => ligne.body.prosody.speed === 1 && !("references" in ligne.body)), true);
  assert.equal((await readFile(trace, "utf8")).includes(cle), false);
  assert.equal((await readFile(stats, "utf8")).includes(cle), false);
  assert.match(await readFile(stats, "utf8"), /Requêtes envoyées \| 11/);
  assert.match(await readFile(stats, "utf8"), /Minutes facturées \| 5.5/);
  const deuxieme = lancer(["--chapter", "g10", "--lang", "en", "--cache", dir, "--stats", stats], env, true);
  assert.equal(deuxieme.status, 0, deuxieme.stderr);
  assert.match(deuxieme.stdout, /requêtes: 0/);
  assert.match(deuxieme.stdout, /cache: 11/);
  const apres = (await readFile(trace, "utf8")).trim().split("\n");
  assert.equal(apres.length, 11);
  const journal = await readFile(stats, "utf8");
  assert.match(journal, /Requêtes envoyées \| 11/);
  assert.match(journal, /Succès de cache \| 11/);
  assert.match(journal, /Minutes facturées \| 5.5/);
});

test("exigerCle refuse une valeur vide", () => {
  assert.throws(() => exigerCle({}), { code: "FISH_API_KEY" });
  assert.throws(() => exigerCle({ FISH_API_KEY: "  " }), { code: "FISH_API_KEY" });
  assert.equal(exigerCle({ FISH_API_KEY: cle }), cle);
  assert.equal(minutesReponse(new Headers()), null);
  assert.equal(minutesReponse(new Headers({ "x-billed-minutes": "1.25" })), 1.25);
});

function lancer(args, env = {}, fictif = false) {
  const importe = fictif ? join(here, "../doubles/fish-fictif.mjs") : join(here, "bloquer-reseau.mjs");
  const propre = { ...process.env, ...env };
  if (env.FISH_API_KEY === undefined) delete propre.FISH_API_KEY;
  return spawnSync(process.execPath, ["--import", importe, tts, ...args], {
    encoding: "utf8",
    env: propre,
  });
}
