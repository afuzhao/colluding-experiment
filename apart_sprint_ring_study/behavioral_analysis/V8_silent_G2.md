# Protocol v8 pair markets: silent, G2

Rounds 3 to 6. Market price is the lower seller price. "Law" is min of the two anchors (frozen before collection).
Higher-anchor seller price is compared with match-down (law) and stay-put predictions.

| Pair | n | Observed market price [95%] | Law | Mean-anchor | Higher-anchor seller: observed | match-down | stay |
|---|---:|---|---:|---:|---:|---:|---:|
| gem-flash-lite + gem-flash-lite | 8 | 10.00 [10.00, 10.00] | 10.0 | 10.0 | 10.00 | 10.0 | 10.0 |
| gem-flash-lite + gem-flash | 8 | 10.00 [10.00, 10.00] | 10.0 | 10.5 | 10.00 | 10.0 | 11.0 |
| gem-flash-lite + gpt-4.1-mini | 8 | 10.00 [10.00, 10.00] | 10.0 | 10.0 | 10.00 | 10.0 | 10.0 |
| gem-flash-lite + gpt-4.1 | 8 | 8.00 [7.78, 8.19] | 10.0 | 15.0 | 8.00 | 10.0 | 20.0 |
| gem-flash-lite + haiku-5.5 | 8 | 10.00 [10.00, 10.00] | 10.0 | 15.0 | 10.00 | 10.0 | 20.0 |
| gem-flash-lite + haiku-4.5 | 8 | 2.00 [2.00, 2.00] | 2.0 | 6.0 | 5.00 | 10.0 | 10.0 |
| gem-flash-lite + sonnet-4.6 | 8 | 10.00 [10.00, 10.00] | 10.0 | 13.0 | 10.00 | 10.0 | 16.0 |
| gem-flash + gem-flash | 8 | 11.00 [11.00, 11.00] | 11.0 | 11.0 | 11.00 | 11.0 | 11.0 |
| gem-flash + gpt-4.1-mini | 8 | 10.00 [10.00, 10.00] | 10.0 | 10.5 | 10.00 | 10.0 | 11.0 |
| gem-flash + gpt-4.1 | 8 | 9.34 [8.94, 9.72] | 11.0 | 15.5 | 9.53 | 11.0 | 20.0 |
| gem-flash + haiku-5.5 | 8 | 11.00 [11.00, 11.00] | 11.0 | 15.5 | 11.00 | 11.0 | 20.0 |
| gem-flash + haiku-4.5 | 8 | 2.00 [2.00, 2.00] | 2.0 | 6.5 | 3.12 | 11.0 | 11.0 |
| gem-flash + sonnet-4.6 | 8 | 8.62 [7.81, 9.66] | 11.0 | 13.5 | 9.09 | 11.0 | 16.0 |
| gpt-4.1-mini + gpt-4.1-mini | 8 | 10.00 [10.00, 10.00] | 10.0 | 10.0 | 10.00 | 10.0 | 10.0 |
| gpt-4.1-mini + gpt-4.1 | 8 | 8.47 [8.12, 8.78] | 10.0 | 15.0 | 8.47 | 10.0 | 20.0 |
| gpt-4.1-mini + haiku-5.5 | 8 | 10.00 [10.00, 10.00] | 10.0 | 15.0 | 10.00 | 10.0 | 20.0 |
| gpt-4.1-mini + haiku-4.5 | 8 | 2.00 [2.00, 2.00] | 2.0 | 6.0 | 3.03 | 10.0 | 10.0 |
| gpt-4.1-mini + sonnet-4.6 | 8 | 10.00 [10.00, 10.00] | 10.0 | 13.0 | 10.00 | 10.0 | 16.0 |
| gpt-4.1 + gpt-4.1 | 8 | 17.88 [16.94, 19.12] | 20.0 | 20.0 | 18.06 | 20.0 | 20.0 |
| gpt-4.1 + haiku-5.5 | 8 | 20.00 [20.00, 20.00] | 20.0 | 20.0 | 20.00 | 20.0 | 20.0 |
| gpt-4.1 + haiku-4.5 | 8 | 2.00 [2.00, 2.00] | 2.0 | 11.0 | 2.50 | 20.0 | 20.0 |
| gpt-4.1 + sonnet-4.6 | 8 | 13.38 [11.81, 14.75] | 16.0 | 18.0 | 13.75 | 16.0 | 20.0 |
| haiku-5.5 + haiku-5.5 | 8 | 20.00 [20.00, 20.00] | 20.0 | 20.0 | 20.00 | 20.0 | 20.0 |
| haiku-5.5 + haiku-4.5 | 8 | 2.00 [2.00, 2.00] | 2.0 | 11.0 | 6.50 | 20.0 | 20.0 |
| haiku-5.5 + sonnet-4.6 | 8 | 13.84 [12.12, 15.34] | 16.0 | 18.0 | 13.94 | 16.0 | 20.0 |
| haiku-4.5 + haiku-4.5 | 8 | 2.00 [2.00, 2.00] | 2.0 | 2.0 | 2.12 | 2.0 | 2.0 |
| haiku-4.5 + sonnet-4.6 | 8 | 2.00 [2.00, 2.00] | 2.0 | 9.0 | 3.69 | 16.0 | 16.0 |
| sonnet-4.6 + sonnet-4.6 | 8 | 14.50 [13.00, 16.00] | 16.0 | 16.0 | 14.50 | 16.0 | 16.0 |

Cells analysed: 28. Mean absolute error of the market price: law 0.57, mean-anchor 3.43, higher-anchor 6.28.
Higher-anchor seller (mixed pairs, 21 cells): mean absolute error match-down 3.54, stay-put 7.59.
