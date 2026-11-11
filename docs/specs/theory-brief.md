# Common theory brief (report §formulation, thesis §theory)

This brief fixes the statements and proofs that the report and the thesis proposal must take up consistently. Notation: `docs/specs/notation.md`.

## 0. Setting

- Control parameters $\boldsymbol\lambda \in \Lambda \subset \mathbb{R}^p$ (e.g. $Re$, $Rm$, $\mu_r$, $\Gamma$).
- Discretized dynamics $\mathrm{d}\mathbf{x} = F_{\boldsymbol\lambda}(\mathbf{x})\,\mathrm{d}t + \Sigma\,\mathrm{d}W_t$ ($\Sigma = 0$: deterministic). Generator $\mathcal{L}_{\boldsymbol\lambda}\varphi = F_{\boldsymbol\lambda}\cdot\nabla\varphi + \tfrac12 \Sigma\Sigma^\top : \nabla^2\varphi$.
- Data: snapshots of a statistically stationary state, with law $\mu_{\boldsymbol\lambda}$ (invariant measure, time average).
- Model: $q_\theta(\cdot\mid\boldsymbol\lambda) = (\Phi^{\boldsymbol\lambda}_1)_\# \mathcal{N}(0, I)$ where $\Phi^{\boldsymbol\lambda}_t$ is the flow of $\dot{\mathbf{z}} = v_\theta(\mathbf{z}, t, \boldsymbol\lambda)$. Flow matching loss on the linear path $\mathbf{x}_t = (1-t)\mathbf{x}_0 + t\mathbf{x}_1$, target $\mathbf{x}_1 - \mathbf{x}_0$; the minimizer is $v^\star(\mathbf{x}, t) = \mathbb{E}[\mathbf{x}_1 - \mathbf{x}_0 \mid \mathbf{x}_t = \mathbf{x}]$.

## 1. Taxonomy of constraints (Definition)

| Class | Form | MHD examples | True for | Suitable mechanism |
|---|---|---|---|---|
| C1 local linear | $\mathbf{x} \in S$, $S = \ker A$ closed subspace | $\nabla\cdot\mathbf{u} = 0$, $\nabla\cdot\mathbf{B} = 0$, homogeneous linear boundary conditions | each sample | architecture (potentials) or projection |
| C2 local nonlinear | $c(\mathbf{x}) = 0$ | stationary state of a PDE (Darcy in PIDM), algebraic constraint | each sample (if no time derivative is involved) | nonlinear projection (PCFM, ECI) or penalty/guidance |
| C3 symmetry | $g_\#\mu_{\boldsymbol\lambda} = \mu_{\boldsymbol\lambda}$, $g \in G$ | $\mathbf{B} \to -\mathbf{B}$; rotation $R_\pi$ of VKS; $(Q,D,V)\to(-Q,-D,V)$ | the law | equivariance of the velocity field |
| C4 statistical (stationarity) | $\mathbb{E}_{\mu_{\boldsymbol\lambda}}[\mathcal{L}_{\boldsymbol\lambda}\varphi] = 0$, $\varphi \in \Phi$ | mean energy balance $\langle\varepsilon\rangle = \langle P\rangle$, cross-helicity and $\langle a^2\rangle$ balances | the law only | law-level loss at training time; exponential tilting at sampling time |

Key remark: for a snapshot of a **non-stationary** PDE, the residual $\partial_t\mathbf{x} - F(\mathbf{x})$ cannot be computed (the time derivative is not in the snapshot). Only constraints without a time derivative (divergence, boundary conditions, diagnostic elliptic equations) are per-sample constraints. The energy balance $\mathrm{d}E/\mathrm{d}t = P - \varepsilon$ is an **identity** (the right-hand side is computable), not a constraint; the constraint is $\mathbb{E}[P - \varepsilon] = 0$.

## 2. Statements

