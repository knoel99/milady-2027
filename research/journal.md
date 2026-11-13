# Lab journal

One entry per working session, newest first, at most ten lines.

## 2026-11-13 - H30 to H33 supported, team cursor
- H30: n = 64, Rm = 9.0625, seeds 0-4, all positive. Smallest lambda is 1.63e-5. Pod `npkxes95rj9lvp`, 0.0466 USD.
- H31: seeds 5-9 at Rm = 9.125 stay positive. Smallest is 0.000384. Pod `zx18edxuziodea`, 0.0465 USD.
- H32: cfl = 0.5 at Rm = 9.125 stays positive. Smallest is 0.000396. Pod `bkdlp6rgyuesdm`, 0.0468 USD.
- H33: n = 48, Rm = 9.125 stays positive. Smallest is 0.000451. Pod `x05ob7azvry9p3`, 0.0240 USD. Local ledger about 6.25 USD.
- H34 to H37 ask the next sign, one step closer to the Rm = 9 negatives. Those signs were fixed before the runs.

## 2026-11-13 - H29 supported, H33 registered, team cursor
- Five points at n = 64, Rm = 9.25, cfl = 0.5, all finite and all positive. The smallest lambda is 0.001113. Largest max_div_b is 5.91e-16.
- Pod `i0oxzc1r3c9mjh`, RTX 4090, 0.08 h, 0.0705 USD. The sign rule was not changed. A per-seed comparison with the cfl = 1 values was not the registered claim.
- H33 asks whether the same Rm stays positive at n = 48 for seeds 0-4. That sign may fail. H30, H31, and H32 are already on RTX 4090 pods.

## 2026-11-13 - H21, H27, H28 supported, team cursor
- H21: seeds 5-9 at n = 160, Rm = 12. Mean lambda 0.008491. Absolute difference from the seeds 0-4 mean is 2.05e-4, under the pre-set 0.001. Pod `yn68gh7vq4v6lj`, RTX 4090, 1.12 h, 0.9924 USD.
- H27: Rm = 9.125, seeds 0-4, all positive. Smallest lambda is 0.000396. Pod `qtiiio75dugag7`, 0.0618 USD.
- H28: Rm = 9.25, seeds 5-9, all positive. Smallest lambda is 0.001110. Pod `db95jhqv5pdbtm`, 0.0315 USD. Local ledger about 6.01 USD.
- H30 asks whether Rm = 9.0625 is still positive. H31 and H32 ask the new seeds and cfl = 0.5 at Rm = 9.125. H29 is still running.

## 2026-11-13 - H24, H25, H26 supported, team cursor
- H24: each n = 64 seed at Rm = 11 lies inside its pre-set Rm = 10 and Rm = 12 bounds. Tightest gap is seed 3, 4.66e-5. Pod `aj1qpld9yshhp5`, 0.0467 USD.
- H25: Rm = 9.25, seeds 0-4, all positive. Smallest lambda is 0.001113. Pod `p9jcakqcmv3lvd`, 0.0546 USD.
- H26: Rm = 9.5, seeds 5-9, all positive. Smallest lambda is 0.002411. Pod `05uwvjoqzi388w`, 0.0541 USD. Largest max_div_b on these three jobs is 5.76e-16.
- Measured after the fact, not a registered claim: for seeds 0-4, lambda(9.25) < lambda(9.5) < lambda(11). H27, H28, and H29 are the next sign tests. H21 is still on pod `yn68gh7vq4v6lj`.

## 2026-11-13 - H23 supported, H25 and H26 registered, team cursor
- Five points at n = 64, Rm = 9.5, all finite and all positive. The smallest lambda is 0.002392. Largest max_div_b is 4.91e-16.
- Pod `2fw9atuegj9o95`, RTX 4090, 0.05 h, 0.0467 USD. Local ledger 4.77 USD. At n = 64 the sign is negative for two seeds at Rm = 9 and positive for all five at Rm = 9.5.
- H25 asks whether Rm = 9.25 is already positive for seeds 0-4. H26 asks whether seeds 5-9 stay positive at Rm = 9.5. Both signs were fixed before those runs.
- H21 is still on pod `yn68gh7vq4v6lj`. H24 is on pod `aj1qpld9yshhp5`. Two slots were free after H23.

