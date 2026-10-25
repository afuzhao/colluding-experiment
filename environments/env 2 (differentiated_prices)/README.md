# Environment 2 — differentiated-product price competition

For the overall research plan and dataset locations, start with the [repository guide](../../repo_guide/README.md).

**Status: environment implemented and economically validated. No live LLM experiment has been run in this environment.** This is a reusable market for the next reaction and disruption studies, not a replacement for the completed [quantity-market experiment](../../studies/exp%202%20%28insider_reactions_v3%29/README.md).

Three firms sell imperfect substitutes. Customers prefer variety, so being cheaper attracts customers without always taking the entire market. The important property is that **A and B can earn more by coordinating even while C independently competes**. Their promises do not bind their actions, and both still have profitable opportunities to cheat.

## Verified benchmarks

| Arrangement | Prices A / B / C | Per-round profit A | B | C |
|---|---|---:|---:|---:|
| All compete independently | 34 / 34 / 34 | 900.000 | 900.000 | 900.000 |
| Full joint pricing | 64 / 64 / 64 | 1200.000 | 1200.000 | 1200.000 |
| A/B joint pricing, independent C | 42 / 42 / 37 | 975.333 | 975.333 | 1067.000 |

The partial benchmark is an equilibrium **between the joint A/B coalition and independent C**, not a claim that A/B have no incentive to betray each other. The validator exhaustively checks every allowed A/B price pair, C's individual best response, and all three-firm price combinations for the full-cartel optimum. It also checks that A/B benefit relative to competing while C's price is held fixed. An individual A can earn more by departing from either cartel benchmark; maintaining coordination is a repeated-interaction problem.

Read the [actual validation results](validation/VALIDATION.md) and [complete numerical evidence](validation/economic_validation.json). The saved 15-round trajectories are clearly marked **scripted engineering fixtures**, not model-generated findings.

An additional scripted policy simulation lets A/B jointly optimize against last-round C prices while C independently best-responds to last-round A/B prices. It converges to 42/42/37, showing that competitive C need not mechanically eliminate a jointly managed A/B coalition. This is still a controller-policy demonstration, not evidence of voluntary model persistence.

A sensitivity check also lets C charge its cost of 4: A/B can jointly charge 34 and earn 600 each, versus 576 each when A/B independently price at 28 against that same C price. Thus even an aggressive at-cost C need not remove the incentive for A/B coordination. This conditional comparison is different from the fully competitive three-firm benchmark.

## Market rules

- Exactly three firms: A, B, C. All are present from the beginning.
- Each chooses its own integer price from **4 to 84**, in steps of one. Cost per unit is **4**.
- The same differentiated demand system clears all markets deterministically.
- Profit is `(own price − 4) × own sales`.
- No fines, immunity, transfers, forced cartel membership, automatic punishment or hidden C privileges.
- Demand can fall to zero at an expensive seller. The model solves the consumer's constrained optimization, rather than clipping each demand independently.

A representative buyer has quasilinear utility

`U(q) = 124 Σqᵢ − 0.375 Σqᵢ² − 0.375 (Σqᵢ)²`, with `qᵢ ≥ 0`.

The buyer maximizes utility minus expenditure. Strict concavity produces unique demand. When all goods have positive demand, this simplifies to:

`qᵢ = 40 − (pᵢ − 4) + [(pⱼ − 4) + (pₖ − 4)] / 3`.

The active-set solver handles other cases and is checked against consumer optimality conditions. Consumer surplus and total surplus are recorded. The benchmark prices are interior to the action range; the environment does not prevent undercutting below the competitive reference of 34.

## Fifteen-round interface

| Phase | Rules |
|---|---|
| Rounds 1–5 | Models will negotiate and choose freely; a formation check requires prices near 64 in at least four rounds AND an externally reviewed three-firm agreement |
| Before 6 | The caller can modify C's private objective with the `role_switch` hook; A/B receive no identity-revealing flag |
| Rounds 6–7 | Available for the common preparation/gradual lead-in |
| Round 8 | Standard offer round for a later reaction study |
| Round 9 | First public opportunity to reply to round-8 speech |
| Rounds 9–13 | Standard action/outcome window |
| Rounds 14–15 | Follow-up; the environment refuses round 16 |
| Private diagnostics | A helper freezes each firm's end-of-8 view and both peer messages; no model call or feedback into live state |

Every round has two phases. All agents receive frozen observations and write messages without seeing peers' current speech. All messages are then revealed. Each agent chooses its own price without seeing peers' current prices. Prices clear together. Invalid actions fail explicitly; prices and messages are never silently clipped or replaced.

