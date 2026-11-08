import { FRAME, PALETTE } from "./palette.js";
import { randomAt } from "./clock.js";

export class SceneError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
}

const BADGES = new Set(["MEASURED", "PROVED", "CONJECTURE", "PLANNED", "CONTEXT"]);
const MATTERS = new Set(["night", "paper", "blueprint"]);
const ROLES = new Set(Object.keys(PALETTE.role));
const LEVELS = new Set(["L0", "L1", "L2", "L3", "L4", "L5"]);
const CONFIDENCE = new Set(["high", "medium", "low"]);
const QUESTION_BADGES = new Set(["PLANNED", "CONTEXT"]);

const parsers = {
  matter(layer) {
    if (!MATTERS.has(layer.matter)) fail("matiere", "matière inconnue");
    return { kind: "matter", at: layer.at, matter: layer.matter };
  },
  transition(layer) {
    if (layer.frames !== 8) fail("transition", "une transition dure 8 images");
    if (!MATTERS.has(layer.to)) fail("matiere", "matière inconnue");
    return { kind: "transition", at: layer.at, frames: 8, to: layer.to };
  },
  badge(layer) {
    if (!BADGES.has(layer.badge)) fail("pastille", "pastille inconnue");
    if (layer.badge === "CONJECTURE" && !CONFIDENCE.has(layer.confidence)) {
      fail("pastille", "CONJECTURE exige une confiance");
    }
    if (layer.badge === "CONTEXT" && !text(layer.source)) {
      fail("pastille", "CONTEXT exige une source à l'écran");
    }
    return {
      kind: "badge",
      badge: layer.badge,
      primary: layer.primary === true,
      from: layer.from,
      until: layer.until,
      confidence: layer.confidence ?? null,
      source: layer.source ?? null,
    };
  },
  level(layer) {
    if (!LEVELS.has(layer.level)) fail("niveau", "niveau inconnu");
    return { kind: "level", level: layer.level, from: layer.from, until: layer.until };
  },
  "chapter-card"(layer) {
    return {
      kind: "chapter-card",
      from: layer.from,
      until: layer.until,
      number: text(layer.number),
      title: text(layer.title),
      level: LEVELS.has(layer.level) ? layer.level : fail("carte-chapitre", "niveau inconnu"),
      asks: text(layer.asks),
    };
  },
  "question-card"(layer) {
    const sentence = text(layer.sentence);
    const count = sentence.split(/\s+/).filter(Boolean).length;
    if (count > 18) fail("carte-question", "la phrase dépasse 18 mots");
    if (!QUESTION_BADGES.has(layer.badge)) fail("carte-question", "pastille PLANNED ou CONTEXT");
    if (!["A", "B", "C"].includes(layer.class)) fail("carte-question", "classe A, B ou C");
    return {
      kind: "question-card",
      from: layer.from,
      until: layer.until,
      sentence,
      class: layer.class,
      badge: layer.badge,
    };
  },
  waiting(layer) {
    if (!CONFIDENCE.has(layer.confidence)) fail("attente", "confiance inconnue");
    return {
      kind: "waiting",
      from: layer.from,
      until: layer.until,
      campaign: text(layer.campaign),
      criterion: text(layer.criterion),
      confidence: layer.confidence,
    };
  },
  formula(layer) {
    if (!Array.isArray(layer.terms) || layer.terms.length === 0) {
      fail("formule", "une formule a au moins un terme");
    }
    return {
      kind: "formula",
      from: layer.from,
      until: layer.until,
      terms: layer.terms.map((term) => {
        if (!ROLES.has(term.role)) fail("formule", "rôle inconnu");
        return { tex: text(term.tex), role: term.role, cue: term.cue };
      }),
    };
  },
  bars(layer) {
    if (!Array.isArray(layer.rows) || layer.rows.length === 0) fail("graphe", "aucune barre");
    const rows = layer.rows.map((row) => {
      if (!ROLES.has(row.role)) fail("graphe", "rôle inconnu");
      if (!Number.isFinite(row.value) || row.value <= 0) fail("graphe", "valeur positive");
      return {
        name: text(row.name),
        value: row.value,
        role: row.role,
        label: row.label == null ? null : text(row.label),
      };
    });
    if (layer.log === true && rows.some((row) => row.value <= 0)) fail("graphe", "logarithme");
    if (layer.seeds != null && layer.seeds !== 1 && layer.seeds !== 2) fail("graphe", "une ou deux graines");
    if (layer.floor != null && !Number.isFinite(layer.floor)) fail("graphe", "plancher");
    if (layer.floor != null && !Number.isInteger(layer.n)) fail("graphe", "n du plancher");
    return {
      kind: "bars",
      from: layer.from,
      until: layer.until,
      title: text(layer.title),
      log: layer.log === true,
      floor: layer.floor ?? null,
      n: layer.n ?? null,
      seeds: layer.seeds ?? null,
      schematic: layer.schematic === true,
      rows,
    };
  },
  field(layer) {
    if (layer.quantity !== "u" && layer.quantity !== "B") fail("champ", "u ou B");
    return { kind: "field", from: layer.from, until: layer.until, quantity: layer.quantity };
  },
  needle(layer) {
    return { kind: "needle", from: layer.from, until: layer.until, southAt: layer.southAt };
  },
  spots(layer) {
    return { kind: "spots", from: layer.from, until: layer.until };
  },
  axis(layer) {
    if (!Array.isArray(layer.ticks) || layer.ticks.length === 0) fail("axe", "aucun tick");
    return {
      kind: "axis",
      from: layer.from,
      until: layer.until,
      param: text(layer.param),
      ticks: layer.ticks.map((tick) => ({
        value: text(tick.value),
        trained: tick.trained === true,
      })),
    };
  },
  subtitle(layer) {
    const value = text(layer.text);
    if ([...value].length > 42) fail("sous-titre", "42 caractères au plus");
    if (/[\\$]/.test(value)) fail("sous-titre", "le sous-titre ne contient pas de TeX");
    return { kind: "subtitle", from: layer.from, until: layer.until, text: value };
  },
};

