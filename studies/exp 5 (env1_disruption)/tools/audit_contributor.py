"""Zero-inference audit of pinned contributor evidence. No checkout/source changes."""
import csv,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[1]
SHA='a10db995c8d0e8206d4ae935118cf9b8727fc067';BASE='studies/exp 2 (insider_reactions_v3)/';OUT=ROOT/'reports';OUT.mkdir(exist_ok=True)
def raw(path):return subprocess.check_output(['git','show',SHA+':'+BASE+path],cwd=REPO,text=True)
def read(path):return json.loads(raw(path))
def sha(text):return hashlib.sha256(text.encode()).hexdigest()
original=json.loads((REPO/BASE/'artifacts/final_16/manifest.json').read_text());identity=json.loads((REPO/BASE/'artifacts/final_16/model_identity.json').read_text())
reports=[];rows=[];formation_reviews=[];formations=[]
for name in ['talk_vs_action_v1','talk_vs_action_s2']:
 prefix='artifacts/'+name+'/';manifest=read(prefix+'manifest.json');cp=read(prefix+'checkpoint.json');formations.append(cp);fidelity=[json.loads(x)for x in raw(prefix+'c_fidelity.jsonl').splitlines()]
 env=manifest['config']['environment'];audit={'cohort':name,'source_commit':SHA,'source_manifest_sha256':sha(raw(prefix+'manifest.json')),'model_identity_matches_E1_R':read(prefix+'model_identity.json')==identity,'environment_matches_E1_R':env==original['config']['environment'],'model_settings_match_E1_R':manifest['config']['model']==original['config']['model'],'world_source_matches_E1_R':manifest['files']['trusted_study/world.py']==original['files']['trusted_study/world.py'],'source_changed_files':[k for k,v in manifest['files'].items()if original['files'].get(k)!=v],'original_qualification':read(prefix+'qualification.json'),'original_status':read(prefix+'status.json'),'C_action_checks':sum(x['kind']=='quantity'for x in fidelity),'C_action_deviations':sum(x['kind']=='quantity'and not x['compliant']for x in fidelity),'undelivered_C_drafts':sum(x['kind']!='quantity'and not x['compliant']for x in fidelity),'branches':[]}
 assert all(audit[k]for k in ['model_identity_matches_E1_R','environment_matches_E1_R','model_settings_match_E1_R','world_source_matches_E1_R'])
 # Raw formation speech has been read by the assistant. This sidecar does not overwrite contributor qualification.
 quotes=[{'round':2,'agent':m['agent'],'quote':m['message']}for m in cp['rounds'][1]['messages']]
 formation_reviews.append({'cohort':name,'reviewer':'assistant_reviewed','agreement_qualified':True,'evidence_quotes':quotes,'note':'All15actual formation utterances read: proposals then reciprocal endorsements; actual output16each in all5. Original contributor qualification says pending and remains unchanged.'})
 for arm in ['direct','unequal','talk_only','act_only','iago']:
  branch=read(prefix+'branches/unannounced_'+arm+'.json');assert len(branch['rounds'])==15;assert branch['rounds'][:5]==cp['rounds']
  intended=32 if arm in ['unequal','act_only']else 16;errors=[]
  for r in branch['rounds']:
   q=r['quantities'];P=max(0,env['demand_intercept']-env['demand_slope']*sum(q.values()));profit={a:(P-env['unit_cost'])*v for a,v in q.items()}
   if P!=r['outcome']['price']or profit!=r['outcome']['profits']:errors.append(r['round'])
   if r['round']>=8:rows.append({'cohort':name,'arm':arm,'round':r['round'],**{a:q[a]for a in env['firm_ids']},'price':P,**{a+'_profit':profit[a]for a in env['firm_ids']},'source_commit':SHA})
  assert not errors
  assert all(r['quantities']['firm_C']==intended for r in branch['rounds'][8:13])
  audit['branches'].append({'arm':arm,'rounds':15,'shared_formation_exact':True,'economics_recalculation_errors':errors,'C_target9_13_met':True,'original_cartel_output_implemented9_13':sum(all(q==16 for q in r['quantities'].values())for r in branch['rounds'][8:13]),'all_firms_zero_profit9_13':sum(all(v==0 for v in r['outcome']['profits'].values())for r in branch['rounds'][8:13])})
 reports.append(audit)
result={'source_branch':'sumin/disruption','source_commit':SHA,'contributor':'Sumin Hong','new_model_calls':0,'audit_type':'Source, economic outcomes, formation review and C action fidelity; not full independent response/coalition annotation or provider re-execution','cohorts':reports,'formation_messages_differ_between_two_cohorts':sum(a['message']!=b['message']for r,s in zip(formations[0]['rounds'],formations[1]['rounds'])for a,b in zip(r['messages'],s['messages'])),'inference':'Two generated histories support observed loss of original16unit implementation and price-war onset; do not establish universal breakup or independent profit-maximizing competition.'}
(OUT/'SOURCE_AUDIT.json').write_text(json.dumps(result,indent=2));(OUT/'formation_review.json').write_text(json.dumps(formation_reviews,indent=2))
with(OUT/'round_outcomes.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print('Audited10branches,2formation histories,150round economics; no inference. Wrote',OUT)