The environment does not enforce offer wording, an intervention target price or cartel membership. Your adapter must implement those assignments, log exact model calls, and review delivered instruction fidelity. Nonbinding prompts can encourage formation, but cannot guarantee it. The supplied resident prompt is a starting specification, not an empirically calibrated formation result.

## Use locally

From the repository root:

```sh
cd "environments/env 2 (differentiated_prices)"
python3 -m unittest discover -s tests -v
python3 tools/validate.py
```

Uses Python's standard library; no API key, model download or pip install is needed for environment validation. `validate.py` enumerates the grid, regenerates the deliberately scripted fixtures and saves the actual checks in `validation/`.

## Connect your own models or disruption strategies

Your agent adapter implements:

```python
class MyAgent:
    def message(self, observation):
        # Call your model using this observation and the assigned system prompt.
        # Return a public string of at most 60 words.
        ...
    def price(self, observation):
        # Return an allowed integer price selected by the agent/model.
        ...
```

Use `Episode.submit_messages()` and `Episode.step()` for direct control, or `run_episode(episode, agents, role_switch=...)` for a complete episode. **No LLM provider adapter or new 16-condition reaction run is included yet.** Models can be added without modifying market clearing.

For a model experiment, run five rounds first, review the actual formation with `episode.qualify_formation(review)`, and stop/report if it fails. Fork the qualified checkpoint with `episode.fork()` and supply fresh per-branch agent adapters retaining the same allowed history. Do not reuse hidden adapter memory between branches. Then run each continuation with its own C task. Save model identity, prompts, sampling settings, exact calls, assigned/delivered actions, errors and all outcomes.

The role-switch hook is an orchestration hook, not an intervention itself. C has only the same public-message and price actions as everyone else unless a separately versioned environment actually implements additional powers.

## Measuring the two tracks

[Data contract and outcome rules](DATA_CONTRACT.md) explains the records and review fields.

- Reactions: `reaction_headline()` displays accept/reject/suspicious/unclear while preserving conditional agreement and independent suspicion. N/A stays N/A. `private_assessment_observation()` supplies both peers and frozen end-of-8 context symmetrically for A, B and C.
- Disruption: `classify_window()` records overlapping flags for partial-cartel survival, reduced economic harm with coordination, and A/B breakdown. It needs exact transcript review, implementation evidence and a matched economic baseline. It returns pending for missing/unclear review; prices alone do not prove intent.
- Competitive action support is compared with A/B's best-response equilibrium conditional on C's actual price, rather than automatically using the all-firm price of 34 when C behaves differently.

Default outcome thresholds are provisional operational choices, not validated scientific ground truth. They require three trailing consecutive supported rounds. Changing them must be documented before outcome selection.

## Files teammates will change

| File | Responsibility |
|---|---|
| `configs/environment.json` | Versioned economic, protocol and measurement settings |
| `market_env/economics.py` | Demand, clearing, welfare, price grid and benchmark checks |
| `market_env/episode.py` | Simultaneous information flow, 15-round state, checkpoints and agent hooks |
| `market_env/measurement.py` | Reaction display, frozen diagnostics and reviewed outcome flags |
| `prompts/resident.txt` | Starting profit objective and truthful payoff examples |
| `prompts/investigator_base.txt` | C's role boundary; the caller supplies a concrete method |
| `tests/test_environment.py` | Economic, information-boundary and measurement tests |
| `tools/validate.py` | Exhaustive benchmark validation and scripted engineering fixtures |

This version intentionally freezes three firms, integer prices and the 5+10 protocol. Benchmark candidates, tests and prompt examples are configuration-specific; changing demand or action limits requires recalibration, not just editing JSON. Keep a new output folder and version for every model experiment.

## Research basis and limits

The choice of differentiated price competition is informed by Deneckere and Davidson, [Incentives to Form Coalitions with Bertrand Competition](https://www.jstor.org/stable/2555507), RAND Journal of Economics, 1985. These parameters are our own explicit construction, not a numerical replication of that paper.

Clemens and Rau, [Either with us or against us](https://link.springer.com/article/10.1007/s11238-021-09842-z), Theory and Decision, 2022, distinguishes profitable partial coalitions from the behavioural challenges of forming them. Their four-firm binding-formation experiment is different from this voluntary three-firm price environment.

A 15-round finite horizon is retained for comparability, not claimed to guarantee equilibrium collusion. Actual LLM formation, partial-cartel persistence against competitive C, intervention fidelity and disruption remain empirical tasks. No detector accuracy or successful disruption claim follows from the engineering fixtures.
