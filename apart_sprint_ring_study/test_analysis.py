import unittest

from analyze_behavioral import paired, holm, quantile, validate_episode
from behavioral import initial, allocation


class AnalysisTests(unittest.TestCase):
    def test_constant_paired_effect_has_correct_reference_p(self):
        result = paired([1] * 8)
        self.assertEqual(result['mean'], 1)
        self.assertEqual(result['ci95'], [1, 1])
        self.assertEqual(result['sign_flip_p'], 2 / 256)

    def test_null_paired_difference_and_holm(self):
        self.assertEqual(paired([0] * 8)['sign_flip_p'], 1)
        self.assertEqual(holm([0.01, 0.04, 0.03]), [0.03, 0.06, 0.06])
        self.assertEqual(quantile([0, 10], 0.5), 5)

    def test_economic_tampering_detected_by_replay(self):
        state = initial()
        state['history'] = [{'round': 1, 'observer': [], 'messages': [],
            'exposures': {'seller_1': [], 'seller_2': []}, 'prices': {'seller_1': 8, 'seller_2': 8},
            'active_floor': None, 'invalid_actions': [], 'outcome': allocation({'seller_1': 8, 'seller_2': 8})}]
        state['history'][0]['outcome']['net_profits']['seller_1'] = 999
        episode = {'complete': True, 'state': state, 'config': {'name': 'test', 'prefix_hash': None,
            'enforcement': None, 'mediator': None, 'rounds': 1}}
        with self.assertRaisesRegex(ValueError, 'Economic replay'):
            validate_episode(episode)


if __name__ == '__main__':
    unittest.main()
