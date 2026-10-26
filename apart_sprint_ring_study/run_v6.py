"""Collect one model's v6 maverick-entrant arms on its own ledger: python3 run_v6.py MODEL CAP [--arms a,b] [--limit N]."""
import argparse
import json
import time
import traceback
from pathlib import Path

import paid_client

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('model')
parser.add_argument('cap', type=float)
parser.add_argument('--arms', default='')
parser.add_argument('--limit', type=int, default=8)
args = parser.parse_args()
slug = args.model.replace('/', '__')
ledger = Path.home() / '.config/apart' / ('ledger_v6_' + slug)
ledger.mkdir(exist_ok=True)
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'

import market6  # noqa: E402

if args.model.startswith('anthropic/'):
    import copy
    from client_v8 import ClientV8
    paid_client.Client = ClientV8
    _compat_schema = copy.deepcopy(market6.MESSAGE_SCHEMA)
    _compat_schema['properties']['floor'] = {'type': ['integer', 'null']}
    market6.MESSAGE_SCHEMA = _compat_schema
from behavioral import ROOT, SEEDS, persist  # noqa: E402

paid_client.CAP = args.cap
EXCLUDED = {(e['model'], e['episode']) for e in (json.loads(Path('network_exclusions_extra.json').read_text()) if Path('network_exclusions_extra.json').exists() else [])}
SOURCE = 'openai__gpt-4.1-mini'


def checkpoint(seed):
    path = ROOT / 'behavioral_v3' / SOURCE / 'episodes' / f'formation_induced_{seed}.json'
    saved = json.loads(path.read_text())
    return saved['state'] if saved.get('complete') else None


if __name__ == '__main__':
    arms = args.arms.split(',') if args.arms else ['mav_none', 'mav5', 'mav3', 'mav7']
    status_path = ROOT / f'v6_status_{slug}.json'
    status = {'started_unix': time.time(), 'state': 'running', 'model': args.model, 'cap': args.cap, 'failures': []}
    persist(status_path, status)
    try:
        runner = market6.Runner6(args.model)
        for arm in arms:
            for seed in SEEDS[:args.limit]:
                name = f'{arm}_{seed}'
                if (args.model, name) in EXCLUDED:
                    status['failures'].append({'episode': name, 'reason': 'excluded uncertain network request'})
                    continue
                try:
                    runner.maverick(name, seed, checkpoint(seed), arm)
                except RuntimeError as error:
                    if not str(error).startswith('Three technical/schema failures'):
                        raise
                    status['failures'].append({'episode': name, 'reason': str(error)})
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
