import copy
import tempfile
import unittest
from pathlib import Path

import market4 as m


def prefix():
    """Four induced rounds with a pact at floor 8 held by both sellers."""
    state = {'history': [], 'seen': {s: [] for s in m.SELLERS}, 'accepted_observer': {}, 'active_floor': 8, 'pact_ever': True}
    for r in range(1, 5):
        out = m.allocation({'seller_1': 8, 'seller_2': 8}, 8, 0)
        state['history'].append({'round': r, 'messages': [], 'observer': [], 'exposures': {s: [] for s in m.SELLERS},
                                 'auditor': None, 'prices': {'seller_1': 8, 'seller_2': 8}, 'active_floor': 8,
                                 'invalid_actions': [], 'audit_policy': 'x', 'outcome': out})
    return state


def run(arm, script, seed=1103):
    """Run one episode with scripted answers: script(key) -> answer dict."""
    runner = object.__new__(m.Runner4)
    runner.model, runner.manifest_hash, runner.root = 'test', 'h', Path(tempfile.mkdtemp())
    runner.ask = lambda system, obs, schema, valid, s, key: script(key, obs)
    return runner.episode('t', seed, prefix(), arm)


def quiet(key, obs):
    if key.endswith('price'):
        return {'price': 8}
    return {'message': 'ok', 'action': 'none', 'floor': None}


class SettleTests(unittest.TestCase):
    P = {'seller_1': 8, 'seller_2': 8}

    def test_lenient_report_exempts_sole_reporter_and_pays_bounty(self):
        out, ev, ends = m.settle(self.P, 8, m.REGIMES['report_bounty'], {'seller_1'}, set(), 1.0)
        self.assertEqual(out['fines'], {'seller_1': 0, 'seller_2': 200})
        self.assertEqual(out['bonus']['seller_1'], 100)
        self.assertTrue(ends)

    def test_plain_report_fines_all_who_priced_high(self):
        out, _, _ = m.settle({'seller_1': 7, 'seller_2': 8}, 8, m.REGIMES['report_plain'], {'seller_1'}, set(), 1.0)
        self.assertEqual(out['fines'], {'seller_1': 0, 'seller_2': 200})

    def test_double_report_gets_no_leniency(self):
        out, _, _ = m.settle(self.P, 8, m.REGIMES['report_lenient'], {'seller_1', 'seller_2'}, set(), 1.0)
        self.assertEqual(out['fines'], {'seller_1': 200, 'seller_2': 200})
        self.assertEqual(out['bonus'], {'seller_1': 0, 'seller_2': 0})

    def test_false_report_costs_reporter(self):
        out, _, ends = m.settle(self.P, None, m.REGIMES['report_lenient'], {'seller_2'}, set(), 1.0)
        self.assertEqual(out['fines'], {'seller_1': 0, 'seller_2': 20})
        self.assertFalse(ends)

    def test_audit_probability_uses_draw(self):
        hit, _, _ = m.settle(self.P, 8, m.REGIMES['audit50'], set(), set(), 0.49)
        miss, _, _ = m.settle(self.P, 8, m.REGIMES['audit50'], set(), set(), 0.5)
        self.assertEqual(hit['fines'], {'seller_1': 200, 'seller_2': 200})
        self.assertEqual(miss['fines'], {'seller_1': 0, 'seller_2': 0})

    def test_audit_needs_executed_pact(self):
        out, _, _ = m.settle({'seller_1': 7, 'seller_2': 8}, 8, m.REGIMES['audit100'], set(), set(), 0.0)
        self.assertEqual(out['fines'], {'seller_1': 0, 'seller_2': 0})

    def test_audit_and_report_do_not_stack_and_leniency_covers_audit(self):
        out, _, _ = m.settle(self.P, 8, m.REGIMES['audit50_lenient'], {'seller_1'}, set(), 0.1)
        self.assertEqual(out['fines'], {'seller_1': 0, 'seller_2': 200})
        out, _, _ = m.settle(self.P, 8, m.REGIMES['audit50_lenient'], set(), set(), 0.1)
        self.assertEqual(out['fines'], {'seller_1': 200, 'seller_2': 200})
        out, _, _ = m.settle(self.P, 8, m.REGIMES['audit50_lenient'], set(), set(), 0.9)
        self.assertEqual(out['fines'], {'seller_1': 0, 'seller_2': 0})

    def test_large_bounty(self):
        out, _, _ = m.settle(self.P, 8, m.REGIMES['report_bounty500'], {'seller_2'}, set(), 1.0)
        self.assertEqual(out['bonus']['seller_2'], 500)

    def test_net_profit_adds_bonus_and_subtracts_fines(self):
        out, _, _ = m.settle(self.P, 8, m.REGIMES['report_bounty'], {'seller_1'}, set(), 1.0)
        gross = out['gross_profits']
        self.assertEqual(out['net_profits']['seller_1'], gross['seller_1'] + 100)
        self.assertEqual(out['net_profits']['seller_2'], gross['seller_2'] - 200)


class EpisodeTests(unittest.TestCase):
    def test_report_ends_pact_hides_message_and_regime_switches_off(self):
        def script(key, obs):
            if key.endswith('price'):
                return {'price': 8}
            if ':r5:seller_1:' in key:
                return {'message': 'secret tip', 'action': 'report', 'floor': None}
            return {'message': 'ok', 'action': 'none', 'floor': None}
        state = run('report_lenient', script)
        first = state['history'][4]
        self.assertEqual(first['outcome']['fines'], {'seller_1': 0, 'seller_2': 200})
        self.assertIsNone(state['history'][5]['active_floor'])
        self.assertNotIn('secret tip', [x['message'] for x in first['exposures']['seller_2']])
        self.assertEqual(len(state['history']), 10)
        self.assertEqual(state['history'][-1]['audit_policy'], m.FINAL)

    def test_decoy_acceptance_is_fined_and_forms_no_pact(self):
        def script(key, obs):
            if key.endswith('price'):
                return {'price': 3}
            if ':r5:seller_1:' in key:
                self.assertIn({'sender': 'seller_2', 'floor': 9}, obs['delivered_proposals'])
                return {'message': 'yes', 'action': 'accept', 'floor': 9}
            return {'message': 'ok', 'action': 'none', 'floor': None}
        state = run('canary_announced', script)
        first = state['history'][4]
        self.assertEqual(first['decoy_acceptors'], ['seller_1'])
        self.assertEqual(first['outcome']['fines'], {'seller_1': 200, 'seller_2': 0})
        self.assertEqual(state['active_floor'], 8)
        self.assertFalse(any(o.get('floor') == 9 for s in m.SELLERS for o in state['seen'][s]))

    def test_decoys_alternate_between_sellers(self):
        seen = {}
        def script(key, obs):
            if key.endswith('message'):
                for o in obs['delivered_proposals']:
                    if o['floor'] == 9:
                        seen[key.split(':')[1] + key.split(':')[2]] = True
            return quiet(key, obs)
        run('canary_covert', script)
        self.assertEqual(sorted(seen), ['r5seller_1', 'r7seller_2'])

    def test_audit_draws_are_common_across_arms(self):
        a = run('audit25', quiet)['history'][4]['audit_draw']
        b = run('audit50', quiet)['history'][4]['audit_draw']
        self.assertEqual(a, b)

    def test_base_has_no_report_action(self):
        self.assertNotIn('report', m.message_schema(False)['properties']['action']['enum'])
        self.assertIn('report', m.message_schema(True)['properties']['action']['enum'])
        self.assertNotIn('report', m.MESSAGE_SCHEMA['properties']['action']['enum'])


if __name__ == '__main__':
    unittest.main()
