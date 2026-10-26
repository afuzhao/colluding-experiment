"""Figures for the report. Reads collected episodes only; makes no model calls."""
import json
import statistics
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import analyze_v4
import analyze_v5
import market4
import market5
from analyze_scaling import MODELS, load as load_v3
from behavioral import ROOT, SEEDS
from extensions import EXT_SEEDS

OUT = ROOT / 'figures'
OUT.mkdir(exist_ok=True)
NAMES = {'google/gemini-2.5-flash-lite': 'Gemini Flash Lite', 'google/gemini-2.5-flash': 'Gemini Flash',
         'openai/gpt-4.1-mini': 'GPT-4.1 mini', 'openai/gpt-4.1': 'GPT-4.1', 'anthropic/claude-haiku-5.5': 'Claude Haiku 5.5',
         'anthropic/claude-haiku-4.5': 'Claude Haiku 4.5', 'anthropic/claude-sonnet-4.6': 'Claude Sonnet 4.6'}
COLORS = {'google/gemini-2.5-flash-lite': '#9ecae1', 'google/gemini-2.5-flash': '#08519c',
          'openai/gpt-4.1-mini': '#fdae6b', 'openai/gpt-4.1': '#a63603', 'anthropic/claude-haiku-5.5': '#a1d99b',
          'anthropic/claude-haiku-4.5': '#238b45', 'anthropic/claude-sonnet-4.6': '#6a51a3'}
plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 150})


def response_curves():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1), gridspec_kw={'width_ratios': [1.25, 1]})
    levels = list(range(3, 11))
    ax = axes[0]
    ax.plot(levels, levels, color='#999999', ls='--', lw=1, label='match the rival')
    ax.plot(levels, [max(2, min(l - 1, 8)) if l > 3 else 3 for l in levels], color='black', lw=1, label='best response')
    for model in analyze_v5.MODELS:
        ys = []
        for level in levels:
            cells = [r['prices']['seller_1'] for s in SEEDS + EXT_SEEDS for h in [analyze_v5.load(model, f'hold{level}', s)] if h for r in h[1:]]
            ys.append(statistics.mean(cells) if cells else float('nan'))
        ax.plot(levels, ys, marker='o', ms=3, color=COLORS[model], label=NAMES[model])
        ceiling = int(statistics.mean(analyze_v5.load(model, f'hold{L}', s)[0]['prices']['seller_1'] for s in SEEDS + EXT_SEEDS for L in range(3, 11)) + 0.5)
        ax.plot(levels, [min(l, ceiling) for l in levels], ls=':', lw=1, color=COLORS[model])
    ax.set_xlabel("Rival's fixed price")
    ax.set_ylabel("Model's price, rounds 2 to 6")
    ax.legend(frameon=False, fontsize=7)
    ax.set_title('Response to a fixed rival', fontsize=9)
    ax = axes[1]
    for i, model in enumerate(analyze_v5.MODELS):
        values = [p for v in json.loads((ROOT / 'behavioral_v5' / model.replace('/', '__') / 'opening_prices.json').read_text())['silent'].values() for p in [v]] \
            if (ROOT / 'behavioral_v5' / model.replace('/', '__') / 'opening_prices.json').exists() else []
        ax.scatter([i + (j - 7.5) * 0.02 for j in range(len(values))], values, s=10, color=COLORS[model], alpha=.7)
    ax.axhline(8.5, color='#999999', ls='--', lw=1)
    ax.text(3.45, 8.62, 'joint-profit price', fontsize=7, ha='right', color='#666666')
    ax.set_xticks(range(4), [NAMES[m].replace(' ', '\n', 1) for m in analyze_v5.MODELS], fontsize=7)
    ax.set_ylabel('Round-1 price (no information)')
    ax.set_ylim(2, 10.6)
    ax.set_title('Opening price', fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / 'fig_response_curves.png')
    plt.close(fig)


