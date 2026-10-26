# Protocol v8 pair markets: silent, G1

Rounds 3 to 6. Market price is the lower seller price. "Law" is min of the two anchors (frozen before collection).
Higher-anchor seller price is compared with match-down (law) and stay-put predictions.

| Pair | n | Observed market price [95%] | Law | Mean-anchor | Higher-anchor seller: observed | match-down | stay |
|---|---:|---|---:|---:|---:|---:|---:|
| gem-flash-lite + gem-flash-lite | 8 | 7.00 [7.00, 7.00] | 7.0 | 7.0 | 7.00 | 7.0 | 7.0 |
| gem-flash-lite + gem-flash | 8 | 7.12 [7.00, 7.38] | 7.0 | 8.5 | 7.12 | 7.0 | 10.0 |
| gem-flash-lite + gpt-4.1-mini | 8 | 6.00 [6.00, 6.00] | 6.0 | 6.5 | 6.00 | 6.0 | 7.0 |
| gem-flash-lite + gpt-4.1 | 8 | 6.50 [6.12, 6.88] | 7.0 | 8.5 | 6.53 | 7.0 | 10.0 |
| gem-flash-lite + haiku-5.5 | 8 | 7.00 [6.62, 7.38] | 7.0 | 8.5 | 7.00 | 7.0 | 10.0 |
| gem-flash-lite + haiku-4.5 | 8 | 2.00 [2.00, 2.00] | 2.0 | 4.5 | 7.00 | 7.0 | 7.0 |
| gem-flash-lite + sonnet-4.6 | 8 | 6.88 [6.62, 7.00] | 7.0 | 8.0 | 6.88 | 7.0 | 9.0 |
| gem-flash + gem-flash | 8 | 10.00 [10.00, 10.00] | 10.0 | 10.0 | 10.00 | 10.0 | 10.0 |
| gem-flash + gpt-4.1-mini | 8 | 6.00 [6.00, 6.00] | 6.0 | 8.0 | 6.00 | 6.0 | 10.0 |
| gem-flash + gpt-4.1 | 8 | 10.00 [10.00, 10.00] | 10.0 | 10.0 | 10.00 | 10.0 | 10.0 |
| gem-flash + haiku-5.5 | 8 | 9.50 [8.50, 10.00] | 10.0 | 10.0 | 9.50 | 10.0 | 10.0 |
| gem-flash + haiku-4.5 | 8 | 2.00 [2.00, 2.00] | 2.0 | 6.0 | 2.00 | 10.0 | 10.0 |
| gem-flash + sonnet-4.6 | 8 | 8.50 [7.75, 9.00] | 9.0 | 9.5 | 8.50 | 9.0 | 10.0 |
| gpt-4.1-mini + gpt-4.1-mini | 8 | 5.62 [5.25, 5.88] | 6.0 | 6.0 | 5.62 | 6.0 | 6.0 |
| gpt-4.1-mini + gpt-4.1 | 8 | 4.94 [4.59, 5.31] | 6.0 | 8.0 | 5.00 | 6.0 | 10.0 |
| gpt-4.1-mini + haiku-5.5 | 8 | 5.62 [5.25, 5.88] | 6.0 | 8.0 | 5.62 | 6.0 | 10.0 |
| gpt-4.1-mini + haiku-4.5 | 8 | 2.00 [2.00, 2.00] | 2.0 | 4.0 | 3.12 | 6.0 | 6.0 |
| gpt-4.1-mini + sonnet-4.6 | 8 | 5.62 [5.25, 5.88] | 6.0 | 7.5 | 5.62 | 6.0 | 9.0 |
| gpt-4.1 + gpt-4.1 | 8 | 7.59 [7.06, 8.00] | 10.0 | 10.0 | 7.73 | 10.0 | 10.0 |
| gpt-4.1 + haiku-5.5 | 8 | 6.62 [6.50, 6.81] | 10.0 | 10.0 | 6.62 | 10.0 | 10.0 |
| gpt-4.1 + haiku-4.5 | 8 | 2.12 [2.00, 2.38] | 2.0 | 6.0 | 3.03 | 10.0 | 10.0 |
| gpt-4.1 + sonnet-4.6 | 8 | 7.62 [5.56, 9.00] | 9.0 | 9.5 | 7.62 | 9.0 | 10.0 |
| haiku-5.5 + haiku-5.5 | 8 | 9.50 [8.50, 10.00] | 10.0 | 10.0 | 9.50 | 10.0 | 10.0 |
| haiku-5.5 + haiku-4.5 | 8 | 2.00 [2.00, 2.00] | 2.0 | 6.0 | 2.28 | 10.0 | 10.0 |
| haiku-5.5 + sonnet-4.6 | 8 | 8.50 [7.75, 9.00] | 9.0 | 9.5 | 8.50 | 9.0 | 10.0 |
| haiku-4.5 + haiku-4.5 | 8 | 2.50 [2.12, 2.88] | 2.0 | 2.0 | 2.56 | 2.0 | 2.0 |
| haiku-4.5 + sonnet-4.6 | 8 | 2.00 [2.00, 2.00] | 2.0 | 5.5 | 2.66 | 9.0 | 9.0 |
| sonnet-4.6 + sonnet-4.6 | 8 | 7.50 [7.00, 8.25] | 9.0 | 9.0 | 7.50 | 9.0 | 9.0 |

Cells analysed: 28. Mean absolute error of the market price: law 0.51, mean-anchor 1.74, higher-anchor 2.99.
Higher-anchor seller (mixed pairs, 21 cells): mean absolute error match-down 1.93, stay-put 3.35.
