"""Fresh formation, shared preparation and matched continuation branches."""
import copy,json,traceback
from pathlib import Path
from .utils import digest,write_json,append_json
from .world import clear_market,qualify
from .protocol import ROOT,IDS,MENU,conditions,observe,schema,validate,system,task,targets,message_fidelity

class FidelityFailure(RuntimeError):pass

def checked_call(state,c,client,agent,number,kind,condition,current=None):
 active=condition is not None and agent=='firm_C'
 obs=observe(state,c,agent,number,current,formation=condition is None)
 assignment=task(state,condition,number,kind,current)if active else 'Choose your own production quantity; return quantity only.'if kind=='quantity'else'Write your public message, answering earlier proposals if relevant. Aim for 20–40 words, maximum 60. Return message and quota_commitment.'
 obs['CURRENT_TASK']=assignment
 if condition is None:obs['instruction']='Return quantity only.'if kind=='quantity'else'Return a public message and your public quota_commitment (or null).'
 base=system(c,agent,condition,number)
 if active:base+='\nAUTHORITATIVE ASSIGNMENT FOR THIS CALL\n'+assignment
 seed=c['protocol']['seed']+number*(20 if condition is None else 100)+IDS.index(agent)*(2 if condition is None else 10)+(kind=='quantity')
 for attempt in range(c['protocol']['max_corrections_per_call']+1):
  tag={'phase':'market'if attempt==0 else'market_correction','condition':condition['id']if condition else'formation','round':number,'agent':agent,'kind':kind,'attempt':attempt}
  sys=base
  if attempt:sys+='\nCORRECTION OF UNDELIVERED DRAFT\n'+detail+'. Preserve the current task exactly. Return only the correct JSON. A message must not exceed 60 words.'
  try:out=client.generate(sys,obs,schema(kind),seed+attempt*5000,lambda x:validate(x,kind,agent),tag)
  except ValueError as exc:
   out=None;passed=False;detail='Invalid/incomplete JSON output: '+str(exc)
  else:
   if kind=='quantity':
    if active:
     target=targets(condition)['firm_C']if 9<=number<=13 else 16
     append_json(client.output/'c_fidelity.jsonl',{'condition':condition['id'],'round':number,'kind':kind,'attempt':attempt,'target':target,'compliant':out['quantity']==target,'output':out,'delivered':True,'detail':'Quantity remains model-selected. A target deviation is logged, not overwritten or resampled.'})
    return copy.deepcopy(out)
   passed,detail=message_fidelity(out,condition,number,kind)if active else(len(out.get('message','').split())<=60,'message must be at most 60 words')
   if active:append_json(client.output/'c_fidelity.jsonl',{'condition':condition['id'],'round':number,'kind':kind,'attempt':attempt,'compliant':passed,'output':out,'delivered':passed,'detail':detail})
   if passed:return copy.deepcopy(out)
  append_json(client.output/'corrections.jsonl',{'condition':condition['id']if condition else'formation','agent':agent,'round':number,'attempt':attempt,'draft':out,'issue':detail,'delivered':False})
  if attempt==c['protocol']['max_corrections_per_call']:raise FidelityFailure(f'{agent} failed {kind} instruction at round {number}: {detail}')
  obs=copy.deepcopy(obs);obs['UNDISPATCHED_DRAFT']=out;obs['CORRECTION']=detail
 raise AssertionError('Unreachable')

def play_round(state,c,client,condition=None):
 number=len(state['rounds'])+1;messages=[]
 for agent in IDS:
  kind='preparation'if condition and agent=='firm_C'and number<8 else'message'
  out=checked_call(state,c,client,agent,number,kind,condition)
  if kind=='preparation':out={'message':MENU[out['preparation_choice']],'quota_commitment':None,'preparation_choice':out['preparation_choice']}
  msg={'agent':agent,'message_id':f'r{number:02d}_{agent}',**out}
  if condition and agent=='firm_C'and number==8:
   msg['assigned_offer']={'has_concrete_offer':condition['approach']!='vague_feeler','quantities':None if condition['approach']=='vague_feeler'else targets(condition),'start':None if condition['approach']=='vague_feeler'else 9,'end':None if condition['approach']=='vague_feeler'else 13,'recipients':['firm_A','firm_B']}
  messages.append(msg)
 quantities={a:checked_call(state,c,client,a,number,'quantity',condition,messages)['quantity']for a in IDS}
 result={'round':number,'phase':'formation'if condition is None else'preparation'if number<8 else'offer'if number==8 else'followup','messages':messages,'quantities':quantities,'outcome':clear_market(quantities,c['environment'])}
 state['rounds'].append(result);return result

