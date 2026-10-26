"""Read E2-R progress or completed evidence; no model calls or writes."""
import argparse,csv,gzip,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from price_study.protocol import ROOT,config
from price_study.engine import manifest
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',default='results/final_16');p.add_argument('--verify',action='store_true');a=p.parse_args()
out=Path(a.output);out=out if out.is_absolute()else ROOT/out
if not out.exists():raise SystemExit('No saved output at '+str(out))
for name in ['live_status.json','status.json']:
 f=out/name
 if f.exists():print(name,json.dumps(json.loads(f.read_text()),indent=2))
if(out/'RESULTS_TABLE.md').exists():print((out/'RESULTS_TABLE.md').read_text())
if a.verify:
 assert json.loads((out/'manifest.json').read_text())==manifest(config()),'Frozen source/config differs'
 status=json.loads((out/'status.json').read_text())
 assert status['state'] in ['complete','complete_with_failures'],'Execution is not terminal'
 branches={f.stem:json.loads(f.read_text())for f in(out/'branches').glob('*.json')if not f.name.endswith('.failure.json')}
 failed=set(status.get('failures',[]))
 assert len(branches)==16,'Expected all sixteen original slots, including explicit failures'
 completed={k for k,b in branches.items()if len(b['rounds'])==15}
 assert completed.isdisjoint(failed)and completed|failed==set(branches),'Completion and failure records disagree'
 for key,b in branches.items():
  assert [r['round']for r in b['rounds']]==list(range(1,len(b['rounds'])+1)),'Noncontiguous trajectory'
  if key in failed:assert (out/'branches'/f'{key}.failure.json').exists(),'Missing explicit failure record'
 public=list(csv.DictReader((out/'public_annotations.csv').open()));private=list(csv.DictReader((out/'private_assessments.csv').open()))
 delivered={k for k,b in branches.items()if len(b['rounds'])>=9}
 assert len(public)==6*len(delivered)and len(private)==6*len(delivered),'Pair denominator differs from delivered branches'
 assert all(x['reviewer']=='assistant_reviewed'for x in public)
 assert all(x['evidence_quote']and any(x['evidence_quote']in x[k]for k in ['reply_text','offer_text'])for x in public),'Nonexact evidence quotation'
 print(f'Verified frozen source, {len(completed)} complete original branches, {len(failed)} explicit failures, and {len(public)} public/private pairs each')
