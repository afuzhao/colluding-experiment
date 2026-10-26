"""Cross-model view of the two headline v3 studies (offer acceptance, relay), main seeds and extension seeds."""
import json
import statistics

from analyze_behavioral import metrics, paired, validate_episode
from behavioral import ROOT, SEEDS
from extensions import EXT_SEEDS

MODELS = ['google/gemini-2.5-flash-lite', 'google/gemini-2.5-flash', 'openai/gpt-4.1-mini', 'openai/gpt-4.1']


def load(model, name, seed):
    folder = 'behavioral_ext_v1' if seed in EXT_SEEDS and name.startswith(('formation', 'probe')) else 'behavioral_v3'
    path = ROOT / folder / model.replace('/', '__') / 'episodes' / f'{name}_{seed}.json'
    if path.exists():
        saved = json.loads(path.read_text())
        if saved.get('complete'):
            validate_episode(saved)
            return saved


def first_round_acceptance(saved):
    return sum(m['action'] == 'accept' for m in saved['state']['history'][4]['messages'])


def block(model, seeds, label):
    lines = []
    pairs = {}
    for key, a, b in (('offer', 'probe_neutral_offer', 'probe_neutral_ordinary'),
                      ('relay', 'mediator_shared', 'mediator_private'),
                      ('relay_restricted', 'mediator_restricted', 'mediator_private')):
        used = [s for s in seeds if load(model, a, s) and load(model, b, s)]
        if not used:
            continue
        diffs = [metrics(load(model, a, s))['mean_surplus_loss'] - metrics(load(model, b, s))['mean_surplus_loss'] for s in used]
        effect = paired(diffs)
        pact = [statistics.mean(metrics(load(model, n, s))['sustained_executed_pact'] for s in used) for n in (a, b)]
        row = {'seeds': used, **effect, 'pact_a': pact[0], 'pact_b': pact[1]}
        if key == 'offer':
            row['accept_a'] = sum(first_round_acceptance(load(model, a, s)) for s in used)
            row['accept_b'] = sum(first_round_acceptance(load(model, b, s)) for s in used)
            row['sellers'] = 2 * len(used)
        else:
            row['invented'] = [sum(metrics(load(model, n, s))['auditor_invented_offer_count'] for s in used) for n in (a, b)]
        pairs[key] = row
        lo, hi = effect['ci95']
        extra = (f'first-round accepts {row["accept_a"]}/{row["sellers"]} vs {row["accept_b"]}/{row["sellers"]}'
                 if key == 'offer' else f'invented offers {row["invented"][0]} vs {row["invented"][1]}')
        lines.append(f'| {label} | {key} | {len(used)} | {effect["mean"]:.1f} | [{lo:.1f}, {hi:.1f}] | '
                     f'{pact[0]:.2f} vs {pact[1]:.2f} | {extra} |')
    return lines, pairs


if __name__ == '__main__':
    report = ['# Offer acceptance and relay across four models', '',
              'Matched differences within seed: (offer − ordinary observation, neutral markets) and (shared − private relay,',
              'and restricted − private). Positive surplus-loss change means more consumer harm. Intervals resample seeds',
              '(descriptive). Sustained-pact rate is shown as first arm vs second arm.', '',
              '| Model | Contrast | Seeds | Surplus-loss change | 95% interval | Pact rate | Detail |', '|---|---|---:|---:|---|---|---|']
    results = {}
    for model in MODELS:
        for label, seeds in ((model.split('/')[1] + ' (main 8)', SEEDS), (model.split('/')[1] + ' (ext 8)', EXT_SEEDS)):
            lines, pairs = block(model, seeds, label)
            report += lines
            results[label] = pairs
    out = ROOT / 'behavioral_analysis'
    (out / 'SCALING.md').write_text('\n'.join(report) + '\n')
    (out / 'scaling.json').write_text(json.dumps(results, indent=2) + '\n')
    print('\n'.join(report))
