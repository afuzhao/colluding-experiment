# v18 part 3 (post hoc, not preregistered): share of 17 cartels where the firm changes its own choice at all

The earlier "moves at least halfway to the Nash choice" count understates firms that best-respond to the announced move (for example choosing 20 against an announced 32). This table counts any change from the firm's round 4 choice.

| Run | placebo | partner message | partner message tagged unverified |
|---|---:|---:|---:|
| claude-haiku-5.5, API, answer only | 2/17 | 14/17 | 10/17 |
| claude-haiku-5.5, API, reason first | 3/17 | 14/17 | 9/17 |
| claude-haiku-4.5, API, answer only | 1/17 | 11/17 | 12/17 |
| claude-haiku-4.5, API, reason first | 1/17 | 17/17 | 17/17 |
| haiku, Claude Code subagent | 17/17 | 17/17 | 17/17 |
| sonnet, Claude Code subagent | 2/17 | 17/17 | 17/17 |
| opus, Claude Code subagent | 4/17 | 17/17 | 2/17 |
| fable, Claude Code subagent | 2/17 | 17/17 | 1/17 |
