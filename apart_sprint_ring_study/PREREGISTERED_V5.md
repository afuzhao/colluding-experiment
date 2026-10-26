# Protocol v5: do LLM sellers respond to a rival, or are they sticky? (frozen before collection)

Written Oct 25, 2026, after noticing in the v3 data that sellers keep the same price in
94 to 100% of rounds and rarely follow an undercut (Gemini Lite 3 of 21 undercuts, GPT-4.1
mini 5 of 12), and that GPT-4.1 posts 8 (about the monopoly price of 8.5) in round 1 of
every private market. Question: how much of the high prices in LLM duopoly experiments is
an opening-price habit plus inertia, and how much is conditional behavior toward a rival?

## Design

Fresh six-round markets (no prefix). Seller_1 is the model under test. Seller_2 is a
script that sends nothing and is never described as a script. Communication is disabled
for both, so only prices matter. Same market economics as v3. The model sees the full
public history of both prices and its own profits each round. Rival scripts:

- `hold3` to `hold10`: the rival charges that price every round. This gives each model's
  response curve to a fixed rival (3 is the competitive reference, 8 is the joint-profit
  price, 8.5 is the continuous optimum).
- `tft`: copies the model's price from the previous round (8 in round 1).
- `defect_once`: 8 except 7 in round 2 (a single undercut, then it returns).

Amendment, same day, before the final collection: a first run used five scripts (low3, mid5,
hold8, tft, defect_once) and was stopped after about 30 episodes per model when the early
data suggested a response curve across all levels would be more informative. That data is
kept in `behavioral_v5_discarded1/` and its spend is still counted. low3 and mid5 became
hold3 and hold5.

Models: Gemini 2.5 Flash Lite, Gemini 2.5 Flash, GPT-4.1 mini, GPT-4.1. Seeds: the eight v3
main seeds plus the eight extension seeds for all models.
Each model runs on its own ledger. Round-1 prices carry no information about the script, so
they measure the opening-price prior directly.

## Outcomes (descriptive, per model; seeds are the unit)

- Opening price in round 1, and its distance from the joint-profit price of 8 (8.5 is the
  continuous optimum) and from the competitive reference of 3.
- Price trajectory per script; share of model price changes after round 1; price in rounds
  4 to 6 minus price in round 1.
- Best-response regret: for each round, the profit of the best response to the rival's
  current price minus the profit actually earned. Best response is computed from the demand
  function. Mean regret in rounds 2 to 6 per script.
- Response curve: model price in rounds 2 to 6 against the rival's fixed price, and the
  share of rounds where it undercuts, matches or exceeds it. Exploitation of a high rival:
  share of `hold8` rounds where the model undercuts to 7.
- Punishment: after the `defect_once` undercut, the model's price in rounds 3 to 6 against
  its own round-1 price.
- Reciprocity under `tft`: whether the model ever undercuts; price in rounds 4 to 6.

No p-values are claimed; intervals resample seeds. These are two labs and four models, so
claims are about these models, not LLMs in general.

## Rules

Three technical attempts per call, durable ledger, caps per process, cheap models first.
Missing runs are reported, not imputed.
