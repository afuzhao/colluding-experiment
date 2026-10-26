# Deep analysis across all studies

## 1. What do firms do with a claim? Choice classified by what would be right if the claim were true

Best reply = the choice that maximizes the firm's own profit if the partner really plays the claimed value. Stay = repeats its round 4 choice. Pooled over cartels and runs of each group.

### api runs (6 models x 17 cartels per row)

| Claim shown | stay | best reply to the claim | best reply to no change | copy the claim | other |
|---|---:|---:|---:|---:|---:|
| fmsg | 19% | 51% | 3% | 0% | 24% | n=102
| outsider | 47% | 44% | 0% | 0% | 7% | n=101
| verified | 14% | 61% | 3% | 0% | 19% | n=102
| tagged | 29% | 45% | 2% | 0% | 21% | n=101
| leak | 29% | 50% | 0% | 0% | 19% | n=102
| trojan | 47% | 0% | 12% | 39% | 0% | n=102
| raise | 50% | 1% | 0% | 40% | 5% | n=102
| hold | 95% | 0% | 0% | 4% | 0% | n=101

Placebo choices classified as if the partner message had been shown (the baseline rate of that behavior without any claim): stay 95%, other 3%, best reply to no change 0%

### subagent runs (3 models x 17 cartels per row)

| Claim shown | stay | best reply to the claim | best reply to no change | copy the claim | other |
|---|---:|---:|---:|---:|---:|
| fmsg | 0% | 100% | 0% | 0% | 0% | n=51
| outsider | 62% | 0% | 19% | 0% | 17% | n=51
| verified | 0% | 100% | 0% | 0% | 0% | n=51
| tagged | 60% | 23% | 3% | 0% | 11% | n=51
| leak | 0% | 100% | 0% | 0% | 0% | n=51
| trojan | 0% | 45% | 5% | 25% | 23% | n=51
| raise | 90% | 5% | 1% | 0% | 1% | n=51
| hold | 86% | 3% | 0% | 3% | 5% | n=51

Placebo choices classified as if the partner message had been shown (the baseline rate of that behavior without any claim): stay 84%, best reply to no change 3%, other 11%


## 2. Cut rates with the cartel as the unit (bootstrap over 17 cartels, difference from placebo)

| Claim | API models (6): mean cut rate above placebo [95% CI] | Claude subagents (3) |
|---|---|---|
| fmsg | +0.73 [+0.62, +0.82] | +0.84 [+0.67, +0.98] |
| outsider | +0.47 [+0.36, +0.59] | +0.22 [+0.08, +0.31] |
| verified | +0.75 [+0.65, +0.86] | +0.84 [+0.67, +0.98] |
| tagged | +0.64 [+0.55, +0.74] | +0.24 [+0.14, +0.31] |
| leak | +0.61 [+0.47, +0.74] | +0.84 [+0.67, +0.98] |
| trojan | +0.48 [+0.38, +0.58] | +0.84 [+0.67, +0.98] |
| raise | +0.04 [-0.05, +0.11] | -0.06 [-0.16, +0.02] |
| hold | +0.00 [-0.03, +0.03] | -0.02 [-0.06, +0.00] |

## 3. What makes a cartel fragile? Cut rate on the partner message (API models), by market and by source of the cartel

By market:
{'L': '90% (n=30)', 'P': '89% (n=36)', 'Q': '56% (n=36)'}

By source model of the cartel:
{'claude-haiku-4.5': '75% (n=12)', 'claude-haiku-5.5': '78% (n=18)', 'gemini-2.5-flash': '72% (n=18)', 'gemini-2.5-flash-lite': '78% (n=18)', 'gpt-4.1': '83% (n=18)', 'gpt-4.1-mini': '78% (n=18)'}

Correlation of cartel strength (round 4 price index) with how often the firm cuts: Spearman -0.64 (p=0.01, 17 cartels)


## 4. Mechanism in the full 8-round episodes: what happens after a firm cuts on a forged message?

Among cells where firm_1 cut at round 5 after a forged claim (partner message, outsider, verified record, two paraphrases):

