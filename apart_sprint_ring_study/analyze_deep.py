"""Cross-study analysis of all collected data. python3 analyze_deep.py. Reads collected files only, makes no model calls."""
import glob
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

from market11 import GAMES

ROOT = Path(__file__).parent
A = ROOT / 'behavioral_analysis'
meta = json.load(open(ROOT / 'v18_io' / 'meta.json'))
rng = np.random.default_rng(7)
out = []
P = out.append

# ---------- single-decision data ----------
scen = {}
for f in glob.glob(str(ROOT / 'v18_io' / 'scenarios_*.json')):
    arm = Path(f).stem.split('_', 1)[1]
    for it in json.load(open(f)):
        last = it['observation']['current_messages'][-1] if it['observation']['current_messages'] else {}
        hist = it['observation']['complete_visible_history']
        scen[(arm, it['id'])] = {'claim': last.get('target'), 'other4': hist[3]['other_choice'], 'price4': hist[3]['market_price'], 'grid': it['allowed_choices']}
rows = []  # run, harness, arm, id, choice
for p in glob.glob(str(A / 'v18_api_*.json')) + glob.glob(str(A / 'v18_leak_*.json')) + glob.glob(str(A / 'v18_ctrl_*.json')):
    d = json.load(open(p)); m = d['model'].split('/')[1]
    rows += [(m, 'api', r['arm'], r['id'], r['choice']) for r in d['results']]
for p in glob.glob(str(A / 'v18_reason_*.json')):
    d = json.load(open(p)); m = d['model'].split('/')[1]
    rows += [(m, 'api-reason', r['arm'], r['id'], r['choice']) for r in d['results']]
for p in glob.glob(str(ROOT / 'v18_io' / 'out' / '*.json')):
    m, arm = Path(p).stem.split('_', 1)
    if m == 'haiku':
        continue
    rows += [(m, 'subagent', arm, r['id'], r['choice']) for r in json.load(open(p))]
API = ['gpt-4.1', 'gpt-4.1-mini', 'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'claude-haiku-5.5', 'claude-haiku-4.5']
CC = ['sonnet', 'opus', 'fable']
CLAIMARMS = ['fmsg', 'outsider', 'verified', 'tagged', 'leak', 'trojan', 'raise', 'hold']


def classify(arm, cid, c):
    k = meta[f'{arm}|{cid}']; G = GAMES[k['game']]; s = scen[(arm, cid)]
    own4, other4 = k['own4'], s['other4']
    x = s['claim'] if s['claim'] is not None else k['nash']
    best = lambda b: {a for a in G.grid if G.profit(a, b)[0] >= max(G.profit(a2, b)[0] for a2 in G.grid) - 1e-9}
    if c in best(x) and c != own4:
        return 'best reply to the claim'
    if c == own4:
        return 'stay'
    if c in best(other4):
        return 'best reply to no change'
    if c == x:
        return 'copy the claim'
    return 'other'


P('# Deep analysis across all studies\n')
P('## 1. What do firms do with a claim? Choice classified by what would be right if the claim were true\n')
P('Best reply = the choice that maximizes the firm\'s own profit if the partner really plays the claimed value. Stay = repeats its round 4 choice. Pooled over cartels and runs of each group.\n')
for harness, runs in (('api', API), ('subagent', CC)):
    P(f'### {harness} runs ({len(runs)} models x 17 cartels per row)\n')
    P('| Claim shown | stay | best reply to the claim | best reply to no change | copy the claim | other |\n|---|---:|---:|---:|---:|---:|')
    for arm in CLAIMARMS:
        cnt = Counter(classify(arm, cid, c) for m, h, a, cid, c in rows if h == harness and a == arm and m in runs)
        n = sum(cnt.values())
        if n:
            P(f'| {arm} | ' + ' | '.join(f'{100 * cnt[k] // n}%' for k in ('stay', 'best reply to the claim', 'best reply to no change', 'copy the claim', 'other')) + f' | n={n}')
    cnt = Counter(classify('fmsg', cid, c) for m, h, a, cid, c in rows if h == harness and a == 'placebo' and m in runs for _ in [0] if (('fmsg', cid) in scen))
    n = sum(cnt.values())
    P(f'\nPlacebo choices classified as if the partner message had been shown (the baseline rate of that behavior without any claim): ' + ', '.join(f'{k} {100 * v // n}%' for k, v in cnt.items()) + '\n')

P('\n## 2. Cut rates with the cartel as the unit (bootstrap over 17 cartels, difference from placebo)\n')
cutv = lambda arm, cid, c: (c - meta[f'{arm}|{cid}']['own4']) * (meta[f'{arm}|{cid}']['nash'] - meta[f'{arm}|{cid}']['own4']) > 0
cartels = sorted({cid for (_, cid) in scen})
def boot(harness, runs, arm):
    per = []
    for cid in cartels:
        a = [cutv(arm, cid, c) for m, h, ar, i, c in rows if h == harness and ar == arm and i == cid and m in runs]
        b = [cutv('placebo', cid, c) for m, h, ar, i, c in rows if h == harness and ar == 'placebo' and i == cid and m in runs]
        if a and b:
            per.append(np.mean(a) - np.mean(b))
    per = np.array(per); bs = [rng.choice(per, len(per)).mean() for _ in range(5000)]
    return per.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5), len(per)
