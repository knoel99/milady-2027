"""Rename the French identifiers of the E1–E3 result files to English, without recomputing anything.

The scripts of ``experiments/`` write English keys since November 2026; results produced before keep
French keys (``V0_libre``, ``entrainement``, ``e1_echantillons.npz``…). This script rewrites them in
place with the table :data:`RENAME`: JSON files keep their key order and their exact float values
(same ``json.dumps`` settings as ``common.save_json``), npz files their arrays, and the E1 cache
(``results/cache_e1/``) is renamed too, so that a re-run reuses it.

Usage: python3 rename_results.py [results_dir]      (default: results/ next to this script)
It is idempotent: already renamed files are left as they are.
"""
from __future__ import annotations

import json
import pickle
import sys
from pathlib import Path

import numpy as np

# French → English. Keys are matched exactly (whole JSON key, whole variant name).
RENAME: dict[str, str] = {
    # E1 variants
    "C_court": "C_short",
    "C_court_moitie": "C_short_half",
    "A_reference_moitie": "A_reference_half",
    "C_equivariant_moitie": "C_equivariant_half",
    "D_inclinaison_A": "D_tilting_A",
    "D_inclinaison_C": "D_tilting_C",
    "D_inclinaison_Ccourt": "D_tilting_Cshort",
    "F_stationnarite_C": "F_stationarity_C",
    "F_stationnarite_Ccourt": "F_stationarity_Cshort",
    "F0_temoin_C": "F0_control_C",
    "F0_temoin_Ccourt": "F0_control_Cshort",
    "C_grand": "C_large",
    # E2 variants
    "V0_libre": "V0_free",
    "V1_penalite": "V1_penalty",
    "V2_proj_finale": "V2_final_projection",
    "V3_flot_projete": "V3_projected_flow",
    "V4_potentiels": "V4_potentials",
    "V5_potentiels_stat": "V5_potentials_stat",
    "V5_temoin": "V5_control",
    "reference_sous_echantillon": "reference_subsample",
    # sections
    "donnees": "data",
    "entrainement": "training",
    "resume": "summary",
    "grille_fine": "fine_grid",
    "duree_totale_s": "total_duration_s",
    "planchers_bruit_MC": "mc_noise_floors",
    "variantes": "variants",
    "en_loi": "in_law",
    "inclinaison": "tilting",
    "recalage": "rescaling",
    "taux": "rates",
    "seuils_interpoles": "interpolated_thresholds",
    "duree_s": "duration_s",
    "lambda_dernier_quart": "lambda_last_quarter",
    # configuration
    "trajectoires_par_Gamma": "trajectories_per_Gamma",
    "duree_gardee": "kept_duration",
    "pas_ODE_Heun": "heun_ode_steps",
    "largeur_MLP": "mlp_width",
    "profondeur_MLP": "mlp_depth",
    "inclinaison_reg": "tilting_reg",
    "reglage_fin": "finetuning",
    "gammas_par_pas": "gammas_per_step",
    "echantillons_par_gamma": "samples_per_gamma",
    "pas_Heun_differentiable": "differentiable_heun_steps",
    "dim_potentiels": "dim_potentials",
    "dim_composantes": "dim_components",
    "largeur": "width",
    "n_train_par_eta": "n_train_per_eta",
    # metrics
    "energie": "energy",
    "pont": "bridge",
    "pont_ref": "bridge_ref",
    "pont_modele": "bridge_model",
    "pont_modele_F": "bridge_model_F",
    "liou_train_moy": "liou_train_mean",
    "liou_test_moy": "liou_test_mean",
    "dEdt_moy": "dEdt_mean",
    "taux_rice": "rice_rate",
    "taux_rice_ref": "rice_rate_ref",
    "taux_rice_modele": "rice_rate_model",
    "taux_rice_modele_F": "rice_rate_model_F",
    "taux_rice_reference": "rice_rate_reference",
    "taux_simulation": "simulation_rate",
    "taux_passages_simulation": "simulation_crossing_rate",
    "taux_passages": "crossing_rate",
    "V_q99_modele": "V_q99_model",
    "dans_entrainement": "in_training",
    "erreur_pont": "bridge_error",
    "erreur_taux_rice": "rice_rate_error",
    "erreur_taux_rice_ref": "rice_rate_error_ref",
    "balance_residual_energie": "balance_residual_energy",
    "Hc_moy": "Hc_mean",
    "ess_frac_b_moy": "ess_frac_b_mean",
    # times
    "perte_finale": "final_loss",
    "temps_entrainement_s": "training_time_s",
    "temps_generation_s_par_1000": "generation_time_s_per_1000",
    "temps_generation_s_par_echantillon": "generation_time_s_per_sample",
    "temps_reglage_fin_s": "finetuning_time_s",
}

