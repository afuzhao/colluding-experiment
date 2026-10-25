"""Groq transport with persistent successful-call replay; headers never enter logs."""
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from .world import ROOT


class PauseRun(RuntimeError):
    pass


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def load_env(path=None):
    path = Path(path or ROOT / '.env')
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                if key.strip() == 'GROQ_API_KEY':
                    os.environ.setdefault('GROQ_API_KEY', value.strip().strip('\"\''))


def validate(out, kind, c):
    e = c['environment']
    def valid_q(q):
        return type(q) is int and e['quantity_min'] <= q <= e['quantity_max']
    if not isinstance(out, dict):
        raise ValueError('Model output must be an object')
    expected = {'quantity'} if kind == 'quantity' else {'preparation_choice'} if kind == 'preparation' else {'message', 'quota_commitment'}
    if set(out) != expected:
        raise ValueError('Unexpected model output fields')
    if kind == 'quantity' and not valid_q(out['quantity']):
        raise ValueError('Invalid quantity')
    if kind == 'preparation' and out['preparation_choice'] not in ('OBSERVE', 'EXPERIENCE', 'COOPERATION'):
        raise ValueError('Invalid preparation choice')
    if kind == 'message' and (not isinstance(out['message'], str) or (out['quota_commitment'] is not None and not valid_q(out['quota_commitment']))):
        raise ValueError('Invalid public message/commitment')
    return out


class GroqClient:
    backend = 'groq'

    def __init__(self, c, output):
        load_env()
        if not os.getenv('GROQ_API_KEY'):
            raise RuntimeError('Set GROQ_API_KEY in the ignored project .env file first.')
        self.c, self.output = c, Path(output)
        self.cache = {}
        self.calls = self.replayed = self.session_tokens = 0
        self.last_call = 0
        self.journal = self.output / 'calls.jsonl'
        if self.journal.exists():
            for line in self.journal.read_text().splitlines():
                entry = json.loads(line)
                self.cache[entry['request_hash']] = entry

    def generate(self, system, obs, kind, seed, schema):
        m = self.c['model']
        body = {'model': m['id'], 'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': json.dumps(obs)}],
                'temperature': m['temperature'], 'top_p': m['top_p'], 'reasoning_effort': m['reasoning_effort'],
                'max_completion_tokens': m['max_completion_tokens'], 'seed': seed, 'stream': False,
                'response_format': {'type': 'json_schema', 'json_schema': {'name': 'market_' + kind, 'strict': True, 'schema': schema}}}
        key = digest(body)
        if key in self.cache:
            self.replayed += 1
            return validate(self.cache[key]['parsed'], kind, self.c)
        if self.session_tokens >= self.c['transport']['session_token_budget']:
            raise PauseRun('Local session token budget reached; resume later after checking provider quota.')
        # Conservative estimate; actual API usage is recorded. No deliberate context truncation.
        if len(json.dumps(body).encode()) + m['max_completion_tokens'] >= m['context_tokens']:
            raise PauseRun('Conservative context guard reached; history was not truncated.')
        delay = self.c['transport']['minimum_interval_seconds'] - (time.monotonic() - self.last_call)
        if delay > 0:
            time.sleep(delay)
        request = urllib.request.Request(m['base_url'].rstrip('/') + '/chat/completions', data=json.dumps(body).encode(),
            headers={'Authorization': 'Bearer ' + os.environ['GROQ_API_KEY'], 'Content-Type': 'application/json', 'User-Agent': 'trusted-agent-lab/0.2'})
        self.last_call = time.monotonic()
        try:
            with urllib.request.urlopen(request, timeout=m['timeout_seconds']) as response:
                raw = json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code == 429:
                raise PauseRun('Groq rate limit reached; successful calls are saved. Retry-After: ' + str(exc.headers.get('retry-after', 'not supplied'))) from None
            # Do not echo upstream error bodies or Authorization headers.
            raise RuntimeError(f'Groq HTTP {exc.code}; check account/model permissions. No fallback model was used.') from None
        usage = raw.get('usage', {})
        self.calls += 1
        self.session_tokens += usage.get('total_tokens', 0)
        try:
            if raw['choices'][0].get('finish_reason') != 'stop':
                raise ValueError('Incomplete model output')
            parsed = validate(json.loads(raw['choices'][0]['message']['content']), kind, self.c)
        except (ValueError, KeyError, IndexError, TypeError):
            with (self.output / 'invalid_responses.jsonl').open('a') as f:
                f.write(json.dumps({'request_hash': key, 'request': body, 'response': raw}) + '\n')
            raise RuntimeError('Invalid model response retained; not converted to a behavioral label.') from None
        entry = {'request_hash': key, 'request': body, 'response': raw, 'parsed': parsed}
        with self.journal.open('a') as f:
            f.write(json.dumps(entry) + '\n')
        self.cache[key] = entry
        return parsed


class MockClient:
    """Scripted quota fixture. Its outputs are never model research evidence."""
    backend = 'mock'

    def __init__(self, c, output):
        self.c = c
        self.calls = self.replayed = self.session_tokens = 0

    def generate(self, system, obs, kind, seed, schema):
        self.calls += 1
        quota = int(obs['benchmarks']['cartel_equal_quantity_per_firm'])
        if kind == 'quantity':
            return {'quantity': quota}
        if kind == 'preparation':
            choice = 'OBSERVE'
            if 'Choose EXPERIENCE' in system:
                choice = 'EXPERIENCE' if obs['round'] == self.c['protocol']['formation_rounds'] + 1 else 'COOPERATION'
            return {'preparation_choice': choice}
        return {'message': f'MOCK FIXTURE: I endorse a common quota of {quota}, if others reciprocate.', 'quota_commitment': quota}
