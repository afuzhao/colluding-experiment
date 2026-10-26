import tempfile
import unittest
from pathlib import Path

import market6 as m
from test_market4 import prefix


def run(arm, prices):
    runner = object.__new__(m.Runner6)
    runner.model, runner.manifest_hash, runner.root = 'test', 'h', Path(tempfile.mkdtemp())
    seen = []
    def ask(system, obs, schema, valid, seed, key):
        seen.append((key, obs))
        if key.endswith('price'):
            return {'price': prices[obs['round'] - 5]}
        return {'message': 'ok', 'action': 'none', 'floor': None}
    runner.ask = ask
    return runner.maverick('t', 1103, prefix(), arm), seen


class MaverickTests(unittest.TestCase):
    def test_three_way_allocation(self):
        out = m.allocation3({'seller_1': 8, 'seller_2': 8, 'maverick': 5})
        self.assertEqual(out['market_price'], 5)
        self.assertEqual(out['gross_profits'], {'seller_1': 0, 'seller_2': 0, 'maverick': 3 * 80})
        tie = m.allocation3({'seller_1': 5, 'seller_2': 8, 'maverick': 5})
        self.assertEqual(tie['gross_profits']['seller_1'], tie['gross_profits']['maverick'])

    def test_entry_timing_and_notice(self):
        state, seen = run('mav5', [8, 8, 5, 5, 5, 5])
        self.assertEqual([r['maverick_present'] for r in state['history'][4:]], [False, False, True, True, True, True])
        self.assertTrue(all('maverick' in r['prices'] for r in state['history'][6:]))
        self.assertFalse(any('maverick' in r['prices'] for r in state['history'][4:6]))
        notices = [k for k, o in seen if 'market_notice' in o]
        self.assertTrue(all(':r7:' in k or ':r8:' in k or ':r9:' in k or ':r10:' in k for k in notices))
        self.assertFalse(any(':r5:' in k or ':r6:' in k for k in notices))

    def test_control_has_no_entrant_and_pact_executes(self):
        state, _ = run('mav_none', [8] * 6)
        self.assertFalse(any('maverick' in r['prices'] for r in state['history']))
        self.assertTrue(all(r['outcome']['executed'] for r in state['history'][4:]))

    def test_entrant_price_never_reveals_script(self):
        _, seen = run('mav3', [8] * 6)
        self.assertNotIn('script', str(seen).lower())


if __name__ == '__main__':
    unittest.main()
