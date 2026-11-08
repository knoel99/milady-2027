import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtemp, readdir, stat } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { capturer } from "../capture.mjs";
import { servir } from "../servir.mjs";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");

test("la capture courte n'écrit aucun PNG", async () => {
  const dir = await mkdtemp(join(tmpdir(), "fondations-"));
  const previous = process.env.TMPDIR;
  process.env.TMPDIR = dir;
  const server = await servir(root);
  const sortie = join(dir, "demo.mp4");
  try {
    const result = await capturer({
      url: `http://127.0.0.1:${server.port}/engine/demo/index.html`,
      repere: "show",
      secondes: 0.5,
      sortie,
      crf: 20,
    });
    assert.equal(result.frames, 15);
    const files = await walk(dir);
    assert.equal(files.some((file) => file.endsWith(".png")), false);
    assert.equal(files.includes(sortie), true);
    const probe = spawnSync(
      "ffprobe",
      ["-v", "error", "-show_entries", "stream=codec_name,width,height,pix_fmt,color_space", "-of", "json", sortie],
      { encoding: "utf8" },
    );
    assert.equal(probe.status, 0, probe.stderr);
    const stream = JSON.parse(probe.stdout).streams[0];
    assert.equal(stream.codec_name, "h264");
    assert.equal(stream.width, 1920);
    assert.equal(stream.height, 1080);
    assert.equal(stream.pix_fmt, "yuv420p");
    assert.equal(stream.color_space, "bt709");
  } finally {
    if (previous == null) delete process.env.TMPDIR;
    else process.env.TMPDIR = previous;
    await server.close();
  }
});

async function walk(dir) {
  const found = [];
  for (const name of await readdir(dir)) {
    const path = join(dir, name);
    const info = await stat(path);
    if (info.isDirectory()) found.push(...(await walk(path)));
    else found.push(path);
  }
  return found;
}
