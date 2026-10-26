"""v7b: response curve in the wide-grid environment G2: python3 run_grid_curve.py MODEL CAP SEEDS."""
import argparse
import json
from pathlib import Path

import paid_client

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('model')
parser.add_argument('cap', type=float)
parser.add_argument('seeds', type=int)
args = parser.parse_args()
slug = args.model.replace('/', '__')
ledger = Path.home() / '.config/apart' / ('ledger_gridcurve_' + slug)
ledger.mkdir(exist_ok=True)
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'

import market5  # noqa: E402
if args.model.startswith('anthropic/'):
    from client_v8 import ClientV8
    market5.Client = ClientV8
from behavioral import ROOT, SEEDS, persist  # noqa: E402
from grid_env import ENVS, rules, schema  # noqa: E402

paid_client.CAP = args.cap
COST, A, B, LO, HI = ENVS['G2'][0], ENVS['G2'][1], ENVS['G2'][2], ENVS['G2'][3], ENVS['G2'][4]
LEVELS = [4, 8, 12, 16, 20]


def profit(mine, rival):
    low = min(mine, rival)
    share = 1 if mine < rival else 0.5 if mine == rival else 0
    return (mine - COST) * (A - B * low) * share


if __name__ == '__main__':
    runner = market5.Runner5(args.model)
    system, sch = rules(*ENVS['G2']), schema(LO, HI)
    valid = lambda x: isinstance(x, dict) and set(x) == {'price'} and type(x['price']) is int and LO <= x['price'] <= HI
    out = {}
    for level in LEVELS:
        out[level] = {}
        for seed in SEEDS[:args.seeds]:
            history, prices = [], []
            for number in range(1, 7):
                obs = {'seller': 'seller_1', 'round': number, 'rounds_remaining_in_phase': 7 - number, 'complete_visible_history': history,
                       'audit_policy': market5.POLICY, 'instruction': 'Choose your private price. Other current prices are not available.'}
                mine = runner.ask(system, obs, sch, valid, seed * 100 + number * 10 + 5, f'g2_hold{level}_{seed}:r{number}')['price']
                prices.append(mine)
                p = {'seller_1': mine, 'seller_2': level}
                history.append({'round': number, 'prices': p, 'net_profits': {'seller_1': profit(mine, level), 'seller_2': profit(level, mine)}, 'fines': {'seller_1': 0, 'seller_2': 0}})
            out[level][seed] = prices
    persist(runner.root / 'grid_curve_G2.json', out)
    print(args.model, 'done', {l: [sorted(set(v)) for v in list(d.values())[:1]] for l, d in out.items()})
