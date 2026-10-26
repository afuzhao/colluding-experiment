# Do single-agent response curves predict two-agent markets?

Private-relay markets (two copies of one model, prices visible, no messages between them). The response curve
f(L) is the model's mean price against a fixed rival at L (v5). Prediction iterates f from the observed round-1
prices. "Stay" keeps round-1 prices. Error is mean absolute difference in the final-round market price.

| Model | Seeds | Observed final | Response-curve prediction | Stay-put | Constant 8 | Err curve | Err stay | Err const 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gemini-2.5-flash-lite | 6 | 6.33 | 6.17 | 6.17 | 8.00 | 0.17 | 0.17 | 1.67 |
| gemini-2.5-flash | 8 | 7.00 | 6.00 | 7.00 | 8.00 | 1.00 | 0.00 | 1.00 |
| gpt-4.1-mini | 8 | 5.38 | 5.38 | 5.38 | 8.00 | 0.00 | 0.00 | 2.62 |
| gpt-4.1 | 8 | 8.00 | 8.00 | 8.00 | 8.00 | 0.00 | 0.00 | 0.00 |

## Pact vs no pact: price held after an agreement at 8 exists (v4 base) against the no-communication response f(8)

| Model | f(8), no communication | Observed with pact and chat (rounds 5 to 8 mean) | Difference |
|---|---:|---:|---:|
| gemini-2.5-flash-lite | 7.00 | 8.00 | +1.00 |
| gemini-2.5-flash | 8.00 | 8.00 | +0.00 |
| gpt-4.1-mini | 5.75 | 8.00 | +2.25 |
