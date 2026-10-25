#!/usr/bin/env python3
"""Persistent sequential queue for an unchanged, resumable Cournot experiment.

This is client-side orchestration, not Groq's paid Batch API. It honors provider
waits, preserves successful-call replay, and never changes experimental settings.
"""
import argparse
from datetime import datetime, timedelta, timezone
import fcntl
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def now():
    return datetime.now(timezone.utc)


def read_json(path, default=None):
    try:
        return json.loads(path.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def atomic(path, value):
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(value, indent=2))
    tmp.replace(path)


def progress(output):
    manifest = read_json(output / 'manifest.json', {})
    c = manifest.get('config', {})
    total = c.get('protocol', {}).get('total_rounds', 30)
    histories = []
    for folder in sorted(output.glob('history_*')):
        checkpoint = read_json(folder / 'checkpoint.json')
        prefix = checkpoint or read_json(folder / 'formation.partial.json', {'rounds': []})
        branches = []
        for path in sorted((folder / 'branches').glob('*.json')):
            data = read_json(path, {'rounds': []})
            n = len(data['rounds'])
            branches.append({'condition': path.stem, 'round': n, 'complete': n == total})
        histories.append({'history': folder.name, 'formation_rounds': len(prefix['rounds']),
                          'qualification': read_json(folder / 'qualification.json'), 'branches': branches})
    calls, tokens = 0, 0
    journal = output / 'calls.jsonl'
    if journal.exists():
        for line in journal.read_text().splitlines():
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            calls += 1
            tokens += entry.get('response', {}).get('usage', {}).get('total_tokens', 0)
    return {'histories': histories, 'successful_calls_saved': calls, 'recorded_tokens': tokens,
            'complete_conditions': sum(b['complete'] for h in histories for b in h['branches']),
            'target_conditions': 8 * c.get('protocol', {}).get('histories', 1)}


def wait_seconds(status, consecutive_limits=0):
    reason = status.get('reason', '')
    if 'session token budget' in reason.lower():
        tomorrow = (now() + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        return max(60, (tomorrow - now()).total_seconds())
    if 'rate limit' in reason.lower():
        match = re.search(r'Retry-After:\s*(\d+(?:\.\d+)?)', reason)
        requested = float(match.group(1)) if match else 60
        # Never retry earlier than the provider requests; back off on repeated limits.
        return max(requested, min(300, 30 * 2 ** min(consecutive_limits, 4)))
    return None


def write_progress(output, state, **extra):
    payload = {'state': state, 'pid': os.getpid(), 'updated_utc': now().isoformat(), **progress(output), **extra}
    atomic(output / 'batch_status.json', payload)
    return payload


def wait_with_heartbeat(output, seconds, reason):
    until = now() + timedelta(seconds=seconds)
    while now() < until:
        if (output / 'STOP_BATCH').exists():
            write_progress(output, 'stopped', reason='STOP_BATCH requested')
            return False
        write_progress(output, 'waiting_for_quota', reason=reason, next_attempt_utc=until.isoformat())
        time.sleep(min(15, max(0.1, (until - now()).total_seconds())))
    return True


def validate_resume(output):
    """Keep archived source/config immutable; refuse execution after a code change."""
    sys.path.insert(0, str(ROOT))
    from trusted_lab.cournot.runner import source_manifest
    manifest = read_json(output / 'manifest.json')
    if manifest is None:
        raise ValueError('Run formation/initialize a saved experiment before batching it.')
    if manifest['backend'] != 'groq':
        raise ValueError('Persistent live queue requires a Groq run, not a mock fixture.')
    if source_manifest(manifest['config'], 'groq') != manifest:
        raise ValueError('Code/prompts differ from the saved manifest. Do not alter the archived run.')
    return manifest


def work(output):
    output = output.resolve()
    # One worker per experiment. Advisory lock is released automatically on exit.
    with (output / '.batch.lock').open('a') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return 2
        try:
            manifest = validate_resume(output)
        except Exception as exc:
            write_progress(output, 'needs_attention', reason=str(exc))
            return 1
        # Use the archived configuration, not a possibly edited current default.
        config_path = output / 'batch_config.json'
        atomic(config_path, manifest['config'])
        consecutive = 0
        attempt = 0
        with (output / 'batch.log').open('a', buffering=1) as log:
            while not (output / 'STOP_BATCH').exists():
                attempt += 1
                write_progress(output, 'running', attempt=attempt)
                log.write(f'\n[{now().isoformat()}] Resume attempt {attempt}\n')
                command = [sys.executable, '-u', '-m', 'trusted_lab.cournot', 'run', '--resume', '--config', str(config_path), '--output', str(output)]
                child = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=log)
                interrupted = False
                while child.poll() is None:
                    if (output / 'STOP_BATCH').exists() and not interrupted:
                        child.send_signal(signal.SIGINT)
                        interrupted = True
                    write_progress(output, 'stopping' if interrupted else 'running', attempt=attempt, worker_pid=child.pid)
                    time.sleep(2)
                if interrupted:
                    write_progress(output, 'stopped', reason='User requested stop; successful calls remain saved.')
                    return 0
                status = read_json(output / 'status.json', {})
                if child.returncode != 0:
                    write_progress(output, 'needs_attention', reason=status.get('reason', 'Worker failed; inspect batch.log.'))
                    return 1
                if status.get('status') == 'complete':
                    # Complete may mean formation failed qualification, not eight branches.
                    p = progress(output)
                    success = p['complete_conditions'] == p['target_conditions']
                    write_progress(output, 'complete' if success else 'formation_not_qualified',
                                   reason='All conditions reached their final round.' if success else 'Formation did not qualify; no cartel was invented.')
                    return 0
                delay = wait_seconds(status, consecutive)
                if status.get('status') != 'paused' or delay is None:
                    write_progress(output, 'needs_attention', reason=status.get('reason', 'Unexpected worker state.'))
                    return 1
                consecutive += 1
                if not wait_with_heartbeat(output, delay, status.get('reason', 'quota wait')):
                    return 0
            write_progress(output, 'stopped', reason='STOP_BATCH requested')
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['start', 'work', 'status'])
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output).resolve()
    if args.command == 'work':
        raise SystemExit(work(output))
    if args.command == 'status':
        print(json.dumps(read_json(output / 'batch_status.json', progress(output)), indent=2))
        return
    validate_resume(output)
    if (output / 'STOP_BATCH').exists():
        parser.error('Remove STOP_BATCH deliberately before restarting.')
    prior = read_json(output / 'batch_status.json', {})
    if prior.get('state') in ('running', 'waiting_for_quota', 'stopping') and prior.get('pid'):
        try:
            os.kill(prior['pid'], 0)
            print('Batch worker already running, PID', prior['pid'])
            return
        except ProcessLookupError:
            pass
    # Child is detached from the terminal; secrets are loaded only by the worker.
    with (output / 'batch_launcher.log').open('a') as log:
        child = subprocess.Popen([sys.executable, '-u', str(Path(__file__).resolve()), 'work', '--output', str(output)],
                                 cwd=ROOT, stdout=log, stderr=log, start_new_session=True)
    print('Batch worker started, PID', child.pid)
    print('Progress:', output / 'batch_status.json')
    print('Log:', output / 'batch.log')


if __name__ == '__main__':
    main()
