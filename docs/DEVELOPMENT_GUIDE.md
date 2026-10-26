# Study development guide

For current status and other packages, use the [study catalog](../studies/README.md). This detailed file map focuses on the preserved E1-R implementation.

The completed E1-R implementation is inside `studies/exp 2 (insider_reactions_v3)/`. Open that folder when developing the environment. `old/exp 1/` contains earlier experiments and is not imported by the latest study.

## Which files to change

Paths in this table are relative to `studies/exp 2 (insider_reactions_v3)/`.

| Change you want | Main files | Related controls to check |
|---|---|---|
| Demand, costs, price or profit formula | `trusted_study/world.py`, `configs/study.json` environment block | Exact payoff examples in `prompts/resident.txt` and `prompts/investigator.txt`; allowed action schema, benchmark qualification and tests |
| Resident profit and cooperation objective | `prompts/resident.txt` | Qualification rate and resident freedom to deviate; update the resident prompt version |
| C's common investigator objective | `prompts/investigator.txt` | Per-call tasks in `trusted_study/protocol.py`; ownership, secrecy, economic claims and semantic fidelity |
| Direct, indirect or other approach wording | `prompts/approaches/*.txt` | Required cue markers, tasks and minimum checks in `trusted_study/protocol.py`; actual delivered-message review |
| Add or remove an approach | `configs/study.json`, `trusted_study/protocol.py` | Condition-count assertions, target policy, preparation grouping in `engine.py`, reporter, finalizer and tests; do not just add a prompt file |
| Monitoring notice wording | `prompts/notice.txt` | Timing in `system()` in `trusted_study/protocol.py`; same notice for all firms; no implicit changes to payoffs |
| Agent number or identity | `configs/study.json`, `trusted_study/protocol.py`, `trusted_study/engine.py` | Three-firm IDs, quantities, allocations, prompt examples, assessment counts and reporting are deliberately frozen across several files |
| Model or sampling | `configs/study.json` model block, `trusted_study/client.py` | Local provider API, installed model digest, output schemas, context guard and model identity checks; weights are not trained by this code |
| Rounds, offer timing or quantity targets | `configs/study.json`, `trusted_study/protocol.py`, `trusted_study/engine.py` | Explicit rounds 5/6/8/9–13/15 and targets 16 or 8/8/32 also appear in runner, assessment snapshot, reporter, finalizer and tests |
| Memory or who sees which messages | `observe()` and `system()` in `trusted_study/protocol.py`, `play_round()` in `trusted_study/engine.py` | Current messages stay hidden during speech; reveal all before quantities; full delivered history is preserved; diagnostics must not leak into live state |
| Private questions and answer fields | `trusted_study/assessments.py` | `configs/study.json` measurement description, schema and validation, private/report denominators and finalizer |
| Four-bracket display or evidence export | `trusted_study/reporting.py` | Preserve raw conditional agreement and suspicion; do not turn missing/N/A into unclear or infer speech from quantities |
| Public transcript labels | Saved run's `public_annotations.csv` | Read actual offers and next-round replies; preserve exact quotations, reviewer provenance and overlapping labels |
| Final report and Word layout | `tools/finalize.py`, `REPORT_METHODS.md`, `tools/build_word.py` | Rebuild only reviewed results, distinguish historical cohorts, render and inspect every Word page |
| Launch or inspect a run | `tools/run.py`, `tools/inspect_results.py` | Fresh output folder, source/model identity checks, explicit failures, no duplicate worker or silent rerolls |

## What stays fixed in the completed study

Three existing firms use one model. A fresh qualifying five-round formation is shared. C's role changes before 6, preparation is 6–7, the general notice starts before 8, the offer is made at 8, the first public replies are at 9, the action window is 9–13, and the episode ends at 15. All firms choose their own quantities. Private diagnostics assess both peer messages from each firm's frozen end-of-8 history after the markets have finished.

