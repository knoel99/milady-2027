# Lab journal

One entry per working session, newest first, at most ten lines.

## 2026-11-13 - H168 registered, team cursor
- A normalized ResMLP probe, one seed, not quoted, reached C1 4.35. The five-seed GPU run is registered and not yet started.
- The report source stays site/teams/cursor/report/index.qmd. No separate tex file.

## 2026-11-13 - H167 supported, team cursor
- The kmax=7 midpoint meets the null-count bound. Mean relative error 0.08397, at most 0.1.
- C5 now quotes that error. The coarser counts stay recorded as misses.

## 2026-11-13 - H166 refuted, team cursor
- The kmax=6 midpoint misses the null-count bound. Mean relative error 0.172, above 0.1.
- H167, the same comparison at kmax=7, is registered and not yet run.

## 2026-11-13 - H165 refuted, team cursor
- The kmax=6 truncation still moves the null count. Mean relative error 0.160, above 0.1.
- Two truncation widths missed 0.1, so that comparison is dropped.
- H166, the midpoint against the held-out field, is registered and not yet run.

## 2026-11-13 - H164 refuted, team cursor
- The kmax=4 truncation changes the trilinear null count. Mean relative error 0.428, above 0.1.
- C5 now quotes that error. C7 is 2 after src/milady/eval/nulls.py.
- The five seed pairs are in experiments/results/cursor_nulls.json.

## 2026-11-13 - H144 refuted, team cursor
- At n=128, Rm=8.98699951171875, seed 0 is negative, lambda -7.53e-7. Pod `6igk1bsvmdnkow`, 0.39 h, 0.3446 USD.
- The seeds 0-4 bracket is now between this Rm and 8.9871826171875. It is not bisected.
- No team pod is left running.

## 2026-11-13 - H162 supported, H163 refuted, team cursor
- The second-half total energy balance of the dynamic ABC run has mean absolute residual 3.74e-6. H162 holds. C3 now quotes that number.
- The magnetic residual on the same window has mean 0.067. H163 is refuted.
- n=16, t=8, five seeds, CPU. H144 stays in flight.

## 2026-11-13 - H161 refuted, team cursor
- The kmax=7 midpoint has mean C3 0.085, above 0.05 and not below the kmax=6 value 0.083.
- The cutoff is not the lever for the balance residual on this n=16 grid. cursor_metrics.json stays on kmax=6.
- H144 stays in flight. Spend stays 21.56 USD.

## 2026-11-13 - H158 and H159 supported, H160 refuted, team cursor
- The kmax=6 midpoint has mean C4 0.0093, below 0.150 and below 0.1. H158 and H159 hold.
- Mean C3 is 0.083, above 0.05. H160 is refuted. C1 on this map is 0.014.
- cursor_metrics.json now quotes the kmax=6 midpoint. C5 stays the sentinel. H144 stays in flight.

## 2026-11-13 - H138 supported, team cursor
- At n=160, Rm=9.0625, seeds 0-4, every lambda is positive. Smallest is seed 3, 5.84e-5. Pod `g0w33xugwvc37o`, 1.12 h, 1.00 USD.
- n=160 at Rm=9 was negative. The bracket is (9, 9.0625). It is not bisected.
- H144 stays in flight. The quoted generator metrics are the kmax=4 midpoint, not this run.

## 2026-11-13 - H156 and H157 supported, team cursor
- The kmax=4 midpoint between Rm=11 and Rm=13 has mean energy-distance ratio 0.743. H156 and H157 hold.
- cursor_metrics.json now quotes that midpoint. C1 and C2 meet their targets. C3 is 0.099 and C4 is 0.150.
- Seed 0 alone is 1.80. The criterion was the mean. The flow-matching ratios stay near 750. H138 and H144 stay in flight.

## 2026-11-13 - H154 supported, H155 refuted, team cursor
- Training on six Rm values around 12 lowers the ratio from 787.34 to 781.66. H154 holds. The gap is about 5.7.
- H155 is refuted. 781.66 is above 1.2. The perfect kmax=4 cutoff remains 0.728.
- The next comparison is linear interpolation between Rm=11 and Rm=13, not more flow steps. H138 and H144 stay in flight.

## 2026-11-13 - projection ceiling under 1.2, team cursor
- A perfect cutoff at kmax=4 has mean energy-distance ratio 0.728. kmax=6 is 0.0092. kmax=7 is 0.0028. H151, H152, and H153 hold.
- The learned flows stay near 750. The cutoff is not what misses C1. The learner is.
- The next comparison trains on Rm values around 12 and still holds 12 out. H138 and H144 stay in flight.

## 2026-11-13 - H149 supported, H150 refuted, team cursor
- Hidden width 768 at kmax=4 lowers the ratio from 791.02 to 787.34. H149 holds. The gap is about 3.7.
- H150 is refuted. 787.34 is above 1.2. The metrics file stays on the kmax=2 ratio, 757.56.
- The next measurement is the projection ceiling, not another learned width. H138 and H144 stay in flight.

## 2026-11-13 - H147 and H148 refuted, team cursor
- Raising kmax from 2 to 4, with hidden width 64, raises the energy-distance ratio from 757.56 to 791.02.
- Both H147 and H148 are refuted. The extra modes did not help through a width-64 layer.
- C1 stays the kmax=2 measurement. The next comparison changes the width, not Rm.
- H138 and H144 stay in flight. Spend about 20.56 USD.

