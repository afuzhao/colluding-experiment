import tempfile
import unittest
from pathlib import Path

import market8 as m


def duopoly(script):
    d = object.__new__(m.Duopoly)
    d.models = ['a/x', 'b/y']
    d.root = Path(tempfile.mkdtemp())
    d.runners = {}
    for model in d.models:
        r = type('R', (), {})()
        r.model = model
        r.ask = (lambda mod: lambda system, obs, schema, valid, seed, key: script(mod, obs, key))(model)
        d.runners[model] = r
    return d


class DuopolyTests(unittest.TestCase):
    def test_silent_pair_uses_each_models_own_answers_and_alternating_seats(self):
        def script(model, obs, key):
            return {'price': 9 if model == 'a/x' else 3}
        even = duopoly(script).run('t', 1102, 'silent')
        self.assertEqual(even['history'][0]['prices'], {'seller_1': 9, 'seller_2': 3})
        odd = duopoly(script).run('t', 1103, 'silent')
        self.assertEqual(odd['history'][0]['prices'], {'seller_1': 3, 'seller_2': 9})
        self.assertEqual(even['history'][0]['outcome']['market_price'], 3)

    def test_history_shows_rivals_prices_and_no_script_hint(self):
        seen = []
        def script(model, obs, key):
            seen.append(obs)
            return {'price': 6}
        duopoly(script).run('t', 1102, 'silent')
        self.assertEqual(seen[0]['complete_visible_history'], [])
        self.assertEqual(seen[2]['complete_visible_history'][0]['prices'], {'seller_1': 6, 'seller_2': 6})

    def test_chat_pair_forms_agreement_and_executes(self):
        def script(model, obs, key):
            if key.endswith('message'):
                if obs['round'] == 1:
                    return {'message': 'floor 8?', 'action': 'propose', 'floor': 8}
                return {'message': 'ok', 'action': 'accept', 'floor': 8}
            return {'price': 8}
        state = duopoly(script).run('t', 1102, 'chat')
        self.assertIsNone(state['history'][0]['active_floor'])  # proposals are delivered after round 1
        self.assertEqual(state['history'][1]['active_floor'], 8)  # accepted in round 2
        self.assertEqual(state['active_floor'], 8)
        self.assertTrue(state['history'][-1]['outcome']['executed'])

    def test_wide_grid_profit_is_parametric(self):
        out = m.alloc({'seller_1': 12, 'seller_2': 12}, 'G2', None)
        self.assertEqual(out['gross_profits']['seller_1'], (12 - 2) * (240 - 8 * 12) / 2)


if __name__ == '__main__':
    unittest.main()
