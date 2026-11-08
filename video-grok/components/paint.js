import { PALETTE } from "../engine/palette.js";

export function paint(stage, view) {
  stage.replaceChildren();
  stage.dataset.cue = view.cueId ?? "";
  stage.dataset.matter = view.matter;
  stage.className = "stage";
  stage.append(matterLayer(view));
  if (view.subtitle) stage.append(subtitleBand());
  const safe = el("div", "safe");
  safe.style.color = view.ink;
  if (view.badges.length) safe.append(paintBadges(view.badges));
  if (view.level) safe.append(paintLevel(view.level));
  if (view.chapterCard) safe.append(paintChapter(view.chapterCard));
  if (view.questionCard) safe.append(paintQuestion(view.questionCard));
  if (view.needle) safe.append(paintNeedle(view.needle));
  if (view.spots) safe.append(paintSpots());
  if (view.axis) safe.append(paintAxis(view.axis));
  if (view.bars) safe.append(paintBars(view.bars));
  if (view.field) safe.append(paintField(view.field));
  if (view.formula) safe.append(paintFormula(view.formula));
  if (view.waiting) safe.append(paintWaiting(view.waiting));
  if (view.subtitle) safe.append(paintSubtitle(view.subtitle));
  stage.append(safe);
}

function matterLayer(view) {
  const wrap = el("div", "matters");
  if (!view.transition) {
    wrap.append(matterPane(view.matter, "1"));
    return wrap;
  }
  const from = matterPane(view.transition.from, String(1 - view.transition.progress));
  const to = matterPane(view.transition.to, String(view.transition.progress));
  wrap.append(from, to);
  return wrap;
}

function matterPane(matter, opacity) {
  const pane = el("div", `matter matter-${matter}`);
  pane.style.opacity = opacity;
  return pane;
}

function paintBadges(badges) {
  const row = el("div", "badges");
  for (const badge of badges) {
    const pill = el("p", badge.primary ? "badge primary" : "badge");
    pill.style.background = badge.color;
    pill.style.color = PALETTE.badgeInk;
    pill.append(el("span", "badge-kind", badge.kind));
    if (badge.confidence) pill.append(el("span", "badge-note", badge.confidence));
    if (badge.source) pill.append(el("span", "badge-note", badge.source));
    row.append(pill);
  }
  return row;
}

function paintLevel(level) {
  return el("p", "level-banner", level);
}

function paintChapter(card) {
  const box = el("section", "chapter-card");
  box.append(el("p", "chapter-number", card.number));
  box.append(el("h1", "chapter-title", card.title));
  box.append(el("p", "chapter-level", card.level));
  box.append(el("p", "chapter-asks-label", "this chapter asks"));
  box.append(el("p", "chapter-asks", card.asks));
  return box;
}

function paintQuestion(card) {
  const box = el("section", "question-card");
  const pill = el("p", "badge", card.badge);
  pill.style.background = PALETTE.badge[card.badge];
  pill.style.color = PALETTE.badgeInk;
  box.append(pill);
  box.append(el("p", "question-class", card.class));
  box.append(el("p", "question-sentence", card.sentence));
  return box;
}

function paintNeedle(needle) {
  const box = el("section", "needle");
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", "0 0 200 200");
  svg.setAttribute("width", "220");
  svg.setAttribute("height", "220");
  const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  circle.setAttribute("cx", "100");
  circle.setAttribute("cy", "100");
  circle.setAttribute("r", "78");
  circle.setAttribute("fill", "none");
  circle.setAttribute("stroke", PALETTE.rule);
  circle.setAttribute("stroke-width", "4");
  const hand = document.createElementNS("http://www.w3.org/2000/svg", "polygon");
  hand.setAttribute("points", "100,28 112,108 100,100 88,108");
  hand.setAttribute("fill", PALETTE.role.field);
  hand.setAttribute("transform", `rotate(${needle.angle} 100 100)`);
  svg.append(circle, hand);
  box.append(svg);
  box.append(el("p", "needle-label", needle.label));
  return box;
}

function paintSpots() {
  const box = el("div", "spots");
  box.append(el("span", "spot"), el("span", "spot"));
  return box;
}

function paintAxis(axis) {
  const box = el("section", "axis");
  box.append(el("p", "axis-param", axis.param));
  const line = el("div", "axis-line");
  for (const tick of axis.ticks) {
    const item = el("div", tick.trained ? "tick trained" : "tick open");
    item.append(el("span", "tick-mark"));
    item.append(el("span", "tick-value", tick.value));
    line.append(item);
  }
  box.append(line);
  return box;
}

function paintBars(bars) {
  const box = el("section", "bars");
  box.append(el("h2", "bars-title", bars.title));
  if (bars.seedLabel) box.append(el("p", "bars-seeds", bars.seedLabel));
  if (bars.schematic) box.append(el("p", "bars-schematic", "schematic, not a measurement"));
  if (bars.floor) {
    const legend = el("p", "bars-floor");
    legend.append(el("span", null, bars.floor.label));
    legend.append(el("span", "bars-n", `n = ${bars.floor.n}`));
    box.append(legend);
  }
  const plot = el("div", "plot");
  for (const row of bars.rows) {
    const line = el("div", "bar-row");
    line.append(el("span", "bar-name", row.name));
    const track = el("span", "bar-track");
    const fill = el("span", "bar-fill");
    fill.style.width = `${row.fraction * 100}%`;
    fill.style.background = row.color;
    track.append(fill);
    if (bars.floor) {
      const mark = el("span", "floor-line");
      mark.style.left = `${bars.floor.fraction * 100}%`;
      track.append(mark);
    }
    line.append(track);
    if (!bars.schematic) line.append(el("span", "bar-value", row.label));
    plot.append(line);
  }
  box.append(plot);
  return box;
}

function paintField(field) {
  const box = el("section", "field");
  box.append(el("p", "field-label", field.quantity));
  const canvas = document.createElement("canvas");
  canvas.width = 520;
  canvas.height = 300;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = field.color;
  ctx.lineWidth = 3;
  ctx.lineCap = "round";
  for (const arrow of field.arrows) {
    const cx = arrow.x * canvas.width;
    const cy = arrow.y * canvas.height;
    const len = arrow.len * 36;
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(cx + Math.cos(arrow.angle) * len, cy + Math.sin(arrow.angle) * len);
    ctx.stroke();
  }
  box.append(canvas);
  return box;
}

function paintFormula(formula) {
  const box = el("div", "formula");
  if (!window.katex) throw new Error("KaTeX absent");
  for (const term of formula.terms) {
    const holder = el("span", "term");
    holder.style.color = term.color;
    holder.style.opacity = term.lit ? "1" : "0.4";
    window.katex.render(term.tex, holder, { throwOnError: true, output: "html", displayMode: false });
    box.append(holder);
  }
  return box;
}

function paintWaiting(waiting) {
  const box = el("section", "waiting");
  box.append(el("h2", "waiting-title", waiting.campaign));
  box.append(el("p", "waiting-criterion", waiting.criterion));
  box.append(el("p", "waiting-confidence", waiting.confidence));
  box.append(el("p", "waiting-label", waiting.label));
  return box;
}

function paintSubtitle(subtitle) {
  return el("p", "subtitle", subtitle.text);
}

function subtitleBand() {
  return el("div", "subtitle-band");
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  return node;
}
