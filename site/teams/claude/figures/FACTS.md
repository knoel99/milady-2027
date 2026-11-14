# Facts for the figures of team claude (experiment E4)

Source of every statement: the code and results of this branch (`experiments/e4_*.py`, `src/milady/train/constraints.py`,
`experiments/results/`, `research/journal.md`, `research/hypotheses.json`). A figure must not show or imply anything that
is not here. Numbers marked *(pending)* are not final: do not draw them.

## The physical system (measured in this repository unless said otherwise)

- 3D incompressible magnetohydrodynamics in the periodic box [0, 2π)³, Alfvén units:
  ∂t u = u × ω + j × B − ∇Π + ν ∇²u + f, ∂t B = ∇ × (u × B) + η ∇²B, ∇·u = ∇·B = 0, ω = ∇ × u, j = ∇ × B.
- Forcing: constant ABC force (A = B = C = 1) at wavenumber k_f = 2, amplitude ν k_f²:
  f ∝ (sin k_f z + cos k_f y, sin k_f x + cos k_f z, sin k_f y + cos k_f x). It is helical (∇ × f = k_f f).
- ν = 0.05 fixed (Re = 1/(k_f ν) = 10). Control parameter: the magnetic diffusivity η, 11 values log-spaced from 0.08 to 0.03,
  i.e. Rm = 1/(k_f η) from 6.25 to 16.7. Dynamo threshold near Rm ≈ 5 (exploratory, not a result).
- Solver: pseudo-spectral, `milady.sim.mhd3d`, grid 16³ with the 2/3 rule: the modes |m_i| ≤ 5 are kept.
  Convergence checked at 24³ and 32³ and with half the time step: energies and helicity agree within 1–2 standard errors.
- Saturated dynamo, statistically stationary. From η = 0.08 to η = 0.03: kinetic energy E_u falls from 0.48 to 0.25, magnetic
  energy E_B rises from 0.08 to 0.17, magnetic helicity H_M = ⟨A·B⟩ goes from −0.044 to −0.10.
- The magnetic field has a large-scale part at k = 1 (about 40 % of E_B) with negative magnetic helicity; the helicity
  spectrum H(k) is negative at k = 1 and k = 2 and positive for k ≥ 3 (positive part of k² H(k) peaks at k = 4).
- Exact identities of the stationary law (each mean is zero): energy ⟨f·u⟩ − ν⟨|ω|²⟩ − η⟨|j|²⟩; magnetic helicity ⟨j·B⟩
  (from d⟨A·B⟩/dt = −2η⟨j·B⟩); cross helicity ⟨f·B⟩ − (ν + η)⟨ω·j⟩. Measured on the reference: energy residual of a few 1e-4 of the dissipation.
- Magnetic null points (B = 0): 20 per snapshot at η = 0.08 to 52 at η = 0.03 (trilinear method, 48³ evaluation grid).

## Data and protocol

- Per value of η: 24 independent trajectories, transient 200 time units, then one snapshot every 2 time units over 200:
  2400 snapshots of (u, B).
- The 11 values of η alternate: 6 training values (indices 0, 2, 4, 6, 8, 10), 2 validation values (3, 7), 3 held-out test
  values (1, 5, 9). The test values are used neither for training nor for choosing the model.
- 5 model seeds per variant; every quoted comparison is a paired difference over the 5 seeds (mean ± standard error).
- Noise floor of the energy distance: distance between two reference subsamples of 512 snapshots drawn from disjoint halves of
  the 24 trajectories. The reported number is the ratio "energy distance to the reference / floor".
- Hypotheses are registered with a quantitative refutation criterion before the computation; a supervisor role (`encadrant`)
  recomputes and gives the verdict.

## The generative pipeline

1. Snapshot (u, B) on the 16³ grid → Fourier transform → the modes |m_i| ≤ 5: 665 independent complex modes (one per pair m, −m).
2. Vector potentials in Coulomb gauge, Â = i k × B̂ / |k|² (same for u), written in the Craya–Herring basis (e₁, e₂) of the
   plane perpendicular to k: 2 complex numbers per mode and per field, i.e. a latent of 665 × 8 = 5320 real numbers.
   (The unconstrained baseline keeps the 3 complex components of û and B̂ instead: 7980 real numbers.)
3. Per-mode normalization (mean and standard deviation).
4. Conditional flow matching: noise x₀ ~ N(0, I), data x₁, straight path x_t = (1 − t) x₀ + t x₁; a network v_θ(x, t, c)
   learns the velocity x₁ − x₀; the condition is c = normalized log η.
5. Sampling: integrate dx/dt = v_θ from t = 0 to 1 (Heun, 50 steps).
6. Decoding: B̂ = i k × Â, u likewise, inverse Fourier transform. Zero divergence by construction (measured: 1e-8, float32).

## Constraint mechanisms compared (names of the variants)

Where a mechanism acts, in the words of the internship offer: **model design**, **training loss**, **sampling procedure**.

- Design: vector potentials (W4); B → −B equivariant velocity field (W4s); explicit mode-wise affine term of the velocity
  field, v = G(t, η) x + b(t, η) + network (W9); anchor on the exact field of a Gaussian law (W10), with a learned affine
  correction (W11).
- Loss: penalty on the divergence of the end-of-path prediction x̂₁ = x_t + (1 − t) v (W1); law-level stationarity loss on the
  energy and magnetic-helicity identities, imposed at values of η without data (W5; W5_control is the same fine-tuning without it).
