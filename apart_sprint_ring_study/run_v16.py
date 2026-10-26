"""Collect v16 episodes: python3 run_v16.py SHARD CAP TAG MODEL SEEDS GAMES ARMS   (SEEDS e.g. 5101,5202,5303)"""
import json
import sys
import time
import traceback
from pathlib import Path

import paid_client

shard, cap, tag, model, seeds, games, arms = sys.argv[1:8]
ledger = Path.home() / '.config/apart' / ('ledger_v16_' + shard)
ledger.mkdir(exist_ok=True)
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'

import market16  # noqa: E402
from behavioral import ROOT, persist  # noqa: E402

paid_client.CAP = float(cap)

if __name__ == '__main__':
    status_path = ROOT / f'v16_status_{shard}.json'
    status = {'started_unix': time.time(), 'state': 'running', 'shard': shard, 'model': model, 'done': 0, 'failures': []}
    persist(status_path, status)
    excl = Path(__file__).parent / 'network_exclusions_extra.json'
    lost = {e['episode'] for e in (json.loads(excl.read_text()) if excl.exists() else []) if e['ledger'] == 'ledger_v16_' + shard}
    try:
        runner = market16.Runner16(model, tag)
        for seed in map(int, seeds.split(',')):
            for game in games:
                for arm in arms.split(','):
                    epath = runner.root / 'episodes' / f'{game}_{arm}_{seed}.json'
                    if f'{game}_{arm}16_{seed}' in lost and epath.exists() and not json.loads(epath.read_text()).get('complete'):
                        status['failures'].append({'game': game, 'arm': arm, 'seed': seed, 'reason': 'excluded: uncertain network request mid-episode'})
                        continue
                    try:
                        runner.run16(game, arm, seed)
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
