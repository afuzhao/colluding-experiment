"""Match-down rule vs alternatives on v5, on informative rows only, with seed-level intervals (reviewer-requested)."""
import json
import random
import statistics

import analyze_v5
import market5
from analyze_v5 import MODELS, load
from behavioral import ROOT, SEEDS
from extensions import EXT_SEEDS

LEVELS = range(3, 11)


def rate_ci(per_seed):
    """per_seed: list of (hits, n) pairs. Mean over pooled rows with a seed-resampling interval."""
    rng = random.Random(20261025)
    def pooled(sample):
        h, n = sum(x[0] for x in sample), sum(x[1] for x in sample)
        return h / n if n else float('nan')
    draws = sorted(pooled(rng.choices(per_seed, k=len(per_seed))) for _ in range(5000))
    return pooled(per_seed), draws[125], draws[4875]


def rows(model, seeds):
    out = []
    for s in seeds:
        for L in LEVELS:
            h = load(model, f'hold{L}', s)
            out.append((s, L, [r['prices']['seller_1'] for r in h]))
    return out


if __name__ == '__main__':
    seeds = SEEDS + EXT_SEEDS
    lines = ['# Match-down rule, informative rows only', '',
             'Rows are (seed, rival level L). p1 is the model\'s own round-1 price in that episode. Informative rows have L < p1,',
             'where the rules differ: match-down predicts L, stay predicts p1, best response is the profit-maximising price.',
             'Rates are exact-match shares, with 95% intervals that resample seeds (rows within a seed are correlated).', '',
             '| Model | Rows (L < p1) | Round 2 only: match / undercut below L / stay | Rounds 2-6: match | Rounds 2-6: best response | Rows (L ≥ p1): price stays at p1 |',
             '|---|---:|---|---|---|---|']
    results = {}
    for model in MODELS:
        data = rows(model, seeds)
        m2, below2, stay2, m26, br26, up = ([] for _ in range(6))
        nrows = 0
        for s in seeds:
            sub = [(L, p) for (ss, L, p) in data if ss == s]
            a = [0, 0]; b = [0, 0]; c = [0, 0]; d = [0, 0]; e = [0, 0]; f = [0, 0]
            for L, p in sub:
                if L < p[0]:
                    nrows += 1
                    a[1] += 1; a[0] += p[1] == L
                    b[1] += 1; b[0] += p[1] < L
                    c[1] += 1; c[0] += p[1] == p[0]
                    d[1] += len(p) - 1; d[0] += sum(x == L for x in p[1:])
                    br = market5.best_response(L)[0]
                    e[1] += len(p) - 1; e[0] += sum(x == br for x in p[1:])
                else:
                    f[1] += len(p) - 1; f[0] += sum(x == p[0] for x in p[1:])
            m2.append(a); below2.append(b); stay2.append(c); m26.append(d); br26.append(e); up.append(f)
        fmt = lambda per: '{:.2f} [{:.2f}, {:.2f}]'.format(*rate_ci(per))
        lines.append(f'| {model.split("/")[1]} | {nrows} | {fmt(m2)} / {fmt(below2)} / {fmt(stay2)} | {fmt(m26)} | {fmt(br26)} | {fmt(up)} |')
        results[model] = {'rows': nrows, 'round2_match': rate_ci(m2), 'round2_below': rate_ci(below2), 'round2_stay': rate_ci(stay2),
                          'match_2_6': rate_ci(m26), 'br_2_6': rate_ci(e if False else br26), 'stay_when_rival_higher': rate_ci(up)}
    # pooled opening price across every episode (not only one script)
    lines += ['', '## Opening price pooled over all scripts and seeds', '', '| Model | Mean round-1 price | Range | Episodes |', '|---|---:|---|---:|']
    for model in MODELS:
        first = [load(model, f'hold{L}', s)[0]['prices']['seller_1'] for s in seeds for L in LEVELS]
        lines.append(f'| {model.split("/")[1]} | {statistics.mean(first):.2f} | {min(first)} to {max(first)} | {len(first)} |')
        results[model]['opening_mean_pooled'] = statistics.mean(first)
    (ROOT / 'behavioral_analysis' / 'MATCHDOWN.md').write_text('\n'.join(lines) + '\n')
    (ROOT / 'behavioral_analysis' / 'matchdown.json').write_text(json.dumps(results, indent=2) + '\n')
    print('\n'.join(lines))
