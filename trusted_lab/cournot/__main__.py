"""python -m trusted_lab.cournot plan|doctor|run|report"""
import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from .client import GroqClient, MockClient, load_env
from .evaluation import report
from .runner import conditions, run
from .world import ROOT, benchmarks, load_config


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['plan', 'doctor', 'run', 'report'])
    p.add_argument('--config', default=str(ROOT / 'configs/cournot_groq.json'))
    p.add_argument('--backend', choices=['groq', 'mock'], default='groq')
    p.add_argument('--output')
    p.add_argument('--resume', action='store_true')
    p.add_argument('--formation-only', action='store_true')
    args = p.parse_args()
    c = load_config(args.config)
    if args.command == 'plan':
        f, t = c['protocol']['formation_rounds'], c['protocol']['total_rounds']
        print(json.dumps({'conditions': conditions(c), 'benchmarks': benchmarks(c['environment']),
            'calls_per_qualified_history': 6 * f + 8 * 5 * (t - f),
            'note': 'Three formation message/quantity pairs; after replacement C dialogue is generated but C quantity is fixed. No judging calls included.'}, indent=2))
        return
    if args.command == 'doctor':
        load_env()
        print(json.dumps({'model': c['model']['id'], 'groq_key_configured': bool(os.getenv('GROQ_API_KEY')), 'network_tested': False}))
        return
    if args.command == 'report':
        if not args.output:
            p.error('--output required')
        output = Path(args.output)
        manifest = json.loads((output / 'manifest.json').read_text())
        report(output, manifest['config'], manifest['backend'])
        return
    if args.resume and not args.output:
        p.error('--resume requires --output')
    output = Path(args.output) if args.output else ROOT / 'results' / ('cournot_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    if output.exists() and not args.resume:
        p.error('Output exists; use --resume or a new path')
    if args.backend == 'groq':
        load_env()
        if not os.getenv('GROQ_API_KEY'):
            p.error('Set GROQ_API_KEY in the ignored project .env file. No API requests were sent.')
    output.mkdir(parents=True, exist_ok=True)
    client = (GroqClient if args.backend == 'groq' else MockClient)(c, output)
    print('Output:', output, flush=True)
    print(json.dumps(run(c, client, output, args.resume, args.formation_only), indent=2))


if __name__ == '__main__':
    main()
