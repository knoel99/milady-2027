"""X6 data (batch 4): data/X6_rm_conventions.json, a transcription of the three published VKS Rm definitions
(en/prep/p3-mhd-dynamo/index.qmd, Example 6.1, and en/rapport/index.qmd:141). No run: the printed values are
re-derived from the example's own formulas and constants and asserted against the printed output, to one decimal.
The Miralles values (54.2 / 74.5) and the 44 of P3:1167 are left out on purpose (decision D19, critique B15)."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data', 'X6_rm_conventions.json')

mu0, sigma = 4e-7 * math.pi, 9.6e6                    # P3:1178 (sodium at about 120 °C)
R_cyl, R_imp, R_o, K = 0.206, 0.1545, 0.289, 0.6      # P3:1179
rm = lambda F, r2, k=1.0: k * mu0 * sigma * 2 * math.pi * F * r2
printed = {('monchaux', 16): 30.9, ('monchaux', 22): 42.5, ('nore', 16): 51.5, ('nore', 22): 70.8}   # P3:1193-1199
for (key, F), v in printed.items():
    calc = rm(F, R_cyl ** 2, K if key == 'monchaux' else 1.0)
    assert round(calc, 1) == v, (key, F, calc, v)
ratio_mn = round(1 / K, 2)
ratio_mi = round(R_imp * R_o / R_cyl ** 2, 2)
assert ratio_mn == 1.67 and ratio_mi == 1.05

data = {
    'meta': {'source': 'en/prep/p3-mhd-dynamo/index.qmd', 'stamp': 'SITE · VKS Rm definitions (P3 Ex. 6.1)',
             'generator': 'tools/data_X6.py', 'extracted': '2026-11-08', 'how': 'transcribed; printed values re-derived from the example formulas (tools/data_X6.py), no run'},
    'F_hz': [16, 22], 'K': K, 'radii_mm': {'R_cyl': 206, 'R_imp': 154.5, 'R_o': 289},
    'defs': [
        {'key': 'monchaux', 'card': 'Monchaux et al. 2007', 'rule': 'with K ≈ 0.6', 'tex': 'K 2πF R_cyl²/η',
         'at': {'16': printed[('monchaux', 16)], '22': printed[('monchaux', 22)]},
         'threshold': {'text': 'Rm_c ≈ 31', 'value': 31}},
        {'key': 'nore', 'card': 'Nore et al. 2018', 'rule': 'without K', 'tex': '2πF R_cyl²/η',
         'at': {'16': printed[('nore', 16)], '22': printed[('nore', 22)]},
         'threshold': {'text': '52 ≤ Rm_c ≤ 71', 'lo': 52, 'hi': 71, 'note': 'dynamos seen from 16 to 22 Hz'}},
        {'key': 'miralles', 'card': 'Miralles et al. 2013', 'rule': 'other radii', 'tex': '2πF R_imp R_o/η',
         'at': None, 'threshold': None, 'ratio_to_nore': ratio_mi},
    ],
    'ratios': {'nore_over_monchaux': ratio_mn, 'miralles_over_nore': ratio_mi},
}
with open(OUT, 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print('wrote', os.path.relpath(OUT))
