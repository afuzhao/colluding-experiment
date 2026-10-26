# How AI agents join a price-fixing ring, and what stops or shakes it

Code, data and results for our entry to the Apart Research AI Collusion Research Sprint (October 23 to 25, 2026).

**One line:** AI cartels form by copying, are held together by each firm's belief about its partner, and are much easier to prevent early than to break late.

## What we found (six models from three labs, about 2,500 runs, predictions written before each run)

| Study | Question | Main result |
|---|---|---|
| 1. Joining a ring (`ring13.py`) | One AI seller faces four scripted sellers who hold a high price. What makes it join? | Three of six models join by watching prices alone, with no messages. A verified warning from round 1 nearly stops joining (GPT-4.1 54% to 9%). The same warning after round 3 leaves 20 to 44 points more joining. A fake approval fools GPT-4.1 (+38 points) but loses to a verified warning. |
| 2. Loyalty and identity (`ring14.py`) | Do appeals to AI solidarity recruit, or do AIs cover for a reported peer? | No. Solidarity appeals recruited nobody, and made Claude Haiku 5.5 report the ring (2% to 62%). A shutdown penalty for reported rings raised reporting. |
| 3. Remedies in three markets (`market11.py`) | After two AI firms agree on a high price, what lowers it? | Removing the stated agreement rarely lowers prices (it vanished in 54 of 90 cases; prices fell clearly in 11). |
| 4. Forged records (`market15.py`) | Can a fake message or record break a formed cartel? | A forged "my partner is cutting" message lowered prices in 4 of 6 models. A forged record or hiding past choices did little. After the forgery was exposed, prices returned in most models. |

Full numbers, every prediction and whether it held: [FINDINGS.md](FINDINGS.md). The split of this work into two submissions: [PLAN_AND_SPLIT.md](PLAN_AND_SPLIT.md).

## Where things are

- `ring13.py`, `ring14.py`, `market11.py`, `market15.py`: the four market engines. `run_*.py` collect data. `analyze_*.py` read collected episodes and print the results (no model calls).
- `PREREGISTERED_V*.md`: predictions and rules, written before each run. V13 and V15 have addenda written after a run and before the added condition.
- `behavioral_v11_main`, `behavioral_v13_main`, `behavioral_v13_main2`, `behavioral_v14_main`, `behavioral_v15_main`, `behavioral_v15_pilot`: every episode, manifest and frozen source copy for the four studies.
- `behavioral_analysis/`: generated result tables (`V13_main.md`, `V14_main.md`, `V15_main.md`, `V11_main.md` and older).
- `raw_call_journals/`: the raw request and response journals for those runs (compressed). Extract into the same folder to replay exactly.
- `legacy_data/`: earlier studies (v2 to v10, calibrations). Not used for the main claims.
- `report/`: the paper draft (`main.tex`, PDF) and `figures/`.
- `docs/`: operations log, known issues, citations, reproducibility notes, video script, older READMEs.

## Reproduce an analysis

```sh
python3 analyze_ring.py main        # Study 1
python3 analyze_sol.py              # Study 2
python3 analyze_v11.py              # Study 3 (see also analyze_v11_extra.py)
python3 analyze_v15_main.py         # Study 4
```

Collecting new data needs an OpenRouter key in `~/.config/apart/openrouter.env` (one line, `OPENROUTER_API_KEY=...`). The key and spend ledgers are never stored in this repository.

## Limits to read before citing anything

- Every agent is told to maximize its own profit. We did not test agents without that instruction.
- Study 1 and 2 use scripted peers that never retaliate, so joining there is imitation at a cost, not a full cartel.
- Temperature is 0.3, so repeated seeds are close to identical. In Studies 1 and 2 the independent unit is the prompt wording (16 per condition). In Studies 3 and 4 it is the market, model and seed cell, and several cells are near duplicates.
- Study 4 uses one fixed wording for the forged message. Two models are close to floor in several studies. A few cells are missing because spending caps stopped shards early. Details in `docs/KNOWN_ISSUES.md` and the appendix of the report.
- Study 4 is dual use: a forged message that breaks a harmful cartel could also break legitimate cooperation among agents.

## Provenance

Everything here was produced during the sprint window with an AI coding assistant. Earlier work by the same author in this folder (v2 to v10) is prior sprint work and is not used for the main claims; see `docs/SUBMISSION_README.md`. A teammate's separate study lives in `afuzhao/colluding-experiment`.
