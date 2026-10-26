"""Read pinned Git objects and published local evidence; never import a model client."""
from pathlib import Path
import subprocess,tarfile,io,json,math,csv,hashlib,collections
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[1]
REF='e3c0b8790cd2fb802251187faa72a71a6f98c767'
paths=['behavioral_v15_main','behavioral_v16_main','behavioral_v17_main','behavioral_v18_claude_code','behavioral_analysis']
buf=subprocess.check_output(['git','archive',REF+':apart_sprint_ring_study',*paths],cwd=REPO)
files={}
with tarfile.open(fileobj=io.BytesIO(buf))as t:
 for m in t:
  if m.isfile()and m.name.endswith('.json'):
   try:files[m.name]=json.load(t.extractfile(m))
   except(ValueError,UnicodeDecodeError):pass
# Direct implementation of the frozen equations; no source imports or network calls.
def pf(g,a,b):
 if g=='P':
  low=min(a,b);return(a-2)*(120-8*low)*(0.5 if a==b else 1 if a<b else 0)
 if g=='Q':return(max(0,100-a-b)-4)*a
 z=[math.exp((2-p)/.25)for p in(a,b)];return(a-1)*z[0]/(sum(z)+1)
def price(g,a,b):return min(a,b)if g=='P'else max(0,100-a-b)if g=='Q'else(a+b)/2
G={}
for g,grid in [('P',list(range(2,11))),('Q',list(range(0,41,4))),('L',[round(1.4+.05*k,2)for k in range(13)])]:
 eq=[(a,b)for a in grid for b in grid if all(pf(g,x,b)<=pf(g,a,b)+1e-9 for x in grid)and all(pf(g,x,a)<=pf(g,b,a)+1e-9 for x in grid)]
 n=(3,3)if g=='P'else min(eq,key=lambda ab:(abs(ab[0]-ab[1]),price(g,*ab)))
 j=max(((a,a)for a in grid),key=lambda ab:pf(g,*ab)+pf(g,*reversed(ab)))
 G[g]={'grid':grid,'nash':n,'joint':j,'nash_price':price(g,*n),'joint_price':price(g,*j)}
rows=[];summary={};validation=collections.Counter()
for path,e in files.items():
 if '/episodes/'not in path or not e.get('complete'):continue
 root=path.split('/')[0]
 if root not in paths[:3]:continue
 cfg=e['config'];g=cfg['game'];arm=cfg['arm'];h=e['state']['history'];model=path.split('/')[1].split('__',1)[1]
 if len(h)<8:continue
 for z in h:
  a,b=z['choices']['firm_1'],z['choices']['firm_2'];assert abs(z['market_price']-price(g,a,b))<1e-7
  # net may include regime penalties; these forged/action arms have no fine.
  for k,aa,bb in [('firm_1',a,b),('firm_2',b,a)]:assert abs(z['net_profits'][k]-pf(g,aa,bb))<1e-6
  validation['rounds_recalculated']+=1
 own4=h[3]['choices']['firm_1'];own5=h[4]['choices']['firm_1'];n=G[g]['nash'][0]
 idx=lambda z:(z['market_price']-G[g]['nash_price'])/(G[g]['joint_price']-G[g]['nash_price'])
 row={'source_group':root,'model':model,'game':g,'arm':arm,'seed':cfg['seed'],'initial_change':own5!=own4,'initial_toward_benchmark':(own5-own4)*(n-own4)>0,'prefix_sha256':hashlib.sha256(json.dumps(h[:4],sort_keys=True).encode()).hexdigest(),'history':[{'round':z.get('round',i+1),'index_raw':idx(z),'index_source_clipped':max(-1,min(2,idx(z))),'price':z['market_price'],'choices':z['choices']}for i,z in enumerate(h)],'git_path':'apart_sprint_ring_study/'+path}
 rows.append(row)
 if root=='behavioral_v15_main':
  d=summary.setdefault(model,{}).setdefault(arm,{'n':0,'changes':0,'toward_benchmark':0});d['n']+=1;d['changes']+=row['initial_change'];d['toward_benchmark']+=row['initial_toward_benchmark']
# Paired raw trajectories for cheap-model V17 arms. No independent-cell inference.
traj={};cheap=['gpt-4.1-mini','gemini-2.5-flash','gemini-2.5-flash-lite']
for model in cheap:
 subset=[x for x in rows if x['model']==model];lookup={(x['game'],x['seed'],x['arm']):x for x in subset}
 for arm in ['fmsg','act','act3']:
  pairs=[(x,lookup[(x['game'],x['seed'],'placebo')])for x in subset if x['arm']==arm and(x['game'],x['seed'],'placebo')in lookup]
  if pairs:traj[model+'|'+arm]={'pairs':len(pairs),'identical_prefix_pairs':sum(a['prefix_sha256']==b['prefix_sha256']for a,b in pairs),'raw_index_difference_by_round':[sum(a['history'][i]['index_raw']-b['history'][i]['index_raw']for a,b in pairs)/len(pairs)for i in range(8)],'source_clipped_difference_by_round':[sum(a['history'][i]['index_source_clipped']-b['history'][i]['index_source_clipped']for a,b in pairs)/len(pairs)for i in range(8)]}
meta=files['behavioral_v18_claude_code/meta.json'];v18={}
for path,rs in files.items():
 if path.startswith('behavioral_v18_claude_code/out/')and isinstance(rs,list):
  model,arm=Path(path).stem.split('_',1);half=anyc=direction=0
  for x in rs:
   k=meta[f'{arm}|{x["id"]}'];c=x['choice'];own=k['own4'];n=k['nash'];half+=c!=own and abs(c-n)<=abs(own-n)/2;anyc+=c!=own;direction+=(c-own)*(n-own)>0
  v18.setdefault(model,{})[arm]={'n':len(rs),'halfway':half,'any_change':anyc,'toward_benchmark':direction}
assert sum(x['fmsg']['changes']for x in summary.values())==40
assert sum(x['fmsg']['n']for x in summary.values())==53
assert sum(x['placebo']['changes']for x in summary.values())==1
assert all(x['fmsg']['changes']==x['fmsg']['toward_benchmark']for x in summary.values())
result={'branch_sha':REF,'main_input_sha':'a853c35cf6eaef5dcc020fc354f0aae0b7f9440c','new_model_calls':0,'games':G,'V15':summary,'V17_matched_trajectories':traj,'V18_subagent':v18,'validation':dict(validation),'complete_episode_records':len(rows),'notes':['Pure arithmetic validation is not semantic transcript review or authentication of provider identities.','Branch frozen_sources retain source model strings; agent labels are execution configuration labels, not verified capability rankings.','Raw and source-clipped normalized indices retained separately; plotted index differences use raw values.']}
(ROOT/'data/report_metrics.json').write_text(json.dumps(result,indent=2)+'\n');(ROOT/'data/contributor_episode_derivatives.json').write_text(json.dumps(rows,indent=2)+'\n')
with(ROOT/'data/first_response.csv').open('w',newline='')as f:
 w=csv.DictWriter(f,fieldnames=['model','arm','n','changes','toward_benchmark'],lineterminator='\n');w.writeheader()
 for model,d in summary.items():
  for arm,x in d.items():w.writerow(dict(model=model,arm=arm,**x))
print(json.dumps({'episodes':len(rows),'recalculated_rounds':validation['rounds_recalculated'],'games':G,'V17_pairs':{k:v['pairs']for k,v in traj.items()}},indent=2))
