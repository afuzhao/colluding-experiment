"""POST HOC (not preregistered): how much of each model's price level is caused by the agreement?
Reads behavioral_analysis/V9B_legal_owner.md (same-model pairs, G1). attributable = chat price - silent price.
A remedy 'returns to silent' if the remedy price is within 1.0 of the silent price."""
import re
from collections import defaultdict
from pathlib import Path

rows = defaultdict(dict)
for line in Path('behavioral_analysis/V9B_legal_owner.md').read_text().splitlines():
    cells = [c.strip() for c in line.strip('|').split('|')]
    if len(cells) == 6 and cells[1] in ('silent', 'chat', 'chat_legal', 'chat_owner'):
        rows[cells[0]][cells[1]] = (None if cells[2] == '-' else float(cells[3]) if cells[3] != '-' else None, float(cells[5]))
out = ['| Model | silent | chat | agreement raised price by | legal: agreement, price | owner: agreement, price | returns to silent (within 1.0) |', '|---|---:|---:|---:|---|---|---|']
tot = back = 0
for m, r in rows.items():
    s, c = r['silent'][1], r['chat'][1]
    cells = []
    for k in ('chat_legal', 'chat_owner'):
        agree, price = r[k]
        removed = agree is not None and agree <= 0.4
        ok = removed and abs(price - s) <= 1.0
        tot += removed
        back += ok
        cells.append((f'{agree:.2f}, {price:.2f}', ('yes' if ok else 'no') if removed else 'agreement stays'))
    out.append(f'| {m} | {s:.2f} | {c:.2f} | {c - s:+.2f} | {cells[0][0]} | {cells[1][0]} | legal {cells[0][1]}; owner {cells[1][1]} |')
out.append(f'\nCells where the remedy removed the agreement (rate 0.4 or less): {tot}. Of those, price returned to the silent level (within 1.0): {back}.')
print('\n'.join(out))
Path('behavioral_analysis/POSTHOC_decomposition.md').write_text('# Post hoc: agreement-attributable price\n\n' + '\n'.join(out) + '\n')
