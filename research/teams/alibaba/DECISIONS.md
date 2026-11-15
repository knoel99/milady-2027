# DECISIONS.md — race-alibaba (MilaDy: physics-constrained generative AI for parametric dynamical systems)

Mission window: 2026-11-15T00:31:53Z → 02:01:53Z (90 min). Budgets: LLM 5 USD, Runpod 5 USD, Scaleway uncapped.
This file is the running log of strategy and decisions, with time and reason.

## Strategy (00:35)

**Scope.** The subject asks for: (a) conditional generative models (diffusion or flow matching) for
parameter-dependent physical fields, (b) physics constraints (energy balance, divergence-free) imposed by design,
loss or sampling, (c) validation first on simple PDE benchmarks then on dynamo fields, (d) statistical + physical
consistency metrics (energy spectra, helicity, divergence control, topology preservation), (e) a comparative study.
With a 90-minute window and a 5 USD LLM cap we cannot run a turbulent 3D MHD dynamo campaign at high resolution.
We therefore choose the *smallest scientific setting that still exercises every requirement, with numbers that are
actually measured here*:

- **Data generator (validated):** pseudo-spectral **kinematic MHD dynamo with the ABC flow** in a periodic box, with
  the magnetic Reynolds number `Rm` as the control parameter. The ABC flow is an exact Beltrami eigenfunction
  (curl u = u), the induction operator is spectrally exact, and the fields are divergence-free by spectral
  projection. The generator is validated (exact diffusive decay, Beltrami identity, resolution convergence of the
  measured dynamo threshold `Rm_c`) before any learning, so the dataset is trustworthy.
- **Transition/reversal benchmark:** a 1D **mean-field α² dynamo** with a stochastic α (OU process), the classical
  low-order model of polarity reversals. Cheap (CPU), and it gives a genuine "abrupt reversal / topology" target.
- **Simple PDE benchmark:** a 2D **periodic Poisson** problem (parametrised source → potential), where the
  governing-equation residual *and* the solvability/boundary-condition constraint (zero-mean source) are exactly
  computable. Used to compare constraint-by-loss vs constraint-by-design vs constraint-by-sampling on ground truth.
- **Generative framework:** **conditional flow matching** (rectified-flow / stochastic-interpolant form, which is the
  diffusion-family model the subject asks for) on a small fully-convolutional field network with FiLM conditioning on
  the control parameter. Five physics-constraint strategies compared (see below) plus two prior strategies.

