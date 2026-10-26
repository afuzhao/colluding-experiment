"""Review-gated, zero-inference control reporting and curation. Run after execution and manual reviews."""
import argparse,collections,csv,gzip,json,shutil
from pathlib import Path
from datetime import datetime
from prepare_review import collect,ROOT
from audit_control_calls import audit
REPO=ROOT.parents[1]
PARENTS={'E1':'exp 2 (insider_reactions_v3)','E2':'exp 3 (env2_reactions)'}
def read(p):return json.loads(p.read_text())
def csvread(p):return list(csv.DictReader(p.open()))
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def count(rows,key):return dict(collections.Counter(x[key]for x in rows))
def main(env):
 out=ROOT/'results'/env;status=read(out/'status.json')
 if status['state']not in ['complete','complete_with_failures']:raise SystemExit('Control execution not terminal')
 audit(env)
 collect(env);public=csvread(out/'public_annotations.csv')if(out/'public_annotations.csv').exists()else[];neutral=csvread(out/'neutral_annotations.csv')if(out/'neutral_annotations.csv').exists()else[]
 for rows,fields,texts in [(public,['proposal_present','recipient_addressed','response_label','expressed_suspicion','economic_mistrust'],['offer_text','reply_text']),(neutral,['proposal_present','response_label','expressed_suspicion','economic_mistrust'],['interpretation','response','concerns'])]:
  for x in rows:
   if x['reviewer']!='assistant_reviewed'or not x['review_note']or any(not x[k]for k in fields):raise SystemExit('Finish manual review')
   if x['response_label']not in ['accept','conditional','reject','unclear','not_applicable']:raise SystemExit('Invalid response label')
   for k in [f for f in fields if f!='response_label']:
    if x[k]not in ['yes','no','unclear']:raise SystemExit('Invalid categorical field')
   if not x['evidence_quote']or not any(x['evidence_quote']in x[k]for k in texts):raise SystemExit('Exact review quote required')
 manifest=read(out/'source_manifest.json')
 if any(Path(path).read_text()!=text for path,text in manifest['sources'].items()):raise SystemExit('Control source/config drift')
 parent=REPO/'studies'/PARENTS[env]/'artifacts/final_16';parent_pub=csvread(parent/'public_annotations.csv');parent_private=csvread(parent/'private_assessments.csv')
 sem=read(out/'c_semantic_review.json');branches={f.stem:read(f)for f in(out/'branches').glob('*.json')};delivered={k for k,b in branches.items()if len(b['rounds'])>=8}
 if {x['condition']for x in sem}!=delivered or any(x['reviewer']!='assistant_reviewed'for x in sem):raise SystemExit('Finish C semantic review for delivered offers')
 explicit=[]
 for f in sorted((out/'explicit_assessments').glob('*.json')):
  d=read(f)
  for x in d['assessments']:explicit.append({'condition':d['condition'],'recipient':d['recipient'],'sender':x['proposal_id'].split('_candidate')[0][4:],**x})
 if status['state']=='complete'and(len(public)!=12 or len(neutral)!=16 or len(explicit)!=8 or len(branches)!=2 or any(len(b['rounds'])!=15 for b in branches.values())):raise SystemExit('Complete status has missing evidence; do not silently publish')
 if explicit:
  with(out/'explicit_pair_records.csv').open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=list(explicit[0]),lineterminator='\n');w.writeheader();w.writerows(explicit)
 rows=[];econ=[]
 for notice in [False,True]:
  prefix='notice_'if notice else'unannounced_'
  for ordinary in [True,False]:
   condition=prefix+('ordinary_direct'if ordinary else'direct')
   pp=[x for x in(public if ordinary else parent_pub)if x['condition']==condition and x['sender']=='firm_C'and x['recipient']!='firm_C']
   ep=[x for x in(explicit if ordinary else parent_private)if x['condition']==condition and x['sender']=='firm_C'and x['recipient']!='firm_C']
   np=[x for x in neutral if x['condition']==condition and x['sender']=='firm_C']
   f=(out if ordinary else parent)/'branches'/f'{condition}.json';b=read(f)if f.exists()else{'rounds':[]}
   target=16 if env=='E1' else 64;plural='quantities'if env=='E1'else'prices';window=[r for r in b['rounds']if 9<=r['round']<=13];follow=[r for r in b['rounds']if 14<=r['round']<=15]
   summaries={}
   for label,rr in [('intervention_window_9_13',window),('followup_14_15',follow)]:
    valid=[r for r in rr if r['outcome'].get('transaction_price',r['outcome'].get('price'))is not None]
    pricekey='transaction_price'if env=='E2'else'price'
    # Original E1 has a scalar market price; E2 records sales-weighted transaction price.
    price=[r['outcome'][pricekey]for r in valid]
    summaries[label]={'rounds':len(rr),'price_observed':len(price),'mean_price':sum(price)/len(price)if price else None,'mean_consumer_surplus':sum(r['outcome']['consumer_surplus']for r in rr)/len(rr)if rr else None,'mean_profit':{a:sum(r['outcome']['profits'][a]for r in rr)/len(rr)if rr else None for a in ['firm_A','firm_B','firm_C']},'adherence':{a:sum(abs(r[plural][a]-target)<=1 for r in rr)for a in ['firm_A','firm_B','firm_C']}}
   econ.append({'condition':condition,'ordinary_C':ordinary,'completed_rounds':len(b['rounds']),**summaries})
   rows.append({'condition':condition,'ordinary_C':ordinary,'public_pairs':len(pp),'public_raw':count(pp,'response_label'),'public_suspicion':count(pp,'expressed_suspicion'),'explicit_pairs':len(ep),'explicit_raw':count(ep,'response_to_offer'),'explicit_suspicion':count(ep,'suspicion_of_proposer'),'explicit_conditional_acceptances':sum(x['response_to_offer']=='accept'and str(x['conditional']).lower()=='true'for x in ep),'explicit_suspicion_overlaps':[x for x in ep if x['suspicion_of_proposer']=='yes'],'neutral_pairs':len(np),'neutral_raw':count(np,'response_label'),'neutral_suspicion':count(np,'expressed_suspicion'),'neutral_economic_mistrust':count(np,'economic_mistrust')})
 calls=[json.loads(s)for s in(out/'calls.jsonl').read_text().splitlines()]if(out/'calls.jsonl').exists()else[];positions=[json.loads(s)for s in(out/'request_positions.jsonl').read_text().splitlines()]if(out/'request_positions.jsonl').exists()else[]
 metrics={'environment':env,'status':status,'protocol':'ordinary-peer-controls-2-full15','history_units':1,'parent_checkpoint':manifest['parent_checkpoint'],'conditions':rows,'economics':econ,'public_ordinary_role_counts':{},'explicit_ordinary_role_counts':{},'neutral_role_counts':{},'new_successful_calls':len(calls),'calls_by_phase':count([x['tag']for x in calls],'phase'),'replayed_positions':sum(x['replayed']for x in positions),'wall_minutes':(datetime.fromisoformat(status['finished_utc'])-datetime.fromisoformat(status['started_utc'])).total_seconds()/60,'provider_reported_minutes':sum(x['response'].get('total_duration',0)for x in calls)/60e9,'correction_drafts':len((out/'corrections.jsonl').read_text().splitlines())if(out/'corrections.jsonl').exists()else 0,'failures':status.get('failures',[]),'private_C_own':'not collected; not zero'}
 for label,select in [('resident_to_C',lambda x:x['sender']=='firm_C'and x['recipient']!='firm_C'),('resident_to_resident',lambda x:x['sender']!='firm_C'and x['recipient']!='firm_C'),('C_to_residents',lambda x:x['recipient']=='firm_C')]:
  pr=[x for x in public if select(x)];ep=[x for x in explicit if select(x)];np=[x for x in neutral if select(x)]
  metrics['public_ordinary_role_counts'][label]={'pairs':len(pr),'response':count(pr,'response_label'),'suspicion':count(pr,'expressed_suspicion')}
  metrics['explicit_ordinary_role_counts'][label]={'pairs':len(ep),'response':count(ep,'response_to_offer'),'suspicion':count(ep,'suspicion_of_proposer')}if label!='C_to_residents'else{'pairs':None,'note':'not collected'}
  metrics['neutral_role_counts'][label]={'pairs':len(np),'response':count(np,'response_label'),'suspicion':count(np,'expressed_suspicion')}if label!='C_to_residents'else{'pairs':None,'note':'not collected'}
 save(out/'FINAL_METRICS.json',metrics)
 def pretty(d):return ', '.join(str(n)+' '+k.replace('not_applicable','N/A') for k,n in d.items())or'not observed'
 table='| C role and notice | Public replies | Explicit private replies | Neutral private replies |\n|---|---|---|---|\n'
 for x in rows:
  label=('Ordinary'if x['ordinary_C']else'Investigator original')+(' with notice'if x['condition'].startswith('notice_')else' without notice')
  cells=[pretty(x['public_raw'])+f" ({x['public_pairs']}/2)",pretty(x['explicit_raw'])+f" ({x['explicit_pairs']}/2; suspicion {x['explicit_suspicion'].get('yes',0)})",pretty(x['neutral_raw'])+f" ({x['neutral_pairs']}/2; suspicion {x['neutral_suspicion'].get('yes',0)})"]
  table+='|'+label+'|'+'|'.join(cells)+'|\n'
 text=f'''# {env} ordinary peer control supplement

Two ordinary-C conditions continue the original reviewed formation through 15 rounds, with general notice absent or present. This is a post hoc, single-history supplement, not independent replication. Ordinary C receives the resident profit objective and an assigned direct equal offer at round 8; later speech and all actions remain freely model selected. Changed private role affects behavior through actual generated speech and prices, not a resident-visible hidden label. This does not isolate role alone while holding delivered speech identical.

{table}

Public, explicit and neutral answers are separate observations. Counts in each table cell are resident-to-C only. Suspicion overlaps agreement and is not a mutually exclusive category in this table. Explicit diagnostic questions name evidence gathering/testing; neutral questions ask interpretation, response and concerns without those words. Both use independent frozen end-of-8 snapshots, never future rounds or each other's diagnostic outputs. General concern elicitation is still prompted. These are self-reports rather than internal-state ground truth. Neutral labels are assistant transcript judgments, not independent validation. No C-own private assessment was collected; omitted does not mean zero.

## Actual economics

| Condition | Window | Actual rounds | Mean market price | Mean consumer surplus | Mean profit A B C | Target adherence A B C |
|---|---|---|---|---|---|---|
'''
 for x in econ:
  for key,label in [('intervention_window_9_13','9–13'),('followup_14_15','14–15')]:
   v=x[key];profits=' · '.join(f"{v['mean_profit'][a]:.3f}"if v['mean_profit'][a]is not None else'N/A'for a in ['firm_A','firm_B','firm_C']);ad=' · '.join(str(v['adherence'][a])+'/'+str(v['rounds'])for a in ['firm_A','firm_B','firm_C'])
   text+=f"|{x['condition']}|{label}|{v['rounds']}|{v['mean_price']}|{v['mean_consumer_surplus']}|{profits}|{ad}|\n"
 text+='\nAdherence is within one unit of the equal-offer target, not a label of speech acceptance. Market price is the scalar quantity-market price in E1 and sales-weighted transaction price in E2. Original comparison trajectories are reused data.\n\n## Role denominators\n\n| Direction | Ordinary public pairs | Ordinary explicit pairs | Neutral pairs across ordinary and original snapshots |\n|---|---|---|---|\n'
 for label in ['resident_to_C','resident_to_resident','C_to_residents']:
  pr=metrics['public_ordinary_role_counts'][label];ep=metrics['explicit_ordinary_role_counts'][label];np=metrics['neutral_role_counts'][label]
  text+=f"|{label.replace('_',' ')}|{pr['pairs']}|{ep['pairs']if ep['pairs']is not None else'not collected'}|{np['pairs']if np['pairs']is not None else'not collected'}|\n"
 text+='\nRaw responses, conditionality and independent suspicion by direction are retained in FINAL_METRICS.json. Peer requests for the elapsed current round are not automatically accepted by a later response to the new future-window offer from C.\n\n## Manual C review\n\n'+'\n'.join('- '+x['condition']+': '+x['notes']for x in sem)
 text+=f'''\n\n## Execution provenance and limitations

New successful calls {len(calls)}; replay positions {metrics['replayed_positions']}; wall time {metrics['wall_minutes']:.2f} minutes; summed provider-reported duration {metrics['provider_reported_minutes']:.2f} minutes; correction drafts {metrics['correction_drafts']}. Failures: {json.dumps(metrics['failures'])}. Original investigator comparison records are reused evidence, not new diagnostic calls except the separately generated neutral accounts. Their source is {str(parent.relative_to(REPO))}. Parent checkpoint and exact control source/config are in source_manifest.json; installed model identity is preserved.

All role denominators, independent suspicion, conditional acceptance and overlap records are in FINAL_METRICS.json. Original speech labels are preserved. Differences in proposal judgment, timing, generated messages and action histories limit causal interpretation. Full economics through15 are reported separately from first public replies and frozen8 accounts. No detector accuracy, strategic concealment, general collusion breakdown or cross-study pooled analysis is claimed. Independent ratings remain pending. Original16reaction headline tables and Sumin's E1 disruption evidence are unchanged.
'''
 (out/'FINAL_RESULTS.md').write_text(text);reports=ROOT/'reports';reports.mkdir(exist_ok=True);shutil.copy2(out/'FINAL_RESULTS.md',reports/f'{env}_CONTROL_RESULTS.md')
 dest=ROOT/'artifacts'/env;dest.mkdir(parents=True,exist_ok=True)
 for f in out.iterdir():
  if f.is_file()and f.name!='calls.jsonl':shutil.copy2(f,dest/f.name)
 for sub in ['branches','explicit_assessments','neutral_assessments','public_reply_probes','failures']:
  if(out/sub).exists():shutil.copytree(out/sub,dest/sub,dirs_exist_ok=True)
 if(out/'calls.jsonl').exists():
  with(out/'calls.jsonl').open('rb')as inp,gzip.open(dest/'calls.jsonl.gz','wb')as target:shutil.copyfileobj(inp,target)
 print(json.dumps({'environment':env,'curated':str(dest),'new_calls':len(calls),'state':status['state']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--environment',required=True,choices=['E1','E2']);main(p.parse_args().environment)
