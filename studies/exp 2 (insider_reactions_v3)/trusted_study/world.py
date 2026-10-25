"""Pure Cournot economics and formation proxy."""
from collections import Counter
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
