import { appendFileSync } from "node:fs";
import http from "node:http";
import https from "node:https";

const bloquer = () => {
  throw new Error("reseau");
};

http.request = bloquer;
https.request = bloquer;
http.get = bloquer;
https.get = bloquer;

globalThis.fetch = async (url, init = {}) => {
  if (url !== "https://api.fish.audio/v1/tts") throw new Error("reseau");
  const cle = process.env.FISH_API_KEY ?? "";
  const headers = init.headers ?? {};
  const authorization = headers.Authorization ?? headers.authorization ?? "";
  const body = JSON.parse(init.body);
  const trace = {
    model: headers.model ?? null,
    authorizationOk: cle !== "" && authorization === `Bearer ${cle}`,
    frequence: frequence(body.text),
  };
  const ligne = JSON.stringify(trace);
  if (cle && ligne.includes(cle)) throw new Error("trace");
  if (process.env.FISH_TRACE) appendFileSync(process.env.FISH_TRACE, `${ligne}\n`);
  return new Response(wav(trace.frequence), {
    status: 200,
    headers: { "content-type": "audio/wav" },
  });
};

function frequence(texte) {
  if (texte.includes("Une contrainte peut occuper")) return 880;
  if (texte.includes("A constraint can sit")) return 440;
  return 220;
}

function wav(freq) {
  const rate = 8000;
  const count = Math.round(rate * 0.25);
  const data = Buffer.alloc(count * 2);
  for (let index = 0; index < count; index += 1) {
    const sample = Math.round(32000 * Math.sin((2 * Math.PI * freq * index) / rate));
    data.writeInt16LE(sample, index * 2);
  }
  const header = Buffer.alloc(44);
  header.write("RIFF", 0);
  header.writeUInt32LE(36 + data.length, 4);
  header.write("WAVE", 8);
  header.write("fmt ", 12);
  header.writeUInt32LE(16, 16);
  header.writeUInt16LE(1, 20);
  header.writeUInt16LE(1, 22);
  header.writeUInt32LE(rate, 24);
  header.writeUInt32LE(rate * 2, 28);
  header.writeUInt16LE(2, 32);
  header.writeUInt16LE(16, 34);
  header.write("data", 36);
  header.writeUInt32LE(data.length, 40);
  return Buffer.concat([header, data]);
}