## 2026-11-13 - H145 supported, H146 refuted, team cursor
- The sampling constraint mean maximum divergence is 1.56e-8. The free baseline is 0.645. H145 holds.
- The same variant has energy-distance ratio 757.56, above 1.2. H146 is refuted. CPU, no pod.
- C1, C3, and C4 are now measured and far from their targets. C5 stays the sentinel. C2 is 2.20e-8.
- H138 and H144 stay in flight. The next comparison has to change the model.

## 2026-11-13 - H143 refuted, team cursor
- At n = 128, Rm = 9.056640625, seeds 5-9, seed 9 is negative, lambda -5.35e-6. Pod `09sisn0uy6qnop`, PRO 4500, 0.51 h, 0.365 USD.
- The seeds 5-9 bracket is now between 9.0546875 and 9.056640625. It is not bisected while C1-C5 are the sentinel.
- H138 and H144 stay in flight. H145 and H146, the constraint comparison, are registered and not yet run.

## 2026-11-13 - H141 refuted, next step leaves the Rm split, team cursor
- At n = 136, Rm = 9, seeds 2 and 4 are negative. Most negative is -3.97e-4, seed 2. Pod `v8ijpyib68z0fq`, 0.56 h, 0.4966 USD.
- n = 128 is positive at this Rm. The resolution bracket stays open. The free slot is not used for n = 132.
- C1 to C5 are still the sentinel. The next job compares two constraint mechanisms and writes cursor_metrics.json. H138, H143, and H144 stay in flight. Local ledger about 20.20 USD.

## 2026-11-13 - H142 supported, team cursor
- At n = 128, Rm = 8.9871826171875, seeds 0-4 are all positive. Smallest is 4.76e-7, seed 0. Pod `wz78fngpuvhk0y`, 0.38 h, 0.3416 USD.
- H144 asks Rm = 8.98699951171875. H138, H141, and H143 stay in flight. Local ledger about 19.70 USD.

## 2026-11-13 - H143 fell through to an RTX PRO 4500, team cursor
- Secure RTX 4090 capacity was empty. Pod `09sisn0uy6qnop` is an RTX PRO 4500 at 0.72 USD/h. H142 stayed on an RTX 4090. H138 and H141 stay in flight.

## 2026-11-13 - H139 and H140 supported, team cursor
- At n = 128, Rm = 8.987548828125, seeds 0-4 are all positive. Smallest is 2.93e-6, seed 0. Pod `5vazrnsmf3z5dw`, 0.38 h, 0.3366 USD.
- At n = 128, Rm = 9.05859375, seeds 5-9 are all positive. Smallest is 2.24e-5, seed 5. Pod `rmgfzfvfk1cg5n`, 0.38 h, 0.3371 USD.
- H142 asks Rm = 8.9871826171875. H143 asks Rm = 9.056640625. H138 and H141 stay in flight. Local ledger about 19.36 USD.

## 2026-11-13 - H137 refuted, arguments with spaces checked, team cursor
- At n = 144, Rm = 9, seed 3 is negative, lambda -3.59e-4. Pod `8srkxbqud65eqi`, 0.66 h, 0.5883 USD.
- n = 128 is positive at this Rm. H141 asks n = 136. Merged main `a34e8f3`. No cursor job passed an argument with a space after `--`. H138, H139, and H140 stay in flight. Local ledger about 18.68 USD.

## 2026-11-13 - H128, H135, and H136 refuted, team cursor
- At n = 160, Rm = 9, seeds 1 and 3 are negative. Most negative is -3.45e-4, seed 3. Pod `6gasccypas5tfc`, 1.11 h, 0.992 USD.
- At n = 128, Rm = 8.98681640625, seed 0 is negative, lambda -1.98e-6. Pod `8syrkj8xbo0u5q`, 0.39 h, 0.3442 USD.
- At n = 128, Rm = 9.0546875, seed 5 is negative, lambda -2.45e-6. Pod `k0g1m78qtpx10i`, 0.39 h, 0.3438 USD.
- H138 asks n = 160 at Rm = 9.0625. H139 asks Rm = 8.987548828125. H140 asks Rm = 9.05859375. H137 stays in flight. Local ledger about 18.10 USD.

## 2026-11-13 - H131 and H132 refuted, H134 supported, seeds 5-9 stop holds, team cursor
- At n = 128, Rm = 8.9853515625, seed 0 is negative, lambda -1.18e-5. Pod `slc2wdm73ih5e5`, 0.39 h, 0.3452 USD.
- At n = 128, Rm = 9.046875, seed 5 is negative, lambda -5.22e-5. Pod `dlfdpzntb9mo5f`, 0.39 h, 0.351 USD.
- At n = 96, Rm = 8.936634063720703125, cfl = 0.5, seed 7 stays positive, lambda 1.24e-9. The cfl = 1 value is 1.24e-9. The seeds 5-9 stop holds. Pod `6upk12yyka52m8`, 0.20 h, 0.1766 USD.
- H135 asks Rm = 8.98681640625. H136 asks Rm = 9.0546875. H137 asks n = 144 at Rm = 9. H128 stays in flight. Local ledger about 16.42 USD.

