export class ClockError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
}

export function createClock(fps = 30) {
  let seconds = 0;
  return {
    seek(t) {
      if (!Number.isFinite(t) || t < 0) {
        throw new ClockError("temps", "t doit être un nombre fini supérieur ou égal à 0");
      }
      seconds = t;
      return this.snapshot();
    },
    snapshot() {
      return {
        t: seconds,
        millis: Math.round(seconds * 1000),
        performanceMillis: seconds * 1000,
        frame: Math.round(seconds * fps),
        fps,
      };
    },
  };
}

export function mulberry32(seed) {
  let state = seed >>> 0;
  return function next() {
    state = (state + 0x6d2b79f5) | 0;
    let value = Math.imul(state ^ (state >>> 15), 1 | state);
    value = (value + Math.imul(value ^ (value >>> 7), 61 | value)) ^ value;
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}

export function randomAt(seed, frame) {
  const mixed = (seed + Math.imul(frame + 1, 0x9e3779b1)) >>> 0;
  return mulberry32(mixed);
}
