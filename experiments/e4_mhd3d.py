"""E4 - Conditional generation of 3D MHD fields (u, B): comparison of constraint mechanisms.

Data: ``e4_data.py`` (saturated dynamo forced by an ABC force at kf = 2, 16³, η swept). The latent
space holds every Fourier mode of the Galerkin system that produced the data, so the quadratic
budgets of a generated snapshot are exact. A flow matching network (``milady.train.fm3d.ResMLP``)
conditioned on log η generates the modes of (u, B).

Variants (same network, same budget; mechanisms of ``milady.train.constraints``):
  group A (free components)
    W0_free             : (û, B̂) components, no constraint;
    W1_penalty          : W0 + divergence penalty on the end-of-path prediction (training loss);
    W2_final_projection : W0, then Leray projection of the final samples (sampling);
    W3_projected_flow   : projected noise and projection of every integration stage (sampling);
  group B (vector potentials: zero divergence by design)
    W4_potentials       : Craya–Herring potentials of u and B;
    W4s_potentials_sym  : W4 with a velocity field equivariant under B → −B (design);
    W5_stationarity     : W4s fine-tuned with the law-level stationarity loss (energy and
                          magnetic-helicity identities, imposed at η drawn over the whole range);
    W5_control          : the same fine-tuning without the loss;
    W6_diffusion        : variance-preserving diffusion on the potentials (model family);
    W7_tilting          : exponential tilting of the W5_control samples on the same identities
                          (multipliers fitted on one half, the other half evaluated with weights);
    W8_rescaling        : per-sample rescaling of the W5_control samples to the energy balance.

Evaluation at the validation and held-out test η (n = 512) and at three training η (n = 256):
energy distance on the physical features against the reference, divided by the noise floor (two
reference subsamples from disjoint sets of trajectories), divergence, energy balance, spectra,
helicities, polarity asymmetry, magnetic null points, and the drift of the magnetic energy when
the solver is restarted from the generated snapshots (test η only).

Usage:
    python3 e4_mhd3d.py --reference [--quick]         # reference statistics, once (no model)
    python3 e4_mhd3d.py [--quick] --seed k [--group A|B|all] [--threads 1]
Output: results/e4_reference[_quick].json; results/e4_mhd3d[_quick]_s<k>_<group>.json, merged into
results/e4_mhd3d[_quick]_s<k>.json when both groups exist.
"""
from __future__ import annotations

import argparse
import copy
import json
import time
import numpy as np
import torch

import e4_data as D
from e4_digest import merge
from common import RESULTS, save_json, seed_all
from milady.eval import metrics as M
from milady.eval.topology import null_count
from milady.sim.mhd3d import MHD3D
from milady.train import constraints as C
from milady.train.data import FourierPotentialSpace
from milady.train.diffusion import diffusion_loss, diffusion_sample
from milady.train.flow import fm_loss, heun_sample
from milady.train.fm3d import ResMLP, SignSymmetrized

ETAS, ETA_TRAIN, ETA_VAL, ETA_TEST = D.ETAS, D.ETA_TRAIN, D.ETA_VAL, D.ETA_TEST
ETA_TRAIN_EVAL = [ETA_TRAIN[0], ETA_TRAIN[2], ETA_TRAIN[5]]
LOG_LO, LOG_HI = np.log(0.028), np.log(0.085)          # normalization range of the condition
AMP = D.NU * D.KF**2                                   # forcing amplitude (laminar rule)
N_GRID = D.N
NULL_GRID = 48
GROUPS = {"A": ["W0_free", "W1_penalty", "W2_final_projection", "W3_projected_flow"],
          "B": ["W4_potentials", "W4s_potentials_sym", "W5_stationarity", "W5_control", "W6_diffusion",
                "W7_tilting", "W8_rescaling"],
          "C": ["W4c_potentials_smooth"],      # H15: W4 with a smooth embedding of the condition
          "D": ["G0_gaussian_modes", "W9_skip_sym"],                    # H16, H17: second-order baseline, affine skip
          "E": ["W10_anchored", "W11_anchored_skip"],                   # H19, H20: anchored on the Gaussian field
          "L": ["W9L_skip_long", "W11L_anchored_skip_long"],            # H18: 8 times the iterations (not in "all")
          "S": ["S_w512", "S_w2048", "S_w5632", "S_w512_long", "S_w2048_long"]}   # H21: width scan (not in "all")

FULL = {"iters": 4000, "batch": 128, "width": 512, "depth": 4, "lr": 5e-4, "n_gen": 512, "n_gen_train": 256,
        "steps": 50, "ft_iters": 400, "ft_lr": 2e-4, "beta": 20.0, "stat_cond": 4, "stat_per": 16, "stat_steps": 6,
        "n_null": 200, "n_restart": 128, "tau": 4.0, "floor_splits": 10, "n_ref_null": 400, "long_factor": 8}
QUICK = {**FULL, "iters": 150, "width": 256, "depth": 2, "n_gen": 96, "n_gen_train": 64, "steps": 12, "long_factor": 2,
         "ft_iters": 20, "n_null": 24, "n_restart": 24, "tau": 1.0, "floor_splits": 4, "n_ref_null": 32}


def cn(eta) -> np.ndarray:
    """Normalized condition in [0, 1]."""
    return (np.log(eta) - LOG_LO) / (LOG_HI - LOG_LO)


def eta_of(c: torch.Tensor) -> torch.Tensor:
    return torch.exp(LOG_LO + (LOG_HI - LOG_LO) * c)


