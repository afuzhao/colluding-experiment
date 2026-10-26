"""v18 part 5 analysis (PREREGISTERED_V18.md, Part 5): python3 analyze_v18_ctrl.py. Experiment A: reverse-direction and reassurance controls. Experiment B: reasoning-first on four more API models."""
import glob
import json
from pathlib import Path

ROOT = Path(__file__).parent
meta = json.load(open(ROOT / 'v18_io' / 'meta.json'))
A = ROOT / 'behavioral_analysis'
API = ['gpt-4.1', 'gpt-4.1-mini', 'gemini-2.5-flash', 'gemini-2.5-flash-lite', 'claude-haiku-5.5', 'claude-haiku-4.5']
CC = ['sonnet', 'opus', 'fable']
cut = lambda arm, r: (lambda k: (r['choice'] - k['own4']) * (k['nash'] - k['own4']) > 0)(meta[f'{arm}|{r["id"]}'])
def load(pattern):
    out = {}
    for p in glob.glob(str(A / pattern)):
        d = json.load(open(p)); m = d['model'].split('/')[1]
        for r in d['results']:
            out.setdefault(m, {}).setdefault(r['arm'], []).append(r)
    return out
plain = load('v18_api_*.json'); ctrl = load('v18_ctrl_*.json'); reas = load('v18_reason_*.json')
for m in CC:
    for a in ('placebo', 'fmsg', 'raise', 'hold'):
        p = ROOT / 'v18_io' / 'out' / f'{m}_{a}.json'
        if p.exists():
            ctrl.setdefault(m, {})[a] = [{**x, 'arm': a} for x in json.load(open(p))]
def c(d, m, a):
    return sum(cut(a, r) for r in d[m][a]) if m in d and a in d[m] else None
cell = lambda v: 'n/a' if v is None else f'{v}/17'
hostile = lambda m: c(plain, m, 'fmsg') if m in API else c(ctrl, m, 'fmsg')
plac = lambda m: c(plain, m, 'placebo') if m in API else c(ctrl, m, 'placebo')
L = ['# v18 part 5, experiment A: does the firm cut only on a hostile claim? (cuts of 17)', '', '| Model | placebo | partner says it will cut | partner says it will raise | partner says it holds |', '|---|---:|---:|---:|---:|']
for m in API + CC:
    L.append(f'| {m} | ' + ' | '.join(cell(v) for v in (plac(m), hostile(m), c(ctrl, m, 'raise'), c(ctrl, m, 'hold'))) + ' |')
holds = [c(ctrl, m, 'hold') for m in API + CC]; raises = {m: c(ctrl, m, 'raise') for m in API + CC}
a1 = all(v is not None and v <= 3 for v in holds)
a2 = sum(v is not None and v <= 4 for v in raises.values())
big = [m for m in API + CC if hostile(m) is not None and hostile(m) >= 12 and m != 'haiku']
a3 = bool(big) and all(raises[m] is not None and raises[m] <= hostile(m) / 2 for m in big)
H = lambda b: 'HELD' if b else 'FAILED'
L += ['', f'- A1 (hold: at most 3 cuts in every run): {H(a1)}', f'- A2 (raise: at most 4 cuts in at least 7 of 9 runs): {a2} of 9. {H(a2 >= 7)}', f'- A3 (raise at most half of the hostile cuts wherever hostile was at least 12): runs {big}. {H(a3)}', '',
      '# v18 part 5, experiment B: does the "unverified" tag work only when the model reasons first? (cuts of 17)', '', '| Model | method | placebo | partner message | partner message tagged unverified |', '|---|---|---:|---:|---:|']
M4 = ['gpt-4.1', 'gpt-4.1-mini', 'gemini-2.5-flash', 'gemini-2.5-flash-lite']
eff = {}
for m in M4:
    for name, d in (('answer only', plain), ('reason first', reas)):
        L.append(f'| {m} | {name} | ' + ' | '.join(cell(c(d, m, a)) for a in ('placebo', 'fmsg', 'tagged')) + ' |')
    if all(c(d, m, a) is not None for d in (plain, reas) for a in ('fmsg', 'tagged')):
        eff[m] = (c(reas, m, 'fmsg') - c(reas, m, 'tagged')) - (c(plain, m, 'fmsg') - c(plain, m, 'tagged'))
b1 = all((c(reas, m, 'placebo') is not None and c(reas, m, 'placebo') <= 3) for m in M4)
b2 = sum(v >= 4 for v in eff.values())
b3 = c(reas, 'gpt-4.1', 'tagged') is not None and c(reas, 'gpt-4.1', 'tagged') <= 8
L += ['', f'- B1 (placebo at most 3 in all four): {H(b1)}', f'- B2 (tag effect at least 4 cells larger with reasoning, at least 3 of 4): {eff}. {H(b2 >= 3)}', f'- B3 (GPT-4.1 tagged at most 8 with reasoning): {H(b3)}']
print('\n'.join(L)); (A / 'V18_ctrl.md').write_text('\n'.join(L) + '\n')
