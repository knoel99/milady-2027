# Decisions — race-deepseek (MilaDy physics-constrained generative modelling)

Chronological log of the strategy and of every decision that changed it. Times are UTC.

## Mission interpretation

The subject (`subject/stage_milady_2027.pdf`) is an internship offer, not a protocol. Its research
requirements are: (i) implement conditional generative models (diffusion / flow matching) of physical
fields conditioned on control parameters (Re, Rm, material properties); (ii) enforce physics —
energy balance and divergence-free conditions — through architecture, losses and/or sampling;
(iii) validate first on simple PDE benchmarks, then on MHD fields with statistical/physical metrics
(energy spectra, helicity, divergence control, topology preservation); (iv) deliver a comparative
study, a concise technical report and reproducible code. We treat every such statement as an
instruction (traceability in `COMPLIANCE.md`).

## Strategy (00:33)

Deliver a compact but complete *pilot* study that is fully reproducible on CPU inside the 90-minute
mission window, instead of a large but unreproducible one. Three ingredients:

1. **Benchmarks we can solve and check**: a 1D viscous Burgers benchmark (simple PDE; energy balance
   is exact) and a 2D incompressible MHD benchmark (pseudo-spectral solver, random initial
   conditions, parameters Re and Rm). Both produce paired snapshots `(t0, t1)` so that a discrete
   energy balance and a Crank–Nicolson PDE residual can be evaluated per sample.
2. **One generative family, four constraint strategies**: conditional flow matching (CFM, linear
   interpolant) with (a) raw velocity/magnetic fields (unconstrained), (b) stream-function /
   flux-function output (divergence-free by construction), (c) (b) + physics-informed training loss
   (energy balance + PDE residual), (d) parameter-blind ablation. Post-hoc Helmholtz projection is
   evaluated as a sampling-time alternative on the raw model.
3. **Metrics that separate claims**: divergence residual, shell energy spectra, kinetic/magnetic
   energy, magnetic-potential invariant `<A^2>` (the 2D analogue of magnetic helicity, which
   vanishes identically for in-plane 2D fields), Wasserstein distances between vorticity/vector-
   potential distributions (topology proxy), discrete energy-balance residual, PDE residual,
   ensemble diversity and parameter-sensitivity slopes.

## Decisions and reasons

- **00:34 — CPU, no cloud GPU.** The models are small spectral MLPs (<=0.7 M parameters) and the
  datasets are 64^2 fields; a cloud pod would add image-pull/install latency larger than the whole
  training time. Runpod/Scaleway budgets are left untouched (cost control).
- **00:36 — spectral coefficient representation.** Fields are generated as free Fourier
  coefficients of `psi` and `A` (`u = curl(psi z)`, `b = curl(A z)`), which makes `div u = div b = 0`
  exact at every sampling step and makes the divergence-free constraint testable against a baseline
  that does not have it.
- **00:48 — first data design rejected.** The first dataset reused the same 16 initial-condition
  seeds for all 16 (Re,Rm) pairs. Training then saw only 16 distinct flows, and validation latent
  distributions were 1.6-6x wider than training: a distribution-coverage artefact, not a modelling
  result. Dataset regenerated (00:52) with independent random ICs for every (parameter, sample);
  this is the dataset used below. The failed run is logged in this file rather than hidden.
- **00:49 — full-space CFM rejected in favour of a PCA latent space.** Conditional CFM directly on
  1156 coefficients left a validation loss at chance level and made physics backpropagation the
  bottleneck. The MHD data are strongly low-rank (16 principal components explain 99.92 % of the
  variance), so the flow is learned on a whitened PCA latent (32 components, 99.985 % variance) and
  decoded linearly before the physics operators. This is a reduced-order generative model, exactly
  the interface the subject asks for ("input for reduced-order models").
- **00:50 — two-seed / three-seed design.** Three seeds for every reported MHD variant, three for
  Burgers, to report seed variability. Held-out test parameter grid (4x4 Re,Rm) plus an
  interpolation grid at Re,Rm in {75,150,300} (never seen in training) to test parameter
  generalisation.
