# Budget estimate per team (2026-11-13)

Basis: the Claude pilot, measured by `tools/usage_report.py` and `research/compute-ledger.jsonl` on its branch: 23.9 h of work, **329 USD API-equivalent** of Claude (Fable 5.2 high for the main session and the roles), **52 GPU-hours, 46.7 USD** on RunPod (0.89 USD per GPU-hour). Its token mix (1.3 % uncached input, 97.8 % cache reads, 0.5 % output, over 23.9 h) is applied to each provider's API prices; a model that reads, writes or reasons more or less than Fable shifts the figure. "One pilot" = the work the Claude pilot did in 24 h (report v4, 33 hypotheses, deliverables).

| Team | Main model | Cost ratio to Fable at the same tokens | API for one pilot | Plan alternative | Credit advised |
|---|---|---|---|---|---|
| openai | GPT-6 Astra | 2.4 | ~780 USD | ChatGPT Pro 200 USD/month (no 5-hour limit) | **Pro 200 USD**; or API 150 USD with GPT-6.1 Sol as main model (ratio 0.3) |
| google | Gemini 4 Carbon | 0.3 (0.6 from 1 December) | ~100 USD (~200 from December) | AI Ultra 100 to 200 USD/month | **API 150 USD**, billing enabled (the free tier refused Carbon once) |
| xai | Grok 4.7 | 0.95 | ~310 USD | X subscription Ultra 200 USD/month | **Ultra 200 USD**, or API 350 USD |
| mistral | Mistral Large 4 | 0.15 | ~50 USD | Pro 15 USD/month + pay-as-you-go | **API 75 USD** on a paid tier (this key allows 1,000 tokens per minute) |
| zhipu | GLM-5.3 | 0.5 | ~170 USD | GLM Coding Plan Max 118 to 168 USD/month | **Coding Plan Max** (cancel 24 h before renewal), or API 250 USD |
| moonshot | Kimi K3.1 Pro | 0.44 (official CNY prices: 13 / 1.30 / 68 CNY per 1M tokens, at 7.1 CNY per USD) | ~145 USD | Max ~80 to 100 USD/month | **API 200 USD** (a recharge also lifts the 3 requests per minute of tier 0) |
| deepseek | DeepSeek V4.1 Flash 1017 | 0.03 | ~10 USD | none | **API 25 USD** (V4 Pro for the jury included) |
| alibaba | Qwen3.8-Max | 0.44 to 0.78 if a cache hit costs 10 to 20 % of the input price (Alibaba writes that for qwen3.8-max it is "not 20 %" and gives no figure); 3.5 without any cache | 145 to 260 USD (1,160 without cache) | none usable (the Coding Plan forbids automation) | **API 150 USD with a hard cap**, then read the real cost after one hour |

GPU (RunPod, shared credit): about **50 USD per team per pilot**, so about 350 USD for seven teams on top of what the Claude and Cursor pilots used. On Scaleway the same 52 GPU-hours would cost about 41 EUR on an L4 (0.79 EUR/h) or 76 EUR on an L40S (1.47 EUR/h), but `tools/runpod_job.py` has no Scaleway equivalent yet and the L40S and H100 of pl-waw-2 were out of stock on 12 November.

Scaleway race host (`race/HOST.md`): POP2-HC-32C-64G at 0.85 EUR/h, about **20 EUR per 24 h pilot** or **145 EUR per week** running all the time, plus about 3 EUR per week for 150 GB of block storage.
