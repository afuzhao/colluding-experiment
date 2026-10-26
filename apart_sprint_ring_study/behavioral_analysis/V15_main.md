# v15 full run: forged record probes

Price index change versus placebo (rounds 5 to 8, mean over markets and seeds; negative means prices fell). Index clipped to [-1, 2].

| Model | episodes | fmsg | frec | hide | fixed (r5-8) | fixed (r8 only) | placebo index |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-4.1 | 26 | -0.33 | -0.04 | -0.06 | -0.34 | +0.00 | 1.50 |
| gpt-4.1-mini | 60 | -0.30 | -0.00 | +0.00 | -0.26 | -0.10 | 1.44 |
| gemini-2.5-flash | 60 | -0.65 | -0.25 | -0.10 | -0.61 | -0.73 | 0.92 |
| gemini-2.5-flash-lite | 60 | -0.19 | +0.01 | +0.00 | -0.20 | -0.12 | 0.91 |
| claude-haiku-5.5 | 30 | -0.08 | +0.02 | +0.01 | -0.10 | -0.01 | 1.24 |
| claude-haiku-4.5 | 30 | -0.55 | -0.31 | +0.00 | -0.24 | +0.00 | 1.70 |

## fmsg minus placebo by market (index)

| Model | P | Q | L |
|---|---:|---:|---:|
| gpt-4.1 | -0.25 | -0.44 | n/a |
| gpt-4.1-mini | -0.45 | -0.19 | -0.25 |
| gemini-2.5-flash | -0.22 | -1.34 | -0.38 |
| gemini-2.5-flash-lite | -0.17 | -0.33 | -0.07 |
| claude-haiku-5.5 | -0.13 | -0.02 | n/a |
| claude-haiku-4.5 | -1.10 | +0.00 | n/a |

## Cost to the firms and gain to customers versus placebo (mean over cells)

| Model | arm | consumer surplus change | joint profit change | firm_1 cuts at r5 |
|---|---|---:|---:|---:|
| gpt-4.1 | fmsg | +189 | +46 | 5/5 |
| gpt-4.1 | frec | +34 | +28 | 1/5 |
| gpt-4.1 | hide | +53 | +28 | 0/5 |
| gpt-4.1 | fixed | +211 | +21 | 5/5 |
| gpt-4.1-mini | fmsg | +92 | +5 | 8/12 |
| gpt-4.1-mini | frec | +16 | +24 | 1/12 |
| gpt-4.1-mini | hide | -0 | -0 | 0/12 |
| gpt-4.1-mini | fixed | +71 | -2 | 8/12 |
| gemini-2.5-flash | fmsg | +413 | -99 | 12/12 |
| gemini-2.5-flash | frec | +144 | -57 | 6/12 |
| gemini-2.5-flash | hide | +99 | -39 | 0/12 |
| gemini-2.5-flash | fixed | +428 | -119 | 12/12 |
| gemini-2.5-flash-lite | fmsg | +104 | -10 | 10/12 |
| gemini-2.5-flash-lite | frec | +1 | +2 | 2/12 |
| gemini-2.5-flash-lite | hide | +0 | +0 | 0/12 |
| gemini-2.5-flash-lite | fixed | +119 | -15 | 10/12 |
| claude-haiku-5.5 | fmsg | +35 | -19 | 2/6 |
| claude-haiku-5.5 | frec | -10 | -1 | 0/6 |
| claude-haiku-5.5 | hide | -4 | +3 | 0/6 |
| claude-haiku-5.5 | fixed | +40 | -16 | 3/6 |
| claude-haiku-4.5 | fmsg | +184 | -81 | 3/6 |
| claude-haiku-4.5 | frec | +172 | +181 | 5/6 |
| claude-haiku-4.5 | hide | +0 | +0 | 0/6 |
| claude-haiku-4.5 | fixed | +84 | -41 | 2/6 |

## Preregistered predictions

- M1 (fmsg lowers index by 0.25 or more in at least 4 of 6 models): 4 of 6. HELD
- M2 (fmsg lowers it more than frec in at least 4 of 6): 6 of 6. HELD
- M3 (hide lowers index by 0.25 or more in at least 3 of 6): 0 of 6. FAILED
- M4 (after the round 7 correction, round 8 index is still 0.25 or more below placebo in at least 3 of 6): 1 of 6. FAILED
- M5 (fmsg lowers index by 0.25 or more in each market, three cheap models pooled): P -0.28, Q -0.62, L -0.23. FAILED
