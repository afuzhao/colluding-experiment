"""Consume lost-request reservations on one ledger and exclude their branches: python3 reconcile_ledger.py LEDGER_DIR_NAME.
Run only after the collector on that ledger has stopped. Never retries the uncertain request."""
import fcntl
import json
import sys
import time
from pathlib import Path

import paid_client

ledger = Path.home() / '.config/apart' / sys.argv[1]
paid_client.DIR, paid_client.STATE, paid_client.LOG = ledger, ledger / 'behavioral_spend.json', ledger / 'behavioral_calls.jsonl'
EXCLUSIONS = Path(__file__).parent / 'network_exclusions_extra.json'

if __name__ == '__main__':
    with (ledger / 'behavioral_spend.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state = json.loads(paid_client.STATE.read_text())
        exclusions = json.loads(EXCLUSIONS.read_text()) if EXCLUSIONS.exists() else []
        for pending in state['pending']:
            entry = {'ledger': sys.argv[1], 'model': pending['model'], 'episode': pending['key'].split(':')[1],
                     'reserved_upper_bound_usd': pending['reserved'], 'time': time.time(),
                     'reason': 'Lost network response; full cost bound consumed; no retry of uncertain request'}
            exclusions.append(entry)
            state['spent'] += pending['reserved']
            state.setdefault('conservative_network_charges', []).append(entry)
            print(json.dumps(entry))
        EXCLUSIONS.write_text(json.dumps(exclusions, indent=1) + '\n')   # persisted before the pending list is cleared
        state['pending'] = []
        paid_client.save(state)
