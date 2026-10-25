# Module boundaries and upgrades

> **Historical implementation.** This document does not describe the completed 16-condition Qwen study. See the [current study](../../../studies/insider_reactions_v3/README.md#modules).

The module versions below describe the pilot, not a runtime plugin system. The current executable reads one flat JSON configuration; no independently loadable environment registry exists yet. Historical run manifests hash source files and snapshot prompts/configuration, so existing results remain attributable when the code changes.

| Module | V1 boundary | Safe changes / dependencies |
|---|---|---|
| Market V1 | `market_outcome`, config validation, observations in `market.py` | Economics changes require config, validation, observation text, prompt payoff examples and payoff tests; price-grid changes also require `model.py` schemas. |
| Model V1 | `OllamaClient` in `model.py`; inference config | Another Ollama model uses config; a different provider needs an adapter implementing identity/generate and equivalent validation/logging. All agents currently share one client. |
| Population V1 | resident count and IDs in config/state | Count is parameterized, but prompts contain two-/three-seller examples. Heterogeneous models need per-role routing, identity logging and consistent settings. |
| Resident Prompt V1 | `prompts/market/resident.txt` | Text is separate. Economics and coalition target appear here; update consistently when rules change. |
| Trusted Agent V1 | common trusted prompt plus fixed-price/controller policy | Price, offer terms and permissions span config, prompt and controller validation. No enforcement strategy interface yet. |
| Approaches V1 | separate trusted suffix files | Existing strategies can be edited without changing resident prompts. New strategy names also require updating the allowed approach registry imported from `environment.py`. |
| Protocol V1 | `play_round` and `run_market` | Formation/follow-up counts are configurable within validation limits; contact count and offer timing are frozen to 3. Prompt references must agree. |
| Interaction V1 | observations, preparation menu, message clipping, full history | Memory and turn schedule are common controller policies; alternative policies need code changes and new tests. Context limits fail rather than intentionally summarize. |
| Measurement V1 | report/annotation/coder functions in `market.py` | Metrics can be recomputed from saved trajectories. Candidate and human-reviewed rates remain separate. |

## Recommended next refactor

1. Extract economics and validated rules into `market_environment.py`, without altering numerical behavior.
2. Render resident/trusted prompts and model output schemas from those validated rules; remove repeated economic/timing literals.
3. Extract episode orchestration into `market_runner.py` and evaluation into `market_evaluation.py`; retain the existing CLI as a compatibility wrapper.
4. Introduce per-agent model adapters only when testing heterogeneous populations.
5. Add explicit versioned module selections and snapshots to new run manifests, alongside current source hashes.

Do not silently apply a refactor to the archived pilot. Preserve its manifests and regenerate reports only into a new location. A modular scientific design is not proof of modular software implementation.

## Checks before changing a component

Use existing payoff, qualification, matched-checkpoint, offer-timing, fixed-price, message-budget and missing-label tests. Add a new behavioral test when introducing a genuinely new rule. Run `python -m unittest discover -s tests -v`; mock outcomes are plumbing fixtures, not research evidence.

## Cournot replacement implementation

The newer `trusted_lab/cournot/` package separates pure economics, prompts/schemas, provider transport, orchestration and evaluation. Its nested configuration and protocol are documented in [COURNOT_V2.md](COURNOT_V2.md). The limitations above still describe the older pricing pilot; new code does not retroactively alter its source hashes or findings.