export function loadScene(raw) {
  if (!raw || typeof raw !== "object" || !Array.isArray(raw.cues) || !Array.isArray(raw.layers)) {
    fail("document", "document illisible");
  }
  if (raw.width !== FRAME.width || raw.height !== FRAME.height || raw.fps !== FRAME.fps) {
    fail("cadre", "le cadre est 1920×1080 à 30 images par seconde");
  }
  if (!Number.isInteger(raw.seed) || raw.seed < 0) fail("graine", "graine entière");
  if (!Number.isFinite(raw.duration) || raw.duration <= 0) fail("duree", "durée");
  const cues = parseCues(raw.cues, raw.duration);
  const layers = raw.layers.map((layer) => {
    const parse = parsers[layer?.kind];
    if (!parse) fail("document", "calque inconnu");
    const parsed = parse(layer);
    assertCues(parsed, cues);
    return parsed;
  });
  const scene = {
    id: text(raw.id),
    width: FRAME.width,
    height: FRAME.height,
    fps: FRAME.fps,
    duration: raw.duration,
    seed: raw.seed,
    cues: [...cues.values()],
    layers,
  };
  checkCards(scene);
  checkBadges(scene);
  checkTransitions(scene);
  checkFormulas(scene);
  checkSubtitles(scene);
  return scene;
}

export function cueTime(scene, id) {
  const cue = scene.cues.find((item) => item.id === id);
  if (!cue) fail("repere", `repère inconnu: ${id}`);
  return cue.at;
}

