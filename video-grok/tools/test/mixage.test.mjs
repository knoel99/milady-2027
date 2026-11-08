import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtemp } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";
import { mixer } from "../mixage.mjs";

test("le mixage écrit une piste avec la voix et une piste sans", async () => {
  const dir = await mkdtemp(join(tmpdir(), "mix-"));
  const voix = join(dir, "voix.wav");
  const musique = join(dir, "musique.wav");
  const effets = join(dir, "effets.wav");
  const sortie = join(dir, "mix.m4a");
  tone(voix, 440);
  tone(musique, 220);
  tone(effets, 880);
  await mixer({ voix, musique, effets, sortie });
  const probe = spawnSync(
    "ffprobe",
    ["-v", "error", "-show_entries", "stream=codec_type,codec_name", "-of", "json", sortie],
    { encoding: "utf8" },
  );
  assert.equal(probe.status, 0, probe.stderr);
  const streams = JSON.parse(probe.stdout).streams;
  assert.equal(streams.length, 2);
  assert.deepEqual(
    streams.map((stream) => stream.codec_type),
    ["audio", "audio"],
  );
});

function tone(path, frequency) {
  const result = spawnSync(
    "ffmpeg",
    ["-y", "-f", "lavfi", "-i", `sine=frequency=${frequency}:duration=0.4`, path],
    { encoding: "utf8" },
  );
  if (result.status !== 0) throw new Error(result.stderr);
}
