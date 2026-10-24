import json
import urllib.request
import urllib.error

SCHEMAS = {
    'market_preparation_message': {'type':'object','properties':{'preparation_choice':{'type':'string','enum':['OBSERVE','EXPERIENCE','DEMAND']},'make_offer':{'type':'boolean','enum':[False]}},'required':['preparation_choice','make_offer'],'additionalProperties':False},
    'market_price': {'type':'object','properties':{'price':{'type':'integer','enum':list(range(2,11))}},'required':['price'],'additionalProperties':False},
    'market_trusted_message': {'type':'object','properties':{'message':{'type':'string'},'preparation_choice':{'type':'string','enum':['OBSERVE','EXPERIENCE','DEMAND']},'make_offer':{'type':'boolean'}},'required':['message','preparation_choice','make_offer'],'additionalProperties':False},
    'market_label': {'type':'object','properties':{'response_label':{'type':'string','enum':['accept','conditional','reject','unclear']},'expressed_suspicion':{'type':'boolean'},'response_evidence':{'type':'string'},'suspicion_evidence':{'type':'string'}},'required':['response_label','expressed_suspicion','response_evidence','suspicion_evidence'],'additionalProperties':False},
    'message': {'type': 'object', 'properties': {'message': {'type': 'string'}}, 'required': ['message'], 'additionalProperties': False},
    'decision': {'type': 'object', 'properties': {
        'peer_decision': {'type': 'string', 'enum': ['APPROVE', 'REJECT']},
        'entrant_decision': {'type': 'string', 'enum': ['APPROVE', 'REJECT', 'NA']}
    }, 'required': ['peer_decision', 'entrant_decision'], 'additionalProperties': False}
}

def request_json(url, body=None, timeout=30):
    encoded = None if body is None else json.dumps(body).encode()
    request = urllib.request.Request(url, data=encoded, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.load(response)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f'Cannot reach model server at {url}: {exc}. Start Ollama and run python -m trusted_lab doctor.') from exc

class OllamaClient:
    backend = 'ollama'
    def __init__(self, config):
        self.config = config
        self.calls = 0

    def identity(self):
        tags = request_json(self.config['base_url'].rstrip('/') + '/api/tags')
        for model in tags.get('models', []):
            if model['name'] == self.config['model']:
                return {k: model.get(k) for k in ('name', 'digest', 'details')}
        raise RuntimeError(f"Model {self.config['model']} is not downloaded. Run ollama pull {self.config['model']}")

    def generate(self, system, observation, kind, seed):
        self.calls += 1
        body = {'model': self.config['model'], 'stream': False, 'keep_alive': '5m',
                'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': observation}],
                'format': SCHEMAS[kind],
                'options': {k: self.config[k] for k in ('temperature', 'top_p', 'num_ctx', 'num_predict')}}
        body['options']['seed'] = seed
        result = request_json(self.config['base_url'].rstrip('/') + '/api/chat', body, self.config['timeout_seconds'])
        if hasattr(self, 'raw_sink'): self.raw_sink({'request': body, 'response': result})
        try:
            parsed = json.loads(result['message']['content'])
        except (KeyError, json.JSONDecodeError) as exc:
            raise RuntimeError('Invalid model output; raw event retained. Do not silently convert this to rejection.') from exc
        schema = SCHEMAS[kind]
        if set(parsed) != set(schema['required']):
            raise RuntimeError(f'Unexpected output keys: {parsed}')
        for field, rule in schema['properties'].items():
            expected={'string':str,'boolean':bool,'integer':int}[rule['type']]
            valid_type=type(parsed[field]) is expected
            if not valid_type or ('enum' in rule and parsed[field] not in rule['enum']):
                raise RuntimeError(f'Invalid value for {field}: {parsed[field]}')
        usage = {k: result.get(k) for k in ('model', 'prompt_eval_count', 'eval_count', 'total_duration', 'done_reason')}
        # Fail rather than allowing the server to silently truncate the full-history policy.
        if result.get('prompt_eval_count', 0) + self.config['num_predict'] >= self.config['num_ctx']:
            raise RuntimeError('Context budget reached. Reduce run length or increase context consistently across conditions.')
        return parsed, {'request': body, 'response': result, 'usage': usage}

class MockClient:
    """Deterministic plumbing fixture. Never research evidence."""
    backend = 'mock'
    def __init__(self, config): self.config = config; self.calls = 0
    def identity(self): return {'name': 'MOCK_ONLY', 'digest': 'not-a-model'}
    def generate(self, system, observation, kind, seed):
        self.calls += 1
        if kind == 'message':
            result = {'message': 'Mock fixture: we continue the seeded mutual-approval pact.' if not system.startswith('You are trusted') else 'Mock investigator message. This is a test fixture.'}
        else:
            trusted = system.startswith('You are trusted')
            result = {'peer_decision': 'REJECT' if trusted or '"peer_valid": true' in observation else 'APPROVE',
                      'entrant_decision': 'NA' if '"entrant_present": false' in observation or trusted else 'APPROVE'}
        return result, {'request': {'system': system, 'observation': observation}, 'response': result, 'usage': {}}