FILES = {
    "e1_echantillons.npz": "e1_samples.npz",
    "e1_echantillons_quick.npz": "e1_samples_quick.npz",
    "e2_echantillons.npz": "e2_samples.npz",
    "e2_echantillons_quick.npz": "e2_samples_quick.npz",
    "e1_echantillons_complet.npz": "e1_samples_full.npz",
    "e1_echantillons_complet_quick.npz": "e1_samples_full_quick.npz",
}


def rename(obj):
    """Rename the keys of nested dicts (order kept); values are left untouched."""
    if isinstance(obj, dict):
        return {RENAME.get(k, k) if isinstance(k, str) else k: rename(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [rename(v) for v in obj]
    return obj


def has_french_keys(obj) -> bool:
    """True if a nested dict has a key of :data:`RENAME`."""
    if isinstance(obj, dict):
        return any(k in RENAME for k in obj if isinstance(k, str)) or any(has_french_keys(v) for v in obj.values())
    if isinstance(obj, list):
        return any(has_french_keys(v) for v in obj)
    return False


def npz_key(key: str) -> str:
    """``variant|Γ`` keys of e1 samples, plain keys elsewhere."""
    name, sep, rest = key.partition("|")
    return RENAME.get(name, name) + sep + rest


def rename_json(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    new = json.dumps(rename(json.loads(text)), indent=1, ensure_ascii=False)
    if new == text:
        return False
    path.write_text(new, encoding="utf-8")
    return True


def rename_npz(path: Path, target: Path) -> bool:
    with np.load(path) as d:
        arrays = {npz_key(k): d[k] for k in d.files}
        changed = list(arrays) != d.files or target != path
    if not changed:
        return False
    np.savez_compressed(target, **arrays)
    if target != path:
        path.unlink()
    return True


def rename_cache(cache: Path) -> int:
    """E1 cache: ``<variant>_s<seed>[_quick].pkl`` file names and the dict keys inside the pickles."""
    n = 0
    for path in sorted(cache.glob("*.pkl")):
        stem = path.stem
        quick = stem.endswith("_quick")
        base = stem[: -len("_quick")] if quick else stem
        name, sep, seed = base.rpartition("_s")
        if sep and seed.isdigit():
            base = RENAME.get(name, name) + sep + seed
        target = path.with_name(base + ("_quick" if quick else "") + ".pkl")
        obj = pickle.loads(path.read_bytes())
        if target == path and not has_french_keys(obj):
            continue
        target.write_bytes(pickle.dumps(rename(obj)))
        if target != path:
            path.unlink()
        n += 1
    for old, new in FILES.items():
        if (cache / old).is_file():
            rename_npz(cache / old, cache / new)
            n += 1
    return n


def main(results: Path) -> None:
    for path in sorted(results.glob("e[123]_*.json")):
        print(f"{path.name}: {'renamed keys' if rename_json(path) else 'unchanged'}")
    for path in sorted(results.glob("e[123]_*.npz")):
        target = results / FILES.get(path.name, path.name)
        if rename_npz(path, target):
            print(f"{path.name} -> {target.name}")
    cache = results / "cache_e1"
    if cache.is_dir():
        print(f"cache_e1: {rename_cache(cache)} files renamed")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "results")
