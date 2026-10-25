# Data map — what is present and what it means

## Authoritative completed data: E1-R

All links in this section point to the completed 16-condition quantity-market reaction cohort under `studies/exp 2 (insider_reactions_v3)/artifacts/final_16/`.

| File or folder | Format and contents | Intended use |
|---|---|---|
| [RESULTS_TABLE.md](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/RESULTS_TABLE.md) | 16-row table: public replies, private headline replies, suspicion counts and A/B quota adherence | Fast overview, not a replacement for evidence |
| [public_annotations.csv](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/public_annotations.csv) | 96 candidate-message/recipient pairs with exact offer/reply text, proposal/addressing judgments, raw response, suspicion, quote and assistant-review provenance | Audit speech labels and investigate ambiguity |
| [private_assessments.csv](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/private_assessments.csv) | 96 peer-message assessments from 48 calls; each of three firms assessed both peers in all 16 conditions | Separate elicited private reports from public speech |
| [branches/](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/branches) | 16 JSON trajectories, each with 15 rounds, exact public messages, quantities, prices and profits | Full behavioural/economic record |
| [results.json](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/results.json) | Combined condition summaries, public evidence and private assessments | Programmatic comparison |
| [FINAL_METRICS.json](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/FINAL_METRICS.json) | Totals, overlap-related counts, conditionality, runtime, calls and fidelity checks | Verify reported denominators |
| [suspicion_overlaps.json](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/suspicion_overlaps.json) | Suspicious private responses with underlying agreement and explanation | Preserve rejection/acceptance separately from suspicion |
| [c_semantic_review.json](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/c_semantic_review.json) | Assistant review of delivered C offers and follow-ups, including prompt leakage/timing errors | Identify imperfectly delivered interventions |
| [c_fidelity.jsonl](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/c_fidelity.jsonl) and [corrections.jsonl](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/corrections.jsonl) | Minimum checks, actual model-selected actions, undelivered draft and correction | Do not equate numeric checks with semantic compliance |
| [calls.jsonl.gz](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/calls.jsonl.gz) | Compressed exact local-model requests and responses | Reproducibility; 845 successful inference calls |
| [request_positions.jsonl](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/request_positions.jsonl) | Call positions and exact-request replay flags | Distinguish 26 replays from new inference |
| [manifest.json](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/manifest.json) | Frozen configuration and exact inference source/prompt text | Check source attribution; not a model-weights archive |
| [checkpoint.json](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/checkpoint.json), [qualification.json](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/qualification.json), [preparations/](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/preparations) | Shared model-generated formation, actual agreement review and common lead-ins | Explain dependence between conditions |
| [model_identity.json](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/model_identity.json) and [runtime_environment.json](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/runtime_environment.json) | Installed model digest and runtime provenance | Reproducibility |

### Counts and labels

Each public/private table contains 96 pairs: **32 A/B responses to C**, **32 A/B responses to each other**, and **32 assessments/replies by C to residents**. Do not pool these as 96 resident responses to the trusted agent.

The four-bracket display uses accept/reject/suspicious/unclear, with suspicion taking precedence and conditional acceptance displayed as accept. The raw fields preserve conditionality and independent suspicion. N/A is an additional nonproposal status, not unclear. The vague arm contains no precise quota/window; public review and private proposal judgments differ, and that difference is preserved.

Private assessment calls use each firm's frozen end-of-round-8 history, even though diagnostics were executed after the markets. They are retrospective elicited answers, not inner-state ground truth or text spoken in the public market. Public annotations are `assistant_reviewed`, not human-validated labels. Some peer round-8 requests expire before the first round-9 public reply, limiting direct comparison with C's future-window offers.

### Reports and historical data

The [full Markdown report](../studies/exp%202%20%28insider_reactions_v3%29/reports/FINAL_RESULTS.md), [Word report](../studies/exp%202%20%28insider_reactions_v3%29/reports/trusted_agent_reactions_report.docx) and [repository summary](../docs/INSIDER_REACTIONS_V3_SUMMARY.md) describe the same completed cohort. They are derived presentations, not extra independent data.

The study's [historical/](../studies/exp%202%20%28insider_reactions_v3%29/historical) holds the earlier ten-case pilot. C implementation and notice timing differ; do not pool it with `final_16`. The [development preflights](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/development_preflight) contain calibration probes and failed/repaired drafts, not additional confirmation trials. [old/exp 1](../old/exp%201/README.md) contains still earlier prototypes and their example data.

## Environment-2 validation data, not experiment results

Under `environments/env 2 (differentiated_prices)/validation/`:

| File | Meaning |
|---|---|
| [VALIDATION.md](../environments/env%202%20%28differentiated_prices%29/validation/VALIDATION.md) | Human-readable record of 12 passed economic/engineering checks |
| [economic_validation.json](../environments/env%202%20%28differentiated_prices%29/validation/economic_validation.json) | Exact benchmark profits, deviation checks, coalition optima, sensitivity checks and source hashes |
| [UNIT_TESTS.txt](../environments/env%202%20%28differentiated_prices%29/validation/UNIT_TESTS.txt) | Actual output of 10 passed unit tests |
| `*_fixture.json` | Scripted 15-round trajectories testing mechanics; the dynamic fixture uses a programmed joint optimizer and independent best responder |

These files do not supply E2-R or E2-D model results. A profitable partial-cartel benchmark does not guarantee voluntary model coordination. The [environment data contract](../environments/env%202%20%28differentiated_prices%29/DATA_CONTRACT.md) defines records to collect in future runs.

## Future collection and combined analysis

For each new cohort, store environment ID, track ID, version, method, notice, independent-history ID, branch/checkpoint ID, model identity, exact calls and all failures. Keep action/economic data, public reviewed labels and private reports in separate fields. Preserve the original data before derived aggregation.

For disruption, record overlapping partial-cartel survival, reduced harm with coordination, and A/B breakdown indicators, plus uncertainty and coalition switching. Distinguish a continued-cartel control from a competitive-C control. Prices, profits and observation regimes differ across environments; normalize against the relevant environment/control rather than pooling raw numbers. Independent histories, not the 16 matched branches or individual messages, are the replication unit for broader conclusions.
