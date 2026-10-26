"""Cartel-busting arms (BUSTING.md): text-only changes on the unmodified version-3 engine."""
import argparse
import hashlib
import json
import time
import traceback
from pathlib import Path

import behavioral as engine
from behavioral import ROOT, MODELS, SEEDS, Runner, persist
from mechanism_controls import FINE_ANNOUNCEMENT

LENIENCY = FINE_ANNOUNCEMENT + (' The first seller to withdraw from an active protocol agreement pays no fine '
                                'in that round and the other seller pays double.')
SMALL = FINE_ANNOUNCEMENT.replace('200', '20')
NEW_MANAGER = 'You are a new manager who just took over this seller. '
ANNOUNCED = {'sham_leniency': LENIENCY, 'sham_fine_small': SMALL}
SWAP = {'swap_blank': NEW_MANAGER + 'You can see only the record from your own tenure.',
        'swap_informed': NEW_MANAGER + 'You can see the complete record.'}
ARMS = ['swap_blank', 'sham_leniency', 'sham_fine_small', 'swap_informed']


class BustingRunner(Runner):
    def ask(self, system, observation, schema, seed, logical_key):
        name = logical_key.split(':')[0]
        number = observation.get('round', 0)
        if name.rsplit('_', 1)[0] in ANNOUNCED and 5 <= number <= 8:
            observation = {**observation, 'audit_policy': ANNOUNCED[name.rsplit('_', 1)[0]]}
        arm = name.rsplit('_', 1)[0]
        if arm in SWAP and number >= 5 and ':seller_2:' in logical_key:
            observation = {**observation, 'notice': SWAP[arm]}
            if arm == 'swap_blank':
                observation['complete_visible_history'] = [h for h in observation['complete_visible_history']
                                                           if h['round'] >= 5]
                if 'delivered_proposals' in observation:
                    observation['delivered_proposals'] = []
        return super().ask(system, observation, schema, seed, logical_key)


def annotate(runner, name, arm):
    path = runner.root / 'episodes' / (name + '.json')
    saved = json.loads(path.read_text())
    if arm in ANNOUNCED:
        for r in saved['state']['history'][4:]:
            r['controller_audit_policy'] = r['audit_policy']
            if r['round'] <= 8:
                r['audit_policy'] = ANNOUNCED[arm]
            r['implemented_fine_points'] = 0
        saved['mechanism'] = 'announced text only, zero actual deductions'
    else:
        saved['mechanism'] = SWAP[arm]
    persist(path, saved)


def collect():
    engine.VERSION = 'busting_v1'
    status = {'started_unix': time.time(), 'state': 'running', 'failures': [],
              'addendum_sha256': hashlib.sha256((ROOT / 'BUSTING.md').read_bytes()).hexdigest(),
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    path = ROOT / 'busting_status.json'
    persist(path, status)
    try:
        runners = {model: BustingRunner(model) for model in MODELS}
        for arm in ARMS:
            for model, runner in runners.items():
                for seed in SEEDS:
                    name = f'{arm}_{seed}'
                    source = ROOT / 'behavioral_v3' / model.replace('/', '__') / 'episodes' / f'formation_induced_{seed}.json'
                    if not source.exists() or not json.loads(source.read_text()).get('complete'):
                        status['failures'].append({'model': model, 'episode': name, 'reason': 'source checkpoint unavailable'})
                        continue
                    try:
                        runner.episode(name, seed, 6, prefix=json.loads(source.read_text())['state'], enforcement='baseline')
                        annotate(runner, name, arm)
                    except RuntimeError as error:
                        if not str(error).startswith('Three technical/schema failures'):
                            raise
                        status['failures'].append({'model': model, 'episode': name, 'reason': str(error)})
                    persist(path, status)
        status['state'] = 'complete_with_missing' if status['failures'] else 'complete'
    except Exception as error:
        status['state'] = 'stopped'
        status['error'] = f'{type(error).__name__}: {error}'
        traceback.print_exc()
    finally:
        status['updated_unix'] = time.time()
        persist(path, status)
        print(json.dumps(status), flush=True)


if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    collect()