export function viewAt(scene, t) {
  if (!Number.isFinite(t) || t < 0) fail("temps", "t invalide");
  const frame = Math.round(t * scene.fps);
  const cue = [...scene.cues].reverse().find((item) => item.at <= t + 1e-9) ?? null;
  const matter = matterAt(scene, t);
  const show = (layer) => visible(scene, layer, t);
  const badges = scene.layers.filter((layer) => layer.kind === "badge" && show(layer));
  const level = scene.layers.find((layer) => layer.kind === "level" && show(layer)) ?? null;
  const chapter = scene.layers.find((layer) => layer.kind === "chapter-card" && show(layer)) ?? null;
  const question = scene.layers.find((layer) => layer.kind === "question-card" && show(layer)) ?? null;
  const waiting = scene.layers.find((layer) => layer.kind === "waiting" && show(layer)) ?? null;
  const formula = scene.layers.find((layer) => layer.kind === "formula" && show(layer)) ?? null;
  const bars = scene.layers.find((layer) => layer.kind === "bars" && show(layer)) ?? null;
  const field = scene.layers.find((layer) => layer.kind === "field" && show(layer)) ?? null;
  const needle = scene.layers.find((layer) => layer.kind === "needle" && show(layer)) ?? null;
  const spots = scene.layers.some((layer) => layer.kind === "spots" && show(layer));
  const axis = scene.layers.find((layer) => layer.kind === "axis" && show(layer)) ?? null;
  const subtitle = scene.layers.find((layer) => layer.kind === "subtitle" && show(layer)) ?? null;
  return {
    t,
    frame,
    fps: scene.fps,
    seed: scene.seed,
    width: scene.width,
    height: scene.height,
    cueId: cue ? cue.id : null,
    matter: matter.matter,
    transition: matter.transition,
    ink: PALETTE[matter.matter].ink,
    badges: badges.map((layer) => ({
      kind: layer.badge,
      primary: layer.primary,
      confidence: layer.confidence,
      source: layer.source,
      color: PALETTE.badge[layer.badge],
    })),
    level: level ? level.level : null,
    chapterCard: chapter
      ? { number: chapter.number, title: chapter.title, level: chapter.level, asks: chapter.asks }
      : null,
    questionCard: question
      ? { sentence: question.sentence, class: question.class, badge: question.badge }
      : null,
    waiting: waiting
      ? {
          campaign: waiting.campaign,
          criterion: waiting.criterion,
          confidence: waiting.confidence,
          label: "not yet run",
        }
      : null,
    formula: formula
      ? {
          terms: formula.terms.map((term) => ({
            tex: term.tex,
            role: term.role,
            color: PALETTE.role[term.role],
            lit: cue != null && term.cue === cue.id,
          })),
        }
      : null,
    bars: bars ? barView(bars) : null,
    field: field ? fieldView(scene.seed, frame, field.quantity) : null,
    needle: needle ? needleView(scene, needle, t) : null,
    spots,
    axis: axis ? { param: axis.param, ticks: axis.ticks.map((tick) => ({ ...tick })) } : null,
    subtitle: subtitle ? { text: subtitle.text } : null,
  };
}

function barView(layer) {
  const samples = layer.rows.map((row) => row.value);
  if (layer.floor != null) samples.push(layer.floor);
  const fractions = layer.log ? logFractions(samples) : linearFractions(samples);
  const rowFractions = fractions.slice(0, layer.rows.length);
  return {
    title: layer.title,
    log: layer.log,
    seeds: layer.seeds,
    schematic: layer.schematic,
    seedLabel: layer.seeds === 1 ? "one seed" : layer.seeds === 2 ? "two seeds" : null,
    floor:
      layer.floor == null
        ? null
        : { fraction: fractions[fractions.length - 1], n: layer.n, label: "noise floor" },
    rows: layer.rows.map((row, index) => ({
      name: row.name,
      value: row.value,
      role: row.role,
      label: row.label ?? String(row.value),
      color: PALETTE.role[row.role],
      fraction: rowFractions[index],
    })),
  };
}

function linearFractions(samples) {
  const max = Math.max(...samples);
  return samples.map((value) => value / max);
}

function logFractions(samples) {
  const logs = samples.map((value) => Math.log10(value));
  const lo = Math.min(...logs);
  const hi = Math.max(...logs);
  const span = hi - lo || 1;
  return logs.map((value) => (value - lo + 1) / (span + 1));
}

function fieldView(seed, frame, quantity) {
  const random = randomAt(seed, frame);
  const arrows = [];
  const cols = 6;
  const rows = 4;
  for (let y = 0; y < rows; y += 1) {
    for (let x = 0; x < cols; x += 1) {
      arrows.push({
        x: (x + 0.5) / cols,
        y: (y + 0.5) / rows,
        angle: random() * Math.PI * 2,
        len: 0.45 + random() * 0.4,
      });
    }
  }
  return {
    quantity,
    color: quantity === "B" ? PALETTE.role.field : PALETTE.role.velocity,
    arrows,
  };
}

function needleView(scene, layer, t) {
  const start = cueTime(scene, layer.from);
  const south = cueTime(scene, layer.southAt);
  const span = south - start;
  const progress = span <= 0 ? 1 : Math.min(1, Math.max(0, (t - start) / span));
  return { angle: progress * 180, label: "illustration, not to time scale" };
}

function matterAt(scene, t) {
  let matter = "night";
  const events = [];
  for (const layer of scene.layers) {
    if (layer.kind === "matter") events.push({ t: cueTime(scene, layer.at), kind: "matter", layer });
    if (layer.kind === "transition") {
      events.push({ t: cueTime(scene, layer.at), kind: "transition", layer });
    }
  }
  events.sort((a, b) => a.t - b.t);
  for (const event of events) {
    if (event.kind === "matter" && event.t <= t + 1e-9) matter = event.layer.matter;
    if (event.kind === "transition") {
      const dur = event.layer.frames / scene.fps;
      if (event.t + dur <= t + 1e-9) matter = event.layer.to;
    }
  }
  let transition = null;
  for (const event of events) {
    if (event.kind !== "transition") continue;
    const start = event.t;
    const dur = event.layer.frames / scene.fps;
    if (t + 1e-9 >= start && t < start + dur - 1e-9) {
      transition = {
        frames: event.layer.frames,
        from: matterBefore(scene, start),
        to: event.layer.to,
        progress: (t - start) / dur,
      };
    }
  }
  if (transition) matter = transition.to;
  return { matter, transition };
}

