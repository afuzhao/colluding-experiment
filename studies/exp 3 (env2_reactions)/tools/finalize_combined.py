"""Combine original and supplemental reciprocal evidence without overwriting either.
Call only after both executions and assistant transcript/semantic reviews complete.
"""
import collections,csv,gzip,html,json,shutil,sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from price_study.protocol import ROOT,config,conditions
from price_study.reporting import report,show,display_name
from price_study.engine import manifest
from price_study.utils import write_json
c=config();original=ROOT/'results/final_16';repair=ROOT/'results/reciprocal_repairs_v1';combined=ROOT/'results/combined_16'
for folder in [original,repair]:
 status=json.loads((folder/'status.json').read_text())
 if status['state']not in ['complete','complete_with_failures']:raise SystemExit(str(folder)+' is still active')
base=json.loads((original/'manifest.json').read_text())
if base!=manifest(c):raise SystemExit('Original frozen source/config drift')
provenance=json.loads((repair/'repair_manifest.json').read_text())
if provenance['base_manifest']!=base or any(Path(p).read_text()!=t for p,t in provenance['repair_sources'].items()):raise SystemExit('Repair source drift')
results=[report(c,f)for f in [original,repair]]
for folder,r in zip([original,repair],results):
 for x in r['public_evidence']:
  if x['reviewer']!='assistant_reviewed'or x['response_label']not in ['accept','conditional','reject','unclear','not_applicable']or x['expressed_suspicion']not in ['yes','no','unclear']or x['proposal_present']not in ['yes','no','unclear']or x['recipient_addressed']not in ['yes','no','unclear']:raise SystemExit('Unreviewed public pair in '+str(folder))
  if not x['evidence_quote']or not any(x['evidence_quote']in x[k]for k in ['reply_text','offer_text']):raise SystemExit('Nonexact quote')
 sem=json.loads((folder/'c_semantic_review.json').read_text());expected={x['condition']for x in r['conditions']if x['latest_round']>=8}
 if{x['condition']for x in sem}!=expected or any(x.get('reviewer')!='assistant_reviewed'for x in sem):raise SystemExit('Missing semantic review')
combined.mkdir(exist_ok=True);selected=[];public=[];private=[]
for cond in conditions(c):
 i=1 if cond['approach']=='reciprocal'else 0;r=next(x for x in results[i]['conditions']if x['condition']==cond['id']);selected.append(r|{'evidence_revision':'repaired_C_prompt_v1'if i else'original','source_output':str([original,repair][i].relative_to(ROOT))})

 if not r['market_complete']:raise SystemExit('Selected condition incomplete: '+cond['id'])
 public +=[x|{'evidence_revision':selected[-1]['evidence_revision']}for x in results[i]['public_evidence']if x['condition']==cond['id']]
 private +=[x|{'evidence_revision':selected[-1]['evidence_revision']}for x in results[i]['private_assessments']if x['condition']==cond['id']]
for name,rows in [('public_annotations.csv',public),('private_assessments.csv',private)]:
 if rows:
  with(combined/name).open('w')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
