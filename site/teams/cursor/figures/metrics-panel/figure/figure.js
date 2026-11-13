export const figure = { width: 160, height: 78, name: 'metrics-panel', illustrate: true };

export default function draw(F, L) {
  const C = L.STYLE.color;
  const rows = [
    ['C1', 'Energy distance / floor', 'lower is closer'],
    ['C2', 'max ||div B|| / ||grad B||', 'lower is cleaner'],
    ['C3', 'Mean energy balance', 'injection against dissipation'],
    ['C4', 'Spectrum plus helicity', 'two relative errors'],
    ['C5', 'Null-count error', 'Haynes–Parnell'],
  ];
  const a = F.panel('a', { x: 2, y: 2, w: 156, h: 74 });
  rows.forEach((row, i) => {
    const y = 22 + i * 12;
    L.box(a, 8, y, 16, 9, row[0], { fill: '#e8eef6', stroke: C.ink, r: 1, F, name: row[0] });
    L.text(a, 30, y + 6, row[1], { size: 6 });
    L.text(a, 148, y + 6, row[2], { anchor: 'end', size: 5 });
  });
}
