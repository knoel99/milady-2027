import { readFile, writeFile } from "node:fs/promises";
import { appliquer, lire, planifier } from "../cache.mjs";

export async function changer({ manifest, referenceId, cacheDir }) {
  const probe = planifier(manifest, referenceId, new Set());
  const presents = new Set();
  for (const paragraph of probe.paragraphs) {
    if (await lire(cacheDir, paragraph.after)) presents.add(paragraph.after);
  }
  return planifier(manifest, referenceId, presents);
}

if (process.argv[1] && process.argv[1].endsWith("changer.mjs")) {
  const values = {};
  const argv = process.argv.slice(2);
  for (let index = 0; index < argv.length; index += 2) {
    values[argv[index].replace(/^--/, "")] = argv[index + 1];
  }
  const manifest = JSON.parse(await readFile(values.manifest, "utf8"));
  const plan = await changer({
    manifest,
    referenceId: values.vers,
    cacheDir: values.cache,
  });
  process.stdout.write(`${JSON.stringify(plan)}\n`);
  if (values.ecrire) {
    await writeFile(values.ecrire, `${JSON.stringify(appliquer(manifest, plan), null, 2)}\n`);
  }
}
