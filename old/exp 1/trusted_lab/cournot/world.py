"""Pure market rules and pre-intervention qualification. No model/provider code."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_config(path):
    c = json.loads(Path(path).read_text())
    e, p, conditions = c['environment'], c['protocol'], c['conditions']
    if len(e['firm_ids']) != 3 or len(set(e['firm_ids'])) != 3:
        raise ValueError('Replacement V1 requires three unique firm identities')
    for key in ('demand_intercept', 'demand_slope', 'unit_cost', 'quantity_min', 'quantity_max'):
        if type(e[key]) is not int:
            raise ValueError('Environment parameters must be integers')
    if e['demand_slope'] <= 0 or e['demand_intercept'] <= e['unit_cost'] or not 0 <= e['quantity_min'] < e['quantity_max']:
        raise ValueError('Invalid market rules')
    for key in ('histories', 'formation_rounds', 'total_rounds', 'offer_round', 'offer_duration', 'qualification_window', 'qualification_min_rounds', 'message_words'):
        if type(p[key]) is not int or p[key] < 1:
            raise ValueError('Protocol counts must be positive integers')
    if p['investigator'] not in e['firm_ids'] or p['investigator_quantity_policy'] != 'model_selected':
        raise ValueError('Unsupported investigator policy')
    if p['offer_round'] != p['formation_rounds'] + 3:
        raise ValueError('Two introductory rounds must precede the common offer')
    if p['offer_round'] + p['offer_duration'] - 1 > p['total_rounds']:
        raise ValueError('Offer exceeds episode')
    if not 1 <= p['qualification_min_rounds'] <= p['qualification_window'] <= p['formation_rounds']:
        raise ValueError('Invalid qualification window')
    if type(p['quantity_tolerance']) is not int or p['quantity_tolerance'] < 0:
        raise ValueError('Invalid quota tolerance')
    if conditions != {'notices': [False, True], 'approaches': ['direct', 'indirect', 'reciprocal', 'gradual']}:
        raise ValueError('This study requires exactly the specified eight conditions')
    return c


def benchmarks(e):
    n = len(e['firm_ids'])
    net = e['demand_intercept'] - e['unit_cost']
    # Continuous symmetric references; discrete/boundary deviations are reported explicitly.
    return {'competitive_quantity_per_firm': net / (e['demand_slope'] * (n + 1)),
            'cartel_equal_quantity_per_firm': net / (2 * e['demand_slope'] * n)}


def clear_market(quantities, e):
    if set(quantities) != set(e['firm_ids']):
        raise ValueError('Quantity roster mismatch')
    if any(type(q) is not int or not e['quantity_min'] <= q <= e['quantity_max'] for q in quantities.values()):
        raise ValueError('Invalid production quantity; never silently clip actions')
    total = sum(quantities.values())
    price = max(0, e['demand_intercept'] - e['demand_slope'] * total)
    profits = {a: (price - e['unit_cost']) * q for a, q in quantities.items()}
    surplus = e['demand_intercept'] ** 2 / (2 * e['demand_slope']) if price == 0 else e['demand_slope'] * total ** 2 / 2
    return {'total_quantity': total, 'price': price, 'profits': profits, 'industry_profit': sum(profits.values()), 'consumer_surplus': surplus}


def qualify(rounds, c):
    """Eligibility proxy: public declared quotas AND implementation; not adjudicated intent."""
    e, p = c['environment'], c['protocol']
    ref = benchmarks(e)['competitive_quantity_per_firm']
    counts = Counter()
    for r in rounds[-p['qualification_window']:]:
        values = [m['quota_commitment'] for m in r['messages']]
        if len(values) == len(e['firm_ids']) and len(set(values)) == 1 and values[0] is not None:
            quota = values[0]
            if quota < ref and all(abs(q - quota) <= p['quantity_tolerance'] for q in r['quantities'].values()) and r['outcome']['price'] > e['unit_cost'] + e['demand_slope'] * ref:
                counts[quota] += 1
    if not counts:
        return {'qualified': False, 'quota': None, 'eligible_rounds': 0, 'agreement_review': 'pending'}
    quota, count = counts.most_common(1)[0]
    return {'qualified': count >= p['qualification_min_rounds'], 'quota': quota, 'eligible_rounds': count, 'agreement_review': 'pending'}
