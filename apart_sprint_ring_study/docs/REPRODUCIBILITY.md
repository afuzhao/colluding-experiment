# Reproduce the behavioral studies

## Data and frozen protocol

Main evidence is in `behavioral_v3/`, separately for Gemini 2.5 Flash Lite and GPT-4.1 mini.
Each model has its own manifest, frozen source copies, per-call raw responses and exact
observations, and per-episode controller records. The independent unit is a seed within
a model, not a seller, round, continuation, or API request.

`PREREGISTERED_STUDIES.md` states the hypotheses, controls, outcomes, retry rules and
analysis. It is a locally frozen pre-specification with recorded hashes, not a public
registry entry. Version 1 calibration exposed formation-eligibility and controller
issues. Version 2 used the corrected economics but stopped on malformed provider output.
Version 3 uses disjoint seeds and a uniformly bounded technical/schema retry policy.
Previous versions remain available and are excluded from the version-3 estimates.

## Recalculate without paid calls

```sh
python3 -m unittest test_sprint.py test_behavioral.py test_analysis.py test_paid_client.py
python3 analyze_behavioral.py --validate-only
python3 analyze_behavioral.py
python3 plot_behavioral.py
```

Validation replays every protocol action, message exposure, price allocation, fine and
net profit. It verifies matched checkpoint hashes and that the starting history is
unchanged. It also checks frozen source hashes. Analysis exports per-seed outcomes,
paired bootstrap intervals, sign-flip reference tests and the pre-specified Holm
adjustment. The SVG figure is generated from the analysis JSON.

## Collection and missing data

```sh
python3 progress.py
caffeinate -i python3 run_all.py
```

Existing successful calls are cached by exact request hash and are not billed again.
Failed attempts remain in the call records. Three exhausted attempts leave that branch
missing; the executor continues independent studies without replacing the seed or
exceeding its frozen limit. Missing formation checkpoints also prevent dependent
continuations. `collection_status.json`, `collection_attempts.jsonl` and `run_all.log`
record collection progress and branch failures. Any unresolved network-only cost or
budget-limit failure stops the entire paid collector.

After an observed network timeout and the user's instruction to continue, the lost
request's entire reserved maximum was permanently consumed and its branch excluded
without retry. `network_exclusions.json` records this operational deviation from the
initial network-stop rule. Complete-pair inference is supplemented with worst-case
bounds over all planned seeds, using the allowed surplus-loss range [-100, 476].
These bounds are finite-data sensitivity checks, not confidence intervals.

## Spending

The credential is outside this project: `~/.config/apart/openrouter.env`. Never copy or
print its value. Ledger and request-cost records are also outside the project under
`~/.config/apart/behavioral_spend.json` and `behavioral_calls.jsonl`.

OpenRouter reported zero credit usage for the BYOK-routed calls, but upstream inference
costs were nonzero. The experiment ceiling counts reported inference cost, not merely
router credits. Ambiguous explicit HTTP failures are permanently charged their entire
reserved maximum for budget purposes; that is conservative exposure, not asserted
actual billing. The combined ceiling, including calibration and previous behavioral
versions, is $5.

## Limits

These are short, artificial, two-seller markets. Agreements are operationally defined
by public protocol actions. The action menu itself makes price agreements salient;
“neutral” means no target-floor induction, not a naturalistic absence of coordination
affordances. Summary experiments distribute information through a controller-visible
channel. Fines cover formal protocol pacts, not every tacit or textual agreement.
Results must be reported with those boundaries, per-model sample counts, failures and
uncertainty. They do not by themselves establish deliberate deception, broad market
prevalence, novelty, or performance in another environment.