## 2026-11-13 - H133 refuted, seeds 5-9 split stops, H134 registered, team cursor
- At n = 96, Rm = 8.9366283416748046875, seed 7 is negative, lambda -3.87e-8. Pod `uux321o5twqwxt`, 0.12 h, 0.1077 USD.
- The next Rm is positive at 1.24e-9. The cfl = 1 split for seeds 5-9 stops. H134 repeats that positive point at cfl = 0.5. H128, H131, and H132 stay in flight. Local ledger about 15.54 USD.

## 2026-11-13 - H130 supported, H133 registered, team cursor
- At n = 96, Rm = 8.936634063720703125, seeds 5-9 are all positive. Smallest is 1.24e-9, seed 7. Pod `yap81mxhdtxo6a`, 0.12 h, 0.1078 USD.
- The negative neighbour is -7.87e-8. H133 asks the midpoint Rm = 8.9366283416748046875. H128, H131, and H132 stay in flight. Local ledger about 15.44 USD.

## 2026-11-13 - H125 and H126 refuted, H131 and H132 registered, team cursor
- At n = 128, Rm = 8.982421875, seed 0 is negative, lambda -3.15e-5. Pod `qbj624lrtfp2lr`, 0.38 h, 0.3368 USD.
- At n = 128, Rm = 9.03125, seeds 5 and 9 are negative. Most negative is -1.52e-4. Pod `b5kd8vkys86m6n`, 0.39 h, 0.3442 USD.
- H131 asks Rm = 8.9853515625. H132 asks Rm = 9.046875. H128 and H130 stay in flight. Local ledger about 15.33 USD.

## 2026-11-13 - H129 refuted, H130 registered, team cursor
- At n = 96, Rm = 8.93662261962890625, seed 7 is negative, lambda -7.87e-8. The positive neighbour is +8.11e-8. Pod `ik9xvtteuwatn4`, 0.12 h, 0.1077 USD.
- H130 asks the midpoint Rm = 8.936634063720703125. H125, H126, and H128 stay in flight. Local ledger about 14.65 USD.

## 2026-11-13 - H127 refuted, H129 registered, team cursor
- At n = 96, Rm = 8.9365997314453125, seed 7 is negative, lambda -2.38e-7. Pod `hdrkv57tilzo53`, RTX 4090, 0.10 h, 0.0925 USD.
- H129 asks the midpoint Rm = 8.93662261962890625. Merged main `fd76483`. The pilot has no deadline. The GPU budget is the stop. H125, H126, and H128 stay in flight. Local ledger about 14.54 USD.

## 2026-11-13 - H124 supported, seeds 0-4 stop holds, H128 registered, team cursor
- At n = 96, Rm = 8.8983001708984375, cfl = 0.5, seed 3 stays negative, lambda -3.04e-9. The cfl = 1 value is -3.04e-9. Pod `vr9keepc5ltdsf`, 0.20 h, 0.1767 USD.
- The cfl = 1 split for seeds 0-4 stays stopped. H128 asks n = 160 at Rm = 9, where n = 128 is positive. H125, H126, and H127 stay in flight. Local ledger about 14.45 USD.

## 2026-11-13 - H117 and H118 supported, H123 refuted, team cursor
- At n = 128, Rm = 8.98828125, seeds 0-4 are all positive. Smallest is 7.84e-6, seed 0. Pod `w17y435xtrpz8t`, 0.39 h, 0.3435 USD.
- At n = 128, Rm = 9.0625, seeds 5-9 are all positive. Smallest is 4.71e-5, seed 5. Pod `r5tg8rha7ptjq1`, 0.38 h, 0.3364 USD.
- At n = 96, Rm = 8.936553955078125, seed 7 is negative, lambda -5.58e-7. Pod `rtdz2szboddlsd`, 0.10 h, 0.0929 USD.
- H125 asks Rm = 8.982421875. H126 asks Rm = 9.03125. H127 asks Rm = 8.9365997314453125. Merged main `84a76b2`. The budget fixture stays. Local ledger about 14.27 USD.

## 2026-11-13 - H121 refuted, H122 supported, seeds 0-4 split stops, team cursor
- At n = 96, Rm = 8.93646240234375, seed 7 is negative, lambda -1.20e-6. Pod `ai271fv1pnkcob`, 0.11 h, 0.0998 USD.
- At n = 96, Rm = 8.89830780029296875, seeds 0-4 are all positive. Smallest is 5.16e-8, seed 3. Pod `pg5oy9szrtgp0t`, 0.11 h, 0.100 USD.
- The cfl = 1 split for seeds 0-4 stops. Seed 3 is -3.04e-9 at Rm = 8.8983001708984375 and +5.16e-8 one step higher. H123 continues seeds 5-9. H124 repeats the negative neighbour at cfl = 0.5. Local ledger about 13.50 USD.

## 2026-11-13 - H119 supported, H120 refuted, H121 and H122 registered, team cursor
- At n = 96, Rm = 8.9366455078125, seeds 5-9 are all positive. Smallest is 8.11e-8, seed 7. Pod `ud32b2k2klsjfy`, 0.11 h, 0.1002 USD.
- At n = 96, Rm = 8.8983001708984375, seed 3 is negative, lambda -3.04e-9. Pod `hqgasseggjnvrr`, 0.10 h, 0.0924 USD.
- H121 asks Rm = 8.93646240234375 for seeds 5-9. H122 asks Rm = 8.89830780029296875 for seeds 0-4. Local ledger about 13.30 USD.