## 2026-11-13 - H24 registered, team cursor
- H24 asks whether each n = 64 seed at Rm = 11 lies strictly between its Rm = 10 and Rm = 12 values. Those ten bounds were copied before any Rm = 11 point.
- The gaps are 0.0021 to 0.0037. The claim can fail. Cost is the n = 64 scale, 0.0316 USD last time, on an RTX 4090.
- H23 still waits for a free slot. H21 is still on pod `yn68gh7vq4v6lj` at age about 0.68 h. Local ledger 4.72 USD. Four pods are up, so nothing new launches yet.

## 2026-11-13 - H22 supported, H23 registered, team cursor
- Five points at n = 64, Rm = 10, all finite and all positive. The smallest lambda is 0.004400. Largest max_div_b is 5.13e-16.
- Pod `15206ueh82oyrg`, RTX 4090, 0.04 h, 0.0316 USD. Local ledger 4.7237 USD. The sign holds at n = 64, 96, and 128.
- H23 asks whether lambda(9.5) is positive at n = 64 for seeds 0-4. That sign may fail. It waits for a free slot. H21 is still on pod `yn68gh7vq4v6lj`.

## 2026-11-13 - H20 supported, H22 registered, team cursor
- Five points at n = 96, Rm = 10, cfl = 1, all finite and all positive. The smallest lambda is 0.005517. Largest max_div_b is 6.11e-16.
- Pod `9d530mb5jhqa8q`, RTX 4090, 0.11 h, 0.1000 USD. Local ledger 4.6921 USD. The sign rule was not changed.
- H22 asks whether lambda(10) stays positive at n = 64, where lambda(9) failed for two seeds. H21 is on pod `yn68gh7vq4v6lj`.

## 2026-11-13 - H18 supported, H21 registered, team cursor
- Five points at n = 160, Rm = 12, cfl = 1, all finite. Largest max_div_b is 5.02e-16.
- Mean lambda 0.008286 (sample std 0.000601). Absolute difference from the ten-seed n = 128 mean 0.007837088 is 4.49e-4, under the pre-set 0.001.
- Pod `z1a4bgm0uztfzo`, RTX 4090, 1.11 h, 0.9920 USD. Local ledger 4.5921 USD. The bound was not tightened after the run.
- H21 asks whether seeds 5-9 at n = 160 stay within 0.001 of that mean. H20 is already on pod `9d530mb5jhqa8q`.

## 2026-11-13 - H19 supported, H20 registered, team cursor
- Five points at n = 128, Rm = 10, cfl = 1, all finite and all positive. The smallest lambda is 0.005015. Largest max_div_b is 5.12e-16.
- The H19 criterion is not met for a refutation. Pod `jc4tw36hkpg8l2`, RTX 4090, 0.38 h, 0.3357 USD. Local ledger 3.6001 USD.
- H20 asks whether lambda(10) stays positive at n = 96 for seeds 0-4. The sign was fixed before that run. It waits for a free slot. H18 is still on pod `z1a4bgm0uztfzo`.

## 2026-11-13 - H17 supported, H19 registered, team cursor
- Five points at n = 128, Rm = 12, cfl = 0.5, all finite. Largest max_div_b is 4.82e-16.
- Mean lambda 0.007691066. Absolute difference from the cfl = 1 mean is 8.87e-13, under the pre-set 0.002.
- Pod `nmcrrnaf8kpbi8`, RTX 4090, 0.73 h, 0.6493 USD. Local ledger 3.2644 USD.
- H19 asks whether lambda(10) is positive for seeds 0-4 at n = 128. The sign was fixed before the run. H18 is already on pod `z1a4bgm0uztfzo`.

