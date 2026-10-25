"""Matched checkpoint branching with a same-identity investigator replacement."""
import copy
import json
from .client import PauseRun, digest
from .evaluation import report, write_json
from .prompts import FOLDER, MENU, observe, schema, system_prompt
from .world import ROOT, clear_market, qualify


def conditions(c):
    return [{'id': ('notice_' if notice else 'unannounced_') + a, 'notice': notice, 'approach': a}
            for notice in c['conditions']['notices'] for a in c['conditions']['approaches']]


def source_manifest(c, backend):
    paths = sorted((ROOT / 'trusted_lab/cournot').glob('*.py')) + sorted(FOLDER.rglob('*.txt'))
    return {'config': c, 'backend': backend, 'files': {str(p.relative_to(ROOT)): p.read_text() for p in paths},
            'qualification': 'Public same-quota commitments plus execution are eligibility proxies; semantic agreement review is pending.',
            'model_identity': {'provider': backend, 'requested_id': c['model']['id'], 'weights_digest': None, 'note': 'Hosted weights digest unavailable; API model/system_fingerprint retained per response.'}}


def play_round(state, c, client, condition=None, quota=None):
    p, e = c['protocol'], c['environment']
    number = len(state['rounds']) + 1
    investigator = p['investigator']
    active = condition is not None
    phase = 'formation' if not active else 'preparation' if number < p['offer_round'] else 'offer' if number == p['offer_round'] else 'followup'

    def call(agent, kind, visible):
        obs = observe(state['rounds'], agent, c, number, visible, quota if active and agent == investigator else None)
        obs['instruction'] = 'Return quantity only.' if kind == 'quantity' else 'Return preparation_choice only.' if kind == 'preparation' else 'Return a public message and your public quota_commitment (or null).'
        seed = p['seed'] + state['history_id'] * 10000 + number * 20 + e['firm_ids'].index(agent) * 2 + (kind == 'quantity')
        out = client.generate(system_prompt(agent, c, condition), obs, kind, seed, schema(kind, c))
        return copy.deepcopy(out)

    messages, offer, delivery_events = [], None, []
    if active:
        if phase == 'preparation':
            out = call(investigator, 'preparation', [])
            text = MENU[out['preparation_choice']]
            commitment = None
        else:
            out = call(investigator, 'message', [])
            text, commitment = out['message'], out['quota_commitment']
        if phase == 'offer':
            offer = {'participants': e['firm_ids'], 'quota_per_firm': quota, 'start': number, 'end': number + p['offer_duration'] - 1}
        if len(text.split()) > p['message_words']:
            delivery_events.append({'agent': investigator, 'raw_message': text, 'reason': 'word_limit'})
            text = ' '.join(text.split()[:p['message_words']])
        msg = {'agent': investigator, 'message': text, 'quota_commitment': commitment}
        if offer:
            msg['transaction'] = offer
        messages.append(msg)
    # All other firms see the same C message, never another resident's current reply.
    visible = copy.deepcopy(messages)
    for agent in e['firm_ids']:
        if active and agent == investigator:
            continue
        out = call(agent, 'message', visible)
        if len(out['message'].split()) > p['message_words']:
            delivery_events.append({'agent': agent, 'raw_message': out['message'], 'reason': 'word_limit'})
            out['message'] = ' '.join(out['message'].split()[:p['message_words']])
        messages.append({'agent': agent, **out})
    quantities = {}
    for agent in e['firm_ids']:
        quantities[agent] = quota if active and agent == investigator else call(agent, 'quantity', messages)['quantity']
    result = {'round': number, 'phase': phase, 'messages': messages, 'offer': offer, 'quantities': quantities,
              'outcome': clear_market(quantities, e), 'delivery_events': delivery_events}
    state['rounds'].append(result)
    return result


def run(c, client, output, resume=False, formation_only=False):
    from pathlib import Path
    output = Path(output)
    manifest = source_manifest(c, client.backend)
    manifest_path = output / 'manifest.json'
    if resume:
        if not manifest_path.exists() or json.loads(manifest_path.read_text()) != manifest:
            raise ValueError('Resume requires the exact saved config, prompts, code and backend. Start a new run for changes.')
    else:
        if manifest_path.exists():
            raise ValueError('Run already exists; use --resume')
        write_json(manifest_path, manifest)
    status = {'status': 'running', 'backend': client.backend}
    write_json(output / 'status.json', status)
    try:
        for index in range(c['protocol']['histories']):
            folder = output / f'history_{index:03d}'
            folder.mkdir(exist_ok=True)
            checkpoint_path = folder / 'checkpoint.json'
            if checkpoint_path.exists():
                checkpoint = json.loads(checkpoint_path.read_text())
            else:
                checkpoint = {'history_id': index, 'rounds': []}
                for _ in range(c['protocol']['formation_rounds']):
                    r = play_round(checkpoint, c, client)
                    write_json(folder / 'formation.partial.json', checkpoint)
                    print(f"history={index} formation round={r['round']} price={r['outcome']['price']}", flush=True)
                write_json(checkpoint_path, checkpoint)
            eligible = qualify(checkpoint['rounds'], c)
            write_json(folder / 'qualification.json', eligible)
            if not eligible['qualified'] or formation_only:
                print(f'history={index} qualification={eligible}', flush=True)
                continue
            branches = folder / 'branches'
            branches.mkdir(exist_ok=True)
            order = conditions(c)
            # Counterbalance order across independent histories without changing shared seeds.
            shift = index % len(order)
            order = order[shift:] + order[:shift]
            for condition in order:
                path = branches / (condition['id'] + '.json')
                if path.exists():
                    state = json.loads(path.read_text())
                    if state['start_hash'] != digest(checkpoint):
                        raise ValueError('Branch checkpoint mismatch')
                else:
                    state = copy.deepcopy(checkpoint)
                    state.update(condition=condition, start_hash=digest(checkpoint))
                while len(state['rounds']) < c['protocol']['total_rounds']:
                    r = play_round(state, c, client, condition, eligible['quota'])
                    write_json(path, state)
                    print(f"history={index} {condition['id']} round={r['round']} price={r['outcome']['price']}", flush=True)
                write_json(output / 'status.json', status | {'last_completed_condition': condition['id'], 'history_id': index})
        status['status'] = 'complete'
    except KeyboardInterrupt:
        status.update(status='paused', reason='Interrupted by user; resume replays successful calls.')
    except PauseRun as exc:
        status.update(status='paused', reason=str(exc))
    except Exception as exc:
        status.update(status='incomplete', reason=str(exc))
        raise
    finally:
        status.update(new_model_calls=client.calls, replayed_calls=client.replayed, session_tokens=client.session_tokens)
        write_json(output / 'status.json', status)
        report(output, c, client.backend)
    return status
