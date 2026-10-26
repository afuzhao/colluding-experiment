"""One isolated paired-order microbenchmark; never delivers responses to agents.
Temporarily SIGSTOPs only the active study controller, then SIGCONTs in finally.
An independent watchdog also resumes it after10minutes.
"""
import json,os,signal,subprocess,sys,time,urllib.request
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from price_study.protocol import ROOT
from price_study.utils import append_json,write_json
out=ROOT/'results/development_cache_timing';out.mkdir(parents=True,exist_ok=True)
active=ROOT/'results/final_16';state=json.loads((active/'live_status.json').read_text());pid=state['pid']
if state['state']!='running_markets':raise SystemExit('Benchmark requires an explicitly active market controller')
if(out/'status.json').exists():raise SystemExit('Do not silently repeat this benchmark')
rows={x['request_hash']:x for x in map(json.loads,(active/'calls.jsonl').read_text().splitlines())}
positions=[json.loads(x)for x in(active/'request_positions.jsonl').read_text().splitlines()]
requests={}
for x in positions:
 t=x['tag']
 if t.get('condition')=='notice_direct'and t.get('round')==12 and t.get('attempt')==0:
  requests[(t['agent'],t['kind'])]=rows[x['request_hash']]
assert len(requests)==6
orders={'baseline':[('firm_A','message'),('firm_B','message'),('firm_C','message'),('firm_A','price'),('firm_B','price'),('firm_C','price')],'c_first':[('firm_C','message'),('firm_A','message'),('firm_B','message'),('firm_A','price'),('firm_B','price'),('firm_C','price')]}
info={'state':'running','controller_pid':pid,'started_utc':datetime.now(timezone.utc).isoformat(),'source_condition':'notice_direct','source_round':12,'scope':'Frozen recorded requests, responses not delivered; ABBA order microbenchmark, no claim of identical future speed. Main pending response is retained in socket while controller stopped.'};write_json(out/'status.json',info)
def stopped(signum,frame):raise KeyboardInterrupt('Benchmark interrupted')
signal.signal(signal.SIGTERM,stopped)
watch=None;paused=False
try:
 os.kill(pid,signal.SIGSTOP);paused=True
 watch=subprocess.Popen([sys.executable,'-c','import os,signal,time;time.sleep(600);os.kill('+str(pid)+',signal.SIGCONT)'],stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
 def call(key,block,order):
  row=requests[key];start=time.monotonic();req=urllib.request.Request('http://127.0.0.1:11434/api/chat',data=json.dumps(row['request']).encode(),headers={'Content-Type':'application/json'})
  with urllib.request.urlopen(req,timeout=100)as f:raw=json.load(f)
  if raw.get('done_reason')!='stop':raise RuntimeError('Incomplete benchmark output')
  item={'block':block,'order':order,'agent':key[0],'kind':key[1],'source_request_hash':row['request_hash'],'request':row['request'],'response':raw,'seconds':round(time.monotonic()-start,3),'delivered_to_market':False}
  append_json(out/'benchmark_calls.jsonl',item);print(block,order,*key,item['seconds'],flush=True)
  return item
 call(('firm_C','price'),-1,'warmup_not_timed')
 blocks=[]
 for number,order in enumerate(['baseline','c_first','c_first','baseline']):
  records=[call(key,number,order)for key in orders[order]]
  blocks.append({'block':number,'order':order,'seconds':round(sum(x['seconds']for x in records),3),'prompt_seconds':round(sum(x['response'].get('prompt_eval_duration',0)for x in records)/1e9,3),'output_tokens':sum(x['response'].get('eval_count',0)for x in records),'cached_prompt_tokens':sum(x['response'].get('prompt_eval_cached_count',0)for x in records)})
  write_json(out/'blocks.json',blocks)
 info.update(state='complete',blocks=blocks)
except BaseException as e:info.update(state='failed',error=str(e));print('BENCHMARK FAILURE',repr(e),flush=True)
finally:
 if paused:os.kill(pid,signal.SIGCONT)
 if watch:watch.terminate()
 info['finished_utc']=datetime.now(timezone.utc).isoformat();info['controller_resumed']=paused;write_json(out/'status.json',info)
 append_json(active/'operational_pauses.jsonl',{'reason':'User-authorized isolated cache-order benchmark; no inference protocol or requests changed','started_utc':info['started_utc'],'finished_utc':info['finished_utc'],'controller_pid':pid,'resumed':paused,'benchmark_state':info['state'],'record':'results/development_cache_timing','call_wall_latencies_may_include_pause':True})
 print('BENCHMARK STATUS',json.dumps(info),flush=True)
