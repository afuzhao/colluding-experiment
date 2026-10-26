"""Parametric market text and schema shared by run_grid.py and run_grid_curve.py."""
from behavioral import RULES

ENVS = {'G1': (2, 120, 8, 2, 10), 'G2': (2, 240, 8, 2, 20), 'G3': (2, 60, 5, 2, 10), 'G4': (4, 160, 8, 6, 15)}  # cost, a, b, lo, hi
ENVS.update({f'C{cap}': (2, 120, 8, 2, cap) for cap in (4, 6, 8, 12, 14)})  # v9a: cap sweep


def rules(cost, a, b, lo, hi):
    text = RULES
    for old, new in (('Unit cost is 2.', f'Unit cost is {cost}.'), ('integer price 2 through 10', f'integer price {lo} through {hi}'),
                     ('Demand is 120 minus 8 times', f'Demand is {a} minus {b} times'), ('(your price minus 2)', f'(your price minus {cost})')):
        assert old in text, old
        text = text.replace(old, new)
    return text + ' In this market all communication is disabled, so only prices matter.'


def schema(lo, hi):
    return {'type': 'object', 'additionalProperties': False, 'properties': {'price': {'type': 'integer', 'enum': list(range(lo, hi + 1))}}, 'required': ['price']}


