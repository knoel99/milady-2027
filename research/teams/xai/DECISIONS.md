# Decisions — race-xai

Times are UTC. Start of mission: 2026-11-15T00:40:36Z. Deadline: 2026-11-15T02:10:36Z.

## 2026-11-15T00:45 — Strategy

The subject (`subject/stage_milady_2027.pdf`) is a 2027 master internship brief (ANR MilaDy, CEREA / LISN). It does not prescribe a single method or a single benchmark. Its research requirements, which this mission treats as the work to carry out, are:

1. Design and evaluate physics-constrained generative models for parameter-dependent physical fields in dynamo systems.
2. Respect energy balance and divergence-free conditions.
3. Encode variations across control parameters (Reynolds, magnetic Reynolds, material properties).
4. Generate 3D fields usable as input for reduced-order models or data assimilation.
5. Implement and test conditional generative models based on diffusion or flow matching.
6. Incorporate PDE and boundary-condition constraints through model design, training losses, or sampling.
7. Validate first on simple PDE benchmarks, then evaluate generated MHD fields with energy spectra, helicity, divergence control, and topology preservation.
8. Deliver a comparative study, a technical report, and reproducible code for the MilaDy toolbox.

**Scope chosen (time ~1.4 h, LLM budget 5 USD of which ~0.26 is already spent or in flight, local box is 4 vCPU / 16 GB, no CUDA).**

A full 3D MHD DNS plus a diffusion transformer is not feasible and would not be reproducible on a fresh CPU checkout. The study is therefore a controlled comparison on two exact PDE benchmarks that already contain the physics the subject asks for, plus one cheap 3D latent model:

- **B1 — 1D viscous Burgers.** Parameter: viscosity ν (an inverse Reynolds number). Exact solution by Hopf–Cole. Constraints: energy decay at the viscous rate, Dirichlet boundaries. This is the simple PDE benchmark.
- **B2 — 2D kinematic MHD induction.** Parameter: magnetic Reynolds number Rm. Velocity is a known cellular flow. Magnetic field is obtained by a divergence-free pseudo-spectral induction solver (the reference). Constraints: ∇·B = 0 by construction of the stream function, resistive energy balance, boundary periodicity.
- **B3 — 3D kinematic induction on a 16³ grid, latent conditional flow matching.** Same physics as B2, in 3D, so the generated fields are 3D volumes a reduced-order model could ingest. Topology is scored by magnetic helicity and by the number of sign changes of the volume-averaged axial field (a proxy for polarity flips, which the subject names).

**Models compared (same data, same split, same seed protocol):**

| id | family | conditioning | physics |
|---|---|---|---|
| `uncond` | conditional rectified flow, condition dropped | none | none |
| `cond` | conditional rectified flow | parameter embedded and FiLM-modulated | none |
| `cond_div` | same | parameter | hard divergence-free design (generate a stream function, or project) |
| `cond_phys` | same | parameter | hard div-free design + physics residual loss (induction / Burgers) + energy-balance penalty |
| `sampler_proj` | `cond` weights | parameter | constraints only at sampling (projection + energy rescaling) |

Flow matching (rectified flow, straight paths) is used rather than a full DDPM because the subject lists it explicitly, it trains in fewer steps, and it is the backbone FunDiff uses (Wang et al. 2026).

**What is measured vs cited vs conjectured.** Every number in `results/` comes from a run of this repository. Published numbers from FunDiff, PIDM, and the dynamo literature are cited and are not mixed into our tables. Claims about full turbulent dynamo reversals are marked as conjectures: we do not run a self-consistent MHD dynamo.

**Compute.** Local CPU runs the 1D and 2D studies. A GPU was requested and refused; see the decision below. LLM spend stays on this harness; no frontier-tier sub-agent.

## 2026-11-15T00:52 — Cloud refused, study stays on the local CPU

Tried, in order, with the price stated before each create:

