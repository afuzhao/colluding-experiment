import unittest
from unittest.mock import patch

from behavioral import Runner, PRICE_SCHEMA
from mechanism_controls import ControlRunner, FINE_ANNOUNCEMENT


class MechanismTests(unittest.TestCase):
    def test_sham_announcement_only_changes_enforcement_phase(self):
        runner = object.__new__(ControlRunner)
        with patch.object(Runner, 'ask', side_effect=lambda system, observation, *args: observation):
            first = runner.ask('same system', {'round': 5, 'audit_policy': 'controller has no fine'},
                               PRICE_SCHEMA, 1, 'sham_fine_1103:r5:seller_1:price')
            final = runner.ask('same system', {'round': 9, 'audit_policy': 'fine has ended'},
                               PRICE_SCHEMA, 1, 'sham_fine_1103:r9:seller_1:price')
        self.assertEqual(first['audit_policy'], FINE_ANNOUNCEMENT)
        self.assertEqual(final['audit_policy'], 'fine has ended')


if __name__ == '__main__':
    unittest.main()
