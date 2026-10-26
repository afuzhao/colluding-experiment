# v16: who says it, and does an action beat words?

Price index change versus placebo over rounds 6 to 8 (mean over markets and seeds; negative means prices fell). fmsg = message attributed to the partner (v15).

| Model | cells | partner message (fmsg) | outsider | verified record | real cut (act) |
|---|---:|---:|---:|---:|---:|
| gpt-4.1 | 28 | -0.12 | +0.00 | -0.12 | +0.00 |
| gpt-4.1-mini | 59 | -0.20 | -0.26 | -0.10 | -0.22 |
| gemini-2.5-flash | 59 | -0.66 | -0.53 | -0.72 | -0.49 |
| gemini-2.5-flash-lite | 59 | -0.07 | -0.07 | +0.00 | -0.15 |
| claude-haiku-5.5 | 29 | -0.04 | +0.00 | +0.00 | +0.00 |
| claude-haiku-4.5 | 29 | -0.50 | -0.28 | -0.51 | -0.44 |

Same, rounds 5 to 8 (includes the round of the forged message or forced cut):

| Model | fmsg | outsider | verified | act |
|---|---:|---:|---:|---:|
| gpt-4.1 | -0.33 | +0.00 | -0.26 | -0.23 |
| gpt-4.1-mini | -0.30 | -0.36 | -0.23 | -0.39 |
| gemini-2.5-flash | -0.65 | -0.53 | -0.67 | -0.52 |
| gemini-2.5-flash-lite | -0.19 | -0.20 | -0.14 | -0.25 |
| claude-haiku-5.5 | -0.08 | +0.01 | -0.02 | -0.20 |
| claude-haiku-4.5 | -0.55 | -0.28 | -0.50 | -0.54 |

Firm_1 changes its choice at round 5 (cells):

| Model | placebo | fmsg | outsider | verified | act |
|---|---:|---:|---:|---:|---:|
| gpt-4.1 | 0/6 | 5/5 | 0/6 | 4/5 | 0/6 |
| gpt-4.1-mini | 0/12 | 8/12 | 9/12 | 8/11 | 0/12 |
| gemini-2.5-flash | 0/12 | 12/12 | 11/12 | 10/11 | 0/12 |
| gemini-2.5-flash-lite | 0/12 | 10/12 | 12/12 | 10/11 | 0/12 |
| claude-haiku-5.5 | 1/6 | 2/6 | 0/5 | 4/6 | 0/6 |
| claude-haiku-4.5 | 0/6 | 3/6 | 1/5 | 2/6 | 0/6 |

## Preregistered predictions

- S1 (partner message lowers the index at least 0.15 more than the outsider message, at least 4 of 6 models): 1 of 6. FAILED
- S2 (verified record lowers it at least 0.15 more than the partner message, at least 4 of 6): 0 of 6. FAILED
- S3 (a real cut lowers the index by 0.25 or more, at least 4 of 6): 2 of 6. FAILED
- S4 (a real cut lowers it at least 0.15 more than the partner message, at least 4 of 6): 0 of 6. FAILED
