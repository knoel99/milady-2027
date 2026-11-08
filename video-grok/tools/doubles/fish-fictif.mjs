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
  const trace = {
    url,
    model: headers.model ?? null,
    authorizationOk: cle !== "" && authorization === `Bearer ${cle}`,
    body: JSON.parse(init.body),
  };
  const ligne = JSON.stringify(trace);
  if (cle && ligne.includes(cle)) throw new Error("trace");
  if (process.env.FISH_TRACE) appendFileSync(process.env.FISH_TRACE, `${ligne}\n`);
  const status = Number(process.env.FISH_STATUS ?? "200");
  const reponse = { "content-type": "audio/mpeg" };
  if (process.env.FISH_MINUTES) reponse["x-billed-minutes"] = process.env.FISH_MINUTES;
  return new Response(Buffer.from("audio-fictif"), { status, headers: reponse });
};