## 2026-11-13 - H115 and H116 refuted, H119 and H120 registered, team cursor
- At n = 96, Rm = 8.936279296875, seed 7 is negative, lambda -2.48e-6. Pod `3fwq9nvyvvotd4`, 0.10 h, 0.0928 USD.
- At n = 96, Rm = 8.898284912109375, seed 3 is negative, lambda -1.12e-7. Pod `637zwwe6nnjmhc`, 0.10 h, 0.0925 USD.
- H119 asks Rm = 8.9366455078125 for seeds 5-9. H120 asks Rm = 8.8983001708984375 for seeds 0-4. Local ledger about 13.10 USD.

## 2026-11-13 - H109 and H110 refuted, H117 and H118 registered, team cursor
- At n = 128, Rm = 8.9765625, seed 0 is negative, lambda -7.10e-5. Pod `vwz9je92kdekeb`, 0.39 h, 0.344 USD.
- At n = 128, Rm = 9, seeds 5 and 9 are negative. Most negative is -3.56e-4. Seeds 0-4 are positive at that Rm. Pod `rq42gukg38euct`, 0.39 h, 0.3444 USD.
- H117 asks Rm = 8.98828125 for seeds 0-4. H118 asks Rm = 9.0625 for seeds 5-9. Local ledger about 12.92 USD.

## 2026-11-13 - H113 supported, H114 refuted, H115 and H116 registered, team cursor
- At n = 96, Rm = 8.93701171875, seeds 5-9 are all positive. Smallest is 2.64e-6, seed 7. Pod `z69yt406ykoo6c`, 0.11 h, 0.0995 USD.
- At n = 96, Rm = 8.89825439453125, seed 3 is negative, lambda -3.31e-7. Pod `c1lodndr65t421`, 0.12 h, 0.1077 USD.
- H115 asks Rm = 8.936279296875 for seeds 5-9. H116 asks Rm = 8.898284912109375 for seeds 0-4. Local ledger about 12.23 USD.

## 2026-11-13 - H111 and H112 supported, H113 and H114 registered, team cursor
- At n = 96, Rm = 8.9384765625, seeds 5-9 are all positive. Smallest is 1.29e-5, seed 7. Pod `lu4eednznn02ml`, 0.10 h, 0.0928 USD.
- At n = 96, Rm = 8.8983154296875, seeds 0-4 are all positive. Smallest is 1.06e-7, seed 3. Pod `lshdx2bh2nqygw`, 0.11 h, 0.0939 USD.
- H113 asks Rm = 8.93701171875 for seeds 5-9. H114 asks Rm = 8.89825439453125 for seeds 0-4. Local ledger about 12.02 USD.

## 2026-11-13 - H107 and H108 refuted, H111 and H112 registered, team cursor
- At n = 96, Rm = 8.935546875, seed 7 is negative, lambda -7.59e-6. Pod `zt1dfiehzum7di`, RTX 4090, 0.11 h, 0.100 USD.
- At n = 96, Rm = 8.898193359375, seed 3 is negative, lambda -7.68e-7. Pod `wlub1d420h9quf`, RTX 4090, 0.11 h, 0.1001 USD.
- H111 asks Rm = 8.9384765625 for seeds 5-9. H112 asks Rm = 8.8983154296875 for seeds 0-4. H109 and H110 stay in flight. Local ledger about 11.84 USD.

## 2026-11-13 - H102 supported, H103 refuted, H109 and H110 registered, team cursor
- At n = 128, Rm = 9, seeds 0-4 are all positive. Smallest is 8.62e-5, seed 0. Pod `d5948m7mtwer00`, RTX 4090, 0.39 h, 0.344 USD.
- At n = 128, Rm = 8.953125, seed 0 is negative, lambda -2.30e-4. Pod `6s0ni2gmh17tq1`, RTX 4090, 0.39 h, 0.3438 USD.
- H109 asks the midpoint Rm = 8.9765625. H110 asks seeds 5-9 at Rm = 9. Local ledger about 11.64 USD.

## 2026-11-13 - H106 refuted, H108 registered, team cursor
- At n = 96, Rm = 8.89794921875, seed 3 is negative, lambda -2.52e-6. Pod `eeip6ctp4hlh9w`, RTX 4090, 0.11 h, 0.1002 USD.
- H108 asks the midpoint Rm = 8.898193359375. The positive neighbour is Rm = 8.8984375. H102, H103, and H107 stay in flight. Local ledger about 10.95 USD.

## 2026-11-13 - H105 supported, H107 registered, team cursor
- At n = 96, Rm = 8.94140625, seeds 5-9 are all positive. Smallest is 3.33e-5, seed 7. Seed 7 was -4.86e-5 at Rm = 8.9296875.
- Pod `zmvygt7ikdiahe`, RTX 4090, 0.17 h, 0.1533 USD. Largest max_div_b is 5.74e-16.
- H107 asks the midpoint Rm = 8.935546875. H102, H103, and H106 stay in flight. Local ledger about 10.85 USD.

## 2026-11-13 - H104 refuted, H106 registered, team cursor
- At n = 96, Rm = 8.8974609375, seed 3 is negative, lambda -6.02e-6. Pod `t25phixffvhfbi`, RTX 4090, 0.11 h, 0.1002 USD.
- H106 asks the midpoint Rm = 8.89794921875. The positive neighbour is Rm = 8.8984375. H102, H103, and H105 stay in flight. Local ledger about 10.70 USD.

