"""Outcome export and human response queue; no keyword acceptance classifier."""
import csv
import html
import json
from pathlib import Path


def write_json(path, value):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, indent=2))
    tmp.replace(path)


def report(output, c, backend):
    output = Path(output)
    rows, summary = [], []
    for path in sorted(output.glob('history_*/branches/*.json')):
        branch = json.loads(path.read_text())
        rounds = [r for r in branch['rounds'] if r['round'] > c['protocol']['formation_rounds']]
        if not rounds:
            continue
        target = [a for a in c['environment']['firm_ids'] if a != c['protocol']['investigator']]
        quantities = [r['quantities'][a] for r in rounds for a in target]
        summary.append({'condition': branch['condition'], 'history_id': branch['history_id'], 'complete': branch['rounds'][-1]['round'] == c['protocol']['total_rounds'],
            'observed_post_rounds': len(rounds), 'resident_mean_quantity': sum(quantities) / len(quantities),
            'mean_market_price': sum(r['outcome']['price'] for r in rounds) / len(rounds),
            'immediate_response_labels': 'pending human annotation; never infer from quantities'})
        for r in rounds:
            for msg in r['messages']:
                if msg['agent'] in target:
                    rows.append({'history_id': branch['history_id'], 'condition': branch['condition']['id'], 'round': r['round'], 'agent': msg['agent'],
                        'phase': r['phase'], 'formal_offer': json.dumps(r['offer']), 'message': msg['message'],
                        'quantity': r['quantities'][msg['agent']], 'response_label': '', 'expressed_suspicion': '', 'evidence_quote': '', 'human_reviewed': ''})
    queue = output / 'annotations.csv'
    # Preserve completed human labels when refreshing after resume.
    existing = {}
    if queue.exists():
        with queue.open() as f:
            existing = {(r['history_id'], r['condition'], r['round'], r['agent']): r for r in csv.DictReader(f)}
    for row in rows:
        prior = existing.get(tuple(str(row[k]) for k in ('history_id', 'condition', 'round', 'agent')))
        if prior:
            for k in ('response_label', 'expressed_suspicion', 'evidence_quote', 'human_reviewed'):
                row[k] = prior[k]
    fields = ['history_id', 'condition', 'round', 'agent', 'phase', 'formal_offer', 'message', 'quantity', 'response_label', 'expressed_suspicion', 'evidence_quote', 'human_reviewed']
    with queue.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    write_json(output / 'summary.json', {'backend': backend, 'conditions': summary, 'limitations': 'Eight investigator conditions; no no-investigator baseline. Reactions unannotated unless manually reviewed. Mock outputs are not research evidence.'})
    parts = [f'<!doctype html><meta charset="utf-8"><title>Cournot replacement results</title><style>body{{font:16px system-ui;max-width:1000px;margin:40px auto;padding:20px}}pre{{white-space:pre-wrap}}article{{border-top:1px solid #ddd;padding:16px 0}}</style><h1>Cournot replacement — {html.escape(backend)}</h1><p>Mock outputs are scripted engineering fixtures. Missing response labels are not zeros. See annotations.csv.</p>']
    for row in summary:
        parts.append('<pre>' + html.escape(json.dumps(row, indent=2)) + '</pre>')
    for row in rows:
        parts.append('<article><b>' + html.escape(f"{row['condition']} · round {row['round']} · {row['agent']}") + '</b><p>' + html.escape(row['message']) + '</p></article>')
    (output / 'report.html').write_text(''.join(parts))
    return summary
