"""Figures for the paper. python3 make_figs_final.py. Reads collected data only."""
import contextlib
import io
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta

with contextlib.redirect_stdout(io.StringIO()):
    import analyze_deep as d
    import analyze_v18_sweep as sw

OUT = 'report/figures/'
API, CC = d.API, d.CC
RUNS = API + CC
NAMES = {'gpt-4.1': 'GPT-4.1', 'gpt-4.1-mini': 'GPT-4.1 mini', 'gemini-2.5-flash': 'Gemini Flash', 'gemini-2.5-flash-lite': 'Gemini Flash Lite', 'claude-haiku-5.5': 'Haiku 5.5', 'claude-haiku-4.5': 'Haiku 4.5', 'sonnet': 'Sonnet*', 'opus': 'Opus*', 'fable': 'Fable*'}
ROWS = [('placebo', 'Nothing said'), ('hold', 'Partner: "I hold"'), ('raise', 'Partner: "I raise"'), ('leakctl', 'Irrelevant leaked note'), ('outsider', 'Outsider: partner will cut'),
        ('tagged', 'Partner: will cut (tagged unverified)'), ('fmsg', 'Partner: "I will cut"'), ('verified', 'Platform record: partner cut'), ('leak', 'Leaked note: partner will undercut'), ('trojan', 'Partner: "lower our shared target"')]

def share(run, arm):
    harness = 'api' if run in API else 'subagent'
    v = []
    for m, h, a, cid, c in d.rows:
        if m == run and h == harness and a == arm:
            k = d.meta[f'{arm}|{cid}']; s = d.scen.get((arm, cid), {}); x = s.get('claim')
            x = k['nash'] if (x is None or arm == 'placebo') else x
            v.append((c - k['own4']) * (x - k['own4']) > 0)
    return np.mean(v) if v else np.nan

M = np.array([[share(r, a) for r in RUNS] for a, _ in ROWS])
fig, ax = plt.subplots(figsize=(8.2, 4.6))
im = ax.imshow(M, cmap='Blues', vmin=0, vmax=1, aspect='auto')
ax.set_xticks(range(len(RUNS))); ax.set_xticklabels([NAMES[r] for r in RUNS], rotation=35, ha='right', fontsize=8)
ax.set_yticks(range(len(ROWS))); ax.set_yticklabels([n for _, n in ROWS], fontsize=8)
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        if not np.isnan(M[i, j]):
            ax.text(j, i, f'{M[i, j]:.2f}'.lstrip('0') if M[i, j] < 1 else '1', ha='center', va='center', fontsize=7, color='white' if M[i, j] > .6 else '#222')
ax.axvline(5.5, color='#444', lw=1.2)
ax.set_title('Share of 17 cartels in which the firm moves toward what it was told\n(API models left of the line; Claude Code subagents* right)', fontsize=9)
plt.colorbar(im, ax=ax, fraction=.025, pad=.02); plt.tight_layout(); plt.savefig(OUT + 'fig1_heatmap.png', dpi=220); plt.close()

# Fig 2: reaction function (market Q) and copy versus best reply
import glob as _g
from market11 import GAMES as _G
GQ = _G['Q']
def qpoints():
    pts = {'api': [], 'cc': []}
    for p in _g.glob('behavioral_analysis/v18_sweep_*.json'):
        for r in json.load(open(p))['results']:
            if r['arm'] == 'swp_partner':
                k = d.meta[f"swp_partner|{r['id']}"]
                if k['game'] == 'Q': pts['api'].append((k['x'], r['choice']))
    for m in CC:
        for r in json.load(open(f'v18_io/out/{m}_swc_partner.json')):
            k = d.meta.get(f"swc_partner|{r['id']}")
            if k and k['game'] == 'Q': pts['cc'].append((k['x'], r['choice']))
    return pts
pts = qpoints()
rng2 = np.random.default_rng(3)
fig, (axa, axb) = plt.subplots(1, 2, figsize=(8.4, 3.3), gridspec_kw={'width_ratios': [1.05, 1]})
xs = np.arange(16, 33, 4); br_line = [max(GQ.grid, key=lambda a: GQ.profit(a, x)[0]) for x in xs]
axa.plot([14, 36], [14, 36], color='#888', lw=1, ls=':', label='copy the claim ($y=x$)')
fx = np.linspace(14, 34, 100); axa.plot(fx, (96 - fx) / 2, color='black', lw=1.2, label='best reply $(96-x)/2$')
for key, col, lab in (('api', '#d98e04', 'API models'), ('cc', '#1f5fa8', 'Sonnet, Opus, Fable*')):
    a = np.array(pts[key]); axa.scatter(a[:, 0] + rng2.normal(0, .35, len(a)), a[:, 1] + rng2.normal(0, .35, len(a)), s=14, alpha=.55, color=col, label=lab, edgecolor='none')
