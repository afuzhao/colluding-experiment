# Environment 2 colluding-agent reactions

E2-R ports the completed environment-1 reaction design to differentiated-product price competition. Eight approach families are crossed with general notice absent/present, for 16 conditions with 15 rounds each. This is reaction elicitation, not a disruption study.

**Status: execution and assistant review complete.** The original cohort completed 14/16 markets and 42 eligible private calls; both reciprocal offers failed delivery. Two separately versioned reciprocal repairs completed all 15 rounds and six private calls. The selected 16-slot presentation combines 14 original and two revised-prompt conditions, with original failures preserved. One fresh formation is shared throughout; these are not independent replications.

[Selected results](artifacts/combined_16/RESULTS_TABLE.md) · [Detailed report](reports/FINAL_RESULTS.md) · [Word report](reports/env2_reactions_report.docx) · [Original evidence](artifacts/final_16) · [Reciprocal repairs](artifacts/reciprocal_repairs_v1) · [Development review](reports/PREFLIGHT_REVIEW.md)

Across 32 resident responses to C: public speech has 15 acceptances including 12 conditional, 4 rejections and 13 unclear replies, with no expressed suspicion. Private reports have 24 raw acceptances including 22 conditional, 4 rejections and 4 nonproposals; 6 suspicion flags overlap 3 acceptances and 3 rejections. With suspicion displayed first, the private headline is 21 accept, 1 reject, 6 suspicious and 4 N/A. Public and private are separate tasks, not validated measures of internal state.

The ordinary-C supplement for both environments has completed execution and assistant review, with two full 15-round conditions per environment. See [control protocol](../exp%204%20%28ordinary_peer_controls%29/README.md).

See [methods](REPORT_METHODS.md), [environment 2](../../environments/env%202%20%28differentiated_prices%29/README.md), [repository guide](../../repo_guide/README.md), and [completed E1-R evidence](../exp%202%20%28insider_reactions_v3%29/README.md).

## Important translations

Equal offers request prices A=64 B=64 C=64 for rounds 9–13. Unequal requests A=76 B=76 C=52. Under the unequal offer A/B earn 576 each and C 1920, versus equal-cartel profits of 1200 each. This reduces joint profit and is not the old quantity allocation's pure redistribution. The vague feeler specifies no exact price/window. C prices remain model selected, with misses logged rather than overwritten.

## Local files

| Location | Contents |
|---|---|
| `configs/study.json` | Frozen versions, model settings, seed and 16-condition matrix |
| `prompts/` | Price-specific residents, C role, notice and eight approaches |
| `price_study/` | Local model client, protocol, exact history, branches, diagnostics and reports |
| `tools/pilot.py` | Separate development formation, preflight and short live integration test |
| `tools/run.py` | Final formation and 16-condition worker; refuses duplicate worker/source drift |
| `tests/` | Synthetic controller checks; not real-model findings |
| `results/` | Ignored local runtime outputs; never committed directly |
| `artifacts/` | Original, repair, combined and development evidence after review |
| `reports/` | Methods, development checks and reviewed Markdown and Word reports |

Environment-2 economics are imported from `environments/env 2 (differentiated_prices)/market_env/`; their source is included in the frozen manifest. The study uses its own reaction orchestration, with simultaneous-message/price behaviour checked against the environment interface. Do not change shared environment source during a running cohort.

## Commands

From this study directory:

```sh
python3 -m unittest discover -s tests -v
python3 tools/pilot.py --stage formation --output results/development_8101
# Review the actual development checkpoint before the next command.
python3 tools/pilot.py --stage checks --output results/development_8101
python3 tools/run.py --formation-only --output results/final_16
# Review the actual fresh final formation before continuations.
python3 tools/run.py --output results/final_16
```

Live commands contact the existing local Qwen service. Do not duplicate workers, silently reroll failed formation, or rerun a resident response because its result is uninteresting. The final dataset and publication must keep preflight and final histories separate. Model-based public/private results require actual calls and transcript review, not simulated fixtures.

## Completed ordinary peer control supplement

The two full15 ordinary-C continuations for this environment are separately reviewed and reported in the [control supplement](../exp%204%20%28ordinary_peer_controls%29/reports/E2_CONTROL_RESULTS.md), with [exact evidence](../exp%204%20%28ordinary_peer_controls%29/artifacts/E2). See the [two-environment comparison](../exp%204%20%28ordinary_peer_controls%29/reports/CONTROL_COMPARISON.md) for explicit versus neutral frozen8 accounts. These reuse the original formation and do not enter the original16condition headline table. Ordinary-C suspicion, scope objections and proposal ambiguity remain separate, with actual denominators and all failures.
