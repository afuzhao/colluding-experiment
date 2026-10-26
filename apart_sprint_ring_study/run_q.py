"""Collect v10 episodes on one ledger: python3 run_q.py SHARD CAP TAG MODEL SEEDS REGIME [REGIME ...]
REGIME is a market10 regime or script name. SEEDS is 'main' (eight seeds), 'pilot' (one seed) or an integer count."""
import argparse
import json
import time
import traceback
from pathlib import Path

import paid_client

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('shard')
parser.add_argument('cap', type=float)
parser.add_argument('tag')
parser.add_argument('model')
parser.add_argument('seeds')
parser.add_argument('regimes', nargs='+')
args = parser.parse_args()
ledger = Path.home() / '.config/apart' / ('ledger_q_' + args.shard)
ledger.mkdir(exist_ok=True)
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'

import market10  # noqa: E402
from behavioral import ROOT, persist  # noqa: E402

paid_client.CAP = args.cap
Q_SEEDS = [4101, 4202, 4303, 4404, 4505, 4606, 4707, 4808]

if __name__ == '__main__':
    seeds = Q_SEEDS[:1] if args.seeds == 'pilot' else Q_SEEDS[1:2] if args.seeds == 'pilot2' else Q_SEEDS if args.seeds == 'main' else Q_SEEDS[:int(args.seeds)]
    status_path = ROOT / f'v10_status_{args.shard}.json'
    status = {'started_unix': time.time(), 'state': 'running', 'shard': args.shard, 'cap': args.cap, 'model': args.model, 'failures': []}
    persist(status_path, status)
    try:
        runner = market10.Runner10(args.model, args.tag)
        for regime in args.regimes:
            for seed in seeds:
                try:
                    (runner.scripted if regime in market10.SCRIPTS else runner.run)(regime, seed)
                except RuntimeError as error:
                    if not str(error).startswith('Three technical/schema failures'):
                        raise
                    status['failures'].append({'regime': regime, 'seed': seed, 'reason': str(error)})
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
