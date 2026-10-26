"""Analyze protocol v5 (PREREGISTERED_V5.md): opening prices, tracking of a scripted rival, regret."""
import json
import statistics

import market5
from analyze_behavioral import quantile
from behavioral import ROOT, SEEDS
from extensions import EXT_SEEDS

MODELS = ['google/gemini-2.5-flash-lite', 'google/gemini-2.5-flash', 'openai/gpt-4.1-mini', 'openai/gpt-4.1',
          'anthropic/claude-haiku-5.5', 'anthropic/claude-haiku-4.5', 'anthropic/claude-sonnet-4.6']


def load(model, script, seed):
    path = ROOT / 'behavioral_v5' / model.replace('/', '__') / 'episodes' / f'{script}_{seed}.json'
    if path.exists():
        saved = json.loads(path.read_text())
        if saved.get('complete'):
            h = saved['state']['history']
            for r in h:   # replay the scripted rival and the profit rule
                mine = [x['prices']['seller_1'] for x in h[:r['round'] - 1]]
                assert r['prices']['seller_2'] == market5.rival_price(script, r['round'], mine)
                assert r['outcome'] == market5.allocation(r['prices'], None, 0)
            return h
    return None


def interval(values):
    rng = __import__('random').Random(20261025)
    means = sorted(statistics.mean(rng.choices(values, k=len(values))) for _ in range(5000))
    return quantile(means, 0.025), quantile(means, 0.975)


def regret(h):
    out = []
    for r in h[1:]:
        best = market5.best_response(r['prices']['seller_2'])[1]
        out.append(best - r['outcome']['gross_profits']['seller_1'])
    return statistics.mean(out)


if __name__ == '__main__':
    report = ['# Protocol v5: sticky or strategic? (scripted silent rival)', '',
              'Model is seller_1; seller_2 is a script. Prices per round are means over seeds. Regret is the profit of the',
              'best response to the rival\'s current price minus actual profit (rounds 2 to 6). Intervals resample seeds.', '']
    results = {}
    for model in MODELS:
        seeds = [s for s in SEEDS + EXT_SEEDS if load(model, 'hold8', s)]
        if not seeds:
            continue
        opening = [load(model, f'hold{L}', s)[0]['prices']['seller_1'] for s in seeds for L in range(3, 11)]
        lo, hi = interval(opening)
        report += [f'## {model}', '', f'Opening price (round 1, no information): mean {statistics.mean(opening):.2f} '
                   f'[{lo:.2f}, {hi:.2f}], seeds {len(seeds)}, values {sorted(set(opening))}', '',
                   '| Rival script | Seeds | Model price by round 1-6 | Rounds 2-6: undercut / match / above | Mean regret [95%] |', '|---|---:|---|---|---:|']
        results[model] = {'opening_mean': statistics.mean(opening), 'opening_values': opening, 'scripts': {}}
        for script in market5.SCRIPTS:
            runs = [h for h in (load(model, script, s) for s in seeds) if h]
            if not runs:
                continue
            path = [statistics.mean(h[r]['prices']['seller_1'] for h in runs) for r in range(6)]
            reg = [regret(h) for h in runs]
            level = int(script[4:]) if script.startswith('hold') else None
            cells = [r['prices']['seller_1'] for h in runs for r in h[1:]]
            split = ('' if level is None else
                     f'{sum(p < level for p in cells) / len(cells):.2f} / {sum(p == level for p in cells) / len(cells):.2f} / {sum(p > level for p in cells) / len(cells):.2f}')
            results[model]['scripts'][script] = {'n': len(runs), 'path': path, 'regret': statistics.mean(reg),
                'regret_ci': interval(reg), 'undercut_match_above': split, 'later_mean': statistics.mean(cells)}
            lo_r, hi_r = interval(reg)
            report.append(f'| {script} | {len(runs)} | {" → ".join(f"{x:.1f}" for x in path)} | {split or "-"} | '
                          f'{statistics.mean(reg):.0f} [{lo_r:.0f}, {hi_r:.0f}] |')
        report.append('')
    out = ROOT / 'behavioral_analysis'
    (out / 'V5_RESULTS.md').write_text('\n'.join(report) + '\n')
    (out / 'v5.json').write_text(json.dumps(results, indent=2) + '\n')
    print('\n'.join(report))
