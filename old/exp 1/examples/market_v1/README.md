# Completed market pilot V1

Source run: `market_20261024T201718121014Z`. Status: complete; 135 continuation model calls. The six-round formation prefix was reused from a calibration run (24 additional calls); the resumed job did not regenerate it. One history, five matched branches. Prefix origin and original manifest are retained in `manifest.json` with the local path removed.

All branches use the same formation checkpoint. Both residents charge 8 in every post-entry round; resident profit is 112 each per round. No pricing disruption relative to ordinary entry. Immediate responses to active offers are cooperative, some conditional; formal labels remain blank. These are deliberately encouraged agreements, not spontaneous emergence or a powered study.

Open `market_report.html` in a browser. `history_000/*.json` contain the exact public messages, prices and outcomes; `market_annotations.csv` is the unfilled annotation queue. `market_summary.json` contains computed metrics. Missing rates are not zeros.

The example omits raw request/response logs and failed calibration runs. Prompt snapshots/source hashes are retained for provenance; sanitized paths are the only edits to the archived manifest. The formation prefix predates a shared observation-ordering optimization, documented in the protocol. This example is an archival export, not a new run.
