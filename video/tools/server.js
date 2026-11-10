'use strict';
/* tools/server.js: the one static HTTP server used by capture.js, stills.js and `make serve`.
 *
 *   /<path>        -> files under video/ (scenes, runtime, vendor, data, script/_test/data ...)
 *   /site/<path>   -> files under the repository root (read-only: site assets, figures, results)
 *
 * fetch() of data files needs http (file:// blocks it). Paths are confined to their root; only GET/HEAD.
 * Usage as a module: const { serve } = require('./tools/server'); const srv = await serve(); srv.address().port
 * Usage as a program: node tools/server.js [port]   (preview a scene: http://127.0.0.1:<port>/scenes/<unit>/<file>.html)
 */
const http = require('http'), fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '..');
const SITE = path.resolve(ROOT, '..');
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.otf': 'font/otf',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.svg': 'image/svg+xml',
  '.f32': 'application/octet-stream', '.bin': 'application/octet-stream', '.csv': 'text/csv', '.txt': 'text/plain',
  '.wav': 'audio/wav', '.mp4': 'video/mp4', '.webm': 'video/webm', '.gif': 'image/gif' };

function resolve(urlPath) {
  let rel = decodeURIComponent(urlPath);
  let root = ROOT;
  if (rel === '/site' || rel.startsWith('/site/')) { root = SITE; rel = rel.slice(5) || '/'; }
  const p = path.join(root, rel);
  if (p !== root && !p.startsWith(root + path.sep)) return null;
  return p;
}

function serve(port = 0) {
  return new Promise((resolveP) => {
    const srv = http.createServer((req, res) => {
      if (req.method !== 'GET' && req.method !== 'HEAD') { res.writeHead(405); return res.end(); }
      let p;
      try { p = resolve(new URL(req.url, 'http://x').pathname); } catch (e) { p = null; }
      if (!p || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
      res.writeHead(200, { 'content-type': MIME[path.extname(p).toLowerCase()] || 'application/octet-stream', 'cache-control': 'no-store' });
      if (req.method === 'HEAD') return res.end();
      fs.createReadStream(p).pipe(res);
    });
    srv.listen(port, '127.0.0.1', () => resolveP(srv));
  });
}

module.exports = { serve, ROOT, SITE };

if (require.main === module) {
  serve(+(process.argv[2] || 8765)).then((s) => console.log(`serving ${ROOT} (and the site under /site/) at http://127.0.0.1:${s.address().port}/`));
}