**Proposition 1 (C1 by construction).** If the decoder is written $\mathbf{x} = \mathcal{C}(\mathbf{z})$ with $\mathrm{Im}\,\mathcal{C} \subset S$ (e.g. $\mathbf{u} = \nabla^\perp\psi$, $\mathbf{B} = \nabla\times\mathbf{A}$), then $q(S) = 1$ whatever the law of $\mathbf{z}$. In a bounded domain, $\mathcal{C}$ must in addition respect the boundary conditions (e.g. $\psi$ constant on an impermeable wall; gauge and matching to the exterior field for $\mathbf{A}$).

**Proposition 2 (decomposition of the optimal flow on a subspace).** If $\mu(S) = 1$ with $S$ a linear subspace, $P$ the orthogonal projector onto $S$ and $\mathbf{x}_0 \sim \mathcal{N}(0, I)$, then for $t < 1$
$$ v^\star(\mathbf{x}, t) = \underbrace{\mathbb{E}[\mathbf{x}_1 - P\mathbf{x}_0 \mid P\mathbf{x}_t = P\mathbf{x}]}_{\in S,\ \text{depends only on } P\mathbf{x}} \; - \; \frac{(I-P)\mathbf{x}}{1-t}. $$
*Proof.* $P\mathbf{x}_0$ and $(I-P)\mathbf{x}_0$ are independent Gaussians (isotropy). $\mathbf{x}_1 \in S$ so $(I-P)\mathbf{x}_t = (1-t)(I-P)\mathbf{x}_0$, independent of $(P\mathbf{x}_t, \mathbf{x}_1, P\mathbf{x}_0)$. We condition each component. ∎
*Consequences.* (a) With exact $v^\star$, free sampling lands exactly in $S$: $(I-P)\mathbf{x}(t) = (1-t)(I-P)\mathbf{x}(0)$. (b) In the limit of perfect learning, free sampling, final projection, projected flow and potentials give **the same law**: the observed differences come from approximation error and inductive bias, not from the target. (c) With a **bounded** error $e = v_\theta - v^\star$, the final orthogonal component equals $\lim_{t\to1}(1-t)\Big[(I-P)\mathbf{x}(0) + \int_0^t \frac{(I-P)e(s)}{1-s}\mathrm{d}s\Big] = 0$, since $(1-t)\ln(1-t) \to 0$: in continuous time, the stiff term $-(I-P)\mathbf{x}/(1-t)$ erases any bounded error. The residual divergence of a free model (E2, V0) therefore comes from elsewhere: a regular network does not represent the singular $1/(1-t)$ term, so its error is not bounded near $t = 1$, and an explicit fixed-step scheme integrates this stiffness poorly. *(Correction of 7 November 2026: an earlier version of this brief wrongly stated that the limit was $(I-P)e(1)$; pointed out by the report review.)* (d) The term $-(I-P)\mathbf{x}/(1-t)$ is stiff as $t \to 1$: an explicit fixed-step scheme resolves it poorly.

**Proposition 3 (unbiased penalty for a linear constraint; Jensen gap otherwise).** The end-of-path prediction $\hat{\mathbf{x}}_1 = \mathbf{x}_t + (1-t)v(\mathbf{x}_t, t)$ equals $\mathbb{E}[\mathbf{x}_1 \mid \mathbf{x}_t]$ at $v = v^\star$. For $A$ linear with $A\mathbf{x}_1 = 0$ a.s., the penalty $\|A\hat{\mathbf{x}}_1\|^2$ vanishes at $v^\star$: it does not move the optimum. For nonlinear $c$, $c(\mathbb{E}[\mathbf{x}_1\mid\mathbf{x}_t]) \neq \mathbb{E}[c(\mathbf{x}_1)\mid\mathbf{x}_t] = 0$ in general: the penalty biases the optimum (Jensen gap discussed by Bastek, Sun, Kochmann 2025).
*Proof.* $\mathbf{x}_t + (1-t)(\mathbf{x}_1 - \mathbf{x}_0) = \mathbf{x}_1$, then linearity of conditional expectation. ∎

