"""Freeze v8 predictions from single-agent anchors (PREREGISTERED_V8.md). Run before any pair data exist."""
import glob
import hashlib
import itertools
import json
import statistics
import time

from behavioral import ROOT

MODELS = ['google/gemini-2.5-flash-lite', 'google/gemini-2.5-flash', 'openai/gpt-4.1-mini', 'openai/gpt-4.1',
          'anthropic/claude-haiku-5.5', 'anthropic/claude-haiku-4.5', 'anthropic/claude-sonnet-4.6']
COST = 2


def round1_prices(model, env):
    slug = model.replace('/', '__')
    prices = []
    opening = ROOT / 'behavioral_v5' / slug / 'grid_opening.json'
    if env == 'G1':
        for path in glob.glob(str(ROOT / 'behavioral_v5' / slug / 'episodes' / 'hold*_*.json')):
            saved = json.loads(open(path).read())
            if saved.get('complete'):
                prices.append(saved['state']['history'][0]['prices']['seller_1'])
    grid = ROOT / 'behavioral_v5' / slug / 'grid_opening.json'
    # grid_opening.json is written by run_grid.py under behavioral_v5/<slug>/ (G1..G4, 16 seeds)
    if grid.exists():
        prices += list(json.loads(grid.read_text())[env].values())
    return prices


if __name__ == '__main__':
    anchors, counts = {}, {}
    for env in ('G1', 'G2'):
        anchors[env] = {}
        for model in MODELS:
            p = round1_prices(model, env)
            counts[f'{env}|{model}'] = len(p)
            anchors[env][model] = {'median': statistics.median(p), 'mean': statistics.mean(p), 'n': len(p)}
    predictions = {}
    for env in ('G1', 'G2'):
        for a, b in itertools.combinations_with_replacement(MODELS, 2):
            lo, hi = sorted((anchors[env][a]['median'], anchors[env][b]['median']))
            predictions[f'{env}|{a}|{b}'] = {'law_market_price': lo, 'mean_anchor': (lo + hi) / 2, 'max_anchor': hi,
                'higher_seller_law': lo if lo > COST else hi, 'higher_seller_stay': hi, 'floor_pair': lo <= COST}
    out = {'frozen_unix': time.time(), 'anchors': anchors, 'predictions': predictions}
    text = json.dumps(out, indent=1, sort_keys=True)
    (ROOT / 'v8_predictions.json').write_text(text + '\n')
    print('sha256', hashlib.sha256(text.encode()).hexdigest())
    for env in ('G1', 'G2'):
        print(env, {m.split('/')[1]: (anchors[env][m]['median'], anchors[env][m]['n']) for m in MODELS})
