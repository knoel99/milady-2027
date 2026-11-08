# Scenes batch 3 — done (2026-11-08)

Units in order: ch09, chSOA2, ch10, ch10q, ch11, all pushed to main. Every unit: `make check` (estimated and French
estimate; no narration audio in the clone) with 0 errors, `make det` exit 0, a draft built. No independent subagent
review was run for any unit (lead's instruction, token budget): CONTRACT §13.5 item 8 is not met for this batch.
Details per unit in `script/_review/scenes_<unit>.md`.

**ch09** (3b6257c). 7 pages. New `tools/data_ch09.py` → `data/ch09_rice.json` (Rice check, factors, spread ratios).
09.3 deps changed to the four available `e1_samples_*` files because `data/ch09_sweep.json` does not exist (the sweep
is shown on four Γ only). Known issues: see the unit report.

**chSOA2** (4b4b9f7). 9 pages, shared map helper `SM.map` in `chSOA2_kit.js`; pins and verdicts transcribed from
`entry.params` (no data file). The chSOA1 map module does not exist, so SOA2.1 redraws a simple century map.
chSOA2.Q: why/unblocks texts too long for the card (3 warnings, card enlarged by a page workaround). SOA2.7 has 4 QA
false positives (formula subscript).

**ch10** (f7ef247). 11 pages, `UK.seat` / `UK.formulaLayers` helpers. Only the pending seat variants are tested (no
cloud data). `data/fm3d_guarantees.json` (10.6) is missing: rendered as pending/AWAITING. Two formulas (10.5, 10.8)
and ch10.Q `unblocks` are too long (warnings). Kit issues filed: `Kit.seat` throws on result-only cues, does not
return its plot; `Kit.formulaLayer` leaves an empty frame between items.

**ch10q** (323a197). 6 pages. Board built from the current register (37 questions; Q15 LATU grid vs SFEMaNS mesh,
Q31 PBFM positioning, Q32–Q37 new short labels) in `scenes/ch10q/ch10q_board.js`, not from the old 30-ticket
`params.board`. QA items in 10q.1/10q.5/10q.6 are tickets crossing mid-move; resting layouts are clean. The writer should
refresh `params.board` and on-screen labels in the script to the current register.

**ch11** (b82c62f). 3 pages. New `tools/data_ch11.py` → `data/ch11_measured.json` and `data/ch11_ledger.json` (all six
bets awaiting, `pending: true`); `entry.data` of 11.1 and 11.2 set. 11.1 has 5 QA false positives (pen underline on a
span inside its label). The ledger still has to be refreshed by `data_cloud.py` once cloud results exist. 2D compass
instead of WebGL in 11.2.

Blockers for the final render: narration timing not yet applied in this clone (estimated only); `fm3d_guarantees.json`
missing; no cloud result files, so no result variant was rendered.
