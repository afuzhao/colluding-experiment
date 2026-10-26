"""Recount the late contributor sweep without model calls or importing provider code."""
from pathlib import Path
import subprocess,json
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[1];REF='07a92fc01832d131cb7d77970ea3ff0e73a53b55';base='apart_sprint_ring_study/behavioral_v18_claude_code/'
def read(p):return json.loads(subprocess.check_output(['git','show',REF+':'+base+p],cwd=REPO))
meta=read('meta.json');out={'source_sha':REF,'new_model_calls':0,'metric':'competitive-direction change at claim equal to competitive benchmark','results':{}}
for model in ['fable','opus']:
 rows=read('out/'+model+'_swc_tagged.json');rs=[]
 for r in rows:
  k=meta['swc_tagged|'+r['id']]
  if k['x']==k['nash']:rs.append((r['choice']-k['own4'])*(k['nash']-k['own4'])>0)
 out['results'][model]={'moves':sum(rs),'n':len(rs)}
assert out['results']['fable']=={'moves':15,'n':17};assert out['results']['opus']=={'moves':1,'n':17}
(ROOT/'data/late_sweep_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
