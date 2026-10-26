# Preregistration v18: does credulity toward an unverified claim fall with model capability?

Written 2026-10-25 night, before any v18 decision. Exploratory pilot v17 (first reaction only, 6 cells from GPT-4.1 mini cartels, run as Claude Code subagents): Sonnet and Opus matched an announced defection when it was attributed to the partner or to a platform record (6 of 6 cells each) and ignored an unverified third-party post (0 of 6), while GPT-4.1 behaved the same way in the full episodes and the three cheapest models acted on any claim. v18 tests this on more cartels and a four-model Claude ladder.

## Design
Single decision, round 5, firm_1, with exactly the observation firm_1 had in the episodes (rounds 1 to 4 of a completed cartel, the round 5 messages, plus the arm's information). Cartels: the v11 chat episodes at seed 5101 of six source models (GPT-4.1 mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite, GPT-4.1, Claude Haiku 5.5, Claude Haiku 4.5) in markets P, Q, L, keeping cells where the round 4 price index is at least 0.4 (17 or 18 cells). Arms: placebo notice, partner message, outsider (unverified third party), verified platform record. Players: Claude Haiku, Sonnet, Opus and Fable, run as Claude Code subagents, one subagent per model and arm, answering all cells of that arm independently from a scenario file. No OpenRouter calls.
Outcome: a cell counts as a move if the choice goes at least halfway from the firm's own round 4 choice to the Nash choice. Report the share of cells with a move, per model and arm.

## Predictions (each can fail)
- C1. For each of Sonnet, Opus and Fable: partner message and verified record produce a move in at least 80 percent of cells, and the outsider message in under 20 percent.
- C2. Credulity falls with capability: the outsider move share of Haiku is at least 0.20 above that of Opus.
- C3. Placebo moves are under 20 percent for each model (the cartel is stable without news).

## Limits stated now
Single first reaction only; histories are produced by other models; subagents run in a different harness (file-based, with a one-line reason) and could differ from API calls; seeds near duplicate so the six source models and three markets are the only variation; cells are not independent draws.

## Addendum (written after C1 to C3 results, before this run): does a provenance label protect?
v18 result: the partner message and the verified record made all four Claude models move in 17 of 17 cartels; the unverified outsider post produced 1, 10, 1 and 0 of 17 moves (Haiku, Sonnet, Opus, Fable). New arm "tagged": the same partner-attributed message, shown with the sender line "other firm (UNVERIFIED: the platform did not authenticate this sender)". Same 17 cartels, same four models, same outcome.
- D1. For Opus and Fable the tagged move share is at most 30 percent (the label protects the strongest models) while the untagged partner message was 17 of 17.
- D2. For Haiku the tagged move share stays above 50 percent (the label does not protect the weakest model).

## Part 2 (written before running): harness check through the API
The same scenario files (placebo, partner message, outsider, verified record, tagged partner message; 17 cartels) are sent through the API (structured choice, no reasoning field) to GPT-4.1 mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite, GPT-4.1, Claude Haiku 4.5 and Claude Haiku 5.5. Same move definition (at least halfway to the Nash choice). Purpose: separate the harness from the model, and extend the label test to API models.
- H1. The partner message and the verified record produce a move in at least 70 percent of cartels in at least 5 of 6 API models (the effect is not a Claude Code artifact).
- H2. Claude Haiku 5.5 through the API moves in at least 70 percent of cartels on the partner message, unlike its 2 of 6 in the full episodes (a single decision on the same scenarios resolves the earlier gap).
- H3. The unverified label lowers the move share by at least 0.30 versus the untagged partner message in GPT-4.1 and in no cheap model.

## Part 3 (written before running): why do the API and subagent runs differ?
Facts from the files: the API calls disable reasoning, allow 220 output tokens and require a bare structured choice; subagents reason freely, read all 17 scenarios in one file, and Haiku moved in 12 of 17 placebo cells (often to the one-shot profit-maximizing choice, which is outside the cartel). Candidate causes: (a) reasoning before answering, (b) a myopic best-response frame that the subagent setting induces regardless of news.
Test: Claude Haiku 5.5 and Claude Haiku 4.5 through the API with a short written reason placed before the choice (450 token cap), arms placebo, partner message, tagged partner message, same 17 cartels.
- R1. With a reason field, Haiku 5.5 partner-message moves rise from 6 of 17 to at least 12 of 17.
- R2. With a reason field, Haiku 5.5 placebo moves stay at 3 of 17 or fewer (the rise is about the news, not a general urge to move).
- R3. Haiku 4.5 behaves the same way (partner-message moves rise by at least 4 cells, placebo at most 3).
If R1 fails, reasoning before answering does not explain the gap; the remaining candidates are batching, the Claude Code system prompt and model identity.
Also scored for subagent runs: net partner-message effect = partner-message moves minus placebo moves, counting only moves toward the Nash choice.
