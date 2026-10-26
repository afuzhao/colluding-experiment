"""Collect v14 episodes: python3 run_ring14.py SHARD CAP TAG MODEL VARIANTS"""
import argparse
import json
import time
import traceback
from pathlib import Path

import paid_client

parser = argparse.ArgumentParser()
for a in ('shard', 'cap', 'tag', 'model', 'variants'):
    parser.add_argument(a)
args = parser.parse_args()
ledger = Path.home() / '.config/apart' / ('ledger_v14_' + args.shard)
ledger.mkdir(exist_ok=True)
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'

import ring14  # noqa: E402
from behavioral import ROOT, persist  # noqa: E402

paid_client.CAP = float(args.cap)

if __name__ == '__main__':
    status_path = ROOT / f'v14_status_{args.shard}.json'
    status = {'started_unix': time.time(), 'state': 'running', 'shard': args.shard, 'model': args.model, 'done': 0, 'failures': []}
    persist(status_path, status)
    try:
        runner = ring14.Runner14(args.model, args.tag)
        for v in range(int(args.variants)):
            for cond in ring14.CONDITIONS:
                try:
                    runner.episode(cond, v)
                    status['done'] += 1
                except RuntimeError as error:
                    if not str(error).startswith('Three technical/schema failures'):
                        raise
                    status['failures'].append({'condition': cond, 'variant': v, 'reason': str(error)})
        status['state'] = 'complete_with_missing' if status['failures'] else 'complete'
    except Exception as error:
        status['state'] = 'stopped'
        status['error'] = f'{type(error).__name__}: {error}'
        traceback.print_exc()
    finally:
        status['updated_unix'] = time.time()
        persist(status_path, status)
        print(json.dumps(status), flush=True)
