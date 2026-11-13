export const figure = { width: 160, height: 62, name: 'pipeline-panel', illustrate: true };

export default function draw(F, L) {
  const C = L.STYLE.color;
  const a = F.panel('a', { x: 2, y: 2, w: 156, h: 58 });
  const y = 78;
  const boxes = [
    ['data', 8, 'ABC field', 'n = 16'],
    ['pack', 46, 'Fourier pack', '|m| ≤ kmax'],
    ['flow', 84, 'ResMLP flow', 'v(x, t, Rm)'],
    ['decode', 122, 'Decode', 'real B'],
  ];
  for (const [name, x, title, sub] of boxes) {
    L.box(a, x, y - 16, 28, 32, title, { fill: '#e8eef6', stroke: C.ink, r: 2, F, name });
    L.text(a, x + 14, y + 24, sub, { anchor: 'middle', size: 5 });
  }
  F.relate('data.right', 'pack.left', 'next');
  F.relate('pack.right', 'flow.left', 'next');
  F.relate('flow.right', 'decode.left', 'next');
  L.connect(F, 'data.right', 'pack.left', { stroke: C.ink });
  L.connect(F, 'pack.right', 'flow.left', { stroke: C.ink });
  L.connect(F, 'flow.right', 'decode.left', { stroke: C.ink });
  L.text(a, 78, 28, 'Held-out Rm = 12 is never a training condition', { anchor: 'middle', size: 6 });
}
