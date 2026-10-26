"""Can single-agent response curves (v5) predict two-agent outcomes (v3 relay-private, v4 base)? Descriptive."""
import json
import statistics

import analyze_v4
import analyze_v5
from analyze_scaling import MODELS, load as load_v3
from behavioral import ROOT, SEEDS
from extensions import EXT_SEEDS


def curve(model):
    """Mean model price in rounds 2-6 for each fixed rival price 3..10 (nearest level outside the range)."""
    table = {}
    for level in range(3, 11):
        cells = [r['prices']['seller_1'] for s in SEEDS + EXT_SEEDS for h in [analyze_v5.load(model, f'hold{level}', s)] if h for r in h[1:]]
        if cells:
            table[level] = statistics.mean(cells)
    return lambda rival: table[min(max(rival, min(table)), max(table))] if table else None


def simulate(f, p1, p2, rounds):
    path = [(p1, p2)]
    for _ in range(rounds - 1):
        p1, p2 = int(f(p2) + 0.5), int(f(p1) + 0.5)
        path.append((p1, p2))
    return path


if __name__ == '__main__':
    lines = ['# Do single-agent response curves predict two-agent markets?', '',
             'Private-relay markets (two copies of one model, prices visible, no messages between them). The response curve',
             'f(L) is the model\'s mean price against a fixed rival at L (v5). Prediction iterates f from the observed round-1',
             'prices. "Stay" keeps round-1 prices. Error is mean absolute difference in the final-round market price.', '',
             '| Model | Seeds | Observed final | Response-curve prediction | Stay-put | Constant 8 | Err curve | Err stay | Err const 8 |',
             '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    out = {}
    for model in MODELS:
        f = curve(model)
        rows = []
        for s in SEEDS:
            e = load_v3(model, 'mediator_private', s)
            if e and f(8) is not None:
                h = e['state']['history']
                start = (h[0]['prices']['seller_1'], h[0]['prices']['seller_2'])
                predicted = min(simulate(f, *start, 6)[-1])
                rows.append((h[-1]['outcome']['market_price'], predicted, min(start)))
        if not rows:
            continue
        obs, pred, stay = ([r[i] for r in rows] for i in range(3))
        err = lambda xs: statistics.mean(abs(a - b) for a, b in zip(obs, xs))
        out[model] = {'n': len(rows), 'observed': statistics.mean(obs), 'curve': statistics.mean(pred), 'stay': statistics.mean(stay),
                      'err_curve': err(pred), 'err_stay': err(stay), 'err_const8': err([8] * len(obs))}
        lines.append(f'| {model.split("/")[1]} | {len(rows)} | {statistics.mean(obs):.2f} | {statistics.mean(pred):.2f} | {statistics.mean(stay):.2f} | 8.00 | '
                     f'{err(pred):.2f} | {err(stay):.2f} | {err([8] * len(obs)):.2f} |')
    lines += ['', '## Pact vs no pact: price held after an agreement at 8 exists (v4 base) against the no-communication response f(8)', '',
              '| Model | f(8), no communication | Observed with pact and chat (rounds 5 to 8 mean) | Difference |', '|---|---:|---:|---:|']
    for model in MODELS:
        folder = ROOT / 'behavioral_v4' / model.replace('/', '__') / 'episodes'
        prices = []
        for s in SEEDS:
            path = folder / f'base_{s}.json'
            if path.exists() and json.loads(path.read_text()).get('complete'):
                h = json.loads(path.read_text())['state']['history'][4:8]
                prices += [p for r in h for p in r['prices'].values()]
        f = curve(model)
        if prices and f(8) is not None:
            lines.append(f'| {model.split("/")[1]} | {f(8):.2f} | {statistics.mean(prices):.2f} | {statistics.mean(prices) - f(8):+.2f} |')
            out.setdefault(model, {})['pact_premium'] = statistics.mean(prices) - f(8)
    (ROOT / 'behavioral_analysis' / 'PREDICTION.md').write_text('\n'.join(lines) + '\n')
    (ROOT / 'behavioral_analysis' / 'prediction.json').write_text(json.dumps(out, indent=2) + '\n')
    print('\n'.join(lines))
