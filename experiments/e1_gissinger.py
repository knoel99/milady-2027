"""E1 - Parametric invariant law of the Gissinger reversal model (2012).

Three-mode model (quadrupole Q, dipole D, velocity V):
    dQ/dt = mu Q - V D
    dD/dt = -nu D + V Q
    dV/dt = Gamma - V + Q D
mu = 0.119, nu = 0.1; the control parameter is Gamma. Symmetry: (Q, D, V) -> (-Q, -D, V),
the analogue of the B -> -B reversal.

We learn the law p(Q, D, V | Gamma) by conditional flow matching and compare:
  A. baseline (flow matching);
  B. baseline + data augmentation by the symmetry;
  C. equivariant velocity field (exact symmetry by construction);
  C_court. same architecture as C, reduced training budget (biased model);
  D_*. exponential tilting on the stationarity identities (constraint in law);
  E_C. projection of each sample of C onto dE/dt = 0 (sample-by-sample constraint);
  F_*. fine-tuning with a stationarity loss (Liouville identities imposed at every Gamma,
       including values without data), with its control F0_* (same fine-tuning, without the loss).
We also estimate the frequency of zero crossings of D (reversals and excursions) from
the generated law alone, using Rice's formula, and compare it with the simulations.

Usage: python3 e1_gissinger.py [--quick]
Outputs: results/e1_gissinger[_quick].json, results/e1_echantillons[_quick].npz
"""
from __future__ import annotations

import argparse
import itertools
import time

import numpy as np
import torch

from common import (MLPField, SymmetrizedField, energy_distance, exp_tilt, heun_sample, save_json, sample_ode,
                    seed_all, sliced_w1, systematic_resample, train, RESULTS)

import pickle

CACHE = RESULTS / "cache_e1"


def cached(name, fn):
    """Compute fn() only once: the result is kept in results/cache_e1/ (resume after interruption)."""
    CACHE.mkdir(exist_ok=True)
    path = CACHE / f"{name}.pkl"
    if path.is_file():
        print(f"(cache) {name}", flush=True)
        return pickle.loads(path.read_bytes())
    out = fn()
    tmp = path.with_suffix(".tmp")
    tmp.write_bytes(pickle.dumps(out))
    tmp.replace(path)
    return out


MU, NU = 0.119, 0.1
S = np.array([-1.0, -1.0, 1.0])
G_TRAIN = np.round(np.arange(0.80, 1.0001, 0.02), 3)
G_TEST = np.round(np.arange(0.81, 0.9901, 0.02), 3)
G_FINE = np.round(np.arange(0.80, 1.0001, 0.005), 3)
G_LO, G_HI = 0.78, 1.02
H_RICE = 0.2  # half-width of the |D| < h window of the Rice estimator


def rhs(x, g):
    q, d, v = x[..., 0], x[..., 1], x[..., 2]
    return np.stack([MU * q - v * d, -NU * d + v * q, g - v + q * d], -1)


def simulate(gammas, n_traj, t_burn, t_keep, every, dt=0.01, seed=0):
    """Integrate (RK4) n_traj trajectories per value of Gamma, symmetric initial conditions.

    Also counts, at each time step, the zero crossings of D (after the transient).
    """
    rng = np.random.default_rng(seed)
    g = np.repeat(np.asarray(gammas, dtype=float), n_traj)
    x = rng.normal(size=(len(g), 3)) * 0.8
    x[:, 2] = np.abs(x[:, 2])
    nb, nk, ne = int(t_burn / dt), int(t_keep / dt), int(every / dt)
    out = []
    crossings = np.zeros(len(g))
    for k in range(nb + nk):
        sd = np.sign(x[:, 1])
        k1 = rhs(x, g); k2 = rhs(x + 0.5 * dt * k1, g)
        k3 = rhs(x + 0.5 * dt * k2, g); k4 = rhs(x + dt * k3, g)
        x = x + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if k >= nb:
            crossings += np.sign(x[:, 1]) != sd
            if (k - nb) % ne == 0:
                out.append(x.copy())
    arr = np.stack(out, 1)  # (len(g), n_samples, 3)
    data = {}
    for i, gam in enumerate(gammas):
        sl = slice(i * n_traj, (i + 1) * n_traj)
        data[float(gam)] = {"x": arr[sl].reshape(-1, 3),
                            "taux_passages": float(crossings[sl].sum() / (n_traj * t_keep)),
                            "P(D>0)": float((arr[sl][..., 1] > 0).mean())}
    return data


