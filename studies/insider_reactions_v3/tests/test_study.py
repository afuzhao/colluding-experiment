import copy,io,json,tempfile,unittest
from contextlib import redirect_stdout
from pathlib import Path
from trusted_study.protocol import IDS,MARKERS,config,conditions,system
from trusted_study.engine import run_markets,checked_call
from trusted_study.assessments import run_assessments,diagnostic_observation,validate_report
from trusted_study.reporting import report,headline

class Fixture:
 def __init__(self,output):self.output=Path(output);self.calls=0;self.observations=[]
 def generate(self,sys,obs,sc,seed,validator,tag):
  self.calls+=1;self.observations.append(copy.deepcopy((sys,obs,tag)))
  if tag['phase']=='private_assessment':
   out={'assessments':[{'proposal_id':p['proposal_id'],'proposal_present':'no','response_to_offer':'not_applicable','conditional':False,'suspicion_of_proposer':'yes'if tag['condition'].endswith('vague_feeler')and p['sender']=='firm_C'else'no','brief_explanation':'TEST FIXTURE ONLY'}for p in obs['peer_texts']]}
  elif tag['kind']=='quantity':out={'quantity':32 if tag.get('condition','').endswith('unequal')and tag['agent']=='firm_C'and 9<=tag['round']<=13 else 16}
  elif tag['kind']=='preparation':out={'preparation_choice':obs['CURRENT_TASK'].split('preparation_choice=')[1].split()[0]}
  else:
   approach=next((a for a in config()['conditions']['approaches']if tag.get('condition','').endswith('_'+a)),None)
   if tag['round']==8 and tag['agent']=='firm_C'and approach:
    if approach=='vague_feeler':out={'message':MARKERS[approach],'quota_commitment':None}
    else:out={'message':'Please agree to '+('A=8, B=8, C=32'if approach=='unequal'else'A=16, B=16, C=16')+' for rounds 9 through 13. '+MARKERS.get(approach,''),'quota_commitment':None if approach=='unequal'else 16}
   else:out={'message':'TEST FIXTURE ONLY. I commit to the quota of 16.','quota_commitment':16}
  validator(out);return out

class StudyTests(unittest.TestCase):
 def test_shared_prefixes_budget_visibility_and_diagnostics(self):
  c=config()
  with tempfile.TemporaryDirectory()as t:
   f=Fixture(t)
   with redirect_stdout(io.StringIO()):r=run_markets(c,f,t)
   self.assertEqual(r['state'],'markets_complete');self.assertEqual(f.calls,822)
   branches=[json.loads(p.read_text())for p in(Path(t)/'branches').glob('*.json')];self.assertEqual(len(branches),16)
   for sys,obs,tag in f.observations:
    self.assertEqual(len(obs['current_messages']),3 if tag['kind']=='quantity'else 0)
    self.assertNotIn('assigned_offer',json.dumps(obs));self.assertNotIn('message_id',json.dumps(obs))
    if tag['round']<8:self.assertNotIn('MONITORING NOTICE',sys)
   for a in c['conditions']['approaches']:
    pair=[b for b in branches if b['condition']['approach']==a];self.assertEqual(pair[0]['rounds'][:7],pair[1]['rounds'][:7])
   for b in branches:
    for agent in IDS:
     d=diagnostic_observation(b,c,agent);self.assertEqual(max(x['round']for x in d['public_history']),8)
     self.assertEqual(len(d['peer_texts']),2);self.assertTrue(all(x['sender']!=agent for x in d['peer_texts']))
   before=copy.deepcopy(branches)
   with redirect_stdout(io.StringIO()):self.assertEqual(run_assessments(c,f,t),[])
   self.assertEqual(f.calls,870);self.assertEqual(branches,before)
   result=report(c,t);self.assertEqual(len(result['public_evidence']),96);self.assertEqual(len(result['private_assessments']),96)
   vague=[x for x in result['conditions']if x['approach']=='vague_feeler']
   self.assertTrue(all(x['quota_adherence_counts']is None for x in vague))
   self.assertTrue(all(x['private_counts']['suspicious']==2 for x in vague))
   self.assertTrue(all(x['private_agreement_counts']['not_applicable']==2 for x in vague))
   self.assertTrue(all(x['public_reviewed']==0 for x in result['conditions']))
 def test_bounded_repair_and_no_silent_quantity_override(self):
  c=config();cond=conditions(c)[0]
  with tempfile.TemporaryDirectory()as t:
   class WrongOnce(Fixture):
    def generate(self,*args):
     out=super().generate(*args);return {'message':'wrong window','quota_commitment':16}if self.calls==1 else out
   f=WrongOnce(t);ans=checked_call({'rounds':[]},c,f,'firm_C',8,'message',cond)
   self.assertIn('rounds 9 through 13',ans['message']);self.assertEqual(f.calls,2)
   class WrongQuantity(Fixture):
    def generate(self,*args):super().generate(*args);return {'quantity':24}
   f=WrongQuantity(t);ans=checked_call({'rounds':[]},c,f,'firm_C',6,'quantity',cond)
   self.assertEqual(ans['quantity'],24);self.assertEqual(f.calls,1)
   log=[json.loads(x)for x in(Path(t)/'c_fidelity.jsonl').read_text().splitlines()]
   self.assertFalse(log[-1]['compliant']);self.assertTrue(log[-1]['delivered'])
 def test_notice_timing_and_nonproposal_suspicion(self):
  c=config();cond=next(x for x in conditions(c)if x['notice'])
  self.assertNotIn('MONITORING NOTICE',system(c,'firm_A',cond,7));self.assertIn('MONITORING NOTICE',system(c,'firm_A',cond,8))
  self.assertEqual(headline('not_applicable','yes','no'),'suspicious');self.assertEqual(headline('not_applicable','no','no'),'not_applicable')
 def test_no_proposal_still_requires_independent_suspicion(self):
  row={'proposal_id':'p','proposal_present':'no','response_to_offer':'not_applicable','conditional':False,'suspicion_of_proposer':'yes','brief_explanation':'Test'}
  self.assertEqual(validate_report({'assessments':[row]},['p'])['assessments'][0]['suspicion_of_proposer'],'yes')
  row['response_to_offer']='reject'
  with self.assertRaises(ValueError):validate_report({'assessments':[row]},['p'])
if __name__=='__main__':unittest.main()
