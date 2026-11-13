single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H6 protocol, before the twelve points. At seed 0 the kinematic ABC growth rate changes sign in (8, 9), (17, 18) and (26, 28), at n = 64 and n = 96, and final max_div_b stays below 1e-8.

Trace. Digest table, `experiments/results/digest.md`: Rm 8 gamma -0.007649 (line 470), Rm 9 gamma 9.61e-04 (line 472), Rm 17 gamma 0.001394 (line 480), Rm 18 gamma -9.07e-04 (line 482), Rm 26 gamma -0.002578 (line 487), Rm 28 gamma 0.003897 (line 488). Interpolated thresholds on line 492 are 8.87, 17.6 and 26.8. CONFIRMED that each bracket has opposite digest signs and that the brackets were taken from that table. No H6 number exists yet.

Numerical protocol. Same integrator as H5 (dt cap 0.05, CFL 1, t = 120, float64). One seed, so a seed scatter is not claimed. Two resolutions. Divergence is an output of the script. The runs are UNCHECKED.

Verdict. UNCHECKED. The brackets match the digest. The claim is not supported until the twelve points exist.
