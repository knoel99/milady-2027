export const figure = { width: 160, height: 70, name: 'constraint-mechanisms', illustrate: true };

export default function draw(F, L) {
  const C = L.STYLE.color;
  const panels = [
    ['a', 2, 'Design', 'Decode B = curl A', 'divergence is zero'],
    ['b', 56, 'Loss', 'Add a penalty', 'soft, during training'],
    ['c', 110, 'Sampling', 'Project after Heun', 'hard, at sample time'],
  ];
  for (const [id, x, title, line, sub] of panels) {
    const p = F.panel(id, { x, y: 2, w: 48, h: 66 });
    L.box(p, 8, 28, 32, 18, 'B', { fill: '#f6f1e4', stroke: C.ink, r: 2, F, name: 'field' });
    L.text(p, 24, 58, title, { anchor: 'middle', size: 7, weight: 700 });
    L.text(p, 24, 72, line, { anchor: 'middle', size: 5 });
    L.text(p, 24, 84, sub, { anchor: 'middle', size: 5 });
  }
}
