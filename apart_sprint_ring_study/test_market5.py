import tempfile
import unittest
from pathlib import Path

import market5 as m


def run(script, prices_by_round):
    runner = object.__new__(m.Runner5)
    runner.model, runner.manifest_hash, runner.root = 'test', 'h', Path(tempfile.mkdtemp())
    runner.ask = lambda system, obs, schema, valid, seed, key: {'price': prices_by_round[obs['round'] - 1]}
    return runner.scripted('t', 1, script)


class ScriptTests(unittest.TestCase):
    def test_rival_scripts(self):
        self.assertEqual([m.rival_price('defect_once', n, []) for n in range(1, 5)], [8, 7, 8, 8])
        self.assertEqual(m.rival_price('tft', 1, []), 8)
        self.assertEqual(m.rival_price('tft', 3, [8, 6]), 6)
        self.assertEqual(m.rival_price('hold3', 4, []), 3)
        self.assertEqual(m.rival_price('hold10', 1, []), 10)

    def test_best_response(self):
        self.assertEqual(m.best_response(8)[0], 7)      # undercut a high rival
        self.assertEqual(m.best_response(3), (3, 48.0))  # tie at 3 beats undercutting to 2 (zero profit)
        self.assertEqual(m.best_response(10)[0], 8)

    def test_episode_records_both_prices_and_profits(self):
        state = run('hold3', [8, 8, 3, 3, 3, 3])
        self.assertEqual(len(state['history']), 6)
        first = state['history'][0]
        self.assertEqual(first['prices'], {'seller_1': 8, 'seller_2': 3})
        self.assertEqual(first['outcome']['gross_profits']['seller_1'], 0)
        self.assertEqual(state['history'][2]['outcome']['gross_profits']['seller_1'], 48)

    def test_round_one_observation_does_not_reveal_script(self):
        seen = []
        runner = object.__new__(m.Runner5)
        runner.model, runner.manifest_hash, runner.root = 'test', 'h', Path(tempfile.mkdtemp())
        runner.ask = lambda system, obs, schema, valid, seed, key: seen.append(obs) or {'price': 8}
        runner.scripted('t', 1, 'hold3')
        self.assertEqual(seen[0]['complete_visible_history'], [])
        self.assertNotIn('hold3', str(seen[0]))


if __name__ == '__main__':
    unittest.main()