## 2026-11-13 - H100 and H101 refuted, H104 and H105 registered, team cursor
- At n = 96, Rm = 8.896484375, seed 3 is negative, lambda -1.30e-5. Pod `fxmgol555wb8so`, RTX 4090, 0.11 h, 0.0999 USD.
- At n = 96, Rm = 8.9296875, seed 7 is negative, lambda -4.86e-5. Pod `qtfg7wdr9wop2b`, RTX 4090, 0.11 h, 0.1002 USD.
- H104 asks the seeds 0-4 midpoint Rm = 8.8974609375. H105 asks the seeds 5-9 midpoint Rm = 8.94140625. H102 and H103 stay in flight. Local ledger about 10.60 USD.

## 2026-11-13 - H95 refuted, H103 registered, team cursor
- At n = 128, Rm = 8.890625, seeds 0 and 1 are negative. Most negative is -6.64e-4. Pod `p79984sx0e3aro`, RTX 4090, 0.39 h, 0.3513 USD.
- H103 asks n = 128 at Rm = 8.953125. H102 asks Rm = 9. Claude pods stay up. Local ledger about 10.40 USD.

## 2026-11-13 - H96 refuted, H102 registered, team cursor
- At n = 128, Rm = 8.90625, seeds 0 and 1 are negative. Most negative is -5.54e-4. The same Rm is positive at n = 96.
- Pod `5ruyqody0p5tyj`, RTX 4090, 0.38 h, 0.3362 USD. Largest max_div_b is 4.13e-16.
- H102 asks n = 128 at Rm = 9. H95 is still running. Local ledger about 10.04 USD.

## 2026-11-13 - H99 supported, H101 registered, team cursor
- At n = 96, Rm = 8.953125, seeds 5-9 are all positive. Smallest is 1.15e-4, seed 7. Seed 7 was -2.14e-4 at Rm = 8.90625.
- Pod `vuupjgd79fimmq`, RTX 4090, 0.13 h, 0.1152 USD. Largest max_div_b is 5.41e-16.
- H101 asks the midpoint. The parallel cap now counts only `milady-cursor-job-*`. H100 is in flight. Local ledger about 9.71 USD.

## 2026-11-13 - parallel cap counts this team's pods, team cursor
- `runpod_job.py run` applies `[gpu].max_parallel` to pods whose name starts with this checkout's prefix. The budget reservation still sums every `milady-*job-*` pod. The credit stays shared.
- Test `test_parallel_cap_counts_this_teams_pods_only`. Claude pods are left in place. Pod names stay `milady-cursor-job-*`.

## 2026-11-13 - H98 refuted, H100 registered, team cursor
- At n = 96, Rm = 8.89453125, seed 3 is negative, lambda -2.70e-5. It was +9.81e-7 at Rm = 8.8984375.
- Pod `0q5ipquvid11fg`, RTX 4090, 0.12 h, 0.1079 USD. Largest max_div_b is 5.41e-16.
- H100 asks the midpoint and waits for a free slot. Two Claude pods are up. They are left in place. Local ledger about 9.59 USD.

## 2026-11-13 - H97 supported, H99 registered, team cursor
- At n = 96, Rm = 9, seeds 5-9 are all positive. Smallest is 4.35e-4, seed 7. Seed 7 was -2.14e-4 at Rm = 8.90625.
- Pod `s8ebnuqst9fecc`, RTX 4090, 0.10 h, 0.0926 USD. Largest max_div_b is 6.14e-16.
- H99 asks the midpoint for seeds 5-9. H95, H96, and H98 are in flight. Local ledger about 9.48 USD.

## 2026-11-13 - H94 supported, H98 registered, team cursor
- At n = 96, Rm = 8.8984375, seeds 0-4 are all positive. Smallest is 9.81e-7, seed 3. It was -5.51e-5 at Rm = 8.890625.
- Pod `tqefulq6a1gyy3`, RTX 4090, 0.12 h, 0.1079 USD. Largest max_div_b is 6.40e-16.
- H98 asks the midpoint. H95, H96, and H97 are in flight. Local ledger about 9.39 USD.

## 2026-11-13 - H93 refuted, H97 registered, team cursor
- At n = 96, Rm = 8.90625, seed 7 is negative, lambda -2.14e-4. Seeds 0-4 at this Rm are positive. Pod `iwi25z0iibq140`, 0.0998 USD.
- H97 asks seeds 5-9 at Rm = 9 before treating that bracket as closed. H94, H95, and H96 are still running.
- Local ledger about 9.28 USD.

## 2026-11-13 - H87 and H91 refuted, H92 supported, team cursor
- n = 96 seed 3 is negative at Rm = 8.890625, lambda -5.51e-5. Pod `c7bhiyc0v8oifm`, 0.0998 USD. H94 asks Rm = 8.8984375.
- n = 48 seed 7 is negative, lambda -4.19e-9. n = 32 seed 0 is positive, lambda 1.62e-9. Those two splits stop. The remaining gaps are a few times 1e-6 in Rm, and the lambdas are a few times 1e-9. The cfl = 0.5 check differed by 2.7e-11.
- H95 and H96 ask the same two Rm values at n = 128. H93 is still running. Local ledger about 9.18 USD.

