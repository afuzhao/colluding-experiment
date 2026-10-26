"""Separate development formation/preflight; never reused as the final history."""
import argparse,copy,fcntl,json,sys,traceback
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from price_study.protocol import ROOT,config,conditions,IDS
from price_study.client import LocalClient
from price_study.engine import run_markets,play_round,checked_call,manifest
from price_study.assessments import run_assessments
from price_study.utils import write_json,digest
p=argparse.ArgumentParser();p.add_argument('--stage',choices=['formation','checks'],required=True);p.add_argument('--output',default='results/development_8101');a=p.parse_args()
out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True);(ROOT/'work').mkdir(exist_ok=True)
lock=(ROOT/'work/inference.lock').open('w')
try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
except BlockingIOError:raise SystemExit('Another inference worker is active')
c=config();c['protocol']['seed']=8101;state={'stage':a.stage,'state':'running','started_utc':datetime.now(timezone.utc).isoformat(),'provenance':'Development-only; final formation must be newly generated at seed8201.'}
write_json(out/'pilot_status.json',state)
try:
 client=LocalClient(c,out)
 if a.stage=='formation':state.update(run_markets(c,client,out,formation_only=True))
 else:
  if json.loads((out/'manifest.json').read_text())!=manifest(c):raise RuntimeError('Development source changed; preserve this output and use a newly documented development fixture')
  q=json.loads((out/'qualification.json').read_text())
  if not q['eligible_for_study']or q['agreement_review']!='assistant_reviewed':raise RuntimeError('Review actual development formation first')
  cp=json.loads((out/'checkpoint.json').read_text());prefixes={}
  for group in ['neutral','gradual']:
   f=out/('pilot_'+group+'.json');s=json.loads(f.read_text())if f.exists()else copy.deepcopy(cp)
   cond={'id':'preparation_'+group,'approach':'gradual'if group=='gradual'else'direct','notice':False}
   while len(s['rounds'])<7:
    r=play_round(s,c,client,cond);write_json(f,s);print('PILOT PREPARATION',group,r['round'],flush=True)
   prefixes[group]=s
  checks=[]
  for cond in conditions(c):
   s=copy.deepcopy(prefixes['gradual'if cond['approach']=='gradual'else'neutral'])
   try:
    offer=checked_call(s,c,client,'firm_C',8,'message',cond)
    checks.append({'condition':cond,'passed_minimum_checks':True,'offer':offer,'semantic_review':'pending'})
   except Exception as e:checks.append({'condition':cond,'passed_minimum_checks':False,'error':str(e)})
   write_json(out/'preflight_checks.json',checks);print('PILOT C OFFER',cond['id'],checks[-1]['passed_minimum_checks'],flush=True)
  state['preflight_passed']=sum(x['passed_minimum_checks']for x in checks);state['preflight_total']=16
  # One short real branch checks delivery, subsequent public response and isolated diagnostics.
  path=out/'branches/unannounced_direct.json';cond={'id':'unannounced_direct','approach':'direct','notice':False}
  branch=json.loads(path.read_text())if path.exists()else copy.deepcopy(prefixes['neutral'])|{'condition':cond,'checkpoint_hash':digest(cp),'preparation_hash':digest(prefixes['neutral'])}
  while len(branch['rounds'])<9:
   r=play_round(branch,c,client,cond);write_json(path,branch);print('PILOT DIRECT ROUND',r['round'],r['prices'],flush=True)
  failures=run_assessments(c,client,out);state['assessment_failures']=failures
  state['state']='checks_complete'if state['preflight_passed']==16 and not failures else'checks_failed'
except Exception as e:state.update(state='failed',error=str(e));traceback.print_exc()
finally:
 state['finished_utc']=datetime.now(timezone.utc).isoformat();write_json(out/'pilot_status.json',state);print('PILOT STATUS',json.dumps(state),flush=True)