P('| Claim | API models (6): mean cut rate above placebo [95% CI] | Claude subagents (3) |\n|---|---|---|')
for arm in CLAIMARMS:
    cells = []
    for harness, runs in (('api', API), ('subagent', CC)):
        r = boot(harness, runs, arm); cells.append(f'{r[0]:+.2f} [{r[1]:+.2f}, {r[2]:+.2f}]' if r[3] else 'n/a')
    P(f'| {arm} | ' + ' | '.join(cells) + ' |')

P('\n## 3. What makes a cartel fragile? Cut rate on the partner message (API models), by market and by source of the cartel\n')
def agg(key):
    d = defaultdict(list)
    for m, h, a, cid, c in rows:
        if h == 'api' and a == 'fmsg' and m in API:
            d[key(cid)].append(cutv('fmsg', cid, c))
    return {k: f'{100 * np.mean(v):.0f}% (n={len(v)})' for k, v in sorted(d.items())}
P('By market:', ) ; P(str(agg(lambda cid: meta['fmsg|' + cid]['game']))); P('\nBy source model of the cartel:'); P(str(agg(lambda cid: cid.rsplit('_', 1)[0])))
strength = {}
for cid in cartels:
    G = GAMES[meta['fmsg|' + cid]['game']]; strength[cid] = G.index(scen[('fmsg', cid)]['price4'])
xs = [strength[cid] for cid in cartels]; ys = [np.mean([cutv('fmsg', cid, c) for m, h, a, i, c in rows if h == 'api' and a == 'fmsg' and i == cid and m in API]) for cid in cartels]
rho, pv = spearmanr(xs, ys); P(f'\nCorrelation of cartel strength (round 4 price index) with how often the firm cuts: Spearman {rho:+.2f} (p={pv:.2f}, 17 cartels)\n')

# ---------- full episodes ----------
P('\n## 4. Mechanism in the full 8-round episodes: what happens after a firm cuts on a forged message?\n')
def episodes(root, arms):
    for f in glob.glob(str(ROOT / root / '*__*' / 'episodes' / '*.json')):
        e = json.load(open(f))
        if e.get('complete') and e['config']['arm'] in arms and len(e['state']['history']) >= 8:
            yield f.split('/')[-3].split('__')[1], e
dyn = defaultdict(lambda: Counter())
for root in ('behavioral_v15_main', 'behavioral_v16_main', 'behavioral_v17_main'):
    for m, e in episodes(root, {'fmsg', 'outsider', 'verified', 'fmsg_p2', 'fmsg_p3'}):
        G = GAMES[e['config']['game']]; h = e['state']['history']; gi = G.grid.index
        c4, c5, c6 = h[3]['choices'], h[4]['choices'], h[5]['choices']
        step = lambda a, b: abs(gi(a) - gi(b))
        if c5['firm_1'] != c4['firm_1'] and (c5['firm_1'] - c4['firm_1']) * (G.nash[0] - c4['firm_1']) > 0:
            d = dyn[m]; d['cells'] += 1
            d['firm_2 held at round 5'] += c5['firm_2'] == c4['firm_2']
            d['firm_1 profit up at round 5'] += h[4]['net_profits']['firm_1'] > h[3]['net_profits']['firm_1']
            d['firm_2 profit down at round 5'] += h[4]['net_profits']['firm_2'] < h[3]['net_profits']['firm_2']
            d['firm_1 back within 1 step at round 6'] += step(c6['firm_1'], c4['firm_1']) <= 1
            d['firm_2 cuts at round 6'] += (c6['firm_2'] - c4['firm_2']) * (G.nash[1] - c4['firm_2']) > 0
            d['both low at round 6'] += (c6['firm_1'] != c4['firm_1'] and (c6['firm_2'] - c4['firm_2']) * (G.nash[1] - c4['firm_2']) > 0)
