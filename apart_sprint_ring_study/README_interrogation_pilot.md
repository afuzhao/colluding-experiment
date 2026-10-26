# Apart sprint: interrogation evidence

Recovered work from the Oct 24, 2026 session, plus a local follow-up on the same frozen markets.

## Files

- `pilot/`: original smoke-test source, 16 market histories, 160 interviews, log, and SHA-256 provenance. Archived without changing their contents.
- `PILOT_AUDIT.md`: recomputed market outcomes and answer counts.
- `clean_prompt/`: 64 new interviews, raw Ollama responses, exact prompt/configuration, and results.
- `auditor_test/`: 48 matched audits with no testimony, synthetic confession, or synthetic denial; exact citation checks.
- `auditor_recheck/`: 12 fresh-seed audits on the two initially anomalous markets.
- `HANDOFF.md`: findings, interpretation limits, and the next experiment.
- `sprint.py`: archival, validation, and resumable local interview runner.

```sh
python3 sprint.py audit
python3 -m unittest test_sprint.py
caffeinate -i python3 sprint.py followup
caffeinate -i python3 auditor.py
caffeinate -i python3 auditor.py --recheck
```

The follow-up command skips completed interviews. It refuses to reuse an output directory with different prompt/configuration settings. It uses local `llama3:8b`, with zero paid API requests.

The archived `pilot/orclient.py` is historical code, not the paid runner. Its guard checks spend before a request without reserving the upcoming cost, and treats missing cost as zero. It does **not** enforce the promised hard cap reliably. Fix and test reservation/accounting before using any paid runner.

The OpenRouter credential is outside this project at `~/.config/apart/openrouter.env`. Never copy it into project artifacts or print its value. The user authorized at most $5–6 total; use $5 as the experiment ceiling and reconcile any previous spend before paid runs.

Prior-session novelty claims and citations remain leads, not independently verified literature conclusions.