## 2026-11-13 - H88 supported, H89 and H90 refuted, team cursor
- n = 48 seeds 5-9 stay positive at Rm = 9.062614440917969. Smallest is 1.96e-8, seed 7. Pod `0ipf3qcxgzzqwr`, 0.0467 USD.
- n = 32 seed 0 is negative at Rm = 9.052364349365234, lambda -1.06e-8. Pod `0hpfymeqdew2dx`, 0.0468 USD.
- n = 64 seed 1 is negative at Rm = 9.059858322143555, lambda -4.82e-9, and positive at Rm = 9.059860229492188, lambda 7.00e-9. The cfl = 0.5 check differed by 2.7e-11. No further n = 64 split. Pod `jggunh2atv066z`, 0.0466 USD.
- H91 and H92 ask the n = 48 and n = 32 midpoints. H93 asks n = 96 seeds 5-9 at Rm = 8.90625. H87 is still running.

## 2026-11-13 - H80 supported, H84 H85 H86 refuted, team cursor
- n = 96 at Rm = 8.90625 is all positive. Smallest is 5.68e-5, seed 3. Pod `ka74qxg592d0hh`, 0.1002 USD.
- n = 48 seed 7 is negative at the latest midpoint, lambda -2.80e-8. Pod `je3x33cpp1q2kv`, 0.0471 USD.
- n = 32 seed 0 is negative, lambda -3.49e-8. Pod `ts73xpcevlladp`, 0.0392 USD.
- n = 64 seed 1 is negative, lambda -1.66e-8. Pod `aa4bz815b5i1tp`, 0.0317 USD.
- H87 asks n = 96 at the midpoint. H88, H89, and H90 ask the three small midpoints. Local ledger about 8.85 USD.

## 2026-11-13 - H83 refuted, H86 registered, team cursor
- At n = 64, Rm = 9.059852600097656, seed 1 is negative, lambda -4.03e-8. It was +7.00e-9 at Rm = 9.059860229492188.
- Pod `5m9resf34p49a1`, RTX 4090, 0.06 h, 0.0544 USD. Largest max_div_b is 4.77e-16.
- H86 asks the midpoint. H80, H84, and H85 are in flight. Local ledger about 8.63 USD.

## 2026-11-13 - H81 and H82 refuted, team cursor
- n = 48 seed 7 is negative at Rm = 9.062591552734375, lambda -1.23e-7. Pod `9ihsmkh0tuleze`, 0.0239 USD.
- n = 32 seed 0 is negative at Rm = 9.052352905273438, lambda -8.36e-8. Pod `7x3pewu848zlr1`, 0.0240 USD.
- H84 and H85 ask those midpoints. H80 and H83 are still running.

## 2026-11-13 - H79 supported, H83 registered, team cursor
- At n = 64, Rm = 9.059860229492188, seeds 0-4 are all positive. Seed 1 is 7.00e-9. It was -8.75e-8 one step lower.
- Pod `02lzppd8ook0ss`, RTX 4090, 0.05 h, 0.0464 USD. Largest max_div_b is 5.77e-16.
- H83 asks the midpoint. H80, H81, and H82 are in flight. Local ledger about 8.53 USD.

## 2026-11-13 - H73 supported, H77 and H78 refuted, team cursor
- n = 96 at Rm = 8.9375 is all positive. Smallest is 2.78e-4, seed 3. Pod `1zncsnmt5efp6c`, 0.1002 USD.
- n = 48 seeds 6 and 7 are negative at Rm = 9.06256103515625. Pod `mkwv5iy5rku29p`, 0.0544 USD.
- n = 32 seed 0 is negative at Rm = 9.052337646484375, lambda -1.81e-7. Pod `as1pofdjhtfvwv`, 0.0239 USD.
- H80 asks n = 96 at Rm = 8.90625. H81 and H82 are the next small midpoints. H79 is still running.

## 2026-11-13 - H74 supported, H75 and H76 refuted, team cursor
- n = 48 seeds 5-9 at Rm = 9.0626220703125 are all positive. Smallest is 6.72e-8, seed 7. Pod `qaziio81h5gurb`, 0.0467 USD.
- n = 64 seed 1 at Rm = 9.059844970703125 is negative, lambda -8.75e-8. Pod `iearzvag61uoax`, 0.0547 USD.
- n = 32 seed 0 at Rm = 9.05230712890625 is negative, lambda -3.76e-7. Pod `vs1wic83swf5ix`, 0.0471 USD.
- H77, H78, and H79 ask the next midpoints. H77 and H78 are in flight. H73 is still running.

## 2026-11-13 - H66 refuted, H70 H71 H72 supported, team cursor
- n = 96 at Rm = 8.875 has seed 3 negative, lambda -1.68e-4. Pod `p32lpzy6h9yade`, 0.1005 USD.
- n = 48 seeds 5-9 stay positive at Rm = 9.062744140625. Smallest is 8.29e-7. Pod `s1ah8ic5vxdhx9`, 0.0391 USD.
- n = 32 seed 0 is positive at Rm = 9.0523681640625, lambda 1.38e-8. Pod `0e8zh26tehom3d`, 0.0391 USD.
- The cfl = 0.5 repeat of the n = 64 point keeps seed 1 at 1.02e-7. The cfl = 1 value was 1.015e-7. Pod `88amwjefmkbx0g`, 0.0469 USD.
- H73 asks n = 96 at Rm = 8.9375. H74, H75, and H76 are the next midpoints. Local ledger about 8.16 USD.

