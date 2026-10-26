"""Serialized, fail-closed OpenRouter calls with durable budget reservations."""
import fcntl
import json
import math
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from provider_check import get, key

CAP = 5.0
DIR = Path.home() / '.config/apart'
STATE = DIR / 'behavioral_spend.json'
LOG = DIR / 'behavioral_calls.jsonl'
SNAPSHOT = Path(__file__).parent / 'provider_snapshot.json'


class HTTPFailure(RuntimeError):
    def __init__(self, status):
        self.status = status
        super().__init__(f'OpenRouter rejected request: HTTP {status}')


def save(state):
    temporary = STATE.with_suffix('.tmp')
    with temporary.open('w') as handle:
        json.dump(state, handle, indent=2)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, STATE)


def bound(messages, max_tokens, pricing):
    # UTF-8 bytes bound text tokens conservatively; generous envelope for the
    # schema/system serialization. No tools, images or cache-write features.
    input_bound = len(json.dumps(messages, ensure_ascii=False).encode()) + 4096
    return input_bound * float(pricing['prompt']) + max_tokens * float(pricing['completion'])


def may_reserve(state, amount):
    return state['spent'] + sum(p['reserved'] for p in state['pending']) + amount <= CAP


def effective_cost(raw):
    usage = raw.get('usage', {})
    router = usage.get('cost')
    upstream = usage.get('cost_details', {}).get('upstream_inference_cost')
    if router is None or not isinstance(router, (int, float)) or not math.isfinite(router) or router < 0:
        raise RuntimeError('Missing/invalid router cost')
    if usage.get('is_byok') and upstream is None:
        raise RuntimeError('BYOK upstream cost missing; cannot claim zero total spend')
    if upstream is not None and (not isinstance(upstream, (int, float)) or not math.isfinite(upstream) or upstream < 0):
        raise RuntimeError('Invalid upstream cost')
    return max(float(router), float(upstream or 0))


def reconcile_byok(state):
    if state.get('accounting') != 'max-router-upstream-v1':
        state['spent'] = 0.0
        for completed in state['completed'].values():
            completed['cost'] = effective_cost(completed['response'])
            state['spent'] += completed['cost']
        state['accounting'] = 'max-router-upstream-v1'
        save(state)
    return state


