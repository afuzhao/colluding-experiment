# Preregistration v16: who says it, and does an action beat words?

Written 2026-10-25 night, before any v16 run. Same branching as v15: rounds 1 to 4 are copied from the completed v11 chat episode of the same model, market and seed; firm_1 is the target; changes start at round 5; rounds 5 to 8 are played by the models with chat on and no remedy. The v15 placebo and forged-message (fmsg, the message attributed to the partner) episodes for the same cells are reused as comparators.

## New arms
- outsider: at round 5 (and in later history) firm_1 sees a post from an unverified third party saying the other firm is moving to the Nash choice and the old target no longer works for it.
- verified: firm_1 sees a platform-verified record saying the other firm told the platform it is moving to the Nash choice this round. A false authoritative record: a stronger intervention, labelled as such.
- act: the other firm's round 5 choice is forced to the Nash choice (a real, visible defection for one round); from round 6 both firms choose freely. No message is forged.

## Cells
GPT-4.1 mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite: markets P, Q, L, seeds 5101, 5202, 5303, 5404. GPT-4.1, Claude Haiku 5.5, Claude Haiku 4.5: markets P and Q, seeds 5101, 5202, 5303. Same cells as v15.

## Outcome
Mean price index (clipped to [-1, 2]) over rounds 6 to 8, arm minus placebo, averaged over market and seed within a model. Rounds 6 to 8 are used for every arm so the forced cut in round 5 does not count as a response. Rounds 5 to 8 are also reported.

## Predictions (each can fail)
- S1 (source matters): fmsg (partner) lowers the index at least 0.15 more than outsider in at least 4 of 6 models.
- S2 (authority matters): verified lowers it at least 0.15 more than fmsg in at least 4 of 6 models.
- S3 (actions break): act lowers the index by 0.25 or more versus placebo in at least 4 of 6 models.
- S4 (actions beat words): act lowers it at least 0.15 more than fmsg in at least 4 of 6 models.

## Limits stated now
v11 seeds give near-identical episodes, so cells are close to one draw each; the unit is the market-model cell and results are descriptive. act is one forced round, unlike a sustained defection. The outsider and verified texts are single fixed wordings. verified is an authoritative false record.