- **00:53 — physics weights.** Energy-balance weight 0.5, PDE-residual weight 0.1, linearly ramped
  in after 300 steps and weighted by `t^2` so that the strongly noised early flow-matching times do
  not dominate. Chosen to keep the CFM loss on the same scale as the physics terms; the ablation
  (struct vs phys) measures whether it helps.
- **00:54 — budgets.** LLM spend is kept far below the 5 USD cap (the whole mission is a few
  dollars at DeepSeek prices); no cloud resources are created. Delivery before the 02:01 deadline is
  the binding constraint.

(Further decisions appended below as they happen.)

## Changes during execution (continued)

- **00:58 — solver stability and a stronger parameter regime.** The intended low-Re end
  (Re = 5) made the explicit diffusion term stiff and the MHD run overflowed at `dt=0.01`. Replaced
  the explicit diffusion with exact half-step integrating factors (Strang splitting) around the RK4
  advection; this is stable for all Re and costs nothing. At the same time the parameter grid was
  moved to `Re,Rm in {5,10,20,50}` and `t0=1.0, t1=1.2`, where the control parameters produce a
  five-fold change in mean energy (0.07 at Re=5 to 0.21 at Re=50, Rm fixed) instead of the ~1 %
  latent variance of the first grid. OOD interpolation grid `{7,14,32}`.
- **01:03 — training data are unique per sample.** 256 training fields, each with its own random
  initial condition; validation and test likewise. The first design (same 16 IC seeds reused
  across parameter pairs) was rejected at 00:48 for exactly this reason.
- **01:05 — physics loss scale corrected.** A squared, normalised energy-balance residual is
  O(1e-3) and had no gradient effect at weight 0.5. The implemented loss uses the **absolute**
  normalised residual (energy weight 1.0, PDE weight 0.05, `t^2` weighting, ramp after 300 steps),
  i.e. a ~10 % perturbation of the flow-matching objective. This is the ablation actually reported.
- **01:06 — raw baseline is trained in full coefficient space.** A PCA latent fitted to
  divergence-free data is itself divergence-free, so the raw ablation had to avoid PCA to be a
  meaningful unconstrained control. This is stated in the report.
- **01:08 — model size chosen by validation.** PCA 32 / hidden 96 gave the best held-out CFM loss
  (1.53 vs 1.75-2.16 for larger latents/models); the latent retains 95.8 % of training variance.
  Larger models overfit 256 training fields. This is a deliberate pilot-scale choice.
- **01:10 — budget guard.** Remaining LLM budget is untouched (well under 5 USD) and no cloud
  resource has been created; all remaining time is spent on experiments and the report.

## Final execution record

- **01:28 — final model set, cut to fit the window.** Delivered: MHD divergence-free CFM with 3
  seeds, physics CFM with 2 seeds, raw full-space CFM with 1 seed; Burgers structural and physics
  CFM with 2 seeds each; PCA truncation floor computed for both grids. The parameter-blind ablation
  (`noparam`) and two extra seeds were dropped when the shared CPU quota made each physics run
  3x slower than benchmarked. This is a deliberate completeness-versus-deadline trade-off; the
  remaining seed count is reported in every table and the limits are stated in `REPORT.md` §6.
- **01:31–01:38 — evaluation runs had been reading `checkpoints/` (the rejected full-space
  directory) because the argparse default was not overridden.** All final numbers were regenerated
  with `--ckptdir checkpoints_pca`; the earlier tables were discarded. The default is now fixed to
  `checkpoints_pca` and `reproduce.sh` passes it explicitly.
- **01:39 — Hugging Face publication attempted twice (dataset and model) and failed inside
  `hf_publish` with `InvalidURL: Invalid port: ':1]'`, before any upload.** The cards and files are
  staged in `hf/dataset/` and `hf/model/`; this is recorded in `DELIVERY.md`.
- **01:40 — report, checklist, compliance matrix, citation and figures frozen and committed.**