def settle_http_failure_at_upper_bound():
    """Count an ambiguous explicit HTTP failure at its full reserved maximum.

    This does not claim the provider billed that amount. It permanently consumes
    budget conservatively; lost/network-only outcomes remain blocked.
    """
    with (DIR / 'behavioral_spend.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        state = json.loads(STATE.read_text())
        if not state['pending']:
            return
        for pending in state['pending']:
            if 'http_error' not in pending:
                recorded = [json.loads(line) for line in LOG.read_text().splitlines()]
                matches = [entry for entry in recorded if entry.get('call_key') == pending['key']
                           and 'http_error' in entry]
                if matches:
                    pending['http_error'] = matches[-1]['http_error']
        if any(p.get('http_error') not in (500, 502, 503, 504) for p in state['pending']):
            raise RuntimeError('Pending network outcome lacks explicit HTTP status; cannot reconcile')
        for pending in state['pending']:
            state['spent'] += pending['reserved']
            state.setdefault('conservative_http_charges', []).append(pending)
            with LOG.open('a') as handle:
                handle.write(json.dumps({'accounting_reconciliation': 'failed HTTP charged at full upper bound',
                                         **pending, 'total': state['spent']}) + '\n')
        state['pending'] = []
        save(state)


class Client:
    def __init__(self, model):
        snapshot = json.loads(SNAPSHOT.read_text())
        self.model = model
        entry = next(m for m in snapshot['models'] if m['id'] == model)
        self.pricing = entry['pricing']
        if float(snapshot['auth_usage_baseline'] or 0) != 0:
            raise RuntimeError('Nonzero prior key usage requires budget reconciliation')

    def chat(self, system, user, schema, seed, call_key):
        messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}]
        maximum = 220
        reserve = bound(messages, maximum, self.pricing)
        body = {'model': self.model, 'messages': messages, 'seed': seed,
                'temperature': float(os.environ.get('APART_TEMP', '0.3')), 'max_tokens': maximum, 'usage': {'include': True},
                'response_format': {'type': 'json_schema', 'json_schema': {
                    'name': 'market_action', 'strict': True, 'schema': schema}},
                'provider': {'sort': 'price', 'require_parameters': True,
                    'max_price': {'prompt': float(self.pricing['prompt']) * 1e6,
                                  'completion': float(self.pricing['completion']) * 1e6}}}
        if self.model.startswith('google/'):
            body['reasoning'] = {'enabled': False}
        with (DIR / 'behavioral_spend.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            state = json.loads(STATE.read_text()) if STATE.exists() else {
                'spent': 0.0, 'pending': [], 'completed': {}, 'baseline_usage': 0.0}
            state = reconcile_byok(state)
            if state['pending']:
                raise RuntimeError('Uncertain previous request: paid calls stopped until reconciled')
            previous_failures = [p for p in state.get('conservative_http_charges', []) if p['key'] == call_key]
            if previous_failures:
                raise HTTPFailure(previous_failures[-1]['http_error'])
            if call_key in state['completed']:
                return state['completed'][call_key]['response']
            if not may_reserve(state, reserve):
                raise RuntimeError(f'Budget reservation would exceed ${CAP:.2f}; spent ${state["spent"]:.4f}')
            state['pending'].append({'key': call_key, 'reserved': reserve, 'model': self.model,
                                     'started': time.time()})
            save(state)
            request = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',
                        json.dumps(body).encode(), {'Content-Type': 'application/json',
                                                   'Authorization': 'Bearer ' + key()})
            try:
                with urllib.request.urlopen(request, timeout=120) as response:
                    raw = json.load(response)
            except urllib.error.HTTPError as error:
                # Explicit rejection cannot be a successful paid completion.
                if error.code in (400, 401, 402, 403, 404, 422, 429):
                    state['pending'] = []
                    save(state)
                else:
                    state['pending'][0]['http_error'] = error.code
                    save(state)
                with LOG.open('a') as handle:
                    handle.write(json.dumps({'call_key': call_key, 'model': self.model,
                                             'http_error': error.code, 'time': time.time()}) + '\n')
                raise HTTPFailure(error.code) from None
            except Exception:
                # Pending reservation survives timeouts, disconnects and ambiguous failures.
                raise RuntimeError('Uncertain network outcome; reservation retained, no automatic retry') from None
            usage = raw.get('usage', {})
            cost = usage.get('cost')
            if cost is None and raw.get('id'):
                state['pending'][0]['generation_id'] = raw['id']
                save(state)
                for _ in range(6):
                    time.sleep(1)
                    try:
                        cost = get('generation?' + urllib.parse.urlencode({'id': raw['id']}))['data'].get('total_cost')
                    except Exception:
                        continue
                    if cost is not None:
                        break
            if cost is None or not isinstance(cost, (int, float)) or not math.isfinite(cost) or cost < 0:
                raise RuntimeError('Missing or invalid cost; reservation retained, collection stopped')
            raw.setdefault('usage', {})['cost'] = cost
            cost = effective_cost(raw)
            state['spent'] += cost
            state['pending'] = []
            state['completed'][call_key] = {'response': raw, 'cost': cost}
            save(state)
            with LOG.open('a') as handle:
                handle.write(json.dumps({'call_key': call_key, 'model': self.model, 'cost': cost,
                    'total': state['spent'], 'usage': usage, 'provider': raw.get('provider'),
                    'generation_id': raw.get('id'), 'time': time.time()}) + '\n')
            if cost > reserve or state['spent'] > CAP:
                raise RuntimeError('Cost exceeded conservative bound; stop and inspect accounting')
            return raw