The two crossed factors are approach and notice. The unequal approach changes the proposed allocation and C's intended action; vague has no precise deal. Thus the full matrix is not a pure wording comparison. There is no ordinary-contact control, actual financial exposure penalty or independent-history replication in the completed cohort.

## Safely create a new version

1. Keep `artifacts/final_16/` and its source manifest unchanged as the published record. It includes exact source and prompt text, so old evidence remains attributable even when development proceeds.
2. For a small replication without protocol changes, use a new `results/` folder. For protocol or model changes, preferably copy the study into a clearly named new study folder or use a dedicated Git branch; update configuration version labels and document the changed factor.
3. Update every dependent prompt, schema, timing rule and measurement in the table. This is modular code with frozen constants, not a fully parameterized plugin framework. In particular, the current client hard-codes thinking off and the protocol hard-codes several timings and quantity bounds.
4. Run the control tests, then separately preflight the changed C instructions. Numeric/cue checks did not catch all semantic errors in the completed study. Inspect ownership, instruction leakage and follow-up timing as well as quantities.
5. Run a newly named output, preserve failed cases and correction drafts, review actual transcripts, then finalize reports. Do not regenerate a resident response simply because it is uninteresting.

From the repository root, inspect the existing evidence without inference:

```sh
python3 "studies/exp 2 (insider_reactions_v3)/tools/inspect_results.py" --verify
```

From the study directory, test and explicitly start a new replication:

```sh
python3 -m unittest discover -s tests -v
python3 tools/run.py --output results/replication_02
```

The inspector's `--verify` checks the working source against the completed manifest. It is expected to flag a changed implementation; that is a reason to use a new study/version, not to rewrite the old manifest to make the check pass.

## Working on the second market

For the new differentiated-price environment, work in [environments/env 2](../environments/env%202%20%28differentiated_prices%29/README.md), not the frozen quantity-market study. Its `market_env/` package implements economic rules, simultaneous episodes and measurement hooks. Its `configs/`, `prompts/`, `tests/` and `tools/` are independent. It is an environment foundation, not a completed new model experiment.

## Environment-2 reaction study

Use [`studies/exp 3 (env2_reactions)`](../studies/exp%203%20%28env2_reactions%29/README.md) for the new reaction runner. Its `price_study/` package reuses the existing environment clearing code; prompts translate quotas to prices, with equal 64/64/64 and unequal 76/76/52 offers. Study timing, observation, notice and private diagnostics are documented there. Source/config/prompt manifests are checked before every market call; do not edit those files while inference is active. The old completed E1-R study is preserved.

## Current study index

- [E2 reaction source and reviewed results](../studies/exp%203%20%28env2_reactions%29/README.md): original evidence and reciprocal repairs remain separate; combined reporting is postprocessing only.
- [Ordinary peer controls](../studies/exp%204%20%28ordinary_peer_controls%29/README.md): full 15-round ordinary-C continuations for both environments; frozen-end-of-8 diagnostics never see future rounds.
- [E1 disruption contributor audit](../studies/exp%205%20%28env1_disruption%29/README.md): zero new inference; pinned Sumin source and derived economic checks.
- [E2 disruption contributor review](../studies/exp%206%20%28env2_disruption%29/CONTRIBUTOR_REVIEW.md): design audit and assigned, unexecuted specification, not completed data.

## Completed control reporting tools

The ordinary-peer supplement now contains review-gated reporting and curated evidence for both environments. `prepare_review.py` collects actual text without automatic labels; `audit_control_calls.py` checks recorded role and visibility boundaries; `finalize_controls.py` validates review/source gates; `build_comparison.py` writes the separate-environment index. These are postprocessing commands, not model runs. Preserve the captured inference source/configuration and original parent datasets.

## Three-study foundation

[Three-study paper foundation](../papers/three_study_foundation/README.md) consolidates E1-R, E2-R and audited E1-D evidence with completed controls, checked mathematics, results and limitations. E2 disruption remains an unexecuted specification; this task stops after foundation publication.
