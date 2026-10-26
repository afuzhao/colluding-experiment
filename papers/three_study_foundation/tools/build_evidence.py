"""Rebuild three-study derived summaries and mathematical checks from immutable evidence; no model calls."""
import csv,hashlib,itertools,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[1];OUT=ROOT/'data';OUT.mkdir(exist_ok=True)
E1=REPO/'studies/exp 2 (insider_reactions_v3)';E2=REPO/'studies/exp 3 (env2_reactions)';CT=REPO/'studies/exp 4 (ordinary_peer_controls)';D=REPO/'studies/exp 5 (env1_disruption)'
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
sys.path.insert(0,str(E1));from trusted_study.world import clear_market
sys.path.insert(0,str(REPO/'environments/env 2 (differentiated_prices)'));from market_env.economics import Market
m=Market();cfg=read(E1/'configs/study.json');ids=['firm_A','firm_B','firm_C']
def qclear(q):return clear_market(dict(zip(ids,q)),cfg['environment'])
# Exhaustively check finite quantity-game best responses, retaining ties.
br={s:{q for q in range(41)if (max(0,100-s-q)-4)*q==max((max(0,100-s-v)-4)*v for v in range(41))}for s in range(81)}
ne1=[q for q in itertools.product(range(41),repeat=3)if all(q[i]in br[sum(q)-q[i]]for i in range(3))]
# Same demand model for all products: one best-response lookup per unordered rival pair.
br2={}
for b in m.grid:
 for c in m.grid:
  if b<=c:br2[(b,c)]=set(m.best_responses({'firm_A':4,'firm_B':b,'firm_C':c},'firm_A')['prices'])
ne2=[p for p in itertools.product(m.grid,repeat=3)if all(p[i]in br2[tuple(sorted(p[j]for j in range(3)if j!=i))]for i in range(3))]
math={'new_model_calls':0,'E1_pure_integer_stage_equilibria':ne1,'E2_pure_integer_stage_equilibria':ne2,'E1_benchmarks':{},'E2_benchmarks':{},'infinite_horizon_illustration':{'E1_cooperate_deviate_punish':[768,1024,576],'E2_cooperate_deviate_punish':[1200,1600,900],'grim_trigger_threshold_both':'4/7','applied_to_actual_finite15_game':False}}
for name,q in [('joint',(16,16,16)),('symmetric_independent',(24,24,24)),('unilateral_deviation',(32,16,16)),('competitive_C_AB_unchanged',(16,16,32)),('all32',(32,32,32)),('profitable_deviation_from_all32',(16,32,32))]:math['E1_benchmarks'][name]={'quantities':q,**qclear(q)}
for name,p in [('joint',(64,64,64)),('symmetric_independent',(34,34,34)),('unilateral_deviation',(44,64,64)),('partial_coalition',(42,42,37)),('unequal_offer',(76,76,52))]:math['E2_benchmarks'][name]=m.clear(dict(zip(ids,p)))
math['E1_best_response_to_B16_C32']=sorted(br[48]);math['E1_best_response_to_B32_C32']=sorted(br[64]);math['E2_conditional_AB_independent_given_C37']=m.conditional_ab_nash(37)
math['E2_AB_joint_best_response_C37']=m.coalition_best_responses({'firm_A':42,'firm_B':42,'firm_C':37},['firm_A','firm_B'])
assert ne1==[(23,24,25),(23,25,24),(24,23,25),(24,24,24),(24,25,23),(25,23,24),(25,24,23)]
assert ne2==[(34,34,34)]
assert math['E1_best_response_to_B32_C32']==[16]
assert abs(math['E2_benchmarks']['partial_coalition']['profits']['firm_A']-975.3333333333334)<1e-6
save(OUT/'mathematical_checks.json',math)
conditions=[];summary={};tables=[]
for label,folder,metricsfile in [('E1-R',E1/'artifacts/final_16',E1/'artifacts/final_16/FINAL_METRICS.json'),('E2-R selected',E2/'artifacts/combined_16',E2/'artifacts/combined_16/FINAL_METRICS.json')]:
 r=read(folder/'results.json');pub=r['public_evidence'];prv=r['private_assessments'];cp=[x for x in pub if x['sender']=='firm_C'];cv=[x for x in prv if x['sender']=='firm_C'];cnt=lambda rows,k:dict(__import__('collections').Counter(x[k]for x in rows))
 summary[label]={'independent_generated_histories':1,'public_C_pairs':len(cp),'public_raw':cnt(cp,'response_label'),'public_suspicion':cnt(cp,'expressed_suspicion'),'private_C_pairs':len(cv),'private_raw':cnt(cv,'response_to_offer'),'private_suspicion':cnt(cv,'suspicion_of_proposer'),'private_suspicion_overlaps':cnt([x for x in cv if x['suspicion_of_proposer']=='yes'],'response_to_offer'),'notice_private_suspicion':{str(notice):sum(x['suspicion_of_proposer']=='yes'for x in cv if x['condition'].startswith('notice_')==notice)for notice in [False,True]},'metrics_source':str(metricsfile.relative_to(REPO))}
 table='| Condition | Evidence version | Public headline | Private headline | Private suspicion | A/B adherence |\n|---|---|---|---|---|---|\n'
 pretty=lambda d:', '.join(f'{v} '+k.replace('not_applicable','N/A')for k,v in d.items()if v)
 for x in r['conditions']:
  counts=x['quota_adherence_counts']if label=='E1-R'else x['price_adherence_counts'];ad='N/A'if not x['concrete_assigned_offer']else' · '.join(f"{counts[a]}/{x['window_rounds']}"for a in ['firm_A','firm_B'])
  row={'study':label,'condition':x['condition'],'revision':x.get('evidence_revision','original'),'public_headline':pretty(x['public_counts']),'private_headline':pretty(x['private_counts']),'private_suspicion':x['private_suspicion_yes'],'private_pairs':x['private_observed'],'AB_adherence':ad,'mean_price9_13':x['mean_window_price'],'mean_resident_profit9_13':x['mean_resident_window_profit'],'mean_consumer_surplus9_13':x['mean_consumer_surplus']};conditions.append(row)
  table+=f"|{row['condition']}|{row['revision']}|{row['public_headline']}|{row['private_headline']}|{row['private_suspicion']}/{row['private_pairs']}|{ad}|\n"
 tables.append('## '+label+'\n\n'+table)
