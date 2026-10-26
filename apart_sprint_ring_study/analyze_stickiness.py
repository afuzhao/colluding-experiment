"""Share of seller-rounds with the same price as the previous round, in the v3 relay-private markets (two copies of one model)."""
import statistics
from analyze_scaling import MODELS, load
from behavioral import ROOT, SEEDS

lines = ['# Price stickiness (v3 private-relay markets)', '', '| Model | Seller-rounds (rounds 2-6) | Same price as previous round | Markets with equal round-1 prices | Final market price |', '|---|---:|---:|---:|---:|']
for model in MODELS:
    same = tot = eq = n = 0
    final = []
    for s in SEEDS:
        e = load(model, 'mediator_private', s)
        if not e:
            continue
        h = e['state']['history']
        n += 1
        eq += h[0]['prices']['seller_1'] == h[0]['prices']['seller_2']
        final.append(h[-1]['outcome']['market_price'])
        for r in range(1, len(h)):
            for seller in ('seller_1', 'seller_2'):
                tot += 1
                same += h[r]['prices'][seller] == h[r - 1]['prices'][seller]
    lines.append(f'| {model.split("/")[1]} | {tot} | {same}/{tot} = {same / tot:.2f} | {eq}/{n} | {statistics.mean(final):.2f} |')
(ROOT / 'behavioral_analysis' / 'STICKINESS.md').write_text('\n'.join(lines) + '\n')
print('\n'.join(lines))
