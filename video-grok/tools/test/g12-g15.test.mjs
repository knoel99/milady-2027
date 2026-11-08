import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { readFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "../..");
const verifier = join(root, "narration/en/g12-g15-verify.py");
const chapters = ["g12", "g13", "g14", "g15"];

const cues = {
  "g12.learn": ["cue.g12.learn.show"],
  "g12.gen": ["cue.g12.gen.show"],
  "g12.lawlit": ["cue.g12.lawlit.show"],
  "g12.people": ["cue.g12.people.show"],
  "g12.gaps": ["cue.g12.gaps.show", "cue.g12.gaps.caveat"],
  "g12.place": ["cue.g12.place.show"],
  "g12.close": ["cue.g12.close.show"],
  "g12.card": ["cue.g12.card"],
  "g13.ladder": ["cue.g13.ladder.show"],
  "g13.bets": ["cue.g13.bets.show", "cue.g13.bets.blur", "cue.g13.bets.tg", "cue.g13.bets.anchor"],
  "g13.cost": ["cue.g13.cost.show", "cue.g13.cost.caveat"],
  "g13.close": ["cue.g13.close.show"],
  "g13.card": ["cue.g13.card"],
  "g14.a": ["cue.g14.a.show"],
  "g14.b": ["cue.g14.b.show"],
  "g14.c": ["cue.g14.c.show"],
  "g14.close": ["cue.g14.close.show"],
  "g14.card": ["cue.g14.card"],
  "g15.needle": ["cue.g15.needle.show"],
  "g15.close": ["cue.g15.close.show"],
  "g15.card": ["cue.g15.card"],
};

function beatsOf(markdown) {
  const beats = [];
  let beat = null;
  let cue = null;
  for (const line of markdown.split(/\r?\n/)) {
    if (line.startsWith("## ")) {
      beat = { id: line.slice(3).trim(), duration: 0, badge: "", cues: [] };
      beats.push(beat);
      cue = null;
      continue;
    }
    if (line.startsWith("### ")) {
      cue = { id: line.slice(4).trim(), role: "", text: [] };
      beat.cues.push(cue);
      continue;
    }
    if (beat && line.startsWith("duration:")) {
      const [minutes, seconds] = line.slice("duration:".length).trim().split(":");
      beat.duration = Number(minutes) * 60 + Number(seconds);
      continue;
    }
    if (beat && line.startsWith("badge:") && cue == null) {
      beat.badge = line.slice("badge:".length).trim();
      continue;
    }
    if (!cue) continue;
    if (line.startsWith("role:") || line.startsWith("screen:") || line.startsWith("class:") || line.startsWith("pause:")) {
      if (line.startsWith("role:")) cue.role = line.slice("role:".length).trim();
      continue;
    }
    if (line.trim() === "") continue;
    cue.text.push(line.trim());
  }
  return beats;
}

function planBeats(plan) {
  const start = plan.indexOf("## g12 ");
  const end = plan.indexOf("## Modules", start);
  const rows = [];
  for (const line of plan.slice(start, end).split(/\r?\n/)) {
    const match = line.match(/^\| ((g1[2-5])\.([a-z0-9]+)) \| ([0-9]+):([0-9]+) \| ([^|]+) \|/);
    if (!match) continue;
    rows.push({
      chapter: match[2],
      id: match[1],
      duration: Number(match[4]) * 60 + Number(match[5]),
      badge: match[6].trim(),
    });
  }
  return rows;
}

function rateOf(text, duration) {
  const script = `
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("chk", sys.argv[1])
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
payload = json.loads(sys.stdin.read())
said = payload["text"]
count = len(mod.words(mod.expand_spoken(said)))
rate = mod.speech_rate(said, payload["duration"], 0)
print(json.dumps({"count": count, "rate": rate}))
`;
  const out = execFileSync("python3", ["-c", script, verifier], {
    input: JSON.stringify({ text, duration }),
    encoding: "utf8",
  });
  return JSON.parse(out);
}

test("les repères et les durées de g12 à g15 suivent le plan", async () => {
  const plan = await readFile(join(root, "PLAN.md"), "utf8");
  const expected = planBeats(plan);
  assert.equal(expected.length, Object.keys(cues).length);
  const found = [];
  for (const chapter of chapters) {
    const markdown = await readFile(join(root, "narration/en", `${chapter}.md`), "utf8");
    found.push(...beatsOf(markdown));
  }
  assert.deepEqual(
    found.map((beat) => beat.id),
    expected.map((beat) => beat.id),
  );
  for (let index = 0; index < expected.length; index += 1) {
    const beat = found[index];
    assert.ok(beat.duration >= expected[index].duration, `${beat.id} plus court que le plan`);
    assert.equal(beat.badge, expected[index].badge, beat.id);
    assert.deepEqual(
      beat.cues.map((cue) => cue.id),
      cues[beat.id],
      beat.id,
    );
    for (const cue of beat.cues) {
      assert.equal(cue.role, "spoken", cue.id);
      assert.equal(cue.id.startsWith(`cue.${beat.id}`), true, cue.id);
    }
  }
});

test("chaque beat g12 à g15 reste à 156 mots par minute", async () => {
  for (const chapter of chapters) {
    const markdown = await readFile(join(root, "narration/en", `${chapter}.md`), "utf8");
    for (const beat of beatsOf(markdown)) {
      const text = beat.cues
        .filter((cue) => cue.role === "spoken")
        .map((cue) => cue.text.join(" "))
        .join("\n");
      const result = rateOf(text, beat.duration);
      assert.ok(result.rate <= 156, `${beat.id}: ${result.count} mots, ${result.rate} mots/min`);
    }
  }
  const tooFast = rateOf(Array.from({ length: 100 }, () => "word").join(" "), 30);
  assert.ok(tooFast.rate > 156, `${tooFast.rate} mots/min`);
});

test("le vérificateur g12-g15 tient le débit et les repères", () => {
  const report = execFileSync("python3", [verifier], { encoding: "utf8" });
  assert.match(report, /g12: \d+ mots parlés, cible 500-\d+/);
  assert.match(report, /g13: \d+ mots parlés, cible 271-\d+/);
  assert.match(report, /g14: \d+ mots parlés, cible 292-\d+/);
  assert.match(report, /g15: \d+ mots parlés, cible 115-119/);
  assert.match(report, /débit g12\.gaps:/);
  assert.match(report, /débit g13\.bets:/);
  assert.match(report, /plafond 156/);
  assert.match(report, /g12-g15: chiffres, repères, cartes et horloges tenus/);
});
