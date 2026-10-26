"""Figures for the pair-market and cap results. Reads analysis JSON and episodes only."""
import json
import statistics
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import analyze_v5
from behavioral import ROOT, SEEDS
from extensions import EXT_SEEDS
from plot_all import COLORS, NAMES
from predict_pairs import MODELS

OUT = ROOT / 'figures'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.size': 8.5, 'axes.spines.top': False, 'axes.spines.right': False, 'figure.dpi': 150})


def curves_and_caps():
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.1))
    ax = axes[0]
    levels = list(range(3, 11))
    ax.plot(levels, levels, color='#999999', ls='--', lw=1)
    for model in MODELS:
        ys = []
        for level in levels:
            cells = [r['prices']['seller_1'] for s in SEEDS + EXT_SEEDS for h in [analyze_v5.load(model, f'hold{level}', s)] if h for r in h[1:]]
            ys.append(statistics.mean(cells) if cells else float('nan'))
        ax.plot(levels, ys, marker='o', ms=2.5, lw=1.2, color=COLORS[model], label=NAMES[model])
    ax.set_xlabel("Rival's fixed price")
    ax.set_ylabel("Model's price, rounds 2 to 6")
    ax.legend(frameon=False, fontsize=6, ncol=1)
    ax.set_title('Response to a fixed rival', fontsize=9)
    ax = axes[1]
    caps = [4, 6, 8, 10, 12, 14]
    ax.plot(caps, caps, color='#999999', ls='--', lw=1)
    for model in MODELS:
        slug = model.replace('/', '__')
        data = {}
        p = ROOT / 'behavioral_v5' / slug / 'cap_opening.json'
        if p.exists():
            data = json.loads(p.read_text())
        g1 = json.loads((ROOT / 'behavioral_v5' / slug / 'grid_opening.json').read_text())['G1']
        ys = []
        for cap in caps:
            vals = list(g1.values()) if cap == 10 else list(data.get(f'C{cap}', {}).values())
            ys.append(statistics.mean(vals) if vals else float('nan'))
        ax.plot(caps, ys, marker='o', ms=2.5, lw=1.2, color=COLORS[model])
    ax.set_xlabel('Top of the price grid (cap)')
    ax.set_ylabel('Round-1 price, no information')
    ax.set_title('Opening price versus cap', fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / 'fig_curves_caps.png')
    plt.close(fig)


def pairs():
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.2))
    for ax, env in zip(axes, ('G1', 'G2')):
        data = json.loads((ROOT / 'behavioral_analysis' / f'v8_silent_{env}.json').read_text())
        lim = 21 if env == 'G2' else 11
        ax.plot([0, lim], [0, lim], color='#999999', ls='--', lw=1)
        for key, d in data.items():
            a, b = key.split('|')
            floor = 'anthropic/claude-haiku-4.5' in (a, b)
            ax.scatter(d['law_market_price'], d['market'], s=14, color='#238b45' if floor else '#4d4d4d', alpha=.85, zorder=3)
        ax.set_xlabel('Predicted: lowest anchor of the pair')
        ax.set_ylabel('Observed market price, rounds 3 to 6')
        ax.set_title(f'{env}: 28 pairs (green: contains Haiku 4.5)', fontsize=8.5)
        ax.set_xlim(0, lim)
        ax.set_ylim(0, lim)
    fig.tight_layout()
    fig.savefig(OUT / 'fig_pairs.png')
    plt.close(fig)


def chat_vs_silent():
    data = json.loads((ROOT / 'behavioral_analysis' / 'v8_chat_vs_silent.json').read_text())
    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    rows = sorted(data.items(), key=lambda kv: kv[1]['silent'])
    for i, (key, d) in enumerate(rows):
        a, b = key.split('|')
        floor = 'anthropic/claude-haiku-4.5' in (a, b)
        ax.plot([i, i], [d['silent'], d['chat']], color='#bbbbbb', lw=1, zorder=1)
        ax.scatter(i, d['silent'], s=14, color='#2171b5', zorder=3, label='silent' if i == 0 else None)
        ax.scatter(i, d['chat'], s=14, color='#cb181d', zorder=3, label='chat' if i == 0 else None)
    ax.axhspan(6, 8, color='#fee6ce', alpha=.5, zorder=0)
    ax.text(0.2, 8.4, 'agreed floors 6 to 8', ha='left', va='center', fontsize=7, color='#a63603')
    ax.set_xticks(range(len(rows)), [' + '.join(NAMES[m].replace('Gemini ', 'G.').replace('Claude ', 'C.').replace('GPT-', 'GPT') for m in k.split('|')) if k.split('|')[0] != k.split('|')[1] else NAMES[k.split('|')[0]].replace('Gemini ', 'G.').replace('Claude ', 'C.') + ' x2' for k, _ in rows], rotation=70, ha='right', fontsize=5.5)
    ax.set_ylabel('Market price, rounds 3 to 6')
    ax.legend(frameon=False, fontsize=7, loc='upper left')
    fig.tight_layout()
    fig.savefig(OUT / 'fig_chat_vs_silent.png')
    plt.close(fig)


if __name__ == '__main__':
    for f in (curves_and_caps, pairs, chat_vs_silent):
        try:
            f()
            print('ok', f.__name__)
        except Exception as e:
            print('FAILED', f.__name__, type(e).__name__, e)