# ---------------------------------------------------------------------------
# Stationarity identities (weak form of Liouville): E[F·∇phi] = 0
# ---------------------------------------------------------------------------
MONO_TRAIN = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 1, 0), (1, 0, 1), (0, 1, 1)]
MONO_TEST = [p for p in itertools.product(range(4), repeat=3) if sum(p) == 3]


def generator_terms(x, g, monos):
    """For each monomial phi = Q^a D^b V^c, return F(x)·∇phi(x), of shape (N, len(monos))."""
    f = rhs(x, g)
    q, d, v = x[:, 0], x[:, 1], x[:, 2]
    cols = []
    for a, b, c in monos:
        dq = a * q ** max(a - 1, 0) * d ** b * v ** c if a else 0 * q
        dd = b * q ** a * d ** max(b - 1, 0) * v ** c if b else 0 * q
        dv = c * q ** a * d ** b * v ** max(c - 1, 0) if c else 0 * q
        cols.append(f[:, 0] * dq + f[:, 1] * dd + f[:, 2] * dv)
    return np.stack(cols, 1)


def liouville_residual(x, g, monos, ref):
    """Residuals |E_q[F·∇phi]| normalised by the standard deviation of F·∇phi under the reference law."""
    gq = generator_terms(x, g, monos).mean(0)
    sd = generator_terms(ref, g, monos).std(0) + 1e-12
    return np.abs(gq) / sd


def dEdt(x, g):
    """Time derivative of the energy E = (Q² + D² + V²)/2 along the flow."""
    return generator_terms(x, g, [(2, 0, 0), (0, 2, 0), (0, 0, 2)]).sum(1) / 2


def rice_rate(x, h=H_RICE):
    """Rice formula: frequency of zero crossings of D = E[|dD/dt| δ(D)] ≈ E[|VQ| 1{|D|<h}] / (2h)."""
    q, d, v = x[:, 0], x[:, 1], x[:, 2]
    ddot = np.abs(-NU * d + v * q)
    return float(np.mean(ddot * (np.abs(d) < h)) / (2 * h))


def project_energy_balance(x, g, iters=20):
    """Projection of each sample onto the surface dE/dt(x) = 0 (Newton, minimal displacement)."""
    y = x.copy()
    eps = 1e-5
    for _ in range(iters):
        r = dEdt(y, g)
        grad = np.stack([(dEdt(y + eps * e, g) - dEdt(y - eps * e, g)) / (2 * eps) for e in np.eye(3)], 1)
        y = y - (r / (np.sum(grad ** 2, 1) + 1e-12))[:, None] * grad
    return y


def generator_terms_torch(x, g, monos):
    """PyTorch (differentiable) version of generator_terms; g: (N,) tensor."""
    q, d, v = x[:, 0], x[:, 1], x[:, 2]
    f = torch.stack([MU * q - v * d, -NU * d + v * q, g - v + q * d], 1)
    cols = []
    for a, b, c in monos:
        z = torch.zeros_like(q)
        dq = a * q ** max(a - 1, 0) * d ** b * v ** c if a else z
        dd = b * q ** a * d ** max(b - 1, 0) * v ** c if b else z
        dv = c * q ** a * d ** b * v ** max(c - 1, 0) if c else z
        cols.append(f[:, 0] * dq + f[:, 1] * dd + f[:, 2] * dv)
    return torch.stack(cols, 1)


