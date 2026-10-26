"""Monitor collection without computing effects or making model calls."""
import argparse
import json
import time

from behavioral import ROOT, MODELS, VERSION
from paid_client import STATE


def show():
    status = json.loads((ROOT / 'collection_status.json').read_text())
    counts = {}
    for model in MODELS:
        directory = ROOT / ('behavioral_' + VERSION) / model.replace('/', '__') / 'episodes'
        episodes = [json.loads(path.read_text()) for path in directory.glob('*.json')] if directory.exists() else []
        counts[model] = sum(bool(episode.get('complete')) for episode in episodes)
    ledger = json.loads(STATE.read_text())
    print(json.dumps({'state': status['state'], 'completed_episodes_out_of_128_each': counts,
        'budget_counted_usd': round(ledger['spent'], 4), 'pending': len(ledger['pending'])}), flush=True)
    return status['state']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wait', type=int, default=0)
    args = parser.parse_args()
    end = time.monotonic() + args.wait
    while True:
        state = show()
        if state != 'running' or time.monotonic() >= end:
            break
        time.sleep(min(60, max(0, end - time.monotonic())))
