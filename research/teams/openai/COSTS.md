# Costs

Written by the framework from its ledgers at 2026-11-15T00:51:22+00:00 (`.frontier/`).

## LLM

Spent 0.6432 USD of 5.0 USD, of which 0.0087 USD after delivery (the harness finishing its turn).

| model | calls | input tokens | output tokens | USD |
|---|---:|---:|---:|---:|
| openai/gpt-6.1-terra | 93 | 5929528 | 49544 | 0.6415 |
| xai/grok-4.7 | 1 | 1246 | 1 | 0.0008 |
| moonshot/kimi-k3 | 1 | 90 | 38 | 0.0006 |
| google/gemini-4-hydrogen | 1 | 35 | 16 | 0.0002 |
| alibaba/qwen3.8-27b | 1 | 40 | 23 | 0.0000 |
| deepseek/deepseek-v4-pro | 1 | 8 | 17 | 0.0000 |
| mistral/mistral-small-2603 | 1 | 19 | 2 | 0.0000 |
| zhipu/glm-5.3-flash | 1 | 16 | 3 | 0.0000 |
| openai/gpt-6-luna | 1 | 10 | 5 | 0.0000 |
| anthropic/claude-haiku-5-5 | 1 | 15 | 4 | 0.0000 |

## Cloud

- scaleway: not used.
- runpod: 0.2334 USD of 5.0 USD.

| provider | resource | id | type | price/h | max h | created | deleted |
|---|---|---|---|---:|---:|---|---|
| runpod | pod | 598b0r2dfknu2l | 1x NVIDIA GeForce RTX 4090 | 0.89 | 1.25 | 2026-11-15T00:32:52+00:00 | 2026-11-15T00:48:36+00:00 |

## Time

Elapsed: 0.331 h. Deadline: 2026-11-15T02:01:32+00:00.

## Ledgers

Integrity of the hash-chained logs: {"llm.jsonl": true, "events.jsonl": true}.
Last hash of llm.jsonl: `3e4333be07038b5dc63db84dd5b1c0ec2afa798e31a54f3f1ba23b513336e76c`.

## Publications

- https://huggingface.co/datasets/knoel/milady-20261115-race-openai-race-openai-milady-20261115-0031-7c9-data (dataset, private)
- https://huggingface.co/knoel/milady-20261115-race-openai-race-openai-milady-20261115-0031-7c9-models (model, private)
