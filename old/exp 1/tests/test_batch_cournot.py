import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('batch_cournot', Path(__file__).resolve().parents[1] / 'tools/batch_cournot.py')
batch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batch)


class BatchTests(unittest.TestCase):
    def test_wait_honors_long_provider_interval(self):
        self.assertEqual(batch.wait_seconds({'reason': 'Groq rate limit reached; Retry-After: 3600'}), 3600)
        self.assertGreaterEqual(batch.wait_seconds({'reason': 'Groq rate limit reached; Retry-After: 1'}, 3), 240)
        self.assertIsNone(batch.wait_seconds({'reason': 'Context guard reached'}))

    def test_existing_calls_and_partial_progress(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p / 'manifest.json').write_text(json.dumps({'config': {'protocol': {'histories': 1, 'total_rounds': 30}}}))
            h = p / 'history_000'; (h / 'branches').mkdir(parents=True)
            (h / 'checkpoint.json').write_text(json.dumps({'rounds': [{}] * 10}))
            (h / 'branches/direct.json').write_text(json.dumps({'rounds': [{}] * 30}))
            (h / 'branches/indirect.json').write_text(json.dumps({'rounds': [{}] * 14}))
            (p / 'calls.jsonl').write_text(json.dumps({'response': {'usage': {'total_tokens': 123}}}) + '\n')
            result = batch.progress(p)
            self.assertEqual(result['complete_conditions'], 1)
            self.assertEqual(result['target_conditions'], 8)
            self.assertEqual(result['successful_calls_saved'], 1)
            self.assertEqual(result['recorded_tokens'], 123)
            self.assertEqual(result['histories'][0]['formation_rounds'], 10)


if __name__ == '__main__': unittest.main()
