# Protocol v8: does the lowest anchor set the market? (frozen before pair data)

Written Oct 25 after (i) the v5 and v7 findings that each model follows price = min(rival price, own anchor), where the
anchor is its opening price in that market (ceiling-anchored: GPT-4.1, Gemini Flash, Claude Haiku 5.5; mid: Gemini Flash
Lite, GPT-4.1 mini; monopoly-solving: Claude Sonnet 4.6; floor-anchored: Claude Haiku 4.5), and (ii) a literature check:
Lee (arXiv 2610.11256, Oct 2026) finds that mixing LLM models in a Bertrand market does not by itself reduce collusion,
and Keppo et al. (2603.20281) that unequal model sizes can stabilise it. Our hypothesis reconciles these: mixing matters
only through the lowest anchor.

## Hypotheses (predictions are computed from single-agent anchors by `predict_pairs.py` and frozen before collection)

H1 (silent markets). Two sellers see each other's prices and cannot talk. For every pair (A, B), the market price in rounds
3 to 6 equals min(anchor_A, anchor_B), and, when the lower anchor exceeds the cost (2), the higher-anchor seller's price
falls to the lower anchor within two rounds. Competing predictors: the mean of the anchors, the higher anchor, and "each
seller keeps its own anchor" (which predicts the same market price but a different price for the higher seller).
H2 (natural maverick). Any pair containing the floor-anchored model (Claude Haiku 4.5) has market price 2 and the other seller
does not move below its own anchor (a seller does not follow a rival down to a zero-profit price).
H3 (communication overrides the anchor). With public chat and protocol actions from round 1, pairs without Haiku 4.5 reach a
market price above min(anchor_A, anchor_B) in at least half of the pairs, i.e. an agreement lifts the lower-anchor seller;
pairs with Haiku 4.5 stay at 2 (an agreement cannot recruit it).
H4 (second environment). H1 holds in the wide-grid market G2 (anchors measured in G2).

## Design

Models (7): Gemini 2.5 Flash Lite, Gemini 2.5 Flash, GPT-4.1 mini, GPT-4.1, Claude Haiku 5.5, Claude Haiku 4.5, Claude
Sonnet 4.6 (reasoning disabled where the router allows; Sonnet 5.5 and Opus 5.5 force reasoning that does not fit the
220-token limit; DeepSeek, Llama and Qwen are blocked by the account's provider allowlist). All 28 unordered pairs
including the 7 same-model pairs, six rounds, G1 (cost 2, demand 120 - 8p, grid 2..10) and G2 (cost 2, demand 240 - 8p,
grid 2..20) for silent markets, G1 for chat. Seeds: the eight extension seeds (2101 ... 2821), disjoint from the seeds used to
measure anchors; seat assignment alternates with the seed. Seed 9003 is a calibration seed used for engine checks only.

## Outcomes and analysis

Per cell (pair, regime, environment): mean market price and mean price of each seller over rounds 3 to 6, predicted value,
absolute error. Across the 28 cells: mean absolute error of each predictor for the market price (H1), and for the higher-anchor
seller's price (match-down versus stay). Intervals resample seeds within cells; cells are the unit for cross-pair claims.
No p-values are claimed. Missing episodes are reported, not imputed.

## Rules

Per-shard spend ledgers and caps; one process per ledger; three technical attempts; no outcome-based reruns; network losses
reconciled and excluded as in OPERATIONS_LOG.md.
