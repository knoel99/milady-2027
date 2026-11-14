# Spec: stationarity-identities
**Takeaway:** see brief.md. **Size:** 183 x 84 mm. Hero: none, a conceptual diagram (flat route).
**Structure:** one principle shown in three linked panels: signal (a), spectrum (b), use (c); the same identities are named in each.
Colour key (team): velocity u blue (#0072B2), magnetic field B orange/red (#D55E00), forcing grey (#6f6f6f). Extra roles in this figure only: network and "the rest" purple (#6A4C93); linear part / exact Gaussian field green (#00896A).

## Panels
| Panel | Job |
|---|---|
| a | schematic dE/dt(t) fluctuating around its zero mean vs the flat per-sample constraint (marked as not what the law says); energy identity coloured by the key |
| b | schematic k^2 H(k) by shell: negative k=1,2, positive k>=3, peak at k=4; identity sum k^2 H(k) = E[<j.B>] = 0 |
| c | generator at eta without data -> samples -> means of balances -> training loss (W5) or sampling weights (W7); measured W5 residual 0.29 -> 0.19 (5 seeds, GPU) |

## Relations
Generator -> samples -> means -> two uses; training loss -> generator (dashed feedback); weights -> reweighted samples.

## Conventions
Curve and bars are schematic: bar heights are not data, only signs, the peak at k=4 and the cancellation. Forcing grey, viscous term blue (u), Joule term orange/red (B), helicity orange/red (B).

## Negative constraints
No invented values; no number for W7; no cross-helicity result.

## Render and gate (from the repository root)
`CHROME=<path of Chrome/Chromium, add --no-sandbox in a wrapper if running as root> node .claude/skills/schematic-figure/foundation/tools/render.mjs --root site/teams/claude/figures/stationarity-identities --fig site/teams/claude/figures/stationarity-identities/figure/figure.js`
`node .claude/skills/schematic-figure/foundation/tools/check.mjs --root site/teams/claude/figures/stationarity-identities --fig site/teams/claude/figures/stationarity-identities/figure/figure.js --out site/teams/claude/figures/stationarity-identities/figure/out`
The engine is referenced in place (no copy): .claude/skills/schematic-figure/foundation/.
