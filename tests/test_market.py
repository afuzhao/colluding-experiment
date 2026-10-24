import copy
import json
import tempfile
import unittest
from pathlib import Path
from trusted_lab.market import ROOT, ENTRANT, load_market_config, market_outcome, new_market_state, market_observation, qualifies, run_market, market_report

class MarketFixture:
    backend='mock'
    def __init__(self,c): self.config=c;self.calls=0
    def identity(self):return {'name':'MOCK_ONLY','digest':'not-a-real-model'}
    def generate(self,system,observation,kind,seed):
        self.calls+=1;obs=json.loads(observation)
        if kind=='market_price':out={'price':8}
        elif kind in ('market_trusted_message','market_preparation_message'):
            ordinary=system.split('ASSIGNED APPROACH\n')[1].startswith('CONTROL CONDITION.')
            active=obs['contact_round']==3 and not ordinary
            out={'message':'We can maintain the proposed floor.' if active else 'Hello, how is the market going?','preparation_choice':'OBSERVE','make_offer':active}
        else:out={'message':'I agree to maintain a price floor of 8.'}
        return out,{'request':{'system':system,'observation':observation},'response':out}

class MarketTests(unittest.TestCase):
    def setUp(self):self.c=load_market_config(ROOT/'configs/market.json')
    def test_payoffs_ties_and_deviation(self):
        x=market_outcome({'a':8,'b':8},self.c)
        self.assertEqual(x['profits'],{'a':168,'b':168});self.assertEqual(x['consumer_surplus'],196)
        x=market_outcome({'a':7,'b':8},self.c)
        self.assertEqual(x['profits'],{'a':320,'b':0})
        x=market_outcome({'a':8,'b':8,'c':8},self.c)
        self.assertEqual(list(x['profits'].values()),[112,112,112])
    def test_preparation_action_space_cannot_offer(self):
        from trusted_lab.model import SCHEMAS
        self.assertEqual(SCHEMAS['market_preparation_message']['properties']['make_offer']['enum'],[False])

    def test_neutral_public_identity(self):
        s=new_market_state(self.c,0)
        obs=market_observation(s,self.c,'seller_1','contact',1)
        self.assertNotIn('trusted',json.dumps(obs));self.assertNotIn('available_test_transaction',obs)
    def test_sustained_qualification(self):
        s=new_market_state(self.c,0);s['rounds']=[{'prices':{'seller_1':8,'seller_2':8}}]*3
        self.assertTrue(qualifies(s,self.c))
        s['rounds']=copy.deepcopy(s['rounds']);s['rounds'][-1]['prices']['seller_1']=7
        self.assertFalse(qualifies(s,self.c))
    def test_fixed_protocol_and_checkpoint_branches(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'run';client=MarketFixture(self.c);run_market(self.c,client,out)
            self.assertEqual(client.calls,159)
            hist=json.loads((out/'histories.json').read_text())[0]
            self.assertTrue(all(b['start_hash']==hist['checkpoint_hash'] for b in hist['branches']))
            for a in self.c['approaches']:
                state=json.loads((out/'history_000'/f'{a}.json').read_text())
                self.assertEqual(len(state['rounds']),12)
                offered=[r for r in state['rounds'] if r['offer']]
                self.assertEqual(len(offered),0 if a=='ordinary' else 1)
                if offered:
                    self.assertEqual(offered[0]['round'],9)
                    self.assertEqual(offered[0]['offer']['end_round'],11)
                self.assertTrue(all(r['prices'][ENTRANT]==8 for r in state['rounds'] if r['phase']!='formation'))
            resumed=Path(d)/'resumed';resume_client=MarketFixture(self.c)
            run_market(self.c,resume_client,resumed,checkpoint=out/'history_000/checkpoint.json')
            self.assertEqual(resume_client.calls,135)
            resumed_history=json.loads((resumed/'histories.json').read_text())[0]
            self.assertEqual(resumed_history['checkpoint_hash'],hist['checkpoint_hash'])
            self.assertTrue(all(b['start_hash']==hist['checkpoint_hash'] for b in resumed_history['branches']))
            summary=market_report(out)
            self.assertTrue(all(r['candidate_response_rates']['accept'] is None for r in summary))
            self.assertTrue(all(r['joint_floor_difference_vs_ordinary']==0 for r in summary))
    def test_common_message_budget_is_enforced_and_logged(self):
        from trusted_lab.market import play_round
        class VerboseFixture(MarketFixture):
            def generate(self,*args,**kwargs):
                out,raw=super().generate(*args,**kwargs)
                if 'message' in out:out['message']=' '.join(['word']*70)
                return out,raw
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d);state=new_market_state(self.c,0)
            play_round(state,self.c,VerboseFixture(self.c),None,'formation',None,folder)
            self.assertTrue(all(len(m['message'].split())==60 for m in state['rounds'][0]['messages']))
            events=[json.loads(line) for line in (folder/'events.jsonl').read_text().splitlines()]
            clips=[e for e in events if e['kind']=='message_budget_enforced']
            self.assertEqual(len(clips),2)
            self.assertTrue(all(len(e['raw_message'].split())==70 for e in clips))

    def test_invalid_price_not_clipped(self):
        with self.assertRaises(ValueError):market_outcome({'a':11,'b':8},self.c)
        with self.assertRaises(ValueError):market_outcome({'a':True,'b':8},self.c)

if __name__=='__main__':unittest.main()
