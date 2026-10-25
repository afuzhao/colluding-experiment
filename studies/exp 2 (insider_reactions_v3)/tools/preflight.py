"""C-only offer verification on a disclosed development fixture, never a new formation."""
import argparse,copy,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from trusted_study.protocol import ROOT,config,conditions
from trusted_study.engine import checked_call
from trusted_study.client import LocalClient
from trusted_study.utils import write_json,digest
p=argparse.ArgumentParser();p.add_argument('--only',nargs='*');p.add_argument('--fixture',required=True);p.add_argument('--output',default='results/preflight');a=p.parse_args()
c=config();c['protocol']['seed']=7201
base=json.loads(Path(a.fixture).read_text());state={'rounds':base['rounds'][:7]};out=Path(a.output);client=LocalClient(c,out)
write_json(out/'provenance.json',{'description':'C-only development preflight; not fresh formation or resident results','fixture':Path(a.fixture).name,'fixture_hash':digest(state),'config':c})
rows=[]
for cond in conditions(c):
 if a.only and cond['approach']not in a.only:continue
 try:
  ans=checked_call(copy.deepcopy(state),c,client,'firm_C',8,'message',cond)
  row={'condition':cond,'passed_minimum_checks':True,'output':ans,'semantic_review':'pending'}
 except Exception as exc:row={'condition':cond,'passed_minimum_checks':False,'error':str(exc),'semantic_review':'pending'}
 rows.append(row);write_json(out/'checks.json',rows);print(json.dumps(row),flush=True)
print('PREFLIGHT DONE',sum(r['passed_minimum_checks']for r in rows),'/',len(rows),flush=True)