cols = ['cells', 'firm_2 held at round 5', 'firm_1 profit up at round 5', 'firm_2 profit down at round 5', 'firm_1 back within 1 step at round 6', 'firm_2 cuts at round 6']
P('Among cells where firm_1 cut at round 5 after a forged claim (partner message, outsider, verified record, two paraphrases):\n')
P('| Model | ' + ' | '.join(cols) + ' |\n|---|' + '---:|' * len(cols))
for m in ['gpt-4.1', 'gpt-4.1-mini', 'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'claude-haiku-5.5', 'claude-haiku-4.5']:
    if dyn[m]['cells']:
        P(f'| {m} | ' + ' | '.join(str(dyn[m][c]) for c in cols) + ' |')
tot = Counter(); [tot.update(v) for v in dyn.values()]
P('| all | ' + ' | '.join(str(tot[c]) for c in cols) + ' |')

# real cut persistence
P('\n### Does a real cut persist more than a forged claim? Share of episodes where the price index is back at 0.4 or above at round 8 (cheap models only)\n')
P('| Arm | episodes | back to cartel level at round 8 | mean index round 8 |\n|---|---:|---:|---:|')
pers = defaultdict(list)
for root in ('behavioral_v15_main', 'behavioral_v16_main', 'behavioral_v17_main'):
    for m, e in episodes(root, {'placebo', 'fmsg', 'outsider', 'verified', 'act', 'act3'}):
        if m in ('gpt-4.1-mini', 'gemini-2.5-flash', 'gemini-2.5-flash-lite'):
            G = GAMES[e['config']['game']]; pers[e['config']['arm']].append(G.index(e['state']['history'][7]['market_price']))
for arm in ('placebo', 'fmsg', 'outsider', 'verified', 'act', 'act3'):
    v = pers.get(arm, [])
    if v:
        P(f'| {arm} | {len(v)} | {100 * np.mean([x >= 0.4 for x in v]):.0f}% | {np.mean(v):+.2f} |')

# ---------- cross-study traits ----------
P('\n## 5. Is credulity one trait of a model across studies? (6 API models; rank correlations are descriptive only)\n')
ring = {}
txt = (A / 'V13_main.md').read_text().split('## All conditions, every model')[1]
started = False
for line in txt.splitlines():
    if line.startswith('| ') and 'tacit' in line:
        started = True
    elif started and not line.startswith('|'):
        break
    if started and line.startswith('| ') and 'tacit' not in line and '---' not in line:
        cells = [x.strip() for x in line.strip('|').split('|')]
        try: ring[cells[0]] = float(cells[2])
        except Exception: pass
single = {m: np.mean([cutv('fmsg', cid, c) for mm, h, a, cid, c in rows if h == 'api' and a == 'fmsg' and mm == m]) for m in API}
proposal = {m: np.mean([cutv('trojan', cid, c) for mm, h, a, cid, c in rows if h == 'api' and a == 'trojan' and mm == m]) for m in API}
outs = {m: np.mean([cutv('outsider', cid, c) for mm, h, a, cid, c in rows if h == 'api' and a == 'outsider' and mm == m]) for m in API}
P('| Model | ring: joins with no words (%) | single decision: cuts on partner message | cuts on outsider | follows cooperative proposal |\n|---|---:|---:|---:|---:|')
for m in API:
    P(f'| {m} | {ring.get(m, float("nan")):.0f} | {single[m]:.2f} | {outs[m]:.2f} | {proposal[m]:.2f} |')
ok = [m for m in API if m in ring]
for name, other in (('partner message', single), ('outsider', outs), ('proposal', proposal)):
    r, p = spearmanr([ring[m] for m in ok], [other[m] for m in ok]); P(f'\nSpearman, ring tacit joining vs {name}: {r:+.2f} (n={len(ok)} models, p={p:.2f})')
r, p = spearmanr([single[m] for m in API], [proposal[m] for m in API]); P(f'Spearman, partner message vs proposal: {r:+.2f} (p={p:.2f})')
r, p = spearmanr([single[m] for m in API], [outs[m] for m in API]); P(f'Spearman, partner message vs outsider: {r:+.2f} (p={p:.2f})')

P('\n## 6. Extra checks\n')
by_m = defaultdict(list)
for cid in cartels:
    by_m[meta['fmsg|' + cid]['game']].append((strength[cid], ys[cartels.index(cid)]))
for g, v in sorted(by_m.items()):
    xs2, ys2 = zip(*v); r, p = spearmanr(xs2, ys2) if len(v) > 3 else (float('nan'), float('nan'))
    P(f'Cartel strength vs cut rate within market {g}: n={len(v)}, mean strength {np.mean(xs2):.2f}, mean cut rate {np.mean(ys2):.2f}, Spearman {r:+.2f}')
# does firm_1 stay low only when firm_2 really cuts?
cond = Counter()
for root in ('behavioral_v15_main', 'behavioral_v16_main', 'behavioral_v17_main'):
    for m, e in episodes(root, {'fmsg', 'outsider', 'verified', 'fmsg_p2', 'fmsg_p3'}):
        G = GAMES[e['config']['game']]; h = e['state']['history']; gi = G.grid.index
        c4, c5, c6 = h[3]['choices'], h[4]['choices'], h[5]['choices']
        if c5['firm_1'] != c4['firm_1'] and (c5['firm_1'] - c4['firm_1']) * (G.nash[0] - c4['firm_1']) > 0:
            partner_cut = (c6['firm_2'] - c4['firm_2']) * (G.nash[1] - c4['firm_2']) > 0
            back = abs(gi(c6['firm_1']) - gi(c4['firm_1'])) <= 1
            cond[(partner_cut, back)] += 1
from scipy.stats import fisher_exact
P(f"\nFirm_1 after cutting on a forged claim (all full-episode cells pooled): partner really cut at round 6 and firm_1 back to the cartel level {cond[(True, True)]}, partner cut and firm_1 stays low {cond[(True, False)]}, partner held and firm_1 back {cond[(False, True)]}, partner held and firm_1 stays low {cond[(False, False)]}. Fisher exact p={fisher_exact([[cond[(True, True)], cond[(True, False)]], [cond[(False, True)], cond[(False, False)]]])[1]:.2g}")
for a, b in (('fmsg', 'placebo'), ('act', 'placebo'), ('act3', 'placebo'), ('act3', 'fmsg')):
    xa = [x >= 0.4 for x in pers[a]]; xb = [x >= 0.4 for x in pers[b]]
    P(f'Round 8 back at cartel level, {a} {sum(xa)}/{len(xa)} vs {b} {sum(xb)}/{len(xb)}: Fisher p={fisher_exact([[sum(xa), len(xa) - sum(xa)], [sum(xb), len(xb) - sum(xb)]])[1]:.3f}')
mirror = {}
for arm in ('raise', 'trojan'):
    mirror[arm] = {m: np.mean([abs(c - scen[(arm, cid)]['claim']) < 1e-9 for mm, h, a, cid, c in rows if h == 'api' and a == arm and mm == m]) for m in API}
P('\nShare of cartels where the firm copies the claimed value exactly (API): ' + '; '.join(f"{arm}: " + ', '.join(f"{m} {v:.2f}" for m, v in d.items()) for arm, d in mirror.items()))

P('\nWithin each model: after firm_1 cut on a forged claim, firm_1 back at the cartel level at round 6 when the partner held vs when the partner really cut at round 6')
percond = defaultdict(Counter)
for root in ('behavioral_v15_main', 'behavioral_v16_main', 'behavioral_v17_main'):
    for m, e in episodes(root, {'fmsg', 'outsider', 'verified', 'fmsg_p2', 'fmsg_p3'}):
        G = GAMES[e['config']['game']]; h = e['state']['history']; gi = G.grid.index
        c4, c5, c6 = h[3]['choices'], h[4]['choices'], h[5]['choices']
        if c5['firm_1'] != c4['firm_1'] and (c5['firm_1'] - c4['firm_1']) * (G.nash[0] - c4['firm_1']) > 0:
            pc = (c6['firm_2'] - c4['firm_2']) * (G.nash[1] - c4['firm_2']) > 0
            percond[m][(pc, abs(gi(c6['firm_1']) - gi(c4['firm_1'])) <= 1)] += 1
for m, c in percond.items():
    held = c[(False, True)] + c[(False, False)]; cut_ = c[(True, True)] + c[(True, False)]
    P(f"- {m}: partner held {c[(False, True)]}/{held} back; partner cut {c[(True, True)]}/{cut_} back")

(A / 'DEEP.md').write_text('\n'.join(out) + '\n'); print('\n'.join(out))
