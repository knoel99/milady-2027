import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import http from "node:http";
import { extname, join, normalize, sep } from "node:path";

const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".woff2": "font/woff2",
  ".mp4": "video/mp4",
};

export function servir(root) {
  const server = http.createServer(async (request, response) => {
    const url = new URL(request.url, "http://127.0.0.1");
    const path = normalize(join(root, decodeURIComponent(url.pathname)));
    if (path !== root && !path.startsWith(root + sep)) {
      response.writeHead(403);
      response.end();
      return;
    }
    try {
      const info = await stat(path);
      if (!info.isFile()) throw new Error("dossier");
      response.writeHead(200, { "content-type": TYPES[extname(path)] ?? "application/octet-stream" });
      createReadStream(path).pipe(response);
    } catch {
      response.writeHead(404);
      response.end();
    }
  });
  return new Promise((resolve) => {
    server.listen(0, "127.0.0.1", () => {
      const { port } = server.address();
      resolve({
        port,
        close: () => new Promise((done) => server.close(done)),
      });
    });
  });
}