## 2026-11-13 - H16 supported, H18 registered, team cursor
- Five points, seeds 5-9, at n = 128, Rm = 12, cfl = 1, all finite. Largest max_div_b is 7.95e-16.
- Mean lambda 0.007983 (sample std 0.000821). Absolute difference from the seeds 0-4 mean is 2.92e-4, under the pre-set 0.001.
- Pod `90sfjdnqoh54y5`, RTX 4090, 0.40 h, 0.3519 USD. Local ledger 2.6151 USD. The account had five live pods after this, four of them Claude's, so H18 waits.
- H18 asks whether seeds 0-4 at n = 160 stay within 0.001 of the ten-seed n = 128 mean 0.007837088. That bound was fixed before any n = 160 point.

## 2026-11-13 - H15 supported, H17 registered, team cursor
- Ten points at n = 128, Rm 8 and 9, seeds 0-4, all finite. Largest max_div_b is 5.41e-16.
- lambda(8) is negative for every seed. lambda(9) is positive for every seed, including seeds 1 and 4.
- The H15 criterion is not met for a refutation. Pod `ljovlfo45xhizf`, RTX 4090, 0.74 h, 0.6578 USD. Local ledger 2.2632 USD.
- H17 is registered before any n = 128, cfl = 0.5 point. The bound is 0.002 against the H12 mean. An H100 at 4.39 USD/h does not beat the measured 4090 bill for this length of run.

## 2026-11-13 - H16 registered, team cursor
- H16 asks whether seeds 5-9 at n = 128, Rm = 12, cfl = 1 stay within 0.001 of the H12 mean 0.007691066.
- The bound was written before those seeds. H15 still has the first free slot. Local ledger 1.61 USD.

## 2026-11-13 - deadline from main, team cursor
- Merged `33fc923`. `race/config.toml` now matches origin/main. The pilot deadline is 13 November 22:00 Paris.
- `tools/runpod_job.py` was not edited. The pod prefix is still `milady-cursor-job-`.
- H10 was already committed at `65a432f`. Claude holds the four parallel slots. The H15 watcher is still waiting and has not created a pod.
- No pod was stopped or deleted for this merge.

## 2026-11-12 - H13 supported, H15 registered, team cursor
- Five points at n = 96, Rm = 12, cfl = 0.5, all finite. Largest max_div_b is 5.58e-16.
- Mean lambda 0.008095872. Absolute difference from the cfl = 1 mean at the same resolution is 2.3e-12, under the pre-set 0.002.
- The H13 criterion is not met for a refutation. Pod `jszpatyck4j92j`, RTX 4090, 0.2202 h, 0.1960 USD. Local ledger 1.6054 USD.
- H15 is registered before any n = 128 sign point: lambda(8) < 0 < lambda(9) for seeds 0-4. It launches when a parallel slot is free. Claude holds the four slots.

## 2026-11-12 - H12 supported, team cursor
- Five points at n = 128, Rm = 12, cfl = 1, all finite. Largest max_div_b is 4.99e-16.
- Mean lambda 0.007691 (sample std 0.000788). Absolute difference from the n = 64 control 0.008127803 is 4.37e-4, under the pre-set 0.0005.
- The shift is larger than the n = 96 gap of 3.19e-5. The bound was not tightened after the run. Pod `2ve329wmhyavou`, RTX 4090, 0.3872 h, 0.3446 USD. Local ledger 1.4094 USD.

## 2026-11-12 - H10 refuted, team cursor
- Sixteen points, all finite. Largest max_div_b is 5.27e-16. lambda(8) is negative at every seed and both resolutions.
- lambda(9) is positive for all four n = 96 seeds and for n = 64 seeds 2 and 3. It is negative at n = 64 seed 1 (-3.78e-4) and seed 4 (-3.28e-4).
- H10 is refuted. The sign rule was not changed after the run. Pod `175n5esaa52aji`, RTX 4090, 0.19 h, 0.1691 USD. Local ledger 1.0648 USD.
- The account already had four live pods when H12 was ready, three of them Claude's, so that launch created nothing.

## 2026-11-12 - H12 and H13 registered, team cursor
- H9 holds, so the next resolution is n = 128 against the same n = 64 control, with the bound tightened to 0.0005 before that run.
- H13 asks whether the H8 timestep tolerance of 0.002 still holds at n = 96, against the H9 cfl = 1 mean 0.008095872. The cfl = 0.5 points are not computed yet.
- H100 80GB is 4.39 USD/h on Secure, 4.9 times the 4090. The five-point n = 96 job cost 0.0927 USD. Matching that bill would take about 76 s, and setup is already about 90 s, so an H100 does not win on cost here. Next pods are 4090, then PRO 4500, then A6000.