c_pub=[x for x in public if x['sender']=='firm_C'];c_prv=[x for x in private if x['sender']=='firm_C']
role=lambda rows,key:dict(collections.Counter(x[key]for x in rows))
metrics={'design':'One encouraged shared formation;14original condition slots plus2explicitly revised reciprocal slots; not16unchanged-protocol successes','original_execution':json.loads((original/'FINAL_METRICS.json').read_text()),'repair_execution':json.loads((repair/'status.json').read_text()),'completed_selected_scenarios':sum(x['market_complete']for x in selected),'selected_scenarios':selected,'public_C_pairs':len(c_pub),'private_C_pairs':len(c_prv),'public_C_raw_agreement':role(c_pub,'response_label'),'public_C_suspicion':role(c_pub,'expressed_suspicion'),'private_C_raw_agreement':role(c_prv,'response_to_offer'),'private_C_suspicion':role(c_prv,'suspicion_of_proposer'),'private_C_accept_conditional_count':sum(x['response_to_offer']=='accept'and x['conditional']for x in c_prv),'public_C_conditional_count':sum(x['response_label']=='conditional'for x in c_pub),'public_headline_totals':{k:sum(x['public_counts'][k]for x in selected)for k in ['accept','reject','suspicious','unclear','not_applicable']},'private_headline_totals':{k:sum(x['private_counts'][k]for x in selected)for k in ['accept','reject','suspicious','unclear','not_applicable']},'separate_roles':{}}
for name,pr,pv in [('resident_to_resident',[x for x in public if x['sender']!='firm_C'and x['recipient']!='firm_C'],[x for x in private if x['sender']!='firm_C'and x['recipient']!='firm_C']),('C_own',[x for x in public if x['recipient']=='firm_C'],[x for x in private if x['recipient']=='firm_C'])]:metrics['separate_roles'][name]={'public_pairs':len(pr),'public_agreement':role(pr,'response_label'),'public_suspicion':role(pr,'expressed_suspicion'),'private_pairs':len(pv),'private_agreement':role(pv,'response_to_offer'),'private_suspicion':role(pv,'suspicion_of_proposer')}
metrics['private_C_suspicion_overlaps']=[x for x in c_prv if x['suspicion_of_proposer']=='yes']
metrics['repair_new_journal_calls']=sum(1 for _ in(repair/'calls.jsonl').open())if(repair/'calls.jsonl').exists()else 0
metrics['repair_replayed_positions']=sum(json.loads(x)['replayed']for x in(repair/'request_positions.jsonl').read_text().splitlines())
metrics['repair_runtime_minutes']=(datetime.fromisoformat(metrics['repair_execution']['finished_utc'])-datetime.fromisoformat(metrics['repair_execution']['started_utc'])).total_seconds()/60
write_json(combined/'FINAL_METRICS.json',metrics);write_json(combined/'results.json',{'conditions':selected,'public_evidence':public,'private_assessments':private,'limitations':metrics['design']})
table='| Scenario | Public replies | Private assessments | Private suspicion | A/B adherence9–13 |\n|---|---|---|---|---|\n'
for x in selected:
 q=x['price_adherence_counts'];n=x['window_rounds'];ad=f"{q['firm_A']}/{n} · {q['firm_B']}/{n}"if q and n else'N/A—no precise offer'if n else'not available'
 name=display_name(x['condition'])+(' *'if x['evidence_revision']!='original'else'')
 table+=f"|{name}|{show(x['public_counts'],x['public_observed']-x['public_reviewed'])}|{show(x['private_counts'])}|{x['private_suspicion_yes']}/{x['private_observed']}|{ad}|\n"
