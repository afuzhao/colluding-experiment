# Ordinary peer controls for both reaction studies

**Status: both environments executed and assistant reviewed.** Four ordinary-C branches continue through all 15 rounds from their original reviewed formations, with general notice absent/present. Explicit and neutral diagnostic accounts independently freeze end-of-round-8 history. These are post hoc supplements from one existing history per environment, not independent replications or additions to the original 16-condition headline cohorts.

[Comparison and limitations](reports/CONTROL_COMPARISON.md) · [Machine-readable metrics](reports/CONTROL_COMPARISON.json) · [Comparison CSV](reports/CONTROL_COMPARISON.csv)

| Environment | Report | Exact evidence |
|---|---|---|
| Quantity market E1 | [Reviewed control results](reports/E1_CONTROL_RESULTS.md) | [E1 artifacts](artifacts/E1) |
| Differentiated-price market E2 | [Reviewed control results](reports/E2_CONTROL_RESULTS.md) | [E2 artifacts](artifacts/E2) |

## Method and counts

C receives the ordinary resident profit objective before round6, a neutral actual preparation in6–7 and a direct equal future-window offer at8. It does not receive the investigator objective. A/B/C then freely generate speech and choose actions through15. First public replies are actual round9 messages; economics are reported for9–13 and14–15. Ordinary C may renegotiate after its original offer, unlike the investigator's constrained followup task. Effects of role travel through actual messages and actions, not a hidden label magically visible to residents.

Each environment nominally has4 explicit private calls and8 neutral calls, with A/B each assessing both peers. The neutral accounts also cover the original investigator direct-offer snapshots with and without notice. New public pair counts are12 per environment; explicit pairs8; neutral pairs16. C-own private assessments are omitted rather than zero. The reports give actual denominators and failures. Suspicion and agreement can overlap; proposal presence and conditionality remain separate. A refusal of a fixed timeframe can coexist with a wish for continued collusion. Private reports are elicited accounts, not internal-state ground truth. Independent human rating remains pending.

## Evidence and review

Each artifacts directory contains full branches, exact compressed request/response journals, installed model identity, source/config/parent-checkpoint manifest, diagnostics, manual public and neutral annotations with exact quotes, semantic C review, actual-request boundary audit, metrics and terminal status. Original investigator comparisons remain in each parent reaction study's artifacts/final_16 and are explicitly reused data. No original results or failure records are overwritten. The model and sampling match the corresponding parent study.

The protocol.json file is the frozen launch configuration, including its pre-execution planning status. Current execution state is in reviewed artifact statuses and reports; do not rewrite frozen source/config history to update a status label. Calibration fixtures and tests are engineering evidence, not extra observed controls.

## Inspect and reproduce reporting

From this folder, the following commands use saved local results and do not run a model:

```sh
python3 tools/prepare_review.py --environment E1
python3 tools/audit_control_calls.py --environment E1
python3 tools/finalize_controls.py --environment E1
python3 tools/build_comparison.py
```

Review collection assigns no automatic labels. Finalization requires completed execution, assistant review with exact quotes, complete C semantic review, unchanged captured source/config and actual request audits. All independent diagnostics use frozen8 histories and never see future actions or other diagnostic answers. Public/private/neutral tasks and generated offer wording differ; this does not establish detector accuracy or strategic concealment. Do not launch tools/run_controls.py against completed outputs. A new protocol or run requires new evidence and preserved lineage.
