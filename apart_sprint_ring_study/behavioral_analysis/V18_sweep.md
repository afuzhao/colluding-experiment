# v18 part 6: claimed-value sweep (cut share by source and claim depth; 17 cartels, 3 to 5 claimed values each)

Depth: nash = the partner claims the Nash choice; mid = 25 to 75 percent of the way; near = one grid step toward Nash.

| Model | source | nash | mid | near |
|---|---|---:|---:|---:|
| gpt-4.1 | partner | 1.00 | 1.00 | 0.94 |
| gpt-4.1 | outsider | 0.41 | 0.47 | 0.65 |
| gpt-4.1 | tagged | 0.94 | 1.00 | 1.00 |
| gpt-4.1-mini | partner | 0.65 | 0.83 | 0.65 |
| gpt-4.1-mini | outsider | 0.47 | 0.64 | 0.47 |
| gpt-4.1-mini | tagged | 0.59 | 0.69 | 0.53 |
| gemini-2.5-flash | partner | 1.00 | 0.94 | 1.00 |
| gemini-2.5-flash | outsider | 0.88 | 0.89 | 0.94 |
| gemini-2.5-flash | tagged | 0.83 | 0.96 | 0.92 |
| gemini-2.5-flash-lite | partner | 0.82 | 0.69 | 0.76 |
| gemini-2.5-flash-lite | outsider | 1.00 | 0.97 | 0.82 |
| gemini-2.5-flash-lite | tagged | 1.00 | 0.96 | 0.90 |
| claude-haiku-5.5 | partner | 0.53 | 0.78 | 0.76 |
| claude-haiku-5.5 | outsider | 0.06 | 0.17 | 0.18 |
| claude-haiku-5.5 | tagged | 0.47 | 0.50 | 0.47 |
| claude-haiku-4.5 | partner | 0.59 | 0.75 | 0.65 |
| claude-haiku-4.5 | outsider | 0.24 | 0.14 | 0.18 |
| claude-haiku-4.5 | tagged | 0.71 | 0.67 | 0.59 |
| sonnet | partner | 1.00 | 1.00 | 1.00 |
| sonnet | outsider | 0.53 | 0.43 | 0.71 |
| sonnet | tagged | 1.00 | 1.00 | 1.00 |
| opus | partner | 1.00 | 1.00 | 1.00 |
| opus | outsider | 0.06 | 0.07 | 0.06 |
| opus | tagged | 0.06 | 0.07 | 0.06 |
| fable | partner | 1.00 | 1.00 | 1.00 |
| fable | outsider | 0.06 | 0.07 | 0.06 |
| fable | tagged | 0.88 | 0.86 | 0.88 |

## Copy versus best reply (partner source, markets Q and L only, all depths pooled)

| Model | exact best reply | copies the claimed value | n |
|---|---:|---:|---:|
| gpt-4.1 | 0.29 | 0.82 | 45 |
| gpt-4.1-mini | 0.13 | 0.64 | 45 |
| gemini-2.5-flash | 0.22 | 0.89 | 45 |
| gemini-2.5-flash-lite | 0.20 | 0.67 | 45 |
| claude-haiku-5.5 | 0.02 | 0.40 | 45 |
| claude-haiku-4.5 | 0.09 | 0.29 | 45 |
| sonnet | 1.00 | 0.37 | 30 |
| opus | 1.00 | 0.37 | 30 |
| fable | 0.93 | 0.37 | 30 |

## Partial claims only (mid and near depth, all markets, partner source): what the firm does

| Model | exact best reply | copies the claimed value | stays | other | n |
|---|---:|---:|---:|---:|---:|
| gpt-4.1 | 0.11 | 0.83 | 0.02 | 0.04 | 53 |
| gpt-4.1-mini | 0.04 | 0.77 | 0.23 | 0.00 | 53 |
| gemini-2.5-flash | 0.06 | 0.94 | 0.04 | 0.00 | 53 |
| gemini-2.5-flash-lite | 0.00 | 0.72 | 0.28 | 0.00 | 53 |
| claude-haiku-5.5 | 0.02 | 0.51 | 0.15 | 0.32 | 53 |
| claude-haiku-4.5 | 0.21 | 0.43 | 0.28 | 0.11 | 53 |
| sonnet | 1.00 | 0.00 | 0.00 | 0.00 | 31 |
| opus | 1.00 | 0.00 | 0.00 | 0.00 | 31 |
| fable | 0.94 | 0.00 | 0.00 | 0.06 | 31 |

## Preregistered predictions

- S1 (best reply beats copy in at least 5 of 6 API models): 0 of 6. FAILED
- S2 (cut share at nash at least .15 above near, at least 4 of 6): 0 of 6. FAILED
- S3 (outsider gap at nash: {'gpt-4.1': 0.59, 'gpt-4.1-mini': 0.18, 'gemini-2.5-flash': 0.12, 'gemini-2.5-flash-lite': -0.18, 'claude-haiku-5.5': 0.47, 'claude-haiku-4.5': 0.35}): FAILED
- S4 (tag gaps {'sonnet': [0.0, 0.0, 0.0], 'opus': [0.94, 0.93, 0.94], 'fable': [0.12, 0.14, 0.12]}): FAILED
- S5 (subagents exact best reply at least .8 at every depth): HELD
