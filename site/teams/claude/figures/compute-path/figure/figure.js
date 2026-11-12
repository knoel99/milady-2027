// Figure: compute path of the pilot (team claude, E4). Content only from site/teams/claude/figures/FACTS.md.
// Hero: none, a flow diagram of a tool chain (boxes and arrows); flat route, no 3D part.
export const figure = { width: 183, height: 100, name: 'compute-path', format: 'journal' };

export default function draw(F, L) {
  const C = L.STYLE.color, INK = C.ink, MID = C.mid;
  const BAD = '#B2182B';                       // failure markers only (not a data colour)
  const badge = (p, x, y, n) => {
    L.circle(p, x, y, 4.2, { fill: BAD, stroke: '#fff', width: 0.6 });
    L.text(p, x, y + 0.2, String(n), { anchor: 'middle', valign: 'middle', size: 6, weight: 'bold', color: '#fff' });
  };

  // ---------------------------------------------------------------- a: the path
  const a = F.panel('a', { x: 0, y: 0, w: 183, h: 56 });   // 519 x 159 pt
  // session container
  L.rect(a, 12, 4, 184, 152, { fill: C.tintGrey, stroke: MID, width: 0.5, r: 3 });
  L.text(a, 20, 11, 'Session container', { size: 6, weight: 'bold', valign: 'middle' });
  L.text(a, 20, 19, '4 CPU cores, no GPU', { size: 5.5, valign: 'middle', color: INK });
  const sb = (x, y, w, h, t) => L.box(a, x, y, w, h, t, { fill: '#fff', stroke: INK, size: 5.5, r: 2 });
  sb(22, 34, 72, 26, 'Commit and push'); sb(112, 34, 76, 26, 'Job tool\nrunpod\\_job.py run');
  sb(112, 86, 76, 26, 'Fetch outputs,\ndelete pod'); sb(22, 86, 72, 26, 'Cost line in\ncompute ledger');
  sb(112, 124, 76, 26, 'Commit and push\nresults'); sb(22, 124, 72, 26, 'digest.py\nbuilds the digest');
  L.arrow(a, [94, 47], [112, 47], { stroke: INK, gap1: 0.5 });
  L.arrow(a, [112, 99], [94, 99], { stroke: INK, gap1: 0.5 });
  L.arrow(a, [150, 112], [150, 124], { stroke: INK, gap1: 0.5 });
  L.arrow(a, [112, 137], [94, 137], { stroke: INK, gap1: 0.5 });
  // pod
  L.rect(a, 262, 4, 250, 152, { fill: C.tintBlue, stroke: L.shade(C.tintBlue, -0.45), width: 0.5, r: 3 });
  L.text(a, 270, 11, 'RunPod pod, rented for one job', { size: 6, weight: 'bold', valign: 'middle' });
  const steps = ['Clone the pushed commit', 'Pinned packages in a virtual environment', 'Run the job under a time limit', 'Serve outputs over HTTP, random path'];
  steps.forEach((t, i) => {
    const y = 26 + i * 30;
    L.box(a, 272, y, 230, 22, t, { fill: '#fff', stroke: INK, size: 5.5, r: 2 });
    if (i < 3) L.arrow(a, [387, y + 22], [387, y + 30], { stroke: INK, gap1: 0.3, head: 2.4 });
  });
  // links between session and pod
  L.arrow(a, [188, 47], [262, 47], { stroke: INK, gap1: 0.5, width: 0.7 });          // rent
  L.text(a, 225, 41, 'rent pod', { anchor: 'middle', valign: 'middle', size: 5.5 });
  L.arrow(a, [58, 34], [272, 37], { via: [[58, 24], [250, 24], [250, 37]], stroke: MID, dash: '2 1.4', radius: 3, gap1: 0.5, width: 0.5 });
  L.text(a, 150, 24, 'pushed commit', { anchor: 'middle', valign: 'middle', size: 5.5, color: MID, halo: true });
  L.arrow(a, [272, 127], [188, 99], { via: [[232, 127], [232, 99]], stroke: INK, gap1: 0.5, width: 0.7, radius: 4 });   // fetch
  L.text(a, 226, 120, 'fetch', { anchor: 'end', valign: 'middle', size: 5.5 });
  L.arrow(a, [188, 108], [262, 148], { via: [[200, 108], [200, 148]], stroke: MID, dash: '2 1.4', gap1: 0.5, width: 0.5, radius: 3 });  // delete
  L.text(a, 232, 144, 'delete', { anchor: 'middle', valign: 'middle', size: 5.5, color: MID });
  // failure markers
  badge(a, 225, 53, 1);
  badge(a, 207, 99, 2);
  badge(a, 262, 61, 3);
  badge(a, 262, 14, 4);
  badge(a, 196, 4, 5);

  // ---------------------------------------------------------------- b: failures
  const b = F.panel('b', { x: 0, y: 59, w: 112, h: 41 });   // 317 x 116 pt
  L.text(b, 11, 6, 'Five failures, in the order found', { size: 6, weight: 'bold', valign: 'middle' });
  const fl = [
    ['No capacity', 'retry'],
    ['Job status never read', 'the HTTP proxy refuses the default Python user agent'],
    ['Pod set-up broken', 'a system package'],
    ['Running pods deleted', 'another session on the account; per-team pod names'],
    ['Job orphaned', 'the session restarted; collect takes it over'],
  ];
  fl.forEach(([t, r], i) => {
    const y = 24 + i * 18;
    badge(b, 8, y, i + 1);
    L.text(b, 17, y - 3.2, t, { size: 6, weight: 'bold', valign: 'middle' });
    L.text(b, 17, y + 4.6, r, { size: 5.5, valign: 'middle', color: INK });
  });

  // ---------------------------------------------------------------- c: measured costs
  const c = F.panel('c', { x: 104, y: 59, w: 79, h: 41 });   // 190 x 116 pt
  L.text(c, 11, 6, 'Measured on the pilot', { size: 6, weight: 'bold', valign: 'middle' });
  const m = [
    ['83 min, 1.02 USD', 'full protocol: 5 seeds, 9 variants, RTX PRO 4500'],
    ['35–60 s vs 15 min', 'one training: GPU vs one CPU core'],
    ['4–5 ms per step', 'solver at 64³ on the GPU'],
  ];
  m.forEach(([big, small], i) => {
    const y = 14 + i * 34;
    L.rect(c, 0, y, 224, 30, { fill: C.tintGrey, stroke: 'none', r: 2 });
    L.text(c, 8, y + 10, big, { size: 7, weight: 'bold', valign: 'middle' });
    L.text(c, 8, y + 21, small, { size: 5.5, valign: 'middle', color: INK });
  });
}
