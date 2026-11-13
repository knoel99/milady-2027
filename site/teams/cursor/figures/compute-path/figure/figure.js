export const figure = { width: 160, height: 58, name: 'compute-path', illustrate: true };

export default function draw(F, L) {
  const C = L.STYLE.color;
  const a = F.panel('a', { x: 2, y: 2, w: 156, h: 54 });
  const steps = [
    ['session', 6, 'Session'],
    ['pod', 44, 'RunPod'],
    ['json', 82, 'Result JSON'],
    ['report', 120, 'Race report'],
  ];
  for (const [name, x, label] of steps) {
    L.box(a, x, 28, 30, 16, label, { fill: '#e8eef6', stroke: C.ink, r: 2, F, name });
  }
  F.relate('session.right', 'pod.left', 'next');
  F.relate('pod.right', 'json.left', 'next');
  F.relate('json.right', 'report.left', 'next');
  L.connect(F, 'session.right', 'pod.left', { stroke: C.ink });
  L.connect(F, 'pod.right', 'json.left', { stroke: C.ink });
  L.connect(F, 'json.right', 'report.left', { stroke: C.ink });
  L.text(a, 8, 58, 'Pod names start with milady-cursor-job-. The ledger stores hours and dollars.', { size: 5 });
}
