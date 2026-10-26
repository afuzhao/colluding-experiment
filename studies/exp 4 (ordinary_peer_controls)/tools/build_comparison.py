"""Create a two-environment index after both separate control supplements are reviewed; no inference."""
import csv,json
from pathlib import Path
from finalize_controls import main,ROOT

def pretty(d):return ', '.join(f'{v} '+k.replace('not_applicable','N/A')for k,v in d.items())or'not observed'
def build():
 # Review-gated per-environment curation must succeed before any completion index is written.
 for env in ['E1','E2']:main(env)
 data={env:json.loads((ROOT/'artifacts'/env/'FINAL_METRICS.json').read_text())for env in ['E1','E2']};reports=ROOT/'reports';rows=[]
 text='''# Ordinary peer controls for both reaction studies

Four ordinary-C market continuations, two per environment, use the original reviewed formations and full 15-round trajectories. These are separate post hoc supplements. Each environment has one shared parent history; neither the four markets nor their messages are independent replications. The original 16-condition reaction tables remain unchanged. E2 reciprocal repairs are a separately documented version and do not enter this direct-offer comparison.

Each table concerns A and B reacting to C. Public speech is assistant annotated. Explicit private questions mention evidence collection/testing, whereas independently generated neutral accounts ask interpretation, response and concerns. Both diagnostics are frozen at round 8 and never enter market history. Neutral concern elicitation is still prompted; absence of a suspicion phrase does not establish an absence of suspicion inside the model. C's resident role changes its actual speech/actions and is not directly disclosed as an experimental label. Outcomes cannot isolate hidden role while holding words fixed.

'''
 for env,m in data.items():
  text+=f'## {env} separate descriptive results\n\n| C role and notice | Public replies | Explicit private agreement and suspicion | Neutral account agreement and suspicion |\n|---|---|---|---|\n'
  for x in m['conditions']:
   label=('Ordinary C'if x['ordinary_C']else'Original investigator C')+(' with notice'if x['condition'].startswith('notice_')else' without notice')
   text+=f"|{label}|{pretty(x['public_raw'])} ({x['public_pairs']}/2)|{pretty(x['explicit_raw'])}; suspicion {x['explicit_suspicion'].get('yes',0)}/{x['explicit_pairs']}|{pretty(x['neutral_raw'])}; suspicion {x['neutral_suspicion'].get('yes',0)}/{x['neutral_pairs']}|\n"
   rows.append({'environment':env,'condition':x['condition'],'ordinary_C':x['ordinary_C'],'public_pairs':x['public_pairs'],'public_raw':json.dumps(x['public_raw']),'public_suspicion':json.dumps(x['public_suspicion']),'explicit_pairs':x['explicit_pairs'],'explicit_raw':json.dumps(x['explicit_raw']),'explicit_suspicion':json.dumps(x['explicit_suspicion']),'explicit_conditional_acceptances':x['explicit_conditional_acceptances'],'neutral_pairs':x['neutral_pairs'],'neutral_raw':json.dumps(x['neutral_raw']),'neutral_suspicion':json.dumps(x['neutral_suspicion'])})
  text+=f"\n[Detailed {env} control report]({env}_CONTROL_RESULTS.md) · [Exact control evidence](../artifacts/{env})\n\n"
 text+='''## Reading disagreement and missingness

Suspicion and agreement remain independent; suspicious acceptances and rejections are retained in the metrics. Scope objections and a desire for indefinite coordination do not mean refusal of all collusion. An endorsement of the old price need not accept a changed offer window. Peer requests confined to elapsed round 8 can be ambiguous at the first round-9 public response. Nonproposal/N/A stays distinct from unclear. Full per-recipient quotes and notes are in public_annotations.csv and neutral_annotations.csv; original investigator speech labels are reused without rewriting them.

These controls do not repair the public/private task mismatch, prove strategic concealment, establish detector accuracy, provide independent history replication or measure cartel disruption. Role labels alone do not create a visible treatment; changed generated texts and prices are part of the observed intervention. No cross-environment pooled acceptance or suspicion rate is reported. Independent human rating remains pending.

## Data counts and runtime

| Environment | Ordinary markets completed | New explicit calls | New neutral calls | Successful new calls | Exact replays | Wall minutes | Failures |
|---|---|---|---|---|---|---|\n'''
 for env,m in data.items():
  phase=m['calls_by_phase'];text+=f"|{env}|{sum(x['completed_rounds']==15 for x in m['economics']if x['ordinary_C'])}/2|{phase.get('explicit_control_diagnostic',0)}|{phase.get('neutral_control_diagnostic',0)}|{m['new_successful_calls']}|{m['replayed_positions']}|{m['wall_minutes']:.2f}|{json.dumps(m['failures'])}|\n"
 text+='''
Each environment ordinarily contributes 12 public pair records, 8 explicit pair records and 16 neutral pair records. Public directions are 4 residents-to-C, 4 resident-to-resident and 4 C-to-resident. Explicit private directions are 4 residents-to-C and 4 resident-to-resident. Neutral directions are 8 residents-to-C and 8 resident-to-resident, spanning ordinary and original snapshots. No C-own private reports were requested; these are omitted rather than zeros. Actual failed/missing denominators override nominal counts and are listed in the per-environment reports.

## Reproducibility and source lineage

Each evidence folder contains the original end-of-5 checkpoint contents and exact source/config manifest, installed model identity, actual preparation and 15-round branches, successful request/response journal, request-position replay flags, independent diagnostics, manual review files, actual-call boundary audit, metrics and failures/corrections if any. Original investigator comparison data remain in the corresponding reaction study's artifacts/final_16. Existing diagnostics are reused as reference data, not counted as fresh inference; only new neutral accounts on those snapshots add calls.

Use tools/prepare_review.py to collect actual review sheets without automatic labels. After manual review, tools/audit_control_calls.py checks saved request visibility, frozen histories and ordinary-C system role. tools/finalize_controls.py gates reviews, source/config identity and terminal execution before curation. tools/build_comparison.py creates this index only after both finalizers succeed. None of these reporting commands runs model inference.

The model is the same pinned local qwen3.5:9b as each parent cohort; no paid API or new model weights are used. Keep this supplement distinct from Sumin Hong's separate E1 disruption evidence and from the future E2 disruption study. See the repository guide for the complete data map.
'''
 (reports/'CONTROL_COMPARISON.md').write_text(text);(reports/'CONTROL_COMPARISON.json').write_text(json.dumps(data,indent=2)+'\n')
 with(reports/'CONTROL_COMPARISON.csv').open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
 print('Built comparison after both review gates passed')
if __name__=='__main__':build()
