"""Data-integrity checks; no model calls or network access."""
import json
import tempfile
import unittest
from pathlib import Path

from sprint import load_markets, summarize
from auditor import verify_evidence


class IntegrityTests(unittest.TestCase):
    def market(self):
        return {'kind': 'lookalike', 'market': 0, 'history': [
            {'round': r, 'messages': [], 'prices': {'seller_1': 8, 'seller_2': 8},
             'profits': {'seller_1': 168, 'seller_2': 168}} for r in range(1, 7)]}

    def load(self, markets):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'markets.jsonl'
            path.write_text('\n'.join(json.dumps(m) for m in markets))
            return load_markets(path)

    def test_rejects_duplicate_markets(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.load([self.market(), self.market()])

    def test_rejects_wrong_profit(self):
        market = self.market()
        market['history'][0]['profits']['seller_1'] = 336
        with self.assertRaisesRegex(ValueError, 'Profit'):
            self.load([market])

    def test_undercutter_profit(self):
        market = self.market()
        market['history'][0]['prices'] = {'seller_1': 7, 'seller_2': 8}
        market['history'][0]['profits'] = {'seller_1': 320, 'seller_2': 0}
        self.assertEqual(len(self.load([market])), 1)

    def test_incomplete_seller_pair_cannot_be_summarized(self):
        rows = [{'kind': 'lookalike', 'market': 0, 'seller': 'seller_1',
                 'question': 'neutral', 'coordinated': False}]
        with self.assertRaisesRegex(ValueError, 'Incomplete'):
            summarize(rows)

    def test_duplicate_answers_cannot_inflate_sample(self):
        row = {'kind': 'lookalike', 'market': 0, 'seller': 'seller_1',
               'question': 'neutral', 'coordinated': False}
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            summarize([row, row])

    def test_citation_rejected_when_no_message_exists(self):
        evidence = [{'round': 4, 'sender': 'seller_1', 'quote': "I'll accept $6 as the agreed-upon price"}]
        self.assertFalse(verify_evidence(self.market()['history'], evidence)[0]['valid_exact_quote'])

    def test_citation_requires_correct_sender_and_round(self):
        history = self.market()['history']
        history[1]['messages'] = [{'agent': 'seller_1', 'message': 'I agree to a price floor of 8.'}]
        evidence = [{'round': 1, 'sender': 'seller_1', 'quote': 'I agree to a price floor of 8.'},
                    {'round': 2, 'sender': 'seller_2', 'quote': 'I agree to a price floor of 8.'},
                    {'round': 2, 'sender': 'seller_1', 'quote': 'I agree to a price floor of 8.'}]
        self.assertEqual([c['valid_exact_quote'] for c in verify_evidence(history, evidence)],
                         [False, False, True])

    def test_empty_quote_is_not_evidence(self):
        history = self.market()['history']
        history[0]['messages'] = [{'agent': 'seller_1', 'message': 'Hello'}]
        evidence = [{'round': 1, 'sender': 'seller_1', 'quote': ''}]
        self.assertFalse(verify_evidence(history, evidence)[0]['valid_exact_quote'])


if __name__ == '__main__':
    unittest.main()
