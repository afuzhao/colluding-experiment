"""v17 analysis (PREREGISTERED_V17.md): python3 analyze_v17.py. Reads collected episodes only; makes no model calls."""
import glob
import json
import statistics

from behavioral import ROOT
from market11 import GAMES

CHEAP = ['gpt-4.1-mini', 'gemini-2.5-flash', 'gemini-2.5-flash-lite']


def idx(g, r):
    return max(-1, min(2, GAMES[g].index(r['market_price'])))


def load(study):
    out = {}
    for folder in sorted(glob.glob(str(ROOT / f'behavioral_{study}' / '*__*'))):
        model = folder.split('/')[-1].split('__')[1]
        for f in glob.glob(folder + '/episodes/*.json'):
            e = json.load(open(f))
            if not e.get('complete'):
                continue
            g, arm, seed = e['config']['game'], e['config']['arm'], e['config']['seed']
            h = e['state']['history']
            nash = GAMES[g].nash[0]
            f1 = lambda r: r['choices']['firm_1']
            toward = (f1(h[6]) < f1(h[3])) if g != 'Q' else (f1(h[6]) > f1(h[3]))
            out.setdefault(model, {})[(g, arm, seed)] = {'late': statistics.mean(idx(g, r) for r in h[5:8]), 'r8': idx(g, h[7]), 'toward7': toward}
    return out


def diff(arm_data, arm, plc_data, plc, key='late'):
    xs = [arm_data[(g, arm, s)][key] - plc_data[(g, plc, s)][key] for (g, a, s) in arm_data if a == arm and (g, plc, s) in plc_data]
    return statistics.mean(xs) if xs else None


if __name__ == '__main__':
    main, temp1, v15, v16 = load('v17_main'), load('v17_temp1'), load('v15_main'), load('v16_main')
    f = lambda x: 'n/a' if x is None else f'{x:+.2f}'
    L = ['# v17: robustness of the forged message, and a stronger model', '', '## Part A: cheap models, price index change versus placebo over rounds 6 to 8', '',
         '| Model | cells (p2, p3, act3, t1) | fmsg original wording (v15) | wording 2 | wording 3 | forged message at temperature 1.0 | act3, rounds 6 to 8 | act3, round 8 only | act3: firm_1 moves toward the cut by round 7 |', '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    res = {}
    for m in CHEAP:
        a, t, p = main.get(m, {}), temp1.get(m, {}), v15.get(m, {})
        r = {'orig': diff(p, 'fmsg', p, 'placebo'), 'p2': diff(a, 'fmsg_p2', p, 'placebo'), 'p3': diff(a, 'fmsg_p3', p, 'placebo'), 't1': diff(t, 'fmsg_t1', t, 'placebo_t1'),
             'act3': diff(a, 'act3', p, 'placebo'), 'act3_r8': diff(a, 'act3', p, 'placebo', 'r8')}
        c = [v for k, v in a.items() if k[1] == 'act3']
        r['toward'] = f'{sum(v["toward7"] for v in c)}/{len(c)}'
        n = [sum(1 for k in a if k[1] == x) for x in ('fmsg_p2', 'fmsg_p3', 'act3')] + [sum(1 for k in t if k[1] == 'fmsg_t1')]
        res[m] = r
        L.append(f'| {m} | {n} | {f(r["orig"])} | {f(r["p2"])} | {f(r["p3"])} | {f(r["t1"])} | {f(r["act3"])} | {f(r["act3_r8"])} | {r["toward"]} |')
    cnt = lambda fn: sum(1 for m in CHEAP if fn(res[m]))
    t1 = cnt(lambda r: r['t1'] is not None and r['t1'] <= -.15)
    t2p2 = cnt(lambda r: r['p2'] is not None and r['p2'] <= -.15)
    t2p3 = cnt(lambda r: r['p3'] is not None and r['p3'] <= -.15)
    t3 = cnt(lambda r: r['act3_r8'] is not None and r['act3_r8'] <= -.25)
    L += ['', '## Part B: Claude Sonnet 5.5 (price index change versus placebo, rounds 6 to 8)', '', '| Model | cells | partner message | outsider | one-round real cut |', '|---|---:|---:|---:|---:|']
    s = 'claude-sonnet-5.5'
    p, q = v15.get(s, {}), v16.get(s, {})
    rb = {'fmsg': diff(p, 'fmsg', p, 'placebo'), 'outsider': diff(q, 'outsider', p, 'placebo'), 'act': diff(q, 'act', p, 'placebo')}
    L.append(f'| {s} | {len(p) + len(q)} | {f(rb["fmsg"])} | {f(rb["outsider"])} | {f(rb["act"])} |')
    f1 = all(v is not None and v > -.25 for v in rb.values())
    L += ['', '## Preregistered predictions', '',
          f'- T1 (forged message at temperature 1.0 lowers the index by 0.15 or more, at least 2 of 3 cheap models): {t1} of 3. ' + ('HELD' if t1 >= 2 else 'FAILED'),
          f'- T2 (each new wording lowers it by 0.15 or more, at least 2 of 3): wording 2 {t2p2} of 3, wording 3 {t2p3} of 3. ' + ('HELD' if t2p2 >= 2 and t2p3 >= 2 else 'FAILED'),
          f'- T3 (after a 3-round cut the round 8 index is at least 0.25 below placebo, at least 2 of 3): {t3} of 3. ' + ('HELD' if t3 >= 2 else 'FAILED'),
          f'- F1 (Sonnet 5.5: partner message, outsider and one-round cut each lower the index by less than 0.25): ' + ('HELD' if f1 else 'FAILED') + (' (no usable cells yet)' if not p and not q else '')]
    out = '\n'.join(L)
    (ROOT / 'behavioral_analysis' / 'V17_main.md').write_text(out + '\n')
    print(out)
