"""v16 analysis (PREREGISTERED_V16.md): python3 analyze_v16.py. Reads collected episodes only; makes no model calls."""
import glob
import json
import statistics

from behavioral import ROOT
from market11 import GAMES

ORDER = ['gpt-4.1', 'gpt-4.1-mini', 'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'claude-haiku-5.5', 'claude-haiku-4.5']
ARMS = ['fmsg', 'outsider', 'verified', 'act']


def idx(g, r):
    return max(-1, min(2, GAMES[g].index(r['market_price'])))


def load():
    data = {}
    for study in ('v15', 'v16'):
        for folder in sorted(glob.glob(str(ROOT / f'behavioral_{study}_main' / '*__*'))):
            model = folder.split('/')[-1].split('__')[1]
            for f in glob.glob(folder + '/episodes/*.json'):
                e = json.load(open(f))
                if not e.get('complete'):
                    continue
                g, arm, seed = e['config']['game'], e['config']['arm'], e['config']['seed']
                if arm not in ['placebo'] + ARMS:
                    continue
                h = e['state']['history']
                data.setdefault(model, {})[(g, arm, seed)] = {'late': statistics.mean(idx(g, r) for r in h[5:8]), 'all': statistics.mean(idx(g, r) for r in h[4:8]),
                                                             'cut': h[4]['choices']['firm_1'] != h[3]['choices']['firm_1']}
    return data


def diff(d, arm, key='late'):
    xs = [d[(g, arm, s)][key] - d[(g, 'placebo', s)][key] for (g, a, s) in d if a == arm and (g, 'placebo', s) in d]
    return statistics.mean(xs) if xs else None


if __name__ == '__main__':
    data = load()
    models = [m for m in ORDER if m in data]
    f = lambda x: 'n/a' if x is None else f'{x:+.2f}'
    L = ['# v16: who says it, and does an action beat words?', '', 'Price index change versus placebo over rounds 6 to 8 (mean over markets and seeds; negative means prices fell). fmsg = message attributed to the partner (v15).', '',
         '| Model | cells | partner message (fmsg) | outsider | verified record | real cut (act) |', '|---|---:|---:|---:|---:|---:|']
    res = {}
    for m in models:
        res[m] = {a: diff(data[m], a) for a in ARMS}
        L.append(f'| {m} | {len(data[m])} | ' + ' | '.join(f(res[m][a]) for a in ARMS) + ' |')
    L += ['', 'Same, rounds 5 to 8 (includes the round of the forged message or forced cut):', '', '| Model | fmsg | outsider | verified | act |', '|---|---:|---:|---:|---:|']
    for m in models:
        L.append(f'| {m} | ' + ' | '.join(f(diff(data[m], a, 'all')) for a in ARMS) + ' |')
    L += ['', 'Firm_1 changes its choice at round 5 (cells):', '', '| Model | placebo | fmsg | outsider | verified | act |', '|---|---:|---:|---:|---:|---:|']
    for m in models:
        row = []
        for a in ['placebo'] + ARMS:
            c = [v for k, v in data[m].items() if k[1] == a]
            row.append(f'{sum(v["cut"] for v in c)}/{len(c)}')
        L.append(f'| {m} | ' + ' | '.join(row) + ' |')
    cnt = lambda fn: sum(1 for m in models if fn(res[m]))
    both = lambda r, a, b: r[a] is not None and r[b] is not None
    s1 = cnt(lambda r: both(r, 'fmsg', 'outsider') and r['outsider'] - r['fmsg'] >= .15)
    s2 = cnt(lambda r: both(r, 'verified', 'fmsg') and r['fmsg'] - r['verified'] >= .15)
    s3 = cnt(lambda r: r['act'] is not None and r['act'] <= -.25)
    s4 = cnt(lambda r: both(r, 'act', 'fmsg') and r['fmsg'] - r['act'] >= .15)
    L += ['', '## Preregistered predictions', '',
          f'- S1 (partner message lowers the index at least 0.15 more than the outsider message, at least 4 of 6 models): {s1} of {len(models)}. ' + ('HELD' if s1 >= 4 else 'FAILED'),
          f'- S2 (verified record lowers it at least 0.15 more than the partner message, at least 4 of 6): {s2} of {len(models)}. ' + ('HELD' if s2 >= 4 else 'FAILED'),
          f'- S3 (a real cut lowers the index by 0.25 or more, at least 4 of 6): {s3} of {len(models)}. ' + ('HELD' if s3 >= 4 else 'FAILED'),
          f'- S4 (a real cut lowers it at least 0.15 more than the partner message, at least 4 of 6): {s4} of {len(models)}. ' + ('HELD' if s4 >= 4 else 'FAILED')]
    out = '\n'.join(L)
    (ROOT / 'behavioral_analysis' / 'V16_main.md').write_text(out + '\n')
    print(out)
