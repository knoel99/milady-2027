#!/usr/bin/env python3
"""data_ch08.py: scene data for unit ch08 that tools/data_existing.py does not provide (READY scenes, decision D4).

No simulation. data/ch08_hillmap.json (08.3) is derived from data/e2_maps.json (itself extracted by data_existing.py
from experiences/resultats/e2_echantillons.npz; spectral display interpolation of the 32^2 modes to 128^2):
  psi, a: stream function and magnetic potential of V4_potentiels sample 0 at eta = 0.00951, from the stored vorticity
          and current by psi_hat = omega_hat / |k|^2, a_hat = j_hat / |k|^2 (k = 0 set to 0), packed f32, with vmax;
  waves:  the 12 lowest modes (1 <= |k| <= 2.9, half plane) of the V0_libre sample-0 velocity u = grad-perp psi + grad phi
          (from its stored vorticity and divergence; real parts, normalized so the longest arrow is 1), for the Leray-projection picture.
A file is rewritten only when its content changes (the extraction date is ignored).

Usage: python3 -I tools/data_ch08.py [--repo /home/user/milady-2027] [--out data] [--check]
"""
import base64, datetime, hashlib, json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARGS = sys.argv[1:]
REPO = ARGS[ARGS.index("--repo") + 1] if "--repo" in ARGS else os.path.dirname(HERE)
OUT = ARGS[ARGS.index("--out") + 1] if "--out" in ARGS else os.path.join(HERE, "data")
CHECK = "--check" in ARGS
GEN = "tools/data_ch08.py"
SRC = "video/data/e2_maps.json"


def sha(rel):
    with open(os.path.join(REPO, rel), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def dec(p):
    return np.frombuffer(base64.b64decode(p["b64"]), dtype="<f4").reshape(p["shape"]).astype(np.float64)


def enc(a):
    a = np.asarray(a, dtype="<f4")
    return {"dtype": "f32", "shape": list(a.shape), "b64": base64.b64encode(a.tobytes()).decode()}


def build():
    m = json.load(open(os.path.join(REPO, SRC)))
    n = m["grid"][0]
    k = np.fft.fftfreq(n, 1.0 / n)
    KX, KY = np.meshgrid(k, k)            # rows = y, columns = x
    K2 = KX ** 2 + KY ** 2; K2[0, 0] = 1.0
    inv = lambda f: np.real(np.fft.ifft2(np.fft.fft2(f) / K2 * (K2 > 0.5)))
    v4 = m["variants"]["V4_potentiels"]["samples"][0]
    psi, a = inv(dec(v4["omega"])), inv(dec(v4["j"]))
    w0 = dec(m["variants"]["V0_libre"]["samples"][0]["omega"])
    d0 = dec(m["variants"]["V0_libre"]["samples"][0]["div_u"])
    ph = np.fft.fft2(w0) / K2 * (K2 > 0.5) / (n * n)               # stream function (swirl part)
    fh = -np.fft.fft2(d0) / K2 * (K2 > 0.5) / (n * n)              # potential of the slope part: laplacian(phi) = div u
    ux, uy = 1j * KY * ph + 1j * KX * fh, -1j * KX * ph + 1j * KY * fh
    waves = []
    for iy in range(n):
        for ix in range(n):
            kx, ky = k[ix], k[iy]
            r = (kx * kx + ky * ky) ** 0.5
            if 1 <= r <= 2.9 and (kx > 0 or (kx == 0 and ky > 0)):
                waves.append([float(kx), float(ky), float(ux[iy, ix].real), float(uy[iy, ix].real)])
    waves.sort(key=lambda w: (w[0] ** 2 + w[1] ** 2, w[0], w[1]))
    waves = waves[:12]
    s = max((w[2] ** 2 + w[3] ** 2) ** 0.5 for w in waves) or 1.0
    waves = [{"kx": w[0], "ky": w[1], "ux_re": round(w[2] / s, 4), "uy_re": round(w[3] / s, 4)} for w in waves]
    return {"meta": {"source": SRC, "sha256": sha(SRC), "generator": GEN, "extracted": datetime.date.today().isoformat(),
                     "stamp": "DATA · E2 · V4 hill maps, V0 waves, η = 0.00951",
                     "note": "psi, a from V4 sample-0 vorticity and current (inverse Laplacian, spectral); waves: V0 sample-0 velocity modes, normalized",
                     "sources": [{"path": SRC, "sha256": sha(SRC)}]},
            "eta": m["eta"], "grid": [n, n], "native_grid": m["native_grid"],
            "psi": enc(psi), "a": enc(a), "vmax": {"psi": round(float(np.abs(psi).max()), 5), "a": round(float(np.abs(a).max()), 5)},
            "waves": waves}


def write(name, doc):
    p = os.path.join(OUT, name)
    old = json.load(open(p)) if os.path.exists(p) else None
    st = lambda d: {**d, "meta": {k: v for k, v in d["meta"].items() if k != "extracted"}} if d else None
    if st(old) == st(doc): print(f"[data_ch08] {name}: unchanged"); return
    if CHECK: print(f"[data_ch08] {name}: WOULD CHANGE"); return
    with open(p, "w", encoding="utf-8") as f: json.dump(doc, f, ensure_ascii=False, indent=1); f.write("\n")
    print(f"[data_ch08] {name}: written")


if __name__ == "__main__":
    write("ch08_hillmap.json", build())
