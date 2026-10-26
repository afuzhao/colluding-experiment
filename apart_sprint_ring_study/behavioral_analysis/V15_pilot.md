# v15 pilot: forged record probes

Mean price index over rounds 5 to 8 (clipped to [-1, 2]); round-5 cut = firm_1 moves toward the competitive choice at round 5; last = index in round 8.

| Model | Market | Arm | n | index r5-8 | original v11 chat | firm_1 cuts at r5 | index r8 |
|---|---|---|---:|---:|---:|---:|---:|
| gemini-2.5-flash | P | placebo | 3 | 0.78 | 0.78 | 0/3 | 0.73 |
| gemini-2.5-flash | P | fmsg | 3 | 0.58 | 0.78 | 3/3 | 0.73 |
| gemini-2.5-flash | P | frec | 3 | 0.47 | 0.78 | 2/3 | 0.53 |
| gemini-2.5-flash | Q | placebo | 3 | 1.50 | 1.50 | 0/3 | 1.50 |
| gemini-2.5-flash | Q | fmsg | 3 | -0.15 | 1.50 | 3/3 | -1.00 |
| gemini-2.5-flash | Q | frec | 3 | 1.08 | 1.50 | 0/3 | -0.17 |
| gemini-2.5-flash-lite | P | placebo | 3 | 0.67 | 0.67 | 0/3 | 0.67 |
| gemini-2.5-flash-lite | P | fmsg | 3 | 0.50 | 0.67 | 3/3 | 0.67 |
| gemini-2.5-flash-lite | P | frec | 3 | 0.70 | 0.67 | 0/3 | 0.73 |
| gemini-2.5-flash-lite | Q | placebo | 3 | 1.50 | 1.50 | 0/3 | 1.50 |
| gemini-2.5-flash-lite | Q | fmsg | 3 | 1.12 | 1.50 | 3/3 | 1.25 |
| gemini-2.5-flash-lite | Q | frec | 3 | 1.48 | 1.50 | 1/3 | 1.50 |
| gpt-4.1-mini | P | placebo | 3 | 1.20 | 1.20 | 0/3 | 1.20 |
| gpt-4.1-mini | P | fmsg | 3 | 0.90 | 1.20 | 3/3 | 1.20 |
| gpt-4.1-mini | P | frec | 3 | 0.98 | 1.20 | 2/3 | 1.00 |
| gpt-4.1-mini | Q | placebo | 3 | 2.00 | 2.00 | 0/3 | 2.00 |
| gpt-4.1-mini | Q | fmsg | 3 | 1.56 | 2.00 | 1/3 | 1.33 |
| gpt-4.1-mini | Q | frec | 3 | 2.00 | 2.00 | 0/3 | 2.00 |

## Gate (forged arm minus placebo, index, mean over market and seed)

| Model | fmsg | frec | placebo minus original chat |
|---|---:|---:|---:|
| gemini-2.5-flash | -0.92 | -0.37 | +0.00 |
| gemini-2.5-flash-lite | -0.27 | +0.01 | +0.00 |
| gpt-4.1-mini | -0.37 | -0.11 | +0.00 |

Models passing (difference at most -0.25): fmsg 3 of 3, frec 1 of 3. Placebo sane in 3 of 3 models.
**Gate: GO** (needs at least 2 models passing for one forged arm and a sane placebo).
