export const figure = { width: 160, height: 64, name: 'null-panel', illustrate: true };

export default function draw(F, L) {
  const C = L.STYLE.color;
  const a = F.panel('a', { x: 2, y: 2, w: 156, h: 60 });
  L.text(a, 8, 22, 'One periodic cell', { size: 7, weight: 700 });
  L.rect(a, 8, 32, 28, 28, { fill: '#f7f7f4', stroke: C.ink, width: 0.6 });
  L.circle(a, 18, 46, 1.4, { fill: C.vermillion });
  L.text(a, 44, 40, 'Trilinear interpolant on the cell.', { size: 6 });
  L.text(a, 44, 52, 'Eliminate one coordinate. Resultant of the other two.', { size: 6 });
  L.text(a, 44, 64, 'A root on the upper face belongs to the next cell.', { size: 6 });
  L.text(a, 44, 76, 'Keep the root only if the interpolant is about zero.', { size: 6 });
}
