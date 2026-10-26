"""Collect v12 trials on one ledger: python3 run_peer.py SHARD CAP TAG MODEL SCOPE   (SCOPE: calibration or main)"""
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
parser.add_argument('scope')
args = parser.parse_args()
ledger = Path.home() / '.config/apart' / ('ledger_v12_' + args.shard)
ledger.mkdir(exist_ok=True)
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'

import peer12  # noqa: E402
from behavioral import ROOT, persist  # noqa: E402

paid_client.CAP = args.cap

if __name__ == '__main__':
    status_path = ROOT / f'v12_status_{args.shard}.json'
    status = {'started_unix': time.time(), 'state': 'running', 'shard': args.shard, 'cap': args.cap, 'model': args.model, 'done': 0, 'failures': []}
    persist(status_path, status)
    try:
        runner = peer12.Runner12(args.model, args.tag)
        orders = 1 if args.scope == 'check' else peer12.ORDERS
        work = [(sc, c, p, a, l, v, o) for (sc, c, p, a, l) in peer12.cells(args.scope) for v in range(peer12.VARIANTS) for o in range(orders)]
        # interleave so a spend cap leaves balanced data: variant/order outermost
        work.sort(key=lambda w: (w[5], w[6]))
        for sc, c, p, a, l, v, o in work:
            try:
                runner.trial(sc, c, p, a, l, v, o)
                status['done'] += 1
            except RuntimeError as error:
                if not str(error).startswith('Three technical/schema failures'):
                    raise
                status['failures'].append({'trial': [sc, c, p, a, l, v, o], 'reason': str(error)})
            if status['done'] % 10 == 0:
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
