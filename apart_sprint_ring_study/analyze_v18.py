"""v18 analysis (PREREGISTERED_V18.md): python3 analyze_v18.py DIR. Reads subagent answers only; makes no model calls."""
import json
import sys
from pathlib import Path

D = Path(sys.argv[1])
meta = json.load(open(D / 'meta.json'))
MODELS = ['haiku', 'sonnet', 'opus', 'fable']
ARMS = ['placebo', 'fmsg', 'outsider', 'verified', 'tagged']
share = {}
for m in MODELS:
    for a in ARMS:
        p = D / 'out' / f'{m}_{a}.json'
        if not p.exists():
            continue
        try:
            rows = json.load(open(p))
        except Exception:
            continue
        mv = []
        for r in rows:
            k = meta[f'{a}|{r["id"]}']
            own, nash, c = k['own4'], k['nash'], r['choice']
            mv.append(abs(c - nash) <= abs(own - nash) / 2 and c != own)
        share[(m, a)] = (sum(mv), len(mv))
L = ['# v18: share of cartels where firm_1 moves at least halfway to the Nash choice at round 5 (Claude models run as Claude Code subagents)', '',
     '| Model | placebo | partner message | outsider (unverified) | verified record | partner message tagged unverified |', '|---|---:|---:|---:|---:|---:|']
for m in MODELS:
    L.append(f'| {m} | ' + ' | '.join(f'{share[(m, a)][0]}/{share[(m, a)][1]}' if (m, a) in share else 'n/a' for a in ARMS) + ' |')
f = lambda m, a: share[(m, a)][0] / share[(m, a)][1] if (m, a) in share and share[(m, a)][1] else None
ok1 = {m: (f(m, 'fmsg') is not None and f(m, 'verified') is not None and f(m, 'outsider') is not None and f(m, 'fmsg') >= .8 and f(m, 'verified') >= .8 and f(m, 'outsider') < .2) for m in ('sonnet', 'opus', 'fable')}
c2 = f('haiku', 'outsider') is not None and f('opus', 'outsider') is not None and f('haiku', 'outsider') - f('opus', 'outsider') >= .20
c3 = {m: (f(m, 'placebo') is not None and f(m, 'placebo') < .2) for m in MODELS if (m, 'placebo') in share}
d1 = {m: (f(m, 'tagged') is not None and f(m, 'tagged') <= .30) for m in ('opus', 'fable')}
d2 = f('haiku', 'tagged') is not None and f('haiku', 'tagged') > .5
L += ['', '## Preregistered predictions', '', f'- C1 (Sonnet, Opus, Fable: partner and verified at least 80 percent, outsider under 20 percent): {ok1}. ' + ('HELD' if all(ok1.values()) else 'FAILED'),
      f'- C2 (Haiku outsider move share at least 0.20 above Opus): ' + ('HELD' if c2 else 'FAILED'), f'- C3 (placebo moves under 20 percent for each model): {c3}. ' + ('HELD' if c3 and all(c3.values()) else 'FAILED or incomplete'),
      f'- D1 (tagged move share at most 30 percent for Opus and Fable): {d1}. ' + ('HELD' if d1 and all(d1.values()) else 'FAILED or incomplete'),
      f'- D2 (Haiku tagged move share above 50 percent): ' + ('HELD' if d2 else 'FAILED or incomplete')]
print('\n'.join(L))
(Path(__file__).parent / 'behavioral_analysis' / 'V18_main.md').write_text('\n'.join(L) + '\n')
