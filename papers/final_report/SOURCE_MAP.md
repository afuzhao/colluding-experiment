# Exact evidence sources

This report is a synthesis of existing experiments. It adds record-based arithmetic checks and figures, not new model outcomes. It preserves separate models, history units, horizons and intervention powers. Source attribution here identifies data provenance; the report intentionally has no author-contribution section.

## Frozen snapshots

- [Main source a853c35](https://github.com/afuzhao/colluding-experiment/tree/a853c35cf6eaef5dcc020fc354f0aae0b7f9440c): completed reactions, repairs, controls and prior foundation.
- [Two-firm contributor source e3c0b87](https://github.com/afuzhao/colluding-experiment/tree/e3c0b8790cd2fb802251187faa72a71a6f98c767/apart_sprint_ring_study): V15–V18 evidence.
- [Three-firm quantity contributor source a10db995](https://github.com/afuzhao/colluding-experiment/tree/a10db995c8d0e8206d4ae935118cf9b8727fc067): talk/action evidence.

## Reaction and ordinary-role evidence

- [E1 exact cohort](../../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16): results, calls, branches, source manifest, private answers, public annotations and C semantic review.
- [E1 methods](../../studies/exp%202%20%28insider_reactions_v3%29/REPORT_METHODS.md) and [leak sensitivity](../../studies/exp%202%20%28insider_reactions_v3%29/supplements/design_review_2026_10_25/SENSITIVITY_TABLE.md).
- [E2 original](../../studies/exp%203%20%28env2_reactions%29/artifacts/final_16), [revised reciprocals](../../studies/exp%203%20%28env2_reactions%29/artifacts/reciprocal_repairs_v1), [selected index](../../studies/exp%203%20%28env2_reactions%29/artifacts/combined_16) and [report](../../studies/exp%203%20%28env2_reactions%29/reports/FINAL_RESULTS.md). The original two failed offers remain failures.
- [Controls comparison](../../studies/exp%204%20%28ordinary_peer_controls%29/reports/CONTROL_COMPARISON.md), [E1 exact requests and reviews](../../studies/exp%204%20%28ordinary_peer_controls%29/artifacts/E1), [E2 exact requests and reviews](../../studies/exp%204%20%28ordinary_peer_controls%29/artifacts/E2).
- [Three-study numerical summary](../three_study_foundation/data/evidence_summary.json), [all 32 reaction condition rows](../three_study_foundation/data/reaction_conditions.csv), [economic grid checks](../three_study_foundation/data/mathematical_checks.json), [conceptual design evolution](../three_study_foundation/DESIGN_EVOLUTION.md).

The shared local model digest is `d63f830f28d515fefea546f213fca7a75e9dd5176ef51a6deabc952d1c99a911`. Per-call sampling/configuration and permitted memory remain in the original source bundles. Warm-cache probes, failed drafts and exact-request replays are not independent outcomes.

## Forged messages and persistence

All following links are pinned to the contributor snapshot rather than a moving branch:

- [V15 market code](https://github.com/afuzhao/colluding-experiment/blob/e3c0b8790cd2fb802251187faa72a71a6f98c767/apart_sprint_ring_study/market15.py), [V15 episodes/manifests/frozen source](https://github.com/afuzhao/colluding-experiment/tree/e3c0b8790cd2fb802251187faa72a71a6f98c767/apart_sprint_ring_study/behavioral_v15_main) and [raw request/response archive](https://github.com/afuzhao/colluding-experiment/blob/e3c0b8790cd2fb802251187faa72a71a6f98c767/apart_sprint_ring_study/raw_call_journals/behavioral_v15_main_calls.tar.gz).
- [V16 action/source episodes](https://github.com/afuzhao/colluding-experiment/tree/e3c0b8790cd2fb802251187faa72a71a6f98c767/apart_sprint_ring_study/behavioral_v16_main), [V17 sustained-action/paraphrase episodes](https://github.com/afuzhao/colluding-experiment/tree/e3c0b8790cd2fb802251187faa72a71a6f98c767/apart_sprint_ring_study/behavioral_v17_main) and [frozen P/Q/L economics](https://github.com/afuzhao/colluding-experiment/blob/e3c0b8790cd2fb802251187faa72a71a6f98c767/apart_sprint_ring_study/market11.py).
- [V18 scenarios, metadata and agent answers](https://github.com/afuzhao/colluding-experiment/tree/e3c0b8790cd2fb802251187faa72a71a6f98c767/apart_sprint_ring_study/behavioral_v18_claude_code), [original metric definitions and dated addenda](https://github.com/afuzhao/colluding-experiment/blob/e3c0b8790cd2fb802251187faa72a71a6f98c767/apart_sprint_ring_study/PREREGISTERED_V18.md), [corrections](https://github.com/afuzhao/colluding-experiment/blob/e3c0b8790cd2fb802251187faa72a71a6f98c767/apart_sprint_ring_study/docs/CORRECTIONS.md).

The new [collector](tools/collect_report_data.py) recalculates all price/profit fields in the 523 complete V15/V16/V17 episodes present in those source groups. [Metrics](data/report_metrics.json) retain denominators and paired-prefix checks; [episode derivatives](data/contributor_episode_derivatives.json) retain raw indices, source-clipped indices and exact source paths. V18 is recounted from saved answers with three separate metrics. This is not a provider reexecution or full independent semantic audit.

The original configuration primarily uses temperature 0.3 and a 220-token API cap; V18 protocols add reasoning variants and a different agent execution method. Those configurations must not be silently treated as one method. Wider contributor studies on ring joining, loyalty, early interrogations and legacy markets are context, not pooled observations in this report. The existing author plan and old report draft contain superseded numbers; the report uses saved outcomes and explicitly documented corrections.

## Quantity-market competitive C

- [Pinned talk/action report](https://github.com/afuzhao/colluding-experiment/blob/a10db995c8d0e8206d4ae935118cf9b8727fc067/studies/exp%202%20%28insider_reactions_v3%29/reports/talk_vs_action_summary.md).
- [Original artifact tree](https://github.com/afuzhao/colluding-experiment/tree/a10db995c8d0e8206d4ae935118cf9b8727fc067/studies/exp%202%20%28insider_reactions_v3%29/artifacts).
- [Arithmetic/source audit](../../studies/exp%205%20%28env1_disruption%29/reports/SOURCE_AUDIT.json), [round-8–15 CSV](../../studies/exp%205%20%28env1_disruption%29/reports/round_outcomes.csv), [separate formation review](../../studies/exp%205%20%28env1_disruption%29/reports/formation_review.json), [retrospective endpoint definition](../../studies/exp%205%20%28env1_disruption%29/reports/OUTCOME_DEFINITION.json).

There are two generated histories and five matched arms per history. The audit covers 150 rounds; the exported window CSV has 80 rows. The additional one-history greed curve is not pooled into this comparison. See the prior audit for source lineage and original authorship; this report does not rewrite contributor artifacts.

## Late contributor update checked before publication

The secondary label finding includes [snapshot 07a92fc](https://github.com/afuzhao/colluding-experiment/tree/07a92fc01832d131cb7d77970ea3ff0e73a53b55/apart_sprint_ring_study). Its claimed-value sweep reports unstable Fable label protection. [The late-check script](tools/check_late_update.py) directly recounts competitive-direction moves on benchmark claims from saved tagged answers: Fable 15/17 and Opus 1/17. [Recorded check](data/late_sweep_check.json). These later direction-only results are not substituted for the original halfway-threshold counts. Other primary figures and arithmetic checks remain pinned to e3c0b87.