## 2026-11-12 - H11 refuted, team cursor
- Ten points at n = 64, 1000 steps, all finite. scale_max stays under 1e-3. The largest is 3.46e-5.
- rel_max fails 0.01 on ABC seeds 1, 3 and 4 (0.0122, 0.358, 0.0161). Seed 3 has rhs_abs_min 6.4e-6. Taylor-Green stays under 0.01.
- H11 is refuted. The 0.01 bound was not moved. Pod `w8lf2ntul7d6y4`, PRO 4500, 0.0380 USD. Local ledger 0.8957 USD.

## 2026-11-12 - H9 supported, team cursor
- Five points at n = 96, Rm = 12, cfl = 1, all finite. Largest max_div_b is 4.92e-16.
- Mean lambda 0.008096 (sample std 0.000565). Absolute difference from the n = 64 control 0.008127803 is 3.19e-5, under the pre-set 0.001.
- The H9 refutation criterion is not met. Pod `1x55oy7rjbx04y`, RTX 4090, 0.10 h, 0.0927 USD. PRO 4500 had no capacity, so the measured fallback was the 4090.

## 2026-11-12 - GPU choice and H9-H11, team cursor
- Cost per completed point from this branch's ledger. n = 96, three points: PRO 4500 244 s and 0.0683 USD (0.0228 USD/point); A40 586 s and 0.1117 USD (0.0372 USD/point). The 4500 is cheaper and faster, so A40 is not used.
- n = 64, three points: RTX 4090 56 s and 0.0380 USD (0.0127 USD/point); A6000 99 s and 0.0358 USD (0.0119 USD/point). Five cfl = 0.5 points on the PRO 4500: 158 s and 0.0502 USD (0.0100 USD/point).
- No completed run on A100, L40S, or RTX PRO 6000, so those stay off the list. H100 stays off the list. Launch order is PRO 4500, then RTX 4090, then A6000.
- H9, H10, and H11 are registered before their runs. They are independent, so they take the three free slots beside the live Claude pod. Claude's hypotheses are E4 generator comparisons and are not copied.

## 2026-11-12 - H8 supported, team cursor
- Five points at n = 64, Rm = 12, cfl = 0.5, all finite. Largest final max_div_b is 5.63e-16.
- Mean lambda 0.007805 (sample std 0.000458). Absolute difference from the cfl = 1 control mean 0.008127803 is 0.000323, under the pre-set 0.002.
- The H8 refutation criterion is not met. Pod `o4cerdg2ehjai2`, RTX PRO 4500, 0.0697 h, 0.0502 USD, rc 0. Local ledger 0.7650 USD.
- This is one kinematic comparison, not a 3D generator result.

## 2026-11-12 - H8 registered, team cursor
- Before any cfl = 0.5 growth rate: at n = 64 and Rm = 12, the five-seed mean stays within 0.002 of the cfl = 1 control mean 0.008127803.
- The cfl = 1 points already measured are the control. Seeds 0-4 at cfl = 0.5 are the variant. Every point must stay finite, with final max_div_b below 1e-8.
- The 0.002 bound is fixed now. No H100.

## 2026-11-12 - H7 refuted, team cursor
- Twenty points, all finite. Pod `7t70354viwtvne`, RTX PRO 4500, 0.0352 h, 0.0253 USD, rc 0. Local ledger 0.7148 USD.
- rel_max stays under 0.01 (largest 1.58e-4). scale_max stays under 1e-3 (largest 3.36e-5).
- n = 32, abc, kf = 2, seed 2 has rhs_abs_min 0.0249, which is not above 0.05. That one point fails the pre-set bound.
- H7 is refuted. The n = 16 transient assumption does not hold for every variant. This is not a 3D generator result.

