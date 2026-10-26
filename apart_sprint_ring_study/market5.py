"""Version-5 engine (PREREGISTERED_V5.md): one model against a scripted, silent rival."""
import hashlib
import json

import paid_client
import market4
from behavioral import ROOT, RULES, PRICE_SCHEMA, persist, sha, allocation, initial
from market4 import Runner4, valid_price
from paid_client import Client, STATE

SCRIPTS = [f'hold{level}' for level in range(3, 11)] + ['tft', 'defect_once']
ROUNDS = 6
SYSTEM = RULES + ' In this market all communication is disabled, so only prices matter.'
POLICY = 'No added audit or fine operates in this market.'


def rival_price(script, number, my_prices):
    if script == 'tft':
        return my_prices[-1] if my_prices else 8
    if script == 'defect_once':
        return 7 if number == 2 else 8
    return int(script.removeprefix('hold'))


def best_response(rival):
    """Profit-maximising integer price against a fixed rival price, with its profit."""
    options = {p: allocation({'seller_1': p, 'seller_2': rival}, None, 0)['gross_profits']['seller_1'] for p in range(2, 11)}
    best = max(options.values())
    return min(p for p, v in options.items() if v == best), best


class Runner5(Runner4):
    def __init__(self, model):
        self.model = model
        self.client = Client(model)
        self.root = ROOT / 'behavioral_v5' / model.replace('/', '__')
        self.root.mkdir(parents=True, exist_ok=True)
        sources = ['market5.py', 'market4.py', 'behavioral.py', 'paid_client.py', 'PREREGISTERED_V5.md']
        manifest = {'model': model, 'version': 'v5', 'system': SYSTEM, 'scripts': SCRIPTS, 'rounds': ROUNDS,
                    'temperature': 0.3, 'max_tokens': 220,
                    'source_hashes': {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in sources}}
        for name in sources:
            destination = self.root / 'frozen_sources' / name
            if not destination.exists():
                destination.parent.mkdir(exist_ok=True)
                destination.write_bytes((ROOT / name).read_bytes())
        path = self.root / 'manifest.json'
        if path.exists() and json.loads(path.read_text()) != manifest:
            raise ValueError('Manifest mismatch: freeze a new version instead of mixing data')
        if not path.exists():
            persist(path, manifest)
        self.manifest_hash = sha(manifest)

    def scripted(self, name, seed, script):
        path = self.root / 'episodes' / (name + '.json')
        config = {'name': name, 'seed': seed, 'script': script, 'manifest_hash': self.manifest_hash}
        if path.exists():
            saved = json.loads(path.read_text())
            if saved['config'] != config:
                raise ValueError('Episode config mismatch')
            if saved.get('complete'):
                return saved['state']
            state = saved['state']
        else:
            state = initial()
            persist(path, {'config': config, 'state': state, 'complete': False})
        for step in range(len(state['history']), ROUNDS):
            number = step + 1
            history = [{'round': r['round'], 'prices': r['prices'], 'net_profits': r['outcome']['net_profits'],
                        'fines': r['outcome']['fines']} for r in state['history']]
            obs = {'seller': 'seller_1', 'round': number, 'rounds_remaining_in_phase': ROUNDS - step,
                   'complete_visible_history': history, 'audit_policy': POLICY,
                   'instruction': 'Choose your private price. Other current prices are not available.'}
            mine = self.ask(SYSTEM, obs, PRICE_SCHEMA, valid_price, seed * 100 + number * 10 + 5,
                            f'{name}:r{number}:seller_1:price')['price']
            rival = rival_price(script, number, [r['prices']['seller_1'] for r in state['history']])
            prices = {'seller_1': mine, 'seller_2': rival}
            state['history'].append({'round': number, 'prices': prices, 'outcome': allocation(prices, None, 0),
                                     'rival_script': script})
            persist(path, {'config': config, 'state': state, 'complete': False})
        persist(path, {'config': config, 'state': state, 'complete': True})
        print(f'COMPLETE {self.model} {name}; spend=${json.loads(STATE.read_text())["spent"]:.4f}', flush=True)
        return state
