"""v18 part 3 (post hoc): share of 17 cartels where the firm changes its choice at all, by run. python3 analyze_v18_change.py"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
meta = json.load(open(ROOT / 'v18_io' / 'meta.json'))
chg = lambda arm, r: r['choice'] != meta[f'{arm}|{r["id"]}']['own4']
A = ROOT / 'behavioral_analysis'
rows = lambda p: json.load(open(p))['results']
L = ['# v18 part 3 (post hoc, not preregistered): share of 17 cartels where the firm changes its own choice at all', '',
     'The earlier "moves at least halfway to the Nash choice" count understates firms that best-respond to the announced move (for example choosing 20 against an announced 32). This table counts any change from the firm\'s round 4 choice.', '',
     '| Run | placebo | partner message | partner message tagged unverified |', '|---|---:|---:|---:|']
def line(name, get):
    cells = []
    for a in ('placebo', 'fmsg', 'tagged'):
        r = get(a); cells.append(f'{sum(chg(a, x) for x in r)}/{len(r)}' if r else 'n/a')
    L.append(f'| {name} | ' + ' | '.join(cells) + ' |')
for m in ('claude-haiku-5.5', 'claude-haiku-4.5'):
    s = m.replace('.', '_')
    a, b = rows(A / f'v18_api_anthropic__{s}.json'), rows(A / f'v18_reason_anthropic__{s}.json')
    line(f'{m}, API, answer only', lambda arm: [x for x in a if x['arm'] == arm])
    line(f'{m}, API, reason first', lambda arm: [x for x in b if x['arm'] == arm])
for m in ('haiku', 'sonnet', 'opus', 'fable'):
    line(f'{m}, Claude Code subagent', lambda arm, m=m: json.load(open(ROOT / 'v18_io' / 'out' / f'{m}_{arm}.json')))
print('\n'.join(L)); (A / 'V18_change.md').write_text('\n'.join(L) + '\n')
