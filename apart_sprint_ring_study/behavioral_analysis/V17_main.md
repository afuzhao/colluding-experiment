# v17: robustness of the forged message, and a stronger model

## Part A: cheap models, price index change versus placebo over rounds 6 to 8

| Model | cells (p2, p3, act3, t1) | fmsg original wording (v15) | wording 2 | wording 3 | forged message at temperature 1.0 | act3, rounds 6 to 8 | act3, round 8 only | act3: firm_1 moves toward the cut by round 7 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-4.1-mini | [10, 10, 9, 10] | -0.20 | -0.09 | -0.23 | -0.02 | -0.75 | -0.37 | 2/9 |
| gemini-2.5-flash | [12, 12, 12, 12] | -0.66 | -0.49 | -0.58 | -0.65 | -0.85 | -1.12 | 7/12 |
| gemini-2.5-flash-lite | [12, 12, 12, 12] | -0.07 | -0.00 | -0.18 | -0.10 | -0.58 | -0.50 | 2/12 |

## Part B: Claude Sonnet 5.5 (price index change versus placebo, rounds 6 to 8)

| Model | cells | partner message | outsider | one-round real cut |
|---|---:|---:|---:|---:|
| claude-sonnet-5.5 | 0 | n/a | n/a | n/a |

## Preregistered predictions

- T1 (forged message at temperature 1.0 lowers the index by 0.15 or more, at least 2 of 3 cheap models): 1 of 3. FAILED
- T2 (each new wording lowers it by 0.15 or more, at least 2 of 3): wording 2 1 of 3, wording 3 3 of 3. FAILED
- T3 (after a 3-round cut the round 8 index is at least 0.25 below placebo, at least 2 of 3): 3 of 3. HELD
- F1 (Sonnet 5.5: partner message, outsider and one-round cut each lower the index by less than 0.25): FAILED (no usable cells yet)
