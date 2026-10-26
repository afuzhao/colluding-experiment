"""Collect v11 episodes on one ledger: python3 run_v11.py SHARD CAP TAG MODEL SEEDS GAMES REGIMES [--skip-incomplete]
GAMES e.g. PQL or P; REGIMES comma list, e.g. silent,chat,O1,L1,A1,O5,L5,A5 (cure regimes need chat of the same seed first, so list chat first)."""
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
parser.add_argument('games')
parser.add_argument('regimes')
parser.add_argument('--skip-incomplete', action='store_true')
args = parser.parse_args()
ledger = Path.home() / '.config/apart' / ('ledger_v11_' + args.shard)
ledger.mkdir(exist_ok=True)
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'

import market11  # noqa: E402
from behavioral import ROOT, persist  # noqa: E402

paid_client.CAP = args.cap
V_SEEDS = [5101, 5202, 5303, 5404, 5505, 5606, 5707, 5808]

if __name__ == '__main__':
    seeds = V_SEEDS[:1] if args.seeds == 'pilot' else V_SEEDS[:6] if args.seeds == 'main' else V_SEEDS[:int(args.seeds)]
    status_path = ROOT / f'v11_status_{args.shard}.json'
    status = {'started_unix': time.time(), 'state': 'running', 'shard': args.shard, 'cap': args.cap, 'model': args.model, 'failures': []}
    persist(status_path, status)
    try:
        runner = market11.Runner11(args.model, args.tag)
        for seed in seeds:
            for game in args.games:
                for regime in args.regimes.split(','):
                    epath = runner.path(game, regime, seed)
                    if args.skip_incomplete and epath.exists() and not json.loads(epath.read_text()).get('complete'):
                        status['failures'].append({'game': game, 'regime': regime, 'seed': seed, 'reason': 'excluded: uncertain network request mid-episode'})
                        continue
                    base = runner.path(game, 'chat', seed)
                    if regime[0] in 'OLA' and regime.endswith('5') and not (base.exists() and json.loads(base.read_text()).get('complete')):
                        status['failures'].append({'game': game, 'regime': regime, 'seed': seed, 'reason': 'no completed chat episode to branch from'})
                        continue
                    try:
                        runner.run(game, regime, seed)
                    except RuntimeError as error:
                        if not str(error).startswith('Three technical/schema failures'):
                            raise
                        status['failures'].append({'game': game, 'regime': regime, 'seed': seed, 'reason': str(error)})
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
