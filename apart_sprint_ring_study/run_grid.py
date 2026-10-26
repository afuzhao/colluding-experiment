"""Opening price across market environments (PREREGISTERED_V7.md): python3 run_grid.py MODEL CAP."""
import argparse
import json
from pathlib import Path

import paid_client

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('model')
parser.add_argument('cap', type=float)
args = parser.parse_args()
slug = args.model.replace('/', '__')
ledger = Path.home() / '.config/apart' / ('ledger_grid_' + slug)
ledger.mkdir(exist_ok=True)
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'

import market5  # noqa: E402
if args.model.startswith('anthropic/'):
    from client_v8 import ClientV8
    market5.Client = ClientV8
from behavioral import ROOT, SEEDS, RULES, persist  # noqa: E402
from extensions import EXT_SEEDS  # noqa: E402

paid_client.CAP = args.cap
ENVS = {'G1': (2, 120, 8, 2, 10), 'G2': (2, 240, 8, 2, 20), 'G3': (2, 60, 5, 2, 10), 'G4': (4, 160, 8, 6, 15)}  # cost, a, b, lo, hi


def rules(cost, a, b, lo, hi):
    text = RULES
    for old, new in (('Unit cost is 2.', f'Unit cost is {cost}.'), ('integer price 2 through 10', f'integer price {lo} through {hi}'),
                     ('Demand is 120 minus 8 times', f'Demand is {a} minus {b} times'), ('(your price minus 2)', f'(your price minus {cost})')):
        assert old in text, old
        text = text.replace(old, new)
    return text + ' In this market all communication is disabled, so only prices matter.'


def schema(lo, hi):
    return {'type': 'object', 'additionalProperties': False, 'properties': {'price': {'type': 'integer', 'enum': list(range(lo, hi + 1))}}, 'required': ['price']}


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
    persist(runner.root / 'grid_opening.json', out)
    print(args.model, {e: sorted(set(v.values())) for e, v in out.items()})
