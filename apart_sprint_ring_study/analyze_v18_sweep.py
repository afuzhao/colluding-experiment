"""v18 part 6 analysis (PREREGISTERED_V18.md, Part 6): python3 analyze_v18_sweep.py. Reads collected answers only."""
import glob
import json
from collections import defaultdict
from pathlib import Path

from market11 import GAMES

ROOT = Path(__file__).parent
A = ROOT / 'behavioral_analysis'
meta = json.load(open(ROOT / 'v18_io' / 'meta.json'))
API = ['gpt-4.1', 'gpt-4.1-mini', 'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'claude-haiku-5.5', 'claude-haiku-4.5']
CC = ['sonnet', 'opus', 'fable']
SRC = ['partner', 'outsider', 'tagged']
cells = defaultdict(list)  # (model, source, depth) -> list of dict
def add(m, src, arm, r):
    k = meta[f'{arm}|{r["id"]}']; G = GAMES[k['game']]; x, n, o4, own4, c = k['x'], k['nash'], k['other4'], k['own4'], r['choice']
    gi = G.grid.index(min(G.grid, key=lambda g: abs(g - o4))); near = G.grid[gi + (-1 if n < o4 else 1)]
    depth = 'nash' if x == n else 'near' if x == near else 'mid'
    best = max(G.profit(a, x)[0] for a in G.grid)
    cells[(m, src, depth)].append({'cut': (c - own4) * (n - own4) > 0, 'br': G.profit(c, x)[0] >= best - 1e-9 and c != own4, 'copy': abs(c - x) < 1e-9, 'stay': c == own4, 'game': k['game']})
for p in glob.glob(str(A / 'v18_sweep_*.json')):
    d = json.load(open(p)); m = d['model'].split('/')[1]
    for r in d['results']:
        src = r['arm'].split('_', 1)[1]; add(m, src, r['arm'], r)
for m in CC:
    for src in SRC:
        p = ROOT / 'v18_io' / 'out' / f'{m}_swc_{src}.json'
        if p.exists():
            for r in json.load(open(p)):
                add(m, src, f'swc_{src}', r)
sh = lambda m, s, dp, key, game=None: (lambda L: sum(x[key] for x in L) / len(L) if L else None)([x for x in cells[(m, s, dp)] if game is None or x['game'] in game])
f = lambda v: 'n/a' if v is None else f'{v:.2f}'
L = ['# v18 part 6: claimed-value sweep (cut share by source and claim depth; 17 cartels, 3 to 5 claimed values each)', '', 'Depth: nash = the partner claims the Nash choice; mid = 25 to 75 percent of the way; near = one grid step toward Nash.', '',
     '| Model | source | nash | mid | near |', '|---|---|---:|---:|---:|']
for m in API + CC:
    for s in SRC:
        L.append(f'| {m} | {s} | ' + ' | '.join(f(sh(m, s, dp, "cut")) for dp in ('nash', 'mid', 'near')) + ' |')
L += ['', '## Copy versus best reply (partner source, markets Q and L only, all depths pooled)', '', '| Model | exact best reply | copies the claimed value | n |', '|---|---:|---:|---:|']
s1 = 0
for m in API + CC:
    sel = [x for dp in ('nash', 'mid', 'near') for x in cells[(m, 'partner', dp)] if x['game'] in ('Q', 'L')]
    if sel:
        b = sum(x['br'] for x in sel) / len(sel); c = sum(x['copy'] for x in sel) / len(sel); L.append(f'| {m} | {b:.2f} | {c:.2f} | {len(sel)} |')
        s1 += (m in API and b > c)

L += ['', '## Partial claims only (mid and near depth, all markets, partner source): what the firm does', '', '| Model | exact best reply | copies the claimed value | stays | other | n |', '|---|---:|---:|---:|---:|---:|']
part = defaultdict(lambda: defaultdict(int))
for (m, s, dp), v in cells.items():
    if s == 'partner' and dp in ('mid', 'near'):
        for x in v:
            part[m]['n'] += 1; part[m]['br'] += x['br'] and not x['copy']; part[m]['copy'] += x['copy'] and not x['br']; part[m]['both'] += x['br'] and x['copy']; part[m]['stay'] += x['stay']
for m in API + CC:
    p = part[m]
    if p['n']:
        other = p['n'] - p['br'] - p['copy'] - p['both'] - p['stay']
        L.append(f"| {m} | {(p['br'] + p['both']) / p['n']:.2f} | {(p['copy'] + p['both']) / p['n']:.2f} | {p['stay'] / p['n']:.2f} | {other / p['n']:.2f} | {p['n']} |")

H = lambda b: 'HELD' if b else 'FAILED'
s2 = sum((sh(m, 'partner', 'nash', 'cut') or 0) - (sh(m, 'partner', 'near', 'cut') or 0) >= .15 for m in API)
d3 = {m: (sh(m, 'partner', 'nash', 'cut') or 0) - (sh(m, 'outsider', 'nash', 'cut') or 0) for m in API}
s3 = all(d3[m] >= .2 for m in ('gpt-4.1', 'gpt-4.1-mini', 'claude-haiku-5.5', 'claude-haiku-4.5')) and all(abs(d3[m]) <= .1 for m in ('gemini-2.5-flash', 'gemini-2.5-flash-lite'))
d4 = {m: [(sh(m, 'partner', dp, 'cut') or 0) - (sh(m, 'tagged', dp, 'cut') or 0) for dp in ('nash', 'mid', 'near') if cells[(m, 'tagged', dp)]] for m in CC}
s4 = all(v >= .5 for m in ('opus', 'fable') for v in d4[m]) and all(abs(v) <= .2 for v in d4['sonnet'])
s5 = all((sh(m, 'partner', dp, 'br') or 0) >= .8 for m in CC for dp in ('nash', 'mid', 'near'))
L += ['', '## Preregistered predictions', '', f'- S1 (best reply beats copy in at least 5 of 6 API models): {s1} of 6. {H(s1 >= 5)}', f'- S2 (cut share at nash at least .15 above near, at least 4 of 6): {s2} of 6. {H(s2 >= 4)}',
      f'- S3 (outsider gap at nash: {({m: round(v, 2) for m, v in d3.items()})}): {H(s3)}', f'- S4 (tag gaps {({m: [round(x, 2) for x in v] for m, v in d4.items()})}): {H(s4)}', f'- S5 (subagents exact best reply at least .8 at every depth): {H(s5)}']
print('\n'.join(L)); (A / 'V18_sweep.md').write_text('\n'.join(L) + '\n')
