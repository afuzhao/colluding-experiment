"""Local structured inference with pinned weights and exact-request replay."""
import json, time, urllib.request
from pathlib import Path
from .utils import digest, append_json

class LocalClient:

    def __init__(self, c, output):
        self.c = c
        self.output = Path(output)
        self.output.mkdir(parents=True, exist_ok=True)
        self.cache = {}
        self.calls = 0
        self.replayed = 0
        tags = self.http('/api/tags')
        model = next((m for m in tags['models'] if m['name'] == c['model']['id']), None)
        if not model:
            raise RuntimeError('Requested model is not installed; no fallback')
        self.identity = {'model': model['name'], 'digest': model['digest'], 'details': model.get('details', {})}
        p = self.output / 'model_identity.json'
        if p.exists() and json.loads(p.read_text()) != self.identity:
            raise RuntimeError('Model identity changed')
        p.write_text(json.dumps(self.identity, indent=2))
        self.journal = self.output / 'calls.jsonl'
        if self.journal.exists():
            for line in self.journal.read_text().splitlines():
                row = json.loads(line)
                self.cache[row['request_hash']] = row

    def http(self, path, body=None):
        req = urllib.request.Request(self.c['model']['base_url'] + path, data=json.dumps(body).encode() if body else None, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=self.c['model']['timeout_seconds']) as f:
            return json.load(f)

    def generate(self, system, obs, schema, seed, validator, tag):
        m = self.c['model']
        legacy=tag.get('condition')=='formation'
        encoded=json.dumps(obs) if legacy else json.dumps(obs,separators=(',',':'),ensure_ascii=False)
        body = {'model': m['id'], 'stream': False, 'think': False, 'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': encoded}], 'format': schema, 'keep_alive': '30m', 'options': {'temperature': m['temperature'], 'top_p': m['top_p'], 'seed': seed, 'num_ctx': m['context_tokens'], 'num_predict': m['max_completion_tokens'] if legacy else m.get('message_max_tokens',200) if set(schema.get('properties',{}))=={'message','quota_commitment'} else m['max_completion_tokens']}}
        key = digest({'identity': self.identity, 'body': body})
        if key in self.cache:
            self.replayed += 1
            out = self.cache[key]['parsed']
            validator(out)
            append_json(self.output/'request_positions.jsonl', {'tag':tag,'request_hash':key,'replayed':True})
            return out
        if len(json.dumps(body).encode()) + 1024 + m['max_completion_tokens'] >= m['context_tokens']:
            raise RuntimeError('Context guard reached; no truncation')
        start = time.monotonic()
        raw = self.http('/api/chat', body)
        row = {'request_hash': key, 'tag': tag, 'request': body, 'response': raw, 'seconds': round(time.monotonic() - start, 3)}
        try:
            if raw.get('model') != m['id'] or raw.get('done_reason') != 'stop':
                raise ValueError('Incomplete answer or wrong model')
            if raw.get('prompt_eval_count', 0) + m['max_completion_tokens'] >= m['context_tokens']:
                raise ValueError('Context limit')
            out = json.loads(raw['message']['content'])
            validator(out)
        except Exception:
            with (self.output / 'invalid_responses.jsonl').open('a') as f:
                f.write(json.dumps(row) + '\n')
            raise
        row['parsed'] = out
        with self.journal.open('a') as f:
            f.write(json.dumps(row) + '\n')
        self.cache[key] = row
        append_json(self.output/'request_positions.jsonl', {'tag':tag,'request_hash':key,'replayed':False})
        self.calls += 1
        return out
