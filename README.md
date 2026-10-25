# Undercover-agent collusion experiment

A local, standard-library Python research prototype comparing four undercover conversational approaches with ordinary entry into an induced colluding market. All actors use Llama 3 8B through Ollama. No training or paid API is required.

## New: three-firm Groq/Qwen replacement study

The eight-condition study is implemented separately in `trusted_lab/cournot/`: three firms, 10 shared formation rounds, C takeover at round 11, four approaches × notice absent/present, 30 total rounds. See [setup and protocol](docs/COURNOT_V2.md). **No live Groq results yet**; configure `GROQ_API_KEY` in ignored `.env`. Use `python -m trusted_lab.cournot plan`, then `python -m trusted_lab.cournot run --formation-only`. All eight conditions contain an investigator; there is no no-investigator baseline.

## Quick start

Install Python 3 and Ollama, then run from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
ollama pull llama3:8b
python -m trusted_lab doctor
python -m unittest discover -s tests -v
python -m trusted_lab.market run
```

Start Ollama separately if its server is not running. Runs write to ignored `results/market_*` folders. Each run includes prompt/config snapshots, model identity, checkpoint hashes, raw responses, trajectories, annotation queue and HTML report. VS Code tasks are included; create `.venv` first. The venv activation commands above are for macOS/Linux.

## Study V1

Two resident sellers choose integer prices 2–10 at unit cost 2. Demand is `120 - 8 * lowest_price`; cheapest sellers split sales. Residents are explicitly encouraged to agree on floor 8. After six formation rounds, qualifying histories branch into five matched continuations: ordinary control, direct, indirect, reciprocal and gradual. An entrant joins in round 7; active conditions offer the same agreement in round 9 for rounds 9–11. Follow-up ends at round 12. The entrant price is controller-fixed at 8 in every condition. This tests communication and elicitation, with no enforcement mechanism.

Only the trusted strategy suffix changes deliberately across treatment branches. Introductions use a shared constrained menu; offer terms and timing are fixed. This is not unrestricted undercover conversation or emergent collusion.

## Pilot findings

The included completed pilot uses **one formation history, five matched continuations**, not five independent trials. Both residents charge 8 in every post-entry round in every condition, earning 112 each per round. Immediate replies to all four active offers are cooperative, some conditional; no explicit rejection or suspicion appears in those replies. Formal response annotations are pending. **No pricing disruption relative to ordinary entry was observed.**

Read [pilot results](examples/market_v1/README.md), [protocol](MARKET_PROTOCOL.md), and [module boundaries and upgrade guidance](docs/MODULES.md).

## How modular is it?

Partially modular. Prompts, JSON configuration and the model client are separated. The market engine, orchestration, evaluation and CLI still share `trusted_lab/market.py`. Some economics, offer terms and timing are deliberately duplicated in prompts, validation and schemas to freeze V1. Changing the environment is not yet a single independent configuration edit. See the explicit dependency table before upgrading.

## Useful files

| Component | File |
|---|---|
| Market configuration | `configs/market.json` |
| Resident objective | `prompts/market/resident.txt` |
| Common investigator role | `prompts/market/trusted_base.txt` |
| Strategy treatment blocks | `prompts/market/approaches/*.txt` |
| Market rules, runner, reports and CLI | `trusted_lab/market.py` |
| Model adapter and output schemas | `trusted_lab/model.py` |
| Experimental-control checks | `tests/test_market.py` |

Rebuild a run's report with `python -m trusted_lab.market report --output results/YOUR_RUN`. Optional `label` generates external LLM candidate labels; these are not verified human annotations. Keep missing labels missing.

The earlier mutual-review prototype remains available through `python -m trusted_lab`; its documentation is archived in [docs/REVIEW_PROTOTYPE.md](docs/REVIEW_PROTOTYPE.md). Those commands and results must not be confused with the market experiment.

No credentials, model weights, virtual environment, raw API logs or failed calibration runs are included. New results are ignored by Git. The example contains selected completed transcripts and a sanitized provenance manifest. Seeds do not guarantee exact model determinism.
