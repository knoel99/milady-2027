import { readFile, writeFile } from "node:fs/promises";

export function segments(samples, sampleRate, { seuil = 0.02, silenceMin = 0.15 } = {}) {
  const hop = Math.max(1, Math.round(sampleRate * 0.01));
  const marks = [];
  for (let index = 0; index < samples.length; index += hop) {
    const count = Math.min(hop, samples.length - index);
    let energy = 0;
    for (let offset = 0; offset < count; offset += 1) {
      const value = samples[index + offset];
      energy += value * value;
    }
    marks.push(Math.sqrt(energy / count) >= seuil);
  }
  const found = [];
  let start = null;
  for (let index = 0; index <= marks.length; index += 1) {
    const voiced = marks[index] === true;
    if (voiced && start == null) start = index;
    if (!voiced && start != null) {
      if (index - start >= 2) {
        found.push({
          start: (start * hop) / sampleRate,
          duration: ((index - start) * hop) / sampleRate,
        });
      }
      start = null;
    }
  }
  return fusionner(found, silenceMin);
}

export function aligner(phrases, prises, { etirement = 0.12 } = {}) {
  if (phrases.length !== prises.length) {
    throw Object.assign(new Error("phrases"), { code: "phrases" });
  }
  return phrases.map((phrase, index) => {
    const prise = prises[index];
    const ratio = prise.duration / phrase.duration;
    if (Math.abs(ratio - 1) <= etirement + 1e-9) {
      return {
        id: phrase.id,
        cue: phrase.cue,
        action: "atempo",
        atempo: Number(ratio.toFixed(4)),
      };
    }
    return { id: phrase.id, cue: phrase.cue, action: "reminutage", at: prise.start };
  });
}

export async function lireWav(path) {
  const buffer = await readFile(path);
  if (buffer.toString("ascii", 0, 4) !== "RIFF" || buffer.toString("ascii", 8, 12) !== "WAVE") {
    throw Object.assign(new Error("wav"), { code: "wav" });
  }
  let offset = 12;
  let sampleRate = 0;
  let data = null;
  while (offset + 8 <= buffer.length) {
    const id = buffer.toString("ascii", offset, offset + 4);
    const size = buffer.readUInt32LE(offset + 4);
    const body = offset + 8;
    if (id === "fmt ") {
      const channels = buffer.readUInt16LE(body + 2);
      const bits = buffer.readUInt16LE(body + 14);
      if (channels !== 1 || bits !== 16) throw Object.assign(new Error("wav"), { code: "wav" });
      sampleRate = buffer.readUInt32LE(body + 4);
    }
    if (id === "data") data = buffer.subarray(body, body + size);
    offset = body + size + (size % 2);
  }
  if (!data || !sampleRate) throw Object.assign(new Error("wav"), { code: "wav" });
  const samples = new Float64Array(data.length / 2);
  for (let index = 0; index < samples.length; index += 1) {
    samples[index] = data.readInt16LE(index * 2) / 32768;
  }
  return { samples, sampleRate };
}

export async function ecrireWav(path, samples, sampleRate) {
  const data = Buffer.alloc(samples.length * 2);
  for (let index = 0; index < samples.length; index += 1) {
    const clipped = Math.max(-1, Math.min(1, samples[index]));
    data.writeInt16LE(Math.round(clipped * 32767), index * 2);
  }
  const header = Buffer.alloc(44);
  header.write("RIFF", 0);
  header.writeUInt32LE(36 + data.length, 4);
  header.write("WAVE", 8);
  header.write("fmt ", 12);
  header.writeUInt32LE(16, 16);
  header.writeUInt16LE(1, 20);
  header.writeUInt16LE(1, 22);
  header.writeUInt32LE(sampleRate, 24);
  header.writeUInt32LE(sampleRate * 2, 28);
  header.writeUInt16LE(2, 32);
  header.writeUInt16LE(16, 34);
  header.write("data", 36);
  header.writeUInt32LE(data.length, 40);
  await writeFile(path, Buffer.concat([header, data]));
}

function fusionner(found, silenceMin) {
  if (found.length === 0) return found;
  const merged = [found[0]];
  for (const item of found.slice(1)) {
    const previous = merged[merged.length - 1];
    const gap = item.start - (previous.start + previous.duration);
    if (gap < silenceMin) {
      previous.duration = item.start + item.duration - previous.start;
    } else merged.push(item);
  }
  return merged;
}

if (process.argv[1] && process.argv[1].endsWith("aligner.mjs")) {
  const values = {};
  const argv = process.argv.slice(2);
  for (let index = 0; index < argv.length; index += 2) {
    values[argv[index].replace(/^--/, "")] = argv[index + 1];
  }
  const phrases = JSON.parse(await readFile(values.phrases, "utf8"));
  const wav = await lireWav(values.wav);
  const prises = segments(wav.samples, wav.sampleRate);
  process.stdout.write(`${JSON.stringify(aligner(phrases, prises))}\n`);
}
