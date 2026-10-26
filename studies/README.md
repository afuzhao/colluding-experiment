# Study catalog

Use these research IDs when discussing results. Directory numbers reflect development history, not the order of the research questions.

| Research ID | Package | Role and status | Published results |
|---|---|---|---|
| E1-R | [exp 2](exp%202%20%28insider_reactions_v3%29/README.md) | Quantity-market reactions; complete | [Report](exp%202%20%28insider_reactions_v3%29/reports/FINAL_RESULTS.md) |
| E2-R | [exp 3](exp%203%20%28env2_reactions%29/README.md) | Differentiated-price reactions; original and repaired versions separate | [Report](exp%203%20%28env2_reactions%29/reports/FINAL_RESULTS.md) |
| Controls | [exp 4](exp%204%20%28ordinary_peer_controls%29/README.md) | Four ordinary-C continuations; complete | [Comparison](exp%204%20%28ordinary_peer_controls%29/reports/CONTROL_COMPARISON.md) |
| E1-D | [exp 5](exp%205%20%28env1_disruption%29/README.md) | Audit and reuse of existing quantity-disruption evidence | [Source audit](exp%205%20%28env1_disruption%29/reports/SOURCE_AUDIT.json) |
| E2-D | [exp 6](exp%206%20%28env2_disruption%29/README.md) | Assigned three-firm disruption design; not executed | [Specification](exp%206%20%28env2_disruption%29/protocols/ASSIGNED_DESIGN.md) |

## Package conventions

- `configs/`, `prompts/`, implementation modules, and `tools/`: study-specific source; consult the package README before running.
- `reports/`: human-readable interpretations and derived metrics.
- `artifacts/`: published records, including captured source, raw calls, trajectories, and reviews as applicable.
- `results/` and `work/`: local execution and review files; not evidence available in a fresh clone.
- `historical/` and development artifacts: earlier or calibration records, kept separate from final cohorts.

Do not rename completed packages or rewrite their manifests merely to standardize the layout. Source guards, cross-study imports, and historical links rely on these locations. New studies should use descriptive names and an explicit research ID.

[Evidence map](../repo_guide/DATA_MAP.md) · [Contributor branches](../repo_guide/BRANCHES.md) · [Historical prototypes](../old/README.md)
