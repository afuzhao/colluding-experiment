"""Run frozen version-3 studies for another model on its own ledger: python3 run_v3_study.py MODEL CAP LEDGER STUDY[,STUDY]
STUDY is mediator (Study 2) or probe (Study 1, neutral population: ordinary and offer arms only)."""
import argparse
import json
import time
import traceback
from pathlib import Path

import paid_client

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('model')
parser.add_argument('cap', type=float)
parser.add_argument('ledger')
parser.add_argument('studies')
args = parser.parse_args()
ledger = Path.home() / '.config/apart' / ('ledger_' + args.ledger)
ledger.mkdir(exist_ok=True)
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'
paid_client.SNAPSHOT = Path(__file__).parent / 'provider_snapshot_v4.json'
paid_client.CAP = args.cap

from behavioral import ROOT, SEEDS, Runner, persist  # noqa: E402

if __name__ == '__main__':
    status_path = ROOT / f'v3extra_status_{args.model.replace("/", "__")}.json'
    status = {'started_unix': time.time(), 'state': 'running', 'model': args.model, 'cap': args.cap,
              'studies': args.studies, 'failures': []}
    persist(status_path, status)

    def attempt(name, seed, rounds, **kwargs):
        try:
            return runner.episode(name, seed, rounds, **kwargs)
        except RuntimeError as error:
            if not str(error).startswith('Three technical/schema failures'):
                raise
            status['failures'].append({'episode': name, 'reason': str(error)})
        finally:
            persist(status_path, status)

    try:
        runner = Runner(args.model)
        for seed in SEEDS:
            if 'mediator' in args.studies:
                arms = ['private', 'shared', 'restricted']
                rotate = seed % len(arms)
                for arm in arms[rotate:] + arms[:rotate]:
                    attempt(f'mediator_{arm}_{seed}', seed, 6, mediator=arm)
            if 'probe' in args.studies:
                prefix = attempt(f'formation_neutral_{seed}', seed, 4, private_formation=True)
                for arm in (['ordinary', 'offer'] if seed % 2 else ['offer', 'ordinary']):
                    if prefix is not None:
                        attempt(f'probe_neutral_{arm}_{seed}', seed, 4, prefix=prefix, probe=arm)
        status['state'] = 'complete_with_missing' if status['failures'] else 'complete'
    except Exception as error:
        status['state'] = 'stopped'
        status['error'] = f'{type(error).__name__}: {error}'
        traceback.print_exc()
    finally:
        status['updated_unix'] = time.time()
        persist(status_path, status)
        print(json.dumps(status), flush=True)
