"""Collect pair markets for one shard on its own ledger: python3 run_pairs.py SHARD CAP REGIME ENV SEEDS PAIR [PAIR ...]
PAIR is MODEL_A,MODEL_B. SEEDS is 'ext' (eight extension seeds), 'cal' (seed 9001 only, calibration) or an integer count of ext seeds."""
import argparse
import json
import time
import traceback
from pathlib import Path

import paid_client

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('shard')
parser.add_argument('cap', type=float)
parser.add_argument('regime')
parser.add_argument('env')
parser.add_argument('seeds')
parser.add_argument('--skip-incomplete', action='store_true', help='after a reconciled network loss: skip episodes that were mid-run')
parser.add_argument('pairs', nargs='+')
args = parser.parse_args()
ledger = Path.home() / '.config/apart' / ('ledger_pairs_' + args.shard)
ledger.mkdir(exist_ok=True)
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'

import market8  # noqa: E402
from behavioral import ROOT, persist  # noqa: E402
from extensions import EXT_SEEDS  # noqa: E402

paid_client.CAP = args.cap
EVEN_SEEDS = [3102, 3204, 3306, 3408, 3510, 3612, 3714, 3816]  # disjoint from anchor-measurement seeds; even, so seats are the listed order
EXCLUDED = {(e['model'], e['episode']) for e in (json.loads(Path('network_exclusions_extra.json').read_text()) if Path('network_exclusions_extra.json').exists() else [])}

if __name__ == '__main__':
    seeds = [9003] if args.seeds == 'cal' else EXT_SEEDS if args.seeds == 'ext' else EVEN_SEEDS if args.seeds == 'even' else EXT_SEEDS[:int(args.seeds)]
    status_path = ROOT / f'v8_status_{args.shard}.json'
    status = {'started_unix': time.time(), 'state': 'running', 'shard': args.shard, 'cap': args.cap, 'regime': args.regime, 'env': args.env, 'failures': []}
    persist(status_path, status)
    try:
        for pair in args.pairs:
            a, b = pair.split(',')
            duo = market8.Duopoly(a, b)
            for seed in seeds:
                name = f'{seed}'
                epath = duo.root / 'episodes' / f'{args.regime}_{args.env}_{name}.json'
                if args.skip_incomplete and epath.exists() and not json.loads(epath.read_text()).get('complete'):
                    status['failures'].append({'pair': pair, 'seed': seed, 'reason': 'excluded: uncertain network request mid-episode'})
                    continue
                try:
                    duo.run(name, seed, args.regime, args.env)
                except RuntimeError as error:
                    if not str(error).startswith('Three technical/schema failures'):
                        raise
                    status['failures'].append({'pair': pair, 'seed': seed, 'reason': str(error)})
                persist(status_path, status)
        status['state'] = 'complete_with_missing' if status['failures'] else 'complete'
    except Exception as error:
        status['state'] = 'stopped'
        status['error'] = f'{type(error).__name__}: {error}'
        traceback.print_exc()
    finally:
        status['updated_unix'] = time.time()
        persist(status_path, status)
        print(json.dumps(status), flush=True)
