"""Run the frozen 16-condition study; duplicate workers are rejected."""
import argparse,fcntl,json,os,sys,threading,time,traceback
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from trusted_study.protocol import config,conditions
from trusted_study.client import LocalClient
from trusted_study.engine import run_markets
from trusted_study.assessments import run_assessments
from trusted_study.reporting import report
from trusted_study.utils import write_json
p=argparse.ArgumentParser();p.add_argument('--output',default='results/final_16');a=p.parse_args()
c=config();out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
lock=(out/'worker.lock').open('w')
try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
except BlockingIOError:raise SystemExit('An experiment worker already holds this folder')
state={'state':'starting','pid':os.getpid(),'started_utc':datetime.now(timezone.utc).isoformat()};stop=threading.Event();start=time.monotonic()

def snapshot():
 branches={p.stem:len(json.loads(p.read_text())['rounds'])for p in(out/'branches').glob('*.json')if not p.name.endswith('.failure.json')}
 formation=out/'checkpoint.json'
 if not formation.exists():formation=out/'formation.partial.json'
 assessments=[json.loads(p.read_text())for p in(out/'assessments').glob('*.json')]
 preparations={p.stem:len(json.loads(p.read_text()).get('rounds',[]))for p in(out/'preparations').glob('*.json')if not p.name.endswith('.failure.json')}
 return dict(state,updated_utc=datetime.now(timezone.utc).isoformat(),formation_rounds=len(json.loads(formation.read_text())['rounds'])if formation.exists()else 0,preparations=preparations,branches=branches,completed_scenarios=sum(n==15 for n in branches.values()),target_scenarios=len(conditions(c)),failed_scenarios=[p.name.removesuffix('.failure.json')for p in(out/'branches').glob('*.failure.json')],assessments_finished=sum(x.get('state')=='complete'for x in assessments),assessments_failed=sum(x.get('state')=='failed'for x in assessments),target_assessments=len(conditions(c))*3,successful_inference_calls=sum(1 for _ in(out/'calls.jsonl').open())if(out/'calls.jsonl').exists()else 0,elapsed_minutes=round((time.monotonic()-start)/60,2))

def publish_progress():
 import html
 latest=snapshot();write_json(out/'live_status.json',latest)
 (out/'progress.html').write_text('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="15"><title>Study progress</title><style>body{font:17px system-ui;background:#122934;color:#f0f5f7;max-width:1000px;margin:40px auto;padding:20px}pre{white-space:pre-wrap}a{color:#9ee2d0}</style><h1>16-condition study progress</h1><pre>'+html.escape(json.dumps(latest,indent=2))+'</pre><a href="results.html">Results</a> · <a href="run.log">Log</a>')
 return latest

def monitor():
 last=0
 while not stop.is_set():
  try:
   latest=publish_progress()
   if time.monotonic()-start-last>=1200:
    print('20-MINUTE PROGRESS',latest['completed_scenarios'],'/16',latest['branches'],'assessments',latest['assessments_finished'],'/48',flush=True);last=time.monotonic()-start
  except Exception as exc:print('MONITOR NOTE',str(exc),flush=True)
  stop.wait(10)
thread=threading.Thread(target=monitor,daemon=True);thread.start()
try:
 client=LocalClient(c,out);state['state']='running_markets';r=run_markets(c,client,out);state.update(r);report(c,out)
 if r['state'].startswith('markets_complete'):
  state['state']='running_assessments';failures=run_assessments(c,client,out);state['assessment_failures']=failures;report(c,out)
  state['state']='complete_with_failures'if r.get('failures')or failures else'complete'
except KeyboardInterrupt:state.update(state='paused',reason='Stopped; awaiting user signal before resuming')
except Exception as exc:state.update(state='needs_attention',reason=str(exc));traceback.print_exc()
finally:
 try:report(c,out)
 except Exception:traceback.print_exc()
 stop.set();thread.join(timeout=11);state['finished_utc']=datetime.now(timezone.utc).isoformat();write_json(out/'status.json',state);publish_progress();print('FINAL WORKER STATUS',json.dumps(state),flush=True)
