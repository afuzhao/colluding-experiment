# AI Collusion Research

**Experiments on reactions, coordination, and disruption in AI markets**

Research code, reviewed evidence, and study-specific reports. The final paper and its title have not been finalized. We study how AI firms respond to insider proposals and competitive actions, and distinguish what agents say, their immediate actions, and subsequent market outcomes. This is a research repository; GitHub publication does not constitute event submission or endorsement.


## Start here

| I want to… | Start with |
|---|---|
| Read the findings and limitations | [Three-study foundation](papers/three_study_foundation/README.md) |
| Understand the experiments | [Study catalog](studies/README.md) |
| Inspect data, transcripts, and annotations | [Evidence map](repo_guide/DATA_MAP.md) |
| Reproduce checks and figures | [Reproduction guide](docs/REPRODUCIBILITY.md) |
| Find work on other branches | [Branch catalog](repo_guide/BRANCHES.md) |
| Extend the project | [Contributing](CONTRIBUTING.md) and [development guide](docs/DEVELOPMENT_GUIDE.md) |

## Research coverage

| Study | Evidence available | Status |
|---|---|---|
| [E1 reaction](studies/exp%202%20%28insider_reactions_v3%29/README.md) | 16 matched conditions and 48 private calls from one shared formation | Complete |
| [E2 reaction](studies/exp%203%20%28env2_reactions%29/README.md) | 14 original completions and two separately revised reciprocal continuations; original failures retained | Complete, versioned |
| [Ordinary-C controls](studies/exp%204%20%28ordinary_peer_controls%29/README.md) | Two full 15-round conditions per environment; reused formation histories | Complete supplement |
| [E1 disruption](studies/exp%205%20%28env1_disruption%29/README.md) | Audited contributor data: five conditions across two histories | Complete for the scoped economic endpoint |
| [Three-firm E2 disruption](studies/exp%206%20%28env2_disruption%29/README.md) | Assigned design and contributor comparison | Not executed; no run queued |
| [Other-market contributor experiments](repo_guide/BRANCHES.md) | Two-firm forged-message and related experiments on contributor branches | Separate datasets and pinned versions |

Reaction branches are matched continuations, not independent histories. Public replies, private diagnostic answers, and actions are distinct measurements. Source revisions, failed offers, retrospective endpoints, and limits are documented in the study reports. Other-market contributor results are not three-firm E2 disruption data.

## Repository layout

```text
papers/          Three-study foundation and submission planning
studies/         Study implementations, reviewed reports, and published artifacts
environments/    Reusable economic environment and engineering validation
repo_guide/      Evidence map, branch catalog, and collaborator handoff
docs/            Reproduction, development, and study summaries
tools/           Repository maintenance checks
old/             Historical prototype archive
```

Study folder names are stable historical identifiers. [The catalog](studies/README.md) maps them to research IDs. Published evidence lives in `artifacts/`; local `results/`, `work/`, caches, and weights are not part of the public evidence bundle.

## Quick verification

From a clone with Python 3.12 or later, these commands do not call a model:

```sh
python3 tools/check_navigation.py
python3 "studies/exp 2 (insider_reactions_v3)/tools/inspect_results.py" --verify
```

See [reproduction instructions](docs/REPRODUCIBILITY.md) for economics tests, pinned contributor sources, and figure generation. Live inference requires a separate explicit run and the recorded model configuration.

## Versions and reuse

`main` is the integrated research and evidence entry point. Contributor branches retain their separate code and data; [the branch catalog](repo_guide/BRANCHES.md) identifies the exact commits used. Do not treat a moving branch tip as the version behind a published result.

The [three-study foundation](papers/three_study_foundation/README.md) preserves the synthesis and mathematics for the three completed study cells. A final paper and title remain to be agreed. No repository-wide license is currently declared; consult the relevant rights holders before redistribution beyond applicable permissions.