**Proposition 4 (exact symmetry).** Let $G$ be a finite group acting by linear isometries. If $v(g\mathbf{x}, t, \boldsymbol\lambda) = g\,v(\mathbf{x}, t, \boldsymbol\lambda)$ for all $g$ and the base law is $G$-invariant, then $q(\cdot\mid\boldsymbol\lambda)$ is $G$-invariant. The symmetrization $v_{\mathrm{sym}} = \frac{1}{|G|}\sum_g g^{-1}v(g\,\cdot)$ is equivariant, and if $\mu$ is $G$-invariant, the (population) flow matching loss satisfies $\mathcal{J}(v_{\mathrm{sym}}) \le \mathcal{J}(v)$.
*Proof.* Uniqueness of ODE solutions: $g\Phi_t(\mathbf{z})$ and $\Phi_t(g\mathbf{z})$ solve the same ODE with the same initial datum. Image measure: $g_\#q = g_\#(\Phi_1)_\#\gamma = (\Phi_1)_\# g_\#\gamma = q$. For the loss: $\mathcal{J}$ is convex in $v$ and invariant under $v \mapsto g^{-1}v(g\,\cdot)$ when $\mu$ and $\gamma$ are invariant; Jensen. ∎
*Consequence (E1).* The stationarity identities (C4) do not fix the relative weights of two symmetric ergodic components: the set of invariant measures is convex, and the ergodic measures are its extreme points. Below the reversal threshold, any combination $p\,\mu_+ + (1-p)\,\mu_-$ is invariant. The symmetry must be imposed separately (Proposition 4).

**Proposition 5 (stationarity identities).** If $\mu$ is invariant, then $\mathbb{E}_\mu[\mathcal{L}\varphi] = 0$ for every smooth $\varphi$ with controlled growth (weak form of the stationary Liouville / Fokker–Planck equation $\nabla\cdot(\mu F) = \tfrac12\nabla^2 : (\Sigma\Sigma^\top\mu)$). The mean energy balance is the case $\varphi = E$.
*Proof (deterministic).* For $\mathbf{x}_0 \sim \mu$, $\varphi(\mathbf{x}_t) - \varphi(\mathbf{x}_0) = \int_0^t \mathcal{L}\varphi(\mathbf{x}_s)\mathrm{d}s$; expectation, invariance ($\mathbf{x}_s \sim \mu$), Fubini. With noise: Itô formula, the stochastic integral has zero expectation. ∎

**Corollary 6 (inconsistent per-sample constraint).** If $\mathcal{L}\varphi(\mathbf{x})$ has a law with a density under $\mu$ (generic case: $\mathrm{Var}_\mu(\mathcal{L}\varphi) > 0$), the set $\{\mathcal{L}\varphi = 0\}$ is $\mu$-null; any law concentrated on it is singular with respect to $\mu$ ($\mathrm{KL} = \infty$), and the error of the per-sample projection does not vanish even with a perfect generator. Measured: E1 (variance of $\mathrm{d}E/\mathrm{d}t$ brought down to 0, degraded energy distance) and E2 (re-calibration of the small scales).

**Proposition 7 (I-projection).** Among the laws $\nu \ll q$ such that $\mathbb{E}_\nu[g] = c$, the one closest to $q$ in the sense of $\mathrm{KL}(\nu\,\|\,q)$ is $\nu^\star = e^{\boldsymbol\beta\cdot g}q/Z(\boldsymbol\beta)$, with $\boldsymbol\beta$ minimizing the convex dual $\log Z(\boldsymbol\beta) - \boldsymbol\beta\cdot c$ (Csiszár 1975). On a sample: self-normalized weights, ESS $= 1/\sum w_i^2$. Limit: reweighting does not create mass; if $q$ misses a region that $\mu$ charges (e.g. the "bridge" $|D| \approx 0$ near the reversal threshold), the ESS collapses. Hence the **stationarity loss at training time**, $\beta\sum_k(\mathbb{E}_{q_\theta(\cdot\mid\boldsymbol\lambda)}[\mathcal{L}_{\boldsymbol\lambda}\varphi_k]/s_k)^2$ evaluated by differentiable sampling, which also applies at $\boldsymbol\lambda$ **without data**.

