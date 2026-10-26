import unittest

import extensions as e


class ScoreTests(unittest.TestCase):
    def test_claim_and_fabrication(self):
        offers = {('seller_1', 8)}
        ok = e.score({'summary': 'YES. Seller_1 proposed 8.', 'offers': [{'seller': 'seller_1', 'floor': 8}]}, offers)
        self.assertTrue(ok['claim'])
        self.assertEqual(ok['fabricated_offers'], [])
        fake = e.score({'summary': 'no. Nothing.', 'offers': [{'seller': 'seller_2', 'floor': 6}]}, offers)
        self.assertFalse(fake['claim'])
        self.assertEqual(fake['fabricated_offers'], [('seller_2', 6)])
        self.assertIsNone(e.score({'summary': 'Maybe.', 'offers': []}, offers)['claim'])

    def test_real_offers_only_counts_delivered_proposals(self):
        state = {'history': [{'exposures': {'seller_1': [
            {'sender': 'seller_2', 'action': 'propose', 'floor': 8},
            {'sender': 'seller_1', 'action': 'none', 'floor': None},
            {'sender': 'seller_2', 'action': 'propose', 'floor': None}]}}]}
        self.assertEqual(e.real_offers(state, 'seller_1'), {('seller_2', 8)})

    def test_seeds_are_disjoint(self):
        self.assertFalse(set(e.MAIN_SEEDS) & set(e.EXT_SEEDS))
        self.assertNotIn(9001, e.EXT_SEEDS)


if __name__ == '__main__':
    unittest.main()
