# Brief: mhd-dynamo-problem
Mode: describe. Format: journal, double column 183 mm. Audience: physicists and ML readers of the internship report. Source of content: `site/teams/claude/figures/FACTS.md` only.

**Takeaway:** a helical force at wavenumber 2 in a periodic box drives a flow; above a threshold in Rm it sustains a magnetic field with a large-scale part at k = 1; the control parameter η (11 values, Rm 6.25 to 16.7) changes the statistically stationary state, and the generative model must produce snapshots (u, B) of that state for values of η it never saw.

**Key ideas:** forced helical flow in a periodic box; large-scale B at k = 1; η axis with trends of E_u (falls), E_B (rises), H_M (more negative); the two MHD equations; train/validation/held-out split; the generator is judged at held-out η.
**Must not imply:** any generator result; that the trend curves are linear (only the end values are known here); that the Rm ≈ 5 threshold is a result (exploratory); any (pending) number.
**Scope:** the problem, not the model or the results (later figures).