**Comparative study (the deliverable's core).** Same architecture, same data, same optimiser; only the constraint
mechanism changes:
- S1 `free` — unconstrained field-space CFM (baseline).
- S2 `loss` — soft physics loss: divergence penalty on the CFM x₁-prediction (Bastek et al.-style).
- S3 `design` — constraint by design: the network outputs a vector potential A, B = curl A (exactly solenoidal).
- S4 `sample` — constraint at sampling: Helmholtz projection inside the ODE loop (and post-hoc projection).
- S5 `guide` — divergence-gradient guidance at sampling (universal-guidance style).
- P1 `white prior` vs P2 `function-space prior` (smooth, power-law spectral prior — Fundiff-flavoured) crossed with
  the best constraint strategy, because the prior is what controls the high-wavenumber content of generated fields.

**Metrics** (all measured, all in code): relative divergence; magnetic energy spectrum + inertial-range slope;
dissipation D = η⟨|j|²⟩ and production P = ⟨u·(j×B)⟩ and the **energy-balance closure** γ_inst = (P−D)/2E compared
with the measured growth rate γ(Rm); magnetic helicity and normalised helicity σ(k) (topology/linkage); polarity sign
statistics; two-sample discriminative score (AUC) and KS distance on shell energies (distributional quality);
ensemble spread; and *parameter-conditioning fidelity* (does the generated physics track Rm, including at held-out
Rm values the model never saw).

**Cost/time split.** All heavy compute on one rented GPU pod (Runpod RTX 4090, per-second billing, deleted as soon as
the campaign ends). No paid sub-agents for the science: the harness writes and runs everything, so LLM cost stays far
below its cap. One light review sub-agent at the end if the budget and clock allow.

## Log

- **00:32** Read MISSION.md, TOOLS.md, `subject/stage_milady_2027.pdf` in full. No commits in the repo yet: fresh start.
- **00:33** Local machine: 4 CPUs, 15 GB RAM, torch 2.14 **CPU-only**. A 3D spectral campaign does not fit the clock
  on 4 cores → rent a GPU.
- **00:35** Chose **Runpod RTX 4090** (`rp_create_pod`, max_hours=2, image `pytorch/pytorch:2.4.0-cuda12.1-cudnn9-runtime`)
  over Scaleway L4 (€0.79/h): Runpod bills per second and `rp_exec` gives command execution without SSH setup, which
  saves several minutes of wall clock — the binding constraint. Cost ≈ 0.89 USD/h, inside the 5 USD Runpod cap;
  Scaleway would also fit its uncapped budget but needs SSH/image setup. Pod `xqeduphrdeuobe` RUNNING at US-NC-1.
- **00:36** Decided to write the whole campaign locally, upload once as base64 through `rp_exec`, and run a single
  driver in the background that saves `results/*.json` incrementally (partial results survive a crash).
- **00:37** Kinematic (prescribed ABC flow) rather than saturated turbulent MHD: it is reproducible at 32³ within
  minutes, keeps ∇·B at machine precision, and has a measurable, literature-checkable threshold. Stated as a limit:
  no back-reaction, so no true saturated energy balance; the energy-balance metric is the *instantaneous* budget
  closure of the induction equation, which is exactly defined in the kinematic regime.

## Incident and re-planning

- **00:35–00:55** Runpod pod `xqeduphrdeuobe` (RTX 4090) reached state RUNNING but `rp_exec` kept answering
  "Pod is not running"; `rp_logs` showed `start container for pytorch/pytorch:2.4.0-…: begin` repeating every
  16 s: the container was crash-looping on start (image ~9 GB). ~20 min of the 90-minute window lost with zero
  compute. **Decision 00:56: delete the pod and run the whole campaign on the local 4 CPU cores** (torch
  2.14.1+cpu present), rescaling the campaign instead of re-trying another image — a second provisioning gamble
  could not be recovered from. Cost of the pod: ~21 min of one 4090 (≈0.31 USD), recorded in `COSTS.md`.
- **01:00** Rescale: dataset and learning study at **n=16** (instead of 32), 6 `Rm` × 2 `h` groups × 6 ICs ×
  4 energy levels ≈ 240 fields; resolution study at n ∈ {12,16,24}. Rationale: at 16³ the fastest-growing dynamo
  mode (k ≈ 2-4) is still resolved by k_max = 8, and the *shape* metrics we care about (spectrum, helicity, budget
  closure) remain meaningful; the loss is the inertial-range extent, which is now quantified by our own
  convergence table instead of being assumed away. Recorded as a limit in REPORT §4 and `COMPLIANCE.md` S6d.
- **01:04** First campaign pass exposed the real bugs (component-vs-space averaging in the metric reductions,
  a missing 1j in the spectral curl, shell index defined as |k|² instead of |k|, and a vector-potential sign) —
  all caught *because* the validation suite checks exact identities (Beltrami, Parseval, P−D = dE/dt, σ=1 for a
  Beltrami field). This paid for itself immediately: the same suite is reported as Table 1 of the paper.
- **01:09** Growth-rate estimator changed to use the recorded geometric crossings
  (`γ = ln2 · Δlevel/Δt` over the last crossings) because a log-linear fit of the energy history has too few
  samples when the field decays in <1 time unit. Known bias, stated in the report: in the *subcritical* regime the
  last crossings still contain transient multi-mode decay, so |γ| is overestimated there; the threshold is
  therefore reported as bracketed (Rm=16 decaying, Rm=24 growing) and, independently, as the zero crossing of the
  *algebraic* closure `γ_inst = (P−D)/2E` measured on the snapshots (no fit involved).
- **01:11** `pkill -f "exp_gen.py --which 2"` killed my own shell (pattern matched the shell command line), not the
  job. Note for the rest of the mission: bracket the pattern.
- **01:14** Discovered this host is shared: another mission's `code/train.py` jobs (race-zhipu / anthropic runs)
  occupy the same 4 cores. Per the mission rules we do not touch resources we did not create; instead we accept the
  contention, keep jobs few and short, and prefer backgrounding + polling over interactive waits.
- **01:26 RE-SCOPE (second, and it is the binding one).** The dataset build stalled on the *near-threshold*
  groups: at `h = 1` we measured γ(10) = −3.47, γ(14) = −2.31, γ(18) = −1.51, γ(24) = −0.29 (energy-level
  crossings) — `Rm ≈ 24` is marginal, so that run needs the whole `T = 200` integration (5000 steps, 310 s on
  the contended CPU) and the 12-group design could not finish before the deadline *and* leave time for the
  study. Decision: kill the running build, rebuild with `Rm ∈ {10,16,45,24} × h ∈ {1.0,0.55}`, `T = 60`,
  3 energy levels (8 groups, ~7 min), and **hold out `Rm = 24`** (both `h`) as the unseen control parameter —
  it sits between the training values 16 and 45, so the conditioning test stays an interpolation test. The
  study then indexes samples by their per-sample metadata instead of by group arithmetic (a ragged group would
  otherwise silently corrupt the train/test split). Killing the 2D analytic benchmark at that moment was a
  deliberate trade: the 3D comparative study is the deliverable the subject asks for, the 2D benchmark is one
  of its supporting rows and can be re-run afterwards (`reproduce.sh` keeps it).
- **01:36 Third re-scope (the integration cap).** With the whole machine to itself the build still spent >150 s on
  the `Rm = 45` group: at n=16 the batched small-FFT path costs ~50 ms per RK4 right-hand side under the external
  contention, so any group that has to integrate to the cap is minutes, not seconds. Decision: cap the integration
  at `t = 12` (300 steps) and accept that the near-threshold group may deliver fewer than 3 energy levels — the
  study indexes samples by per-sample metadata, so ragged groups are handled, and the *algebraic* closure
  `γ_inst = (P−D)/2E` needs no fit and stays defined for every snapshot. The reversal benchmark (`exp4`) and the
  growth-rate/resolution sweeps (`exp_data` EXP1/EXP1b) are dropped from this delivery to protect the 3D
  comparative study; their code stays in the repository and in `reproduce.sh`. The invalid `exp4_reversals.json`
  produced by the un-quenched (overflowing) version of the 1D model was deleted rather than reported.
- **01:37 Delivery plan.** `exp3_study.json` is now written after *every* strategy, so a delivery at any later
  moment contains a complete, self-consistent subset of the comparison; the report will state how many strategies
  were measured and will not extrapolate over the missing ones. Remaining budget: LLM 0.34/5 USD (not binding),
  ~24 min of clock (binding).



- **01:53 Delivery state.** The full-capacity study (base 16, 3 blocks, 500 steps, 9 strategies) was killed at ~01:50 when its measured throughput showed it needed ~45 min; `code/exp3_fast.py` (same library, base 6 / 2 blocks / 120 steps / 6 strategies) completed in 22 s and is the source of Table 5. That run also exposed the Nyquist-projector bug described in REPORT §3.7 (and the non-scalar loss in the constrained-loss arm, fixed in `milady/flow.py`), i.e. the reduced run produced two real corrections, not just smaller numbers. Dataset published to the Hub (private, user `knoel`): dataset `milady-abc-dynamo-fields` + mission collection. Delivering at 01:56, ~5 min before the deadline.
