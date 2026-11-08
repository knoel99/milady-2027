import { readFile, rename, writeFile } from "node:fs/promises";

const DEBUT = "<!-- fish-stats -->";
const FIN = "<!-- /fish-stats -->";

export function noter(markdown, { requetes, succesCache, minutes }) {
  const precedent = lire(markdown);
  const suivant = {
    requetes: precedent.requetes + requetes,
    succesCache: precedent.succesCache + succesCache,
    minutes: combiner(precedent.minutes, minutes, requetes),
  };
  const bloc = [
    DEBUT,
    "",
    "## Synthèse Fish",
    "",
    "| Champ | Valeur |",
    "|---|---|",
    `| Requêtes envoyées | ${suivant.requetes} |`,
    `| Succès de cache | ${suivant.succesCache} |`,
    `| Minutes facturées | ${afficher(suivant.minutes)} |`,
    "",
    FIN,
    "",
  ].join("\n");
  if (!markdown.includes(DEBUT)) return `${markdown.trimEnd()}\n\n${bloc}`;
  return markdown.replace(new RegExp(`${DEBUT}[\\s\\S]*?${FIN}\\n?`), bloc);
}

export async function ecrireJournal(path, delta) {
  let actuel = "";
  try {
    actuel = await readFile(path, "utf8");
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
  const temporaire = `${path}.${process.pid}.tmp`;
  await writeFile(temporaire, noter(actuel, delta));
  await rename(temporaire, path);
}

function lire(markdown) {
  if (!markdown.includes(DEBUT)) return { requetes: 0, succesCache: 0, minutes: undefined };
  const requetes = Number(cellule(markdown, "Requêtes envoyées"));
  const succesCache = Number(cellule(markdown, "Succès de cache"));
  const brut = cellule(markdown, "Minutes facturées");
  if (!Number.isFinite(requetes) || !Number.isFinite(succesCache) || brut == null) {
    throw Object.assign(new Error("journal"), { code: "journal" });
  }
  return { requetes, succesCache, minutes: brut === "unavailable" ? null : Number(brut) };
}

function combiner(precedent, courant, requetes) {
  if (requetes === 0) return precedent;
  if (courant == null) return null;
  if (precedent === undefined) return courant;
  if (precedent == null) return null;
  return precedent + courant;
}

function afficher(minutes) {
  return typeof minutes === "number" ? String(minutes) : "unavailable";
}

function cellule(markdown, champ) {
  const trouve = markdown.match(new RegExp(`\\| ${champ} \\| ([^|]+) \\|`));
  return trouve ? trouve[1].trim() : null;
}
