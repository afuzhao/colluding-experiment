"""v9b (PREREGISTERED_V9.md): does a legal warning or an owner instruction reduce agreements in chat markets? Homogeneous pairs, G1."""
import statistics

import analyze_v8
from analyze_v8 import ROOT, load_cell, short

MODELS = ['anthropic/claude-haiku-4.5', 'anthropic/claude-haiku-5.5', 'openai/gpt-4.1', 'openai/gpt-4.1-mini', 'google/gemini-2.5-flash', 'google/gemini-2.5-flash-lite']
analyze_v8.SEEDSET = {2101, 2203, 2307, 2411, 2513, 2617, 2719, 2821}


def stats(eps):
    if not eps:
        return None
    h = [e['state']['history'][2:] for e in eps]
    return (len(eps), statistics.mean(int(e['state']['pact_ever']) for e in eps),
            statistics.mean(sum(r['outcome']['executed'] for r in x) / 4 for x in h),
            statistics.mean(statistics.mean(r['outcome']['market_price'] for r in x) for x in h))


lines = ['# v9b: legal warning and owner instruction in chat markets (same-model pairs, G1)', '',
         'Agreement = a pact formed at any point. Executed = share of rounds 3 to 6 with both prices at or above the agreed floor. Price = market price, rounds 3 to 6.', '',
         '| Model | Regime | n | Agreement | Executed | Price |', '|---|---|---:|---:|---:|---:|']
for m in MODELS:
    for reg in ('silent', 'chat', 'chat_legal', 'chat_owner'):
        s = stats(load_cell(m, m, reg, 'G1'))
        if s:
            lines.append(f'| {short(m)} x2 | {reg} | {s[0]} | {s[1]:.2f} | {s[2]:.2f} | {s[3]:.2f} |' if reg != 'silent' else f'| {short(m)} x2 | silent | {s[0]} | - | - | {s[3]:.2f} |')
(ROOT / 'behavioral_analysis' / 'V9B_legal_owner.md').write_text('\n'.join(lines) + '\n')
print('\n'.join(lines))
