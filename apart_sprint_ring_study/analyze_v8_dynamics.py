"""Dynamics given the actual round-1 prices: does the higher-priced seller match down? (reviewer-requested decomposition of v8)"""
import json
import statistics
import sys

import analyze_v8
from analyze_v8 import ROOT, MODELS, load_cell


def episodes(regime, env, seedset=None):
    analyze_v8.SEEDSET = seedset
    out = []
    for i, a in enumerate(MODELS):
        for b in MODELS[i:]:
            out += [(a, b, e) for e in load_cell(a, b, regime, env)]
    return out


if __name__ == '__main__':
    regime, env = sys.argv[1], sys.argv[2]
    seedset = set(json.loads(sys.argv[3])) if len(sys.argv) > 3 else None
    rows = []
    for a, b, e in episodes(regime, env, seedset):
        h = e['state']['history']
        p1 = (h[0]['prices']['seller_1'], h[0]['prices']['seller_2'])
        if p1[0] == p1[1]:
            continue
        hi = 0 if p1[0] > p1[1] else 1
        key = ('seller_1', 'seller_2')[hi]
        later = [r['prices'][key] for r in h[2:]]
        low_later = [r['prices'][('seller_1', 'seller_2')[1 - hi]] for r in h[2:]]
        rows.append({'hi_r1': max(p1), 'lo_r1': min(p1), 'hi_later': statistics.mean(later), 'lo_later': statistics.mean(low_later),
                     'pair': (a, b)})
    n = len(rows)
    md = statistics.mean(abs(r['hi_later'] - r['lo_r1']) for r in rows)
    stay = statistics.mean(abs(r['hi_later'] - r['hi_r1']) for r in rows)
    matched = sum(abs(r['hi_later'] - r['lo_r1']) <= 0.5 for r in rows)
    stayed = sum(abs(r['hi_later'] - r['hi_r1']) <= 0.5 for r in rows)
    between = n - matched - stayed
    lo_up = sum(r['lo_later'] > r['lo_r1'] + 0.5 for r in rows)
    lines = [f'# v8 dynamics, {regime} {env}' + (f' (seed set of {len(seedset)})' if seedset else ''), '',
             f'Episodes whose two sellers opened at different prices: {n}. Higher-priced seller\'s mean price in rounds 3 to 6:',
             f'- within 0.5 of the lower opening price (matched down): {matched} ({matched / n:.0%})',
             f'- within 0.5 of its own opening price (stayed): {stayed} ({stayed / n:.0%})',
             f'- somewhere else: {between} ({between / n:.0%})',
             f'Mean absolute error: match-down {md:.2f}, stay {stay:.2f}.',
             f'Lower-priced seller moved up by more than 0.5: {lo_up} ({lo_up / n:.0%}).']
    (ROOT / 'behavioral_analysis' / f'V8_dynamics_{regime}_{env}{"_even" if seedset else ""}.md').write_text('\n'.join(lines) + '\n')
    print('\n'.join(lines))
