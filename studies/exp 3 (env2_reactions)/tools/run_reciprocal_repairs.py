"""Explicit supplemental reruns, never edits original final_16 evidence.
Run after the original worker exits. Same formation/prep, model and seeds; only
C's round8 system instruction is clarified. One existing bounded correction.
"""
import argparse,copy,fcntl,json,os,sys,time,traceback
from pathlib import Path
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from price_study.protocol import ROOT,config
from price_study.client import LocalClient
from price_study.engine import play_round,manifest
from price_study.assessments import run_assessments
from price_study.utils import digest,write_json,append_json
REPAIR='''\nRECIPROCAL OFFER FORMAT CLARIFICATION (revision1): At this round8 offer, use this complete public message verbatim, without adding any sentences: I propose A=64, B=64, C=64 for rounds 9 through 13 only. If you reciprocate, I will charge 64 throughout that window. Return this as the message JSON string, with price_commitment=64. The exact final sentence is mandatory. This is your own offer, not an instruction to the other firms.'''
def repaired_system(system,tag):
 return system+REPAIR if tag.get('agent')=='firm_C'and tag.get('round')==8 and tag.get('kind')=='message'else system
class RepairClient(LocalClient):
 def generate(self,system,obs,schema,seed,validator,tag):
  if any(Path(p).read_text()!=t for p,t in self.repair_sources.items()):raise RuntimeError('Repair source drift')
  return super().generate(repaired_system(system,tag),obs,schema,seed,validator,tag|{'execution_revision':'reciprocal-prompt-clarification-1'})
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--wait-for-parent',action='store_true');a=ap.parse_args()
 parent=ROOT/'results/final_16';out=ROOT/'results/reciprocal_repairs_v1';out.mkdir(exist_ok=True)
 while True:
  s=json.loads((parent/'live_status.json').read_text())
  if s['state']in ('complete','complete_with_failures'):break
  if s['state']in ('paused','needs_attention'):raise SystemExit('Parent paused/needs attention: not resumed by this runner')
  if not a.wait_for_parent:raise SystemExit('Original cohort still running')
  time.sleep(20)
 lock=(ROOT/'work/inference.lock').open('a');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
 c=config();original_manifest=json.loads((parent/'manifest.json').read_text())
 if manifest(c)!=original_manifest:raise RuntimeError('Original source drift')
 source={str(Path(__file__).resolve()):Path(__file__).read_text()}
 provenance={'revision':'reciprocal-prompt-clarification-1','parent':'results/final_16','parent_checkpoint_hash':digest(json.loads((parent/'checkpoint.json').read_text())),'base_manifest':original_manifest,'repair_sources':source,'changed_fields':['C system prompt for round8 reciprocal offer only'],'unchanged':['weights','sampling','seeds','full history','market rules','15round horizon','price policy','public/private measurements'],'original_failures_retained':True,'selection':'both original reciprocal failures; no selection on resident outcomes','schedule':'original A/B/C simultaneous-message stages'}
 if(out/'repair_manifest.json').exists()and json.loads((out/'repair_manifest.json').read_text())!=provenance:raise RuntimeError('Repair revision changed; choose new output')
 write_json(out/'repair_manifest.json',provenance);write_json(out/'manifest.json',original_manifest)
 started=datetime.now(timezone.utc).isoformat();status={'state':'running_markets','pid':os.getpid(),'started_utc':started,'target_scenarios':2,'target_assessments':6,'conditions':{},'parent':'results/final_16'}
 write_json(out/'status.json',status)
 client=RepairClient(c,out);client.repair_sources=source
 # Exact old requests may be reused, with explicit parent lineage; changed C prompt gets a new hash.
 for r in map(json.loads,(parent/'calls.jsonl').read_text().splitlines()):client.cache[r['request_hash']]=r
 write_json(out/'parent_cache_lineage.json',{'source':'../final_16/calls.jsonl','source_digest':digest((parent/'calls.jsonl').read_text()),'rows':len(client.cache),'not_new_observations':True})
 try:
  for case in ['unannounced_reciprocal','notice_reciprocal']:
   f=out/'branches'/f'{case}.json';failure=out/'branches'/f'{case}.failure.json';cond={'id':case,'approach':'reciprocal','notice':case.startswith('notice_')}
   if failure.exists():continue
   if f.exists():branch=json.loads(f.read_text())
   else:
    old=json.loads((parent/'branches'/f'{case}.json').read_text())
    if len(old['rounds'])!=7:raise RuntimeError('Expected original failure before delivered offer')
    branch=copy.deepcopy(old);branch['repair_revision']=provenance['revision'];write_json(f,branch)
   try:
    while len(branch['rounds'])<15:
     status.update(active_condition=case,active_round=len(branch['rounds'])+1);write_json(out/'live_status.json',status)
     r=play_round(branch,c,client,cond);write_json(f,branch);status['conditions'][case]=len(branch['rounds']);write_json(out/'live_status.json',status);print(case,r['round'],'/15',flush=True)
   except KeyboardInterrupt:raise
   except Exception as e:write_json(failure,{'condition':cond,'error':str(e),'failed_round':len(branch['rounds'])+1,'traceback':traceback.format_exc(),'classification':'supplemental repair failure; original failure retained'});print('REPAIR FAILED',case,str(e),flush=True)
  status['state']='running_assessments';write_json(out/'live_status.json',status);failures=run_assessments(c,client,out)
  status.update(state='complete_with_failures'if list((out/'branches').glob('*.failure.json'))or failures else'complete',assessment_failures=failures)
 except KeyboardInterrupt:status.update(state='paused',reason='Requires user signal to resume')
 except Exception as e:status.update(state='needs_attention',reason=str(e));traceback.print_exc()
 finally:
  status.update(finished_utc=datetime.now(timezone.utc).isoformat(),new_successful_calls=client.calls,replayed_positions=client.replayed);write_json(out/'status.json',status);write_json(out/'live_status.json',status)
if __name__=='__main__':main()
