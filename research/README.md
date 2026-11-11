# Research register

Empty until the research phase starts. One hypothesis per working session:

1. **Register.** Add the hypothesis to `hypotheses.json` with its quantitative refutation criterion, protocol and cost estimate, written before any computation. The user approves the list and any GPU spending.
2. **Quick run.** Write or extend the script in `experiments/` and run it with `--quick`.
3. **Full run.** At most 2 h of CPU, split by seed otherwise; at least five seeds for any quoted comparison.
4. **Digest.** Regenerate `experiments/results/digest.md` with `experiments/digest.py`: it is the only source of quoted numbers.
5. **Verdict.** The `encadrant` agent tries to refute the result; its verdict goes into the register.
6. **Write.** Update one paragraph of the report or the thesis, set the status, add a journal entry, commit and push.

Two cycles without a discriminating verdict: the hypothesis is dropped and reported as a negative result. Milestones (theory brief, report v1, thesis v1) go to `jury-externe`.
