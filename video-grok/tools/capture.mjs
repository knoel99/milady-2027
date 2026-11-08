import { spawn } from "node:child_process";
import { mkdir, rename } from "node:fs/promises";
import { dirname, join } from "node:path";
import { ouvrir } from "./navigateur.mjs";

export async function capturer({
  url,
  repere,
  secondes = 0.5,
  sortie,
  fps = 30,
  largeur = 1920,
  hauteur = 1080,
  crf = 20,
}) {
  if (!Number.isFinite(secondes) || secondes <= 0) throw new Error("durée");
  if (crf < 18 || crf > 23) throw new Error("crf");
  const frames = Math.round(secondes * fps);
  const browserBox = await ouvrir(url, { largeur, hauteur });
  const temporary = join(dirname(sortie), `.${process.pid}.part.mp4`);
  await mkdir(dirname(sortie), { recursive: true });
  const ffmpeg = spawn("ffmpeg", argumentsFfmpeg({ fps, crf, sortie: temporary }), {
    stdio: ["pipe", "ignore", "pipe"],
  });
  let erreur = "";
  ffmpeg.stderr.on("data", (chunk) => {
    erreur += chunk.toString();
  });
  try {
    const debut = await browserBox.page.evaluate((id) => window.__scene.cue(id), repere);
    for (let index = 0; index < frames; index += 1) {
      const t = debut + index / fps;
      await browserBox.page.evaluate((time) => window.seek(time), t);
      const png = await browserBox.page.screenshot({ type: "png", animations: "disabled" });
      await ecrire(ffmpeg.stdin, png);
    }
    ffmpeg.stdin.end();
    const code = await attendre(ffmpeg);
    if (code !== 0) throw new Error(erreur.slice(-2000));
    await rename(temporary, sortie);
  } finally {
    await browserBox.browser.close();
  }
  return { frames, sortie, largeur, hauteur };
}

export function argumentsFfmpeg({ fps, crf, sortie }) {
  return [
    "-y",
    "-f",
    "image2pipe",
    "-framerate",
    String(fps),
    "-i",
    "pipe:0",
    "-c:v",
    "libx264",
    "-pix_fmt",
    "yuv420p",
    "-crf",
    String(crf),
    "-g",
    String(fps * 2),
    "-color_primaries",
    "bt709",
    "-color_trc",
    "bt709",
    "-colorspace",
    "bt709",
    "-movflags",
    "+faststart",
    sortie,
  ];
}

function ecrire(stdin, buffer) {
  if (stdin.write(buffer)) return Promise.resolve();
  return new Promise((resolve) => stdin.once("drain", resolve));
}

function attendre(child) {
  return new Promise((resolve, reject) => {
    child.on("error", reject);
    child.on("close", resolve);
  });
}

if (process.argv[1] && process.argv[1].endsWith("capture.mjs")) {
  const options = lireArguments(process.argv.slice(2));
  capturer(options).then((result) => {
    process.stdout.write(`${JSON.stringify(result)}\n`);
  });
}

function lireArguments(argv) {
  const values = {};
  for (let index = 0; index < argv.length; index += 2) {
    values[argv[index].replace(/^--/, "")] = argv[index + 1];
  }
  return {
    url: values.url,
    repere: values.repere,
    secondes: Number(values.secondes ?? 0.5),
    sortie: values.sortie,
    crf: Number(values.crf ?? 20),
  };
}
