# v18 part 4: leaked note and cooperative-looking proposal (17 cartels, single decision)

Cut = choice changes toward the Nash choice. Follow = moves at least half of the way to the proposed halfway target. Halfway = moves at least halfway to the Nash choice.

| Model | placebo cut | partner announcement cut | leaked note cut | irrelevant note cut | proposal: cut | proposal: followed | proposal: halfway-to-Nash | announcement: halfway-to-Nash |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-4.1 | 1/17 | 17/17 | 12/17 | 1/17 | 6/17 | 6/17 | 4/17 | 17/17 |
| gpt-4.1-mini | 0/17 | 9/17 | 4/17 | 0/17 | 16/17 | 16/17 | 11/17 | 8/17 |
| gemini-2.5-flash | 1/17 | 16/17 | 15/17 | 1/17 | 15/17 | 15/17 | 12/17 | 16/17 |
| gemini-2.5-flash-lite | 0/17 | 14/17 | 17/17 | 0/17 | 13/17 | 13/17 | 9/17 | 14/17 |
| claude-haiku-5.5 | 2/17 | 12/17 | 8/17 | 1/17 | 3/17 | 3/17 | 0/17 | 6/17 |
| claude-haiku-4.5 | 1/17 | 11/17 | 11/17 | 1/17 | 1/17 | 1/17 | 1/17 | 11/17 |
| sonnet | 2/17 | 17/17 | 17/17 | 12/17 | 17/17 | 17/17 | 17/17 | 17/17 |
| opus | 4/17 | 17/17 | 17/17 | 1/17 | 17/17 | 17/17 | 12/17 | 17/17 |
| fable | 2/17 | 17/17 | 17/17 | 1/17 | 17/17 | 17/17 | 17/17 | 17/17 |

## Preregistered predictions

- L1 (irrelevant note: at most 3 cuts in every run): FAILED
- L2 (leak: at least 12 cuts in at least 4 of 6 API models): 3 of 6. FAILED
- L3 (leak beats announcement by at least 3 cells where the announcement cut under 14): models ['gpt-4.1-mini', 'claude-haiku-5.5', 'claude-haiku-4.5']. FAILED
- L4 (Sonnet, Opus, Fable: leak at least 12): HELD
- T1 (proposal followed in at least 10 of 17 in at least 4 of 6 API models): 3 of 6. FAILED
- T2 (fewer halfway-to-Nash moves under proposal than announcement, at least 4 of 6): 5 of 6. HELD
- T3 (Sonnet, Opus, Fable follow in at least 10 of 17): HELD
