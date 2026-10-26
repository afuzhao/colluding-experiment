# Offer acceptance and relay across four models

Matched differences within seed: (offer − ordinary observation, neutral markets) and (shared − private relay,
and restricted − private). Positive surplus-loss change means more consumer harm. Intervals resample seeds
(descriptive). Sustained-pact rate is shown as first arm vs second arm.

| Model | Contrast | Seeds | Surplus-loss change | 95% interval | Pact rate | Detail |
|---|---|---:|---:|---|---|---|
| gemini-2.5-flash-lite (main 8) | offer | 8 | 46.0 | [22.5, 78.0] | 0.62 vs 0.25 | first-round accepts 13/16 vs 0/16 |
| gemini-2.5-flash-lite (main 8) | relay | 6 | 60.2 | [18.9, 101.6] | 0.67 vs 0.00 | invented offers 10 vs 40 |
| gemini-2.5-flash-lite (main 8) | relay_restricted | 6 | 38.6 | [9.4, 74.1] | 0.00 vs 0.00 | invented offers 0 vs 40 |
| gemini-2.5-flash-lite (ext 8) | offer | 8 | 35.6 | [15.0, 52.5] | 0.50 vs 0.50 | first-round accepts 12/16 vs 1/16 |
| gemini-2.5-flash (main 8) | offer | 8 | 87.9 | [68.5, 115.8] | 1.00 vs 0.75 | first-round accepts 16/16 vs 0/16 |
| gemini-2.5-flash (main 8) | relay | 8 | 0.0 | [0.0, 0.0] | 1.00 vs 0.00 | invented offers 45 vs 0 |
| gemini-2.5-flash (main 8) | relay_restricted | 8 | 0.0 | [0.0, 0.0] | 0.00 vs 0.00 | invented offers 0 vs 0 |
| gpt-4.1-mini (main 8) | offer | 8 | 56.4 | [11.5, 101.6] | 0.75 vs 0.75 | first-round accepts 8/16 vs 4/16 |
| gpt-4.1-mini (main 8) | relay | 8 | 34.8 | [4.8, 64.9] | 1.00 vs 0.00 | invented offers 63 vs 54 |
| gpt-4.1-mini (main 8) | relay_restricted | 8 | 10.6 | [-30.0, 45.9] | 0.88 vs 0.00 | invented offers 16 vs 54 |
| gpt-4.1 (main 8) | offer | 8 | 33.5 | [15.0, 52.5] | 0.75 vs 1.00 | first-round accepts 11/16 vs 0/16 |
| gpt-4.1 (main 8) | relay | 8 | 0.0 | [0.0, 0.0] | 1.00 vs 0.00 | invented offers 32 vs 23 |
| gpt-4.1 (main 8) | relay_restricted | 8 | 0.0 | [0.0, 0.0] | 0.88 vs 0.00 | invented offers 6 vs 23 |