function matterBefore(scene, t) {
  let matter = "night";
  for (const layer of scene.layers) {
    if (layer.kind === "matter" && cueTime(scene, layer.at) < t - 1e-9) matter = layer.matter;
    if (layer.kind === "transition") {
      const end = cueTime(scene, layer.at) + layer.frames / scene.fps;
      if (end < t - 1e-9) matter = layer.to;
    }
  }
  return matter;
}

function visible(scene, layer, t) {
  if (layer.from == null) return false;
  const start = cueTime(scene, layer.from);
  const end = cueTime(scene, layer.until);
  return t + 1e-9 >= start && t < end - 1e-9;
}

function parseCues(list, duration) {
  const cues = new Map();
  for (const cue of list) {
    if (!cue || !text(cue.id) || !Number.isFinite(cue.at) || cue.at < 0 || cue.at > duration) {
      fail("repere", "repère illisible");
    }
    if (cues.has(cue.id)) fail("repere", "repère en double");
    cues.set(cue.id, { id: cue.id, at: cue.at });
  }
  return cues;
}

function assertCues(layer, cues) {
  for (const key of ["at", "from", "until", "southAt"]) {
    if (layer[key] != null && !cues.has(layer[key])) fail("repere", `repère inconnu: ${layer[key]}`);
  }
  if (layer.kind === "formula") {
    for (const term of layer.terms) {
      if (!cues.has(term.cue)) fail("repere", `repère inconnu: ${term.cue}`);
    }
  }
}

function checkCards(scene) {
  const chapters = scene.layers.filter((layer) => layer.kind === "chapter-card");
  const questions = scene.layers.filter((layer) => layer.kind === "question-card");
  for (const card of chapters) {
    const span = cueTime(scene, card.until) - cueTime(scene, card.from);
    if (span <= 0 || span > 4 + 1e-9) fail("carte-chapitre", "la carte de chapitre dure au plus 4 s");
  }
  for (const card of questions) {
    const span = cueTime(scene, card.until) - cueTime(scene, card.from);
    if (span < 6 - 1e-9 || span > 10 + 1e-9) {
      fail("carte-question", "la carte question dure de 6 à 10 s");
    }
  }
  rejectOverlap(scene, chapters, "carte-chapitre");
  rejectOverlap(scene, questions, "carte-question");
}

function checkBadges(scene) {
  const primary = scene.layers.filter((layer) => layer.kind === "badge" && layer.primary);
  rejectOverlap(scene, primary, "pastille");
}

function checkTransitions(scene) {
  const transitions = scene.layers.filter((layer) => layer.kind === "transition");
  for (let i = 0; i < transitions.length; i += 1) {
    const a = transitions[i];
    const a0 = cueTime(scene, a.at);
    const a1 = a0 + a.frames / scene.fps;
    for (let j = i + 1; j < transitions.length; j += 1) {
      const b0 = cueTime(scene, transitions[j].at);
      const b1 = b0 + transitions[j].frames / scene.fps;
      if (a0 < b1 && b0 < a1) fail("transition", "transitions qui se chevauchent");
    }
  }
}

function checkFormulas(scene) {
  const formulas = scene.layers.filter((layer) => layer.kind === "formula");
  rejectOverlap(scene, formulas, "formule");
}

function checkSubtitles(scene) {
  const lines = scene.layers.filter((layer) => layer.kind === "subtitle");
  rejectOverlap(scene, lines, "sous-titre");
}

function rejectOverlap(scene, layers, code) {
  for (let i = 0; i < layers.length; i += 1) {
    const a0 = cueTime(scene, layers[i].from);
    const a1 = cueTime(scene, layers[i].until);
    for (let j = i + 1; j < layers.length; j += 1) {
      const b0 = cueTime(scene, layers[j].from);
      const b1 = cueTime(scene, layers[j].until);
      if (a0 < b1 && b0 < a1) fail(code, "chevauchement");
    }
  }
}

function text(value) {
  if (typeof value !== "string" || value.trim() === "") fail("document", "texte vide");
  return value;
}

function fail(code, message) {
  throw new SceneError(code, message);
}
