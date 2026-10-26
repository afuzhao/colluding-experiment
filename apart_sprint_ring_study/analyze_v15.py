"""v15 pilot analysis (PREREGISTERED_V15.md): python3 analyze_v15.py [tag]. Reads collected episodes only; makes no model calls."""
import glob
import json
import statistics
import sys

from behavioral import ROOT
from market11 import GAMES

TAG = sys.argv[1] if len(sys.argv) > 1 else 'pilot'
ARMS = ['placebo', 'fmsg', 'frec']


def idx(game, r):
    return max(-1, min(2, GAMES[game].index(r['market_price'])))


def load():
    data = {}
    for folder in sorted(glob.glob(str(ROOT / f'behavioral_v15_{TAG}' / '*__*'))):
        model = folder.split('/')[-1].replace('__', '/', 1)
        for f in glob.glob(folder + '/episodes/*.json'):
            e = json.load(open(f))
            if not e.get('complete'):
                continue
            g, arm, seed = e['config']['game'], e['config']['arm'], e['config']['seed']
            h = e['state']['history']
            base = json.load(open(ROOT / 'behavioral_v11_main' / folder.split('/')[-1] / 'episodes' / f'{g}_chat_{seed}.json'))['state']['history']
            data.setdefault(model, {})[(g, arm, seed)] = {'post': statistics.mean(idx(g, r) for r in h[4:8]), 'orig': statistics.mean(idx(g, r) for r in base[4:8]),
                                                         'pre': statistics.mean(idx(g, r) for r in h[2:4]), 'cut': h[4]['choices']['firm_1'] < h[3]['choices']['firm_1'] if g != 'Q' else h[4]['choices']['firm_1'] > h[3]['choices']['firm_1'],
                                                         'last': idx(g, h[7]), 'cs': statistics.mean(r['consumer_surplus'] for r in h[4:8])}
    return data


if __name__ == '__main__':
    data = load()
    L = [f'# v15 {TAG}: forged record probes', '', 'Mean price index over rounds 5 to 8 (clipped to [-1, 2]); round-5 cut = firm_1 moves toward the competitive choice at round 5; last = index in round 8.', '',
         '| Model | Market | Arm | n | index r5-8 | original v11 chat | firm_1 cuts at r5 | index r8 |', '|---|---|---|---:|---:|---:|---:|---:|']
    diffs = {}
    for m, d in data.items():
        for g in 'PQ':
            for arm in ARMS:
                c = {k: v for k, v in d.items() if k[0] == g and k[1] == arm}
                if not c:
                    continue
                L.append(f'| {m.split("/")[1]} | {g} | {arm} | {len(c)} | {statistics.mean(v["post"] for v in c.values()):.2f} | {statistics.mean(v["orig"] for v in c.values()):.2f} | '
                         f'{sum(v["cut"] for v in c.values())}/{len(c)} | {statistics.mean(v["last"] for v in c.values()):.2f} |')
        for arm in ARMS[1:]:
            ds = [d[(g, arm, s)]['post'] - d[(g, 'placebo', s)]['post'] for (g, a, s) in d if a == arm and (g, 'placebo', s) in d]
            diffs[(m, arm)] = statistics.mean(ds) if ds else None
    L += ['', '## Gate (forged arm minus placebo, index, mean over market and seed)', '', '| Model | fmsg | frec | placebo minus original chat |', '|---|---:|---:|---:|']
    passed = {a: 0 for a in ARMS[1:]}
    sane = []
    for m, d in data.items():
        po = [v['post'] - v['orig'] for k, v in d.items() if k[1] == 'placebo']
        sane.append(abs(statistics.mean(po)) <= .15 if po else False)
        for a in ARMS[1:]:
            passed[a] += diffs[(m, a)] is not None and diffs[(m, a)] <= -.25
        fmt = lambda x: 'n/a' if x is None else f'{x:+.2f}'
        L.append(f'| {m.split("/")[1]} | {fmt(diffs[(m, "fmsg")])} | {fmt(diffs[(m, "frec")])} | {fmt(statistics.mean(po) if po else None)} |')
    go = max(passed.values()) >= 2 and all(sane)
    L += ['', f'Models passing (difference at most -0.25): fmsg {passed["fmsg"]} of {len(data)}, frec {passed["frec"]} of {len(data)}. Placebo sane in {sum(sane)} of {len(sane)} models.',
          f'**Gate: {"GO" if go else "NO-GO"}** (needs at least 2 models passing for one forged arm and a sane placebo).']
    out = '\n'.join(L)
    (ROOT / 'behavioral_analysis' / f'V15_{TAG}.md').write_text(out + '\n')
    print(out)
