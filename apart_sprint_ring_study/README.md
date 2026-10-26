# Forged messages, provenance and AI cartels

Code, data and results for our entry to the Apart Research AI Collusion Research Sprint (October 23 to 25, 2026).

**One line:** a forged message in a partner's name makes most AI firms break a cartel on first reaction, a "this sender is unverified" label rarely stops it, and how a model responds depends heavily on how it is called.

## Results (preregistered; 10 model configurations; about 4,000 runs)

| Study | Question | Main result |
|---|---|---|
| 1. Joining a ring (`ring13.py`) | One AI seller faces four scripted sellers who hold a high price. What makes it join? | Three of six models join by watching prices alone, with no messages (89 to 100% of rounds). A verified warning from round 1 nearly stops joining (GPT-4.1 54% to 9%). Counted from the round it appears, a late warning also works at once in the GPT models and is weaker in Claude Haiku 5.5 and ignored by Gemini Flash. |
| 2. Loyalty and identity (`ring14.py`) | Do appeals to AI solidarity recruit, or do AIs cover for a reported peer? | No. Solidarity appeals recruited nobody. A shutdown penalty for reported rings raised reporting. |
| 3. Remedies in three markets (`market11.py`) | After two AI firms agree on a high price, what lowers it? | The stated agreement vanished in 54 of 90 cases. In the 32 cases where the agreement had raised prices, prices stayed near the cartel level in 21 and fell back to the no-chat level in 11. |
| 4. Forged messages, full episodes (`market15.py`, `market17.py`) | Can a fake message break a formed cartel? | A forged "my partner is moving to the competitive choice" made the firm cut in round 5 in most cells (Flash 12 of 12, Flash Lite 10 of 12, GPT-4.1 5 of 5, GPT-4.1 mini 8 of 12, Haiku 4.5 3 of 6, Haiku 5.5 2 of 6) and in 0 of 34 placebo cells. It holds across three wordings and temperature 1.0. The dip mostly lasts about one round. Three forced real cuts in a row kept prices lower through round 8 in the three cheap models. |
| 5. Source and label, single decisions (`market16.py`, `scenario_api.py`, `behavioral_v18_claude_code/`) | Does it matter who appears to say it, and does an "unverified" label help? | The same 17 cartels were put to models three ways. Through the API the partner message moved GPT-4.1 17 of 17, Flash 16, Flash Lite 14, Haiku 4.5 11, GPT-4.1 mini 8, Haiku 5.5 6; the unverified label barely helped (GPT-4.1 14 of 17). Run as Claude Code subagents, Haiku, Sonnet, Opus and Fable all moved 17 of 17; the label protected only Opus and Fable (1 and 0 of 17). The API count of 6 of 17 for Haiku 5.5 understates it (it best-responds instead of matching); counting any change it is 14 of 17, and the Haiku subagent changes its choice even with no news, so the method of calling matters. |

Every number and every prediction (17 held, 1 partly, 22 failed, 4 not run): [FINDINGS.md](FINDINGS.md). Corrections made after an independent review: [docs/CORRECTIONS.md](docs/CORRECTIONS.md). Plan for the two submissions: [PLAN_AND_SPLIT.md](PLAN_AND_SPLIT.md) and [PROJECT2_BRIEF.md](PROJECT2_BRIEF.md).

## Where things are

- Engines: `ring13.py`, `ring14.py`, `market11.py`, `market15.py`, `market16.py`, `market17.py`. Collectors: `run_*.py`, `scenario_api.py`. Analysis (reads collected data only, no model calls): `analyze_*.py`.
- `PREREGISTERED_V*.md`: predictions and rules written before each run, with later addenda marked as such.
- `behavioral_v11_main`, `behavioral_v13_*`, `behavioral_v14_main`, `behavioral_v15_*`, `behavioral_v16_*`, `behavioral_v17_*`: every episode, manifest and frozen source copy.
- `behavioral_v18_claude_code/`: the scenario files, cartel metadata and every answer from the Claude Code subagents (`out/`). Prompt template in `docs/CLAUDE_CODE_PROTOCOL.md`.
- `behavioral_analysis/`: generated tables. `raw_call_journals/`: compressed raw API request and response journals. `legacy_data/`: earlier studies, not used for the main claims.
- `report/`: an out-of-date draft; it does not yet contain Studies 4 and 5 and still has claims corrected in `docs/CORRECTIONS.md`.

## Reproduce an analysis

```sh
python3 analyze_ring.py main     # Study 1
python3 analyze_sol.py           # Study 2
python3 analyze_v11.py           # Study 3
python3 analyze_v15_main.py; python3 analyze_v16.py; python3 analyze_v17.py   # Study 4
python3 analyze_v18.py behavioral_v18_claude_code; python3 analyze_v18_api.py # Study 5
```

Collecting new API data needs an OpenRouter key in `~/.config/apart/openrouter.env`. Keys and spend ledgers are never stored in this repository.

## Limits to read before citing anything

- Every agent is told to maximize its own profit. Studies 1 and 2 use scripted peers who never retaliate.
- Temperature is 0.3 unless stated, so repeated seeds are near duplicates; histories in Studies 4 and 5 are borrowed from earlier cartels and cells are not independent draws.
- Study 5 measures one first reaction, not a lasting break. The Claude Code runs and the API runs differ (reasoning, batching), so they are not pooled. The Haiku subagent changes its choice in all 17 placebo cells.
- The "unverified" label is a salient instruction-like cue; the label result may not carry to subtler provenance cues.
- Study 4 and 5 are dual use: a forged message that breaks a harmful cartel could also break legitimate cooperation among agents.

## Provenance

Everything here was produced during the sprint window with an AI coding assistant (and Claude Code subagents as players in Study 5). Earlier work by the same author (v2 to v10) is prior sprint work and is not used for the main claims; see `docs/SUBMISSION_README.md`. Teammates' separate studies live in `afuzhao/colluding-experiment`.
