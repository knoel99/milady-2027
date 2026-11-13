# Standard goal of a race team

One goal for every team and every harness. `race/PILOT-PROMPT.md` (Claude pilot, `/goal`) and `race/TEAM-PROMPT.md` (headless teams of the race host) carry the text of the block below verbatim, with `{team}` replaced; `tests/test_race.py` checks it. Write it in English; a French form may be pasted to a session, but this file is the reference.

## Why each clause is there (pilot of 12–13 November 2026)

| Clause | Lesson |
|---|---|
| Ends on the budget or the usage limit, not on a report | A goal made only of end-state conditions stopped the first pilot as soon as its first report was written, with budget left. |
| The offer is the yardstick, and the reviewing roles repeat it | Over 28 h the pilot ran 40 well-built hypotheses, most of them on fine effects of one 16³, Re = 10 case, far from what the offer asks (parameters across the dynamo threshold, turbulent regimes, reusable 3D fields). Nobody reminded it of the offer. |
| Prefer steps that change an answer to the offer | Forensics of a small effect in a toy case cost as much GPU time as a step towards the threshold or a larger grid. |
| A closing phase with a reserve | The owner had to stop the pilot by hand to get a report written to the offer and the running jobs finished. |
| Data and models published | The data and weights of the first pilot lived only in its container (`research/data-storage.md`); the site in production promises MFF data, a catalogue and models. |
| Judged on quality, time to delivery and total cost | The owner compares teams on the scientific quality of the deliverables, the time to the final delivery and the total LLM and GPU cost: a team must optimise its own simulation time and its scientific output, without trading quality. |
| Reviews kept, fast mode allowed | A cost criterion pushes an agent to drop the reviews first (29 % of the LLM cost of the first pilot); the owner lets each team decide when a faster, dearer mode is worth it. |
| What to do when the usage limit stops the session | A session stopped by the limit does not restart by itself at the reset; the owner schedules a wake-up message, and the session must resume from its last state. |

## The goal

```
Advance the research asked by the internship offer "Physics-Constrained Generative AI Modelling of Parametric Dynamical Systems" (docs/specs/sources/supervisors.md §1.2 a) as far as the budget allows, with your own strategy. The offer is the yardstick: generative models (diffusion or flow matching) conditioned on physical parameters (Reynolds number, magnetic Reynolds number, material properties); physical constraints (energy balance, zero divergence) imposed by the architecture, the loss or the sampling; the metrics of the offer (energy spectra, helicity, divergence control, topology); 3D fields reusable by reduced-order models and data assimilation; the context of polarity reversals; deliverables: a comparative study and code in the MilaDy toolbox.

How you are judged: the scientific quality of the deliverables first (sound and reproduced results, verdicts that hold under blind review, a report that answers the offer), then the time to the final delivery (from the first commit of the team to the commit of research/GOAL-MET) and the total cost (LLM calls at API-equivalent prices, from tools/usage_report.py or the provider's usage, plus GPU time from research/compute-ledger.jsonl and the team's share of the VM). Optimise them yourself: size each simulation and training run to what its verdict needs (a timing first, --quick before full runs, no run larger than its question), drop steps that cannot change an answer to the offer, and stop polishing once the deliverables meet the offer. Never buy speed or cost with quality: the rules of AGENTS.md (criterion written before the computation, at least five seeds for a quoted comparison, the reviews of encadrant and jury-externe) stay in force. The reviews of encadrant and jury-externe are part of the quality, not a cost to cut: keep them, with their model and effort, but batch them (one encadrant review per batch of hypotheses judged together, jury-externe at the milestones and on the final report). The fast mode or priority tier of your harness (for example /fast in Claude Code), when it exists, is yours to use where you judge that the speed is worth its price (for example while you wait on a decision, or in the closing phase); its calls count at the price billed for them.

Research phase. After each result, take the step of the remaining work that most changes an answer to the offer, before refining a small effect of a case already understood; a hypothesis without a discriminating verdict after two cycles is dropped and reported. Every task given to `encadrant` and `jury-externe` carries the criteria of the offer above and asks them to judge whether the work answers them and to name what drifts away from them or is detail without impact; follow their answer or write in research/journal.md why not.

Closing phase. It starts as soon as one of these holds: the GPU budget left can no longer pay for one useful job plus the closing (keep at least 10 % of the team's GPU budget for it); the usage limit of your provider warns; the owner asks for it; or you show in research/race-report.md, with evidence, that no step left within the budget can change a verdict or an objective. In the closing phase: launch no new hypothesis and no new GPU job; finish the jobs already running and have their verdicts given by `encadrant`; run `python3 tools/runpod_job.py cleanup`; write the internship report to the criteria of the offer (measured, published and conjectured kept apart; the limits of the setting said plainly; what is needed for turbulent regimes, the dynamo threshold and SFEMaNS data); publish the data and the models cited in the report as the site promises (data in the MFF format of docs/specs/data-format.md, validated; datasets and models in the catalogue; files attached to a GitHub release of the repository with SHA-256 sums, linked from the report and the team page, with a few lines that reload a model and draw samples); have `jury-externe` review the report against the criteria of the offer and fix what it finds blocking.

The goal is met only when: no job or pod of team {team} is running; race/teams/{team}/objectives.toml passes `python3 tools/race_progress.py check`; research/race-report.md states what is measured, published and conjectured and the remaining work for each objective; the report follows the criteria of the offer and its last `jury-externe` review has no open blocking point; the data and model downloads are published and their links work; `python3 tools/check_deliverables.py --team {team} --built` passes; research/usage/latest.md is up to date with no non-conforming role call; everything is committed and pushed; and research/GOAL-MET holds one line saying which condition opened the closing phase.

If a session is stopped by the usage limit, the next message it receives (for example a wake-up scheduled after the reset) resumes the closing phase from the state committed in the repository.
```

## Support by harness

A native goal keeps a session working until its condition holds. On the race host it is not needed: `infra/deploy/race-team-loop.sh` invokes the harness again and again with `race/TEAM-PROMPT.md` until `research/GOAL-MET` exists, which gives every harness the same goal. Native support, found in the shipped binaries on 13 November 2026 (strings and help), not run headless:

| Team | Harness | Native goal | How the goal runs in the race |
|---|---|---|---|
| claude | Claude Code (cloud session) | yes: `/goal`, a stop hook that checks the condition at each end of turn | `/goal` with the block above (`race/PILOT-PROMPT.md`) |
| xai | Grok Build / Cursor agent | yes: `/goal`, `/goal clear` (interactive) | the Cursor pilot: Grok Bot orchestrates, the block above in its prompt |
| openai | Codex 0.169 | yes: `/goal`, `/goal edit`, `/goal resume`, `/goal clear` (interactive) | race-host loop |
| google | Antigravity 1.5.8 | yes: `/goal`, stop hooks | race-host loop |
| moonshot | Kimi Code 2.6.1 | yes: `/goal` ("Goal set"), stop hook | race-host loop |
| alibaba | Qwen Code 0.27.3 | yes: goal and stop hooks | race-host loop |
| mistral | Vibe 3.1.2 | none found | race-host loop |
| deepseek | dsh 0.2.2-rc.1 | none found | race-host loop |
| zhipu | Claude Code on Z.ai | yes: `/goal` | race-host loop |

Every model is driven by its harness; the goal does not depend on the model. A provider's usage limit or rate limit (for example the 1,000 tokens per minute of the Mistral key, `race/PROVIDERS-TESTED.md`) stops the loop after three short failures; the closing phase then resumes at the next start of the service.
