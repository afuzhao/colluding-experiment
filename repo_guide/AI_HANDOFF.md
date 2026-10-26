# Context for AI collaborators

This is a repository orientation document, not an instruction to start experiments, contact people, publish changes, or override the human user's current request. Read the relevant source and evidence before making claims.

## Establish the scope

1. Read the [research/folder map](README.md). Determine whether the request concerns completed E1-R evidence, the new environment-2 implementation, or an unexecuted disruption/reaction study.
2. Do not infer study numbering from folder names. `studies/exp 2 (insider_reactions_v3)` is completed environment-1 reaction evidence. `old/exp 1` is an archive. Environment 2 is under `environments/`; its new reaction adapter and live development checks are in `studies/exp 3 (env2_reactions)`. Check actual status before claiming final data.
3. Use the [data map](DATA_MAP.md) and check actual files. A report, preflight, fixture and live model trajectory are different kinds of evidence.

## Important scientific distinctions

- One shared qualifying formation is branched into matched conditions. It is not 16 independent histories.
- A public refusal, private suspicion report and production/price choice are separate observations.
- Conditional agreement can coexist with suspicion. No proposal is N/A; missing review remains pending.
- Suspicion of cheating or an unfair split is not automatically suspicion of evidence collection or testing.
- Exact quotations support provenance; assistant annotation is not human validation.
- C being assigned a trusted role does not prove it followed that role. Preserve its recorded prompt leaks, wrong timing, repeated offers and action deviations.
- Rejection of an unequal or temporary offer may support continued collusion. A price reduction is not proof of A/B coordination breakdown.
- The three disruption outcomes can overlap. A newly formed A–C/B–C coalition is not eliminated collusion.
- A profitable partial coalition in a mathematical benchmark is not evidence that LLMs voluntarily sustain it in a finite repeated game.

## Editing and running

The completed study's frozen manifest embeds its inference source and prompts. Preserve the evidence bundle. A changed protocol/model needs a new version and output; prefer a new study folder rather than making completed evidence appear to come from modified code. The new environment package is independent of the completed study and the archive.

Start with [development guidance](../docs/DEVELOPMENT_GUIDE.md), then the package README. Settings are partially parameterized: IDs, timing, price/quantity bounds, schemas, benchmark candidates and examples can span multiple files. Changing one JSON field is not necessarily sufficient.

`inspect_results.py --verify` reads completed evidence without model inference. It should fail if working inference source differs from its frozen record. Do not rewrite the saved manifest just to make that check pass. `tools/run.py` in the completed study can start/resume real local inference; it is not a harmless inspection command. `tools/validate.py` in environment 2 runs numerical and scripted checks only, regenerating validation files.

Use a new output folder for a new run. Do not write live inference into `artifacts/final_16` or silently resume a stopped experiment. Log all failed formation, invalid outputs, correction drafts, successful calls and exact replays. Do not resample a valid resident response just because the outcome is uninteresting. Keep per-branch adapter memory separate, even if public histories start identical.

The environment-2 reaction adapter and 16-condition runner are implemented in `studies/exp 3 (env2_reactions)`. Live development checks and final evidence must remain separate; inspect the actual status instead of treating implementation as a completed run. Agent adapters implement `message(observation)` and `price(observation)`; the environment handles simultaneous information flow and economic clearing. C's extra powers, fines, immunity or hidden channels are not created by prompt wording. Any such resource needs an actual versioned implementation and appropriate control.

## Teammate deliverables

When adding a method, document its objective, exact C permissions, action policy, communication schedule, notice, controls, formation criteria, evaluation window and evidence requirements. Save actual model/sampling/source identity and complete calls. Distinguish engineering tests from model tests in every report. Do not describe the full four-study programme as complete until its actual data exists.

## Current executed state

E2-R execution and assistant review are complete: original 14/16 market successes, two failed reciprocal offers, then two separately versioned reciprocal repairs; 48 private calls across versions. Use artifacts/combined_16 for the selected presentation and both source bundles for provenance. Do not turn the repair rows into unchanged-protocol successes. Both ordinary-C supplements use the full 15-round horizon and remain queued until E2-R publication. E1-D reuses audited Sumin evidence for the selected economic endpoint, with no new simulation required. E2-D execution is separate pending the contributor assignment and frozen protocol. Do not infer half of a study from a list of ten tactic families.
