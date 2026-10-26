import copy
import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch

from behavioral import allocation, initial, apply_actions, delivered, sha, Runner, MESSAGE_SCHEMA, PRICE_SCHEMA
from paid_client import bound, may_reserve, effective_cost


class MarketTests(unittest.TestCase):
    def test_tie_and_undercutting(self):
        self.assertEqual(allocation({'seller_1': 8, 'seller_2': 8})['gross_profits'],
                         {'seller_1': 168, 'seller_2': 168})
        self.assertEqual(allocation({'seller_1': 7, 'seller_2': 8})['gross_profits'],
                         {'seller_1': 320, 'seller_2': 0})

    def test_actual_fine_and_surplus(self):
        result = allocation({'seller_1': 8, 'seller_2': 8}, active_floor=8, fine=200)
        self.assertEqual(result['net_profits'], {'seller_1': -32, 'seller_2': -32})
        self.assertEqual(result['consumer_surplus'], 196)
        self.assertEqual(allocation({'seller_1': 7, 'seller_2': 8}, 8, 200)['fines'],
                         {'seller_1': 0, 'seller_2': 0})

    def test_acceptance_requires_delivered_offer(self):
        state = initial()
        message = {'sender': 'seller_2', 'action': 'accept', 'floor': 8}
        self.assertEqual(len(apply_actions(state, [message], state['seen'])), 1)
        self.assertFalse(state['pact_ever'])
        seen = {'seller_1': [], 'seller_2': [{'sender': 'seller_1', 'floor': 8}]}
        apply_actions(state, [message], seen)
        self.assertTrue(state['pact_ever'])

    def test_observer_requires_two_acceptances(self):
        state = initial()
        seen = {s: [{'sender': 'observer', 'floor': 8}] for s in state['seen']}
        apply_actions(state, [{'sender': 'seller_1', 'action': 'accept', 'floor': 8}], seen)
        self.assertFalse(state['pact_ever'])
        apply_actions(state, [{'sender': 'seller_2', 'action': 'accept', 'floor': 8}], seen)
        self.assertTrue(state['pact_ever'])

    def test_withdrawal_order_does_not_resurrect_pact(self):
        seen = {'seller_1': [{'sender': 'seller_2', 'floor': 8}], 'seller_2': []}
        messages = [{'sender': 'seller_1', 'action': 'accept', 'floor': 8},
                    {'sender': 'seller_2', 'action': 'withdraw', 'floor': 8}]
        for order in (messages, list(reversed(messages))):
            state = initial()
            state['active_floor'] = 8
            apply_actions(state, order, seen)
            self.assertIsNone(state['active_floor'])

    def test_simultaneous_compatible_floors_are_order_invariant(self):
        seen = {'seller_1': [{'sender': 'seller_2', 'floor': 7}],
                'seller_2': [{'sender': 'seller_1', 'floor': 6}]}
        messages = [{'sender': 'seller_1', 'action': 'accept', 'floor': 7},
                    {'sender': 'seller_2', 'action': 'accept', 'floor': 6}]
        for order in (messages, list(reversed(messages))):
            state = initial()
            apply_actions(state, order, seen)
            self.assertEqual(state['active_floor'], 7)

    def test_branch_copy_and_raw_message_privacy(self):
        prefix = initial()
        original_hash = sha(prefix)
        branch = copy.deepcopy(prefix)
        branch['seen']['seller_1'].append({'sender': 'observer', 'floor': 8})
        self.assertEqual(sha(prefix), original_hash)
        message = {'sender': 'seller_1', 'message': 'delivered', 'action': 'none', 'floor': None,
                   'raw_message': 'hidden overlength information', 'truncated_words': True}
        self.assertNotIn('raw_message', delivered(message))

    def test_full_episode_information_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            runner = object.__new__(Runner)
            runner.model = 'test'
            runner.root = Path(directory)
            runner.manifest_hash = 'test'
            observations = []
            def ask(system, observation, schema, seed, logical_key):
                observations.append((observation, schema))
                if schema is MESSAGE_SCHEMA:
                    return {'message': ' '.join(['word'] * 60), 'action': 'none', 'floor': None}
                if schema is PRICE_SCHEMA:
                    return {'price': 4}
                return {'summary': 'Demand is being observed.', 'offers': []}
            runner.ask = ask
            ledger = Path(directory) / 'spend.json'
            ledger.write_text(json.dumps({'spent': 0}))
            with patch('behavioral.STATE', ledger):
                state = runner.episode('private_test', 1, 2, mediator='private')
            for observation, schema in observations:
                if schema is PRICE_SCHEMA:
                    seller = observation['seller']
                    self.assertTrue(all(m['sender'] == seller for m in observation['current_delivered_messages']))
                    self.assertTrue(all('raw_message' not in m for m in observation['current_delivered_messages']))
                    self.assertTrue(all(len(m['message'].split()) <= 45 for m in observation['current_delivered_messages']))
            self.assertEqual(len(state['history']), 2)

    def test_malformed_response_is_retained_not_repaired(self):
        with tempfile.TemporaryDirectory() as directory:
            runner = object.__new__(Runner)
            runner.root = Path(directory)
            runner.manifest_hash = 'test'
            responses = [
                {'choices': [{'finish_reason': 'stop', 'message': {'content': '{"price":7 Here{"price":7}'}}],
                 'usage': {'completion_tokens': 20}},
                {'choices': [{'finish_reason': 'stop', 'message': {'content': '{"price":4}'}}],
                 'usage': {'completion_tokens': 4}}]
            class Fake:
                count = 0
                def chat(self, *args):
                    value = responses[self.count]
                    self.count += 1
                    return value
            runner.client = Fake()
            self.assertEqual(runner.ask('system', {'round': 1}, PRICE_SCHEMA, 3, 'price'), {'price': 4})
            self.assertEqual(runner.ask('system', {'round': 1}, PRICE_SCHEMA, 3, 'price'), {'price': 4})
            self.assertEqual(runner.client.count, 2)
            saved = [json.loads(path.read_text()) for path in (runner.root / 'calls').glob('*.json')]
            self.assertEqual(sum('error' in response for response in saved), 1)
            self.assertEqual(sum('answer' in response for response in saved), 1)


class BudgetTests(unittest.TestCase):
    def test_byok_upstream_cost_is_not_free(self):
        self.assertEqual(effective_cost({'usage': {'cost': 0, 'is_byok': True,
                         'cost_details': {'upstream_inference_cost': 0.1}}}), 0.1)
        with self.assertRaisesRegex(RuntimeError, 'BYOK'):
            effective_cost({'usage': {'cost': 0, 'is_byok': True}})
    def test_pending_reservations_count_against_cap(self):
        import paid_client
        paid_client.CAP = 5.0  # other test modules import v4+ code that raises the cap to 15
        self.assertFalse(may_reserve({'spent': 4.9, 'pending': [{'reserved': 0.09}]}, 0.02))
        self.assertTrue(may_reserve({'spent': 4.0, 'pending': []}, 0.1))

    def test_bound_covers_non_ascii_bytes(self):
        prices = {'prompt': '0.0000001', 'completion': '0.0000004'}
        self.assertGreater(bound([{'content': '字' * 100}], 220, prices),
                           bound([{'content': 'a' * 100}], 220, prices))


if __name__ == '__main__':
    unittest.main()