def finetune(model, batcher, iters, beta, sd, mean, std, cnorm, n_gamma=8, n_per=128, steps=8, lr=5e-4, name=""):
    """Fine-tuning: flow matching loss + beta × stationarity loss.

    Stationarity loss: for n_gamma values of Gamma drawn uniformly in [0.80, 1.00]
    (hence also between the training values), we generate n_per samples with a differentiable
    Heun scheme with `steps` steps, then penalise Σ_k (E[F·∇phi_k] / sd_k)² over the monomials of degree <= 2,
    estimated without bias by the product of the means of two half-batches.
    """
    from common import fm_loss
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    mean_t = torch.tensor(mean, dtype=torch.float32)
    std_t = torch.tensor(std, dtype=torch.float32)
    sd_t = torch.tensor(sd, dtype=torch.float32)
    t0 = time.time()
    for it in range(1, iters + 1):
        x1, c = batcher()
        loss = fm_loss(model, x1, c)
        if beta > 0:
            gam = 0.80 + 0.20 * torch.rand(n_gamma)
            gg = gam.repeat_interleave(n_per)
            cc = torch.tensor(cnorm(gg.numpy()), dtype=torch.float32)
            z = heun_sample(model, torch.randn(n_gamma * n_per, 3), cc, steps=steps)  # differentiable
            x = z * std_t + mean_t
            gt = generator_terms_torch(x, gg, MONO_TRAIN).view(n_gamma, 2, n_per // 2, -1).mean(2) / sd_t
            # Unbiased estimator of (E[F·∇phi])²: product of the means of two independent half-batches.
            # (The square of a single mean equals (E g)² + Var(g)/n: it would penalise the spread of the law.)
            loss = loss + beta * (gt[:, 0] * gt[:, 1]).mean()
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        if it % max(iters // 4, 1) == 0:
            print(f"[{name}] fine-tuning it {it}  loss {loss.item():.4f}  {time.time() - t0:.0f} s", flush=True)
    return time.time() - t0


# ---------------------------------------------------------------------------
def main(quick=False, reverse=False, train_only=False):
    torch.set_num_threads(2)
    t_start = time.time()
    n_traj, t_keep = (8, 800) if quick else (16, 3000)
    print("simulation (training)...", flush=True)
    q = "_quick" if quick else ""
    train_data = cached(f"sim_train{q}", lambda: simulate(G_TRAIN, n_traj, 300, t_keep, every=2.0, seed=1))
    print("simulation (reference)...", flush=True)
    ref_data = cached(f"sim_ref{q}", lambda: simulate(np.concatenate([G_TRAIN, G_TEST]), 2 * n_traj, 300, t_keep, every=2.0, seed=2))
    ref_data = {k: dict(v) for k, v in ref_data.items()}
    for k in ref_data:  # exactly symmetric reference (symmetric initial conditions)
        ref_data[k]["x"] = np.concatenate([ref_data[k]["x"], ref_data[k]["x"] * S])
    print("simulation (fine grid)...", flush=True)
    fine_data = cached(f"sim_fine{q}", lambda: simulate(G_FINE, n_traj, 300, t_keep, every=2.0, seed=3))
    fine_data = {k: dict(v) for k, v in fine_data.items()}
    for k in fine_data:
        fine_data[k]["x"] = np.concatenate([fine_data[k]["x"], fine_data[k]["x"] * S])

    stats = {}
    for gam in sorted(ref_data):
        stats[str(gam)] = {"taux_passages_simulation": ref_data[gam]["taux_passages"],
                           "taux_rice_reference": rice_rate(ref_data[gam]["x"]),
                           "P(|D|<0.25)_ref": float((np.abs(ref_data[gam]["x"][:, 1]) < 0.25).mean())}
        if gam in train_data:
            stats[str(gam)]["P(D>0)_train"] = train_data[gam]["P(D>0)"]

    # Normalisation: zero mean imposed on Q and D (preserves S), standard deviation per coordinate
    allx = np.concatenate([train_data[g]["x"] for g in G_TRAIN])
    mean = np.array([0.0, 0.0, allx[:, 2].mean()])
    std = allx.std(0)
    to_z = lambda x: (x - mean) / std
    from_z = lambda z: z * std + mean
    cnorm = lambda g: (np.asarray(g) - G_LO) / (G_HI - G_LO)

    X = torch.tensor(np.concatenate([to_z(train_data[g]["x"]) for g in G_TRAIN]), dtype=torch.float32)
    C = torch.tensor(np.concatenate([np.full(len(train_data[g]["x"]), cnorm(g)) for g in G_TRAIN]), dtype=torch.float32)
    Sz = torch.tensor(S, dtype=torch.float32)

    def batcher(augment):
        def fn():
            idx = torch.randint(0, len(X), (1024,))
            x, c = X[idx], C[idx]
            if augment:
                flip = (torch.rand(len(x)) < 0.5)[:, None]
                x = torch.where(flip, x * Sz, x)
            return x, c
        return fn

    iters = 3000 if quick else 12000
    variants = {"A_reference": ("plain", False, iters), "B_augmentation": ("plain", True, iters),
                "C_equivariant": ("sym", False, iters), "C_court": ("sym", False, max(iters // 10, 300))}
    seeds = [0] if quick else [0, 1]  # two seeds (shared-CPU compute constraint)
    n_gen = 4000 if quick else 10000
    grid = np.concatenate([G_TRAIN, G_TEST])
    results = {"config": {"mu": MU, "nu": NU, "G_train": G_TRAIN.tolist(), "G_test": G_TEST.tolist(),
                          "G_fine": G_FINE.tolist(), "trajectoires_par_Gamma": n_traj, "duree_gardee": t_keep,
                          "iters": {k: v[2] for k, v in variants.items()}, "seeds": seeds, "n_gen": n_gen,
                          "pas_ODE_Heun": 50, "largeur_MLP": 256, "profondeur_MLP": 4, "h_Rice": H_RICE,
                          "inclinaison_reg": 1.0, "reglage_fin": {"beta": 20.0, "gammas_par_pas": 8, "echantillons_par_gamma": 128, "pas_Heun_differentiable": 8, "lr": 5e-4}},
               "donnees": stats, "entrainement": {}}
    gens, models = {}, {}
    jobs = [(vname, cfg, seed) for vname, cfg in variants.items() for seed in seeds]
    if reverse:
        jobs = jobs[::-1]
    for vname, (kind, aug, n_it), seed in jobs:
        if True:
            base = MLPField(3, width=256, depth=4)
            model = SymmetrizedField(base, S) if kind == "sym" else base

            def run(model=model, aug=aug, n_it=n_it, vname=vname, seed=seed):
                seed_all(seed)
                hist, tsec = train(model, batcher(aug), n_it, lr=2e-3, log_every=max(n_it // 4, 1), name=f"{vname}/s{seed}")
                model.eval()
                t0 = time.time()
                g = {}
                for gam in grid:
                    torch.manual_seed(1000 + seed)
                    c = torch.full((n_gen,), float(cnorm(gam)))
                    z = sample_ode(model, c, (n_gen, 3), steps=50)
                    g[float(gam)] = from_z(z.numpy().astype(np.float64))
                info = {"temps_entrainement_s": tsec, "perte_finale": hist[-1][1],
                        "temps_generation_s_par_1000": (time.time() - t0) / (len(grid) * n_gen / 1000)}
                return {"state": {k: v.clone() for k, v in model.state_dict().items()}, "gens": g, "info": info}
            out = cached(f"{vname}_s{seed}{q}", run)
            model.load_state_dict(out["state"]); model.eval()
            models[(vname, seed)] = model
            for gam, xg in out["gens"].items():
                gens[(vname, seed, gam)] = xg
            results["entrainement"].setdefault(vname, {})[f"seed{seed}"] = out["info"]

    # Fine-tunings (F: with stationarity loss; F0: control without the loss)
    import copy
    sd = generator_terms(np.concatenate([train_data[g]["x"] for g in G_TRAIN]),
                         np.concatenate([np.full(len(train_data[g]["x"]), g) for g in G_TRAIN]), MONO_TRAIN).std(0)
    ft_iters = 200 if quick else 800
    ft_jobs = [(b, t, beta, pre, seed) for b, t in (("C_equivariant", "C"), ("C_court", "Ccourt"))
               for beta, pre in ((20.0, "F_stationnarite_"), (0.0, "F0_temoin_")) for seed in seeds]
    if reverse:
        ft_jobs = ft_jobs[::-1]
    for base_name, tag, beta, prefix, seed in ft_jobs:
        vname = prefix + tag
        if True:
            if True:
                model = copy.deepcopy(models[(base_name, seed)])

                def run_ft(model=model, beta=beta, vname=vname, seed=seed):
                    seed_all(100 + seed)
                    model.train()
                    tsec = finetune(model, batcher(False), ft_iters, beta, sd, mean, std, cnorm, name=f"{vname}/s{seed}")
                    model.eval()
                    g = {}
                    for gam in grid:
                        torch.manual_seed(1000 + seed)
                        z = sample_ode(model, torch.full((n_gen,), float(cnorm(gam))), (n_gen, 3), steps=50)
                        g[float(gam)] = from_z(z.numpy().astype(np.float64))
                    return {"state": {k: v.clone() for k, v in model.state_dict().items()}, "gens": g,
                            "info": {"temps_reglage_fin_s": tsec, "iters": ft_iters, "beta": beta}}
                out = cached(f"{vname}_s{seed}{q}", run_ft)
                model.load_state_dict(out["state"]); model.eval()
                models[(vname, seed)] = model
                for gam, xg in out["gens"].items():
                    gens[(vname, seed, gam)] = xg
                results["entrainement"].setdefault(vname, {})[f"seed{seed}"] = out["info"]

    if train_only:
        print("training only: cache filled, stopping", flush=True)
        return
    # Post-processing in law (D) and per sample (E)
    tilt_info = {}
    for base_name, dname in (("C_equivariant", "D_inclinaison_C"), ("C_court", "D_inclinaison_Ccourt"),
                             ("A_reference", "D_inclinaison_A")):
        for seed in seeds:
            for gam in grid:
                gam = float(gam)
                x = gens[(base_name, seed, gam)]
                half = len(x) // 2
                xa, xb = x[:half], x[half:]
                w, lam, info = exp_tilt(generator_terms(xa, gam, MONO_TRAIN), reg=1.0)
                zb = generator_terms(xb, gam, MONO_TRAIN) @ lam  # λ learned on a, applied to b
                wb = np.exp(zb - zb.max()); wb /= wb.sum()
                gens[(dname, seed, gam)] = xb[systematic_resample(wb, len(xb), seed=seed)]
                tilt_info[(dname, seed, gam)] = {"ess_frac_a": info["ess_frac"], "ess_frac_b": float(1 / np.sum(wb ** 2) / len(xb))}
                # Equal-size comparison baseline: the unweighted half b
                gens[(base_name + "_moitie", seed, gam)] = xb
    for seed in seeds:
        for gam in grid:
            gens[("E_projection_C", seed, float(gam))] = project_energy_balance(gens[("C_equivariant", seed, float(gam))], float(gam))

    names = ["A_reference", "B_augmentation", "C_equivariant", "C_court", "D_inclinaison_A", "D_inclinaison_C",
             "D_inclinaison_Ccourt", "E_projection_C", "F_stationnarite_C", "F0_temoin_C", "F_stationnarite_Ccourt",
             "F0_temoin_Ccourt", "A_reference_moitie", "C_equivariant_moitie", "C_court_moitie"]
    evals = {}
    for vname in names:
        for split, gg in (("train", G_TRAIN), ("test", G_TEST)):
            rows = []
            for gam in gg:
                gam = float(gam)
                ref = ref_data[gam]["x"]
                per_seed = []
                for seed in seeds:
                    x = gens[(vname, seed, gam)]
                    per_seed.append({
                        "energie": energy_distance(to_z(x), to_z(ref), n=3000, seed=seed),
                        "sw1": sliced_w1(to_z(x), to_z(ref), seed=seed),
                        "asym": abs(float((x[:, 1] > 0).mean()) - 0.5),
                        "pont": float((np.abs(x[:, 1]) < 0.25).mean()),
                        "liou_train_moy": float(liouville_residual(x, gam, MONO_TRAIN, ref).mean()),
                        "liou_test_moy": float(liouville_residual(x, gam, MONO_TEST, ref).mean()),
                        "dEdt_moy": float(dEdt(x, gam).mean()),
                        "dEdt_std": float(dEdt(x, gam).std()),
                        "taux_rice": rice_rate(x),
                    })
                agg = {k: [float(np.mean([p[k] for p in per_seed])), float(np.std([p[k] for p in per_seed]))]
                       for k in per_seed[0]}
                agg["Gamma"] = gam
                agg["n"] = len(gens[(vname, seeds[0], gam)])
                agg["pont_ref"] = float((np.abs(ref[:, 1]) < 0.25).mean())
                agg["dEdt_std_ref"] = float(dEdt(ref, gam).std())
                agg["taux_simulation"] = ref_data[gam]["taux_passages"]
                agg["taux_rice_ref"] = rice_rate(ref)
                key = vname if vname.startswith("D_") else None
                if key:
                    agg["ess_frac_b"] = float(np.mean([tilt_info[(vname, s, gam)]["ess_frac_b"] for s in seeds]))
                rows.append(agg)
            evals.setdefault(vname, {})[split] = rows

    # Monte Carlo noise floors: subsamples of the reference of the same size as the models
    floors = {}
    for size, label in ((n_gen, "n_gen"), (n_gen // 2, "n_gen/2")):
        e, l1, l2 = [], [], []
        for gam in G_TEST:
            ref = ref_data[float(gam)]["x"]
            rng = np.random.default_rng(7)
            sub = ref[rng.choice(len(ref), size=size, replace=False)]
            e.append(energy_distance(to_z(sub), to_z(ref), n=3000, seed=1))
            l1.append(liouville_residual(sub, float(gam), MONO_TRAIN, ref).mean())
            l2.append(liouville_residual(sub, float(gam), MONO_TEST, ref).mean())
        floors[label] = {"energie": float(np.mean(e)), "liou_train_moy": float(np.mean(l1)), "liou_test_moy": float(np.mean(l2))}

    summary = {}
    for vname in names:
        summary[vname] = {}
        for split in ("train", "test"):
            rows = evals[vname][split]
            summary[vname][split] = {k: float(np.mean([r[k][0] for r in rows]))
                                     for k in ("energie", "sw1", "asym", "liou_train_moy", "liou_test_moy", "dEdt_std")}
            summary[vname][split]["erreur_pont"] = float(np.mean([abs(r["pont"][0] - r["pont_ref"]) for r in rows]))
            summary[vname][split]["erreur_taux_rice"] = float(np.mean([abs(r["taux_rice"][0] - r["taux_simulation"]) for r in rows]))
            if "ess_frac_b" in rows[0]:
                summary[vname][split]["ess_frac_b"] = float(np.mean([r["ess_frac_b"] for r in rows]))
    summary["planchers_bruit_MC"] = floors
    summary["reference"] = {"dEdt_std": float(np.mean([r["dEdt_std_ref"] for r in evals["A_reference"]["test"]])),
                            "erreur_taux_rice_ref": float(np.mean([abs(r["taux_rice_ref"] - r["taux_simulation"]) for r in evals["A_reference"]["test"]]))}

    # Fine grid around the threshold: model C (seed 0), large sample for Rice
    model = models[("C_equivariant", seeds[0])]
    n_big = 8000 if quick else 20000
    fine = []
    for gam in G_FINE:
        torch.manual_seed(5000)
        z = sample_ode(model, torch.full((n_big,), float(cnorm(gam))), (n_big, 3), steps=50)
        x = from_z(z.numpy().astype(np.float64))
        ref = fine_data[float(gam)]["x"]
        torch.manual_seed(5000)
        zf = sample_ode(models[("F_stationnarite_C", seeds[0])], torch.full((n_big,), float(cnorm(gam))), (n_big, 3), steps=50)
        xf = from_z(zf.numpy().astype(np.float64))
        fine.append({"Gamma": float(gam), "taux_simulation": fine_data[float(gam)]["taux_passages"],
                     "taux_rice_modele_F": rice_rate(xf), "pont_modele_F": float((np.abs(xf[:, 1]) < 0.25).mean()),
                     "taux_rice_ref": rice_rate(ref), "taux_rice_modele": rice_rate(x),
                     "pont_ref": float((np.abs(ref[:, 1]) < 0.25).mean()), "pont_modele": float((np.abs(x[:, 1]) < 0.25).mean()),
                     "V_q99_ref": float(np.quantile(ref[:, 2], 0.99)), "V_q99_modele": float(np.quantile(x[:, 2], 0.99)),
                     "dans_entrainement": bool(np.any(np.isclose(G_TRAIN, gam)))})
        if abs(gam - 0.9) < 1e-9 or abs(gam - 0.85) < 1e-9:
            gens[("C_grand", 0, float(gam))] = x[:8000]
    results["grille_fine"] = fine
    results["evaluation"] = evals
    results["resume"] = summary
    results["duree_totale_s"] = time.time() - t_start
    suffix = "_quick" if quick else ""
    save_json(results, f"e1_gissinger{suffix}.json")
    store = {f"{v}|{g}": gens[(v, seeds[0], float(g))][:4000] for v in names for g in grid}
    store.update({f"ref|{g}": ref_data[g]["x"][:8000] for g in ref_data})
    store.update({f"{k[0]}|{k[2]}": v for k, v in gens.items() if k[0] == "C_grand"})
    CACHE.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(CACHE / f"e1_echantillons_complet{suffix}.npz", **store)  # full (≈ 30 MB, not versioned)
    keep = {"0.85", "0.87", "0.9", "0.93"}  # published version: the Γ values of the figures, in float32 (≈ 3 MB)
    np.savez_compressed(RESULTS / f"e1_echantillons{suffix}.npz",
                        **{k: v.astype(np.float32) for k, v in store.items() if k.split("|")[1] in keep})
    for k, v in summary.items():
        print(k, v, flush=True)
    print(f"total duration {time.time() - t_start:.0f} s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--reverse", action="store_true", help="train the models in reverse order (auxiliary process)")
    ap.add_argument("--train-only", action="store_true", help="only fill the model cache, then stop")
    a = ap.parse_args()
    main(a.quick, a.reverse, a.train_only)
