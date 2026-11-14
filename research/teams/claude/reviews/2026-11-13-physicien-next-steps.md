# Consultation of the `physicien` role: three ranked conjectures after H28, H32 and H33 (E4)

Date: 2026-11-13, 12:46–13:10 UTC, commit 092af2e. Question put by the main session: why the model trained on the data has a deficit of magnetic energy that the same model trained on Gaussian data has not, why the network anchored on G1 learns nothing, which property makes the reference field smoother than a Gaussian field with its covariance, and which three experiments are the most useful with about 100 USD of GPU left. The role edits nothing and decides nothing; its report is copied below. Everything marked "diagnostic" is a CPU check by the role on `experiments/data_e4` (first realisation, one draw), not a result of the study.

## 1. Conjectured: the null excess is a missing fast alignment of B by the flow, plus a slow part

- Mechanism. By B → −B, cov(u, B) = 0, so G1 draws u and B independently. In the reference the flow aligns the small scales of B within about 1/(u_rms k_f) ≈ 0.6 (1/(ηk²) ≈ 1 at k = 4–5), so B varies little along itself.
- Diagnostic (η = 0.049). ⟨|B·∇B|²⟩/⟨|B|²|∇B|²⟩ is 0.134 for the reference and 0.186 for a Gaussian with its moments. Restarting the solver from 96 such Gaussian states:

| τ | 0 | 0.5 | 1 | 2 | 8 |
|---|---|---|---|---|---|
| nulls / reference | 2.09 | 1.49 | 1.44 | 1.29 | 1.06 |
| \|det ∇B\| / reference | 1.45 | 1.27 | 1.24 | 1.14 | 1.00 |
| tension ratio | 0.186 | 0.143 | 0.131 | 0.129 | 0.132 |

  The control restarted from reference snapshots stays at 0.89–0.96.
- Limit. As τ → ∞ every law gives the reference, so only τ ≤ 2 is informative (the k = 1 field decorrelates in 45–75 time units).
- Refutation (seed means, each held-out η, both realisations). Refuted if at τ = 1 the null error of G1 or W16 exceeds 0.6 of its τ = 0 value. Also refuted if the residual burn-in τ* of W16 is not shorter than that of G1, where τ* is the first τ with null error ≤ 0.2 and |E_B/ref − 1| ≤ 0.05.
- Protocol. In `Context.restart_drift`, record `null_count`, the tension ratio and the mean |det ∇B| of the restarted states at each τ. Run groups G and R plus a reference control, `--quick` first.
- Cost. No new data; about 3 GPU-h for both realisations.
- Consequence. It names the statistic behind C5. C5 could then be met only by a generator followed by a short relaxation, reported as such, and τ* would replace T1.

## 2. Conjectured: across the threshold, second moments linear in η are right and smooth η-conditioning of a flow is not

- Mechanism. E_B is 0.078, 0.097, 0.111 at η = 0.080, 0.0725, 0.0658, a slope of about −2.4 that extrapolates to zero near η ≈ 0.11. That is a pitchfork: amplitude ∝ √(η_c − η), covariance ∝ (η_c − η)₊, piecewise linear in η. G1's interpolation is then exact outside the interval holding η_c, while a flow needs an infinite slope there (Proposition 9, attenuated form).
- Orders of magnitude. The amplitude relaxes in 1/(2γ) with γ ≈ (η_c − η)k², so 50–250 time units within 0.01 of η_c. The 200 + 200 protocol is too short in that band: lengthen the burn-in as 1/|η − η_c| or exclude it.
- Limit. For η > η_c, B ≡ 0.
- Refutation (η ∈ [0.07, 0.13], 11 values, held out nearest each side of η_c and one far). Two measures: the relative E_B error at the held-out η just below η_c, and E_B above η_c over E_B(0.08). (i) For W9 conditioned on η, refuted if both are < 0.1 (prediction: ≥ 0.3 and ≥ 0.05). (ii) For W9 conditioned on s = √max(η_c − η, 0), with η_c from a linear fit of the training E_B, refuted if the errors are not at most half those of (i). G1 is the control.
- Cost. A CPU growth-rate bisection for η_c first, then about 5 GPU-h for both realisations.
- Consequence. This is the report's test of Proposition 9 and of generalisation across a bifurcation. No objective moves.

