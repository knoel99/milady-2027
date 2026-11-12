single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/encadrant.md`. No separate role process ran.

Claim. H4 in `research/hypotheses.json`. Both GPU bench jobs (n = 64 and 128, 50 steps, float32 then float64) finish with rc 0 and a finite seconds_per_step at each resolution. One run per dtype. No speedup claim.

Re-run. The GPU jobs were not started again. The check is the committed logs. `research/gpu-logs/bench-float32.log` has n=64 seconds_per_step 0.006443568398244679 and n=128 0.008683746322058141, both finite, dtype float32, device cuda. `research/gpu-logs/bench-float64.log` has n=64 0.003924073041416704 and n=128 0.04840661495923996, both finite, dtype float64. Ledger rc is 0 for both pods (`vui0rucxogb2nx`, `1a7rilk2gah9tn`). CONFIRMED that these two files meet the written criterion. UNCHECKED as a second run.

Trace. The numbers above are the log lines, not digest numbers. The CPUs and the GPUs differ, so the float32 and float64 rates are not a comparison. Status of H4 in the hypothesis file is supported on this criterion only. CONFIRMED that the logs match the ledger commands.

Numerical protocol. One run, no five-seed scatter, no profiler. The criterion explicitly forbids a speedup claim. CONFIRMED that the journal does not claim one. The limiter is UNCHECKED.

Verdict. H4 is not refuted. The two committed logs meet the criterion. A second run was not done.
