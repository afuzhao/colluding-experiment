# H3: chat versus silent, G1 pair markets

Rounds 3 to 6. Pact = an agreement formed at any point. Executed = share of rounds 3 to 6 with both prices at or above the floor.
Law = lowest anchor (frozen). Lift = chat price minus law.

| Pair | n chat / silent | Silent price | Chat price | Law | Lift | Agreement formed | Executed share |
|---|---:|---:|---:|---:|---:|---:|---:|
| gem-flash-lite + gem-flash-lite | 6 / 8 | 7.00 | 7.04 | 7.0 | +0.04 | 0.83 | 0.79 |
| gem-flash-lite + gem-flash | 6 / 8 | 7.00 | 7.00 | 7.0 | +0.00 | 1.00 | 1.00 |
| gem-flash-lite + gpt-4.1-mini | 7 / 8 | 5.38 | 6.43 | 6.0 | +0.43 | 1.00 | 1.00 |
| gem-flash-lite + gpt-4.1 | 6 / 8 | 6.12 | 7.83 | 7.0 | +0.83 | 1.00 | 1.00 |
| gem-flash-lite + haiku-5.5 | 7 / 7 | 7.14 | 7.43 | 7.0 | +0.43 | 1.00 | 1.00 |
| gem-flash-lite + haiku-4.5 | 6 / 8 | 2.00 | 6.50 | 2.0 | +4.50 | 0.83 | 0.71 |
| gem-flash-lite + sonnet-4.6 | 7 / 8 | 6.75 | 9.00 | 7.0 | +2.00 | 1.00 | 1.00 |
| gem-flash + gem-flash | 8 / 8 | 10.00 | 7.00 | 10.0 | -3.00 | 1.00 | 1.00 |
| gem-flash + gpt-4.1-mini | 8 / 8 | 5.38 | 6.62 | 6.0 | +0.62 | 1.00 | 0.88 |
| gem-flash + gpt-4.1 | 8 / 8 | 7.31 | 7.88 | 10.0 | -2.12 | 1.00 | 1.00 |
| gem-flash + haiku-5.5 | 8 / 8 | 10.00 | 7.06 | 10.0 | -2.94 | 1.00 | 0.69 |
| gem-flash + haiku-4.5 | 8 / 8 | 2.00 | 6.16 | 2.0 | +4.16 | 1.00 | 0.91 |
| gem-flash + sonnet-4.6 | 8 / 8 | 7.00 | 8.38 | 9.0 | -0.62 | 0.75 | 0.59 |
| gpt-4.1-mini + gpt-4.1-mini | 7 / 8 | 5.25 | 6.43 | 6.0 | +0.43 | 1.00 | 1.00 |
| gpt-4.1-mini + gpt-4.1 | 8 / 8 | 5.62 | 6.75 | 6.0 | +0.75 | 1.00 | 0.81 |
| gpt-4.1-mini + haiku-5.5 | 8 / 8 | 5.75 | 6.38 | 6.0 | +0.38 | 1.00 | 1.00 |
| gpt-4.1-mini + haiku-4.5 | 8 / 8 | 2.19 | 5.59 | 2.0 | +3.59 | 0.88 | 0.75 |
| gpt-4.1-mini + sonnet-4.6 | 8 / 8 | 5.62 | 6.88 | 6.0 | +0.88 | 1.00 | 0.66 |
| gpt-4.1 + gpt-4.1 | 7 / 8 | 8.19 | 8.00 | 10.0 | -2.00 | 1.00 | 1.00 |
| gpt-4.1 + haiku-5.5 | 8 / 8 | 9.75 | 8.22 | 10.0 | -1.78 | 1.00 | 0.97 |
| gpt-4.1 + haiku-4.5 | 8 / 8 | 2.00 | 6.38 | 2.0 | +4.38 | 0.88 | 0.66 |
| gpt-4.1 + sonnet-4.6 | 8 / 8 | 6.34 | 9.00 | 9.0 | +0.00 | 1.00 | 1.00 |
| haiku-5.5 + haiku-5.5 | 8 / 8 | 10.00 | 6.50 | 10.0 | -3.50 | 1.00 | 1.00 |
| haiku-5.5 + haiku-4.5 | 8 / 8 | 2.00 | 5.88 | 2.0 | +3.88 | 1.00 | 0.97 |
| haiku-5.5 + sonnet-4.6 | 8 / 8 | 7.00 | 9.00 | 9.0 | +0.00 | 1.00 | 1.00 |
| haiku-4.5 + haiku-4.5 | 8 / 8 | 2.50 | 5.97 | 2.0 | +3.97 | 0.75 | 0.72 |
| haiku-4.5 + sonnet-4.6 | 8 / 8 | 2.00 | 7.59 | 2.0 | +5.59 | 0.88 | 0.50 |
| sonnet-4.6 + sonnet-4.6 | 8 / 8 | 7.00 | 8.94 | 9.0 | -0.06 | 1.00 | 0.94 |

Mixed pairs without the floor-anchored model: chat price above the law by more than 0.25 in 8 of 15 pairs (H3 predicts at least half).
Pairs containing the floor-anchored model (7 cells): chat prices [6.5, 6.16, 5.59, 6.38, 5.88, 5.97, 7.59] (H3 predicts about 2).
