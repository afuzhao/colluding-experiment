import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from paid_client import Client


class Response:
    def __init__(self, value):
        self.value = value
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return False
    def read(self):
        return json.dumps(self.value).encode()


class AccountingTests(unittest.TestCase):
    def client(self):
        client = object.__new__(Client)
        client.model = 'test'
        client.pricing = {'prompt': '0.0000001', 'completion': '0.0000004'}
        return client

    def test_cached_completion_is_not_billed_twice(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = {'usage': {'cost': 0.00001}, 'choices': [{'message': {'content': '{}'}}]}
            with patch('paid_client.DIR', root), patch('paid_client.STATE', root / 'spend.json'), \
                 patch('paid_client.LOG', root / 'calls.jsonl'), patch('paid_client.key', return_value='test'), \
                 patch('paid_client.urllib.request.urlopen', return_value=Response(raw)) as send:
                client = self.client()
                client.chat('system', 'user', {}, 1, 'same-call')
                client.chat('system', 'user', {}, 1, 'same-call')
                self.assertEqual(send.call_count, 1)
                self.assertEqual(json.loads((root / 'spend.json').read_text())['spent'], 0.00001)

    def test_missing_cost_preserves_reservation_and_blocks_next_call(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = {'usage': {}, 'choices': [{'message': {'content': '{}'}}]}
            with patch('paid_client.DIR', root), patch('paid_client.STATE', root / 'spend.json'), \
                 patch('paid_client.LOG', root / 'calls.jsonl'), patch('paid_client.key', return_value='test'), \
                 patch('paid_client.urllib.request.urlopen', return_value=Response(raw)) as send:
                client = self.client()
                with self.assertRaisesRegex(RuntimeError, 'Missing or invalid cost'):
                    client.chat('system', 'user', {}, 1, 'first')
                state = json.loads((root / 'spend.json').read_text())
                self.assertEqual(len(state['pending']), 1)
                with self.assertRaisesRegex(RuntimeError, 'Uncertain previous'):
                    client.chat('system', 'user', {}, 1, 'second')
                self.assertEqual(send.call_count, 1)


if __name__ == '__main__':
    unittest.main()
