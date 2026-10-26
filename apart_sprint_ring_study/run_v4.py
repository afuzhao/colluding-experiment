"""Collect one model's version-4 arms on its own spend ledger: python3 run_v4.py MODEL CAP [ARMS] [--ext]."""
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
parser.add_argument('--ext', action='store_true', help='use the extension seeds instead of the main seeds')
args = parser.parse_args()
slug = args.model.replace('/', '__')
ledger = Path.home() / '.config/apart' / ('ledger_' + slug)
ledger.mkdir(exist_ok=True)
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'

import market4  # noqa: E402  (must follow the ledger patch)

if args.model.startswith('anthropic/'):
    # Anthropic strict structured output: no enum mixing null and integers (validators still enforce the range); route via ClientV8.
    import copy
    from client_v8 import ClientV8
    paid_client.Client = ClientV8
    market4.Client = ClientV8
    _orig = market4.message_schema

    def _compat(report, _orig=_orig):
        schema = copy.deepcopy(_orig(report))
        schema['properties']['floor'] = {'type': ['integer', 'null']}
        return schema
    market4.message_schema = _compat
from behavioral import ROOT, SEEDS, persist  # noqa: E402
from extensions import EXT_SEEDS  # noqa: E402

paid_client.CAP = args.cap
EXCLUDED = {(e['model'], e['episode']) for e in (json.loads(Path('network_exclusions_extra.json').read_text()) if Path('network_exclusions_extra.json').exists() else [])}
SOURCE = 'openai__gpt-4.1-mini'


def checkpoint(seed):
    version = 'behavioral_ext_v1' if seed in EXT_SEEDS else 'behavioral_v3'
    path = ROOT / version / SOURCE / 'episodes' / f'formation_induced_{seed}.json'
    if path.exists():
        saved = json.loads(path.read_text())
        if saved.get('complete'):
            return saved['state']


if __name__ == '__main__':
    arms = args.arms.split(',') if args.arms else market4.ARMS
    status_path = ROOT / f'v4_status_{slug}{"_ext" if args.ext else ""}.json'
    status = {'started_unix': time.time(), 'state': 'running', 'model': args.model, 'cap': args.cap, 'failures': []}
    persist(status_path, status)
    try:
        runner = market4.Runner4(args.model)
        for arm in arms:
            for seed in (EXT_SEEDS if args.ext else SEEDS):
                prefix = checkpoint(seed)
                name = f'{arm}_{seed}'
                if (args.model, name) in EXCLUDED:
                    status['failures'].append({'episode': name, 'reason': 'excluded uncertain network request'})
                    continue
                if prefix is None:
                    status['failures'].append({'episode': name, 'reason': 'checkpoint unavailable'})
                    continue
                try:
                    runner.episode(name, seed, prefix, arm)
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