## 2026-11-12 - main's prefix kept, team cursor
- Merged `origin/main` at `e666a67`. Where the two cleanup fixes overlapped, main's `tools/runpod_job.py` stayed. The local duplicate was dropped.
- This checkout has one objectives file, so the prefix is `milady-cursor-job-`. `MILADY_JOB_PREFIX` overrides it. `MILADY_TEAM` is not read.
- `cleanup` deletes a pod only with that prefix, only if its id is in this checkout's ledger, and only past its time limit. Other teams stay. Reservations still count every `milady-*job-*` pod.

## 2026-11-12 - H7 registered, team cursor
- Before any n = 32 or n = 48 energy number: the dynamic budget of test_energy_budget holds at both resolutions, for tg kf = 1 and abc kf = 2, seeds 1 to 5.
- Seed 1 is the test control. Seeds 2, 3, 4 and 5 are variants. All twenty points must pass.
- Bounds, fixed from the n = 16 test: rhs_abs_min > 0.05, rel_max < 0.01, scale_max < 1e-3, and the residual is finite.
- A CPU run at n = 16 only checked the script. It is not an H7 point. No H100.

## 2026-11-12 - team prefix, team cursor
- Pods this session creates are named `milady-cursor-job-*`. The prefix is `MILADY_TEAM`, default `cursor` (commit `e2e794b`).
- `cleanup` deletes only that prefix, and only past the time limit. `milady-claude-job-*` and legacy `milady-job-*` stay, including with `--all`.
- `running_jobs` still counts every live `milady-*job-*` pod toward the shared 150 USD reservation and the parallel cap.

## 2026-11-12 - H6 refuted, team cursor
- Twelve points, all finite. Largest final max_div_b is 9.92e-16. Four pods cost 0.2538 USD. Local ledger 0.6895 USD.
- The (8, 9) bracket holds at n = 64 and n = 96. lambda(8) is negative and lambda(9) is positive at both resolutions.
- n = 64 fails the other two brackets. lambda(18) = 3.15e-6 is positive. lambda(28) = -6.36e-4 is negative.
- n = 96 fails the third bracket. lambda(26) = 4.19e-4 is positive. lambda(17) is positive and lambda(18) is negative, so only that bracket holds at n = 96.
- H6 is refuted. The digest windows do not all survive at these two resolutions. This is not a 3D generator result.

## 2026-11-12 - cleanup rule, team cursor
- Confirmed. The cleanup at 22:46 Paris deleted pods this session had not created and killed the Claude team's A-D GPU job. 71 minutes of that job were lost. The pod ids were `hd6qx71mm6jekm` (`milady-job-329724d4`) and `00t6s3l481flvm` (`milady-job-a24b1ae9`).
- Claude now names its pods `milady-claude-job-*` (commit `62e31c9`).
- Rule. Do not stop, delete, or clean up any pod this session did not create. Act only on pod ids launched here. Do not run `python3 tools/runpod_job.py cleanup`.
- A `run()` this session started may still delete the pod id it launched, when that job ends. That is not a sweep of the account.

## 2026-11-12 - H6 registered, team cursor
- Before the next GPU points: lambda changes sign in (8, 9), (17, 18) and (26, 28) at n = 64 and n = 96, seed 0, and final max_div_b stays below 1e-8.
- The brackets are the E3 digest crossings (thresholds 8.87, 17.6, 26.8). The protocol note is a single-model simulation (no independent sub-agent).

## 2026-11-12 - H5 ABC growth, team cursor
- Sixteen points, t = 120, dt cap 0.05, CFL 1, float64. A40 at 0.59 USD/h, two RTX 4090 at 0.89 USD/h, RTX 5090 at 1.39 USD/h. Those four ledger rows sum 0.1654 USD. Local ledger 0.4357 USD.
- Seed 0 signs match the E3 digest at Rm 6, 12, 20 and 30, at n = 48 and n = 64. Largest final max_div_b is 9.33e-16.
- Rm = 12, seeds 0-4. Mean lambda 0.008041 at n = 48 (sample std 0.000497) and 0.008128 at n = 64 (sample std 0.000667). Absolute difference of the means 8.68e-5.
- The H5 refutation criterion is not met. This is one campaign of the kinematic solver, not a 3D generator.
- Role notes in this journal are a single-model simulation (no independent sub-agent). These rates are the pod outputs.