( ROOT/'RESULTS_TABLES.md').write_text('# Complete reaction condition tables\n\nDerived without new inference. Suspicion has headline precedence, conditional acceptance displays as accept; raw agreement is retained in source metrics. The two E2 reciprocal slots are revised prompts, not original successes.\n\n'+'\n'.join(tables))
with(OUT/'reaction_conditions.csv').open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=list(conditions[0]),lineterminator='\n');w.writeheader();w.writerows(conditions)
summary['controls']={env:read(CT/'artifacts'/env/'FINAL_METRICS.json')for env in ['E1','E2']};summary['E1-D_audit']=read(D/'reports/SOURCE_AUDIT.json');summary['E1-R_leak_sensitivity']=read(E1/'supplements/design_review_2026_10_25/sensitivity_results.json')
sourcepaths=[E1/'artifacts/final_16/results.json',E1/'artifacts/final_16/FINAL_METRICS.json',E2/'artifacts/combined_16/results.json',E2/'artifacts/final_16/FINAL_METRICS.json',E2/'artifacts/combined_16/FINAL_METRICS.json',CT/'artifacts/E1/FINAL_METRICS.json',CT/'artifacts/E2/FINAL_METRICS.json',D/'reports/SOURCE_AUDIT.json',D/'reports/round_outcomes.csv',E1/'trusted_study/world.py',E1/'configs/study.json',REPO/'environments/env 2 (differentiated_prices)/market_env/economics.py',REPO/'environments/env 2 (differentiated_prices)/configs/environment.json']
summary['source_sha256']={str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest()for p in sourcepaths};save(OUT/'evidence_summary.json',summary)
print(json.dumps({'new_model_calls':0,'quantity_stage_NE_count':len(ne1),'price_stage_NE_count':len(ne2),'condition_rows':len(conditions),'sources_hashed':len(sourcepaths)},indent=2))
