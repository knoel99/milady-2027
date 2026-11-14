# Brief: compute-path

Mode describe (no reference image), depth full, web off, route flat, width 183 mm.
**One sentence:** The session has no GPU: each GPU job is a rented pod that clones a pushed commit, runs under a time limit, returns its outputs and is deleted, with its cost written to a ledger.
**Key ideas:** (1) session container, 4 CPU cores, no GPU; (2) push, job tool, rented RunPod pod (clone, environment, job, HTTP outputs); (3) fetch, delete pod, ledger, commit results, digest; (4) five failures in the order found; (5) measured time and cost.
**Must not imply:** any result value, any pending number, any step not in FACTS.md.
**Source:** `site/teams/claude/figures/FACTS.md` only. **Reader:** internship report readers (physicists, supervisors).
