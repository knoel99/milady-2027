export const figure = { width: 160, height: 64, name: 'balance-panel', illustrate: true };

export default function draw(F, L) {
  const C = L.STYLE.color;
  const a = F.panel('a', { x: 2, y: 2, w: 76, h: 60 });
  L.text(a, 8, 22, 'Total balance', { size: 7, weight: 700 });
  L.text(a, 8, 36, 'injection = viscous + ohmic', { size: 6 });
  L.text(a, 8, 52, 'Second-half mean |residual|', { size: 5 });
  L.text(a, 8, 64, '3.74e-6 on five seeds', { size: 6, weight: 700 });
  const b = F.panel('b', { x: 82, y: 2, w: 76, h: 60 });
  L.text(b, 8, 22, 'Magnetic residual', { size: 7, weight: 700 });
  L.text(b, 8, 36, 'exchange kept, no growth subtracted', { size: 5 });
  L.text(b, 8, 52, 'Same window, mean |residual|', { size: 5 });
  L.text(b, 8, 64, '0.067, above 0.05', { size: 6, weight: 700 });
}
