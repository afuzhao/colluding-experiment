"""Run E2-R; formation review precedes continuations; one study worker at a time."""
import argparse,fcntl,json,os,sys,threading,time,traceback
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from price_study.protocol import ROOT,config,conditions
from price_study.client import LocalClient
from price_study.engine import run_markets
from price_study.assessments import run_assessments
from price_study.reporting import report
from price_study.utils import write_json,append_json
p=argparse.ArgumentParser();p.add_argument('--output',default='results/final_16');p.add_argument('--formation-only',action='store_true');a=p.parse_args()
c=config();out=Path(a.output).resolve()
if 'artifacts' in out.parts:raise SystemExit('Never run inference in the published artifacts')
out.mkdir(parents=True,exist_ok=True);(ROOT/'work').mkdir(exist_ok=True)
lock=(ROOT/'work/inference.lock').open('w')
try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
except BlockingIOError:raise SystemExit('Another study worker/preflight owns the local inference lock')
old=out/'status.json';prior=json.loads(old.read_text())if old.exists()else{}
if prior.get('state')in ['complete','complete_with_failures']:raise SystemExit('Completed output is immutable; choose a new folder')
state={'state':'starting','pid':os.getpid(),'started_utc':prior.get('started_utc',datetime.now(timezone.utc).isoformat())};stop=threading.Event();session=time.monotonic()
append_json(out/'worker_sessions.jsonl',{'pid':os.getpid(),'started_utc':datetime.now(timezone.utc).isoformat(),'formation_only':a.formation_only})

def snapshot():
 branches={p.stem:len(json.loads(p.read_text())['rounds'])for p in(out/'branches').glob('*.json')if not p.name.endswith('.failure.json')}
 cp=out/'checkpoint.json'
 if not cp.exists():cp=out/'formation.partial.json'
 assessments=[json.loads(p.read_text())for p in(out/'assessments').glob('*.json')]
 preparations={p.stem:len(json.loads(p.read_text()).get('rounds',[]))for p in(out/'preparations').glob('*.json')if not p.name.endswith('.failure.json')}
 return dict(state,updated_utc=datetime.now(timezone.utc).isoformat(),formation_rounds=len(json.loads(cp.read_text())['rounds'])if cp.exists()else 0,preparations=preparations,branches=branches,completed_scenarios=sum(n==15 for n in branches.values()),target_scenarios=16,failed_scenarios=[p.name.removesuffix('.failure.json')for p in(out/'branches').glob('*.failure.json')],assessments_finished=sum(x.get('state')=='complete'for x in assessments),assessments_failed=sum(x.get('state')=='failed'for x in assessments),target_assessments=48,successful_inference_calls=sum(1 for _ in(out/'calls.jsonl').open())if(out/'calls.jsonl').exists()else 0,elapsed_minutes=round((datetime.now(timezone.utc)-datetime.fromisoformat(state['started_utc'])).total_seconds()/60,2))

def publish():
 import html
 s=snapshot();write_json(out/'live_status.json',s)
 (out/'progress.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="20"><title>Environment 2 reactions progress</title><style>body{font:16px system-ui;background:#edf3ef;color:#193a3e;max-width:1000px;margin:40px auto}pre{white-space:pre-wrap}</style><h1>Environment 2 reactions · 16 conditions</h1><pre>'+html.escape(json.dumps(s,indent=2))+'</pre><a href="results.html">Results</a>')
 return s

def monitor():
 last=0
 while not stop.is_set():
  try:
   s=publish()
   if time.monotonic()-session-last>=1200:
    print('20-MINUTE PROGRESS',s['completed_scenarios'],'/16',s['branches'],'private',s['assessments_finished'],'/48',flush=True);last=time.monotonic()-session
  except Exception as e:print('MONITOR NOTE',str(e),flush=True)
  stop.wait(10)
thread=threading.Thread(target=monitor,daemon=True);thread.start()
try:
 client=LocalClient(c,out);state['state']='running_formation'if a.formation_only else'running_markets'
 r=run_markets(c,client,out,formation_only=a.formation_only);state.update(r);report(c,out)
 if r['state'].startswith('markets_complete'):
  state['state']='running_assessments';failures=run_assessments(c,client,out);state['assessment_failures']=failures;report(c,out)
  state['state']='complete_with_failures'if r.get('failures')or failures else'complete'
except KeyboardInterrupt:state.update(state='paused',reason='Stopped; requires user signal before resume')
except Exception as e:state.update(state='needs_attention',reason=str(e));traceback.print_exc()
finally:
 try:report(c,out)
 except Exception:traceback.print_exc()
 stop.set();thread.join(timeout=11);state['session_finished_utc']=datetime.now(timezone.utc).isoformat()
 if state['state'].startswith('complete'):state['finished_utc']=state['session_finished_utc']
 write_json(out/'status.json',state);publish();print('FINAL WORKER STATUS',json.dumps(state),flush=True)
