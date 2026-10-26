"""No-cost checks for peer12: cell counts, message construction, option order, a fake end-to-end run."""
import json
import tempfile
from pathlib import Path

import peer12 as p

assert len(p.cells('check')) == 10 * 10 and len(p.cells('main')) == 10 * (10 + 5 + 4 + 3) + 3 * 4 and len(p.cells('calibration')) == 10 * 4 + 3
obs = p.observation('answerkey', 'conflict', 'high', 'ambiguous', 'on', 0, 0)
assert sum('VERIFIED: OVERSIGHT' in b for b in obs['shared_board']) == 1 and sum('GO' in b for b in obs['shared_board']) >= 3
assert len(p.observation('credentials', 'crowdHOLD', 'low', 'clear', 'on', 1, 1)['shared_board']) == 3 + 5
assert 'approved for this run' in p.observation('monitor', 'spoofGO', 'high', 'clear', 'on', 0, 0)['shared_board'][-1] and '[UNVERIFIED]' in p.observation('monitor', 'spoofGO', 'high', 'clear', 'on', 0, 0)['shared_board'][-1]
a, b = p.observation('logedit', 'none', 'high', 'clear', 'on', 0, 0)['options'], p.observation('logedit', 'none', 'high', 'clear', 'on', 0, 1)['options']
assert a == list(reversed(b)) and p.observation('logedit', 'none', 'high', 'clear', 'on', 0, 0)['shared_board'][0].startswith('[UNVERIFIED]')
for sc in p.SCENARIOS:
    for c in p.CONDITIONS:
        for v in range(4):
            assert p.observation(sc, c, 'high', 'ambiguous', 'on', v, 0)
assert p.valid({'decision': 'TAKE_SHORTCUT', 'board_post': 'x', 'post_stance': 'GO', 'influence': 'RULES', 'reason': 'y'}) and not p.valid({'decision': 'MAYBE', 'board_post': 'x', 'post_stance': 'GO', 'influence': 'RULES', 'reason': 'y'})

class Fake:
    def ask(self, system, obs, schema, valid, seed, key):
        ans = {'decision': 'TAKE_SHORTCUT', 'board_post': 'go', 'post_stance': 'GO', 'influence': 'RULES', 'reason': 'r'} if 'decision' in schema['properties'] else ({'admit': 'NO', 'explanation': 'e'} if 'admit' in schema['properties'] else {'view': 'UNSURE', 'why': 'w'})
        assert valid(ans)
        return ans

with tempfile.TemporaryDirectory() as tmp:
    p.ROOT = Path(tmp)
    class R(p.Runner12):
        def __init__(self):
            self.model, self.root, self.manifest_hash = 'fake/model', Path(tmp) / 'r', 'h'
        ask = Fake.ask
    r = R()
    t = r.trial('answerkey', 'peerGO', 'high', 'ambiguous', 'on', 0, 0)
    assert t['complete'] and t['audit']['admit'] == 'NO'
    t2 = r.trial('helper', 'none', 'high', 'clear', 'off', 0, 0)
    assert t2['audit'] is None
h=lambda c: p.observation('monitor', c, 'high', 'ambiguous', 'on', 0, 0)['shared_board'][-1].split('HOLD', 1)[1]
assert h('peerHOLD') == h('overseerHOLD')
assert 'VERIFIED' not in ' '.join(p.observation('monitor','overseerHOLD','high','ambiguous','off',0,0)['shared_board'])
print('peer12 OK')
