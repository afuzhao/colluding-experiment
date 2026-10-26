# Contributing

## Work from the evidence

Read the [study catalog](studies/README.md), [branch catalog](repo_guide/BRANCHES.md), and relevant package README before changing a protocol or interpreting a result. A shared formation branched into conditions is not independent replication. Preserve failures, correction attempts, versions, and exact denominators.

## Branch conventions

Use `main` for reviewed integrated documentation, reports, and published evidence. For new work use `study/<study-id>-<description>`, `analysis/<description>`, or `docs/<description>`. Existing contributor branches keep their names and pinned history. Submit focused pull requests describing the research question or change, data lineage, checks run, and limits.

Do not rewrite contributor history or merge a whole experimental branch merely to import a result. Integrate explicit artifacts or documented audits, preserving source commit and path. Avoid committing unfinished model output to `main`.

## Preserve completed experiments

Captured inference source and prompts belong to the evidence record. For a changed protocol, create a new version and output directory; do not alter an old manifest to make a check pass. Keep raw calls, delivered messages, model identity, seeds, and observed actions. Distinguish new inference from exact-request replay and postprocessing.

Place publishable reports and reviewed evidence in the study's `reports/` and `artifacts/` folders. Keep local results, caches, credentials, model weights, and QA intermediates out of Git. Existing stable study paths should not be renamed casually.

## Before publishing

1. Run checks appropriate to the changed package; use [reproduction guidance](docs/REPRODUCIBILITY.md).
2. Validate navigation with `python3 tools/check_navigation.py`.
3. Stage only intended source, documentation, and curated evidence.
4. Run `python3 "studies/exp 2 (insider_reactions_v3)/tools/audit_publication.py"` from the root after staging.
5. Check the staged diff, update evidence and branch catalogs where needed, and preserve methodological limitations in the report.

Navigation CI checks documentation paths only; it is not an experimental-validity or complete-reproducibility certification. The repository currently has no declared blanket license; do not add licensing or third-party materials without appropriate authority.
