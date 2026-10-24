import copy
import csv
import json
import tempfile
import unittest
from pathlib import Path
from trusted_lab.environment import ROOT, load_config, new_state, clone_state, stable_hash, system_prompt, score_decisions
from trusted_lab.model import MockClient
from trusted_lab.runner import run_experiment
from trusted_lab.report import summarise

class ExperimentTests(unittest.TestCase):
    def setUp(self): self.config=load_config(ROOT/'configs/pilot.json')

    def test_branch_does_not_modify_checkpoint(self):
        prefix=new_state(self.config,0); before=stable_hash(prefix)
        branch=clone_state(prefix); branch['public_history'].append({'message':'new'})
        self.assertEqual(stable_hash(prefix),before)
        self.assertNotEqual(stable_hash(branch),before)

    def test_only_strategy_part_of_trusted_prompt_changes(self):
        base=(ROOT/'prompts/trusted_base.txt').read_text()+'\nASSIGNED APPROACH\n'
        for approach in self.config['approaches']:
            self.assertEqual(system_prompt('trusted',approach),base+(ROOT/f'prompts/approaches/{approach}.txt').read_text())
        self.assertNotEqual(system_prompt('trusted','direct'),system_prompt('trusted','ordinary'))

    def test_entrant_excluded_from_resident_metrics(self):
        d=[{'agent':'resident_1','facts':{'peer_valid':False,'entrant_present':True},'peer_decision':'APPROVE','entrant_decision':'REJECT'},
           {'agent':'trusted','facts':{'peer_valid':False,'entrant_present':True},'peer_decision':'REJECT','entrant_decision':'NA'}]
        scored=score_decisions(d)
        self.assertEqual(scored['bad_opportunities'],1)
        self.assertEqual(scored['bad_approvals'],1)
        self.assertEqual(scored['review_opportunities'],1)

    def test_gradual_requires_actual_extra_round(self):
        config=copy.deepcopy(self.config);config['contact_rounds']=1
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'config.json';path.write_text(json.dumps(config))
            with self.assertRaisesRegex(ValueError,'Gradual'): load_config(path)

    def test_nonqualifying_history_never_enters_intervention(self):
        class RejectingClient(MockClient):
            def generate(self,*args,**kwargs):
                parsed,raw=super().generate(*args,**kwargs)
                if 'peer_decision' in parsed: parsed['peer_decision']='REJECT'
                return parsed,raw
        config=copy.deepcopy(self.config);config.update(histories=1,warmup_rounds=1)
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'run';client=RejectingClient(config)
            run_experiment(config,client,path)
            record=json.loads((path/'histories.json').read_text())[0]
            self.assertFalse(record['qualified'])
            self.assertEqual(record['branches'],[])
            self.assertEqual(client.calls,4)

    def test_paired_conditions_and_pending_annotations(self):
        config=copy.deepcopy(self.config);config.update(histories=1,warmup_rounds=1,contact_rounds=2,followup_rounds=1)
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'run';run_experiment(config,MockClient(config),path)
            history=json.loads((path/'histories.json').read_text())[0]
            self.assertTrue(history['qualified'])
            self.assertEqual(len(history['branches']),5)
            self.assertTrue(all(b['start_state_hash']==history['checkpoint_hash'] for b in history['branches']))
            manifest,rows=summarise(path)
            self.assertEqual(manifest['backend'],'mock')
            self.assertTrue(all(r['acceptance_rate'] is None and r['expressed_suspicion_rate'] is None for r in rows))
            self.assertTrue(all(r['followup_bad_approval_difference_vs_control']==0 for r in rows))
            self.assertEqual(len({r['approach'] for r in rows}),5)
            annotation_path=path/'annotations.csv'
            with annotation_path.open() as f:
                reader=csv.DictReader(f); fields=reader.fieldnames; annotations=list(reader)
            first=next(a for a in annotations if a['approach']=='direct')
            first.update(qualifying_offer='yes',response_label='accept',expressed_suspicion='yes')
            def save():
                with annotation_path.open('w',newline='') as f:
                    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(annotations)
            save(); _,partial=summarise(path)
            self.assertIsNone(next(r for r in partial if r['approach']=='direct')['acceptance_rate'])
            for annotation in annotations:
                if not annotation['qualifying_offer']: annotation['qualifying_offer']='no'
            save(); _,labelled=summarise(path)
            direct=next(r for r in labelled if r['approach']=='direct')
            self.assertEqual(direct['acceptance_rate'],1)
            self.assertEqual(direct['expressed_suspicion_rate'],1)
            self.assertEqual(direct['offer_coverage'],0.5)


if __name__=='__main__': unittest.main()
