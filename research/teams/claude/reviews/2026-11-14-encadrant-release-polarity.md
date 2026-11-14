# Review by the `encadrant` role: the polarity diagnostic and the numbers of the released models

Date: 2026-11-14, 06:18–06:22 UTC. Scope: the descriptive polarity diagnostic (`experiments/e4_polarity_diag.py`, digest, section "Polarity" of the report) and the numbers of the released models (table of the section "Data and models", `research/release/catalog.json`, the evaluation files of the release), at commit fbb819f. No new hypothesis; no GPU job. The criteria of the internship offer were given in the task. The role edits nothing; its report is copied below, and the follow-up of the main session is at the end.

No number in either item is wrong. One correction is BLOCKING: the report names one difference between the released and the cited W16, and the code has two.

| Point | Verdict | Evidence |
|---|---|---|
| A. Polarity diagnostic | CONFIRMED, one precision required | Recomputed in the scratchpad without writing to the repository: the 1/e lag and the end-of-window fraction match the JSON to two decimals at all 11 η. The quantity is what the text says: 3 wavevectors of modulus 1, 72 pairs, snapshots from t = 202. Every number of the section matches the JSON and the digest: shares 0.202–0.244; lag 17.05; 67.0, 80.5, 66.2; fractions 0.403–0.597; 198/τ from 2.46 to 11.6; 1/η from 12.5 to 33.3. The normalisation is harmless: a per-lag symmetric normalisation moves the lag by less than 2.5 %. The descriptive status and "data of the session container" are stated in the script, the digest and the report. The weakness is that no uncertainty is given (correction 2). |
| B1. "Cited" column | CONFIRMED | Seed means recomputed from the 5 + 5 committed files: all 24 rows of the table match to 3 digits. The `cited/W16` and `released/W16` catalogue entries were spot-checked on the energy-balance residual only. |
| B2. "Released" column | CONFIRMED | All five `e4_release_eval_s<k>.json` and `e4_release_w16.json` were downloaded; their SHA-256 match `SHA256SUMS`. G0, G1, W9 and W16 rows match. The W16 map used 32768 samples for all five seeds. |
| B3. Held-out samples, convention | CONFIRMED for both; one undeclared difference (REFUTED) | The map seed is `100003·s + 211 + int(1e5·η)` and the evaluation seed `100003·s + 977 + int(1e5·η)`; they never collide over seeds and η. The convention `mean_tgt + (x − mean_src) @ A` is identical to `e4_mhd3d.py` line 1211. However, the cited run symmetrises the source moments under the sign symmetry (lines 1189–1192) and `moments_w9` of the release does not. |
| B4. Sentences | Three CONFIRMED, one incomplete, one to replace | See below. |

Evidence for B4:
- **Gaussian laws.** G0 is identical on all six metrics (largest difference 4e-6). G1 is identical on four (2e-6). The G1 null-count error and restart drift differ, and not because of the draws: the generated null counts are equal (80.35 against 80.36, seed 0), but the reference count differs (implied 47.1 against 42.7 at η = 0.0331), and the restart uses 512 fields in the cited run against 128 in the release.
- **W9 "close".** Confirmed: differences are under one seed standard deviation, except the null-count error (1.03 against 1.24), which carries the same reference shift as G1.
- **W16 farther than G1 and G0.** Confirmed in 5 of 5 seeds at each η; the ranking is indeed not reproduced.

## Corrections required

1. **BLOCKING.** Replace "its map is estimated on four times fewer samples of W9 (the sampler is slow on CPU), and it is at" with: "its map is estimated on four times fewer samples of W9 (the sampler is slow on CPU) and from moments that are not symmetrised under the sign symmetry, as they are in the cited run; which of the two explains the gap was not measured (the release has no null control). It is at".
   - Smallest check: add the Gaussian null control of the cited run to `e4_release_models.py`. In the cited run that control gives 1.30, 3.30, 3.12, about the same as G1, so the estimation error was negligible at 131 072 samples.
2. **Not blocking.** After "66 to 80 at the three smallest" add: "(not monotonic in η; no uncertainty was computed, and each trajectory holds about three correlation times there)".
   - My bootstrap over trajectories gives 5–95 % intervals of 50–99, 52–90 and 54–125 at the three smallest η, and per-mode values from 39 to 104. These figures are not in the digest; add the bootstrap to the script if you want to quote them.
3. **Not blocking.** After "depend on the data and the draws alone" add: "(for G1, the null-count error and the restart drift differ: another draw of the reference count, and 128 restarted fields against 512)".
4. **Replacement of the last sentence.** "These numbers were reviewed by the `encadrant` role on 2026-11-14: both columns were recomputed from the committed and released files; the cause of the gap of the released W16 was not tested. They are a reproduction of the cited laws, not a result of the study."

## Criteria of the offer

Item B answers the deliverable "code integrated into the toolbox" and reusable fields (data, models, catalogue). Its departure is that the released W16, the law the comparative study ranks first, does not reproduce that ranking; the report says so. Item A touches only the context of the offer: it is descriptive, on reference data, and is not a model of reversals; the report says that too. The G1 null-count and restart differences and the float32 storage of the map are detail without impact.

## Not checked

- The CPU retraining itself, the weight and map files, `catalog.sqlite`, and the build commit `240b56cc1863`.
- The cause of the W16 gap.
- The catalogue beyond the one W16 spot check.
- The value 0.011 for the polarity asymmetry of the recoloured model, and the source entry for `berhanu2007`.
- `e4_polarity_diag.py` through its own `main`, to avoid rewriting the JSON; its computation was reproduced instead.

**Verdict: A and B hold numerically; the report is acceptable once correction 1 is made and the last sentence is replaced as in 4.**

Scratch files are in `/tmp/claude-0/-home-user-milady-2027/1e766245-6a94-5a0a-9347-2dc6c46309e5/scratchpad/scripts/` (`chk.py`, `pol.py`, `nul.py`) and the downloads in `/tmp/claude-0/-home-user-milady-2027/1e766245-6a94-5a0a-9347-2dc6c46309e5/scratchpad/dl/`.

## Follow-up of the main session

- Correction 1 (blocking): applied as proposed: the released W16 differs from the cited one by the number of samples of its map and by source moments that are not symmetrised under the sign symmetry; which of the two explains the gap was not measured, the release having no null control. The same is said in the race report and listed in the remaining work (a map on 131 072 samples with symmetrised moments and its null control). The code of the release is left as it built the published files.
- Corrections 2 and 3: applied (the lag is not monotonic in η and has no computed uncertainty; the two differences of G1 between the columns).
- Correction 4: the last sentence of the paragraph is replaced by the one proposed.
