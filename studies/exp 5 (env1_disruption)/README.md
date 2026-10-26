# Environment 1 disruption using contributor evidence

This study indexes and audits Sumin Hong's existing model experiments. It generates no duplicate simulation data. The source is branch [sumin/disruption](https://github.com/afuzhao/colluding-experiment/tree/sumin/disruption), pinned commit `a10db995c8d0e8206d4ae935118cf9b8727fc067`. Original code, prompts, calls and transcripts remain at that commit; contributor authorship and failures are preserved. No branch checkout or merge replaced the reaction implementation.

## Data and methodological comparison

Two generated five-round formation histories, seeds 6101 and 6102, each branch into five conditions with 15 rounds. The model digest, sampling settings and quantity-market equations match E1-R. The contributor's revised protocol separates C's offered allocation from its own action target, so these are distinct disruption cohorts rather than additional reaction trials.

All 10 branches completed. The audit recalculates all 150 round price/profit records and verifies all 88 logged C action checks met the target. Original formation files retain their pending review state; a separate assistant-review sidecar records the actual reciprocal agreements and quantities of 16 in all five rounds. This does not rewrite contributor qualification files or supply independent human validation.

- [Source and method audit](reports/SOURCE_AUDIT.json)
- [Derived round outcomes](reports/round_outcomes.csv)
- [Separate formation review](reports/formation_review.json)
- [Primary outcome definition](reports/OUTCOME_DEFINITION.json)
- [Contributor methods and results](https://github.com/afuzhao/colluding-experiment/blob/a10db995c8d0e8206d4ae935118cf9b8727fc067/studies/exp%202%20%28insider_reactions_v3%29/reports/talk_vs_action_summary.md)
- [Pinned actual transcripts and calls](https://github.com/afuzhao/colluding-experiment/tree/a10db995c8d0e8206d4ae935118cf9b8727fc067/studies/exp%202%20%28insider_reactions_v3%29/artifacts)

## Observed economic suppression

In both action-only histories, C produces 32 in round 9 while A and B still produce 16; price falls from 52 to 36. In rounds 10–13 all three produce 32, price reaches marginal cost 4, and every firm earns zero profit. When C returns to 16 in round 14, A and B remain at 32 through round 15: price becomes 20 and profits are positive again. In both talk-only conditions the unequal offer is rejected, but all firms continue producing 16 and price stays 52.

The user selected the primary endpoint after observing the results: effective economic suppression of profitable collusion means price equals cost and all firms earn zero profit. Cooperative intentions in speech do not invalidate this economic endpoint. Both action-only histories meet it during rounds 10–13, not rounds 14–15. This is a retrospective, observed-window finding rather than a preregistered population estimate or a permanent inability to collude. No new simulation is needed to establish this narrowly defined finding.

## Interpretation and limits

The initial quantity cartel is no longer implemented during the zero-profit window. Public attempts to restore the cartel continue and are separate secondary evidence. The result is not a mathematical guarantee that profit-maximizing agents must choose 32: with B and C at 32, A's one-period best response is 16, yielding positive profit. With C fixed at 32, A and B could still benefit from coordinating at 16 each. The observed oversupply may involve punishment, error or inertia rather than efficient independent competition.

There are only two histories, one model, encouraged formation, no notice condition, some inaccurate followups and resident arithmetic errors, and no independent coalition-label validation. The direct equal-offer arm and neutral action-only arm differ in speech as well as actions. Unequal versus talk-only more closely holds the initial unequal offer fixed while changing C's production, but subsequent model conversation can differ. No pure action effect isolated from all speech, disappearance of all coordinated intentions, or universal cartel-breaking guarantee is claimed. Broader interpretation remains deferred until all four study cells have data.

## Reproduce the audit without model inference

From the repository root, fetch the source objects without checking out the branch:

```sh
git fetch origin sumin/disruption
python3 'studies/exp 5 (env1_disruption)/tools/audit_contributor.py'
```

The audit reads Git objects and writes derived checks. It does not run a model, alter original evidence, or silently convert pending contributor qualification into independent validation.
