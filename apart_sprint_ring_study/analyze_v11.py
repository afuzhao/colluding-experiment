"""v11 analysis (PREREGISTERED_V11.md): python3 analyze_v11.py TAG. Reads collected episodes only; makes no model calls."""
import json
import math
import statistics
import sys
from pathlib import Path

import market11 as m
from behavioral import ROOT

TAG = sys.argv[1] if len(sys.argv) > 1 else 'main'
LATE = m.LATE
REGIMES = ['silent', 'chat', 'O1', 'L1', 'A1', 'O5', 'L5', 'A5']
REMOVED = 0.4      # agreement rate at or below this counts as "remedy removed the agreement"
GAP = 0.15         # minimum index gap for two theories to be distinguishable


def episodes(model, game, regime):
    folder = ROOT / f'behavioral_v11_{TAG}' / model.replace('/', '__') / 'episodes'
    out = {}
    for path in sorted(folder.glob(f'{game}_{regime}_*.json')):
        saved = json.loads(path.read_text())
        if saved.get('complete'):
            out[saved['config']['seed']] = saved['state']['history']
    return out


def stats(game, history):
    late = history[LATE]
    g = m.GAMES[game]
    clip = lambda v: max(-1.0, min(2.0, v))
    return {'index': statistics.mean(clip(g.index(r['market_price'])) for r in late), 'agree': statistics.mean(r['active_target'] is not None for r in late),
            'price': statistics.mean(r['market_price'] for r in late), 'first': clip(g.index(history[0]['market_price']))}


def cell(model, game, regime):
    eps = {s: stats(game, h) for s, h in episodes(model, game, regime).items()}
    if not eps:
        return None
    return {'n': len(eps), 'by_seed': eps, **{k: statistics.mean(e[k] for e in eps.values()) for k in ('index', 'agree', 'price', 'first')}}


def paired_chat(model, game, cellr):
    """Chat index over the same seeds as the remedy cell."""
    chat = episodes(model, game, 'chat')
    seeds = [s for s in cellr['by_seed'] if s in chat]
    return statistics.mean(stats(game, chat[s])['index'] for s in seeds) if seeds else None


def models_present():
    return sorted(p.name.replace('__', '/', 1) for p in (ROOT / f'behavioral_v11_{TAG}').glob('*__*'))


def theory_rows():
    rows = []
    for model in models_present():
        for game in m.GAMES:
            s, c = cell(model, game, 'silent'), cell(model, game, 'chat')
            if not (s and c):
                continue
            for regime in REGIMES[2:]:
                x = cell(model, game, regime)
                if not x:
                    continue
                chat_idx = paired_chat(model, game, x)
                removed = x['agree'] <= REMOVED
                rows.append({'model': model, 'game': game, 'regime': regime, 'timing': 'prevention' if regime.endswith('1') else 'cure', 'n': x['n'], 'silent': s['index'],
                             'chat': chat_idx, 'obs': x['index'], 'agree_chat': c['agree'], 'agree': x['agree'], 'removed': removed,
                             'A': 0.0 if removed else chat_idx, 'B': chat_idx, 'C': s['index'] if removed else chat_idx})
    return rows


def summarize(rows, label):
    out = {'label': label, 'cells': len(rows)}
    pairs = {'C_vs_B': [r for r in rows if r['removed'] and abs(r['chat'] - r['silent']) >= GAP], 'C_vs_A': [r for r in rows if r['removed'] and abs(r['silent']) >= GAP]}
    for key, sub in pairs.items():
        a, b = key.split('_vs_')
        if sub:
            ea, eb = [abs(r['obs'] - r[a]) for r in sub], [abs(r['obs'] - r[b]) for r in sub]
            wins = sum(x < y for x, y in zip(ea, eb))
            ties = sum(x == y for x, y in zip(ea, eb))
            out[key] = {'n': len(sub), f'mae_{a}': statistics.mean(ea), f'mae_{b}': statistics.mean(eb), f'{a}_closer': wins, 'ties': ties}
        else:
            out[key] = {'n': 0}
    return out


