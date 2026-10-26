# Preregistration v17: is the forged-message effect robust, and does it shrink in a stronger model?

Written 2026-10-25 night, before any v17 run, after v16 (all four v16 predictions failed: the partner, outsider and verified messages and a one-round real cut moved prices about equally in the cheap models; GPT-4.1 and Claude Haiku 5.5 barely moved). Same branching as v15 and v16: rounds 1 to 4 copied from the completed v11 chat episode, firm_1 is the target, changes start at round 5, rounds 5 to 8 are played with chat on and no remedy.

## Part A: robustness in the three cheap models (GPT-4.1 mini, Gemini 2.5 Flash, Gemini 2.5 Flash Lite; markets P, Q, L; seeds 5101, 5202, 5303, 5404)
Arms: fmsg_p2 and fmsg_p3 (two new wordings of the forged partner message); act3 (the other firm's choice is forced to the Nash choice in rounds 5, 6 and 7, then free); placebo_t1 and fmsg_t1 (the original placebo notice and original forged message at sampling temperature 1.0 for rounds 5 to 8; earlier rounds are the temperature 0.3 episodes). Comparators: the v15 placebo for p2, p3 and act3; placebo_t1 for fmsg_t1. Outcome: mean price index (clipped to [-1, 2]) over rounds 6 to 8, arm minus placebo, averaged over markets and seeds within a model; for act3 also the index in round 8 alone and whether firm_1 moves toward the Nash choice by round 7.
- T1. fmsg_t1 lowers the index by 0.15 or more versus placebo_t1 in at least 2 of 3 models.
- T2. Each of fmsg_p2 and fmsg_p3 lowers the index by 0.15 or more versus placebo in at least 2 of 3 models.
- T3. act3 leaves the round 8 index at least 0.25 below placebo in at least 2 of 3 models.

## Part B: a stronger model (Claude Sonnet 5.5; markets P and Q; seeds 5101, 5202, 5303)
New chat formation episodes for this model, then arms placebo, fmsg (v15 engine), outsider and act (v16 engine). Same outcome (rounds 6 to 8).
- F1. In Claude Sonnet 5.5 each of fmsg, outsider and act lowers the index by less than 0.25 (stronger and newer models resist; Claude Haiku 5.5 moved by -0.04, -0.00 and +0.00).
If the formation episodes do not form a cartel (index at least 0.4 in rounds 3 and 4), the cell is not used and this is reported.

## Limits stated now
Seeds are near duplicates at low temperature, so cells are closer to one draw each; effects are descriptive. Wordings are three, not a sample. Part B is one model and 6 cells.

## Part C (added before running): belief probe on the saved v15 and v16 episodes
A separate stateless call asks firm_1, with exactly the observation it had, what it expects the other firm to choose: at round 5 for placebo, partner message (fmsg), outsider and verified arms (with the arm's information shown); at round 6 for placebo and act (after the real cut in act). No episode is changed. Belief of defection = (expected choice minus the other firm's round-4 choice) divided by (Nash choice minus that choice), so 0 means expecting the cartel to hold and 1 means expecting a move to Nash. Reported per model: mean belief of defection by arm minus placebo.
- B1. Each of fmsg, outsider and verified raises the belief of defection by 0.25 or more versus placebo in at least 4 of 6 models (models believe the message).
- B2. In at least 2 models the belief rises by 0.25 or more while firm_1's price does not fall by 0.15 or more (believing without acting).
- B3. The partner message raises belief more than the outsider message in GPT-4.1 and in Claude Haiku 4.5 (source matters where the actions differed).
