export const figure = { width: 160, height: 64, name: 'protocol-panel', illustrate: true };

export default function draw(F, L) {
  const C = L.STYLE.color;
  const a = F.panel('a', { x: 2, y: 2, w: 156, h: 60 });
  const rms = [8, 10, 11, 13, 14, 16];
  rms.forEach((rm, i) => {
    L.box(a, 8 + i * 18, 28, 16, 14, String(rm), { fill: '#e8eef6', stroke: C.ink, r: 1, F, name: 'r' + rm });
  });
  L.box(a, 62, 50, 22, 14, '12', { fill: '#f6e8e4', stroke: C.vermillion, r: 1, F, name: 'held' });
  L.text(a, 8, 20, 'Training Rm', { size: 6, weight: 700 });
  L.text(a, 90, 60, 'held out', { size: 5 });
  L.text(a, 8, 78, 'Seeds 0–4. Eight times from 0.25 to 2.0. Same score for the flow and the midpoint.', { size: 5 });
}
