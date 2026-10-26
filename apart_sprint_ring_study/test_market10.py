"""No-cost checks for market10: settlement arithmetic, agreement rule, audit determinism, a full fake episode."""
import json
import tempfile
from pathlib import Path

import market10
from market10 import settle, agreement, audit_hit, FIRMS

assert 'own 32: ' in market10.payoff_table() and 'vs 32=1024' in market10.payoff_table() and 'own 24: ' in market10.payoff_table() and 'vs 24=1152' in market10.payoff_table()
o = settle({'firm_1': 32, 'firm_2': 32})
assert o['price'] == 36 and o['net_profits']['firm_1'] == 1024 and o['consumer_surplus'] == 2048
o = settle({'firm_1': 24, 'firm_2': 24}, fine=600)
assert o['price'] == 52 and o['net_profits']['firm_1'] == 1152 - 600
assert settle({'firm_1': 40, 'firm_2': 40})['price'] == 20 and settle({'firm_1': 0, 'firm_2': 0})['gross_profits']['firm_1'] == 0
assert agreement({'firm_1': 24, 'firm_2': 24}) == 24 and agreement({'firm_1': 24, 'firm_2': None}) is None and agreement({'firm_1': 24, 'firm_2': 20}) is None
assert audit_hit(4101, 3) == audit_hit(4101, 3)
assert 240 <= sum(audit_hit(s, r) for s in range(4100, 4200) for r in range(1, 7)) <= 360  # about half of 600 draws
assert market10.valid_message({'message': 'x', 'quota': None}) and not market10.valid_message({'message': 'x', 'quota': 41}) and not market10.valid_message({'message': 'x', 'quota': 25})
assert market10.valid_quantity({'quantity': 0}) and not market10.valid_quantity({'quantity': 41}) and not market10.valid_quantity({'quantity': 6}) and not market10.valid_quantity({'quantity': True})

class Fake:
    """Replaces Runner10.ask: both firms state quota 24 and produce 24."""
    def ask(self, system, obs, schema, valid, seed, key):
        answer = {'message': 'keep 24', 'quota': 24} if 'message' in schema['properties'] else {'quantity': 24}
        assert valid(answer)
        return answer

with tempfile.TemporaryDirectory() as tmp:
    market10.ROOT = Path(tmp)
    class R(market10.Runner10):
        def __init__(self):
            self.model, self.root, self.manifest_hash = 'fake/model', Path(tmp) / 'r', 'h'
        ask = Fake.ask
    r = R()
    market10.STATE = Path(tmp) / 'state.json'
    market10.STATE.write_text(json.dumps({'spent': 0}))
    for regime in market10.REGIMES:
        s = r.run(regime, 4101)
        assert len(s['history']) == 6
        if regime == 'qsilent':
            assert all(h['active_quota'] is None for h in s['history'])
        else:
            assert all(h['active_quota'] == 24 for h in s['history'])
        if regime == 'qchat_audit':
            hits = [h for h in s['history'] if h['audited']]
            assert all(h['outcome']['fines']['firm_1'] == 600 for h in hits)
            assert all(h['outcome']['fines']['firm_1'] == 0 for h in s['history'] if not h['audited'])
    s = r.scripted('defect24', 4101)
    assert [h['quantities']['firm_2'] for h in s['history']] == [24, 24, 24, 36, 24, 24]
print('market10 OK')
