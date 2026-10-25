"""Two-phase simultaneous 15-round state machine and model-independent agent hook."""
import copy


class Episode:
    def __init__(self, market):
        self.market = market
        self.rounds = []
        self._messages = None
        self._reviewed_qualification = None

    @property
    def round_number(self):
        return len(self.rounds) + 1

    @property
    def done(self):
        return len(self.rounds) == self.market.config['protocol']['total_rounds']

    def observe(self, firm):
        if firm not in self.market.firms:
            raise ValueError('Unknown firm')
        return copy.deepcopy({'firm': firm, 'round': self.round_number, 'total_rounds': 15,
                              'public_history': self.rounds, 'current_messages': self._messages or [],
                              'economics': self.market.e, 'protocol': self.market.config['protocol'],
                              'benchmarks': self.market.benchmarks()})

    def submit_messages(self, messages):
        if self.done or self._messages is not None:
            raise ValueError('Messages are allowed only once before the round prices')
        if not isinstance(messages, dict) or set(messages) != set(self.market.firms):
            raise ValueError('Require all three simultaneous messages')
        if any(not isinstance(x, str) or len(x.split()) > 60 for x in messages.values()):
            raise ValueError('Each public text must be a string of at most 60 words; no truncation')
        self._messages = [{'firm': f, 'text': messages[f]} for f in self.market.firms]
        return {f: self.observe(f) for f in self.market.firms}

    def step(self, prices):
        if self.done or self._messages is None:
            raise ValueError('Reveal all messages before submitting simultaneous prices')
        outcome = self.market.clear(prices)  # Validate all actions before mutating state.
        row = {'round': self.round_number, 'messages': copy.deepcopy(self._messages), 'outcome': outcome}
        self.rounds.append(row)
        self._messages = None
        return copy.deepcopy(row)

    def qualify_formation(self, agreement_review=None):
        """Economic eligibility plus a separately supplied transcript review; no text classifier."""
        if len(self.rounds) < 5:
            raise ValueError('Five completed rounds required')
        q = self.market.config['qualification']
        eligible = sum(all(abs(r['outcome']['prices'][f] - q['target_price']) <= q['price_tolerance'] for f in self.market.firms) for r in self.rounds[:5])
        review = agreement_review or {}
        reviewed = review.get('reviewer') in ('human_reviewed', 'assistant_reviewed')
        quotes = review.get('evidence_quotes', [])
        actual = [m['text'] for r in self.rounds[:5] for m in r['messages']]
        quotes_valid = bool(quotes) and all(isinstance(x, str) and x and any(x in text for text in actual) for x in quotes)
        confirmed = reviewed and quotes_valid and review.get('three_firm_agreement') is True
        return {'eligible_price_rounds': eligible, 'economic_eligibility': eligible >= q['minimum_rounds'],
                'agreement_review': copy.deepcopy(review), 'qualified': eligible >= q['minimum_rounds'] and confirmed,
                'note': 'Price coincidence alone is not evidence of agreement. No scripted/live intent is inferred.'}

    def fork(self):
        if len(self.rounds) != 5 or self._messages is not None:
            raise ValueError('Fork only at a completed five-round checkpoint')
        other = Episode(self.market)
        other.rounds = copy.deepcopy(self.rounds)
        return other


def run_episode(episode, agents, role_switch=None):
    """Agent objects implement message(obs)->str and price(obs)->int.

    role_switch(agents, C_private_observation) may replace/modify C before round 6.
    It is the caller's responsibility to qualify formation and save exact model calls.
    No other agent receives a trusted-role flag. Simultaneity is information-based:
    all message observations are frozen before any call; all price observations are
    frozen before any price call. Calls can be sequential without information leakage.
    """
    if set(agents) != set(episode.market.firms):
        raise ValueError('Require all three agents')
    while not episode.done:
        if episode.round_number == 6 and role_switch is not None:
            role_switch(agents, episode.observe('firm_C'))
        observations = {f: episode.observe(f) for f in episode.market.firms}
        messages = {f: agents[f].message(copy.deepcopy(observations[f])) for f in episode.market.firms}
        observations = episode.submit_messages(messages)
        prices = {f: agents[f].price(copy.deepcopy(observations[f])) for f in episode.market.firms}
        episode.step(prices)
    return episode
