"""Analyze protocol v8 (PREREGISTERED_V8.md): do pair markets follow the lowest anchor? Descriptive."""
import json
import random
import statistics

import market8
from behavioral import ROOT
from predict_pairs import MODELS

SEEDSET = None  # set to restrict to a seed family
PRED = json.loads((ROOT / 'v8_predictions.json').read_text())['predictions']


def short(m):
    return m.split('/')[1].replace('gemini-2.5-', 'gem-').replace('claude-', '')


def load_cell(a, b, regime, env):
    out = []
    paths = []
    for first, second in ((a, b), (b, a)) if a != b else ((a, b),):
        root = ROOT / 'behavioral_v8' / f'{first.replace("/", "__")}--{second.replace("/", "__")}' / 'episodes'
        paths += sorted(root.glob(f'{regime}_{env}_*.json')) if root.exists() else []
    for path in paths:
        saved = json.loads(path.read_text())
        if not saved.get('complete') or saved['config']['seed'] == 9003:  # 9003 is the calibration seed
            continue
        if SEEDSET and saved['config']['seed'] not in SEEDSET:
            continue
        for r in saved['state']['history']:
            assert r['outcome']['market_price'] == market8.alloc(r['prices'], env, r['active_floor'])['market_price']
        out.append(saved)
    return out


def ci(values, reps=4000):
    rng = random.Random(20261025)
    means = sorted(statistics.mean(rng.choices(values, k=len(values))) for _ in range(reps))
    return means[int(0.025 * reps)], means[int(0.975 * reps)]


def cell_stats(episodes, a, b):
    """Per-episode mean market price and per-model mean price over rounds 3-6."""
    rows = []
    for e in episodes:
        seats = e['config']['seats']
        h = e['state']['history'][2:]
        s1, s2 = statistics.mean(r['prices']['seller_1'] for r in h), statistics.mean(r['prices']['seller_2'] for r in h)
        by = {seats[0]: s1, seats[1]: s2} if seats[0] != seats[1] else {a: (s1 + s2) / 2}
        rows.append({'market': statistics.mean(r['outcome']['market_price'] for r in h), 'by': by,
                     'pact': e['state']['pact_ever'], 'executed': sum(r['outcome']['executed'] for r in h)})
    return rows


if __name__ == '__main__':
    import sys
    regime, env = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ('silent', 'G1')
    family = sys.argv[3] if len(sys.argv) > 3 else 'ext'
    SEEDSET = {3102, 3204, 3306, 3408, 3510, 3612, 3714, 3816} if family == 'even' else {2101, 2203, 2307, 2411, 2513, 2617, 2719, 2821} if family == 'ext' else None
    lines = [f'# Protocol v8 pair markets: {regime}, {env}', '',
             'Rounds 3 to 6. Market price is the lower seller price. "Law" is min of the two anchors (frozen before collection).',
             'Higher-anchor seller price is compared with match-down (law) and stay-put predictions.', '',
             '| Pair | n | Observed market price [95%] | Law | Mean-anchor | Higher-anchor seller: observed | match-down | stay |', '|---|---:|---|---:|---:|---:|---:|---:|']
    results, abs_err = {}, {'law': [], 'mean': [], 'max': []}
    hi_err = {'law': [], 'stay': []}
    for i, a in enumerate(MODELS):
        for b in MODELS[i:]:
            eps = load_cell(a, b, regime, env)
            if not eps:
                continue
            p = PRED[f'{env}|{a}|{b}']
            rows = cell_stats(eps, a, b)
            mk = [r['market'] for r in rows]
            lo, hi = ci(mk) if len(mk) > 1 else (mk[0], mk[0])
            anchors = json.loads((ROOT / 'v8_predictions.json').read_text())['anchors'][env]
            high = a if anchors[a]['median'] >= anchors[b]['median'] else b
            hv = statistics.mean(r['by'][high] for r in rows) if a != b else statistics.mean(r['by'][a] for r in rows)
            lines.append(f'| {short(a)} + {short(b)} | {len(rows)} | {statistics.mean(mk):.2f} [{lo:.2f}, {hi:.2f}] | {p["law_market_price"]:.1f} | {p["mean_anchor"]:.1f} | '
                         f'{hv:.2f} | {p["higher_seller_law"]:.1f} | {p["higher_seller_stay"]:.1f} |')
            results[f'{a}|{b}'] = {'n': len(rows), 'market': statistics.mean(mk), 'ci': [lo, hi], 'high_seller': hv, **p}
            abs_err['law'].append(abs(statistics.mean(mk) - p['law_market_price']))
            abs_err['mean'].append(abs(statistics.mean(mk) - p['mean_anchor']))
            abs_err['max'].append(abs(statistics.mean(mk) - p['max_anchor']))
            if a != b:
                hi_err['law'].append(abs(hv - p['higher_seller_law']))
                hi_err['stay'].append(abs(hv - p['higher_seller_stay']))
    lines += ['', f'Cells analysed: {len(abs_err["law"])}. Mean absolute error of the market price: law {statistics.mean(abs_err["law"]):.2f}, '
              f'mean-anchor {statistics.mean(abs_err["mean"]):.2f}, higher-anchor {statistics.mean(abs_err["max"]):.2f}.' if abs_err['law'] else 'No cells.',
              f'Higher-anchor seller (mixed pairs, {len(hi_err["law"])} cells): mean absolute error match-down {statistics.mean(hi_err["law"]):.2f}, stay-put {statistics.mean(hi_err["stay"]):.2f}.' if hi_err['law'] else '']
    out = ROOT / 'behavioral_analysis'
    suffix = '_even' if family == 'even' else ''
    (out / f'V8_{regime}_{env}{suffix}.md').write_text('\n'.join(lines) + '\n')
    (out / f'v8_{regime}_{env}{suffix}.json').write_text(json.dumps(results, indent=2) + '\n')
    print('\n'.join(lines))
