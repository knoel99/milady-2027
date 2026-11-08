# X5a review changelog (adversarial script review, 2026-11-08)

Unit: `script/X5a.json`, "The factory floor" (extension, `insert_after: "10.3"`; scenes X5.1-X5.4 plus `X5a.Q`).

- **Validation.** The JSON is valid and keeps its formatting (indent 1, UTF-8, exact round trip).
  - `tools/assemble_cut.py --unit X5a --strict` (output in the scratchpad) raises no lint warning.
  - All 8 TeX items render with `vendor/katex` and the `Kit.MACROS` table.
  - In the assembled extended cut, the order is 10.3 → X5.1-X5.4 → X5a.Q → X1.1.
- **Pace.** Budgeted at 146 raw words per minute plus breaks, holds, lead-in and tail, with at most 130 words per minute of target.

| Scene | Target s | Words | Est. s | Dev. | Result variant |
|---|---|---|---|---|---|
| X5.1 | 40 | 87 | 39.1 | −2 % | — |
| X5.2 | 35 | 75 | 32.9 | −6 % | — |
| X5.3 | 40 | 86 | 38.4 | −4 % | 75-87 words, 34.6-39.6 s |
| X5.4 | 35 | 75 | 37.7 | +8 % (2.5-s predict hold) | 63-76 words, 32.8-38.1 s |
| X5a.Q | 9 | 16 | 9.1 | 6-10 s | — |

## Changes (what, why, evidence)

1. **X5.4 pending narration never stated the bet.**
   - The bet and the LOW confidence were only in the seat's right column. The brief (§3.2) and the outline ("pending narration states the bet and the criterion") ask for them to be spoken.
   - New s6 (cue `bet`): "A low-confidence bet: generated fields match the simulated count." `params.seat.cues.bet` is now `bet`; the result keeps it on `seat`.
   - To make room:
     - s2 is now "Lines loop around O-points and cross at X-points." (9 words instead of 13).
     - The criterion becomes "The plan lists the count, but sets no pass mark." It is still T:902-903 (tier-1 metrics list "number of X-points of a"; criteria (a)-(d) set no threshold).
     - The scene stays at 75 words.
   - s1 now marks `{metric}critic{/}`, as 10.2 does.
2. **"Sealed" contradiction in X5.2 and X5.3.**
   - X5.2.s1 said "each run seals one file", and X5.2.s5 said "Checksummed, not sealed". X5.3.s2 also said "seals one file".
   - Critique C10 and C:93: `--force` rewrites the file and updates its SHA-256.
   - Both now read "writes". "Checksummed, not sealed" now answers the "sealed in a labelled jar" of 10.2, and the visual says so.
3. **"Run" meant two things.**
   - X5.2.s1 said "each run … one file", but 10.3 and X5.3 use "sixteen runs" for the 16 trajectories that share one file (palier1_mhd2d.yaml `n_traj: 16`).
   - X5.2.s1 is now "one simulation, one file", matching 10.2's "one simulation per setting".
4. **X5.2: the design was not motivated.**
   - Old s4: "...the simulation rows can be rebuilt from files alone". It did not say why that matters.
   - It is split into "The catalog repeats that identifier and adds a checksum." and a new cue `ingest`: "So an offline cluster can rebuild its rows from the files alone."
   - Sources: C:98 ("what makes it possible to work on a cluster without network access") and C:78 (Jean Zay compute nodes have no Internet; `ingest`). The visual's ingest beat moves from "60 % of s4" to `ingest`.
5. **X5.3: two unclear or inexact statements.**
   - Old: "None of this has run yet". This clashed with test campaigns that did run. New: "This campaign has not run yet."
   - Old: "a comparable workload once took about half an hour". It did not say whose workload or when.
     - The new s6 (cue `e2`, pending only) says "The report's own data, from the same solver, took about half an hour."
     - Sources: X:69, `e2_donnees.py` about 30 min; palier1 uses the E2 solver, `mhd2d.py`; dimensionnement.md M1: E2 took 223 000 steps, palier1 198 000.
   - Confidence is now spoken ("Confidence is high: …"), as 10.4 does ("Confidence: medium").
   - s3 is shortened to hold 130 words per minute.
6. **X5.3 measured anchor overstated.**
   - Old chip: "4 simulations done in 4 s on a laptop".
   - IR:362-375: the run was on a test machine without GPU, in laptop (venv) mode, on a reduced Taylor–Green 2 × 2 campaign at 12³. That is the 3D solver, not the 2D one.
   - The chip, `measured_anchor` and `seat.why` now say "reduced test campaigns (3D, 2 × 2, 12³) … in laptop mode". A second chip gives the E2 timing.
7. **X5.4 result: overclaims in the met / not_met meanings.**
   - Old met: "the model joins its field lines like the simulation". Old not_met: "…differently".
   - A matched *mean count* of X-points does not show that field lines connect the same way.
   - New met: "Within tolerance: on this count, the model matches the simulation." New not_met: "Outside tolerance: the model's field lines cross too often, or too rarely."
