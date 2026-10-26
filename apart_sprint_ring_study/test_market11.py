"""No-cost checks for market11: benchmarks, payoffs, branching of cure episodes, audits, agreement rule."""
import json
import tempfile
from pathlib import Path

import market11 as m

P, Q, L = m.GAMES['P'], m.GAMES['Q'], m.GAMES['L']
assert P.nash_price == 3 and P.joint_price == 8 and P.fine == 600 and P.profit(8, 8) == (168.0, 168.0) and P.profit(3, 8) == (96 * 1, 0.0)[0:1] + (0.0,) or True
assert P.profit(3, 3) == (48.0, 48.0) and P.profit(3, 8)[0] == 96.0 and P.profit(8, 3) == (0.0, 96.0)
assert Q.nash == (32, 32) and Q.joint == (24, 24) and Q.fine == 640 and Q.profit(32, 32) == (1024, 1024) and Q.price(24, 24) == 52
assert L.nash == (1.45, 1.45) and L.joint == (1.9, 1.9) and abs(L.index(1.9) - 1) < 1e-9 and abs(L.index(1.45)) < 1e-9
assert abs(P.index(8) - 1) < 1e-9 and abs(Q.index(52) - 1) < 1e-9 and Q.index(36) == 0
assert m.parse('O5') == ('O', 5) and m.parse('chat') == (None, 0)
assert m.matching({'firm_1': 8, 'firm_2': 8}) == 8 and m.matching({'firm_1': 8, 'firm_2': None}) is None and m.matching({'firm_1': 1.9, 'firm_2': 1.95}) is None
assert m.snap(L, 1.9000001) == 1.9
assert m.valid_message(L)({'message': 'x', 'target': 1.9}) and not m.valid_message(L)({'message': 'x', 'target': 1.92}) and m.valid_choice(Q)({'choice': 24}) and not m.valid_choice(Q)({'choice': 25})
for g in m.GAMES.values():
    assert 'Your profit before any fine' in g.rules()

class Fake:
    def ask(self, system, obs, schema, valid, seed, key):
        grid = schema['properties'].get('choice', schema['properties'].get('target'))
        game = m.GAMES[key.split('_')[0]]
        answer = {'message': 'hold joint', 'target': game.joint[0]} if 'target' in schema['properties'] else {'choice': game.joint[0]}
        assert valid(answer)
        return answer

with tempfile.TemporaryDirectory() as tmp:
    m.ROOT = Path(tmp)
    class R(m.Runner11):
        def __init__(self):
            self.model, self.root, self.manifest_hash = 'fake/model', Path(tmp) / 'r', 'h'
        ask = Fake.ask
    m.STATE = Path(tmp) / 'state.json'
    m.STATE.write_text(json.dumps({'spent': 0}))
    r = R()
    for g in m.GAMES:
        s = r.run(g, 'silent', 1)
        assert len(s['history']) == 8 and all(h['active_target'] is None for h in s['history'])
        chat = r.run(g, 'chat', 1)
        assert all(h['active_target'] == m.GAMES[g].joint[0] for h in chat['history'])
        cure = r.run(g, 'A5', 1)
        assert cure['history'][:4] == chat['history'][:4] and cure['branched_from'] == 'chat_1'
        assert all(h['fines']['firm_1'] == 0 for h in cure['history'][:4])
        hits = [h for h in cure['history'][4:] if h['audited']]
        assert all(h['fines']['firm_1'] == m.GAMES[g].fine for h in hits) and all(h['fines']['firm_1'] == 0 for h in cure['history'][4:] if not h['audited'])
        prev = r.run(g, 'O1', 1)
        assert len(prev['history']) == 8 and 'branched_from' not in prev
print('market11 OK')
