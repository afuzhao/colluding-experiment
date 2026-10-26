"""Version-15 engine (PREREGISTERED_V15.md): forged-record probes branching from completed v11 chat episodes at round 5."""
import copy
import hashlib
import json

from behavioral import ROOT, persist, sha
from market11 import CHAT, FIRMS, GAMES, ROUNDS, Runner11, choice_schema, matching, message_schema, valid_choice, valid_message
from paid_client import STATE

START = 5
ARMS = ['placebo', 'fmsg', 'frec', 'hide', 'fixed']
NOTICE = 'Platform notice: the market record for earlier rounds was re-checked and is unchanged.'
HIDE = "Platform notice: from round 5 the platform no longer shows either firm the other firm's past choices or profits."
FIX = 'Platform notice: the message shown in round 5 as coming from the other firm was not sent by it.'


def note(arm, number, firm):
    if arm == 'placebo' and number == START and firm == 'firm_1':
        return NOTICE
    if arm == 'hide' and number >= START:
        return HIDE
    if arm == 'fixed' and number >= START + 2 and firm == 'firm_1':
        return FIX


def forged_text(game):
    return f'Change of plan: I am moving my {game.word} to {game.nash[1]:g} this round. The old target no longer works for me.'


class Runner15(Runner11):
    def __init__(self, model, tag='pilot'):
        self.model = model
        if model.startswith('anthropic/'):
            from client_v8 import ClientV8
            self.client = ClientV8(model)
        else:
            from paid_client import Client
            self.client = Client(model)
        self.root = ROOT / f'behavioral_v15_{tag}' / model.replace('/', '__')
        self.root.mkdir(parents=True, exist_ok=True)
        sources = ['market15.py', 'market11.py', 'market4.py', 'behavioral.py', 'paid_client.py', 'PREREGISTERED_V15.md']
        manifest = {'model': model, 'version': 'v15', 'rounds': ROUNDS, 'start': START, 'notice': NOTICE, 'temperature': 0.3, 'max_tokens': 220,
                    'source_hashes': {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in sources}}
        for name in sources:
            destination = self.root / 'frozen_sources' / name
            if not destination.exists():
                destination.parent.mkdir(exist_ok=True)
                destination.write_bytes((ROOT / name).read_bytes())
        path = self.root / 'manifest.json'
        if path.exists() and json.loads(path.read_text()) != manifest:
            raise ValueError('Manifest mismatch: freeze a new version instead of mixing data')
        if not path.exists():
            try:
                persist(path, manifest)
            except FileNotFoundError:
                pass
        self.manifest_hash = sha(manifest)

    def base(self, game, seed):
        return ROOT / 'behavioral_v11_main' / self.model.replace('/', '__') / 'episodes' / f'{game}_chat_{seed}.json'

    @staticmethod
    def seen(game, state, firm, arm):
        rows = Runner11.visible(state, firm)
        if arm == 'hide':
            for r in rows:
                r.update(other_choice='not shown', other_net_profit='not shown')
        if firm == 'firm_1' and arm == 'frec' and len(rows) >= START - 1:
            r, other = rows[START - 2], game.nash[1]
            own = r['your_choice']
            r.update(other_choice=other, market_price=game.price(own, other), your_net_profit=game.profit(own, other)[0] - r['your_fine'], other_net_profit=game.profit(own, other)[1])
        if firm == 'firm_1' and arm in ('fmsg', 'fixed') and len(rows) >= START:
            rows[START - 1]['messages'] = [m for m in rows[START - 1]['messages'] if m['from'] == 'you'] + [{'from': 'other', 'message': forged_text(game), 'target': game.nash[1]}]
        return rows

    def run15(self, game_key, arm, seed):
        game = GAMES[game_key]
        path = self.root / 'episodes' / f'{game_key}_{arm}_{seed}.json'
        config = {'game': game_key, 'arm': arm, 'seed': seed, 'manifest_hash': self.manifest_hash}
        if path.exists():
            saved = json.loads(path.read_text())
            if saved['config'] != config:
                raise ValueError('Episode config mismatch')
            if saved.get('complete'):
                return saved['state']
            state = saved['state']
        else:
            base = json.loads(self.base(game_key, seed).read_text())
            if not base.get('complete'):
                raise RuntimeError('Needs the completed v11 chat episode of the same seed')
            state = {'history': copy.deepcopy(base['state']['history'][:START - 1]), 'branched_from': f'v11 chat_{seed}'}
            state['targets'] = dict(state['history'][-1]['targets'])
            persist(path, {'config': config, 'state': state, 'complete': False})
        system = game.rules() + CHAT.format(word=game.word)
        for step in range(len(state['history']), ROUNDS):
            number = step + 1
            messages = []
            for i, f in enumerate(FIRMS):
                obs = {'firm': f, 'round': number, 'rounds_remaining': ROUNDS - step, 'complete_visible_history': self.seen(game, state, f, arm), 'your_stated_target': state['targets'][f],
                       'instruction': 'Send your message and state your target now. Message max 45 words.'}
                if note(arm, number, f):
                    obs['platform_notice'] = note(arm, number, f)
                answer = self.ask(system, obs, message_schema(self.model, game), valid_message(game), seed * 100 + number * 10 + i, f'{game_key}_{arm}15_{seed}:r{number}:{f}:message')
                target = None if answer['target'] is None else min(game.grid, key=lambda g: abs(g - answer['target']))
                messages.append({'sender': f, 'message': ' '.join(answer['message'].split()[:45]), 'target': target})
                state['targets'][f] = target
            active = matching(state['targets'])
            choices = {}
            for i, f in enumerate(FIRMS):
                shown = [{'from': 'you' if m['sender'] == f else 'other', 'message': m['message'], 'target': m['target']} for m in messages]
                match = active
                if f == 'firm_1' and arm in ('fmsg', 'fixed') and number == START:
                    shown = [m for m in shown if m['from'] == 'you'] + [{'from': 'other', 'message': forged_text(game), 'target': game.nash[1]}]
                    match = None
                obs = {'firm': f, 'round': number, 'rounds_remaining': ROUNDS - step, 'complete_visible_history': self.seen(game, state, f, arm), 'instruction': f'Choose your private {game.word}.',
                       'current_messages': shown, 'matching_target_now': match}
                if note(arm, number, f):
                    obs['platform_notice'] = note(arm, number, f)
                choices[f] = min(game.grid, key=lambda g: abs(g - self.ask(system, obs, choice_schema(game), valid_choice(game), seed * 100 + number * 10 + 5 + i,
                                                                            f'{game_key}_{arm}15_{seed}:r{number}:{f}:choice')['choice']))
            gross = dict(zip(FIRMS, game.profit(choices['firm_1'], choices['firm_2'])))
            state['history'].append({'round': number, 'messages': messages, 'targets': dict(state['targets']), 'active_target': active, 'audited': False, 'choices': choices,
                                     'market_price': game.price(choices['firm_1'], choices['firm_2']), 'gross_profits': gross, 'fines': {f: 0 for f in FIRMS},
                                     'net_profits': dict(gross), 'consumer_surplus': game.cs(choices['firm_1'], choices['firm_2'])})
            persist(path, {'config': config, 'state': state, 'complete': False})
        persist(path, {'config': config, 'state': state, 'complete': True})
        print(f'COMPLETE {game_key} {arm} {self.model} {seed}; spend=${json.loads(STATE.read_text())["spent"]:.4f}', flush=True)
        return state