## 2026-11-13 - H69 supported, H72 registered, team cursor
- At n = 64, Rm = 9.05987548828125, cfl = 1, seeds 0-4 are all positive. Seed 1 is 1.02e-7.
- Pod `06wh0zrvxx0x5v`, RTX 4090, 0.06 h, 0.0545 USD. Largest max_div_b is 5.75e-16.
- H72 repeats that point at cfl = 0.5 before any further split. H66, H70, and H71 are in flight. Local ledger about 7.93 USD.

## 2026-11-13 - H67 and H68 supported, team cursor
- n = 48 seeds 5-9 at Rm = 9.06298828125 are all positive. Smallest is 2.35e-6, seed 7. Pod `q568jhwf7vcxxl`, 0.0394 USD.
- n = 32 seed 0 at Rm = 9.052490234375 is positive, lambda 7.93e-7. It was -7.65e-7 one step lower. Pod `a9hpfnk6izf20m`, 0.0321 USD.
- H70 and H71 ask those midpoints. H66 and H69 are still running.

## 2026-11-13 - H65 supported, H69 registered, team cursor
- At n = 64, Rm = 9.0599365234375, seeds 0-4 are all positive. Seed 1 is 4.80e-7. It was -2.77e-7 at Rm = 9.059814453125.
- Pod `saimt3y6x17ifn`, RTX 4090, 0.06 h, 0.0543 USD. Largest max_div_b is 5.75e-16.
- H69 asks the midpoint. H66, H67, and H68 are in flight. Local ledger about 7.81 USD.

## 2026-11-13 - H59 and H64 refuted, H63 supported, team cursor
- Every n = 96 seed is negative at Rm = 8.75. Most negative is -1.10e-3. Pod `ttwt0zwzm9aefu`, 0.1002 USD.
- n = 48 seeds 5-9 stay positive at Rm = 9.0634765625. Smallest is 5.40e-6. Pod `ttcz68wqadtfv9`, 0.0392 USD.
- n = 32 seed 0 is negative at Rm = 9.05224609375, lambda -7.65e-7. Pod `znzgqwf7icy4f7`, 0.0466 USD.
- H66 asks n = 96 at Rm = 8.875. H67 and H68 are the next small midpoints. H65 is still running.

## 2026-11-13 - H60 supported, H61 and H62 refuted, team cursor
- n = 48 seeds 5-9 at Rm = 9.064453125 are all positive. Smallest is 1.15e-5, seed 7. Pod `uof8xng35o523n`, 0.0544 USD.
- n = 32 seed 0 at Rm = 9.0517578125 is negative, lambda -3.88e-6. Pod `juneeb2w8kanwe`, 0.0392 USD.
- n = 64 seed 1 at Rm = 9.059814453125 is negative, lambda -2.77e-7. Pod `5yj9263580wl21`, 0.0315 USD.
- H63, H64, and H65 ask the three midpoints. H59 is still running. The criteria were not changed.

## 2026-11-13 - H58 supported, H62 registered, team cursor
- At n = 64, Rm = 9.06005859375, seeds 0-4 are all positive. Seed 1 is 1.24e-6. It was -1.79e-6 at Rm = 9.0595703125.
- Pod `7psi6fa4syqtb9`, RTX 4090, 0.06 h, 0.0544 USD. Largest max_div_b is 5.13e-16. The criterion was not changed.
- H62 asks the midpoint. H59, H60, and H61 are in flight. Local ledger about 7.44 USD.

## 2026-11-13 - H54 refuted, H56 and H57 supported, team cursor
- H54: n = 96, Rm = 8.5, every seed is negative. The most negative lambda is -0.003160. Pod `69nxybu6hgbm75`, 0.1083 USD.
- H56: n = 48, Rm = 9.06640625, seeds 5-9 all positive. Smallest is 2.36e-5. Pod `c87uy2u6fgq7k2`, 0.0392 USD.
- H57: n = 32, Rm = 9.052734375, seeds 0-4 all positive. Smallest is 2.35e-6. Pod `k0i510cxe4fudx`, 0.0467 USD.
- H59 asks n = 96 at Rm = 8.75. H60 and H61 are the next small midpoints. H58 is still running.

## 2026-11-13 - H55 refuted, H58 registered, team cursor
- At n = 64, Rm = 9.0595703125, seed 1 is negative, lambda -1.79e-6. The other four seeds are positive. The all-positive claim fails.
- Pod `ky7n0s6jukffau`, RTX 4090, 0.06 h, 0.0545 USD. The criterion was not changed.
- Seed 1 is positive at Rm = 9.060546875. H58 asks the midpoint. H54, H56, and H57 are in flight.

## 2026-11-13 - H52 supported, H53 refuted, team cursor
- H52: n = 48, Rm = 9.0703125, seeds 5-9 all positive. Smallest lambda is 4.79e-5. Pod `fy8lgoo7n99t3d`, 0.0390 USD.
- H53: n = 32, Rm = 9.05078125, seed 0 is negative, lambda -1.01e-5. The all-positive claim fails. Pod `epewxk9z1fdgm8`, 0.0467 USD.
- H56 and H57 are the next midpoints. H54 and H55 are still running. CI on `defd29f` is green.

