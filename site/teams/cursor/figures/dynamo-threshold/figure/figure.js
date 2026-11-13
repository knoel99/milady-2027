export const figure = { width: 160, height: 68, name: 'dynamo-threshold', illustrate: true };

export default function draw(F, L) {
  const C = L.STYLE.color;
  const a = F.panel('a', { x: 2, y: 2, w: 100, h: 64 });
  L.text(a, 8, 22, 'Kinematic ABC', { size: 7, weight: 700 });
  L.text(a, 8, 36, 'u is imposed. B grows or decays.', { size: 6 });
  L.box(a, 8, 48, 36, 22, 'flow u', { fill: '#e8eef6', stroke: C.ink, r: 2, F, name: 'u' });
  L.box(a, 56, 48, 36, 22, 'field B', { fill: '#f6f1e4', stroke: C.ink, r: 2, F, name: 'b' });
  F.relate('u.right', 'b.left', 'drives');
  L.connect(F, 'u.right', 'b.left', { stroke: C.ink, label: 'induction' });
  L.text(a, 8, 92, 'Sign of λ from ln||B|| on t ∈ [T/2, T]', { size: 5 });

  const b = F.panel('b', { x: 106, y: 2, w: 52, h: 64 });
  L.plot(b, 8, 28, 40, 36, {
    xr: [8.98, 8.99], yr: [-2, 2], xlabel: 'Rm', ylabel: 'sign',
    series: [{ pts: [[8.987, -1], [8.9872, 1]], color: C.vermillion, dots: true }],
  });
  L.text(b, 28, 18, 'n = 128, seeds 0–4', { anchor: 'middle', size: 5 });
}