8. **X5.3 result r8: "the check you just saw".** In the extended cut, X5.1 and X5.2 (about 75 s) sit between 10.3 and this line. It now reads "the first product's check", after 10.3's title "First product off the line". r4 and r5 are trimmed by 4 words.
9. **"Box" collision.** X5.4 said "periodic box", and X1, the next module, is "the twisting box" (E3). The narration, the predict card and its label now say "periodic square", like the toy's own note.
10. **X5.1.**
    - s5 now says "on an ordinary processor", echoing 10.2 (C:153: development CPU, 2 threads).
    - s2 is shortened by one word to stay at 87 words.
    - The visual quoted "a curl is just a multiplication", which is not the narration text; corrected.
11. **Source line numbers that had shifted.**
    - R:1218 → R:1214 (question 6: GPU resources at CEREA or LISN; R:1218 is now the roadmap intro).
    - X:68 → X:69 (E2 data timing).
    - The notes cite RECOMMANDATION-CLOUD §4.2 (:259, Jean Zay) as well as §0.
12. **Notes.**
    - **Open issue 1, re-run (toy field only; no simulation).**
      - The toy's 14 critical points were confirmed by Newton's method: 7 X, 7 O, min |det ∇²a| = 0.976, and all match `params.toy.points`.
      - With B = (∂y a, −∂x a) sampled from the closed form on an 'ij' grid, `xpoint_count` returns 11, 10, 9, 9 at 32², 64², 128², 256². The writer's run gave 11, 8, 10, 10, with another sampling convention.
      - The same cell test classifies 9, 8, 8, 12 points as O-points, so the #X = #O check fails at every resolution. It is the "free check on any counter" of X5.4.
      - The notes now say that the X5.4 result variant must not be played until the counter passes that check.
    - New cues (`ingest`, `e2`, `bet`).
    - Kit.seat does not draw `params.seat.why` (seat.js): the visuals of X5.3 and X5.4 now ask the scene to draw it.
    - The PACE table is updated.

## Checked and correct (no change)

- **X5.1:**
  - C:153: pseudo-spectral PyTorch, integrating-factor RK4, 2/3 dealiasing, Leray projection of u and B, 0.08 s at 64³ (2 threads), no GPU timing.
  - C:155: four RHS evaluations, 11 points drawn, |m| ≤ 21.
  - facts.md: (n−1)//3 = 21 and shape (n_traj, 3, 64, 64, 33).
  - C:176: 0.4 GB state, peak about 15× at 128³ (717 MB), about 6 and 48 GB estimates, 24 / 80 GB cards. B14 is respected: the state is drawn solid, the estimates dashed.
- **X5.2:**
  - The MFF tree (C:111-121), The Well convention and loader replay, and the 18 corruptions (C:124).
  - The catalog tables (C:130-139).
  - The `--force` / SHA-256 rule (C:93).
- **X5.3:**
  - The palier1_mhd2d.yaml values: 11 log-spaced η from 0.004 to 0.0226, n_traj 16, 32², burn-in 30, 150 snapshots, CPU only, max_parallel 11.
  - Pipeline stages and one task per grid point (C:88-96).
  - The hours query: max(n_GPU, 1) (C:144).
  - The conv_trace verdict rule and fields; the data file names match 10.3 (`palier1_sweep.json`).
- **X5.4:**
  - T:876: O = extrema, X = saddles, #X = #O for a Morse function on the torus.
  - P8:1486-1489: Prop. 7.7, index = sign det ∇²a.
  - R:232 and R:739: the offer asks for topology; none was computed.
  - The formula layer is correct. The predict beat is real: the hold is 2.5 s and the answer is in the next paragraph.
- **X5a.Q** (16 words, 9.1 s):
  - R:1213 (open question 5, topology metrics).
  - S:233: C. Nore and Y. Ponty ● on physical metrics, which include topology.
  - It is distinct from ch06.Q (statistics in general) and ends on a decision: which code, and which tolerance.

## Open points (not fixable in this file)

- **Counter (foundation engineer).** `xpoint_count` in `tools/data_cloud.py` is wrong (see change 12). It needs a bilinear-zero test per cell (P8:1497), an O count with #X = #O enforced, and a selftest on a non-separable field. Until then, `x5_xpoints.json` must not be generated.
- **Booleans.** `met` / `not_met` / `inconclusive` are still absent from the converters' `fields`. The X5.3 and X5.4 meaning sentences drop silently; with no booleans, X5.3 is at −13 % of its target.
- **Placeholders.** `{{hours}}` and `{{mean_reference}}` are digit strings from `say()`, as in other units. In result mode the lint warns "digits in narration" and `--strict` fails. This affects the whole film. If `mean_generated` is missing, the text reads "not available per generated one".
- **Symbol sheet.** The letter `a` is both the magnetic potential (X5.4, ch08, X3a) and the Rice level (X4a: "level a", r_a). The sheet lists only the second meaning. This is for the consistency editor.
- **Lexicon.** "X-point" and "O-point" have no pin yet; check them on the first synthesis.
- **ASK overlap.** The X5.3 seat ASK (lab GPUs, Jean Zay, or a rented VM) overlaps the logistics questions of ch10q. The question register should merge them.
