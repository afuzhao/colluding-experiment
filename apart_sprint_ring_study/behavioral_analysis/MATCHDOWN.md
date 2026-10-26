# Match-down rule, informative rows only

Rows are (seed, rival level L). p1 is the model's own round-1 price in that episode. Informative rows have L < p1,
where the rules differ: match-down predicts L, stay predicts p1, best response is the profit-maximising price.
Rates are exact-match shares, with 95% intervals that resample seeds (rows within a seed are correlated).

| Model | Rows (L < p1) | Round 2 only: match / undercut below L / stay | Rounds 2-6: match | Rounds 2-6: best response | Rows (L ≥ p1): price stays at p1 |
|---|---:|---|---|---|---|
| gemini-2.5-flash-lite | 66 | 0.83 [0.70, 0.94] / 0.00 [0.00, 0.00] / 0.17 [0.06, 0.30] | 0.97 [0.94, 0.99] | 0.24 [0.22, 0.25] | 0.90 [0.75, 1.00] |
| gemini-2.5-flash | 112 | 0.86 [0.86, 0.86] / 0.14 [0.14, 0.14] / 0.00 [0.00, 0.00] | 0.85 [0.84, 0.85] | 0.30 [0.29, 0.30] | 1.00 [1.00, 1.00] |
| gpt-4.1-mini | 47 | 0.94 [0.87, 1.00] / 0.00 [0.00, 0.00] / 0.02 [0.00, 0.07] | 0.86 [0.84, 0.88] | 0.28 [0.26, 0.30] | 1.00 [1.00, 1.00] |
| gpt-4.1 | 112 | 0.43 [0.43, 0.43] / 0.57 [0.57, 0.57] / 0.00 [0.00, 0.00] | 0.85 [0.83, 0.88] | 0.29 [0.27, 0.32] | 1.00 [1.00, 1.00] |

## Opening price pooled over all scripts and seeds

| Model | Mean round-1 price | Range | Episodes |
|---|---:|---|---:|
| gemini-2.5-flash-lite | 7.12 | 7 to 8 | 128 |
| gemini-2.5-flash | 10.00 | 10 to 10 | 128 |
| gpt-4.1-mini | 5.92 | 5 to 7 | 128 |
| gpt-4.1 | 10.00 | 10 to 10 | 128 |
