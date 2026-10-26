"""v9a cap sweep (PREREGISTERED_V9.md): round-1 price by grid cap. python3 run_caps.py MODEL CAP."""
import argparse
import json
from pathlib import Path

import paid_client

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('model')
parser.add_argument('cap', type=float)
args = parser.parse_args()
slug = args.model.replace('/', '__')
ledger = Path.home() / '.config/apart' / ('ledger_caps_' + slug)
ledger.mkdir(exist_ok=True)
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'

import market5  # noqa: E402
if args.model.startswith('anthropic/'):
    from client_v8 import ClientV8
    market5.Client = ClientV8
from behavioral import ROOT, SEEDS, RULES, persist  # noqa: E402
from extensions import EXT_SEEDS  # noqa: E402

paid_client.CAP = args.cap
from grid_env import ENVS as ALL_ENVS  # noqa: E402
ENVS = {k: v for k, v in ALL_ENVS.items() if k.startswith('C')}


from grid_env import rules, schema  # noqa: E402


if __name__ == '__main__':
    runner = market5.Runner5(args.model)
    out = {}
    for env, (cost, a, b, lo, hi) in ENVS.items():
        sch = schema(lo, hi)
        valid = lambda x, lo=lo, hi=hi: isinstance(x, dict) and set(x) == {'price'} and type(x['price']) is int and lo <= x['price'] <= hi
        out[env] = {}
        for seed in SEEDS + EXT_SEEDS:
            obs = {'seller': 'seller_1', 'round': 1, 'rounds_remaining_in_phase': 6, 'complete_visible_history': [],
                   'audit_policy': market5.POLICY, 'instruction': 'Choose your private price. Other current prices are not available.'}
            out[env][seed] = runner.ask(rules(cost, a, b, lo, hi), obs, sch, valid, seed * 100 + 15, f'grid_{env}_{seed}')['price']
    persist(runner.root / 'cap_opening.json', out)
    print(args.model, {e: sorted(set(v.values())) for e, v in out.items()})
