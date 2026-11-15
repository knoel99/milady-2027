# DECISIONS — race-zhipu

Mission start: 2026-11-15T00:31:56+00:00. Deadline: 02:01:56+00:00 (90 min).
Budgets: LLM 5.0 USD; Runpod 5.0 USD; Scaleway uncapped.

## Strategy

The subject (`subject/stage_milady_2027.pdf`) is an internship brief: design and evaluate
**physics-constrained conditional generative models** (diffusion / flow matching) for
parameter-dependent physical fields in dynamo systems, respecting constraints (divergence-free,
energy balance), conditioned on control parameters, validated first on simple PDE benchmarks and
evaluated with statistical/physical metrics (energy spectra, helicity, divergence control,
topology preservation), delivering a comparative study + reproducible code.

Given the 90-minute deadline, we run a **compact but genuine version of that study**:

1. **2D PDE benchmark** — 2D Kolmogorov (forced Navier–Stokes) flow simulated with a
   pseudo-spectral solver at several Reynolds numbers Re (control parameter). Conditional flow
   matching generates vorticity fields given Re. Incompressibility is enforced at the *data level*
   (streamfunction/vorticity formulation ⇒ ∇·u ≡ 0 by construction). A *sampling-procedure*
   strategy adds **energy-balance guidance** at sampling (gradient penalty pulling the sampled
   field's energy toward the training-data energy at that Re — no retraining needed).
   Parameter generalisation is measured on a held-out Re (interpolation).
2. **3D benchmark** (stand-in for 3D MHD fields; DNS of 3D MHD is far outside our time/GPU budget
   — stated as a limit) — synthetic solenoidal random fields built in Fourier space from helical
   (Beltrami) modes, with parameter-dependent energy spectrum (peak wavenumber, spectral slope)
   and helicity fraction. Comparative strategies:
   - **S0** raw conditional flow matching (baseline);
   - **S1** S0 + **hard Fourier-space projection** onto the divergence-free subspace at sampling
     (data-free, sampling-level constraint);
   - **S2** **divergence-free-by-design architecture**: the network outputs a vector potential A,
     the field is B = ∇×A (structural constraint);
   - **S3** raw model + **divergence penalty in the training loss** (soft training constraint).
3. Metrics: radial energy spectrum error, divergence statistics, helicity statistics, and a
   distributional metric (RBF-MMD on summary statistics), plus sampling throughput.

All training runs on **one rented Runpod RTX 4090** (0.89 USD/h, HIGH stock; ~40 min of work).
Sub-agents draft report/auxiliary documents in parallel while training runs.

## Decisions log

- **D0 (00:37) — compute**: rent 1× Runpod RTX 4090 (pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime,
  40 GB disk, max_hours=2 ⇒ 1.78 USD committed) instead of Scaleway. Reason: Runpod boots in ~1–2 min
  (vs ~8 for Scaleway) with a ready PyTorch image; 24 GB VRAM is ample for these small models;
  keeps Runpod spend ≈ 1.8 USD of the 5 USD cap; Scaleway left unused (no cap, but no need).
- **D1 (00:37) — scope**: 2D Kolmogorov flow (Reynolds conditioning) + 3D synthetic solenoidal
  helical-field benchmark; no 3D MHD DNS (compute/time impossible in 90 min) — recorded as a
  limitation in the report; the 3D benchmark still exercises every constraint strategy the subject
  lists (model design, sampling procedures, training losses).
- **D2 (00:37) — model budget**: flow matching (rectified flow / conditional OT-CFM) instead of
  DDPM: simpler, fewer sampling steps, better fit to the deadline. One small conditional UNet per
  benchmark; ~1000–1500 training steps per run.
- **D3 (00:37) — LLM budget**: harness on glm-5.3-flash; sub-agents only for drafting
  (deepseek-v4-pro for the report prose, glm-5.3-flash for compliance/checklist scaffolding),
  target ≤ 0.3 USD total LLM spend; results/interpretation written by the harness itself.

## Session 2 (01:11–02:00)

- **D4 (01:14) — diagnosis**: the session-1 pipeline had died with the harness session (its child
  process group was killed): data were generated but 2D data were all-NaN (sigma/E_train NaN, training
  loss NaN) and 3D data had energy 3e-10 instead of 1. Root causes found in the code:
  (a) 2D dealias mask compared physical wavenumbers (2π·n) against the 2/3 cutoff → kept only |n| ≤ 3,
  killing the forcing at k_f = 4 and the initial condition;
  (b) the solver's `rhs` mixed real-space and Fourier-space tensors (returned `-ifft2(W).real` plus
  spectral `νk²ŵ` and `f̂`), so the forcing acted as a grid-scale delta of amplitude ~O(800) → blow-up
  → NaN (this, not CFL, was the true NaN source);
  (c) Biot–Savart velocity had a sign flip (u → −u) — wrong advection;
  (d) 3D mode normalization was off by N⁶ (Parseval for the unnormalized FFT).
- **D5 (01:19) — fixes**: integer-wavenumber 2/3 mask; all-spectral RK2 with correct Biot–Savart
  sign; `m *= N⁶` in the 3D generator; finiteness guards (fail fast) in both generators; three 3D
  trainings run concurrently (small models are launch-bound on the 4090); pipeline relaunched with
  `setsid nohup` so it survives session boundaries. Committed 01:19/01:32.
- **D6 (01:30) — 2D run parameters**: first relaunch (dt = 2e-4, T = 15) still diverged — with the
  forcing now active, advective CFL is the binding constraint. Set dt = 1e-4, T = 10 (transient 2.5,
  snapshot every 0.15 ⇒ 50 snapshots/ν, 250 fields total), added a per-5000-step divergence guard that
  fails fast. Viscous term is explicitly stable at these dt (max νk²dt = 0.035 ≪ 2).
- **D7 (01:33) — deliverables**: COMPLIANCE.md (14 subject instructions: 6 compliant, 4 partial with
  justification, 4 n.a. — the n.a. items are addressed to a human applicant), CHECKLIST.md (NeurIPS
  checklist), CITATION.cff written by the harness itself (no sub-agents — LLM budget and time).
- **D8 — results, figures, report §5–6**: filled from measured run artifacts: the 2D evaluation
  completed and its headline metrics + a direct model probe are reported in §5.2; 3D training losses and
  data-quality checks in §5.1/§5.3. Two further eval bugs were found and fixed during evaluation
  (`torch.rint` does not exist; `spec_train` lacks the held-out ν so the proj target is interpolated;
  `project_divfree_t` stacked non-congruent k-grid views) — all committed.
- **D9 (01:59) — delivery cut**: the 3D sampling/evaluation stage did not finish before the 02:01:56
  deadline (three eval restarts after fixing bugs; the GPU pipeline itself is sound). The report states
  this explicitly in §5.3/§6 and COMPLIANCE marks S7/S8 partial. No Hugging Face publication: the pod's
  only outbound channels were the 4 KB-capped exec RPC (SSH port 22 and the runpod HTTP proxy were
  blocked/unroutable), so multi-MB artifacts (checkpoints, field archives, figures) could not be
  transferred in time; DELIVERY.md documents regeneration instead. Delivering on time with honest,
  reproducible partial results was preferred over risking a late delivery.