- Sampling: Leray projection of the final samples (W2); projected flow: projected noise and projection of every integration
  stage (W3); exponential tilting of the samples on the identities (W7); per-sample rescaling of the small scales to the
  energy balance (W8).
- Baselines and model families: free Fourier components, no constraint (W0); variance-preserving diffusion with ancestral
  sampling (W6); G0: a conditional Gaussian law with one mean and one 8 × 8 covariance per Fourier mode, no network.

## Metrics (all on held-out η unless said otherwise)

- Energy distance between generated and reference snapshots on physical features (log shell spectra of u and B for k = 1…8,
  relative kinetic, magnetic and cross helicities, log energies), divided by the noise floor.
- Relative divergence ‖∇·B‖ / ‖∇B‖.
- Residual of the mean energy balance, |E[⟨f·u⟩ − Dν − Dη]| / E[Dν + Dη].
- Relative error of the shell spectrum E_B(k) and of the mean magnetic helicity.
- Relative error of the mean number of magnetic null points.
- Restart drift: the generated snapshots are advanced by the solver over τ = 4 time units; relative change of the
  ensemble-mean magnetic energy (zero for the true stationary law; 0.006 for reference snapshots).
- Polarity asymmetry |P(⟨u·B⟩ > 0) − ½| (the equations are symmetric under B → −B).

## Results that are final (5 seeds, GPU run of the registered protocol; verdicts of the supervisor role)

- Every generator of the registered protocol (W0–W6) is far from the reference law: 177 to 519 times the floor on held-out η.
- Refuted: potentials better than free components (W0 236 against W4 256); projected flow better than final projection
  (177 against 179); equivariance lowers the polarity asymmetry (both at the sampling floor).
- Confirmed: the divergence penalty does not enforce the constraint (divergence 0.21 against 0.38, energy distance twice worse);
  the stationarity loss lowers the energy residual (0.29 → 0.19); flow matching beats diffusion at held-out η (256 against 519)
  but not at training η (175 against 160); the divergence of the free model does not depend on the number of integration steps.
- Results of G0, W9, W10, W11 on 5 seeds: *(pending)*. On 2 CPU seeds: G0 is at 3.3 times the floor with an energy residual of
  0.002, but has 3.3 times too many null points and a restart drift of 0.21; W9 is at about 10 times the floor.

## Compute path (what the pilot measured)

- Session: a Claude Code cloud container with 4 CPU cores, no GPU. GPU jobs: `tools/runpod_job.py run` rents a RunPod pod,
  which clones the pushed commit, installs the pinned packages in a virtual environment, runs the command under a time limit,
  serves its outputs over HTTP under a random path; the tool fetches them, deletes the pod and writes the cost in
  `research/compute-ledger.jsonl`. Results are committed and pushed; `experiments/digest.py` builds the digest.
- Measured: full protocol (5 seeds, 9 variants) 83 min and 1.02 USD on an RTX PRO 4500; a training takes 35–60 s on the GPU
  against 15 min on a CPU core; solver 64³: 4.9 ms per step on an RTX A6000 (float32), 3.9 ms on an RTX PRO 4500 (float64).
- Failures found and repaired in the tool, in order: no capacity (retry); job status never read (the HTTP proxy refuses the
  default Python user agent); pod set-up broken by a system package; another session sharing the account deleted the running
  pods (per-team pod names); the session restarted and orphaned a running job (`collect` takes it over).

## Team organisation

- Main session (model Fable, effort high): reads, states hypotheses, writes code, runs computations, writes.
- Roles (sub-agents, never edit files): `physicien` (conjectures with refutation criteria), `encadrant` (tries to refute,
  one verdict per criterion), `biblio` (prior art and references), `jury-externe` (milestones).
- Registers: `research/hypotheses.json`, `research/journal.md`, `research/reviews.jsonl`, `research/compute-ledger.jsonl`,
  `research/usage/latest.md`.

## Why the first generators fail, and the remedies (status of each statement given)

- Measured: the networks of W0–W6 are residual MLPs of width 512 for a latent of 5320 (potentials) or 7980 (components)
  dimensions. Their flow-matching loss ends at 1.60–1.63, above π/2 ≈ 1.571, the loss of the exact (linear) field for
  independent unit Gaussian coordinates: they do worse than the trivial Gaussian field, and their samples are over-dispersed
  (2 to 3 times too many null points, fluctuations of dE/dt 2 to 14 times the reference).
- Exact (elementary): for Gaussian data x₁ ~ N(μ, Σ) and noise x₀ ~ N(0, I), the optimal velocity field is affine in x,
  v(x, t) = μ + (tΣ − (1 − t)I)(t²Σ + (1 − t)²I)⁻¹(x − tμ).
- Conjectured (supervisor role: a conjecture until a width scan, hypothesis H21, is done): the cause is that a network narrower
  than the latent dimension cannot carry the linear part of the field.
- Remedies tested: G0, the mode-wise Gaussian law itself (no network); W9, an explicit mode-wise affine term G(t, η) x + b(t, η)
  learned next to the network; W10, the exact Gaussian field plus a network; W11, the exact Gaussian field plus a learned affine
  correction plus a network.
- Measured on 2 CPU seeds (5-seed results pending): G0 3.3 times the floor; W9 9.1 and 10.6; W10 44.7 and 46.3 (worse: the
  network's own linear part perturbs the second-order statistics that the fixed Gaussian field had right); W11 9.3 and 7.6.
  G0 has the best spectra and energy balance but 3.3 times too many null points and a restart drift of 0.21; W9 and W11 have
  fewer spurious nulls (error 1.7) and a smaller drift (0.12).