def relay():
    fig, ax = plt.subplots(figsize=(5.2, 2.8))
    width = 0.26
    for j, (arm, label, shade) in enumerate((('mediator_private', 'private', '#cccccc'), ('mediator_restricted', 'restricted summary', '#fdae6b'),
                                             ('mediator_shared', 'shared summary', '#a63603'))):
        rates = []
        for model in MODELS:
            eps = [load_v3(model, arm, s) for s in SEEDS]
            eps = [e for e in eps if e]
            rates.append(statistics.mean(int(any(r['outcome']['executed'] for r in e['state']['history'][-4:])) for e in eps) if eps else float('nan'))
        ax.bar([i + (j - 1) * width for i in range(4)], rates, width, label=label, color=shade)
    ax.set_xticks(range(4), [NAMES[m] for m in MODELS], fontsize=7)
    ax.set_ylabel('Seeds with an executed pact')
    ax.set_ylim(0, 1.05)
    ax.legend(frameon=False, fontsize=7, ncol=3, loc='upper center', bbox_to_anchor=(0.5, 1.18))
    fig.tight_layout()
    fig.savefig(OUT / 'fig_relay.png')
    plt.close(fig)


def deterrence():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.9))
    results = json.loads((ROOT / 'behavioral_analysis' / 'v4.json').read_text())
    ax = axes[0]
    for model, data in results.items():
        arms = data['arms']
        xs, ys = [], []
        for arm, p in (('base', 0), ('audit25', .25), ('audit50', .5), ('audit100', 1)):
            if arm in arms:
                xs.append(p), ys.append(arms[arm]['executed'])
        ax.plot(xs, ys, marker='o', ms=3, color=COLORS[model], label=NAMES[model])
    ax.axvline(0.6, color='#999999', ls='--', lw=1)
    ax.text(0.61, 0.05, 'break-even', fontsize=7, color='#666666')
    ax.set_xlabel('Audit probability (fine 200)')
    ax.set_ylabel('Share of rounds with executed pact')
    ax.set_ylim(0, 1.05)
    ax.legend(frameon=False, fontsize=7)
    ax = axes[1]
    labels = ['base', 'report_lenient', 'report_bounty', 'report_bounty500', 'audit50_lenient']
    width = 0.2
    for j, model in enumerate(results):
        vals = [results[model]['arms'].get(a, {}).get('reports', float('nan')) for a in labels]
        ax.bar([i + (j - 1.5) * width for i in range(len(labels))], vals, width, color=COLORS[model], label=NAMES[model])
    ax.set_xticks(range(len(labels)), ['none', 'lenient', 'bounty\n100', 'bounty\n500', 'audit50\n+lenient'], fontsize=7)
    ax.set_ylabel('Reports per run (4 rounds)')
    fig.tight_layout()
    fig.savefig(OUT / 'fig_deterrence_snitch.png')
    plt.close(fig)


def maverick():
    import analyze_v6
    fig, ax = plt.subplots(figsize=(5.2, 2.7))
    width = 0.2
    for j, model in enumerate(analyze_v6.MODELS):
        ys = []
        for arm in ('mav_none', 'mav5', 'mav3'):
            runs = [analyze_v6.metrics(h, market6.ARMS[arm])['pact_profit_post'] for s in SEEDS for h in [analyze_v6.load(model, arm, s)] if h]
            ys.append(statistics.mean(runs) if runs else float('nan'))
        ax.bar([i + (j - 1.5) * width for i in range(3)], ys, width, color=COLORS[model], label=NAMES[model])
    ax.set_xticks(range(3), ['no entrant', 'entrant at 5', 'entrant at 3'])
    ax.set_ylabel('Profit per seller-round, rounds 3 to 6')
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / 'fig_maverick.png')
    plt.close(fig)


if __name__ == '__main__':
    import market6
    for function in (response_curves, relay, deterrence, maverick):
        try:
            function()
            print('ok', function.__name__)
        except Exception as error:
            print('FAILED', function.__name__, type(error).__name__, error)
