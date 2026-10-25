"""Differentiated demand from a concave, quasilinear consumer utility.

U(q) = a*sum(q) - b/2*sum(q_i**2) - d/2*sum(q)**2.
The buyer chooses q>=0 to maximize U(q)-p.q. An active-set solution,
not independent clipping of linear demands, handles zero-demand products.
"""
import itertools
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate_config(c):
    if c['firms'] != ['firm_A', 'firm_B', 'firm_C']:
        raise ValueError('V1 is a three-firm environment; changing the roster needs a new version')
    e = c['economics']
    if not (e['own_quadratic'] > 0 and e['aggregate_quadratic'] >= 0):
        raise ValueError('Consumer utility must be strictly concave')
    for field in ['price_min', 'price_max', 'price_tick']:
        if type(e[field]) is not int:
            raise ValueError('V1 uses an integer price grid')
    if not (0 < e['price_tick'] and e['unit_cost'] <= e['price_min'] < e['price_max']):
        raise ValueError('Invalid price grid or cost')
    if (e['price_max'] - e['price_min']) % e['price_tick']:
        raise ValueError('Grid endpoints must align')
    if c['protocol'] != dict(formation_rounds=5, total_rounds=15, role_switch_round=6, offer_round=8, reply_round=9, action_window=[9, 13], message_word_limit=60):
        raise ValueError('V1 freezes the 5+10 schedule; change protocol validation for a new version')
    return c


def load_config(path=None):
    return validate_config(json.loads(Path(path or ROOT / 'configs/environment.json').read_text()))


class Market:
    def __init__(self, config=None):
        self.config = copy.deepcopy(validate_config(config) if config is not None else load_config())
        self.firms = tuple(self.config['firms'])
        self.e = self.config['economics']
        self.grid = tuple(range(self.e['price_min'], self.e['price_max'] + 1, self.e['price_tick']))
        self._conditional_cache = {}

    def validate_prices(self, prices):
        if not isinstance(prices, dict) or set(prices) != set(self.firms):
            raise ValueError('Supply one price for every firm')
        if any(type(p) is not int or p not in self.grid for p in prices.values()):
            raise ValueError('Prices must be grid integers; actions are never clipped or overwritten')

    def clear(self, prices):
        self.validate_prices(prices)
        a, b, d = (self.e[k] for k in ['utility_intercept', 'own_quadratic', 'aggregate_quadratic'])
        active = []
        # Add goods in ascending price order while marginal utility exceeds price.
        for firm in sorted(self.firms, key=lambda f: (prices[f], f)):
            threshold = a if not active else (a * b + d * sum(prices[f] for f in active)) / (b + d * len(active))
            if prices[firm] >= threshold:
                break
            active.append(firm)
        total = (len(active) * a - sum(prices[f] for f in active)) / (b + d * len(active)) if active else 0.0
        threshold = a - d * total
        sales = {f: max(0.0, (threshold - prices[f]) / b) if f in active else 0.0 for f in self.firms}
        profits = {f: (prices[f] - self.e['unit_cost']) * sales[f] for f in self.firms}
        cs = 0.5 * b * sum(q * q for q in sales.values()) + 0.5 * d * total * total
        revenue = sum(prices[f] * sales[f] for f in self.firms)
        return {'prices': dict(prices), 'sales': sales, 'profits': profits, 'total_sales': total,
                'industry_profit': sum(profits.values()), 'consumer_surplus': cs,
                'total_surplus': cs + sum(profits.values()),
                'transaction_price': revenue / total if total > 0 else None}

    def best_responses(self, prices, firm):
        self.validate_prices(prices)
        if firm not in self.firms:
            raise ValueError('Unknown firm')
        values = [(self.clear(prices | {firm: p})['profits'][firm], p) for p in self.grid]
        best = max(v for v, p in values)
        return {'prices': [p for v, p in values if abs(v - best) < 1e-8], 'profit': best}

    def coalition_best_responses(self, prices, members):
        self.validate_prices(prices)
        members = tuple(members)
        if not members or len(set(members)) != len(members) or any(f not in self.firms for f in members):
            raise ValueError('Invalid coalition')
        best, actions = float('-inf'), []
        for choices in itertools.product(self.grid, repeat=len(members)):
            candidate = prices | dict(zip(members, choices))
            value = sum(self.clear(candidate)['profits'][f] for f in members)
            if value > best + 1e-8:
                best, actions = value, [dict(zip(members, choices))]
            elif abs(value - best) < 1e-8:
                actions.append(dict(zip(members, choices)))
        return {'allocations': actions, 'joint_profit': best}

    def conditional_ab_nash(self, outsider_price):
        """A/B noncooperative one-shot references holding C's actual price fixed."""
        self.validate_prices(dict.fromkeys(self.firms, outsider_price))
        if outsider_price not in self._conditional_cache:
            equilibria = []
            for pb in self.grid:
                base = dict(firm_A=self.grid[0], firm_B=pb, firm_C=outsider_price)
                for pa in self.best_responses(base, 'firm_A')['prices']:
                    candidate = base | {'firm_A': pa}
                    if pb in self.best_responses(candidate, 'firm_B')['prices']:
                        equilibria.append({'firm_A': pa, 'firm_B': pb})
            self._conditional_cache[outsider_price] = equilibria
        return [dict(x) for x in self._conditional_cache[outsider_price]]

    def benchmarks(self):
        # Config-specific benchmark candidates; validate.py checks deviations and coalition optima.
        competitive = dict.fromkeys(self.firms, 34)
        full = dict.fromkeys(self.firms, 64)
        partial = dict(firm_A=42, firm_B=42, firm_C=37)
        return {name: self.clear(prices) for name, prices in [('competitive', competitive), ('full_cartel', full), ('partial_cartel', partial)]}
