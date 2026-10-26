"""Sequential collection of both models, with a durable terminal status."""
import json
import time
import traceback

from behavioral import ROOT, MODELS, SEEDS, Runner, persist, VERSION
from paid_client import STATE


def collect_independent(runner, seeds, failures):
    """A branch may exhaust its frozen retry limit without censoring other studies."""
    def attempt(name, seed, rounds, **kwargs):
        exclusion_path = ROOT / 'network_exclusions.json'
        exclusions = json.loads(exclusion_path.read_text()) if exclusion_path.exists() else []
        excluded = [entry for entry in exclusions if entry['model'] == runner.model and entry['episode'] == name]
        if excluded:
            failures.append({k: excluded[-1][k] for k in ('model', 'episode', 'reason')})
            print(f'MISSING {runner.model} {name}: excluded uncertain network request', flush=True)
            return None
        try:
            return runner.episode(name, seed, rounds, **kwargs)
        except RuntimeError as error:
            if not str(error).startswith('Three technical/schema failures'):
                raise
            failures.append({'model': runner.model, 'episode': name, 'reason': str(error)})
            print(f'MISSING {runner.model} {name}: {error}', flush=True)
            return None
    for seed in seeds:
        prefixes = {}
        for population in ('neutral', 'induced'):
            prefixes[population] = attempt(f'formation_{population}_{seed}', seed, 4,
                induced=population == 'induced', private_formation=population == 'neutral')
            arms = ['ordinary', 'benign', 'offer', 'evidence']
            rotate = seed % len(arms)
            for arm in arms[rotate:] + arms[:rotate]:
                name = f'probe_{population}_{arm}_{seed}'
                if prefixes[population] is None:
                    failures.append({'model': runner.model, 'episode': name, 'reason': 'formation checkpoint unavailable'})
                else:
                    attempt(name, seed, 4, prefix=prefixes[population], probe=arm)
        arms = ['private', 'shared', 'restricted']
        rotate = seed % len(arms)
        for arm in arms[rotate:] + arms[:rotate]:
            attempt(f'mediator_{arm}_{seed}', seed, 6, mediator=arm)
        arms = ['baseline', 'warning', 'penalty']
        rotate = seed % len(arms)
        for arm in arms[rotate:] + arms[:rotate]:
            name = f'enforcement_{arm}_{seed}'
            if prefixes['induced'] is None:
                failures.append({'model': runner.model, 'episode': name, 'reason': 'formation checkpoint unavailable'})
            else:
                attempt(name, seed, 6, prefix=prefixes['induced'], enforcement=arm)


if __name__ == '__main__':
    status = {'started_unix': time.time(), 'state': 'running', 'models_complete': [],
              'seeds_per_model': len(SEEDS), 'protocol': VERSION, 'failed_branches': []}
    path = ROOT / 'collection_status.json'
    if path.exists():
        with (ROOT / 'collection_attempts.jsonl').open('a') as handle:
            handle.write(path.read_text().replace('\n', '') + '\n')
    persist(path, status)
    try:
        for model in MODELS:
            status['current_model'] = model
            persist(path, status)
            collect_independent(Runner(model), SEEDS, status['failed_branches'])
            status['models_complete'].append(model)
            persist(path, status)
        status['state'] = 'complete_with_missing' if status['failed_branches'] else 'complete'
    except Exception as error:
        status['state'] = 'stopped'
        status['error'] = f'{type(error).__name__}: {error}'
        traceback.print_exc()
    finally:
        status['updated_unix'] = time.time()
        if STATE.exists():
            ledger = json.loads(STATE.read_text())
            status['budget_counted_usd'] = ledger['spent']
            status['pending_reservations'] = len(ledger['pending'])
        persist(path, status)
        print(json.dumps(status), flush=True)
