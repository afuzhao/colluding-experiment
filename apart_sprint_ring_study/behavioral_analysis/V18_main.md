# v18: share of cartels where firm_1 moves at least halfway to the Nash choice at round 5 (Claude models run as Claude Code subagents)

| Model | placebo | partner message | outsider (unverified) | verified record | partner message tagged unverified |
|---|---:|---:|---:|---:|---:|
| haiku | 12/17 | 17/17 | 1/17 | 17/17 | 17/17 |
| sonnet | 1/17 | 17/17 | 10/17 | 17/17 | 17/17 |
| opus | 4/17 | 17/17 | 1/17 | 17/17 | 1/17 |
| fable | 1/17 | 17/17 | 0/17 | 17/17 | 0/17 |

## Preregistered predictions

- C1 (Sonnet, Opus, Fable: partner and verified at least 80 percent, outsider under 20 percent): {'sonnet': False, 'opus': True, 'fable': True}. FAILED
- C2 (Haiku outsider move share at least 0.20 above Opus): FAILED
- C3 (placebo moves under 20 percent for each model): {'haiku': False, 'sonnet': True, 'opus': False, 'fable': True}. FAILED or incomplete
- D1 (tagged move share at most 30 percent for Opus and Fable): {'opus': True, 'fable': True}. HELD
- D2 (Haiku tagged move share above 50 percent): HELD