**Proposition 8 (Rice formula: reversal frequency from the law).** Let $D(t) = \ell(\mathbf{x}(t))$ be a linear observable (dipole moment) of a stationary process with $C^1$ trajectories whose joint law of $(D, \dot D)$ has a continuous density. The mean number of crossings of $D$ through 0 per unit time is
$$ \nu_0 = \mathbb{E}_\mu\big[\,|\ell(F(\mathbf{x}))|\;\delta(\ell(\mathbf{x}))\,\big] = \lim_{h\to0}\frac{1}{2h}\mathbb{E}_\mu\big[|\ell(F(\mathbf{x}))|\,\mathbf{1}_{|\ell(\mathbf{x})|<h}\big]. $$
(Rice 1944; Kac–Rice formula.) It depends only on the stationary law and on $F$: a snapshot generator predicts the reversal frequency **without integrating in time**. In MHD, $\dot D = \ell(\nabla\times(\mathbf{u}\times\mathbf{B}) + \eta\Delta\mathbf{B})$ is computable on a generated snapshot $(\mathbf{u}, \mathbf{B})$. Limits: $F$ is needed; fast crossings (excursions, "chatter" around 0) are counted; the law of waiting times is not given (the dynamics is needed). Windowed estimator with window $h$: bias $O(h^2)$, variance $O(1/(Nh))$.

