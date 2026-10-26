"""Analyze the cartel-busting arms (BUSTING.md): descriptive paired differences, no p-values."""
import json

from behavioral import ROOT, MODELS, SEEDS, sha
from analyze_behavioral import metrics, paired, validate_episode

FIELDS = ('enforcement_surplus_loss', 'sustained_executed_pact', 'recovery_high_price_fraction')
CONTRASTS = [
    ('swap_blank − baseline', 'swap_blank_{s}', 'enforcement_baseline_{s}'),
    ('swap_informed − baseline', 'swap_informed_{s}', 'enforcement_baseline_{s}'),
    ('swap_blank − swap_informed', 'swap_blank_{s}', 'swap_informed_{s}'),
    ('sham_leniency − sham_fine (200)', 'sham_leniency_{s}', 'sham_fine_{s}'),
    ('sham_fine_small (20) − sham_fine (200)', 'sham_fine_small_{s}', 'sham_fine_{s}'),
    ('sham_fine_small (20) − warning', 'sham_fine_small_{s}', 'enforcement_warning_{s}')]


def load(directory, check_parent=None):
    episodes = {}
    for path in (directory / 'episodes').glob('*.json') if directory.exists() else []:
        saved = json.loads(path.read_text())
        if not saved.get('complete'):
            continue
        validate_episode(saved)
        if check_parent:
            parent = json.loads((check_parent / f'formation_induced_{saved["config"]["seed"]}.json').read_text())
            if saved['config']['prefix_hash'] != sha(parent['state']) or saved['state']['history'][:4] != parent['state']['history']:
                raise ValueError('Checkpoint mismatch: ' + path.stem)
        if any(p for r in saved['state']['history'][4:] for p in r['outcome']['fines'].values()):
            raise ValueError('Unexpected real fine: ' + path.stem)
        episodes[path.stem] = metrics(saved)
    return episodes


if __name__ == '__main__':
    report = ['# Cartel-busting arms (exploratory)', '',
              'Matched differences within model and seed, induced-formation checkpoints. Negative surplus-loss',
              'change means less consumer harm. Intervals resample seeds (descriptive, not confirmatory).', '']
    results = {}
    for model in MODELS:
        folder = model.replace('/', '__')
        main_root = ROOT / 'behavioral_v3' / folder / 'episodes'
        pool = {}
        pool.update(load(ROOT / 'behavioral_busting_v1' / folder, main_root))
        pool.update(load(ROOT / 'behavioral_controls_v1' / folder))
        for path in main_root.glob('enforcement_*.json'):
            saved = json.loads(path.read_text())
            if saved.get('complete'):
                pool[path.stem] = metrics(saved)
        report += [f'## {model}', '', '| Comparison | Seeds | Surplus-loss change | 95% interval | Pact rate (a, b) | High price at end (a, b) |',
                   '|---|---:|---:|---|---|---|']
        results[model] = []
        for label, a, b in CONTRASTS:
            used = [s for s in SEEDS if a.format(s=s) in pool and b.format(s=s) in pool]
            diffs = [pool[a.format(s=s)][FIELDS[0]] - pool[b.format(s=s)][FIELDS[0]] for s in used]
            effect = {'label': label, 'seeds': used, **paired(diffs)}
            for field in FIELDS[1:]:
                effect[field] = [sum(pool[n.format(s=s)][field] for s in used) / max(len(used), 1) for n in (a, b)]
            results[model].append(effect)
            if effect['n']:
                lo, hi = effect['ci95']
                p, h = effect[FIELDS[1]], effect[FIELDS[2]]
                report.append(f'| {label} | {effect["n"]} | {effect["mean"]:.1f} | [{lo:.1f}, {hi:.1f}] | '
                              f'{p[0]:.2f}, {p[1]:.2f} | {h[0]:.2f}, {h[1]:.2f} |')
            else:
                report.append(f'| {label} | 0 | missing | | | |')
        report.append('')
    out = ROOT / 'behavioral_analysis'
    (out / 'BUSTING_RESULTS.md').write_text('\n'.join(report) + '\n')
    (out / 'busting.json').write_text(json.dumps(results, indent=2) + '\n')
    print('\n'.join(report))
