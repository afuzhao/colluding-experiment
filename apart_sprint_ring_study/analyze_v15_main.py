"""v15 full-run analysis (PREREGISTERED_V15.md addendum): python3 analyze_v15_main.py. Reads collected episodes only; makes no model calls."""
import glob
import json
import statistics

from behavioral import ROOT
from market11 import GAMES

ARMS = ['placebo', 'fmsg', 'frec', 'hide', 'fixed']
CHEAP = ['gpt-4.1-mini', 'gemini-2.5-flash', 'gemini-2.5-flash-lite']


def idx(game, r):
    return max(-1, min(2, GAMES[game].index(r['market_price'])))


def load():
    data = {}
    for folder in sorted(glob.glob(str(ROOT / 'behavioral_v15_main' / '*__*'))):
        model = folder.split('/')[-1].split('__')[1]
        for f in glob.glob(folder + '/episodes/*.json'):
            e = json.load(open(f))
            if not e.get('complete'):
                continue
            g, arm, seed = e['config']['game'], e['config']['arm'], e['config']['seed']
            h = e['state']['history']
            data.setdefault(model, {})[(g, arm, seed)] = {'post': statistics.mean(idx(g, r) for r in h[4:8]), 'r8': idx(g, h[7]), 'cs': statistics.mean(r['consumer_surplus'] for r in h[4:8]),
                                                         'profit': statistics.mean(sum(r['net_profits'].values()) for r in h[4:8]), 'cut': h[4]['choices']['firm_1'] != h[3]['choices']['firm_1']}
    return data


def diff(d, arm, key='post', games='PQL'):
    xs = [d[(g, arm, s)][key] - d[(g, 'placebo', s)][key] for (g, a, s) in d if a == arm and g in games and (g, 'placebo', s) in d]
    return statistics.mean(xs) if xs else None


if __name__ == '__main__':
    data = load()
    order = [m for m in ['gpt-4.1', 'gpt-4.1-mini', 'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'claude-haiku-5.5', 'claude-haiku-4.5'] if m in data]
    fmt = lambda x: 'n/a' if x is None else f'{x:+.2f}'
    L = ['# v15 full run: forged record probes', '', 'Price index change versus placebo (rounds 5 to 8, mean over markets and seeds; negative means prices fell). Index clipped to [-1, 2].', '',
         '| Model | episodes | fmsg | frec | hide | fixed (r5-8) | fixed (r8 only) | placebo index |', '|---|---:|---:|---:|---:|---:|---:|---:|']
    res = {}
    for m in order:
        d = data[m]
        res[m] = {a: diff(d, a) for a in ARMS[1:]}
        res[m]['fixed_r8'] = diff(d, 'fixed', 'r8')
        po = statistics.mean(v['post'] for k, v in d.items() if k[1] == 'placebo')
        L.append(f'| {m} | {len(d)} | {fmt(res[m]["fmsg"])} | {fmt(res[m]["frec"])} | {fmt(res[m]["hide"])} | {fmt(res[m]["fixed"])} | {fmt(res[m]["fixed_r8"])} | {po:.2f} |')
    L += ['', '## fmsg minus placebo by market (index)', '', '| Model | P | Q | L |', '|---|---:|---:|---:|']
    for m in order:
        L.append(f'| {m} | ' + ' | '.join(fmt(diff(data[m], 'fmsg', 'post', g)) for g in 'PQL') + ' |')
    L += ['', '## Cost to the firms and gain to customers versus placebo (mean over cells)', '', '| Model | arm | consumer surplus change | joint profit change | firm_1 cuts at r5 |', '|---|---|---:|---:|---:|']
    for m in order:
        for a in ARMS[1:]:
            c = {k: v for k, v in data[m].items() if k[1] == a}
            if c:
                L.append(f'| {m} | {a} | {diff(data[m], a, "cs"):+.0f} | {diff(data[m], a, "profit"):+.0f} | {sum(v["cut"] for v in c.values())}/{len(c)} |')
    n = lambda f: sum(1 for m in order if f(res[m]))
    ok = lambda v, t: v is not None and v <= t
    m1 = n(lambda r: ok(r['fmsg'], -.25))
    m2 = n(lambda r: r['fmsg'] is not None and r['frec'] is not None and r['fmsg'] < r['frec'])
    m3 = n(lambda r: ok(r['hide'], -.25))
    m4 = n(lambda r: ok(r['fixed_r8'], -.25))
    cheap = {g: statistics.mean(x for x in (diff(data[m], 'fmsg', 'post', g) for m in CHEAP if m in data) if x is not None) for g in 'PQL'}
    m5 = all(v <= -.25 for v in cheap.values())
    L += ['', '## Preregistered predictions', '',
          f'- M1 (fmsg lowers index by 0.25 or more in at least 4 of 6 models): {m1} of {len(order)}. ' + ('HELD' if m1 >= 4 else 'FAILED'),
          f'- M2 (fmsg lowers it more than frec in at least 4 of 6): {m2} of {len(order)}. ' + ('HELD' if m2 >= 4 else 'FAILED'),
          f'- M3 (hide lowers index by 0.25 or more in at least 3 of 6): {m3} of {len(order)}. ' + ('HELD' if m3 >= 3 else 'FAILED'),
          f'- M4 (after the round 7 correction, round 8 index is still 0.25 or more below placebo in at least 3 of 6): {m4} of {len(order)}. ' + ('HELD' if m4 >= 3 else 'FAILED'),
          f'- M5 (fmsg lowers index by 0.25 or more in each market, three cheap models pooled): P {cheap["P"]:+.2f}, Q {cheap["Q"]:+.2f}, L {cheap["L"]:+.2f}. ' + ('HELD' if m5 else 'FAILED')]
    out = '\n'.join(L)
    (ROOT / 'behavioral_analysis' / 'V15_main.md').write_text(out + '\n')
    print(out)
