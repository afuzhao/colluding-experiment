"""Audit delivered request boundaries and ordinary-C instructions from saved calls; no inference."""
import argparse,json
from pathlib import Path
from run_controls import load,ROOT

def audit(env):
 folder=ROOT/'results'/env;root,p,d,w,Client,action,plural,commit,target=load(env);c=p.config()
 rows=[json.loads(s)for s in(folder/'calls.jsonl').read_text().splitlines()];checked={'market_requests':0,'ordinary_C_requests':0,'frozen8_explicit':0,'frozen8_neutral':0}
 for row in rows:
  tag=row['tag'];request=row['request'];obs=json.loads(next(m['content']for m in request['messages']if m['role']=='user'));system=next(m['content']for m in request['messages']if m['role']=='system')
  if tag['phase']in['ordinary_control','ordinary_control_correction']:
   n=tag['round'];assert len(obs['public_history'])==n-1,'Future/current action exposure'
   assert len(obs['current_messages'])==(3 if tag['kind']==action else 0),'Simultaneous message boundary'
   if tag['agent']=='firm_C':
    cond={'id':tag['condition'],'approach':'direct','notice':tag['condition'].startswith('notice_')};assert system.startswith(p.system(c,'firm_A',cond,n)),'C was not given resident system role'
    assert obs['CURRENT_TASK']==('Choose your own '+action+'; return '+action+' only.')if tag['kind']==action else True,'Assigned investigator price policy leaked'
    checked['ordinary_C_requests']+=1
   checked['market_requests']+=1
  elif tag['phase']in['neutral_control_diagnostic','explicit_control_diagnostic']:
   assert obs['round']==8 and len(obs['public_history'])==8,'Diagnostic saw post8 history'
   assert len(obs['peer_texts'])==2,'Diagnostic did not assess both peers'
   assert 'accounts'not in obs and 'assessments'not in obs,'Other diagnostic response exposed'
   if tag['phase']=='neutral_control_diagnostic':
    assert not any(word in obs['CURRENT_TASK'].lower()for word in ['investigator','testing','evidence']),'Neutral prompt is primed'
    checked['frozen8_neutral']+=1
   else:checked['frozen8_explicit']+=1
  else:raise AssertionError('Unrecognized call phase')
 result={'environment':env,'reviewer':'assistant_reviewed','source':'actual saved request/response journal','successful_requests_checked':len(rows),**checked,'result':'passed','limits':'Boundary and task checks do not validate model beliefs, semantic compliance or independent annotation.'};(folder/'REQUEST_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--environment',required=True,choices=['E1','E2']);audit(ap.parse_args().environment)