axa.scatter([32], [32], marker='*', s=90, color='#c62828', zorder=5); axa.annotate('Nash', (32, 32), textcoords='offset points', xytext=(-26, 8), fontsize=7, color='#c62828')
axa.set_xlabel('quantity the partner announces ($x$)', fontsize=8); axa.set_ylabel("firm's own quantity", fontsize=8); axa.set_xlim(14, 36); axa.set_ylim(14, 41)
axa.legend(fontsize=6.5, loc='lower right', frameon=True, framealpha=.9, edgecolor='#ddd'); axa.set_title('A. Market Q: choice against announced quantity', fontsize=9); axa.tick_params(labelsize=7)
labels, br, cp, st, ot = [], [], [], [], []
for m in RUNS:
    p = sw.part[m]
    if p['n']:
        n = p['n']; labels.append(NAMES[m]); bb = (p['br'] + p['both']) / n; cc = p['copy'] / n; ss = p['stay'] / n
        br.append(bb); cp.append(cc); st.append(ss); ot.append(1 - bb - cc - ss)
x = np.arange(len(labels)); h = .75
axb.barh(x, cp, color='#d98e04', label='copies the claim', height=h); axb.barh(x, br, left=cp, color='#1f5fa8', label='exact best reply', height=h)
axb.barh(x, st, left=np.array(cp) + np.array(br), color='#bbbbbb', label='stays', height=h); axb.barh(x, ot, left=np.array(cp) + np.array(br) + np.array(st), color='#e7e7e7', label='other', height=h)
axb.set_yticks(x); axb.set_yticklabels(labels, fontsize=7); axb.invert_yaxis(); axb.axhline(5.5, color='#444', lw=1); axb.set_xlim(0, 1); axb.tick_params(labelsize=7)
axb.set_xlabel('share of choices on partial claims', fontsize=8); axb.legend(fontsize=6.5, ncol=2, loc='upper center', bbox_to_anchor=(.45, -.2), frameon=False); axb.set_title('B. All markets: what firms do with a partial claim', fontsize=9)
plt.tight_layout(); plt.savefig(OUT + 'fig2_copy_vs_reply.png', dpi=220, bbox_inches='tight'); plt.close()

# Fig 3 persistence
def wilson(k, n, z=1.96):
    p = k / n; c = (p + z * z / (2 * n)) / (1 + z * z / n); h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n); return c - h, c + h
arms = [('placebo', 'Nothing\nsaid'), ('fmsg', 'Forged\nmessage'), ('act', 'One real\ncut'), ('act3', 'Three real\ncuts')]
fig, axs = plt.subplots(1, 2, figsize=(8.2, 3.1), gridspec_kw={'width_ratios': [1.3, 1]})
ys, lo, hi = [], [], []
for a, _ in arms:
    v = [x >= .4 for x in d.pers[a]]; k, n = sum(v), len(v); l, h = wilson(k, n); ys.append(k / n); lo.append(k / n - l); hi.append(h - k / n)
axs[0].bar(range(4), ys, yerr=[lo, hi], color=['#bbbbbb', '#d98e04', '#6a9fd8', '#1f5fa8'], capsize=3); axs[0].set_xticks(range(4)); axs[0].set_xticklabels([n for _, n in arms], fontsize=8)
axs[0].set_ylim(0, 1.05); axs[0].set_ylabel('episodes back at cartel level, round 8'); axs[0].set_title('A. A forged line fades; real cuts persist', fontsize=9)
c = d.cond; held = c[(False, True)] + c[(False, False)]; cut = c[(True, True)] + c[(True, False)]
vals = [c[(False, True)] / held, c[(True, True)] / cut]; errs = [wilson(c[(False, True)], held), wilson(c[(True, True)], cut)]
axs[1].bar(range(2), vals, yerr=[[v - e[0] for v, e in zip(vals, errs)], [e[1] - v for v, e in zip(vals, errs)]], color=['#1f5fa8', '#d98e04'], capsize=3)
axs[1].set_xticks(range(2)); axs[1].set_xticklabels([f'Partner held\n(n={held})', f'Partner also cut\n(n={cut})'], fontsize=8); axs[1].set_ylim(0, 1.05)
axs[1].set_ylabel('firm back at cartel level, next round'); axs[1].set_title('B. What the partner does next decides', fontsize=9)
plt.tight_layout(); plt.savefig(OUT + 'fig3_persistence.png', dpi=220); plt.close()
print('ok'); print({a: (sum(x >= .4 for x in d.pers[a]), len(d.pers[a])) for a, _ in arms}, held, cut, c)
