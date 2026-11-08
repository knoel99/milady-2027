import { spawn } from "node:child_process";

export function argumentsMixage({ voix, musique, effets, sortie }) {
  return [
    "-y",
    "-i",
    voix,
    "-i",
    musique,
    "-i",
    effets,
    "-filter_complex",
    "[1:a][2:a]amix=inputs=2:duration=longest:normalize=0,asplit=2[lit][bed];[0:a][lit]amix=inputs=2:duration=longest:normalize=0[mix]",
    "-map",
    "[mix]",
    "-map",
    "[bed]",
    "-c:a",
    "aac",
    "-b:a",
    "192k",
    sortie,
  ];
}

export function mixer(options) {
  const child = spawn("ffmpeg", argumentsMixage(options), { stdio: ["ignore", "ignore", "pipe"] });
  let erreur = "";
  child.stderr.on("data", (chunk) => {
    erreur += chunk.toString();
  });
  return new Promise((resolve, reject) => {
    child.on("error", reject);
    child.on("close", (code) => {
      if (code === 0) resolve(options.sortie);
      else reject(new Error(erreur.slice(-2000)));
    });
  });
}
