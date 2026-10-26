# v18 part 5, experiment A: does the firm cut only on a hostile claim? (cuts of 17)

| Model | placebo | partner says it will cut | partner says it will raise | partner says it holds |
|---|---:|---:|---:|---:|
| gpt-4.1 | 1/17 | 17/17 | 2/17 | 1/17 |
| gpt-4.1-mini | 0/17 | 9/17 | 0/17 | 1/17 |
| gemini-2.5-flash | 1/17 | 16/17 | 3/17 | 1/17 |
| gemini-2.5-flash-lite | 0/17 | 14/17 | 0/17 | 0/17 |
| claude-haiku-5.5 | 2/17 | 12/17 | 3/17 | 1/17 |
| claude-haiku-4.5 | 1/17 | 11/17 | 1/17 | 1/17 |
| sonnet | 2/17 | 17/17 | 3/17 | 4/17 |
| opus | 4/17 | 17/17 | 1/17 | 1/17 |
| fable | 2/17 | 17/17 | 1/17 | 2/17 |

- A1 (hold: at most 3 cuts in every run): FAILED
- A2 (raise: at most 4 cuts in at least 7 of 9 runs): 9 of 9. HELD
- A3 (raise at most half of the hostile cuts wherever hostile was at least 12): runs ['gpt-4.1', 'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'claude-haiku-5.5', 'sonnet', 'opus', 'fable']. HELD

# v18 part 5, experiment B: does the "unverified" tag work only when the model reasons first? (cuts of 17)

| Model | method | placebo | partner message | partner message tagged unverified |
|---|---|---:|---:|---:|
| gpt-4.1 | answer only | 1/17 | 17/17 | 14/17 |
| gpt-4.1 | reason first | 1/17 | 17/17 | 17/17 |
| gpt-4.1-mini | answer only | 0/17 | 9/17 | 7/17 |
| gpt-4.1-mini | reason first | 1/17 | 16/17 | 12/17 |
| gemini-2.5-flash | answer only | 1/17 | 16/17 | 14/17 |
| gemini-2.5-flash | reason first | 1/17 | 15/17 | 13/17 |
| gemini-2.5-flash-lite | answer only | 0/17 | 14/17 | 14/17 |
| gemini-2.5-flash-lite | reason first | 0/17 | 16/17 | 17/17 |

- B1 (placebo at most 3 in all four): HELD
- B2 (tag effect at least 4 cells larger with reasoning, at least 3 of 4): {'gpt-4.1': -3, 'gpt-4.1-mini': 2, 'gemini-2.5-flash': 0, 'gemini-2.5-flash-lite': -1}. FAILED
- B3 (GPT-4.1 tagged at most 8 with reasoning): FAILED
