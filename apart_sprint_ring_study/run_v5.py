"""Collect one model's v5 scripted-rival markets on its own ledger: python3 run_v5.py MODEL CAP [--seeds main|all]."""
import argparse
import json
import time
import traceback
from pathlib import Path

import paid_client

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('model')
parser.add_argument('cap', type=float)
parser.add_argument('--seeds', default='all')
args = parser.parse_args()
slug = args.model.replace('/', '__')
ledger = Path.home() / '.config/apart' / ('ledger_v5_' + slug)
ledger.mkdir(exist_ok=True)
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'

import market5  # noqa: E402
if args.model.startswith('anthropic/'):
    from client_v8 import ClientV8
    market5.Client = ClientV8
from behavioral import ROOT, SEEDS, persist  # noqa: E402
from extensions import EXT_SEEDS  # noqa: E402

paid_client.CAP = args.cap
EXCLUDED = {(e['model'], e['episode']) for e in (json.loads(Path('network_exclusions_extra.json').read_text()) if Path('network_exclusions_extra.json').exists() else [])}

if __name__ == '__main__':
    seeds = SEEDS if args.seeds == 'main' else SEEDS + EXT_SEEDS
    status_path = ROOT / f'v5_status_{slug}.json'
    status = {'started_unix': time.time(), 'state': 'running', 'model': args.model, 'cap': args.cap, 'failures': []}
    persist(status_path, status)
    try:
        runner = market5.Runner5(args.model)
        for seed in seeds:
            for script in market5.SCRIPTS:
                if (args.model, f'{script}_{seed}') in EXCLUDED:
                    status['failures'].append({'episode': f'{script}_{seed}', 'reason': 'excluded uncertain network request'})
                    continue
                try:
                    runner.scripted(f'{script}_{seed}', seed, script)
                except RuntimeError as error:
                    if not str(error).startswith('Three technical/schema failures'):
                        raise
                    status['failures'].append({'episode': f'{script}_{seed}', 'reason': str(error)})
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