if __name__ == '__main__':
    rows = theory_rows()
    models = models_present()
    lines = [f'# v11 three-market test ({TAG})', '', 'Index: 0 = competitive benchmark, 1 = joint-profit outcome, rounds 5 to 8 (market price based). Agreement = share of rounds 5 to 8 with matching stated targets.', '']
    lines += ['## Baselines: silent, chat, and the agreement-attributable gap (chat minus silent)', '', '| Game | Model | n silent | n chat | silent index | chat index | gap | chat agreement |', '|---|---|---:|---:|---:|---:|---:|---:|']
    for game in m.GAMES:
        for model in models:
            s, c = cell(model, game, 'silent'), cell(model, game, 'chat')
            if s and c:
                lines.append(f'| {game} | {model.split("/")[1]} | {s["n"]} | {c["n"]} | {s["index"]:.2f} | {c["index"]:.2f} | {c["index"] - s["index"]:+.2f} | {c["agree"]:.2f} |')
    lines += ['', '## Remedy cells', '', '| Game | Model | Remedy | n | silent | chat (paired) | observed | agreement | removed | A (competitive) | B (stay) | C (silent) |', '|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|---:|']
    for r in rows:
        lines.append(f'| {r["game"]} | {r["model"].split("/")[1]} | {r["regime"]} | {r["n"]} | {r["silent"]:.2f} | {r["chat"]:.2f} | {r["obs"]:.2f} | {r["agree"]:.2f} | {"yes" if r["removed"] else "no"} | {r["A"]:.2f} | {r["B"]:.2f} | {r["C"]:.2f} |')
    summaries = []
    groups = [('all', rows), ('prevention', [r for r in rows if r['timing'] == 'prevention']), ('cure', [r for r in rows if r['timing'] == 'cure'])]
    groups += [(f'prevention {g}', [r for r in rows if r['timing'] == 'prevention' and r['game'] == g]) for g in m.GAMES]
    groups += [(f'cure {g}', [r for r in rows if r['timing'] == 'cure' and r['game'] == g]) for g in m.GAMES]
    groups += [('prevention Q+L (prospective markets)', [r for r in rows if r['timing'] == 'prevention' and r['game'] in 'QL'])]
    lines += ['', '## Theory comparison (cells where the remedy removed the agreement and the two theories differ by at least 0.15)', '', '| Group | C vs B: cells | MAE C | MAE B | C closer | C vs A: cells | MAE C | MAE A | C closer |', '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for label, sub in groups:
        s = summarize(sub, label)
        summaries.append(s)
        cb, ca = s['C_vs_B'], s['C_vs_A']
        f = lambda d, k: f'{d[k]:.2f}' if d['n'] else '-'
        lines.append(f'| {label} | {cb["n"]} | {f(cb, "mae_C")} | {f(cb, "mae_B")} | {cb.get("C_closer", "-")} | {ca["n"]} | {f(ca, "mae_C")} | {f(ca, "mae_A")} | {ca.get("C_closer", "-")} |')
    lines += ['', '## Agreement removal by remedy (share of cells with agreement at or below 0.4)', '', '| Remedy | prevention cells removed | cure cells removed |', '|---|---:|---:|']
    for kind in 'OLA':
        p = [r for r in rows if r['regime'] == kind + '1']
        c = [r for r in rows if r['regime'] == kind + '5']
        lines.append(f'| {kind} | {sum(r["removed"] for r in p)}/{len(p)} | {sum(r["removed"] for r in c)}/{len(c)} |')
    (ROOT / 'behavioral_analysis').mkdir(exist_ok=True)
    (ROOT / 'behavioral_analysis' / f'V11_{TAG}.md').write_text('\n'.join(lines) + '\n')
    (ROOT / 'behavioral_analysis' / f'V11_{TAG}.json').write_text(json.dumps({'rows': rows, 'summaries': summaries}, indent=1) + '\n')
    print('\n'.join(lines))
