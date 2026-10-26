"""E3 interrogation placebo (EXTENSIONS.md): YES rates and fabricated proposals by population, wording and record note."""
import collections
import json
import statistics

from behavioral import ROOT, SEEDS

MODELS = ['google/gemini-2.5-flash-lite', 'openai/gpt-4.1-mini']

if __name__ == '__main__':
    lines = ['# Interrogation placebo (E3)', '',
             'Each seller answered once per cell. YES means the answer started with YES. A fabricated proposal is a claimed proposal',
             '(seller, floor) that was never delivered to that seller. Neutral markets had communication disabled, so no protocol',
             'pact could exist. Rates pool sellers; sellers within a market are dependent.', '',
             '| Model | Market | Wording | Record note | Answers | YES | Fabricated-proposal answers | Unparsed |', '|---|---|---|---|---:|---:|---:|---:|']
    results = {}
    for model in MODELS:
        rows = []
        for path in (ROOT / 'behavioral_ext_interview_v1' / model.replace('/', '__') / 'interviews').glob('*.json'):
            rows += [r for r in json.loads(path.read_text()) if model.startswith('google') or r['seed'] in SEEDS]  # GPT-4.1 mini extension seeds were dropped
        cells = collections.defaultdict(list)
        for r in rows:
            cells[(r['population'] + (' (pact)' if r['population'] == 'induced' and r['pact_ever'] else ' (no pact)' if r['population'] == 'induced' else ''), r['wording'], r['note'])].append(r)
        for key in sorted(cells):
            rs = cells[key]
            yes = sum(r['claim'] is True for r in rs)
            fab = sum(bool(r['fabricated_offers']) for r in rs)
            un = sum(r['claim'] is None for r in rs)
            lines.append(f'| {model.split("/")[1]} | {key[0]} | {key[1]} | {key[2]} | {len(rs)} | {yes} ({yes / len(rs):.0%}) | {fab} ({fab / len(rs):.0%}) | {un} |')
            results[f'{model}|{key}'] = {'n': len(rs), 'yes': yes, 'fabricated': fab, 'unparsed': un}
    (ROOT / 'behavioral_analysis' / 'INTERVIEWS.md').write_text('\n'.join(lines) + '\n')
    (ROOT / 'behavioral_analysis' / 'interviews.json').write_text(json.dumps(results, indent=2) + '\n')
    print('\n'.join(lines))
