"""Logged operational cache reset; frozen experiment source and requests unchanged.
Only stops the controller, never its inference runner. The unload is queued behind
any active HTTP request. Its response remains in the controller socket. A watchdog
and finally resume the same controller. Benchmark replies never enter the market.
"""
import argparse,fcntl,json,os,signal,subprocess,sys,time,urllib.request
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
def now():return datetime.now(timezone.utc).isoformat()
def http(path,body=None):
 req=urllib.request.Request('http://127.0.0.1:11434'+path,data=json.dumps(body).encode() if body is not None else None,headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=180) as f:return json.load(f)
def append(path,row):
 with path.open('a') as f:f.write(json.dumps(row)+'\n')
def snapshot():return {'models':http('/api/ps'),'swap':subprocess.check_output(['sysctl','vm.swapusage'],text=True).strip()}
def run():
 lock=(ROOT/'work/runtime_cache_maintenance.lock').open('a')
 fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 ap=argparse.ArgumentParser();ap.add_argument('--benchmark',action='store_true');args=ap.parse_args()
 active=ROOT/'results/final_16';state=json.loads((active/'live_status.json').read_text());pid=state['pid']
 if state['state'] not in ('running_markets','running_assessments'):raise SystemExit('No active supported study state')
 out=ROOT/'results/development_runtime_reset';out.mkdir(exist_ok=True)
 stamp=str(time.time_ns());record={'id':stamp,'started_utc':now(),'controller_pid':pid,'before':snapshot(),'request_parameters_changed':False,'weights_changed':False,'history_changed':False,'benchmark_calls':0}
 rows=[json.loads(x) for x in (active/'calls.jsonl').read_text().splitlines()]
 source=next(r for r in reversed(rows) if r['tag'].get('agent')=='firm_C' and r['tag'].get('kind')=='price')
 record['benchmark_source_hash']=source['request_hash']
 watch=None;paused=False
 try:
  os.kill(pid,signal.SIGSTOP);paused=True
  watch=subprocess.Popen([sys.executable,'-c',f'import os,signal,time;time.sleep(240);os.kill({pid},signal.SIGCONT)'],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
  def probe(label):
   start=time.monotonic();raw=http('/api/chat',source['request']);item={'reset_id':stamp,'label':label,'request':source['request'],'source_request_hash':source['request_hash'],'response':raw,'seconds':time.monotonic()-start,'delivered_to_market':False}
   append(out/'benchmark_calls.jsonl',item);record['benchmark_calls']+=1
   print(label,round(item['seconds'],3),flush=True)
   if raw.get('done_reason')!='stop':raise RuntimeError('Incomplete isolated probe')
   return {k:item[k] for k in ['label','seconds']}
  if args.benchmark:record['baseline']=probe('before_reset')
  record['unload']=http('/api/generate',{'model':source['request']['model'],'keep_alive':0,'stream':False})
  record['unloaded']=snapshot();print('UNLOADED',json.dumps(record['unloaded']),flush=True)
  # Same exact request reloads weights; isolated output is never selected as an action.
  record['cold']=probe('after_reset_cold')
  if args.benchmark:record['warm']=probe('after_reset_warm')
  record['after']=snapshot();record['state']='complete'
 except BaseException as e:record.update(state='failed',error=repr(e));raise
 finally:
  if paused:os.kill(pid,signal.SIGCONT)
  if watch:watch.terminate()
  record['finished_utc']=now();record['controller_resumed']=paused
  append(out/'resets.jsonl',record)
  append(active/'operational_pauses.jsonl',{'reason':'User-authorized MLX runtime cache reset; identical weights and full request histories; benchmark outputs not delivered','started_utc':record['started_utc'],'finished_utc':record['finished_utc'],'controller_pid':pid,'resumed':paused,'runtime_reset_id':stamp,'record':'results/development_runtime_reset','call_wall_latencies_may_include_pause':True})
  print('RESET_RESULT',json.dumps(record),flush=True)
if __name__=='__main__':run()
