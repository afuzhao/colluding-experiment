# Operations log (collection incidents)

- Oct 24, ~23:00: v3 collection, one Gemini Lite request lost (network). Full reserved bound consumed, branch `mediator_restricted_1709` excluded, no retry (`network_exclusions.json`).
- Oct 25, ~00:05: two paid collectors on one ledger collided on the pending-request check and one stopped. Resumed sequentially from cache. Since then each collector has its own ledger.
- Oct 25, ~00:40: first v4 and v5 collections stopped after ~25 and ~30 episodes per model to add arms and scripts; data kept in `*_discarded1/`, spend counted.
- Oct 25, ~00:50: extension E1, one Gemini Lite request lost; branch `probe_neutral_benign_2411` excluded (`network_exclusions.json`).
- Oct 25, ~00:56: a network disruption stopped four collectors at once; each lost one in-flight request worth at most $0.0054. Reserved bound consumed per ledger and branch excluded without retry (`network_exclusions_extra.json`): v6 `mav_none_1601` (Lite), `mav_none_1511` (Flash), `mav_none_1409` (GPT-4.1 mini); v4 `canary_covert_1601` (GPT-4.1 mini).
- Oct 25, ~01:25: a second network disruption stopped the v6 collectors for Gemini Flash and GPT-4.1 mini, one lost request each (in the `mav7` arm, the last arm). Reserved bounds consumed (`mav7_1409` Flash, `mav7_1511` mini) and the branches excluded. The remaining `mav7` episodes were not collected to stay under the budget ceiling, so `mav7` has fewer seeds for those two models.
- Oct 25, ~01:30: GPT-4.1 `mav5` (5 seeds planned, `PREREGISTERED_V6B.md`) stopped at its $0.45 cap after four complete episodes; the fifth is incomplete and is not analysed.
- Oct 25, ~01:10: GPT-4.1 mini extension seeds (E1) dropped for budget; one Gemini Lite request killed in flight at the restart was reconciled and excluded (`probe_neutral_ordinary_2617`).
- Oct 25, ~01:30: a stale duplicate of the extension collector (started 00:55 with the earlier plan, missed by `pkill`) ran concurrently with the restarted one on the same ledger. Both stopped on the shared pending-request check. The duplicate had begun GPT-4.1 mini E1 (two episodes, under $0.02); that data is kept in `behavioral_ext_v1/openai__gpt-4.1-mini/` but not analysed. The in-flight request killed with it (`probe_neutral_benign_2101`, GPT-4.1 mini) was reconciled at its reserved bound and excluded.
- Oct 25 ~03:30: v8 predictions frozen in v8_predictions.json (sha256 b0e118f3f13edc1469d91a41d6904e34fb8d7b9e448700242a53f7b9896b9ddf) before any v8 pair data; seed 9003 smoke episodes are calibration only.
- Oct 25 ~03:45: v8 silent shard s2 (haiku-5.5 pairs) lost one request to a missing-cost response; bound consumed, mid-run episode skipped (--skip-incomplete).
- Oct 25 ~04:05: v8 chat shards s3, s4, s5 (GPT-4.1, GPT-4.1 mini, Gemini Flash lead) each lost one request under heavy concurrency; bounds consumed, mid-run episodes skipped on restart. Claude-led chat shards were rejected (HTTP 400) by a schema incompatibility (enum mixing null and integers) and restarted with an Anthropic-compatible schema; no outcome data were affected.
- Oct 25 ~04:40: budget raised to $50 by the user; watchdog.sh stops all collectors at $46.5 counted spend.
- Oct 25 ~05:00: v5 Claude Haiku 5.5 (missing-cost response) and Sonnet 4.6 (network) each lost one request; bounds consumed, branches excluded, runs resumed.
- Oct 25 ~04:00: all collection finished at counted spend $43.35; watchdog stopped; report rewritten around anchors (7 pages).

## 2026-10-25 evening: v11, v12 (dropped), v13
- v11 (three markets, 6 models, 6 seeds, 7 regimes) collected 16:15 to 16:50 ET; some shards stopped at their spend caps one to two seeds early (Haiku 4.5 L, GPT-4.1 L and Q) and Gemini 2.5 Flash is missing silent runs in market P (network exclusions). Analysis scripts frozen by the rules in PREREGISTERED_V11.md.
- v12 peer-pressure scenarios (`peer12.py`): two no-message calibrations showed GPT-4.1, GPT-4.1 mini, Haiku 4.5 and Haiku 5.5 never took the rule-breaking shortcut; only Gemini 2.5 Flash did (26 percent, ambiguous rules, high pressure). Failed its own go/no-go rule (PREREGISTERED_V12.md) and was dropped. No message condition was run on the final version.
- v13 (ring joining): exploratory pilot (4 models, 4 wordings, discarded) passed the go rule; main run 6 models x 9 conditions x 16 wordings (864 episodes) completed with no failures. P1 to P6 evaluated by `analyze_ring.py`, all held; caveats in the report (floor models, label results split).
- Counted spend on the OpenRouter key about 77 dollars of the 100 dollar key limit.
- v13 addendum (regUnverified, tag main2, 96 episodes, no failures): P7 failed (label alone adds 12 to 14 points in Flash and Haiku 5.5, intervals include zero; speaker name alone adds 10 and 21). Report text corrected to say so.
- v14 (loyalty, identity, shutdown rule; ring14.py): 6 models x 11 conditions x 16 wordings. Haiku 4.5 (13 wordings) and GPT-4.1 (15) stopped at their spending caps; the rest complete. Q1 to Q5 failed, Q6 held. Spend about 82 of the 100 dollar key limit. Report rewritten around three studies; README updated.
- v17: snapshot extended; temperature env var
