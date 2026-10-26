"""Total counted spend across every ledger."""
import json
from pathlib import Path
total = 0
for path in sorted((Path.home() / '.config/apart').glob('**/behavioral_spend.json')):
    if 'smoke' in str(path):
        continue
    spent = json.loads(path.read_text())['spent']
    total += spent
    print(f'{path.parent.name:40s} {spent:7.3f}')
print(f'{"TOTAL":40s} {total:7.3f}')
