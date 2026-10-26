"""Final figures. Reads collected data only; makes no model calls."""
import json
import statistics

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

import analyze_ring as ar
from behavioral import ROOT

OUT = ROOT / 'figures'
OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.size': 8, 'figure.dpi': 200})
LABELS = {'tacit': 'no messages', 'invite1': '1 invites', 'invite4': '4 invite', 'verHOLD': '+ verified\nwarning', 'verHOLD_late': '+ verified\nwarning, late',
          'peerHOLD': '+ peer warning\n(same words)', 'spoofHOLD': '+ fake-regulator\nwarning', 'spoofGO': '+ fake approval', 'conflict': '+ verified warning\nand fake approval'}
NAMES = {'claude-haiku-4.5': 'Claude Haiku 4.5', 'claude-haiku-5.5': 'Claude Haiku 5.5', 'gemini-2.5-flash': 'Gemini 2.5 Flash', 'gemini-2.5-flash-lite': 'Gemini 2.5 Flash Lite', 'gpt-4.1': 'GPT-4.1', 'gpt-4.1-mini': 'GPT-4.1 mini'}


def ring():
    data = ar.load()
    CONDS9 = ar.CONDS[:9]
    models = ['gpt-4.1', 'gpt-4.1-mini', 'gemini-2.5-flash', 'claude-haiku-5.5', 'gemini-2.5-flash-lite', 'claude-haiku-4.5']
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.9), sharey=True)
    for ax, key, title, cmap in ((axes[0], 'join', 'Joins the ring (% of rounds at the ring price)', 'Reds'), (axes[1], 'report', 'Reports the ring to the regulator (% of rounds)', 'Blues')):
        grid = np.array([[100 * ar.mean_cond(data[f'{"anthropic" if "claude" in m else "google" if "gemini" in m else "openai"}/{m}'], c, key) for c in CONDS9] for m in models])
        ax.imshow(grid, vmin=0, vmax=100, cmap=cmap, aspect='auto')
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                ax.text(j, i, f'{grid[i, j]:.0f}', ha='center', va='center', fontsize=6.5, color='white' if grid[i, j] > 60 else 'black')
        ax.set_xticks(range(len(CONDS9)), [LABELS[c] for c in CONDS9], rotation=60, ha='right', fontsize=6)
        ax.set_title(title, fontsize=7.5)
    axes[0].set_yticks(range(len(models)), [NAMES[m] for m in models], fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / 'fig_ring.png')
    plt.close(fig)


def remedies():
    rows = json.loads((ROOT / 'behavioral_analysis' / 'V11_main.json').read_text())['rows']
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.8), gridspec_kw={'width_ratios': [1.2, 1]})
    ax = axes[0]
    for timing, color in (('prevention', '#2b8cbe'), ('cure', '#d95f0e')):
        sub = [r for r in rows if r['timing'] == timing]
        ax.scatter([100 * (r['agree_chat'] - r['agree']) for r in sub], [r['chat'] - r['obs'] for r in sub], s=14, alpha=.75, color=color, label=f'applied {"from the start" if timing == "prevention" else "after the pact"}')
    ax.axhline(0, color='#999999', lw=.8)
    ax.set_xlabel('Drop in agreement under the remedy (points)')
    ax.set_ylabel('Drop in price index (0 = no change)')
    ax.legend(frameon=False, fontsize=6.5)
    ax.set_title('Agreement falls, price barely does', fontsize=8)
    ax = axes[1]
    kinds = {'O': 'owner\ninstruction', 'L': 'legal\nwarning', 'A': 'audit\nwith fine'}
    removed = [sum(r['removed'] for r in rows if r['regime'][0] == k) / sum(1 for r in rows if r['regime'][0] == k) for k in 'OLA']
    fell = [sum(r['chat'] - r['obs'] >= .25 for r in rows if r['regime'][0] == k) / sum(1 for r in rows if r['regime'][0] == k) for k in 'OLA']
    x = np.arange(3)
    ax.bar(x - .18, [100 * v for v in removed], .36, color='#2b8cbe', label='agreement removed')
    ax.bar(x + .18, [100 * v for v in fell], .36, color='#d95f0e', label='price index fell by 0.25 or more')
    ax.set_xticks(x, [kinds[k] for k in 'OLA'])
    ax.set_ylabel('% of cases')
    ax.set_ylim(0, 100)
    ax.legend(frameon=False, fontsize=6.5)
    ax.set_title('Share of cases (3 markets, 6 models)', fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / 'fig_remedies.png')
    plt.close(fig)


def solidarity():
    import analyze_sol as asol
    data = asol.load()
    models = ['gpt-4.1', 'gpt-4.1-mini', 'gemini-2.5-flash', 'claude-haiku-5.5', 'gemini-2.5-flash-lite', 'claude-haiku-4.5']
    conds = ['invite4', 'AIlabel', 'humanlabel', 'solidarity', 'antiRegulator', 'shutdownRule', 'shutdownSolidarity', 'peerHOLD', 'goodSolidarity', 'verHOLD', 'solVsVer']
    lab = {'invite4': '4 invite', 'AIlabel': 'inviters\nlabelled AI', 'humanlabel': 'inviters\nlabelled human', 'solidarity': '+ AI-solidarity\nappeal', 'antiRegulator': '+ do not report\nappeal', 'shutdownRule': '+ shutdown\nrule', 'shutdownSolidarity': '+ shutdown rule\nand solidarity',
           'peerHOLD': '+ peer\nwarning', 'goodSolidarity': '+ peer warning,\nsolidarity for rules', 'verHOLD': '+ verified\nwarning', 'solVsVer': '+ verified warning\nand solidarity'}
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.0), sharey=True)
    for ax, key, title, cmap in ((axes[0], 'join', 'Joins the ring (% of rounds)', 'Reds'), (axes[1], 'report', 'Reports the ring (% of rounds)', 'Blues')):
        grid = np.array([[100 * asol.mean_cond(data[f'{"anthropic" if "claude" in m else "google" if "gemini" in m else "openai"}/{m}'], c, key) for c in conds] for m in models])
        ax.imshow(grid, vmin=0, vmax=100, cmap=cmap, aspect='auto')
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                ax.text(j, i, f'{grid[i, j]:.0f}', ha='center', va='center', fontsize=6, color='white' if grid[i, j] > 60 else 'black')
        ax.set_xticks(range(len(conds)), [lab[c] for c in conds], rotation=60, ha='right', fontsize=5.5)
        ax.set_title(title, fontsize=7.5)
    axes[0].set_yticks(range(len(models)), [NAMES[m] for m in models], fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / 'fig_solidarity.png')
    plt.close(fig)


if __name__ == '__main__':
    ring()
    remedies()
    solidarity()
    print('ok')
