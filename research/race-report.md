# Race report — team claude (pilot)

Branch `claude/modest-newton-zx8fqs`; one session from 2026-11-12 16:45 UTC to 2026-11-13 04:30 UTC; main session Fable, effort high; stopped because the goal of the pilot was reached, not on a budget. One experiment, E4: conditional generative models of a helically forced 3D MHD dynamo (16³ grid, 665 Fourier modes, Re = 10), conditioned on the magnetic diffusivity η. Numbers: `experiments/results/digest.md` (sections E4), five model seeds, held-out η. Deliverables: `site/teams/claude/` (report in HTML and PDF, explorer, 8 schematics, 3 diagrams, 13 data plots; `tools/check_deliverables.py --team claude --built`: 33 of 33).

## Measured

- Zero divergence is exact by design (vector potentials) or by projection (1e-8); a divergence penalty leaves 0.26 and doubles the distance to the reference law.
- Every model of the first protocol is 117 to 519 noise floors from the reference in energy distance. The same network with an explicit mode-wise affine term in the velocity field is at 9.3 floors (factor 22 against its matched control at 205).
- No learned model beats two Gaussian laws without a network. Per Fourier mode (G0): 3.5 floors, but no magnetic production (magnetic balance residual 0.998). With the covariance between modes (G1, fitted on the training η): 2.6 floors, magnetic balance 0.072, null-count error 1.10 against 1.67 for the best learned model, restart drift of the magnetic energy 0.064 against 0.124; confirmed on a second realisation of the data.
- A law-level stationarity loss lowers the residual of the energy identity at η without data (0.29 → 0.19 on a wrong model, 0.057 → 0.029 on a nearly right one), not that of the identity E[⟨j·B⟩] = 0, and on the nearly right model it raises the distance from 9.3 to 16.4 floors. Exponential tilting on the same identities collapses on the wrong model and improves the nearly right one on most metrics (energy residual 0.011, effective sample 17 %).
- Longer training (8×) and wider networks do not close the gap: the loss falls and the law gets worse (W9: 9.3 → 18.8 floors; plain network: 205 floors at width 512, 25.6 at width 2048, 104 at width 5632).
- No generator, Gaussian or learned, has the reference number of magnetic null points (best: 2.1 times) or restarts in the solver without drift (best: 0.06 at τ = 4, reference below 0.01).
- An independent replication on other data seeds changes no verdict. Hypotheses of E4 (H4–H24): 9 confirmed, 11 refuted, 1 dropped; every verdict given by `encadrant` on five seeds (7 reviews), 2 reviews by `jury-externe`, all in `research/reviews/`. The first interpretation of the main result ("third-order correlations") was refuted by `jury-externe` and withdrawn.

## Published (cited, not claimed)

Flow matching, diffusion and v-prediction; divergence-free networks, projection and guidance methods; equivariant flows; the magnetic-helicity budget of periodic MHD; energy distance; the trilinear null-point method; weak stationarity identities as the loss of a sample generator. References and their verification status: `docs/specs/sources/`, and the section "State of the art" of the report.

## Conjectured

That the failure of plain networks at large width or long training is memorisation of the 14 400 training snapshots; that null points and restart drift measure the non-Gaussian part of the law that a better model should learn; that the ranking of the mechanisms carries over to turbulent regimes. Literature searches found no generative model of dynamo simulations and no use of the helicity identity, null counts or a restart test for generative models: negative statements, not proofs.

## Objectives (generator selected on validation: W9, flow matching with the affine term)

| Objective | Target | Measured | Met | Remaining work |
|---|---|---|---|---|
| C1 distance to the reference law | ≤ 10 floors | 9.35 | yes, inside the floor uncertainty (9.96 with a 20-split floor) | anchor the flow on G1 instead of the mode-wise law; confirm with a larger reference |
| C2 divergence of B | ≤ 1e-6 | 1.6e-8 | yes | none |
| C3 energy balance | ≤ 0.05 | 0.057 | no | tilting reaches 0.011 on a weighted sample; make it a resampling step, or a loss weight that does not move the law |
| C4 spectrum + helicity | ≤ 0.15 | 0.34 | no | G1 is at 0.06: a learned correction on top of G1 must not degrade it |
| C5 null points | ≤ 0.2 | 1.66 | no | no law is below 1.10: needs a training signal aimed at topology and a less Gaussian regime |
| C6 decided comparisons | ≥ 6 | 17 | yes | none |
| C7 toolbox mechanisms | ≥ 6 | 13 | yes | none |
| T1 restart drift | ≤ 0.05 | 0.124 | no | best law 0.064 (G1); measure the drift as a curve, not at one time |
| T2 polarity symmetry | ≤ 0.03 | 0.019 | yes | none |

The objectives were written on day 1 and not changed. The selected generator is the best learned one; the Gaussian baselines are not candidates (the objective names the model family; the exclusion was coded after their results were known). G0 would meet 7 of 9.

## Budget and incidents

GPU: 28 ledger entries, 16.6 h, 15.78 USD of 140 (`research/compute-ledger.jsonl`); no pod left running. Claude: 149 USD API-equivalent at 03:42 UTC, no usage warning, every role call conforming (`research/usage/latest.md`). Incidents, each repaired with a test and announced in the journal: GPU capacity refusals; job status unread behind a proxy; pods deleted by another session of the shared account; two restarts of the session (`collect`); a file-naming bug that would have lost a run; one job launched twice (0.36 USD).

## Remaining work

A flow-matching correction anchored on G1 with a local architecture; the magnetic energy balance and a restart curve among the objectives; a 64³ box at higher Reynolds number and a range of η across the dynamo threshold, where the law is less Gaussian; topology-aware training; a nearest-neighbour test of memorisation for the wide and long-trained networks.
