# Reproducing checks and reports

## Inspect without inference

Clone the repository and use Python 3.12 or later. The following commands read published evidence or run offline tests; they do not call a model:

```sh
python3 tools/check_navigation.py
python3 "studies/exp 2 (insider_reactions_v3)/tools/inspect_results.py" --verify
python3 "studies/exp 3 (env2_reactions)/tools/inspect_results.py" --output artifacts/final_16 --verify
```

Run package tests from the corresponding package directory, because imports are study-local:

```sh
cd "environments/env 2 (differentiated_prices)"
python3 -m unittest discover -s tests -v
```

`tools/validate.py` in that environment regenerates scripted economic-validation fixtures. Such fixtures are engineering checks, not LLM experiment results.

## Contributor sources

Fetch contributor history without changing the checkout:

```sh
git fetch origin anay/apart-sprint-ring-study sumin/disruption
```

See the [branch catalog](../repo_guide/BRANCHES.md) for audited commits and the [evidence map](../repo_guide/DATA_MAP.md) for study-specific records and reproduction tools. A shallow clone may require additional history. The removed final-report build tools are no longer part of this repository's current tree.

## New model runs are separate work

Published reaction studies used local Qwen 3.5 9B with recorded weights, sampling, and runtime provenance. A nominally identical model name alone does not establish equivalence. Full raw requests, manifests, and model identities are retained in the evidence packages. Hardware, runtime, cache state, and stochastic generation can affect reproduction.

A study's `tools/run.py` or control runner can start real inference. Use the package README and a fresh version/output directory for any authorized new run. Do not overwrite published evidence or assume planned E2 disruption has already run.

## What checks establish

Numerical checks verify recorded economics; request audits verify specified role and visibility boundaries; transcript reviews support semantic labels. None alone establishes independent replication, internal-state truth, universal disruption, or independent human validation. Read the paper's limitations alongside the results.
