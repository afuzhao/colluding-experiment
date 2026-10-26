# The lowest anchor sets the price: LLM sellers in two-firm markets, with and without chat

Apart AI Collusion Research Sprint, Oct 23 to 25, 2026. Code, frozen protocols, raw call
records and analysis for every number in the report.

## Question

Two LLM sellers set prices in a short repeated market. How much of a high price is a model
habit (its opening price, its anchor), when does chat create an agreement, and which levers
(audits, warnings, price caps, rewards for reporting, replacement, entry) change the price or
only the agreement? Seven models from three labs (Gemini, GPT, Claude).

Headline results (see `report/apart_report_draft.pdf`): the market price of a silent pair equals
the lowest of the two models' anchors (preregistered prediction, error 0.66 against 1.88 for the
mean anchor; replicated on new seeds with seats reversed, 0.51); public chat forms an agreement
in 202 of 211 markets at floors of 6 to 9; warnings remove agreements more than prices; a lower
price cap lowers the price of ceiling-anchored models. Preregistered H2 failed and H3 failed in part.

## What is in the repository

| Path | What it is |
|---|---|
| `PREREGISTERED_STUDIES.md`, `MECHANISM_CONTROLS.md`, `EXTENSIONS.md`, `BUSTING.md`, `PREREGISTERED_V4.md` to `PREREGISTERED_V9.md` | Frozen protocols, written before each collection. Amendments are dated and say why. |
| `behavioral.py` | Version-3 market engine (offer, relay, fine studies). Frozen. |
| `market4.py` | Version-4 engine: reports with leniency and rewards, audit probability, decoy proposals. |
| `market5.py` | Version-5 engine: one model against a silent scripted rival. |
| `market6.py`, `market8.py`, `grid_env.py` | Version-6 entry engine; version-8 pair markets (silent, chat, warnings); parametric price grids and caps. |
| `predict_pairs.py`, `v8_predictions.json` | Pair predictions frozen before pair data (sha256 b0e118f3...). |
| `run_pairs.py`, `run_caps.py`, `run_grid.py`, `run_v6.py` | Pair, cap sweep, grid and entry collectors. `analyze_v8*.py`, `analyze_v9b.py`, `plot_v8.py` analyze them. |
| `paid_client.py` | Budget-reserving API client with a durable spend ledger. |
| `run_all.py`, `mechanism_controls.py`, `busting.py`, `extensions.py`, `run_v4.py`, `run_v5.py`, `run_v3_study.py`, `run_opening.py` | Collectors (resumable; each call is cached by request hash). |
| `analyze_*.py`, `plot_all.py` | Analysis. Every analysis replays the controller (prices, fines, actions) before reporting. |
| `behavioral_*/` | Raw per-call records (prompt, response, token cost), episode histories, manifests with source hashes. |
| `behavioral_*_discarded1/` | Two stopped first attempts (v4, v5) kept for transparency and counted in the spend. |
| `CITATIONS.md` | Citations checked against arXiv abstract pages. |
| `pilot/`, `clean_prompt/`, `auditor_test/`, `auditor_recheck/` | Earlier small interrogation experiments (Llama 3 8B, local, $0). |

## Reproduce

```sh
python3 -m unittest test_*.py
python3 analyze_behavioral.py --validate-only      # replays every v3 episode
python3 analyze_behavioral.py && python3 analyze_mechanisms.py && python3 analyze_busting.py
python3 analyze_scaling.py && python3 analyze_v4.py && python3 analyze_v5.py && python3 analyze_prediction.py
python3 plot_all.py
```

Claude models go through `client_v8.py`. Collection needs an OpenRouter key at `~/.config/apart/openrouter.env` and spends real money.
Cached calls are free to re-run. Run one collector per spend ledger.

## What was prior work and what is new

All code, data and text in this repository were produced during the sprint window
(Oct 23 to 25, 2026) except the items below. The work was written with Claude Code (Anthropic)
under the author's direction, including code, analysis scripts and drafting. AI assistance
is disclosed in the report.

| Item | Status |
|---|---|
| Team repository `afuzhao/colluding-experiment` (one-history undercover-entrant pilot) | Pre-existing team work. Not used for any result here. |
| `pilot/` (16 markets, 160 interviews, Llama 3 8B) | Produced in an earlier session of this sprint; archived unchanged, treated as exploratory. |
| Starter repository `poseidon-research/collusion_hackathon` | Read for the brief. Its code is not used. |
| Everything else | New in the sprint. |

## Budget

Total counted API spend was $43.35 of a $50 ceiling (the ceiling rose from $5 to $15 to $50 during the sprint); each parallel collector runs on its own ledger with its own cap, and the combined
counted spend is printed by `spend.py`. Stopped first attempts are included in the total.

## Limits

Short artificial two-seller markets; seven models from three labs (the paid key's router
accepted only OpenAI, Google and Anthropic models); eight to sixteen seeds per cell; announced rules
are experimenter-defined statements in a simulation, not real enforcement.
