# Scenes chSOA1 — build report (batch 1, 2026-11-08)

Builder: scene-builder session, batch 1. No independent review pass (tight token budget; the launch prompt asked to
skip it). Stills looked at for every scene. **A reviewer pass is still owed.**

## 0. Status

| Scene | en: errors / warnings / QA | fr | det | draft fps |
|---|---|---|---|---|
| SOA1.1 The empty map | 0 / 0 / 0 | 0 / 0 / 0 | ok | 66 |
| SOA1.2 Can a fluid make a magnet? | 0 / 1 / 0 | same | ok | 66 |
| SOA1.3 Building one | 0 / 3 / 0 | same | ok | 64 |
| SOA1.4 Computing one | 0 / 1 / 0 | same | ok | 61 |
| SOA1.5 A few dials | 0 / 2-3 / 0 | same | ok | 67 |
| SOA1.6 Where MilaDy sits | 0 / 5 / 0 | same | ok | 62 |

Estimated length 2:35 (en), 3:20 (fr). `make det U=chSOA1`: 0 DIFFERENT.
**Every remaining warning is the same documented one**: `SOA.map: no room for the named label of <pin> (it stays a
year)`. The map's lanes are 112 px tall (68 px for DATA-DRIVEN) and the 1995-2026 stretch is 440 px wide; at 28 px
the named labels of neighbouring pins cannot all coexist without overlapping each other, a year label or a pin, or
crossing the NOW hairline. Each such pin shows its full two-line callout while it is narrated, then its year.
Affected: T1958 (SOA1.2-1.3), L2006 and LDRES (SOA1.3-1.4), S2026B (SOA1.4-1.6), R2012 and R2026 (SOA1.5-1.6),
S2026C, INTERN, THESIS (SOA1.6). This deviates from params.keep_named; see finding 1.

Files: `map.js` (generated verbatim from the script: SOA1.1 `params.map`, `params.catalog`, each scene's
`keep_named`), `chSOA1_kit.js` (`SOA.map`, the shared map renderer and label placer, plus the C2 helpers),
`chSOA1.css`. chSOA2 can load the same two files (copy them: a unit never loads another unit's folder).

## 1. Deviations

Details in the AS BUILT paragraphs of `script/chSOA1.json`. Main ones: no 1.00-1.02 push; the MilaDy callout sits
over the right side of lanes 1-2, not at the top of lane 3; in SOA1.4 the INDEPENDENT chip is in lane 5 at right,
the legend at bottom left, the Re gauge in lane 5 at left; no DRESDYN precession pictogram in SOA1.3.

## 2. Script fields changed

`visual` (AS BUILT) on every scene. No data, no `deps`. Narration untouched.

## 3. Findings for the writer / map designer

1. The map cannot hold all `keep_named` labels at 28 px (list above). Options: widen the 1990-2026 segment, allow
   two-line lanes, keep fewer named pins, or accept the "callout while narrated, year after" behaviour as built.
2. `map.label_rule` asks for no callout crossing NOW; pins right of NOW (LDRES, INTERN, THESIS) have only 160 px of
   room to their right, so their labels go left of NOW.

## 4. Kit issues

1. No shared "map" component: SOA.map (lanes, piecewise time axis, glyphs, label states, placement) lives in
   `chSOA1_kit.js`; chSOA2 needs the same. Proposed: promote it to `runtime/components/` as `Kit.map`.
2. `runtime/components/hud.js`, `Kit.chip` `anchor`: no top-centre / bottom-centre anchors ('tc', 'bc'); 'c' only.
