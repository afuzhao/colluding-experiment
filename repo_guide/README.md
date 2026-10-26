# Start here — repository guide

This guide explains the research plan, what has actually been completed, and where people or AI assistants should work. Read it before interpreting a folder name as an experiment number or starting a model run.

## The research programme

We want two environments, each with two research tracks:

| Study ID used in this guide | Environment | Question | Current status |
|---|---|---|---|
| E1-R | Environment 1: quantity competition | How do colluding agents react to a trusted peer? | Completed: 16 conditions, 15 rounds each, 48 private assessment calls |
| E1-D | Environment 1: quantity competition | Can a trusted peer disrupt coordination or reduce harm? | Existing Sumin Hong cohorts audited for the selected economic-suppression endpoint; see exp 5 |
| E2-R | Environment 2: differentiated-product pricing | How do colluding agents react to the same approach families? | Complete with original 14/16 markets plus two separately revised reciprocal continuations; 48 eligible private calls across versions |
| E2-D | Environment 2: differentiated-product pricing | Can a trusted peer break a cartel that can survive without it? | Planned; no live LLM disruption run yet |

The study IDs above are navigation labels for the four-part plan, not new dataset names. The completed E1-R cohort happens to live in a folder named **`exp 2 (insider_reactions_v3)`** because earlier prototypes preceded it. **`old/exp 1` is an archive, not E1-R.** Folder names and the new research-plan numbering are different.

The final combined analysis is intended after data from all four studies is collected. Existing reports describe the completed cohort only; they are not a four-study comparison.

## Folder map

```text
README.md                                      Repository landing page
repo_guide/                                    This guide for people and AI assistants
  README.md                                    Research map and starting commands
  DATA_MAP.md                                  Authoritative evidence and formats
  AI_HANDOFF.md                                Context and safeguards for AI collaborators
studies/exp 2 (insider_reactions_v3)/            Completed E1-R implementation and evidence
  configs/                                     Exact study settings
  prompts/                                     Resident/C objectives and eight approaches
  trusted_study/                               Economics, protocol, model calls and reports
  tools/                                       Run, inspect, review-gated finalize and Word
  reports/                                     Detailed Markdown and Word report
  artifacts/final_16/                           Published completed 16-condition cohort
  artifacts/development_preflight/              Separate development-only tests/drafts
  historical/                                  Earlier ten-case pilot, kept separate
  results/                                     Ignored LOCAL outputs, not available on a fresh clone
studies/exp 3 (env2_reactions)/                 Completed E2-R original cohort and separate repairs
  price_study/                                 Price-market model adapter and reaction protocol
  configs/ prompts/ tests/ tools/ reports/       New study controls and review-gated reports
  results/                                     Ignored active local development/final data
  artifacts/                                   Curated evidence after final review
environments/env 2 (differentiated_prices)/      New reusable environment for E2-R and E2-D
  configs/                                     Economic/protocol/measurement settings
  market_env/                                  Clearing, simultaneous episodes, measurement hooks
  prompts/                                     Starting resident and investigator instructions
  tests/                                       Environment control tests
  tools/validate.py                            Economic validation; NO model calls
  validation/                                  Actual checks and SCRIPTED engineering fixtures
docs/                                          Summary, development guide and review notes
old/exp 1/                                     Earlier code, prompts, tests and example evidence
.vscode/tasks.json                             Current-study and environment-2 tasks
```

## Where should I start?

| Goal | Read or open |
|---|---|
| See the completed reaction results | [E1-R results table](../studies/exp%202%20%28insider_reactions_v3%29/artifacts/final_16/RESULTS_TABLE.md) |
| Find transcripts, annotations and raw calls | [Data map](DATA_MAP.md) |
| Understand the completed protocol | [E1-R methods](../studies/exp%202%20%28insider_reactions_v3%29/REPORT_METHODS.md) and [full report](../studies/exp%202%20%28insider_reactions_v3%29/reports/FINAL_RESULTS.md) |
| Develop a method in the new price market | [Environment 2 README](../environments/env%202%20%28differentiated_prices%29/README.md) and [data/API contract](../environments/env%202%20%28differentiated_prices%29/DATA_CONTRACT.md) |
| Identify which files to change | [Development guide](../docs/DEVELOPMENT_GUIDE.md) and the file maps in the two package READMEs |
| Hand this work to an AI assistant | [AI handoff](AI_HANDOFF.md), then the relevant package README |
| Inspect the original prototypes | [Archive README](../old/exp%201/README.md) |

## What the completed study does

E1-R uses three existing firms A/B/C, all with local Qwen 3.5 9B. Five model-generated formation rounds are shared across matched continuations. C keeps its model, identity and full permitted history but receives an investigator objective before round 6. Preparation occupies 6–7; a general notice is introduced before 8 in notice conditions. The offer is at 8, the first public reply at 9, the action window is 9–13, and follow-up ends at 15.

Eight approaches are crossed with notice absent/present: direct, indirect, reciprocal, gradual, unequal, outside review, cover account and vague feeler. Public response labels and private reports are separate. Agreement and investigator suspicion are also separate; conditionality and overlaps are retained. The completed data is one shared qualifying formation and matched branches, not 16 independent histories.

## What environment 2 provides

A standalone 15-round price-setting market with three differentiated products, simultaneous information boundaries, formation-review hooks, agent interfaces, frozen private-diagnostic observations and provisional disruption measurements. Both full joint pricing and A/B joint pricing against independent C can be profitable, while unilateral cheating remains possible.

The environment package itself contains **10 unit tests and 12 economic/engineering checks**. The saved trajectories are scripted fixtures, including a joint-optimizer A/B pair facing independently optimizing C. They are not model-generated cartel formation, voluntary partial-cartel persistence, or successful disruption results. The new reaction adapter and runner are in `studies/exp 3 (env2_reactions)`, with completed original and repaired reaction evidence separate from development. A dedicated disruption runner/study remains future work.

## Safe inspection commands

Run the following from the repository root. Neither command starts model inference:

```sh
python3 "studies/exp 2 (insider_reactions_v3)/tools/inspect_results.py" --verify
```

For environment-2 controls and economic checks:

```sh
cd "environments/env 2 (differentiated_prices)"
python3 -m unittest discover -s tests -v
python3 tools/validate.py
```

The validator regenerates its deliberately scripted validation outputs. For legacy tests, use the archive as the working directory. Python commands and imports are package-directory dependent; this repository is not installed as one global Python package.

## Before a new live experiment

Define the environment, reaction/disruption track, intervention, controls, formation rule, timing, model and independent-history count. Keep a new version/output directory, isolate model memory across branches, and log exact prompts, model identity, calls, failures and delivered actions. Do not silently regenerate failed formation or resident responses to obtain a desired outcome. Keep the completed cohort and its source manifest intact.

## Supplements and remaining work

[E2-R selected results](../studies/exp%203%20%28env2_reactions%29/artifacts/combined_16/RESULTS_TABLE.md) preserve the original failures and mark revised reciprocal rows. [Ordinary-C controls](../studies/exp%204%20%28ordinary_peer_controls%29/README.md) are implemented and queued for both reaction studies, each with two full 15-round conditions. [E1-D](../studies/exp%205%20%28env1_disruption%29/README.md) reuses Sumin Hong's two histories and reports the user-selected retrospective zero-profit endpoint during rounds 10–13. Profits recover after that window. [E2-D review](../studies/exp%206%20%28env2_disruption%29/CONTRIBUTOR_REVIEW.md) distinguishes Anay's other-market experiments from the proposed three-firm price-market study. The contributors' assigned run split still needs an exact condition/history allocation before our half starts.