# ---------------------------------------------------------------------------------------------
# Spaces, forcing, reference
# ---------------------------------------------------------------------------------------------
class Context:
    """Data, latent spaces and reference statistics shared by all variants."""

    def __init__(self, quick: bool, need: tuple[str, ...] = ("pot", "pot_sym", "comp"), device: str = "cpu"):
        """``need``: latent spaces whose training set is built (memory: about 0.3 to 0.5 GB each);
        ``device``: where the networks, the training sets and the generation live (the evaluation is on CPU)."""
        self.quick = quick
        self.cfg = QUICK if quick else FULL
        self.dev = torch.device(device)
        self._floors: dict = {}
        self.pot = D.space()
        self.pot_sym = FourierPotentialSpace(D.kcut(), symmetric_b=True, truncation="cube")
        self.comp = C.FourierComponentSpace(D.kcut(), truncation="cube")
        sim = MHD3D(D.solver_config(ETAS[0], 1, 0, dtype="float64"))
        f = (sim.f_phys / sim.forcing_amp).permute(1, 2, 3, 0).numpy()
        self.forcing_hat = self.pot.vector_modes(f).to(torch.complex128)
        assert abs(sim.forcing_amp - AMP) < 1e-12
        self.data = {e: D.load(e, quick) for e in ETAS}
        xs = torch.cat([torch.as_tensor(self.data[e]["x"]) for e in ETA_TRAIN])
        self.c_train = torch.cat([torch.full((len(self.data[e]["x"]), 1), float(cn(e))) for e in ETA_TRAIN]).to(self.dev)
        self.pot.fit(xs)
        self.pot_sym.fit(xs)
        xc = self.comp.from_hat(self.pot.field_hat(xs))
        self.comp.fit(xc)
        self.x_pot = self.pot.normalize(xs).to(self.dev) if "pot" in need else None
        self.x_pot_sym = self.pot_sym.normalize(xs).to(self.dev) if "pot_sym" in need else None
        self.x_comp = self.comp.normalize(xc).to(self.dev) if "comp" in need else None
        self.n_train = len(xs)
        del xs, xc
        # reference physical statistics per η (all snapshots); the raw snapshots are then dropped
        self.ref = {e: self.physics(self.pot.field_hat(torch.as_tensor(self.data[e]["x"])), e) for e in ETAS}
        if need != ("pot", "pot_sym", "comp"):
            for d in self.data.values():
                d.pop("x")
        # copies of the spaces on the training device (the originals stay on CPU for the evaluation)
        self.pot_d, self.pot_sym_d, self.comp_d = (copy.deepcopy(s).to(self.dev) for s in (self.pot, self.pot_sym, self.comp))
        pool = np.concatenate([self.ref[e]["features"] for e in ETA_TRAIN])
        self.f_mean, self.f_std = pool.mean(0), pool.std(0) + 1e-9
        ref_file = RESULTS / f"e4_reference{'_quick' if quick else ''}.json"
        self.ref_json = json.loads(ref_file.read_text()) if ref_file.exists() else None

    # -- physics of a set of coefficients ------------------------------------------------------
    def physics(self, fh: torch.Tensor, eta: float, chunk: int = 400) -> dict:
        """Per-sample physical quantities of the field coefficients ``fh`` (n, 2, M, 3), by chunks."""
        parts = [self._physics(fh[i:i + chunk], eta) for i in range(0, len(fh), chunk)]
        out = {k: np.concatenate([p[k] for p in parts]) for k in parts[0] if k != "budget"}
        out["budget"] = {k: np.concatenate([p["budget"][k] for p in parts]) for k in parts[0]["budget"]}
        return out

    def _physics(self, fh: torch.Tensor, eta: float) -> dict:
        fh = fh.cpu().to(torch.complex128)
        grid = self.pot.to_grid(fh, (N_GRID,) * 3).numpy()
        u, b = grid[:, 0], grid[:, 1]
        feats, _ = M.features(u, b, n_shells=8)
        params = {"mode": "dynamic", "forcing": "abc", "kf": D.KF, "nu": D.NU, "eta": eta}
        bud = M.energy_budget(u, b, params)
        hel = M.helicities(u, b)
        k = self.pot.k
        bh = fh[:, 1]
        jh = 1j * C._cross(k.to(bh.dtype), bh)
        k2 = (k * k).sum(-1)
        shell = self.pot.shell
        ns = int(shell.max()) + 1
        jdens = 2.0 * (jh * bh.conj()).real.sum(-1)                  # current helicity per mode
        hdens = jdens / k2                                           # magnetic helicity per mode
        zeros = torch.zeros(fh.shape[0], ns, dtype=torch.float64)
        return {
            "features": feats, "budget": bud,
            "div_u": M.divergence_relative(u, per_sample=True), "div_b": M.divergence_relative(b, per_sample=True),
            "spec_u": M.energy_spectrum(u, n_shells=ns)[:, 1:], "spec_b": M.energy_spectrum(b, n_shells=ns)[:, 1:],
            "Hm": hel["magnetic_helicity"], "Hc": hel["cross_helicity"], "j2": hel["mean_square_current"],
            "b2": 2 * hel["magnetic_energy"],
            "J_shell": zeros.index_add(1, shell, jdens).numpy()[:, 1:],
            "H_shell": zeros.index_add(1, shell, hdens).numpy()[:, 1:],
        }

    def standardize(self, feats: np.ndarray) -> np.ndarray:
        return (feats - self.f_mean) / self.f_std

    def half_split(self, eta: float, k: int, n: int) -> tuple[np.ndarray, np.ndarray]:
        """Indices of two reference subsamples of size ``n`` drawn from disjoint halves of the trajectories."""
        traj = self.data[eta]["traj"]
        rng = np.random.default_rng(1000 + k)
        perm = rng.permutation(np.unique(traj))
        in_a = np.isin(traj, perm[: len(perm) // 2])
        ia, ib = np.flatnonzero(in_a), np.flatnonzero(~in_a)
        return (rng.choice(ia, size=min(n, len(ia)), replace=False), rng.choice(ib, size=min(n, len(ib)), replace=False))

    def floor(self, eta: float, n: int) -> float:
        """Noise floor of the energy distance at ``eta``: two reference subsamples of ``n`` snapshots."""
        if (eta, n) not in self._floors:
            self._floors[(eta, n)] = self._floor(eta, n)
        return self._floors[(eta, n)]

    def _floor(self, eta: float, n: int) -> float:
        f = self.standardize(self.ref[eta]["features"])
        vals = []
        for k in range(self.cfg["floor_splits"]):
            ia, ib = self.half_split(eta, k, n)
            vals.append(M.energy_distance(f[ia], f[ib], n=n))
        return float(np.mean(vals))

    # -- evaluation of a generated ensemble ------------------------------------------------------
    def evaluate(self, fh: torch.Tensor, eta: float, w: np.ndarray | None = None, nulls: bool = True) -> dict:
        """Metrics of the coefficients ``fh`` generated at ``eta`` (optionally weighted by ``w``)."""
        ph, ref = self.physics(fh, eta), self.ref[eta]
        n = len(fh)
        w = np.full(n, 1.0 / n) if w is None else w / w.sum()
        uniform = np.allclose(w, 1.0 / n)
        avg = lambda a: np.tensordot(w, a, axes=(0, 0))                       # noqa: E731
        f_gen, f_ref = self.standardize(ph["features"]), self.standardize(ref["features"])
        eds = []
        for k in range(self.cfg["floor_splits"]):
            ia, _ = self.half_split(eta, k, n)
            eds.append(M.energy_distance(f_gen, f_ref[ia], n=n) if uniform
                       else M.weighted_energy_distance(f_gen, w, f_ref[ia], n=n))
        ed, floor = float(np.mean(eds)), self.floor(eta, n)
        bud, rbud = ph["budget"], ref["budget"]
        sinks = avg(bud["kinetic_dissipation"]) + avg(bud["magnetic_dissipation"])
        inj, prod = avg(bud["injection"]), avg(bud["magnetic_production"])
        spec_b, rspec_b = avg(ph["spec_b"]), ref["spec_b"].mean(0)
        spec_u, rspec_u = avg(ph["spec_u"]), ref["spec_u"].mean(0)
        hm, rhm = avg(ph["Hm"]), ref["Hm"].mean()
        J = avg(ph["J_shell"])
        diss = bud["kinetic_dissipation"] + bud["magnetic_dissipation"]
        rdiss = rbud["kinetic_dissipation"] + rbud["magnetic_dissipation"]
        row = {
            "eta": eta, "n": n, "ess_frac": float(1.0 / np.sum(w**2) / n),
            "ed": ed, "ed_floor": floor, "ed_ratio": ed / floor,
            "div_rel_b_max": float(ph["div_b"].max()), "div_rel_b_mean": float(ph["div_b"].mean()),
            "div_rel_u_mean": float(ph["div_u"].mean()),
            "balance_residual_total": float((inj - sinks) / sinks),
            "balance_residual_magnetic": float((prod - avg(bud["magnetic_dissipation"]))
                                               / (abs(prod) + avg(bud["magnetic_dissipation"]))),
            "r_a": float(abs(inj - sinks) / (inj + sinks)),
            "r_b": float(abs(J.sum()) / np.abs(J).sum()),
            "spec_err_b_l2": float(np.linalg.norm(spec_b - rspec_b) / np.linalg.norm(rspec_b)),
            "spec_err_u_l2": float(np.linalg.norm(spec_u - rspec_u) / np.linalg.norm(rspec_u)),
            "hel_m": float(hm), "hel_m_err_rel": float(abs(hm - rhm) / abs(rhm)),
            "err_Eu_rel": float(abs(avg(bud["kinetic_energy"]) / rbud["kinetic_energy"].mean() - 1)),
            "err_Eb_rel": float(abs(avg(bud["magnetic_energy"]) / rbud["magnetic_energy"].mean() - 1)),
            "hc_sign_asym": float(abs(avg((ph["Hc"] > 0).astype(float)) - 0.5)),
            "std_diss_rel": float(np.sqrt(avg((diss - avg(diss)) ** 2)) / rdiss.std()),
            "std_residual_rel": float(np.sqrt(avg((bud["residual_total"] - avg(bud["residual_total"])) ** 2))
                                      / rbud["residual_total"].std()),
            "k_lambda": float(np.sqrt(avg(ph["j2"]) / avg(ph["b2"]))),
        }
        if nulls and self.ref_json is not None:
            m = min(self.cfg["n_null"], n)
            b = self.pot.to_grid(fh[:m, 1:2].cpu().to(torch.complex128), (NULL_GRID,) * 3)[:, 0].numpy()
            wn = w[:m] / w[:m].sum()
            count = float(wn @ null_count(b, device=self.dev))
            ref_count = self.ref_json["values"][f"{eta:.5f}"]["null_count_mean"]
            row.update(null_count=count, null_count_err_rel=abs(count - ref_count) / ref_count)
        return row

    # -- restart: advance generated snapshots with the solver ------------------------------------
    def restart_drift(self, fh: torch.Tensor, eta: float) -> dict:
        """Relative change of the ensemble-mean energies after advancing ``fh`` by τ with the solver."""
        n = min(self.cfg["n_restart"], len(fh))
        fh = fh[:n].cpu().to(torch.complex128)
        grid = self.pot.to_grid(fh, (N_GRID,) * 3)                                 # (n, 2, nx, ny, nz, 3)
        sim = MHD3D(D.solver_config(eta, n, seed=0, device=str(self.dev)))
        to_hat = lambda f: sim._fft(f.permute(0, 4, 1, 2, 3).to(sim.device, sim.rdtype)) * sim.mask     # noqa: E731
        t0 = C.budget_terms_hat(self.pot, fh, D.NU, eta)
        sim.uh, sim.bh = to_hat(grid[:, 0]), to_hat(grid[:, 1])
        sim.advance_to(self.cfg["tau"], dt=D.DT, cfl=D.CFL)
        d = sim.diagnostics()
        eb0, eu0 = float(t0["magnetic_energy"].mean()), float(t0["kinetic_energy"].mean())
        return {"restart_drift_eb": abs(float(d["magnetic_energy"].mean()) - eb0) / eb0,
                "restart_drift_eu": abs(float(d["kinetic_energy"].mean()) - eu0) / eu0,
                "restart_eb_signed": (float(d["magnetic_energy"].mean()) - eb0) / eb0}


# ---------------------------------------------------------------------------------------------
# Reference-only analysis (no model): floors, null counts, restart floor, hypothesis H11
# ---------------------------------------------------------------------------------------------
def reference(quick: bool) -> None:
    t0 = time.time()
    ctx = Context(quick)
    cfg = ctx.cfg
    out: dict = {"config": {"quick": quick, "null_grid": NULL_GRID, "n_ref_null": cfg["n_ref_null"], "tau": cfg["tau"],
                            "n_restart": cfg["n_restart"], "features": M.features(np.zeros((1, 8, 8, 8, 3)),
                                                                                 np.zeros((1, 8, 8, 8, 3)))[1]},
                 "values": {}}
    rng = np.random.default_rng(0)
    for e in ETAS:
        ref, d = ctx.ref[e], ctx.data[e]
        traj = d["traj"]
        tr_ids = np.unique(traj)
        tmean = lambda a: np.stack([a[traj == i].mean(0) for i in tr_ids])       # noqa: E731, B023
        se = lambda a: a.std(0, ddof=1) / np.sqrt(len(a))                         # noqa: E731
        fh = ctx.pot.field_hat(torch.as_tensor(d["x"]))
        idx = rng.choice(len(traj), size=min(cfg["n_ref_null"], len(traj)), replace=False)
        b = ctx.pot.to_grid(fh[idx, 1:2].to(torch.complex128), (NULL_GRID,) * 3)[:, 0].numpy()
        counts = null_count(b)
        bud = ref["budget"]
        res_a = tmean(bud["residual_total"])
        sinks = (bud["kinetic_dissipation"] + bud["magnetic_dissipation"]).mean()
        jb = tmean(ref["J_shell"].sum(1))
        H = tmean(ref["H_shell"])
        Hsmall = H[:, 1:].sum(1)
        eb_shell = tmean(ref["spec_b"])
        frac1 = eb_shell[:, 0] / eb_shell.sum(1)
        row = {
            "split": D.split_of(ETAS.index(e)), "n": len(traj), "n_traj": len(tr_ids),
            "null_count_mean": float(counts.mean()), "null_count_sd": float(counts.std()),
            "null_count_se": float(counts.std(ddof=1) / np.sqrt(len(counts))),
            "k_lambda": float(np.sqrt(ref["j2"].mean() / ref["b2"].mean())),
            "ed_floor_512": ctx.floor(e, min(cfg["n_gen"], len(traj) // 2)),
            "balance_residual_total": float(res_a.mean() / sinks), "balance_residual_total_se": float(se(res_a) / sinks),
            "balance_residual_magnetic": float(M.budget_summary(bud)["balance_residual_magnetique"]),
            "current_helicity_z": float(jb.mean() / se(jb)),
            "r_b": float(abs(ref["J_shell"].mean(0).sum()) / np.abs(ref["J_shell"].mean(0)).sum()),
            "H_k1": float(H[:, 0].mean()), "H_k1_se": float(se(H[:, 0])),
            "H_k_ge_2": float(Hsmall.mean()), "H_k_ge_2_se": float(se(Hsmall)),
            "H_shell": ref["H_shell"].mean(0).tolist(), "J_shell": ref["J_shell"].mean(0).tolist(),
            "EB_k1_fraction": float(frac1.mean()), "EB_k1_fraction_se": float(se(frac1)),
            "E_u": float(bud["kinetic_energy"].mean()), "E_B": float(bud["magnetic_energy"].mean()),
            "H_M": float(ref["Hm"].mean()), "H_M_sd": float(ref["Hm"].std()),
            "hc_sign_asym": float(abs((ref["Hc"] > 0).mean() - 0.5)),
            "spec_b": ref["spec_b"].mean(0).tolist(), "spec_u": ref["spec_u"].mean(0).tolist(),
            "std_diss": float((bud["kinetic_dissipation"] + bud["magnetic_dissipation"]).std()),
        }
        if D.split_of(ETAS.index(e)) == "test":
            ridx = rng.choice(len(traj), size=min(cfg["n_restart"], len(traj)), replace=False)
            row.update(ctx.restart_drift(fh[ridx], e))
            for g in (32, 64):                                         # protocol check of H13: grid convergence
                m = min(len(idx), 100)
                bg = ctx.pot.to_grid(fh[idx[:m], 1:2].to(torch.complex128), (g,) * 3)[:, 0].numpy()
                row[f"null_count_mean_grid{g}_n{m}"] = float(null_count(bg).mean())
            row[f"null_count_mean_grid{NULL_GRID}_n{min(len(idx), 100)}"] = float(counts[: min(len(idx), 100)].mean())
        out["values"][f"{e:.5f}"] = row
        print(f"eta {e:.5f} nulls {row['null_count_mean']:.1f} ± {row['null_count_se']:.1f}  k_lambda {row['k_lambda']:.2f}  "
              f"H(1) {row['H_k1']:+.4f}  H(k>=2) {row['H_k_ge_2']:+.4f}  E1/EB {row['EB_k1_fraction']:.2f}  "
              f"z(j.B) {row['current_helicity_z']:+.1f}  floor {row['ed_floor_512']:.4f}", flush=True)
    out["duration_s"] = time.time() - t0
    save_json(out, f"e4_reference{'_quick' if quick else ''}.json")
    print(f"reference done in {time.time() - t0:.0f} s")


# ---------------------------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------------------------
def _group_of(variant: str) -> str:
    """Group of a variant name (derived rows such as W5_stationarity_half belong to group B, W2 to A)."""
    for g, names in GROUPS.items():
        if variant in names:
            return g
    return "B"


def train(field, loss_fn, x: torch.Tensor, c: torch.Tensor, iters: int, lr: float, batch: int, name: str,
          onecycle: bool = True, ema_from=None, extra_loss=None, log: int = 4):
    """Train ``field`` on (x, c); returns (EMA copy of the field in eval mode, duration in s)."""
    opt = torch.optim.AdamW(field.parameters(), lr=lr, weight_decay=0.0)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=iters, pct_start=0.05) if onecycle else None
    ema = copy.deepcopy(field if ema_from is None else ema_from)
    for p in ema.parameters():
        p.requires_grad_(False)
    t0, run = time.time(), 0.0
    for it in range(1, iters + 1):
        idx = torch.randint(0, len(x), (batch,))
        loss = loss_fn(field, x[idx], c[idx])
        if extra_loss is not None:
            loss = loss + extra_loss(field, it)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(field.parameters(), 1.0)
        opt.step()
        if sched is not None:
            sched.step()
        decay = min(0.999, (1 + it) / (10 + it)) if ema_from is None else 0.99
        with torch.no_grad():
            for pe, p in zip(ema.parameters(), field.parameters(), strict=True):
                pe.mul_(decay).add_(p.detach(), alpha=1 - decay)
        run = loss.item() if it == 1 else 0.98 * run + 0.02 * loss.item()
        if it % max(iters // log, 1) == 0 or it == iters:
            print(f"[{name}] it {it:5d}  loss {run:.4f}  {time.time() - t0:.0f} s", flush=True)
    return ema.eval(), time.time() - t0


def run(quick: bool, seed: int, group: str, device: str = "cpu", cond_scale: float = 8.0) -> None:
    """``cond_scale``: maximum frequency of the condition embedding of every network of the run (8: the
    pre-race default, registered protocol of H4-H14; another value tags the output files ``_cs<value>``)."""
    t_start = time.time()
    groups = [g for g in GROUPS if g not in ("L", "S")] if group == "all" else group.split(",")
    need = tuple(sorted({s for g in groups for s in {"A": ("comp",), "B": ("pot", "pot_sym"), "C": ("pot",),
                                                     "D": ("pot_sym",), "E": ("pot_sym",), "L": ("pot_sym",),
                                                     "S": ("pot_sym",)}[g]}))
    need = ("pot", "pot_sym", "comp") if len(need) == 3 else need
    ctx = Context(quick, need, device)
    cfg, dev = ctx.cfg, ctx.dev
    if ctx.ref_json is None:
        raise SystemExit("run `python3 e4_mhd3d.py --reference` first")
    names = [v for g in groups for v in GROUPS[g]]
    pot, pot_sym, comp = ctx.pot_d, ctx.pot_sym_d, ctx.comp_d          # on the training device
    net = lambda sp, cs=cond_scale: ResMLP(sp.n_modes, sp.n_channels, 1, width=cfg["width"], depth=cfg["depth"],   # noqa: E731
                                           cond_scale=cs).to(dev)
    eval_etas = [(e, cfg["n_gen"]) for e in ETA_VAL + ETA_TEST] + [(e, cfg["n_gen_train"]) for e in ETA_TRAIN_EVAL]
    split = lambda e: "train" if e in ETA_TRAIN else ("val" if e in ETA_VAL else "test")              # noqa: E731
    results: dict = {"config": {**cfg, "quick": quick, "seed": seed, "group": group, "device": str(dev),
                                "cond_scale": cond_scale,
                                "N": D.N, "nu": D.NU, "kf": D.KF,
                                "eta_train": ETA_TRAIN, "eta_val": ETA_VAL, "eta_test": ETA_TEST,
                                "modes": pot.n_modes, "dim_potentials": pot.n_modes * pot.n_channels,
                                "dim_components": comp.n_modes * comp.n_channels,
                                "n_train": ctx.n_train},
                     "evaluation": {}, "times": {}, "h14": [], "h12": []}
    gens: dict = {}

    tag = ("" if cond_scale == 8.0 else f"_cs{cond_scale:g}") + ("_quick" if quick else "")

    def save_parts() -> None:
        """Write one result file per group and the merged file (called after every variant: a job that is
        cut by its time limit keeps what it has evaluated)."""
        results["total_duration_s"] = time.time() - t_start
        for g in groups:
            part = dict(results, evaluation={k: v for k, v in results["evaluation"].items() if _group_of(k) == g},
                        times={k: v for k, v in results["times"].items() if _group_of(k) == g},
                        h14=results["h14"] if g == "A" else [], h12=results["h12"] if g == "B" else [])
            part["config"] = {**results["config"], "group": g}
            if part["evaluation"]:
                save_json(part, f"e4_mhd3d{tag}_s{seed}_{g}.json")
        merge(seed, tag)

    def noise(n: int, sp, salt: int) -> torch.Tensor:
        g = torch.Generator().manual_seed(100003 * seed + salt)
        return torch.randn(n, sp.n_modes, sp.n_channels, generator=g).to(dev)

    @torch.no_grad()
    def generate(model, sp, eta: float, n: int, kind: str = "heun", steps: int | None = None) -> torch.Tensor:
        """Field coefficients (n, 2, M, 3) generated at ``eta`` (same noise for every variant of a space)."""
        c = torch.full((n, 1), float(cn(eta)), device=dev)
        z0 = noise(n, sp, ETAS.index(eta))
        steps = steps or cfg["steps"]
        out = []
        for i in range(0, n, 256):
            zi, ci = z0[i:i + 256], c[i:i + 256]
            if kind == "projected":
                z = C.projected_flow_sample(model, sp, zi, ci, steps=steps)
            elif kind == "diffusion":
                g = torch.Generator().manual_seed(7 + 100003 * seed + ETAS.index(eta))
                z = diffusion_sample(model, zi, ci, steps=2 * steps, stochastic=True, generator=g)
            else:
                z = heun_sample(model, zi, ci, steps=steps)
            out.append(sp.field_hat(sp.denormalize(z)).cpu())
        return torch.cat(out)

    def record(name: str, fhs: dict, restart: bool = True) -> None:
        """Evaluate the ensembles ``{eta: fh}`` (or ``{eta: (fh, weights)}``) of a variant."""
        ev: dict = {"train": [], "val": [], "test": []}
        for e, item in fhs.items():
            fh, w = item if isinstance(item, tuple) else (item, None)
            row = ctx.evaluate(fh, e, w)
            if restart and split(e) == "test" and w is None:
                row.update(ctx.restart_drift(fh, e))
            ev[split(e)].append(row)
        results["evaluation"][name] = ev
        save_parts()
        test = ev["test"]
        print(f"== {name}: test ed_ratio {np.mean([r['ed_ratio'] for r in test]):.2f}  "
              f"div_b {np.mean([r['div_rel_b_mean'] for r in test]):.2e}  "
              f"balance {np.mean([abs(r['balance_residual_total']) for r in test]):.3f}  "
              f"spec_b {np.mean([r['spec_err_b_l2'] for r in test]):.3f}  "
              f"Hm {np.mean([r['hel_m_err_rel'] for r in test]):.3f}  "
              f"nulls {np.mean([r.get('null_count_err_rel', np.nan) for r in test]):.3f}  "
              f"restart {np.mean([r.get('restart_drift_eb', np.nan) for r in test]):.3f}", flush=True)

    def fit(name: str, sp, x, loss_fn):
        seed_all(seed)
        model, tsec = train(net(sp) if not name.endswith("_sym") else SignSymmetrized(net(sp), sp.sign).to(dev),
                            loss_fn, x, ctx.c_train, cfg["iters"], cfg["lr"], cfg["batch"], name)
        results["times"][name] = {"training_time_s": tsec}
        return model

    fm = lambda f, x, c: fm_loss(f, x, c)                                                      # noqa: E731

    # ---------------- group A: free components ----------------
    if "W0_free" in names:
        m0 = fit("W0_free", comp, ctx.x_comp, fm)
        gens["W0_free"] = {e: generate(m0, comp, e, n) for e, n in eval_etas}
        record("W0_free", gens["W0_free"])
        record("W2_final_projection", {e: C.leray_hat(fh, ctx.comp.k) for e, fh in gens["W0_free"].items()})
        for e in ETA_TEST:                                             # H14: 50 against 200 integration steps
            row = {"eta": e}
            for steps in (cfg["steps"], 4 * cfg["steps"]):
                fh = generate(m0, comp, e, min(128, cfg["n_gen"]), steps=steps)
                row[f"div_rel_b_mean_steps{steps}"] = float(C.divergence_fraction_hat(fh, ctx.comp.k)[:, 1].sqrt().mean())
            results["h14"].append(row)
        del m0
        pen = C.divergence_penalty(comp, weight=10.0)
        m1 = fit("W1_penalty", comp, ctx.x_comp, lambda f, x, c: fm_loss(f, x, c, extra=pen))
        record("W1_penalty", {e: generate(m1, comp, e, n) for e, n in eval_etas})
        del m1
        pnoise = lambda shape: comp.project(torch.randn(shape, device=dev))                    # noqa: E731
        m3 = fit("W3_projected_flow", comp, ctx.x_comp, lambda f, x, c: fm_loss(f, x, c, noise_fn=pnoise))
        record("W3_projected_flow", {e: generate(m3, comp, e, n, kind="projected") for e, n in eval_etas})
        del m3

    # ---------------- group B: vector potentials ----------------
    if "W4_potentials" in names:
        m4 = fit("W4_potentials", pot, ctx.x_pot, fm)
        record("W4_potentials", {e: generate(m4, pot, e, n) for e, n in eval_etas})
        del m4
        m6 = fit("W6_diffusion", pot, ctx.x_pot, lambda f, x, c: diffusion_loss(f, x, c))
        record("W6_diffusion", {e: generate(m6, pot, e, n, kind="diffusion") for e, n in eval_etas})
        del m6
        m4s = fit("W4s_potentials_sym", pot_sym, ctx.x_pot_sym, fm)
        gens["W4s"] = {e: generate(m4s, pot_sym, e, n) for e, n in eval_etas}
        record("W4s_potentials_sym", gens["W4s"])

        # law-level identities on a batch of generated coefficients
        def identities(fh: torch.Tensor, eta, sp=ctx.pot_sym) -> dict:
            terms = C.budget_terms_hat(sp, fh, D.NU, eta, forcing_hat=ctx.forcing_hat.to(fh.device, fh.dtype), amp=AMP)
            return C.stationarity_residuals(terms, D.NU, eta)

        def stat_loss(field, it: int) -> torch.Tensor:
            nc, nper = cfg["stat_cond"], cfg["stat_per"]
            lo, hi = float(cn(ETAS[-1])), float(cn(ETAS[0]))
            c = (lo + (hi - lo) * torch.rand(nc, 1, device=dev)).repeat_interleave(nper, 0)
            z = heun_sample(field, torch.randn(nc * nper, pot_sym.n_modes, pot_sym.n_channels, device=dev), c,
                            cfg["stat_steps"])
            res = identities(pot_sym.field_hat(pot_sym.denormalize(z)), eta_of(c[:, 0]), pot_sym)
            pen = sum(C.half_batch_product(r, s, nc) for key, (r, s) in res.items() if key != "cross_helicity")
            return cfg["beta"] * min(1.0, it / max(cfg["ft_iters"] // 4, 1)) * pen

        for vname, extra in (("W5_stationarity", stat_loss), ("W5_control", None)):
            seed_all(1 + seed)
            model, tsec = train(copy.deepcopy(m4s).train().requires_grad_(True), fm, ctx.x_pot_sym, ctx.c_train,
                                cfg["ft_iters"], cfg["ft_lr"], cfg["batch"], vname, onecycle=False, ema_from=m4s,
                                extra_loss=extra)
            results["times"][vname] = {"finetuning_time_s": tsec, "iters": cfg["ft_iters"], "beta": cfg["beta"] if extra else 0.0}
            gens[vname] = {e: generate(model, pot_sym, e, n) for e, n in eval_etas}
            record(vname, gens[vname])
            if vname == "W5_stationarity":
                torch.save(model.state_dict(), D.data_dir(quick) / f"model_W5_stationarity_s{seed}.pt")
            del model
        torch.save(m4s.state_dict(), D.data_dir(quick) / f"model_W4s_potentials_sym_s{seed}.pt")
        del m4s

        # sampling-time constraints in law, on the samples of the control model
        def tilt(fh: torch.Tensor, eta: float, keys: tuple[str, ...]) -> tuple[torch.Tensor, np.ndarray, dict]:
            res = identities(fh.to(torch.complex128), eta)
            g = np.stack([(res[k][0] / res[k][1].mean()).numpy() for k in keys], axis=1)
            half = len(fh) // 2
            _, lam, info = C.balance_tilting(g[:half], reg=1.0)
            zb = g[half:] @ lam
            wb = np.exp(zb - zb.max())
            return fh[half:], wb / wb.sum(), info

        tilted, rescaled, halves = {}, {}, {}
        for e, fh in gens["W5_control"].items():
            fb, wb, _ = tilt(fh, e, ("energy", "magnetic_helicity"))
            tilted[e] = (fb, wb)
            out, _ = C.balance_rescaling(ctx.pot_sym, fh.to(torch.complex128), D.NU, e, ctx.forcing_hat, amp=AMP)
            rescaled[e] = out
            halves[e] = gens["W5_stationarity"][e][len(fh) // 2:]
        record("W7_tilting", tilted)
        record("W8_rescaling", rescaled, restart=False)
        record("W5_stationarity_half", halves, restart=False)
        record("W5_control_half", {e: fh[len(fh) // 2:] for e, fh in gens["W5_control"].items()}, restart=False)
        for e in ETA_TEST:                                             # H12: which identity has leverage
            fh = gens["W4s"][e]
            base = ctx.evaluate(fh[len(fh) // 2:], e, nulls=False)
            row = {"eta": e, "r_a": base["r_a"], "r_b": base["r_b"], "hel_m_err_rel_base": base["hel_m_err_rel"],
                   "ed_ratio_base": base["ed_ratio"]}
            for tag, keys in (("a", ("energy",)), ("b", ("magnetic_helicity",)), ("ab", ("energy", "magnetic_helicity"))):
                fb, wb, _ = tilt(fh, e, keys)
                r = ctx.evaluate(fb, e, wb, nulls=False)
                row.update({f"hel_m_err_rel_tilt_{tag}": r["hel_m_err_rel"], f"ess_frac_tilt_{tag}": r["ess_frac"],
                            f"ed_ratio_tilt_{tag}": r["ed_ratio"], f"balance_tilt_{tag}": r["balance_residual_total"],
                            f"r_b_tilt_{tag}": r["r_b"]})
            results["h12"].append(row)

    if "W4c_potentials_smooth" in names and cond_scale == 8.0:     # H15 (pointless when the whole run is smooth)
        seed_all(seed)
        mc, tsec = train(net(pot, 0.5), fm, ctx.x_pot, ctx.c_train, cfg["iters"], cfg["lr"], cfg["batch"],
                         "W4c_potentials_smooth")
        results["times"]["W4c_potentials_smooth"] = {"training_time_s": tsec}
        record("W4c_potentials_smooth", {e: generate(mc, pot, e, n) for e, n in eval_etas})
        del mc

    # ---------------- group D: second-order baseline and explicit affine term ----------------
    if "G0_gaussian_modes" in names:
        t0 = time.time()
        g0 = C.ModewiseGaussian(sign=pot_sym.sign).fit(ctx.x_pot_sym, ctx.c_train[:, 0])
        results["times"]["G0_gaussian_modes"] = {"fit_time_s": time.time() - t0}

        def sample_g0(eta: float, n: int) -> torch.Tensor:
            g = torch.Generator().manual_seed(100003 * seed + 31 + ETAS.index(eta))
            z = g0.sample(float(np.float32(cn(eta))), n, generator=g)
            return pot_sym.field_hat(pot_sym.denormalize(z)).cpu()

        record("G0_gaussian_modes", {e: sample_g0(e, n) for e, n in eval_etas})
        del g0
    # ---------------- groups D, E, L: explicit affine term, anchor on the Gaussian field ----------------
    def skip(base: torch.nn.Module) -> torch.nn.Module:
        return C.ModewiseAffineSkip(base, pot_sym.n_modes, pot_sym.n_channels, 1, cond_scale=0.5)

    def sym(field: torch.nn.Module) -> torch.nn.Module:
        return SignSymmetrized(field, pot_sym.sign)

    builders = {
        "W9_skip_sym": lambda gauss: sym(skip(net(pot_sym, 0.5))),
        "W10_anchored": lambda gauss: C.GaussianAnchoredField(sym(net(pot_sym, 0.5)), gauss),
        "W11_anchored_skip": lambda gauss: C.GaussianAnchoredField(sym(skip(net(pot_sym, 0.5))), gauss),
    }
    builders["W9L_skip_long"] = builders["W9_skip_sym"]
    builders["W11L_anchored_skip_long"] = builders["W11_anchored_skip"]

    def scan(width: int):                                # H21: no affine term, width of the network varied
        return lambda gauss: sym(ResMLP(pot_sym.n_modes, pot_sym.n_channels, 1, width=width if not quick else width // 8,
                                        depth=cfg["depth"], cond_scale=0.5))

    for w in (512, 2048, 5632):
        builders[f"S_w{w}"] = builders[f"S_w{w}_long"] = scan(w)
    todo = [v for v in names if v in builders]
    if todo:
        gauss = C.ModewiseGaussian(sign=pot_sym.sign).fit(ctx.x_pot_sym, ctx.c_train[:, 0])
        for vname in todo:
            seed_all(seed)
            iters = cfg["iters"] * (cfg["long_factor"] if vname.endswith("_long") else 1)
            model, tsec = train(builders[vname](gauss).to(dev), fm, ctx.x_pot_sym, ctx.c_train, iters, cfg["lr"],
                                cfg["batch"], vname)
            results["times"][vname] = {"training_time_s": tsec, "iters": iters}
            with torch.no_grad():                                     # final flow-matching loss against π/2
                gl = torch.Generator().manual_seed(11)
                idx = torch.randint(0, len(ctx.x_pot_sym), (2048,), generator=gl)
                results["times"][vname]["fm_loss_train_sample"] = float(
                    np.mean([fm_loss(model, ctx.x_pot_sym[idx[k:k + 256]], ctx.c_train[idx[k:k + 256]]).item()
                             for k in range(0, 2048, 256)]))
            record(vname, {e: generate(model, pot_sym, e, n) for e, n in eval_etas})
            del model
        del gauss

    save_parts()
    print(f"total duration {time.time() - t_start:.0f} s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--seed", type=int, default=0, help="seed of the networks, the training and the generation")
    ap.add_argument("--group", default="all", help="A, B, C, D, E, L, a comma-separated list, or all (= A to E)")
    ap.add_argument("--reference", action="store_true", help="reference statistics only (no model)")
    ap.add_argument("--threads", type=int, default=1)
    ap.add_argument("--device", default="cpu", help="cpu or cuda: networks, training sets and generation")
    ap.add_argument("--cond-scale", type=float, default=8.0,
                    help="maximum frequency of the condition embedding of every network (default 8, the registered protocol)")
    a = ap.parse_args()
    torch.set_num_threads(a.threads)
    if a.reference:
        reference(a.quick)
    else:
        run(a.quick, a.seed, a.group, a.device, a.cond_scale)
