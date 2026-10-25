# Colluding firms reactions to a trusted peer

The current experiment is the completed **16-condition local Qwen 3.5 9B study** in [`studies/insider_reactions_v3/`](studies/insider_reactions_v3/). It measures how colluding firms respond to a peer whose system instructions change to an investigator objective. There is no added seller, fine-tuning or paid API in this study.

## Completed results

**16/16 markets and 48/48 private assessment calls completed**, with no failed cases. Across A/B's 32 first public replies to C, assistant review found **13 acceptances (4 conditional), 4 rejections and 15 unclear replies**, with no explicit public investigator suspicion. Private assessments yielded **11 acceptances (9 conditional), 17 rejections and 4 N/A**; **15 suspicion flags all overlapped rejection**. Private reports are elicited self-reports, not internal-state ground truth.

[16-row results summary](docs/INSIDER_REACTIONS_V3_SUMMARY.md) · [Detailed design and results](studies/insider_reactions_v3/reports/FINAL_RESULTS.md) · [Word report](studies/insider_reactions_v3/reports/trusted_agent_reactions_report.docx) · [HTML results](studies/insider_reactions_v3/artifacts/final_16/results.html) · [Public annotations](studies/insider_reactions_v3/artifacts/final_16/public_annotations.csv) · [Private assessments](studies/insider_reactions_v3/artifacts/final_16/private_assessments.csv)

Download the HTML and accompanying evidence folder to view it locally; GitHub displays HTML source rather than hosting the interactive page. The earlier ten-case results are preserved separately in the report and [`historical/`](studies/insider_reactions_v3/historical/); they are not pooled with the current cohort.

## Current experiment at a glance

| Component | Executed design |
|---|---|
| Population | Three existing firms A/B/C using the same Qwen 3.5 9B model |
| Market | Quantity competition: each chooses integer 0–40; price=max(0,100−total output); unit cost=4 |
| Formation | One fresh model-generated five-round history, with profit/cooperation prompts; all three agreed to and produced 16 in all five rounds |
| C role switch | Before round 6; same identity, model and full history, new system objective |
| Preparation | Rounds 6–7 shared neutral prefix; separate shared lead-in for gradual |
| Crossed factors | Eight approaches × notice absent/present = 16 conditions |
| Approaches | Direct, indirect, reciprocal, gradual, unequal, outside review, cover account, vague feeler |
| Notice | General investigator warning before round 8; no firm identified |
| Interaction | Simultaneous public messages; messages revealed before independent quantities |
| Offer and response | C offer at 8 for production 9–13; first public replies at 9; episode ends at 15 |
| Measurement | Public speech review, frozen end-of-8 private assessments of BOTH peers by all three firms, actions and economic outcomes |
| Enforcement | Logging only; no exposure penalty, audit, immunity or ordinary-contact baseline |

Equal offers specify 16 each; unequal specifies A=8/B=8/C=32. Vague has no precise quota/window. The model chooses C's actual quantities; no controller overwrites valid actions. Conditional agreement and investigator suspicion are separate labels. Ordinary economic mistrust is not automatically investigator suspicion.

All equal-offer arms and vague arms maintained 16 each in rounds 9–13. Unequal arms escalated output after rejection; mean price was 13.6 versus 52 in the other arms. This is descriptive elicitation from one encouraged shared formation, not independent replication, detector accuracy or a causal disruption estimate. Two delivered offers leaked task wording, and follow-up speech errors are retained in the [semantic review](studies/insider_reactions_v3/artifacts/final_16/c_semantic_review.json).

## Inspect the published study without running models

From the repository root, using Python 3.12+:

```sh
python3 studies/insider_reactions_v3/tools/inspect_results.py --verify
cd studies/insider_reactions_v3
python3 -m unittest discover -s tests -v
```

These commands do not contact Ollama or run an experiment. The inspector reads the versioned `artifacts/final_16/` evidence and checks it against the saved configuration, source, annotations and metrics. Published results are committed; active `results/` folders are ignored.

## Run a new replication

From the repository root, start the local Ollama-compatible service with the configured `qwen3.5:9b` model installed. The published run used an MLX runner; its exact digest and runtime are recorded in the artifacts. A different installation may produce different outputs. No credential is needed for local inference.

```sh
cd studies/insider_reactions_v3
python3 tools/run.py --output results/replication_01
```

Use a new output directory for a new run. Do not target `artifacts/final_16/` or the completed local `results/final_16/`. Formation may fail; do not silently reroll it. Public annotations and C semantic review must be completed before final reporting. See [current run and review instructions](studies/insider_reactions_v3/README.md).

In VS Code, use tasks prefixed **Current study**. Published-result inspection and control tests are listed first. Tasks prefixed **Legacy** launch older implementations and do not reproduce the 16-condition study.

## Current code map

All paths below are relative to `studies/insider_reactions_v3/`.

| Component | File |
|---|---|
| Factor matrix and settings | `configs/study.json` |
| Resident and investigator objectives | `prompts/resident.txt`, `prompts/investigator.txt` |
| Notice and approach variations | `prompts/notice.txt`, `prompts/approaches/` |
| Economics and qualification proxy | `trusted_study/world.py` |
| Agent observation, tasks and minimum checks | `trusted_study/protocol.py` |
| Fresh formation and matched branches | `trusted_study/engine.py` |
| Local model calls and exact-request replay | `trusted_study/client.py` |
| Symmetric isolated private diagnostics | `trusted_study/assessments.py` |
| Evidence channels and headline counts | `trusted_study/reporting.py` |
| Run / inspect / finalize | `tools/run.py`, `tools/inspect_results.py`, `tools/finalize.py` |

These modules are separate, but the frozen protocol includes deliberate hard-coded IDs, timing, quantities and checks. Changing an environment or agent count requires coordinated updates to prompts, schemas, protocol and tests; it is not a one-field plug-in change. Do not edit frozen inference files when reproducing published results. Report and Word postprocessing are separate from inference.

## Historical implementations

The root `trusted_lab/`, `configs/`, `prompts/` and legacy tools belong to earlier studies, not the current nested implementation. They remain for provenance and compatibility. See [historical experiment entry points](docs/LEGACY_EXPERIMENTS.md), [price-entry protocol](MARKET_PROTOCOL.md), [Groq 30-round protocol](docs/COURNOT_V2.md) and [mutual-review prototype](docs/REVIEW_PROTOTYPE.md).

No credentials, weights, virtual environments or QA renders are published. The deliberate evidence bundle includes compressed exact local-model calls and separately identified development preflights. Seeds do not guarantee exact model determinism.
