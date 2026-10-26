"""Collect v15 episodes: python3 run_v15.py SHARD CAP TAG MODEL SEEDS GAMES ARMS   (SEEDS e.g. 5101,5202,5303)"""
import json
import sys
import time
import traceback
from pathlib import Path

import paid_client

shard, cap, tag, model, seeds, games, arms = sys.argv[1:8]
ledger = Path.home() / '.config/apart' / ('ledger_v15_' + shard)
ledger.mkdir(exist_ok=True)
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'

import market15  # noqa: E402
from behavioral import ROOT, persist  # noqa: E402

paid_client.CAP = float(cap)

if __name__ == '__main__':
    status_path = ROOT / f'v15_status_{shard}.json'
    status = {'started_unix': time.time(), 'state': 'running', 'shard': shard, 'model': model, 'done': 0, 'failures': []}
    persist(status_path, status)
    try:
        runner = market15.Runner15(model, tag)
        for seed in map(int, seeds.split(',')):
            for game in games:
                for arm in arms.split(','):
                    try:
                        runner.run15(game, arm, seed)
                        status['done'] += 1
                    except RuntimeError as error:
                        status['failures'].append({'game': game, 'arm': arm, 'seed': seed, 'reason': str(error)})
        status['state'] = 'complete_with_missing' if status['failures'] else 'complete'
    except Exception as error:
        status['state'] = 'stopped'
        status['error'] = f'{type(error).__name__}: {error}'
        traceback.print_exc()
    finally:
        status['updated_unix'] = time.time()
        persist(status_path, status)
        print(json.dumps(status), flush=True)
