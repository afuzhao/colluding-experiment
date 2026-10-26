# Three-study paper foundation

Completed descriptive synthesis of E1 reactions, E2 reactions and Sumin Hong’s E1 disruption evidence, including all four completed ordinary-C controls. No new model inference was generated for this paper. E2 disruption remains an unexecuted specification; this task stops after publication.

- [Paper](PAPER.md): factors, controls, methods, results, comparative insights and limitations.
- [Mathematical appendix](MATHEMATICAL_APPENDIX.md): implemented payoffs, deviation incentives, coalition benchmarks and exhaustive integer-grid checks.
- [Complete reaction tables](RESULTS_TABLES.md) and [machine-readable condition rows](data/reaction_conditions.csv).
- [Design evolution](DESIGN_EVOLUTION.md): original conceptual proposal versus implemented factors and measurement additions.
- [Evidence map](EVIDENCE_MAP.md): raw-data lineage, reports, failures and authorship.
- [Final-paper handoff](FINAL_PAPER_HANDOFF.md): what later work can combine and what is still missing.
- [Derived evidence summary](data/evidence_summary.json) and [mathematical checks](data/mathematical_checks.json).

Rebuild derived summaries from the repository root with `python3 papers/three_study_foundation/tools/build_evidence.py`. This imports the implemented market code and makes no model calls. Source hashes accompany the derived summaries. Input control publication is pinned at `75ae5a54374cc0ee31ba6dbe45add3adf7f8f4ff`; Sumin’s source is pinned separately in the evidence map.

Reaction branches share one formation per environment, controls reuse those formations, and E1 disruption has two histories. These are not pooled independent replications. Assistant labels are not independent human validation. Original failures, revised prompts, delivered task leaks and retrospective endpoint selection remain explicit. Existing study Word reports remain linked in the evidence map; this foundation is provided as Markdown with reproducible data.
