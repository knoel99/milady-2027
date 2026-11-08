// tools/dbg.js: load a scene, print console output, READY state and errors for 10 s
const { chromium } = require('playwright'); const http=require('http'),fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'..'); const scene=process.argv[2];
const srv=http.createServer((q,r)=>{const p=path.join(ROOT,decodeURIComponent(new URL(q.url,'http://x').pathname)); if(!fs.existsSync(p)||fs.statSync(p).isDirectory()){r.writeHead(404);return r.end();} r.writeHead(200,{'content-type':{'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json'}[path.extname(p)]||'application/octet-stream'}); fs.createReadStream(p).pipe(r);});
srv.listen(0,'127.0.0.1',async()=>{console.log('listening'); const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']}); console.log('launched'); const pg=await b.newPage({viewport:{width:1920,height:1080}});
pg.on('console',m=>console.log('console',m.type(),m.text())); pg.on('pageerror',e=>console.log('pageerror',e)); pg.on('crash',()=>console.log('CRASH'));
await pg.addInitScript('window.__CAPTURE__=true');
await pg.goto(`http://127.0.0.1:${srv.address().port}/${scene}`, {waitUntil:'commit'}); console.log('committed');
for(let i=0;i<6;i++){await new Promise(r=>setTimeout(r,1000)); try{console.log(i, JSON.stringify(await pg.evaluate(()=>[window.READY, window.__SCENE_ERROR__||null])));}catch(e){console.log('eval fail',e.message);break;}}
try { await pg.evaluate(()=>window.seek(2)); console.log('seek ok'); } catch(e) { console.log('seek fail', e.message); }
await b.close(); srv.close();});