(combined/'RESULTS_TABLE.md').write_text(table)
original_report=ROOT/'reports/ORIGINAL_COHORT_RESULTS.md'
if not original_report.exists():shutil.copy2(ROOT/'reports/FINAL_RESULTS.md',original_report)
original_text=original_report.read_text()
intro=f'''# Environment2 reactions: original cohort and reciprocal repairs

The original cohort completed 14 of 16 conditions and 42 eligible private calls; both reciprocal conditions failed C's exact wording before an offer was delivered. Those failures remain intact. Two supplemental reruns retain the same actual 7-round prefixes and 15-round horizon, but clarify C's round 8 prompt with a complete reciprocal message to copy. They are explicitly revised treatment-delivery conditions, not original successes. All other model weights, seeds, sampling, histories, market rules and model-selected prices remain unchanged. No independent new formation was generated for repairs.

## Selected 16 condition view

{table}

*Reciprocal rows use supplemental repaired-prompt evidence. Nonprecise vague requests have no offered-price adherence denominator. Public labels are assistant transcript annotations, not human/independent validation. Conditional acceptance maps to acceptance; suspicion has display precedence and raw agreement is retained. Bare old-price renewal is not automatically acceptance of C's new window or request. Standing resident-to-resident renewals have an indefinite horizon and are coded separately; these are not fully matched speech stimuli.

## Counts and overlaps

Public resident-to-C: {len(c_pub)} actual pairs; raw agreement {json.dumps(metrics['public_C_raw_agreement'])}; expressed suspicion {json.dumps(metrics['public_C_suspicion'])}. Private resident-to-C: {len(c_prv)} actual pairs; raw agreement {json.dumps(metrics['private_C_raw_agreement'])}; suspicion {json.dumps(metrics['private_C_suspicion'])}. Conditional acceptances: public {metrics['public_C_conditional_count']}; private {metrics['private_C_accept_conditional_count']}. Private suspicion overlaps are preserved in the machine-readable metrics, including acceptance/rejection and N/A. Private retrospective reports are elicited answers, not internal-state ground truth. Ordinary-peer and C-own denominators: {json.dumps(metrics['separate_roles'])}.

## Runtime and provenance

Original successful journal calls: {metrics['original_execution']['successful_inference_calls']}; original wall time including formation review/maintenance: {metrics['original_execution']['wall_minutes_including_formation_review']} minutes. Supplemental new successful journal calls: {metrics['repair_new_journal_calls']}; exact parent-request replay positions: {metrics['repair_replayed_positions']}; supplemental wall time: {metrics['repair_runtime_minutes']:.2f} minutes. Replays are not new observations. Isolated performance probes and operational pauses remain separate development records. Neither the alternate call order nor cache resets demonstrated reliable production acceleration. No source/horizon/history shortening was used for speed.

## Scope and evidence

One benchmark-informed encouraged formation supports descriptive elicitation; no detector accuracy or general causal disruption claim. Unequal-offer rejection is not rejection of collusion. A/B prices may change because C changes its own price. Model economic errors, premature assent claims and later C follow-up deviations are retained in both semantic-review files. Revised reciprocal wording should not be treated as an unchanged strategy replication. A separate ordinary-C supplement is queued for both environments with full 15-round economic trajectories; it has no results until actually executed. E1-R remains a separate completed cohort; broad cross-study interpretation is deferred.

Curated evidence: artifacts/final_16 (original), artifacts/reciprocal_repairs_v1 (supplement), artifacts/combined_16 (derived index). The original source/config manifest and source request journal are the parent for imported repair requests; repair_manifest.json records the exact prompt override and driver. No original qualification or failure file is deleted.

## Original cohort methods and audit

The following material describes the original cohort and its original failures, not the selected 16-condition repair view above.

'''
(ROOT/'reports/FINAL_RESULTS.md').write_text(intro+original_text)
(ROOT.parents[1]/'docs/ENV2_REACTIONS_SUMMARY.md').write_text(intro.split('## Original cohort methods')[0])
page=['<!doctype html><meta charset="utf-8"><title>E2 reactions:16condition evidence</title><style>body{font:16px/1.6 system-ui;max-width:1300px;margin:40px auto;padding:20px;background:#f1f5f6;color:#17333d}table{border-collapse:collapse;background:white}td,th{border:1px solid #cad8de;padding:10px}th{background:#d9eae5}pre{white-space:pre-wrap}</style><h1>Environment2 reactions: original and repaired evidence</h1><p>14original condition slots +2explicit revised reciprocal slots. One shared formation. Original failures retained. Private reports are not internal-state ground truth.</p><table>']
for line in table.splitlines():
 if line.startswith('|---'):continue
 cells=[x.strip()for x in line.strip('|').split('|')];tag='th'if line.startswith('| Scenario')else'td';page.append('<tr>'+''.join('<'+tag+'>'+html.escape(v)+'</'+tag+'>'for v in cells)+'</tr>')
page.append('</table><p>*Revised reciprocal prompt. <a href="public_annotations.csv">Public evidence</a> · <a href="private_assessments.csv">Private reports</a> · <a href="FINAL_RESULTS.md">Methods/results</a></p>');(combined/'results.html').write_text(''.join(page));shutil.copy2(ROOT/'reports/FINAL_RESULTS.md',combined/'FINAL_RESULTS.md')
for source,name in [(repair,'reciprocal_repairs_v1'),(combined,'combined_16')]:
 target=ROOT/'artifacts'/name;target.mkdir(parents=True,exist_ok=True)
 for f in source.iterdir():
  if f.is_file()and f.name!='calls.jsonl':shutil.copy2(f,target/f.name)
 for sub in ['branches','assessments']:
  if(source/sub).exists():shutil.copytree(source/sub,target/sub,dirs_exist_ok=True)
 if(source/'calls.jsonl').exists():
  with(source/'calls.jsonl').open('rb')as src,gzip.open(target/'calls.jsonl.gz','wb')as dest:shutil.copyfileobj(src,dest)
print(json.dumps({k:metrics[k]for k in ['completed_selected_scenarios','public_headline_totals','private_headline_totals','repair_new_journal_calls','repair_runtime_minutes']},indent=2))
