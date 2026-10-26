"""v18 part 3 analysis: python3 analyze_v18_reason.py. Compares answer-only API runs with reason-first API runs (same 17 cartels)."""
import glob
import json
from pathlib import Path

ROOT = Path(__file__).parent
meta = json.load(open(ROOT / 'v18_io' / 'meta.json'))
mv = lambda arm, r: (lambda k: abs(r['choice'] - k['nash']) <= abs(k['own4'] - k['nash']) / 2 and r['choice'] != k['own4'])(meta[f'{arm}|{r["id"]}'])
def load(pattern):
    out = {}
    for p in glob.glob(str(ROOT / 'behavioral_analysis' / pattern)):
        d = json.load(open(p)); m = d['model'].split('/')[1]
        for r in d['results']:
            out.setdefault(m, {}).setdefault(r['arm'], []).append(mv(r['arm'], r))
    return out
plain, reason = load('v18_api_*.json'), load('v18_reason_*.json')
cell = lambda d, m, a: f'{sum(d[m][a])}/{len(d[m][a])}' if m in d and a in d[m] else 'n/a'
L = ['# v18 part 3: does writing a reason first change what the API models do? (17 cartels)', '', '| Model | method | placebo | partner message | partner message tagged unverified |', '|---|---|---:|---:|---:|']
for m in ('claude-haiku-5.5', 'claude-haiku-4.5'):
    L.append(f'| {m} | answer only | ' + ' | '.join(cell(plain, m, a) for a in ('placebo', 'fmsg', 'tagged')) + ' |')
    L.append(f'| {m} | reason first | ' + ' | '.join(cell(reason, m, a) for a in ('placebo', 'fmsg', 'tagged')) + ' |')
n = lambda d, m, a: sum(d[m][a]) if m in d and a in d[m] else None
r1 = n(reason, 'claude-haiku-5.5', 'fmsg') is not None and n(reason, 'claude-haiku-5.5', 'fmsg') >= 12
r2 = n(reason, 'claude-haiku-5.5', 'placebo') is not None and n(reason, 'claude-haiku-5.5', 'placebo') <= 3
r3 = all(n(reason, 'claude-haiku-4.5', a) is not None for a in ('fmsg', 'placebo')) and n(reason, 'claude-haiku-4.5', 'fmsg') - n(plain, 'claude-haiku-4.5', 'fmsg') >= 4 and n(reason, 'claude-haiku-4.5', 'placebo') <= 3
L += ['', '## Preregistered predictions', '', f'- R1 (Haiku 5.5 partner message at least 12 of 17 with a reason): ' + ('HELD' if r1 else 'FAILED'), '- R2 (Haiku 5.5 placebo at most 3 of 17): ' + ('HELD' if r2 else 'FAILED'), '- R3 (Haiku 4.5 gains at least 4 cells, placebo at most 3): ' + ('HELD' if r3 else 'FAILED')]
print('\n'.join(L)); (ROOT / 'behavioral_analysis' / 'V18_reason.md').write_text('\n'.join(L) + '\n')
