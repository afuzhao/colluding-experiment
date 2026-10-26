"""Offline exact-request replay equivalence, with HTTP forbidden."""
import copy,json,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from price_study import engine
from price_study.protocol import config,ROOT
from price_study.client import LocalClient
from cache_schedule import play_round_c_first
p=ROOT/'results/final_16';c=config();cache={x['request_hash']:x for x in map(json.loads,(p/'calls.jsonl').read_text().splitlines())};identity=json.loads((p/'model_identity.json').read_text());checked=0;requests=0
assert json.loads((p/'manifest.json').read_text())==engine.manifest(c),'Base source drift'
for f in sorted((p/'branches').glob('*.json')):
 if f.name.endswith('.failure.json'):continue
 branch=json.loads(f.read_text())
 for n in range(8,len(branch['rounds'])+1):
  prefix=copy.deepcopy(branch);prefix['rounds']=prefix['rounds'][:n-1]
  outputs=[];positions=[]
  for fn in [engine.play_round,play_round_c_first]:
   with tempfile.TemporaryDirectory()as temp:
    client=LocalClient.__new__(LocalClient);client.c=c;client.output=Path(temp);client.cache=cache;client.identity=identity;client.calls=0;client.replayed=0
    def forbidden(*a,**kw):raise AssertionError('A request was not found exactly in the actual journal; network prohibited')
    client.http=forbidden
    state=copy.deepcopy(prefix);outputs.append(fn(state,c,client,branch['condition']))
    pos=[json.loads(x)for x in(client.output/'request_positions.jsonl').read_text().splitlines()]
    positions.append(pos)
  assert outputs[0]==outputs[1],(f.name,n,'round differs')
  normalize=lambda rows:sorted((json.dumps(x['tag'],sort_keys=True),x['request_hash'])for x in rows)
  assert normalize(positions[0])==normalize(positions[1]),(f.name,n,'encoded request differs')
  assert [m['agent']for m in outputs[1]['messages']]==['firm_A','firm_B','firm_C']
  checked+=1;requests+=len(positions[0])
result={'offline_rounds_checked':checked,'per_schedule_request_positions':requests,'requests_identical_by_agent_seed_schema_and_encoded_messages':True,'round_outputs_identical_under_exact_replay':True,'new_model_calls':0,'scope':'Existing saved successful rounds; does not prove bitwise generation determinism or speed. Optimization not installed in live worker.'}
(ROOT/'reports/CACHE_SCHEDULE_EQUIVALENCE.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
