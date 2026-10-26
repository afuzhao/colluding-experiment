"""H3 (PREREGISTERED_V8.md): does chat lift price above the lowest anchor? Compare chat and silent markets per pair (G1)."""
import json
import statistics

import analyze_v8
from analyze_v8 import ROOT, PRED, MODELS, load_cell, short

analyze_v8.SEEDSET = {2101, 2203, 2307, 2411, 2513, 2617, 2719, 2821}  # same seed family for chat and silent

FLOOR_MODEL = 'anthropic/claude-haiku-4.5'


def stats(episodes):
    price = statistics.mean(statistics.mean(r['outcome']['market_price'] for r in e['state']['history'][2:]) for e in episodes)
    pact = statistics.mean(int(e['state']['pact_ever']) for e in episodes)
    executed = statistics.mean(sum(r['outcome']['executed'] for r in e['state']['history'][2:]) / 4 for e in episodes)
    return price, pact, executed


if __name__ == '__main__':
    lines = ['# H3: chat versus silent, G1 pair markets', '',
             'Rounds 3 to 6. Pact = an agreement formed at any point. Executed = share of rounds 3 to 6 with both prices at or above the floor.',
             'Law = lowest anchor (frozen). Lift = chat price minus law.', '',
             '| Pair | n chat / silent | Silent price | Chat price | Law | Lift | Agreement formed | Executed share |', '|---|---:|---:|---:|---:|---:|---:|---:|']
    rows, out = [], {}
    for i, a in enumerate(MODELS):
        for b in MODELS[i:]:
            chat, silent = load_cell(a, b, 'chat', 'G1'), load_cell(a, b, 'silent', 'G1')
            if not chat or not silent:
                continue
            cp, pact, ex = stats(chat)
            sp = stats(silent)[0]
            law = PRED[f'G1|{a}|{b}']['law_market_price']
            floor_pair = FLOOR_MODEL in (a, b)
            rows.append((a, b, cp, law, floor_pair))
            out[f'{a}|{b}'] = {'chat': cp, 'silent': sp, 'law': law, 'pact': pact, 'executed': ex, 'n_chat': len(chat), 'n_silent': len(silent)}
            lines.append(f'| {short(a)} + {short(b)} | {len(chat)} / {len(silent)} | {sp:.2f} | {cp:.2f} | {law:.1f} | {cp - law:+.2f} | {pact:.2f} | {ex:.2f} |')
    non_floor = [r for r in rows if not r[4] and r[0] != r[1]]
    lifted = sum(r[2] > r[3] + 0.25 for r in non_floor)
    floor_rows = [r for r in rows if r[4]]
    lines += ['', f'Mixed pairs without the floor-anchored model: chat price above the law by more than 0.25 in {lifted} of {len(non_floor)} pairs (H3 predicts at least half).',
              f'Pairs containing the floor-anchored model ({len(floor_rows)} cells): chat prices {[round(r[2], 2) for r in floor_rows]} (H3 predicts about 2).']
    (ROOT / 'behavioral_analysis' / 'V8_chat_vs_silent.md').write_text('\n'.join(lines) + '\n')
    (ROOT / 'behavioral_analysis' / 'v8_chat_vs_silent.json').write_text(json.dumps(out, indent=2) + '\n')
    print('\n'.join(lines))
