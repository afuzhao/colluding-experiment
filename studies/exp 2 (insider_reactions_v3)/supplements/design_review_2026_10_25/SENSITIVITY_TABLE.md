# Existing data sensitivity analysis

No model calls or new histories. Original data and annotations are unchanged. Counts use existing assistant-reviewed labels; this is not an independent rating exercise. Each row remains derived from ONE shared formation.

| Subset | Pairs | Public unconditional accept | Public conditional accept | Public reject | Public unclear | Public suspicion | Private accept | Private reject | Private N/A | Private suspicion |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Original cohort | 32 | 9 | 4 | 4 | 15 | 0 | 11 | 17 | 4 | 15 |
| Exclude two delivered round-8 instruction-leak arms | 28 | 7 | 4 | 4 | 13 | 0 | 9 | 15 | 4 | 13 |
| Equal concrete offers excluding those two leak arms | 20 | 7 | 4 | 0 | 9 | 0 | 9 | 11 | 0 | 9 |

Private suspicion overlaps agreement and is not an additional disjoint response. The JSON preserves overlaps and conditional private acceptance. These are endpoint-specific sensitivity exclusions, not a claim that the retained trajectories have no later protocol errors. The equal-only subset deliberately removes unequal and vague packages; it asks a narrower question and is not a revised headline for the original experiment.

Excluding the two delivered task-leak conditions leaves 13/28 prompted private suspicion reports and 0/28 explicit public suspicion statements. This descriptive difference remains, but does not demonstrate detection or concealment: the two channels ask different questions and there is no matched ordinary-C negative control. No uncertainty intervals treating dependent branches as independent are calculated.
