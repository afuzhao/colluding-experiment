"""v18 part 4 analysis (PREREGISTERED_V18.md, Part 4): python3 analyze_v18_leak.py. Reads collected answers only."""
import glob
import json
from pathlib import Path

ROOT = Path(__file__).parent
meta = json.load(open(ROOT / 'v18_io' / 'meta.json'))
A = ROOT / 'behavioral_analysis'
API = ['gpt-4.1', 'gpt-4.1-mini', 'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'claude-haiku-5.5', 'claude-haiku-4.5']
CC = ['sonnet', 'opus', 'fable']
cut = lambda arm, r: (lambda k: (r['choice'] - k['own4']) * (k['nash'] - k['own4']) > 0)(meta[f'{arm}|{r["id"]}'])
half = lambda arm, r: (lambda k: abs(r['choice'] - k['nash']) <= abs(k['own4'] - k['nash']) / 2 and r['choice'] != k['own4'])(meta[f'{arm}|{r["id"]}'])
def follow(r):
    k = meta[f'trojan|{r["id"]}']
    return (r['choice'] - k['own4']) / (k['proptarget'] - k['own4']) >= 0.5
data = {}
for p in glob.glob(str(A / 'v18_api_*.json')) + glob.glob(str(A / 'v18_leak_*.json')):
    d = json.load(open(p)); m = d['model'].split('/')[1]
    for r in d['results']:
        data.setdefault(m, {}).setdefault(r['arm'], []).append(r)
for m in CC:
    for a in ('placebo', 'fmsg', 'leak', 'leakctl', 'trojan'):
        p = ROOT / 'v18_io' / 'out' / f'{m}_{a}.json'
        if p.exists():
            data.setdefault(m, {})[a] = [{**x, 'arm': a} for x in json.load(open(p))]
n = lambda m, a, f: sum(f(a, r) for r in data[m][a]) if m in data and a in data[m] else None
c = lambda m, a, f=cut: n(m, a, f)
fol = lambda m: sum(follow(r) for r in data[m]['trojan']) if m in data and 'trojan' in data[m] else None
cell = lambda v: 'n/a' if v is None else f'{v}/17'
L = ['# v18 part 4: leaked note and cooperative-looking proposal (17 cartels, single decision)', '',
     'Cut = choice changes toward the Nash choice. Follow = moves at least half of the way to the proposed halfway target. Halfway = moves at least halfway to the Nash choice.', '',
     '| Model | placebo cut | partner announcement cut | leaked note cut | irrelevant note cut | proposal: cut | proposal: followed | proposal: halfway-to-Nash | announcement: halfway-to-Nash |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for m in API + CC:
    L.append(f'| {m} | ' + ' | '.join(cell(v) for v in (c(m, 'placebo'), c(m, 'fmsg'), c(m, 'leak'), c(m, 'leakctl'), c(m, 'trojan'), fol(m), c(m, 'trojan', half), c(m, 'fmsg', half))) + ' |')
ok = lambda v, t, ge=True: v is not None and (v >= t if ge else v <= t)
l1 = all(ok(c(m, 'leakctl'), 3, False) for m in API + CC if c(m, 'leakctl') is not None)
l2 = sum(ok(c(m, 'leak'), 12) for m in API)
l3m = [m for m in API if c(m, 'fmsg') is not None and c(m, 'fmsg') < 14]
l3 = bool(l3m) and all(ok(c(m, 'leak'), c(m, 'fmsg') + 3) for m in l3m)
l4 = all(ok(c(m, 'leak'), 12) for m in CC)
t1 = sum(ok(fol(m), 10) for m in API)
t2 = sum(c(m, 'trojan', half) is not None and c(m, 'fmsg', half) is not None and c(m, 'trojan', half) < c(m, 'fmsg', half) for m in API)
t3 = all(ok(fol(m), 10) for m in CC)
H = lambda b: 'HELD' if b else 'FAILED'
L += ['', '## Preregistered predictions', '', f'- L1 (irrelevant note: at most 3 cuts in every run): {H(l1)}', f'- L2 (leak: at least 12 cuts in at least 4 of 6 API models): {l2} of 6. {H(l2 >= 4)}',
      f'- L3 (leak beats announcement by at least 3 cells where the announcement cut under 14): models {l3m}. {H(l3)}', f'- L4 (Sonnet, Opus, Fable: leak at least 12): {H(l4)}',
      f'- T1 (proposal followed in at least 10 of 17 in at least 4 of 6 API models): {t1} of 6. {H(t1 >= 4)}', f'- T2 (fewer halfway-to-Nash moves under proposal than announcement, at least 4 of 6): {t2} of 6. {H(t2 >= 4)}', f'- T3 (Sonnet, Opus, Fable follow in at least 10 of 17): {H(t3)}']
print('\n'.join(L)); (A / 'V18_leak.md').write_text('\n'.join(L) + '\n')
