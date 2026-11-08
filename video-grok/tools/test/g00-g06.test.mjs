import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { readFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "../..");
const verifier = join(root, "narration/en/g00-g06-verify.py");
const tokenizer = join(root, "narration/en/g07-g11-verify.py");

const NAMED_CUES = [
  "cue.g00.needle.start",
  "cue.g00.needle.show",
  "cue.g00.title.show",
  "cue.g01.rate.predict",
  "cue.g02.ratio.formula",
  "cue.g06.recap.show",
];

function beatsOf(markdown) {
  const beats = [];
  let beat = null;
  let cue = null;
  for (const line of markdown.split(/\r?\n/)) {
    if (line.startsWith("## ")) {
      beat = { id: line.slice(3).trim(), duration: 0, cues: [] };
      beats.push(beat);
      cue = null;
      continue;
    }
    if (line.startsWith("### ")) {
      cue = { id: line.slice(4).trim(), role: "", pause: 0, text: [] };
      beat.cues.push(cue);
      continue;
    }
    if (beat && line.startsWith("duration:")) {
      const [minutes, seconds] = line.slice("duration:".length).trim().split(":");
      beat.duration = Number(minutes) * 60 + Number(seconds);
      continue;
    }
    if (!cue) continue;
    if (line.startsWith("role:")) {
      cue.role = line.slice("role:".length).trim();
      continue;
    }
    if (line.startsWith("pause:")) {
      cue.pause = Number(line.slice("pause:".length).trim().replace(/s$/, ""));
      continue;
    }
    if (line.startsWith("screen:") || line.startsWith("badge:") || line.startsWith("class:")) continue;
    if (line.trim() === "") continue;
    cue.text.push(line.trim());
  }
  return beats;
}

function clockSeconds(token) {
  const [minutes, seconds] = token.split(":");
  return Number(minutes) * 60 + Number(seconds);
}

function planRows(plan) {
  const rows = [];
  for (const line of plan.split(/\r?\n/)) {
    const match = line.match(/^\| (g0[0-6]\.[a-z0-9]+) \| ([0-9]+:[0-9]+) \|/);
    if (match) rows.push({ id: match[1], duration: clockSeconds(match[2]) });
  }
  return rows;
}

function speech(text, duration, pause) {
  const script = `
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("chk", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
payload = json.loads(sys.stdin.read())
said = payload["text"]
count = len(mod.words(mod.expand_spoken(said)))
rate = mod.speech_rate(said, payload["duration"], payload["pause"])
print(json.dumps({"count": count, "rate": rate, "spelled": mod.expand_spoken(said)}))
`;
  const out = execFileSync("python3", ["-c", script, tokenizer], {
    input: JSON.stringify({ text, duration, pause }),
    encoding: "utf8",
  });
  return JSON.parse(out);
}

const plan = await readFile(join(root, "PLAN.md"), "utf8");
const rows = planRows(plan);
const chapters = {};
for (const id of ["g00", "g01", "g02", "g03", "g04", "g05", "g06"]) {
  chapters[id] = beatsOf(await readFile(join(root, "narration/en", `${id}.md`), "utf8"));
}
const fileBeats = Object.values(chapters).flat();

test("les durées du fichier suivent le plan, et les bandes coupées allongent g01.rate", () => {
  const stripes = rows.find((row) => row.id === "g01.stripes");
  const rate = rows.find((row) => row.id === "g01.rate");
  assert.equal(stripes.duration, 25);
  assert.equal(rate.duration, 40);
  assert.equal(fileBeats.some((beat) => beat.id === "g01.stripes"), false);
  assert.equal(fileBeats.some((beat) => beat.id === "g02.disk"), false);

  const expected = rows
    .filter((row) => row.id !== "g01.stripes")
    .map((row) => (row.id === "g01.rate" ? { id: row.id, duration: row.duration + stripes.duration } : row));
  assert.deepEqual(
    fileBeats.map((beat) => ({ id: beat.id, duration: beat.duration })),
    expected,
  );
});

test("les repères nommés du plan sont dans le script, dans l'ordre des scènes", () => {
  const present = fileBeats.flatMap((beat) => beat.cues.map((cue) => cue.id));
  for (const cueId of NAMED_CUES) assert.equal(present.includes(cueId), true, cueId);
  const ratio = chapters.g02.find((beat) => beat.id === "g02.ratio");
  assert.deepEqual(
    ratio.cues.map((cue) => cue.id),
    ["cue.g02.ratio.predict", "cue.g02.ratio.formula", "cue.g02.ratio.show"],
  );
  assert.equal(ratio.cues[1].role, "unread");
  const predict = ratio.cues[0];
  assert.equal(predict.role, "spoken");
  assert.equal(predict.pause, 2);
  const earth = chapters.g01.find((beat) => beat.id === "g01.rate");
  assert.equal(earth.cues[0].id, "cue.g01.rate.predict");
  assert.equal(earth.cues[0].pause, 3);
});

test("chaque beat g00-g06 reste à 156 mots par minute, avec le tokenizer g07", () => {
  const report = JSON.parse(execFileSync("python3", [verifier, "--json"], { encoding: "utf8" }));
  assert.equal(report.ceiling, 156);
  assert.equal(report.beats.length, fileBeats.length);
  for (const beat of fileBeats) {
    const spoken = beat.cues.filter((cue) => cue.role === "spoken");
    const text = spoken.map((cue) => cue.text.join(" ")).join("\n");
    const pause = spoken.reduce((sum, cue) => sum + cue.pause, 0);
    const result = speech(text, beat.duration, pause);
    assert.ok(result.rate <= 156, `${beat.id}: ${result.count} mots, ${result.rate} mots/min`);
    const fromVerifier = report.beats.find((row) => row.id === beat.id);
    assert.equal(fromVerifier.duration, beat.duration);
    assert.deepEqual(fromVerifier.cues, beat.cues.map((cue) => cue.id));
    assert.equal(fromVerifier.rate, Math.round(result.rate * 10) / 10);
  }
  const tooFast = speech(Array.from({ length: 100 }, () => "word").join(" "), 30, 0);
  assert.ok(tooFast.rate > 156, `${tooFast.rate} mots/min`);
  const spelled = speech("0.82 times 10 to the minus 5", 30, 0);
  assert.match(spelled.spelled, /zero point eight two/);
});

test("le vérificateur g00-g06 et le tokenizer g07 épèlent la même phrase", () => {
  const script = `
import importlib.util, json, sys
def load(path):
    spec = importlib.util.spec_from_file_location("mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
lot, new = load(sys.argv[1]), load(sys.argv[2])
sample = "share 0.3125, 560,612 euros, 0.82 times 10 to the minus 5, ANR-25-CE51-0077"
same = lot.expand_spoken(sample) == new.expand_spoken(sample) and lot.words(sample) == new.words(sample)
same = same and lot.speech_rate(sample, 40, 2) == new.speech_rate(sample, 40, 2)
print(json.dumps({"same": same}))
`;
  const out = JSON.parse(
    execFileSync("python3", ["-c", script, tokenizer, verifier], { encoding: "utf8" }),
  );
  assert.equal(out.same, true);
  const human = execFileSync("python3", [verifier], { encoding: "utf8" });
  assert.match(human, /débit ≤ 156/);
  assert.match(human, /g00-g06: chiffres, repères, cartes et horloges tenus/);
});
