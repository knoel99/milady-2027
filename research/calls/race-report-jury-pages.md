single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/jury-externe.md`. No separate role process ran.

| Claim | Location | Verdict | Evidence | Required change |
| --- | --- | --- | --- | --- |
| The team PDF has 34 pages, between 30 and 50 | report PDF, race report Deliverables | CONFIRMED | `pdfinfo` prints `Pages: 34` on `site/teams/cursor/report/index.pdf` | None |
| The source is one qmd, with html and pdf formats | `site/teams/cursor/report/index.qmd` | CONFIRMED | The yaml has `format.html` and `format.pdf` with `documentclass: report`. No separate `.tex` is committed | Keep `format-links: false` |
| H157 is the kmax=4 midpoint, not the kmax=6 midpoint | report, Results | CONFIRMED | H157 statement in `research/hypotheses.json` names the same protocol as H156, whose result is mean 0.743 | Do not attach H157 to the kmax=6 ratio 0.014 |
| `cursor_metrics.json` C1 equals the kmax=6 midpoint mean | report, Results | CONFIRMED | Recomputed mean 0.013966666402533533 | Label it as a baseline, which the report does |
| H168 has a learned score | report, Abstract | CONFIRMED as an absence | `experiments/results/cursor_fm/metrics.json` is missing. The report says the rerun is not scored | Quote the five-seed mean only after that file exists |
| Weights and the coefficient dataset are published | report, Reproducibility | TO BE SPECIFIED | The report does not give a link that returns those files, because the pod has not written them | Publish the cards with the H168 outputs |

Pre-defence. The page count and the baseline table match the files. The learned generator is still missing. The three changes before this report can be defended as the internship comparison are a scored H168, the weights and the dataset with cards, and a comparative row that uses that score. What remains unverified is the running pod.
