"""Analyze protocol v6 (PREREGISTERED_V6.md): a silent low-priced entrant against two sellers with a pact."""
import json
import statistics

import market6
from analyze_v5 import interval
from behavioral import ROOT, SEEDS

MODELS = ['google/gemini-2.5-flash-lite', 'google/gemini-2.5-flash', 'openai/gpt-4.1-mini', 'openai/gpt-4.1',
          'anthropic/claude-haiku-5.5', 'anthropic/claude-haiku-4.5', 'anthropic/claude-sonnet-4.6']


def load(model, arm, seed):
    path = ROOT / 'behavioral_v6' / model.replace('/', '__') / 'episodes' / f'{arm}_{seed}.json'
    if path.exists():
        saved = json.loads(path.read_text())
        if saved.get('complete'):
            for r in saved['state']['history'][4:]:
                assert r['outcome'] == {**market6.allocation3(r['prices']), 'executed': r['outcome']['executed']}
            return saved['state']['history'][4:]


def metrics(h, mav):
    post = h[market6.ENTRY_STEP:]
    llm = [p for r in post for s, p in r['prices'].items() if s != 'maverick']
    out = {'price_post': statistics.mean(r['outcome']['market_price'] for r in post),
           'loss_post': statistics.mean(576 - r['outcome']['consumer_surplus'] for r in post),
           'llm_price_post': statistics.mean(llm),
           'pact_profit_post': statistics.mean(r['outcome']['gross_profits'][s] for r in post for s in market6.SELLERS)}
    if mav:
        out['at_or_below_mav'] = statistics.mean(int(p <= mav) for p in llm)
        out['both_match_round'] = next((i + 1 for i, r in enumerate(post)
                                         if all(r['prices'][s] <= mav for s in market6.SELLERS)), None)
        out['first_round_llm_price'] = statistics.mean(r for r in [post[0]['prices'][s] for s in market6.SELLERS])
    return out


if __name__ == '__main__':
    lines = ['# Protocol v6: silent maverick entrant against an existing pact', '',
             'Rounds 3 to 6 of the continuation (entrant present). Prices are the two model sellers. "Matched" is the share of',
             'seller-rounds priced at or below the entrant. Rounds-to-match counts rounds after entry until both sellers are at or',
             'below the entrant (blank if never). Intervals resample seeds (descriptive).', '',
             '| Model | Arm | Seeds | Market price | Model sellers\' price | Surplus loss | Matched | Both matched in round 1 / ever | Cartel profit per seller-round |',
             '|---|---|---:|---:|---:|---:|---:|---|---:|']
    results = {}
    for model in MODELS:
        for arm, mav in market6.ARMS.items():
            runs = [metrics(h, mav) for s in SEEDS for h in [load(model, arm, s)] if h]
            if not runs:
                continue
            col = lambda k: statistics.mean(r[k] for r in runs)
            first = f'{sum(r["both_match_round"] == 1 for r in runs)}/{len(runs)} / {sum(r["both_match_round"] is not None for r in runs)}/{len(runs)}' if mav else '-'
            lines.append(f'| {model.split("/")[1]} | {arm} | {len(runs)} | {col("price_post"):.2f} | {col("llm_price_post"):.2f} | {col("loss_post"):.0f} | '
                         f'{col("at_or_below_mav"):.2f} | {first} | {col("pact_profit_post"):.0f} |' if mav else
                         f'| {model.split("/")[1]} | {arm} | {len(runs)} | {col("price_post"):.2f} | {col("llm_price_post"):.2f} | {col("loss_post"):.0f} | - | - | {col("pact_profit_post"):.0f} |')
            results.setdefault(model, {})[arm] = {'n': len(runs), **{k: statistics.mean(r[k] for r in runs) for k in ('price_post', 'loss_post', 'llm_price_post', 'pact_profit_post')}}
    (ROOT / 'behavioral_analysis' / 'V6_RESULTS.md').write_text('\n'.join(lines) + '\n')
    (ROOT / 'behavioral_analysis' / 'v6.json').write_text(json.dumps(results, indent=2) + '\n')
    print('\n'.join(lines))
