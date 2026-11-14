single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H131, every lambda positive at n = 128, Rm = 8.9853515625, seeds 0-4.

Recompute. Seed 0 lambda -1.1814519759945033e-05. Non-positive count 1. Largest max_div_b 5.073369469553955e-16. The GPU job was not re-run.

Verdict. REFUTED.

Claim. H132, every lambda positive at n = 128, Rm = 9.046875, seeds 5-9.

Recompute. Seed 5 lambda -5.2238142418591965e-05. Non-positive count 1. Largest max_div_b 4.162723573227285e-16. The GPU job was not re-run.

Verdict. REFUTED.

Claim. H134, seed 7 and seeds 5, 6, 8, and 9 stay positive at n = 96, Rm = 8.936634063720703125, cfl = 0.5.

Recompute. Seed 7 lambda 1.2416133187519194e-09. The cfl = 1 value is 1.2376744172460915e-09. Other seeds positive. Largest max_div_b 6.579674247421813e-16. The GPU job was not re-run.

Verdict. CONFIRMED.

Claim. H135, before n = 128 at Rm = 8.98681640625, seeds 0-4. Every lambda is positive.

Protocol check. Seed 0 is negative at Rm = 8.9853515625 and every seed is positive at Rm = 8.98828125. No file at the midpoint exists yet.

Verdict. UNCHECKED.

Claim. H136, before n = 128 at Rm = 9.0546875, seeds 5-9. Every lambda is positive.

Protocol check. Seed 5 is negative at Rm = 9.046875 and every seed is positive at Rm = 9.0625. No file at the midpoint exists yet.

Verdict. UNCHECKED.

Claim. H137, before n = 144 at Rm = 9, seeds 0-4. Every lambda is positive.

Protocol check. n = 128 at Rm = 9 is positive. No n = 144 file exists yet.

Verdict. UNCHECKED.