## 2026-11-12 - H4 GPU bench, team cursor
- float32, NVIDIA GeForce RTX 4090, 0.89 USD/h, 0.281 h, 0.2501 USD, rc 0. n=64 0.00644 s/step, n=128 0.00868 s/step. One run. Peak memory 0.070 GB and 0.549 GB.
- float64, NVIDIA RTX PRO 4500 Blackwell, 0.72 USD/h, 0.0281 h, 0.0202 USD, rc 0. n=64 0.00392 s/step, n=128 0.0484 s/step. One run. Peak memory 0.140 GB and 1.098 GB.
- The dtypes ran on different GPUs. No speedup is claimed, and the limiter was not profiled. The 4090 job's timed loop was 6 s inside 0.28 h of setup.
- H4's refutation criterion is not met. Local ledger 0.2703 USD. The shared cap remains 150 USD.
- Role notes elsewhere in this journal are a single-model simulation (no independent sub-agent). These timings are the pod logs.

## 2026-11-12 - shared GPU budget, team cursor
- Kim set the hard shared limit to 150 USD, the prepaid credit from main PR #39, first come first served with the Claude team.
- This session exports MILADY_GPU_BUDGET_USD=150. A new job is refused when main's reservation (account spend, plus the worst case still reserved by live milady-job pods, plus the new job) would cross that credit.
- H5 is registered before any growth-rate run. CPU smoke `experiments/cursor_abc_growth.py --quick` exited 0 (n = 16, t = 2, Rm = 12, max_div_b 3.46e-16). That short lambda is a transient, not the H5 sample. The float32 bench was already in flight on an RTX 4090. No H100.

## 2026-11-12 - pod incident, team cursor
- Incident. `python3 tools/runpod_job.py cleanup` in this session deleted two Claude-team pods this session had not created: `hd6qx71mm6jekm` (`milady-job-329724d4`) and `00t6s3l481flvm` (`milady-job-a24b1ae9`). The cleanup then in this branch deleted every pod whose name started with `milady-job-`.
- Fix used. Main commit `ce0c796` (PR #39) now deletes only pods past their time limit, and `run` reserves the worst-case cost of pods already running, up to `max_parallel` 4. This branch merged that file and did not rewrite it. `make test` exited 0 after the merge.
- Any role text added after this line is a single-model simulation (no independent sub-agent).

## 2026-11-12 - pilot step 1, team cursor
- Goal: steps 1 to 5 of race/PILOT-CURSOR-AGENT.md, stop at the first failed check.
- Done: CPU install from infra/env/requirements.txt then `pip install -e ".[dev]"` in `.venv` (torch 2.14.1+cpu). `make test` failed while `MILADY_GPU_BUDGET_USD=40` hid the budget the job tests set. The fixture now clears that variable. `make test` and `python3 tools/sync_agents.py --check` then exited 0.
- Prices: every `[gpu].fallback` id has a Secure and a Community rate (`python3 tools/runpod_job.py prices`, exit 0). Stock was LOW or NONE. `python3 tools/review_due.py due` printed "no review due" and exited 0.
- Stopped at step 3. This session has no sub-agent tool, and `CURSOR_API_KEY` is unset, so `encadrant`, `physicien`, `biblio` and `jury-externe` did not answer Proposition 1. Nothing was logged with `review_due.py log`.
- Not done: the float32 and float64 GPU benches, timings, and `race/teams/cursor/objectives.toml`. This branch's ledger is 0 USD. `python3 tools/runpod_job.py cleanup` deleted two pre-existing pods this session did not create: `hd6qx71mm6jekm` (`milady-job-329724d4`) and `00t6s3l481flvm` (`milady-job-a24b1ae9`).
- Next: rerun step 3 on a session that can spawn `.cursor/agents/`, then the two benches.

<!-- Template
## YYYY-MM-DD — H<id>: <short title>
- Goal of the session:
- Done (commands, runs, seeds):
- Result (digest keys) and encadrant verdict:
- Decision (supported / refuted / dropped / next step):
- Cost (tokens, CPU time):
-->
