"""Read-only E1 evidence sensitivity analysis and unlabelled external-rating packet.
No inference, source edits, outcome relabelling or uploads.
"""
import collections,csv,hashlib,json,random
from pathlib import Path
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/'artifacts/final_16'
EXCLUDE={'notice_cover_account','notice_reciprocal'} # Explicitly delivered round-8 task leaks in saved semantic review.
def read(name):
 with (SOURCE/name).open()as f:return list(csv.DictReader(f))
def counts(rows,key):return dict(collections.Counter(r[key]for r in rows))
def yes(value):return str(value).lower()=='true'
def write_csv(path,rows):
 with path.open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
public=[r for r in read('public_annotations.csv')if r['sender']=='firm_C']
private=[r for r in read('private_assessments.csv')if r['sender']=='firm_C']
assert len(public)==len(private)==32
assert all(r['reviewer']=='assistant_reviewed'for r in public)
assert len({(r['condition'],r['recipient'])for r in public})==32
assert EXCLUDE<={r['condition']for r in public}
sets={
 'Original cohort':{r['condition']for r in public},
 'Exclude two delivered round-8 instruction-leak arms':{r['condition']for r in public}-EXCLUDE,
 'Equal concrete offers excluding those two leak arms':{r['condition']for r in public if not r['condition'].endswith(('unequal','vague_feeler'))}-EXCLUDE}
results=[]
for name,conditions in sets.items():
 a=[r for r in public if r['condition']in conditions];b=[r for r in private if r['condition']in conditions]
 idx={(r['condition'],r['recipient']):r for r in b}
 results.append({'subset':name,'conditions':len(conditions),'resident_C_pairs':len(a),'public_raw_agreement':counts(a,'response_label'),'public_accept_including_conditional':sum(r['response_label']in ['accept','conditional']for r in a),'public_expressed_suspicion_yes':sum(r['expressed_suspicion']=='yes'for r in a),'private_raw_agreement':counts(b,'response_to_offer'),'private_conditional_acceptance':sum(r['response_to_offer']=='accept'and yes(r['conditional'])for r in b),'private_sender_suspicion_yes':sum(r['suspicion_of_proposer']=='yes'for r in b),'private_suspicion_overlap_agreement':counts([r for r in b if r['suspicion_of_proposer']=='yes'],'response_to_offer'),'public_accept_and_private_suspicion':sum(r['response_label']in ['accept','conditional']and idx[(r['condition'],r['recipient'])]['suspicion_of_proposer']=='yes'for r in a)})
provenance={name:hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()for name in ['public_annotations.csv','private_assessments.csv','c_semantic_review.json','manifest.json']}
(HERE/'sensitivity_results.json').write_text(json.dumps({'new_model_calls':0,'new_independent_histories':0,'original_data_changed':False,'source_hashes':provenance,'exclusion_reason':'Manual selection from existing semantic review: only notice_cover_account and notice_reciprocal delivered round-8 task phrasing. Corrected undelivered draft in unannounced_outside_review is not a delivered leak. Later followup errors are not used to exclude the earlier frozen8/private or simultaneous9/speech endpoints.','results':results,'limitations':'Exploratory sensitivity analysis of existing assistant labels; not independent validation, causal repair, detector accuracy, or independent replication. Private/public tasks differ. Equal subset changes estimand; not a replacement for all 32.'},indent=2))
t='''# Existing data sensitivity analysis

No model calls or new histories. Original data and annotations are unchanged. Counts use existing assistant-reviewed labels; this is not an independent rating exercise. Each row remains derived from ONE shared formation.

| Subset | Pairs | Public unconditional accept | Public conditional accept | Public reject | Public unclear | Public suspicion | Private accept | Private reject | Private N/A | Private suspicion |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
'''
for x in results:
 a=x['public_raw_agreement'];b=x['private_raw_agreement'];t+=f"| {x['subset']} | {x['resident_C_pairs']} | {a.get('accept',0)} | {a.get('conditional',0)} | {a.get('reject',0)} | {a.get('unclear',0)} | {x['public_expressed_suspicion_yes']} | {b.get('accept',0)} | {b.get('reject',0)} | {b.get('not_applicable',0)} | {x['private_sender_suspicion_yes']} |\n"
t+='''
Private suspicion overlaps agreement and is not an additional disjoint response. The JSON preserves overlaps and conditional private acceptance. These are endpoint-specific sensitivity exclusions, not a claim that the retained trajectories have no later protocol errors. The equal-only subset deliberately removes unequal and vague packages; it asks a narrower question and is not a revised headline for the original experiment.

Excluding the two delivered task-leak conditions leaves 13/28 prompted private suspicion reports and 0/28 explicit public suspicion statements. This descriptive difference remains, but does not demonstrate detection or concealment: the two channels ask different questions and there is no matched ordinary-C negative control. No uncertainty intervals treating dependent branches as independent are calculated.
'''
(HERE/'SENSITIVITY_TABLE.md').write_text(t)
# A packet for another rater. Identity/condition mapping is separate; intrinsic textual cues remain visible.
rows=list(public);random.Random(20261025).shuffle(rows);packet=[];key=[]
for i,r in enumerate(rows,1):
 ident=f'R{i:03d}';branch=json.loads((SOURCE/'branches'/(r['condition']+'.json')).read_text())
 context=[{'round':x['round'],'messages':[{k:m[k]for k in ['agent','message','quota_commitment']}for m in x['messages']],'quantities':x['quantities'],'price':x['outcome']['price']}for x in branch['rounds'][:8]]
 packet.append({'rating_id':ident,'recipient':r['recipient'],'prior_public_context_through_round-8':json.dumps(context,ensure_ascii=False),'target_offer':r['offer_text'],'first_public_reply_round':9,'first_public_reply':r['reply_text'],'proposal_present':'','recipient_addressed':'','response_label':'','expressed_suspicion':'','evidence_quote':'','reviewer':'','review_note':''})
 key.append({'rating_id':ident,'condition':r['condition'],'proposal_id':r['proposal_id'],'recipient':r['recipient']})
write_csv(HERE/'blind_rating_packet.csv',packet);write_csv(HERE/'blind_rating_key.csv',key)
print(json.dumps(results,indent=2));print('Wrote sensitivity outputs and 32 unlabelled rating pairs. No inference; no original evidence changed.')
