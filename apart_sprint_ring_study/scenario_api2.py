"""v18 part 3: same scenarios, but the model writes a short reason before the choice. python3 scenario_api2.py SHARD CAP MODEL"""
import json
import sys
from pathlib import Path

import paid_client

shard, cap, model = sys.argv[1:4]
ledger = Path.home() / '.config/apart' / ('ledger_v18r_' + shard)
ledger.mkdir(exist_ok=True)
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'

import market16  # noqa: E402
from behavioral import ROOT, persist  # noqa: E402
from client_v8r import ClientV8R  # noqa: E402

paid_client.CAP = float(cap)
ARMS = ['placebo', 'fmsg', 'tagged']

if __name__ == '__main__':
    runner = market16.Runner16(model, 'v18r')
    runner.client = ClientV8R(model)
    D = ROOT / 'v18_io'
    res, fail = [], []
    for arm in ARMS:
        for it in json.load(open(D / f'scenarios_{arm}.json')):
            grid = it['allowed_choices']
            schema = {'type': 'object', 'additionalProperties': False, 'properties': {'reason': {'type': 'string', 'description': 'Two short sentences: what you expect the other firm to do this round, and why your choice is best.'}, 'choice': {'type': 'number', 'enum': grid}}, 'required': ['reason', 'choice']}
            valid = lambda a, grid=grid: isinstance(a, dict) and set(a) == {'reason', 'choice'} and any(abs(a['choice'] - x) < 1e-9 for x in grid)
            try:
                a = runner.ask(it['system'], it['observation'], schema, valid, 5105, f'v18r_{arm}_{it["id"]}')
                res.append({'arm': arm, 'id': it['id'], 'choice': a['choice'], 'reason': a['reason']})
            except Exception as error:
                fail.append({'arm': arm, 'id': it['id'], 'reason': str(error)[:100]})
    persist(ROOT / 'behavioral_analysis' / f'v18_reason_{shard}.json', {'model': model, 'results': res, 'failures': fail})
    print(json.dumps({'model': model, 'n': len(res), 'fail': len(fail)}), flush=True)