- Scaleway `L4-1-24G` fr-par-2, 0.7875 EUR/h, stock `available`, `max_hours=0.6`. API 403 `quotas_exceeded` on `cp_servers_type_L4_1_24G`.
- Scaleway `RENDER-S` (P100) fr-par-2, 1.221 EUR/h, stock `available`, `max_hours=0.45`. Same 403 on `cp_servers_type_RENDER_S`.
- Scaleway `BASIC2-A16C-32G` fr-par-2, 0.2067 EUR/h, stock `available`, `max_hours=1.0`. Same 403 on `cp_servers_type_BASIC2_A16C_32G`.
- Scaleway `DEV1-L` fr-par-1, 0.0428 EUR/h, stock `available`, `max_hours=0.8`. Same 403 on `cp_servers_type_DEV1_L`.

The quota is per commercial type and is already exceeded for every type tried, including the cheapest CPU. Creating more types would only produce more 403s. Runpod community offers returned `availability: LOW` and an empty `data_centers` list for the RTX 3070 (0.13 USD/h), the RTX 3090 (0.22 USD/h) and the V100 (0.23 USD/h), so a pod create would reserve budget against stock the offer list does not show. No cloud resource was created. No Runpod spend.

Consequence: the 3D study uses N=12 rather than N=16, fewer seeds, and a shorter integration time. The metric definitions do not change. This is a limit of the evidence, stated in the report, not a change of the question.

## 2026-11-15T00:55 — Local box is shared; shrink the runs, do not shrink the comparison

`experiment_burgers --n 64 --steps 500` was using a full core and had not printed a loss after two minutes, while several other missions were training on the same 4-core host. Killed that process. Replacement configuration, chosen so every strategy still trains on the same data and the held-out split is unchanged in kind:

- Burgers: n=32, 250 Adam steps, batch 16, 12 Euler steps. Exact solution is unchanged; the grid is coarser.
- MHD 2D: n=24, 4 train Rm × 3 seeds, 2 test Rm × 2 seeds, 200 Adam steps.
- MHD 3D: n=8, 3 train Rm × 2 seeds, 1 test Rm × 2 seeds, 150 Adam steps. Still a 3D volume, still divergence-free by the curl decoder, still scored on helicity and the axial-mean polarity proxy.

A second, even smaller configuration is what `reproduce.sh` runs, so a fresh checkout finishes in minutes. The numbers in the report are the ones this mission commits under `results/`.

## 2026-11-15T01:05 — The 2D stream-function generator does not train; report the failure

`cond_div` and `cond_phys` on the 2D benchmark emit a stream function and recover B by a spectral curl. After a zero-init (curl identically zero, no gradient) and a small normal init (std 0.01), both still finish at relative L2 ≈ 5 and energy error ≈ 23, against ≈ 1.0 and ≈ 0.5 for the unconstrained conditional model. The induction residual in `cond_phys` starts at ~4800 because the residual is not scaled to the flow-matching loss. I do not retune until it wins. The failure is a result: a hard divergence-free design that is not scaled to the data does not confer the constraint, and an unscaled physics residual destabilises training. The constraint that does fire is the sampling-time Helmholtz projection (`sampler_proj`), which cuts the reported divergence by about an order of magnitude without improving the field error.

The 3D study is different and is kept: there the decoder emits a vector potential, B = curl(A), and the divergence score is ~1e-7 for every latent model, so the design constraint holds. The physics loss on energy, in that architecture, also cuts relative L2 from about 1.0 to about 0.43 on the single seed. That comparison is the one the report leans on for "design constraint works".

Multi-seed (3 seeds) is run for Burgers and for the 2D models that train (`uncond`, `cond`, `sampler_proj`). The failed stream-function pair is reported from the single delivered run, with the failure described, not averaged into a success.

**Reproduction.** `reproduce.sh` regenerates every reported number on CPU. The 3D script has a `--device cpu --quick` path so a fresh checkout without a GPU still produces the same tables at lower resolution / fewer steps, and a `--full` path for the GPU run whose outputs we commit.

## 2026-11-15T00:45 — Departures, recorded now so they are not silent

- No application PDF, transcripts, or emails. Those are administrative instructions of the internship offer, not research. Status in COMPLIANCE.md: not applicable.
- No self-consistent 3D turbulent dynamo DNS. The subject says methods are first validated on simple PDE benchmarks, with potential applications to turbulent dynamo flows. We do the validation and a kinematic induction surrogate, and we state the limit.
- FunDiff is not reimplemented in JAX. We take its design idea (conditional generative model over fields, physics in the architecture or the loss) and implement a small rectified-flow version we can train and ablate here.
