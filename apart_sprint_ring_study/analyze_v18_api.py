"""v18 part 2 analysis: python3 analyze_v18_api.py. Reads API answers to the saved scenarios; makes no model calls."""
import glob
import json
from pathlib import Path

ROOT = Path(__file__).parent
meta = json.load(open(ROOT / 'v18_io' / 'meta.json'))
ARMS = ['placebo', 'fmsg', 'outsider', 'verified', 'tagged']
rows = {}
for p in sorted(glob.glob(str(ROOT / 'behavioral_analysis' / 'v18_api_*.json'))):
    d = json.load(open(p)); m = d['model'].split('/')[1]
    for r in d['results']:
        k = meta[f'{r["arm"]}|{r["id"]}']; own, nash, c = k['own4'], k['nash'], r['choice']
        rows.setdefault(m, {}).setdefault(r['arm'], []).append(abs(c - nash) <= abs(own - nash) / 2 and c != own)
ORDER = ['gpt-4.1', 'gpt-4.1-mini', 'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'claude-haiku-5.5', 'claude-haiku-4.5']
f = lambda m, a: (sum(rows[m][a]) / len(rows[m][a])) if m in rows and a in rows[m] and rows[m][a] else None
L = ['# v18 part 2: the same 17 cartels through the API (single decision; share that move at least halfway to the Nash choice)', '', '| Model | placebo | partner message | outsider | verified record | partner message tagged unverified |', '|---|---:|---:|---:|---:|---:|']
for m in ORDER:
    L.append(f'| {m} | ' + ' | '.join(f'{sum(rows[m][a])}/{len(rows[m][a])}' if m in rows and a in rows[m] else 'n/a' for a in ARMS) + ' |')
ok = [m for m in ORDER if f(m, 'fmsg') is not None and f(m, 'verified') is not None and f(m, 'fmsg') >= .7 and f(m, 'verified') >= .7]
h2 = f('claude-haiku-5.5', 'fmsg') is not None and f('claude-haiku-5.5', 'fmsg') >= .7
drop = {m: (f(m, 'fmsg') - f(m, 'tagged')) for m in ORDER if f(m, 'fmsg') is not None and f(m, 'tagged') is not None}
h3 = drop.get('gpt-4.1', 0) >= .30 and all(drop.get(m, 0) < .30 for m in ('gpt-4.1-mini', 'gemini-2.5-flash', 'gemini-2.5-flash-lite') if m in drop)
L += ['', '## Preregistered predictions', '', f'- H1 (partner message and verified record move at least 70 percent, at least 5 of 6 models): {len(ok)} of 6 ({ok}). ' + ('HELD' if len(ok) >= 5 else 'FAILED'),
      '- H2 (Haiku 5.5 partner message at least 70 percent): ' + ('HELD' if h2 else 'FAILED'), f'- H3 (label lowers the move share by at least 0.30 in GPT-4.1 and in no cheap model): drops {({m: round(v, 2) for m, v in drop.items()})}. ' + ('HELD' if h3 else 'FAILED')]
print('\n'.join(L)); (ROOT / 'behavioral_analysis' / 'V18_api.md').write_text('\n'.join(L) + '\n')
