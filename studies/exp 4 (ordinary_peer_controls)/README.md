# Ordinary peer controls for both reaction environments

Status: authorized and queued after the running environment-2 reaction cohort. No control inference has started. The runner is implemented and offline-tested; actual control results are not yet available.

The user requested adding ordinary-C controls to both environment 1 and environment 2. The controls supplement the two reaction studies and do not replace either frozen cohort or constitute a disruption experiment.

| Environment | Original reaction source | Ordinary C offer | Notice conditions |
|---|---|---|---|
| E1 quantity competition | `studies/exp 2 (insider_reactions_v3)/artifacts/final_16` | A/B/C each 16 for rounds 9–13 | Absent and present |
| E2 differentiated pricing | `studies/exp 3 (env2_reactions)/artifacts/final_16` after completion | A/B/C each 64 for rounds 9–13 | Absent and present |

These are four ordinary-control branches, with four resident-to-C reply pairs per environment. Optional neutral diagnostics are included in the authorized queue. Each environment reuses its own original formation, so this does not add independent formation histories or reliable population false-positive estimates.

See [execution queue](EXECUTION_QUEUE.md), [machine-readable specification](protocol.json), [the detailed E1 control design](../exp%202%20%28insider_reactions_v3%29/supplements/design_review_2026_10_25/CONTROL_PLAN.md), and [runtime findings](RUNTIME_NOTES.md).

## Current horizon amendment

Protocol `ordinary-peer-controls-2-full15` supersedes the earlier8round/9reply-probe specification before any control inference. Each of the four ordinary-C notice branches runs all15rounds. Formation1–5is reused from the corresponding actual reviewed history; fresh ordinary preparation6–7 is shared within each environment; offer8; model-selected actions and speech9–15. First public replies come from actual9, price/quantity adherence and economics from9–13, and post-window follow-up14–15. Symmetric explicit/neutral diagnostics still use isolated frozen8snapshots, so no future information is introduced. Nominal240request positions across both environments, before corrections/replays/failures.

Tests: `python3 -m unittest discover -s tests -v`. Run E1thenE2after main/repair review and publication, using `python3 tools/run_controls.py --environment E1` and then `--environment E2`. These are separately documented post-hoc controls, not independent-history replications or completed disruption experiments.
