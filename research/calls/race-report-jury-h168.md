single-model simulation (no independent sub-agent).

The main session wrote this file by following `.cursor/agents/jury-externe.md`. No separate role process ran.

| Claim | Location | Verdict | Evidence | Required change |
| --- | --- | --- | --- | --- |
| H168 mean C1 is 0.769 and meets 1.2 | race report, C6 | CONFIRMED | `experiments/results/cursor_fm/metrics.json`, five finite seeds, mean 0.7693019720277114 | Keep seed 0 at 1.508 in the same paragraph |
| The learned model beats the midpoint | report, Discussion | REJECTED as a claim the text does not make | Learned mean 0.769, midpoint mean 0.743 | Do not add a sentence that says the flow wins on the mean |
| C4 of the learned model meets 0.1 | metrics file | REJECTED | Learned mean C4 about 0.310. The quoted C4 stays the kmax=6 midpoint 0.0093 | Leave that split explicit |
| The PDF is still between 30 and 50 pages | report PDF | CONFIRMED | `pdfinfo` prints `Pages: 35` | None |
| Weights and the dataset are in the tree with cards | `experiments/results/cursor_fm/` | CONFIRMED as files | five `weights_s*.pt`, `dataset.npz`, `MODEL_CARD.md`, `DATASET_CARD.md` | The HTTP check is outside this note |

Pre-defence. The registered bound holds and the midpoint is not beaten. The three changes before a defence are to keep seed 0 visible, to keep the C4 miss out of the quoted C4, and to show that the weight and card links answer. What remains unverified is the HTTP response of those links after the push.