## 3. Conjectured: the W9 deficit is not a sample-size effect

- Diagnostic. The k = 1 field is 95 % negative-helicity Beltrami and decorrelates in 17, 24, 45, 75 time units at η = 0.080, 0.0725, 0.049, 0.033. That leaves about 140, 100, 50, 30 independent large-scale states per η among 2400 snapshots. The same-trajectory nearest neighbour sits at 0.47 of the typical distance; other trajectories at 0.9.
- Argument. A sample-size cause predicts the largest deficit at the smallest η. The measured order is the opposite (15, 12, 11 %). It follows corr(E_u, E_B) = −0.93, −0.85, −0.69, which is zero in G1: the flow is quenched when B is strong, a u-B-B moment. The sign of the bias is not derived.
- Toy. A 2D law U = U₀ − cA² plus noise with A symmetric, fitted by a small flow, to see whether underfitting loses ⟨A²⟩ (CPU, minutes).
- Refutation. Use 96 trajectories × 25 snapshots, with the same 2400 per η and the same iterations. Refuted if the deficit is ≤ 6 % at each held-out η; supported if it stays ≥ 9 %.
- Condition. Run it only if H34 shows no deficit.
- Cost. About 4.5 GPU-h for both realisations (data CPU × 2.5).
- Consequence. If refuted, "longer and wider is worse" becomes memorisation of 30–140 states, and E4 needs more trajectories.

## Answers outside the three

- (a) No ring or bimodality: ⟨|a|⁴⟩/⟨|a|²⟩² is 2.1–2.6 for the k = 1 amplitudes (Gaussian 2). An energy shell does exist: CV(E_B) is 0.115 and 0.089 against 0.27 for the Gaussian at the two lower η, and equal at 0.0725. It does not follow the deficit either.
- (b) Under G1 the per-sample third-order production has sd 0.08–0.095 of D, so the reference sits 1.6 to 2.9 sd away along a coupling G1's linear field cannot express. Two further conjectured ingredients: at each training η, n = 2400 < d = 5320, so the snapshots whitened by their own covariance form an orthogonal equal-norm frame (ZZᵀ = nI) and the in-sample anchor leaves nothing a smooth map can see; W9's bottleneck mixes u and B from the first step. Possible test: anchor on a low-rank G1 (about 300 pooled components plus the mode-wise rest).
- (c) See conjecture 1. Swapping the shell-1 part between reference snapshots raises |det ∇B| as much as Gaussianising (1.54 against 1.46), so the smoothness lies in the dependence between scales.

## Candidates the diagnostics argue against

- Matching E|det ∇B| by tilting G1: per-sample |det ∇B| is 0.96 correlated with E_B, so nulls rise to 3.1 times the reference.
- Tilting G1 on the energy shell: nulls go from 2.13 to 1.97 only; jointly with |det ∇B| the ESS is 0.
- Tilting G1 on the third-order production: ESS is 5 % and 0.6 %, with E_B up 15 and 32 %.
- u′ as a Stokes response to j×B: it explains ≤ 4 % of u′.

Advice of the role: test conjecture 1 first (no new data, the diagnostic already points its way, the only route seen towards the null count); conjecture 2 second, for the subject. The checks of the role ran over its allowance: about 9 min wall, 14 CPU-min on 2 threads.

## Choice of the main session

The user left the strategy to the pilot (goal of `race/PILOT-PROMPT.md`). Order chosen: conjecture 1 (restart with the null count and the gradient statistics along τ, for G1, the recoloured model and reference snapshots: registered as H35 before any run), then conjecture 2 (a range of η across the dynamo threshold), then conjecture 3 only if H34 shows that the deficit of W9 is not an effect of the time correlation.
