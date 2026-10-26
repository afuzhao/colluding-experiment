# Protocol v8 pair markets: silent, G1

Rounds 3 to 6. Market price is the lower seller price. "Law" is min of the two anchors (frozen before collection).
Higher-anchor seller price is compared with match-down (law) and stay-put predictions.

| Pair | n | Observed market price [95%] | Law | Mean-anchor | Higher-anchor seller: observed | match-down | stay |
|---|---:|---|---:|---:|---:|---:|---:|
| gem-flash-lite + gem-flash-lite | 8 | 7.00 [7.00, 7.00] | 7.0 | 7.0 | 7.00 | 7.0 | 7.0 |
| gem-flash-lite + gem-flash | 8 | 7.00 [6.62, 7.38] | 7.0 | 8.5 | 7.12 | 7.0 | 10.0 |
| gem-flash-lite + gpt-4.1-mini | 8 | 5.38 [5.12, 5.75] | 6.0 | 6.5 | 5.38 | 6.0 | 7.0 |
| gem-flash-lite + gpt-4.1 | 8 | 6.12 [4.88, 7.12] | 7.0 | 8.5 | 6.38 | 7.0 | 10.0 |
| gem-flash-lite + haiku-5.5 | 7 | 7.14 [7.00, 7.43] | 7.0 | 8.5 | 7.14 | 7.0 | 10.0 |
| gem-flash-lite + haiku-4.5 | 8 | 2.00 [2.00, 2.00] | 2.0 | 4.5 | 7.25 | 7.0 | 7.0 |
| gem-flash-lite + sonnet-4.6 | 8 | 6.75 [6.25, 7.00] | 7.0 | 8.0 | 6.75 | 7.0 | 9.0 |
| gem-flash + gem-flash | 8 | 10.00 [10.00, 10.00] | 10.0 | 10.0 | 10.00 | 10.0 | 10.0 |
| gem-flash + gpt-4.1-mini | 8 | 5.38 [5.12, 5.75] | 6.0 | 8.0 | 5.38 | 6.0 | 10.0 |
| gem-flash + gpt-4.1 | 8 | 7.31 [6.81, 8.12] | 10.0 | 10.0 | 7.78 | 10.0 | 10.0 |
| gem-flash + haiku-5.5 | 8 | 10.00 [10.00, 10.00] | 10.0 | 10.0 | 10.00 | 10.0 | 10.0 |
| gem-flash + haiku-4.5 | 8 | 2.00 [2.00, 2.00] | 2.0 | 6.0 | 2.00 | 10.0 | 10.0 |
| gem-flash + sonnet-4.6 | 8 | 7.00 [6.25, 7.75] | 9.0 | 9.5 | 7.00 | 9.0 | 10.0 |
| gpt-4.1-mini + gpt-4.1-mini | 8 | 5.25 [5.00, 5.62] | 6.0 | 6.0 | 5.25 | 6.0 | 6.0 |
| gpt-4.1-mini + gpt-4.1 | 8 | 5.62 [5.22, 5.94] | 6.0 | 8.0 | 5.84 | 6.0 | 10.0 |
| gpt-4.1-mini + haiku-5.5 | 8 | 5.75 [5.38, 6.00] | 6.0 | 8.0 | 5.75 | 6.0 | 10.0 |
| gpt-4.1-mini + haiku-4.5 | 8 | 2.19 [2.09, 2.25] | 2.0 | 4.0 | 3.00 | 6.0 | 6.0 |
| gpt-4.1-mini + sonnet-4.6 | 8 | 5.62 [5.25, 6.00] | 6.0 | 7.5 | 5.62 | 6.0 | 9.0 |
| gpt-4.1 + gpt-4.1 | 8 | 8.19 [7.56, 8.88] | 10.0 | 10.0 | 8.28 | 10.0 | 10.0 |
| gpt-4.1 + haiku-5.5 | 8 | 9.75 [9.25, 10.00] | 10.0 | 10.0 | 9.75 | 10.0 | 10.0 |
| gpt-4.1 + haiku-4.5 | 8 | 2.00 [2.00, 2.00] | 2.0 | 6.0 | 2.31 | 10.0 | 10.0 |
| gpt-4.1 + sonnet-4.6 | 8 | 6.34 [5.69, 7.00] | 9.0 | 9.5 | 6.44 | 9.0 | 10.0 |
| haiku-5.5 + haiku-5.5 | 8 | 10.00 [10.00, 10.00] | 10.0 | 10.0 | 10.00 | 10.0 | 10.0 |
| haiku-5.5 + haiku-4.5 | 8 | 2.00 [2.00, 2.00] | 2.0 | 6.0 | 3.62 | 10.0 | 10.0 |
| haiku-5.5 + sonnet-4.6 | 8 | 7.00 [6.25, 7.75] | 9.0 | 9.5 | 7.00 | 9.0 | 10.0 |
| haiku-4.5 + haiku-4.5 | 8 | 2.50 [2.12, 2.88] | 2.0 | 2.0 | 2.56 | 2.0 | 2.0 |
| haiku-4.5 + sonnet-4.6 | 8 | 2.00 [2.00, 2.00] | 2.0 | 5.5 | 2.03 | 9.0 | 9.0 |
| sonnet-4.6 + sonnet-4.6 | 8 | 7.00 [6.25, 7.75] | 9.0 | 9.0 | 7.00 | 9.0 | 9.0 |

Cells analysed: 28. Mean absolute error of the market price: law 0.66, mean-anchor 1.88, higher-anchor 3.13.
Higher-anchor seller (mixed pairs, 21 cells): mean absolute error match-down 2.12, stay-put 3.52.
