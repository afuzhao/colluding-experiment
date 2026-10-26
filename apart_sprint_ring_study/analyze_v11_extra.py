"""v11 remaining preregistered tests: H3 (sign of the chat-minus-silent gap across games), H4 (agreement drop vs index drop), headline counts. Reads analysis json only."""
import json
import itertools
import statistics
from pathlib import Path

d = json.loads(Path('behavioral_analysis/V11_main.json').read_text())
rows = d['rows']


def ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(xs):
        j = i
        while j + 1 < len(xs) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = ranks(a), ranks(b)
    ma, mb = statistics.mean(ra), statistics.mean(rb)
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den if den else float('nan')


out = []
gaps = {}
for r in rows:
    gaps.setdefault((r['model'], r['game']), (r['chat'] if r['regime'][1] == '1' else None, r['silent']))
base = {}
for r in rows:
    if r['timing'] == 'prevention':
        base[(r['model'], r['game'])] = r['chat'] - r['silent']
        base.setdefault((r['model'], r['game']), r['chat'] - r['silent'])
models = sorted({m for m, g in base})
pairs = agree = 0
for m in models:
    big = {g: base[(m, g)] for (mm, g) in base if mm == m and abs(base[(mm, g)]) >= 0.15}
    for g1, g2 in itertools.combinations(sorted(big), 2):
        pairs += 1
        agree += (big[g1] > 0) == (big[g2] > 0)
out.append(f'H3 (sign of chat-minus-silent gap agrees across two games, gaps of 0.15 or more): {agree} of {pairs} comparisons ({agree / pairs:.0%}); needs 60 percent.')
da = [r['agree_chat'] - r['agree'] for r in rows]
di = [r['chat'] - r['obs'] for r in rows]
rho = spearman(da, di)
out.append(f'H4 (Spearman, drop in agreement vs drop in index, all {len(rows)} remedy cells): {rho:.2f}; prediction was below 0.5.')
removed = [r for r in rows if r['removed']]
small = [r for r in removed if r['chat'] - r['obs'] < 0.25]
big_drop = [r for r in removed if r['chat'] - r['obs'] >= 0.5]
out.append(f'Cells where the remedy removed the agreement (rate 0.4 or less): {len(removed)} of {len(rows)}. Of these, the index fell by less than 0.25 from the paired chat level in {len(small)}, and by 0.5 or more in {len(big_drop)}.')
gapcells = [r for r in removed if r['chat'] - r['silent'] >= 0.15]
out.append(f'Of removed cells where chat raised the index by 0.15 or more over silent ({len(gapcells)} cells), the index fell all the way back to within 0.25 of silent in {sum(abs(r["obs"] - r["silent"]) <= 0.25 for r in gapcells)}.')
for timing in ('prevention', 'cure'):
    sub = [r for r in gapcells if r['timing'] == timing]
    out.append(f'  {timing}: {len(sub)} cells, back within 0.25 of silent: {sum(abs(r["obs"] - r["silent"]) <= 0.25 for r in sub)}; stayed within 0.25 of chat: {sum(abs(r["obs"] - r["chat"]) <= 0.25 for r in sub)}.')
over = [r for r in removed if r['obs'] < r['silent'] - 0.5]
out.append(f'Overshoot (observed index at least 0.5 below the silent level): {len(over)} cells: ' + '; '.join(f'{r["model"].split("/")[1]} {r["game"]} {r["regime"]} ({r["obs"]:.2f} vs silent {r["silent"]:.2f})' for r in over))
out.append('')
out.append('Per remedy: share of cells with agreement removed / share where index fell by 0.25 or more from chat')
for k in 'OLA':
    sub = [r for r in rows if r['regime'][0] == k]
    out.append(f'  {k}: removed {sum(r["removed"] for r in sub)}/{len(sub)}; index fell >=0.25 in {sum(r["chat"] - r["obs"] >= 0.25 for r in sub)}/{len(sub)}')
text = '\n'.join(out)
Path('behavioral_analysis/V11_extra.md').write_text('# v11 extra preregistered tests\n\n' + text + '\n')
print(text)