**Proposition 9 (error bound near a jump in the law).** If $\mathbf{z}\mapsto v_\theta$ is $L_x$-Lipschitz and $\boldsymbol\lambda\mapsto v_\theta$ is $L_\lambda$-Lipschitz, then (Grönwall) $W_1(q_{\boldsymbol\lambda}, q_{\boldsymbol\lambda'}) \le L_\lambda\frac{e^{L_x}-1}{L_x}|\boldsymbol\lambda - \boldsymbol\lambda'| =: K|\boldsymbol\lambda - \boldsymbol\lambda'|$. If the true family jumps at $\lambda_c$ ($W_1(\mu_{\lambda_c^-}, \mu_{\lambda_c^+}) = J > 0$, subcritical bifurcation, multistability), then for every $\delta > 0$, $\max_{|\lambda-\lambda_c|\le\delta} W_1(q_\lambda, \mu_\lambda) \ge (J - 2K\delta)/2$ (in the limit $\lambda \to \lambda_c^\pm$). A generator that is regular in $\boldsymbol\lambda$ makes an error of at least $J/2$ near the jump, unless it has a large constant $K$ (or conditioning on the state/hysteresis).
*Proof.* Triangle inequality between $\mu_{\lambda_1}, q_{\lambda_1}, q_{\lambda_2}, \mu_{\lambda_2}$ with $\lambda_{1,2} = \lambda_c \mp \delta$. ∎ For a supercritical bifurcation (dynamo with continuous threshold, amplitude $\propto\sqrt{Rm - Rm_c}$), the law varies continuously but as $\sqrt{\cdot}$: infinite slope at the threshold, the same difficulty in attenuated form.

## 3. Experimental plan of the internship (carried out in `experiments/`, CPU scale)

- **E1** (Gissinger 2012, 3 modes): Propositions 4, 5, 6, 7, 8 and 9 (reversal threshold, attractor-merging crisis: no reversal at $\Gamma = 0{,}86$, reversals from $0{,}8625$ in the repository's simulations; measured value, unpublished).
- **E2** (forced 2D MHD, truncated Fourier basis = POD): Propositions 1, 2, 3 (five divergence mechanisms), 5, 6, 7 (energy balance, cross-helicity and $\langle a^2\rangle$ at the law level).
- **E3** (ABC kinematic dynamo): validation of the 3D stage (threshold $Rm_c$, divergence at machine precision through the rotational form).

## 4. Prior work and positioning (to be respected in the report and the thesis)

Verified fact base: `docs/specs/sources/data-metrics.md` §3 and `docs/specs/sources/literature.md` (references taken up below).

**Already published — to cite, not to claim:**
- Invariance ⟺ $\mathbb{E}_\mu[\mathcal{L}\varphi] = 0$ on a core of test functions: Echeverría (1982), Ethier & Kurtz (1986), Barbour's generator approach (1988, 1990), Stein discrepancies (Gorham & Mackey 2015; Gorham, Duncan, Vollmer, Mackey 2019; Liu, Lee, Jordan 2016).
- Weak form of the stationary Fokker–Planck equation as the **loss of a sample generator**: Weak Generative Sampler, Cai, Cao, Huang, Zhou, *SIAM J. Sci. Comput.* 48(4):C708–C735 (2026), DOI 10.1137/24M1665271 (loss $\mathbb{E}_\varphi(\mathbb{E}_z[\mathcal{L}^*\varphi(G_\theta(z))])^2$, random Gaussian test functions, dimension ≤ 100); min-max precursor: WAN, Zang et al., *J. Comput. Phys.* 411:109409 (2020).
- Learning through the invariant measure: Yang et al. (SIADS 2023), Botvinick-Greenhouse, Martin, Yang (*Chaos* 2023), Jiang et al. (NeurIPS 2023), DySLIM (Schiff et al., ICML 2024), PINN-IMSM (*Physica D* 2026).
- I-projection / maximum entropy on a pretrained generator: Csiszár (1975), Jaynes (1957), Khalifa et al. (ICLR 2021), Pitera & Chodera (2012); tilting under moment constraints at inference in a diffusion model: Mun (arXiv:2608.30096, 2026); tilting a flow matching model by a weak-form PDE residual (per-sample reward): Tauberschmidt, Fellenz, Vollmer, Duncan (ICLR 2026, arXiv:2508.09156).
- Zero divergence in generative models: stream function (FunDiff 2026), Leray projection (Genuist et al., arXiv:2601.19368, 2026; PCDM, Li, Buzzicotti, Bonaccorso, Biferale, arXiv:2603.12834, 2026; "Project and Generate", arXiv:2603.24500, 2026), divergence-free networks (Richter-Powell et al. 2022).
- Equivariant flows and invariant laws (Proposition 4): classical result for equivariant normalizing flows; present it as standard.
- Propositions 2 and 3: elementary consequences of the definitions; present them as "elementary propositions, probably known in other forms".

**What this work claims (worded cautiously: "to our knowledge, after a literature search on 6 November 2026"):**
1. Using the stationarity identities of a **field PDE** (MHD: energy, cross-helicity and $\langle a^2\rangle$ balances) as **law-level** constraints of a **parametric conditional** generative model, enforceable at parameters **without data** (E1 fine-tuning, E2 law-level loss), and **identities with no target value** (unlike the external moments of Khalifa or Mun).
2. Stating and **measuring** the inconsistency of the per-sample constraint of a stationary balance (Corollary 6): E1 and E2.
3. **Rice formula applied to a snapshot generator** to predict the reversal frequency without time integration (Proposition 8): no prior work found.
4. Symmetry / stationarity complementarity: the identities do not fix the weights of the ergodic components; equivariance is necessary (E1).
5. Technical point: the naive estimator (mini-batch mean)² of a stationarity loss equals $(\mathbb{E}g)^2 + \mathrm{Var}(g)/n$ and penalizes the dispersion of the law; an unbiased estimator (product of the means of two half-batches) removes this bias (observed in E1, quick version).
6. Proposition 9 (lower bound on the error near a jump in the law) applied to the dynamo threshold.

**Points of caution:** the identities are necessary but not sufficient (every invariant measure satisfies them, including those carried by unstable orbits): keep the tie to the data; the selection of the physical measure by the zero-noise limit is guaranteed only in the Axiom A setting (Young 2002); the SRB measure is in general singular, hence the weak form.