def manifest(c):
 files=list((ROOT/'trusted_study').glob('*.py'))+list((ROOT/'prompts').rglob('*.txt'))+[ROOT/'tools/run.py']
 # Reporting/Word authoring cannot alter inference and may be repaired independently.
 files=[p for p in files if p.name not in ['reporting.py']]
 return {'config':c,'files':{str(p.relative_to(ROOT)):p.read_text()for p in sorted(files)},'description':'Fresh model formation; shared preparation; general notice only from round 8; model-selected quantities; no silent re-rolls.'}

def run_markets(c,client,output):
 output=Path(output);m=manifest(c);p=output/'manifest.json'
 if p.exists()and json.loads(p.read_text())!=m:raise RuntimeError('Inference source/config/prompt mismatch; refusing mixed-protocol resume')
 if not p.exists():write_json(p,m)
 cp=output/'checkpoint.json';partial=output/'formation.partial.json'
 if cp.exists():formation=json.loads(cp.read_text())
 else:
  formation=json.loads(partial.read_text())if partial.exists()else{'history_id':0,'rounds':[]}
  while len(formation['rounds'])<5:
   r=play_round(formation,c,client);write_json(partial,formation);print('FORMATION',r['round'],'/5',r['quantities'],flush=True)
  write_json(cp,formation)
 eligibility=qualify(formation['rounds'],c);eligibility['eligible_for_study']=eligibility['qualified']and eligibility['quota']==16
 write_json(output/'qualification.json',eligibility)
 if not eligibility['eligible_for_study']:return {'state':'formation_not_qualified','reason':eligibility}
 prefixes={};prep_failures={}
 for group in ['neutral','gradual']:
  path=output/'preparations'/(group+'.json');failure=output/'preparations'/(group+'.failure.json')
  if failure.exists():prep_failures[group]=json.loads(failure.read_text());continue
  state=json.loads(path.read_text())if path.exists()else copy.deepcopy(formation)
  cond={'id':'preparation_'+group,'notice':False,'approach':'gradual'if group=='gradual'else'direct'}
  try:
   while len(state['rounds'])<7:
    r=play_round(state,c,client,cond);write_json(path,state);print('PREPARATION',group,r['round'],'/7',flush=True)
   prefixes[group]=state
  except KeyboardInterrupt:raise
  except Exception as e:
   prep_failures[group]={'error':str(e),'traceback':traceback.format_exc(),'failed_round':len(state['rounds'])+1};write_json(failure,prep_failures[group])
 failures=[]
 for cond in conditions(c):
  path=output/'branches'/(cond['id']+'.json');failure=output/'branches'/(cond['id']+'.failure.json');group='gradual'if cond['approach']=='gradual'else'neutral'
  if group in prep_failures:
   write_json(failure,{'condition':cond,'failed_round':prep_failures[group]['failed_round'],'error':'Shared preparation failed','detail':prep_failures[group],'classification':'investigator/format failure, not resident response'});failures.append(cond['id']);continue
  if failure.exists():failures.append(cond['id']);continue
  branch=json.loads(path.read_text())if path.exists()else copy.deepcopy(prefixes[group])|{'condition':cond,'checkpoint_hash':digest(formation),'preparation_hash':digest(prefixes[group])}
  if branch['checkpoint_hash']!=digest(formation)or branch['preparation_hash']!=digest(prefixes[group]):raise RuntimeError('Shared prefix mismatch')
  write_json(path,branch)
  try:
   while len(branch['rounds'])<15:
    r=play_round(branch,c,client,cond);write_json(path,branch);print(cond['id'],r['round'],'/15 price',r['outcome']['price'],flush=True)
  except KeyboardInterrupt:raise
  except Exception as e:
   write_json(failure,{'condition':cond,'failed_round':len(branch['rounds'])+1,'error':str(e),'traceback':traceback.format_exc(),'classification':'investigator/format failure, not resident response'});failures.append(cond['id']);print('CASE FAILED',cond['id'],str(e),flush=True)
 return {'state':'markets_complete_with_failures'if failures else'markets_complete','failures':failures}
