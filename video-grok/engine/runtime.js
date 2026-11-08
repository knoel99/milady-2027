import { createClock, randomAt } from "./clock.js";
import { cueTime, loadScene, viewAt } from "./scene.js";
import { paint } from "../components/paint.js";

export function mount(raw, stage) {
  const scene = loadScene(raw);
  const clock = createClock(scene.fps);
  const queue = [];

  Date.now = () => clock.snapshot().millis;
  performance.now = () => clock.snapshot().performanceMillis;
  window.requestAnimationFrame = (callback) => {
    queue.push(callback);
    return queue.length;
  };
  window.cancelAnimationFrame = (id) => {
    queue[id - 1] = null;
  };

  function flush() {
    const stamp = clock.snapshot().performanceMillis;
    for (let round = 0; round < 5; round += 1) {
      const batch = queue.splice(0);
      if (batch.length === 0) break;
      for (const callback of batch) {
        if (callback) callback(stamp);
      }
    }
    queue.length = 0;
  }

  function seek(t) {
    clock.seek(t);
    const snap = clock.snapshot();
    Math.random = randomAt(scene.seed, snap.frame);
    const view = viewAt(scene, snap.t);
    paint(stage, view);
    flush();
    window.__scene.last = {
      t: view.t,
      frame: view.frame,
      cueId: view.cueId,
      millis: snap.millis,
      performanceMillis: snap.performanceMillis,
    };
    return view.t;
  }

  const langue = new URLSearchParams(window.location.search).get("lang");
  if (langue === "fr" || langue === "en") document.documentElement.lang = langue;
  window.seek = seek;
  window.__scene = {
    cue(id) {
      return cueTime(scene, id);
    },
    last: null,
  };
  seek(0);
  return { seek, scene };
}
