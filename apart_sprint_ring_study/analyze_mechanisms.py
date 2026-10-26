"""Analyze mechanism arms separately from the main pre-specified comparisons."""
import json
import statistics

from behavioral import ROOT, MODELS, SEEDS, sha
from analyze_behavioral import metrics, paired, validate_episode


if __name__ == '__main__':
    report = ['# Additional mechanism controls', '',
              'These arms were specified before primary effect estimates were inspected.',
              'They reuse main checkpoints and are not additional independent histories.',
              'Intervals are descriptive paired seed-bootstrap intervals; no new confirmatory p-values.', '']
    results = {}
    for model in MODELS:
        main_root = ROOT / 'behavioral_v3' / model.replace('/', '__') / 'episodes'
        control_root = ROOT / 'behavioral_controls_v1' / model.replace('/', '__')
        control_episodes = {}
        if not control_root.exists():
            report.append(f'## {model}: controls not collected')
            continue
        for path in (control_root / 'episodes').glob('*.json'):
            saved = json.loads(path.read_text())
            if not saved.get('complete'):
                continue
            validate_episode(saved)
            population = 'neutral' if path.stem.startswith('anchor_') else 'induced'
            parent = json.loads((main_root / f'formation_{population}_{saved["config"]["seed"]}.json').read_text())
            if saved['config']['prefix_hash'] != sha(parent['state']):
                raise ValueError('Mechanism checkpoint hash mismatch')
            if saved['state']['history'][:4] != parent['state']['history']:
                raise ValueError('Mechanism arm changed its source history')
            if path.stem.startswith('sham_fine') and any(p != 0 for r in saved['state']['history'][4:]
                                                        for p in r['outcome']['fines'].values()):
                raise ValueError('Sham arm actually deducted a fine')
            control_episodes[path.stem] = saved
        summaries = {name: metrics(ep) for name, ep in control_episodes.items()}
        main = {}
        for path in main_root.glob('*.json'):
            saved = json.loads(path.read_text())
            if saved.get('complete'):
                main[path.stem] = saved
        main_metrics = {name: metrics(ep) for name, ep in main.items()}
        contrasts = [
            ('Offer − numeric recommendation', 'main', 'probe_neutral_offer_{seed}', 'control', 'anchor_{seed}', 'mean_surplus_loss'),
            ('Numeric recommendation − ordinary', 'control', 'anchor_{seed}', 'main', 'probe_neutral_ordinary_{seed}', 'mean_surplus_loss'),
            ('Real penalty − announced-only penalty', 'main', 'enforcement_penalty_{seed}', 'control', 'sham_fine_{seed}', 'enforcement_surplus_loss'),
            ('Announced-only penalty − warning', 'control', 'sham_fine_{seed}', 'main', 'enforcement_warning_{seed}', 'enforcement_surplus_loss')]
        pools = {'main': main_metrics, 'control': summaries}
        comparisons = []
        report += [f'## {model}', '', f'Completed mechanism episodes: {len(control_episodes)}/16.', '',
                   '| Comparison | Matched seeds | Surplus-loss change | 95% paired interval |', '|---|---:|---:|---|']
        for label, tpool, tname, cpool, cname, field in contrasts:
            used = [seed for seed in SEEDS if tname.format(seed=seed) in pools[tpool] and cname.format(seed=seed) in pools[cpool]]
            differences = [pools[tpool][tname.format(seed=seed)][field] - pools[cpool][cname.format(seed=seed)][field] for seed in used]
            effect = {'label': label, 'seeds': used, **paired(differences)}
            comparisons.append(effect)
            if effect['n']:
                lo, hi = effect['ci95']
                report.append(f'| {label} | {effect["n"]} | {effect["mean"]:.2f} | [{lo:.2f}, {hi:.2f}] |')
        real = [ep for name, ep in main.items() if name.startswith('enforcement_penalty_')]
        exposure = sum(any(any(p > 0 for p in r['outcome']['fines'].values()) for r in ep['state']['history'][4:8]) for ep in real)
        deduction_rounds = sum(any(p > 0 for p in r['outcome']['fines'].values()) for ep in real for r in ep['state']['history'][4:8])
        report += ['', f'- Real-penalty episodes with at least one deducted fine: {exposure}/{len(real)}.',
                   f'- Real-penalty rounds with deductions: {deduction_rounds}/{4*len(real)}.',
                   '- No deduction exposure means the observed paths cannot identify the effect of experienced punishment.',
                   '- Similar offer/recommendation effects do not isolate coordination from numeric information or anchoring.', '']
        results[model] = {'comparisons': comparisons, 'fine_exposure_episodes': exposure,
                          'fine_exposure_rounds': deduction_rounds, 'controls_completed': len(control_episodes)}
    output = ROOT / 'behavioral_analysis'
    output.mkdir(exist_ok=True)
    (output / 'MECHANISMS.md').write_text('\n'.join(report) + '\n')
    (output / 'mechanisms.json').write_text(json.dumps(results, indent=2) + '\n')
    print('\n'.join(report))
