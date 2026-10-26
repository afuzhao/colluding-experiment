"""Read-only credential/price check. Never prints credentials."""
import json
import urllib.request
from pathlib import Path


def key():
    for line in (Path.home() / '.config/apart/openrouter.env').read_text().splitlines():
        if line.startswith('OPENROUTER_API_KEY='):
            return line.split('=', 1)[1].strip()
    raise RuntimeError('Credential not found')


def get(path):
    request = urllib.request.Request('https://openrouter.ai/api/v1/' + path,
                                     headers={'Authorization': 'Bearer ' + key()})
    with urllib.request.urlopen(request, timeout=120) as response:
        return json.load(response)


if __name__ == '__main__':
    auth = get('auth/key')['data']
    print(json.dumps({k: auth.get(k) for k in ('usage', 'limit', 'limit_remaining', 'is_free_tier')}))
    catalog = get('models')['data']
    selected = [m for m in catalog if m['id'] in (
        'google/gemini-2.5-flash-lite', 'openai/gpt-4.1-mini', 'meta-llama/llama-3.1-8b-instruct')]
    for model in selected:
        print(json.dumps({k: model.get(k) for k in ('id', 'pricing', 'context_length', 'supported_parameters')}))
    destination = Path(__file__).parent / 'provider_snapshot.json'
    destination.write_text(json.dumps({'auth_usage_baseline': auth.get('usage'), 'models': selected}, indent=2) + '\n')
