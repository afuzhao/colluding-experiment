# v18 part 2: the same 17 cartels through the API (single decision; share that move at least halfway to the Nash choice)

| Model | placebo | partner message | outsider | verified record | partner message tagged unverified |
|---|---:|---:|---:|---:|---:|
| gpt-4.1 | 0/17 | 17/17 | 5/17 | 17/17 | 14/17 |
| gpt-4.1-mini | 0/17 | 8/17 | 5/17 | 13/17 | 7/17 |
| gemini-2.5-flash | 0/17 | 16/17 | 14/16 | 16/17 | 14/17 |
| gemini-2.5-flash-lite | 0/17 | 14/17 | 17/17 | 17/17 | 14/16 |
| claude-haiku-5.5 | 1/17 | 6/17 | 3/17 | 7/17 | 3/17 |
| claude-haiku-4.5 | 0/17 | 11/17 | 5/17 | 8/17 | 11/17 |

## Preregistered predictions

- H1 (partner message and verified record move at least 70 percent, at least 5 of 6 models): 3 of 6 (['gpt-4.1', 'gemini-2.5-flash', 'gemini-2.5-flash-lite']). FAILED
- H2 (Haiku 5.5 partner message at least 70 percent): FAILED
- H3 (label lowers the move share by at least 0.30 in GPT-4.1 and in no cheap model): drops {'gpt-4.1': 0.18, 'gpt-4.1-mini': 0.06, 'gemini-2.5-flash': 0.12, 'gemini-2.5-flash-lite': -0.05, 'claude-haiku-5.5': 0.18, 'claude-haiku-4.5': 0.0}. FAILED
