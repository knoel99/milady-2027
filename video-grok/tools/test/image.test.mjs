import assert from "node:assert/strict";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { randomAt } from "../../engine/clock.js";
import { loadScene } from "../../engine/scene.js";
import demo from "../../engine/demo/scene.json" with { type: "json" };
import { ouvrir } from "../navigateur.mjs";
import { servir } from "../servir.mjs";

const root = join(dirname(fileURLToPath(import.meta.url)), "../..");
const scene = loadScene(demo);

test("deux captures du même repère via seek donnent la même image, et l'horloge suit t", async () => {
  const server = await servir(root);
  const { browser, page } = await ouvrir(`http://127.0.0.1:${server.port}/engine/demo/index.html`);
  try {
    const show = await capture(page, "show");
    await capture(page, "predict");
    const again = await capture(page, "show");
    const card = await capture(page, "card");
    assert.equal(show.byteLength, again.byteLength);
    assert.equal(show.equals(again), true);
    assert.equal(show.equals(card), false);
    assert.equal(pngSize(show).width, 1920);
    assert.equal(pngSize(show).height, 1080);

    const clock = await page.evaluate(() => {
      let stamp = null;
      window.requestAnimationFrame((value) => {
        stamp = value;
      });
      window.seek(2.5);
      return {
        date: Date.now(),
        perf: performance.now(),
        stamp,
        random: Math.random(),
        frame: window.__scene.last.frame,
      };
    });
    assert.equal(clock.date, 2500);
    assert.equal(clock.perf, 2500);
    assert.equal(clock.stamp, 2500);
    assert.equal(clock.frame, 75);
    assert.equal(clock.random, randomAt(scene.seed, 75)());
  } finally {
    await browser.close();
    await server.close();
  }
});

test("le texte reste à 28 px hors de la marge de 80 px", async () => {
  const server = await servir(root);
  const { browser, page } = await ouvrir(`http://127.0.0.1:${server.port}/engine/demo/index.html`);
  try {
    const cues = ["start", "predict", "show", "formula", "caveat", "card", "waiting"];
    for (const cue of cues) {
      const report = await page.evaluate((id) => {
        window.seek(window.__scene.cue(id));
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
        const items = [];
        while (walker.nextNode()) {
          const node = walker.currentNode;
          const text = node.textContent.replace(/\s+/g, " ").trim();
          if (!text) continue;
          const parent = node.parentElement;
          const style = getComputedStyle(parent);
          if (style.display === "none" || style.visibility === "hidden" || Number(style.opacity) === 0) {
            continue;
          }
          const size = Number.parseFloat(style.fontSize);
          const range = document.createRange();
          range.selectNodeContents(node);
          const rects = [...range.getClientRects()]
            .filter((rect) => rect.width > 0.5 && rect.height > 0.5)
            .map((rect) => ({ x: rect.x, y: rect.y, right: rect.right, bottom: rect.bottom }));
          items.push({ text, size, rects });
        }
        const names = [...document.querySelectorAll(".bar-name")].map((node) => node.textContent);
        return { items, names, cue: document.querySelector(".stage").dataset.cue };
      }, cue);
      assert.equal(report.cue, cue);
      assert.ok(report.items.length > 0, cue);
      if (cue === "show") assert.deepEqual(report.names, ["A", "B", "C"]);
      for (const item of report.items) {
        assert.ok(item.size >= 28, `${cue} ${item.text} ${item.size}`);
        for (const rect of item.rects) {
          assert.ok(rect.x >= 80, `${cue} ${item.text} x ${rect.x}`);
          assert.ok(rect.y >= 80, `${cue} ${item.text} y ${rect.y}`);
          assert.ok(rect.right <= 1840, `${cue} ${item.text} right ${rect.right}`);
          assert.ok(rect.bottom <= 1000, `${cue} ${item.text} bottom ${rect.bottom}`);
        }
      }
    }
  } finally {
    await browser.close();
    await server.close();
  }
});

async function capture(page, cue) {
  await page.evaluate((id) => window.seek(window.__scene.cue(id)), cue);
  return page.screenshot({ type: "png", animations: "disabled" });
}

function pngSize(buffer) {
  return { width: buffer.readUInt32BE(16), height: buffer.readUInt32BE(20) };
}
