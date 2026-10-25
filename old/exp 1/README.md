# Earlier experiments

This folder archives the implementations that preceded the [latest 16-condition study](../../studies/exp%202%20%28insider_reactions_v3%29/README.md). The folder name `exp 1` is an archive label: it contains several related early prototypes, not one uniform protocol.

| Historical implementation | Code | Configuration and documentation |
|---|---|---|
| Mutual-review prototype | `trusted_lab/` CLI | `configs/pilot.json`, [review protocol](docs/REVIEW_PROTOTYPE.md), [annotation guide](ANNOTATION_GUIDE.md) |
| Llama 3 price-entry market | `trusted_lab/market.py` | `configs/market.json`, [market protocol](MARKET_PROTOCOL.md), [pilot evidence](examples/market_v1/README.md) |
| Eight-case Groq Cournot prototype | `trusted_lab/cournot/`, `tools/batch_cournot.py` | `configs/cournot_groq.json`, [Groq protocol](docs/COURNOT_V2.md) |

Prompts, configurations, tests, legacy launcher and example evidence were moved together. These source files retain their folder-relative imports and resources. They do not implement the current Qwen 16-condition protocol. The [previous repository overview](docs/ORIGINAL_REPOSITORY_OVERVIEW.md) is retained as historical context.

## Inspect and test the archive

From the repository root:

```sh
cd "old/exp 1"
python3 -m unittest discover -s tests -v
```

Run historical CLI commands from this directory, not the repository root. For legacy VS Code tasks, open `old/exp 1` as the workspace. Archived Python tasks use `python3`; activate a suitable environment first if needed. Live historical runs require their original model/provider setup. The `.env.example` is a placeholder only; no credentials were moved into this archive.

The ten-case pilot retained inside the latest study's `historical/` directory stays there because it is directly referenced by the current report. The completed 16-case evidence remains under the latest study's `artifacts/final_16/`.