| Model | cells | firm_2 held at round 5 | firm_1 profit up at round 5 | firm_2 profit down at round 5 | firm_1 back within 1 step at round 6 | firm_2 cuts at round 6 |
|---|---:|---:|---:|---:|---:|---:|
| gpt-4.1 | 9 | 9 | 5 | 9 | 9 | 2 |
| gpt-4.1-mini | 39 | 39 | 19 | 39 | 29 | 8 |
| gemini-2.5-flash | 55 | 55 | 36 | 55 | 25 | 36 |
| gemini-2.5-flash-lite | 47 | 47 | 31 | 47 | 42 | 1 |
| claude-haiku-5.5 | 4 | 4 | 2 | 4 | 4 | 0 |
| claude-haiku-4.5 | 6 | 6 | 0 | 6 | 2 | 6 |
| all | 160 | 160 | 93 | 160 | 111 | 53 |

### Does a real cut persist more than a forged claim? Share of episodes where the price index is back at 0.4 or above at round 8 (cheap models only)

| Arm | episodes | back to cartel level at round 8 | mean index round 8 |
|---|---:|---:|---:|
| placebo | 36 | 94% | +1.08 |
| fmsg | 36 | 78% | +0.74 |
| outsider | 36 | 72% | +0.86 |
| verified | 33 | 70% | +0.77 |
| act | 36 | 75% | +0.62 |
| act3 | 33 | 45% | +0.34 |

## 5. Is credulity one trait of a model across studies? (6 API models; rank correlations are descriptive only)

| Model | ring: joins with no words (%) | single decision: cuts on partner message | cuts on outsider | follows cooperative proposal |
|---|---:|---:|---:|---:|
| gpt-4.1 | 100 | 1.00 | 0.41 | 0.35 |
| gpt-4.1-mini | 16 | 0.53 | 0.35 | 0.94 |
| gemini-2.5-flash | 94 | 0.94 | 0.88 | 0.88 |
| gemini-2.5-flash-lite | 0 | 0.82 | 1.00 | 0.76 |
| claude-haiku-5.5 | 89 | 0.71 | 0.24 | 0.18 |
| claude-haiku-4.5 | 0 | 0.65 | 0.29 | 0.06 |

Spearman, ring tacit joining vs partner message: +0.67 (n=6 models, p=0.15)

Spearman, ring tacit joining vs outsider: +0.03 (n=6 models, p=0.96)

Spearman, ring tacit joining vs proposal: +0.17 (n=6 models, p=0.74)
Spearman, partner message vs proposal: -0.03 (p=0.96)
Spearman, partner message vs outsider: +0.54 (p=0.27)

## 6. Extra checks

Cartel strength vs cut rate within market L: n=5, mean strength 0.87, mean cut rate 0.90, Spearman +0.46
Cartel strength vs cut rate within market P: n=6, mean strength 1.00, mean cut rate 0.89, Spearman -0.23
Cartel strength vs cut rate within market Q: n=6, mean strength 2.08, mean cut rate 0.56, Spearman +0.23

Firm_1 after cutting on a forged claim (all full-episode cells pooled): partner really cut at round 6 and firm_1 back to the cartel level 14, partner cut and firm_1 stays low 39, partner held and firm_1 back 97, partner held and firm_1 stays low 10. Fisher exact p=2e-16
Round 8 back at cartel level, fmsg 28/36 vs placebo 34/36: Fisher p=0.085
Round 8 back at cartel level, act 27/36 vs placebo 34/36: Fisher p=0.046
Round 8 back at cartel level, act3 15/33 vs placebo 34/36: Fisher p=0.000
Round 8 back at cartel level, act3 15/33 vs fmsg 28/36: Fisher p=0.007

Share of cartels where the firm copies the claimed value exactly (API): raise: gpt-4.1 0.65, gpt-4.1-mini 0.65, gemini-2.5-flash 0.53, gemini-2.5-flash-lite 0.76, claude-haiku-5.5 0.29, claude-haiku-4.5 0.18; trojan: gpt-4.1 0.35, gpt-4.1-mini 0.94, gemini-2.5-flash 0.88, gemini-2.5-flash-lite 0.76, claude-haiku-5.5 0.12, claude-haiku-4.5 0.06

Within each model: after firm_1 cut on a forged claim, firm_1 back at the cartel level at round 6 when the partner held vs when the partner really cut at round 6
- gemini-2.5-flash-lite: partner held 42/46 back; partner cut 0/1 back
- claude-haiku-5.5: partner held 4/4 back; partner cut 0/0 back
- gemini-2.5-flash: partner held 16/19 back; partner cut 9/36 back
- gpt-4.1-mini: partner held 28/31 back; partner cut 1/8 back
- gpt-4.1: partner held 7/7 back; partner cut 2/2 back
- claude-haiku-4.5: partner held 0/0 back; partner cut 2/6 back
