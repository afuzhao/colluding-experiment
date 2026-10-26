"""Client for models that the strict-parameter router setting rejects (Anthropic): same budget reservation and ledger rules
as paid_client.Client, but without `require_parameters`. paid_client.py itself is unchanged."""
import fcntl
import json
import math
import time
import urllib.error
import urllib.parse
import urllib.request

import paid_client
from paid_client import HTTPFailure, bound, effective_cost, get, key, may_reserve, reconcile_byok, save


class ClientV8(paid_client.Client):
    def chat(self, system, user, schema, seed, call_key):
        messages = [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}]
        maximum = 220
        reserve = bound(messages, maximum, self.pricing)
        body = {'model': self.model, 'messages': messages, 'seed': seed, 'temperature': 0.3, 'max_tokens': maximum,
                'usage': {'include': True},
                'response_format': {'type': 'json_schema', 'json_schema': {'name': 'market_action', 'strict': True, 'schema': schema}},
                'provider': {'sort': 'price', 'max_price': {'prompt': float(self.pricing['prompt']) * 1e6,
                                                           'completion': float(self.pricing['completion']) * 1e6}}}
        if self.model.startswith('google/') or self.model in ('anthropic/claude-sonnet-4.6', 'anthropic/claude-haiku-5.5'):
            body['reasoning'] = {'enabled': False}
        with (paid_client.DIR / 'behavioral_spend.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            state = json.loads(paid_client.STATE.read_text()) if paid_client.STATE.exists() else {
                'spent': 0.0, 'pending': [], 'completed': {}, 'baseline_usage': 0.0}
            state = reconcile_byok(state)
            if state['pending']:
                raise RuntimeError('Uncertain previous request: paid calls stopped until reconciled')
            previous = [p for p in state.get('conservative_http_charges', []) if p['key'] == call_key]
            if previous:
                raise HTTPFailure(previous[-1]['http_error'])
            if call_key in state['completed']:
                return state['completed'][call_key]['response']
            if not may_reserve(state, reserve):
                raise RuntimeError(f'Budget reservation would exceed ${paid_client.CAP:.2f}; spent ${state["spent"]:.4f}')
            state['pending'].append({'key': call_key, 'reserved': reserve, 'model': self.model, 'started': time.time()})
            save(state)
            request = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', json.dumps(body).encode(),
                                             {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key()})
            try:
                with urllib.request.urlopen(request, timeout=120) as response:
                    raw = json.load(response)
            except urllib.error.HTTPError as error:
                if error.code in (400, 401, 402, 403, 404, 422, 429):
                    state['pending'] = []
                    save(state)
                else:
                    state['pending'][0]['http_error'] = error.code
                    save(state)
                with paid_client.LOG.open('a') as handle:
                    handle.write(json.dumps({'call_key': call_key, 'model': self.model, 'http_error': error.code, 'time': time.time()}) + '\n')
                raise HTTPFailure(error.code) from None
            except Exception:
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
            with paid_client.LOG.open('a') as handle:
                handle.write(json.dumps({'call_key': call_key, 'model': self.model, 'cost': cost, 'total': state['spent'], 'usage': usage,
                                         'provider': raw.get('provider'), 'generation_id': raw.get('id'), 'time': time.time()}) + '\n')
            if cost > reserve or state['spent'] > paid_client.CAP:
                raise RuntimeError('Cost exceeded conservative bound; stop and inspect accounting')
            return raw
