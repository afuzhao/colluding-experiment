import unittest

import busting as b


class FakeRunner(b.BustingRunner):
    def __init__(self):
        self.seen = None


def captured(key, observation):
    runner = FakeRunner()
    original = b.Runner.ask
    b.Runner.ask = lambda self, system, obs, schema, seed, logical_key: obs
    try:
        return runner.ask('s', observation, None, 0, key)
    finally:
        b.Runner.ask = original


HISTORY = [{'round': r} for r in range(1, 6)]


class BustingTests(unittest.TestCase):
    def test_blank_swap_hides_history_for_seller_2_only(self):
        obs = {'round': 5, 'complete_visible_history': HISTORY, 'delivered_proposals': [{'x': 1}]}
        seller_2 = captured('swap_blank_1103:r5:seller_2:message', obs)
        self.assertEqual([h['round'] for h in seller_2['complete_visible_history']], [5])
        self.assertEqual(seller_2['delivered_proposals'], [])
        self.assertIn('own tenure', seller_2['notice'])
        self.assertEqual(captured('swap_blank_1103:r5:seller_1:message', obs), obs)

    def test_informed_swap_keeps_history(self):
        obs = {'round': 6, 'complete_visible_history': HISTORY}
        out = captured('swap_informed_1103:r6:seller_2:price', obs)
        self.assertEqual(out['complete_visible_history'], HISTORY)
        self.assertIn('complete record', out['notice'])

    def test_announcement_only_in_rounds_5_to_8(self):
        obs = {'round': 5, 'audit_policy': 'x'}
        self.assertIn('20 points', captured('sham_fine_small_1103:r5:seller_1:message', obs)['audit_policy'])
        self.assertIn('pays double', captured('sham_leniency_1103:r8:seller_1:message', {**obs, 'round': 8})['audit_policy'])
        self.assertEqual(captured('sham_leniency_1103:r9:seller_1:message', {**obs, 'round': 9})['audit_policy'], 'x')
        self.assertNotIn('200', b.SMALL)


if __name__ == '__main__':
    unittest.main()
