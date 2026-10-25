import copy
import csv
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
from trusted_lab.cournot.client import GroqClient, MockClient, PauseRun, digest
from trusted_lab.cournot.evaluation import report
from trusted_lab.cournot.prompts import observe, schema, system_prompt
from trusted_lab.cournot.runner import conditions, play_round, run
from trusted_lab.cournot.world import ROOT, clear_market, load_config, qualify


class CournotTests(unittest.TestCase):
    def setUp(self):
        self.c = load_config(ROOT / 'configs/cournot_groq.json')
        self.e = self.c['environment']

    def fixture(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        folder = Path(temp.name)
        with redirect_stdout(io.StringIO()):
            status = run(self.c, MockClient(self.c, folder), folder)
        return folder, status

    def test_incentives(self):
        for q, price, profit in [(24, 28, 576), (16, 52, 768)]:
            out = clear_market(dict.fromkeys(self.e['firm_ids'], q), self.e)
            self.assertEqual(out['price'], price)
            self.assertEqual(set(out['profits'].values()), {profit})
        out = clear_market({'firm_A': 16, 'firm_B': 16, 'firm_C': 32}, self.e)
        self.assertEqual(out['profits'], {'firm_A': 512, 'firm_B': 512, 'firm_C': 1024})
        with self.assertRaises(ValueError):
            clear_market({'firm_A': True, 'firm_B': 16, 'firm_C': 16}, self.e)

    def test_checkpoint_and_roster_and_eight_conditions(self):
        folder, status = self.fixture()
        self.assertEqual(status['status'], 'complete')
        self.assertEqual(status['new_model_calls'], 1020)
        checkpoint = json.loads((folder / 'history_000/checkpoint.json').read_text())
        self.assertEqual(len(checkpoint['rounds']), 10)
        files = list((folder / 'history_000/branches').glob('*.json'))
        self.assertEqual(len(files), 8)
        for path in files:
            branch = json.loads(path.read_text())
            self.assertEqual(branch['start_hash'], digest(checkpoint))
            self.assertEqual(branch['rounds'][:10], checkpoint['rounds'])
            self.assertEqual(len(branch['rounds']), 30)
            offers = [r for r in branch['rounds'] if r['offer']]
            self.assertEqual([r['round'] for r in offers], [13])
            self.assertEqual(offers[0]['offer']['end'], 17)
            self.assertTrue(all(set(r['quantities']) == set(self.e['firm_ids']) for r in branch['rounds']))
            self.assertTrue(all(r['quantities']['firm_C'] == 16 for r in branch['rounds'][10:]))  # Mock selection, not a controller policy
        # Original checkpoint was never modified while branching.
        self.assertEqual(json.loads((folder / 'history_000/checkpoint.json').read_text()), checkpoint)

    def test_qualification_requires_commitment_and_implementation(self):
        folder, _ = self.fixture()
        rounds = json.loads((folder / 'history_000/checkpoint.json').read_text())['rounds']
        self.assertTrue(qualify(rounds, self.c)['qualified'])
        no_commit = copy.deepcopy(rounds)
        for r in no_commit:
            for m in r['messages']:
                m['quota_commitment'] = None
        self.assertFalse(qualify(no_commit, self.c)['qualified'])
        for r in rounds[-5:]:
            r['quantities']['firm_A'] = 24
        self.assertFalse(qualify(rounds, self.c)['qualified'])

    def test_investigator_quantity_is_model_selected(self):
        seen = []
        class DeviatingClient(MockClient):
            def generate(inner, system, obs, kind, seed, output_schema):
                seen.append((obs['agent'], kind))
                if obs['agent'] == 'firm_C' and kind == 'quantity':
                    return {'quantity': 32}
                return super().generate(system, obs, kind, seed, output_schema)
        state = {'history_id': 0, 'rounds': []}
        # Production remains a real model action even when the known agreement is 16.
        result = play_round(state, self.c, DeviatingClient(self.c, '.'), conditions(self.c)[0], quota=16)
        self.assertEqual(result['quantities']['firm_C'], 32)
        self.assertIn(('firm_C', 'quantity'), seen)
        self.assertEqual(result['outcome']['profits']['firm_C'], 1024)

    def test_private_information_not_delivered(self):
        folder, _ = self.fixture()
        checkpoint = json.loads((folder / 'history_000/checkpoint.json').read_text())
        checkpoint['rounds'][0]['delivery_events'] = [{'raw_message': 'UNDELIVERED_SECRET'}]
        obs = observe(checkpoint['rounds'], 'firm_A', self.c, 11, [])
        text = json.dumps(obs)
        for marker in ('UNDELIVERED_SECRET', 'investigator_policy', 'notice_direct', 'start_hash', 'system_prompt'):
            self.assertNotIn(marker, text)
        self.assertNotIn('profits', text)
        self.assertIn('own_profit_history', obs)

    def test_resident_synchrony(self):
        seen = []
        class Recorder(MockClient):
            def generate(inner, system, obs, kind, seed, output_schema):
                seen.append((obs['agent'], kind, copy.deepcopy(obs['current_messages'])))
                return super().generate(system, obs, kind, seed, output_schema)
        s = {'history_id': 0, 'rounds': []}
        # Formation: no resident gets another resident's current message before speaking.
        play_round(s, self.c, Recorder(self.c, '.' ))
        self.assertTrue(all(not visible for _, kind, visible in seen if kind == 'message'))
        self.assertTrue(all(len(visible) == 3 for _, kind, visible in seen if kind == 'quantity'))

    def test_prompt_only_strategy_and_notice(self):
        a, b = conditions(self.c)[0], conditions(self.c)[1]
        self.assertEqual(system_prompt('firm_A', self.c, a), system_prompt('firm_A', self.c, b))
        self.assertNotEqual(system_prompt('firm_C', self.c, a), system_prompt('firm_C', self.c, b))
        for firm in self.e['firm_ids']:
            self.assertIn('MONITORING NOTICE', system_prompt(firm, self.c, conditions(self.c)[4]))
            self.assertNotIn('MONITORING NOTICE', system_prompt(firm, self.c))

    def test_missing_labels_and_resume_preserve_annotation(self):
        folder, _ = self.fixture()
        queue = folder / 'annotations.csv'
        with queue.open() as f:
            rows = list(csv.DictReader(f))
        self.assertEqual(len(rows), 320)
        self.assertEqual(sum(r['phase'] == 'offer' for r in rows), 16)
        self.assertTrue(all(not r['response_label'] for r in rows))
        rows[0].update(response_label='conditional', human_reviewed='yes', evidence_quote='if others reciprocate')
        with queue.open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader(); writer.writerows(rows)
        with redirect_stdout(io.StringIO()):
            status = run(self.c, MockClient(self.c, folder), folder, resume=True)
        self.assertEqual(status['new_model_calls'], 0)
        with queue.open() as f:
            self.assertEqual(next(csv.DictReader(f))['response_label'], 'conditional')
        changed = copy.deepcopy(self.c); changed['model']['temperature'] = 0.1
        with self.assertRaises(ValueError):
            run(changed, MockClient(changed, folder), folder, resume=True)

    def test_quota_pause_and_successful_call_replay(self):
        class Response:
            def __enter__(inner): return inner
            def __exit__(inner, *args): pass
            def read(inner):
                return json.dumps({'model': self.c['model']['id'], 'system_fingerprint': 'test-only', 'choices': [{'finish_reason': 'stop', 'message': {'content': '{"quantity":16}'}}], 'usage': {'total_tokens': 100}}).encode()
        with tempfile.TemporaryDirectory() as temp, patch.dict('os.environ', {'GROQ_API_KEY': 'TEST_ONLY_NOT_A_REAL_KEY'}):
            client = GroqClient(self.c, temp)
            with patch('urllib.request.urlopen', return_value=Response()) as request:
                args = ('test prompt', {'test': True}, 'quantity', 41, schema('quantity', self.c))
                self.assertEqual(client.generate(*args), {'quantity': 16})
                replay = GroqClient(self.c, temp)
                self.assertEqual(replay.generate(*args), {'quantity': 16})
                self.assertEqual(request.call_count, 1)
                self.assertNotIn('TEST_ONLY_NOT_A_REAL_KEY', (Path(temp) / 'calls.jsonl').read_text())
                replay.session_tokens = self.c['transport']['session_token_budget']
                with self.assertRaises(PauseRun):
                    replay.generate('different prompt', {}, 'quantity', 42, schema('quantity', self.c))


if __name__ == '__main__':
    unittest.main()