## 2026-11-13 - H49 supported, H55 registered, team cursor
- At n = 64, Rm = 9.060546875, seeds 0-4 are all positive. Seed 1, negative at Rm = 9.05859375, is 4.26e-6. Largest max_div_b is 5.12e-16.
- Pod `i07ibmsytvr9lw`, RTX 4090, 0.06 h, 0.0544 USD. The all-positive bracket is now 9.05859375 to 9.060546875.
- H55 asks the midpoint Rm = 9.0595703125. That sign may fail. H52, H53, and H54 are in flight.

## 2026-11-13 - H48, H50, H51 supported, team cursor
- H48: n = 96, Rm = 9.03125, seeds 0-4 all positive. Smallest lambda is 0.000920. The same Rm is negative for two seeds at n = 64. Pod `3xqsragjm09ry5`, 0.0926 USD.
- H50: n = 48, Rm = 9.078125, seeds 5-9 all positive. Smallest is 9.63e-5. Pod `vjg69pqzfnk2nx`, 0.0240 USD.
- H51: n = 32, Rm = 9.0546875, seeds 0-4 all positive. Smallest is 1.48e-5. Pod `ejwduhbdkmn69h`, 0.0240 USD.
- H52 and H53 continue those brackets. H54 asks whether n = 96 is already positive at Rm = 8.5. H49 is still running.

## 2026-11-13 - H45 and H47 refuted, H46 supported, team cursor
- H45: n = 64, Rm = 9.05859375, seed 1 is still negative, lambda -7.84e-6. The all-positive claim fails. Pod `wc0jpa3u2s9839`, 0.0467 USD.
- H47: n = 32, Rm = 9.046875, seed 0 is negative, lambda -3.51e-5. Pod `q47is8cxzdfe8b`, 0.0242 USD.
- H46: n = 48, Rm = 9.09375, seeds 5-9 all positive. Smallest lambda is 0.000192. Pod `xo996or9uzz8ep`, 0.0240 USD.
- H49, H50, and H51 are the next midpoints. H48, n = 96 at Rm = 9.03125, is still running.

## 2026-11-13 - H42 and H44 refuted, H40 and H43 supported, team cursor
- H42: n = 64, Rm = 9.0546875, seed 1 still negative. Seed 4 is positive. The all-positive claim fails. Pod `tzl3ff119nzs2f`, 0.0316 USD.
- H44: n = 32, Rm = 9.03125, seed 0 is negative. Pod `ju2osfd8pyjc90`, 0.0240 USD.
- H40: n = 96, Rm = 9.0625, all positive. Smallest lambda is 0.001128. Pod `ilkp6hal3i9fy6`, 0.1004 USD.
- H43: n = 48, Rm = 9.125, seeds 5-9 all positive. Smallest is 0.000382. Pod `2djc7mhnhnyvba`, 0.0239 USD.
- H45, H46, H47, and H48 are the next midpoints. The signs were fixed before those runs. Local ledger about 6.76 USD.

## 2026-11-13 - H39 and H41 refuted, H38 supported, team cursor
- H41: n = 64, Rm = 9.046875, seeds 1 and 4 negative. The all-positive claim fails. Pod `vtjrs9h3ibnbys`, 0.0467 USD.
- H39: n = 48, Rm = 9.0625, seeds 6 and 7 negative. The all-positive claim fails. Pod `my44rr0lt5z12c`, 0.0390 USD.
- H38: n = 32, Rm = 9.0625, seeds 0-4 all positive. Smallest lambda is 6.45e-5. Pod `odeo2utdbjkpx2`, 0.0394 USD.
- The criteria were not changed. H42 is the next n = 64 midpoint. H43 and H44 are the neighbouring sign tests. H40 is still running.

## 2026-11-13 - H34 refuted, team cursor
- At n = 64, Rm = 9.03125, seeds 1 and 4 are negative. Lambdas are -0.000179 and -0.000130. The other three seeds are positive. Largest max_div_b is 5.51e-16.
- The all-positive claim fails. The criterion was not changed. Pod `u3vvb69h7bjcv4`, RTX 4090, 0.07 h, 0.0620 USD.
- At the same resolution, Rm = 9.0625 is positive for seeds 0-4 and 5-9. The all-positive boundary sits between 9.03125 and 9.0625.
- H41 asks whether Rm = 9.046875 is already positive for seeds 0-4. That sign may fail. H38, H39, and H40 are in flight.

## 2026-11-13 - H36 and H37 supported, team cursor
- H36: cfl = 0.5 at n = 64, Rm = 9.0625, all positive. Smallest lambda is 1.63e-5. Pod `94xxtipk5c70o0`, 0.0469 USD.
- H37: n = 48, Rm = 9.0625, seeds 0-4, all positive. Smallest lambda is 7.37e-5. Pod `dl8nqu1e3h9jtm`, 0.0467 USD.
- H35: seeds 5-9 at n = 64, Rm = 9.0625, all positive. Smallest lambda is 2.94e-7. Pod `6oxhe6u585v83v`, 0.0548 USD.
- H38 asks whether n = 32 stays positive. H39 asks whether seeds 5-9 at n = 48 stay positive. H40 asks whether n = 96 stays positive. H34 is still running.

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
