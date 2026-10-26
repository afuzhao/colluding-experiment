"""Reuse environment-2 clearing without mutating that environment's source."""
import sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ENV_ROOT=ROOT.parents[1]/'environments/env 2 (differentiated_prices)'
sys.path.insert(0,str(ENV_ROOT))
from market_env import Market


def benchmarks(environment):return Market(environment).benchmarks()

def clear_market(prices,environment):return Market(environment).clear(prices)

def qualify(rounds,c):
 counts=Counter()
 for r in rounds[-5:]:
  values=[m['price_commitment']for m in r['messages']]
  if len(values)==3 and len(set(values))==1 and values[0]is not None:
   p=values[0]
   if p>34 and all(abs(v-p)<=c['protocol']['price_tolerance']for v in r['prices'].values()):counts[p]+=1
 if not counts:return {'qualified':False,'price':None,'eligible_rounds':0,'agreement_review':'pending'}
 p,n=counts.most_common(1)[0]
 return {'qualified':n>=4,'price':p,'eligible_rounds':n,'agreement_review':'pending'}
