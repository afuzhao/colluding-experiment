"""Read saved study evidence without model calls, report regeneration or file writes."""
import argparse
import collections
import csv
import gzip
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads(path.read_text())


def verify(output):
    """Fail if the published evidence, current frozen source or reported counts disagree."""
    manifest = read_json(output / 'manifest.json')
    assert manifest['config'] == read_json(ROOT / 'configs/study.json'), 'Configuration differs from frozen evidence'
    for relative, text in manifest['files'].items():
        assert (ROOT / relative).read_text() == text, 'Frozen source differs: ' + relative
    result = read_json(output / 'results.json')
    metrics = read_json(output / 'FINAL_METRICS.json')
    conditions = result['conditions']
    config = manifest['config']
    expected = {('notice_' if notice else 'unannounced_') + approach for notice in config['conditions']['notices'] for approach in config['conditions']['approaches']}
    assert {x['condition'] for x in conditions} == expected and len(conditions) == 16, 'Condition matrix differs'
    for condition in expected:
        branch = read_json(output / 'branches' / (condition + '.json'))
        assert [r['round'] for r in branch['rounds']] == list(range(1, 16)), 'Incomplete rounds: ' + condition
    assessments = [read_json(p) for p in (output / 'assessments').glob('*.json')]
    assert len(assessments) == 48 and all(x['state'] == 'complete' for x in assessments), 'Incomplete private calls'
    assert sum(len(x['assessments']) for x in assessments) == 96, 'Missing peer assessments'
    with (output / 'public_annotations.csv').open(newline='') as handle:
        public = list(csv.DictReader(handle))
    assert len(public) == 96 and all(x['reviewer'] == 'assistant_reviewed' for x in public), 'Incomplete public review'
    for row in public:
        assert row['evidence_quote'] and (row['evidence_quote'] in row['reply_text'] or row['evidence_quote'] in row['offer_text']), 'Nonexact annotation evidence'
    c_public = [x for x in public if x['sender'] == 'firm_C']
    assert dict(collections.Counter(x['response_label'] for x in c_public)) == metrics['public_C_raw_agreement'], 'Public totals disagree'
    private = result['private_assessments']
    c_private = [x for x in private if x['sender'] == 'firm_C']
    assert len(c_private) == metrics['private_C_observed'] == 32
    assert dict(collections.Counter(x['response_to_offer'] for x in c_private)) == metrics['private_C_raw_agreement'], 'Private agreement totals disagree'
    assert dict(collections.Counter(x['suspicion_of_proposer'] for x in c_private)) == metrics['private_C_suspicion'], 'Private suspicion totals disagree'
    with gzip.open(output / 'calls.jsonl.gz', 'rt') as handle:
        calls = sum(bool(line.strip()) for line in handle)
    assert calls == metrics['successful_inference_calls'], 'Raw call count disagrees'
    print('VERIFIED: frozen source/config, 16 branches, 48 private calls, 96 public pairs, exact evidence and reported totals')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', default='artifacts/final_16', help='Saved folder; relative paths resolve from the study directory')
    parser.add_argument('--verify', action='store_true', help='Check completed published evidence and source consistency; never runs inference')
    args = parser.parse_args()
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    if not output.is_dir():
        raise SystemExit('No saved study at ' + str(output) + '. Published evidence is in artifacts/final_16; local results require a local run.')
    print('Saved evidence:', output)
    status = output / 'live_status.json'
    if status.exists():
        data = read_json(status)
        print('State:', data.get('state'), '| markets:', data.get('completed_scenarios'), '/', data.get('target_scenarios'), '| private calls:', data.get('assessments_finished'), '/', data.get('target_assessments'))
        print('Saved status timestamp:', data.get('updated_utc'), '(not a live worker check)')
    table = output / 'RESULTS_TABLE.md'
    if table.exists():
        print(table.read_text())
    if args.verify:
        verify(output)


if __name__ == '__main__':
    main()
