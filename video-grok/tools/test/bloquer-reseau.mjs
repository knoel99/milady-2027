import http from "node:http";
import https from "node:https";

const bloquer = () => {
  throw new Error("reseau");
};

http.request = bloquer;
https.request = bloquer;
http.get = bloquer;
https.get = bloquer;
globalThis.fetch = bloquer;
