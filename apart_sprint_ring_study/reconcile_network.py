"""Conservatively consume lost-request reservations and exclude their branches.

Run only after collection stopped. This never retries the uncertain request or
claims to know its actual charge. All other branches can then continue safely.
"""
import fcntl
import json
import time

from behavioral import ROOT, persist
from paid_client import DIR, STATE, LOG, save


if __name__ == '__main__':
    status = json.loads((ROOT / 'collection_status.json').read_text())
    if status['state'] == 'running':
        raise RuntimeError('Do not reconcile an active request')
    with (DIR / 'behavioral_spend.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state = json.loads(STATE.read_text())
        path = ROOT / 'network_exclusions.json'
        exclusions = json.loads(path.read_text()) if path.exists() else []
        for pending in state['pending']:
            episode = pending['key'].split(':')[1]
            entry = {'model': pending['model'], 'episode': episode,
                     'reason': 'Lost network response; full cost bound consumed; no retry of uncertain request',
                     'reserved_upper_bound_usd': pending['reserved'], 'call_key': pending['key'],
                     'time': time.time()}
            exclusions.append(entry)
            state['spent'] += pending['reserved']
            state.setdefault('conservative_network_charges', []).append(entry)
            with LOG.open('a') as handle:
                handle.write(json.dumps({'accounting_reconciliation': 'network timeout booked at full bound; branch excluded',
                                         **entry, 'total': state['spent']}) + '\n')
            print(json.dumps({k: entry[k] for k in ('model', 'episode', 'reserved_upper_bound_usd', 'reason')}))
        # Exclusions are persisted first: interrupted reconciliation can prevent
        # an uncertain retry, never silently allow it.
        persist(path, exclusions)
        state['pending'] = []
        save(state)
