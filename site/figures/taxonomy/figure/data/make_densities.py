"""ILLUSTRATIVE curves of panel b ("taxonomy" figure).

No measurement: a true Gaussian law mu with zero mean (d E/dt in units of its standard deviation),
a deliberately imperfect model q_theta (shifted mean, slightly too narrow),
and the I-projection of q_theta onto {E[dE/dt] = 0} (exponential tilting, Proposition 7),
computed numerically on the grid and on a small sample (self-normalized weights).
Usage: python make_densities.py  -> densities.json (same folder)
"""
import json, os
import numpy as np
from math import erf, sqrt

x = np.linspace(-3.2, 3.2, 321)
def gauss(x, m, s):
    return np.exp(-0.5 * ((x - m) / s) ** 2) / (s * np.sqrt(2 * np.pi))

MU_M, MU_S = 0.0, 1.0     # true law: zero mean (stationarity), spread > 0
Q_M, Q_S = 0.6, 0.85      # model before correction (illustrative choice)
mu = gauss(x, MU_M, MU_S)
q = gauss(x, Q_M, Q_S)

# I-projection on the grid: nu = exp(beta x) q / Z, beta such that E_nu[x] = 0
dx = x[1] - x[0]
def mean_tilt(b):
    w = np.exp(b * x) * q
    return (w * x).sum() / w.sum()
lo, hi = -5.0, 5.0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if mean_tilt(mid) > 0: hi = mid
    else: lo = mid
beta = 0.5 * (lo + hi)
nu = np.exp(beta * x) * q
nu /= nu.sum() * dx

# small deterministic samples (centered quantiles) for the rows of points
N = 7
p = (np.arange(1, N + 1) - 0.5) / N
def ndtri(pp):  # inverse of the Gaussian cumulative distribution function, by bisection
    out = []
    for v in pp:
        a, b = -8.0, 8.0
        for _ in range(100):
            c = 0.5 * (a + b)
            if 0.5 * (1 + erf(c / sqrt(2))) < v: a = c
            else: b = c
        out.append(0.5 * (a + b))
    return np.array(out)
z = ndtri(p)
s_mu = MU_M + MU_S * z
s_q = Q_M + Q_S * z
# self-normalized weights w_i ∝ exp(beta_s g_i) with sum w_i g_i = 0 (Proposition 7, on a sample)
lo, hi = -10.0, 10.0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    w = np.exp(mid * s_q); w /= w.sum()
    if (w * s_q).sum() > 0: hi = mid
    else: lo = mid
beta_s = 0.5 * (lo + hi)
w = np.exp(beta_s * s_q); w /= w.sum()

out = dict(
    note="Courbes illustratives (pas des mesures). Unités : dE/dt / ecart-type de mu.",
    x=x.round(4).tolist(), mu=mu.round(5).tolist(), q=q.round(5).tolist(), nu=nu.round(5).tolist(),
    mu_mean=MU_M, q_mean=Q_M, nu_mean=float((nu * x).sum() * dx), beta=beta,
    nu_sd=float(np.sqrt((nu * x * x).sum() * dx)),
    samples_mu=s_mu.round(4).tolist(), samples_q=s_q.round(4).tolist(), weights=w.round(5).tolist(),
    beta_sample=beta_s, ess=float(1 / (w ** 2).sum()),
)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'densities.json'), 'w') as f:
    json.dump(out, f)
print('beta', round(beta, 4), 'nu mean', round(out['nu_mean'], 5), 'nu sd', round(out['nu_sd'], 4),
      'beta_s', round(beta_s, 4), 'ESS', round(out['ess'], 2), 'w', w.round(3))
