"""Collect actual control evidence into editable review sheets; no inference or automatic labels."""
import argparse,csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
IDS=['firm_A','firm_B','firm_C']
def read(p):return json.loads(p.read_text())
def write_review(path,rows,keys):
 prior={tuple(x[k]for k in keys):x for x in csv.DictReader(path.open())}if path.exists()else{}
 for row in rows:
  saved=prior.get(tuple(row[k]for k in keys))
  if saved:
   for k in row:
    if k in saved and k not in ['offer_text','reply_text','interpretation','response','concerns']:row[k]=saved[k]
 if not rows:return
 with path.open('w',newline='')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
def collect(env):
 p=ROOT/'results'/env;public=[];neutral=[]
 for file in sorted((p/'branches').glob('*.json')):
  b=read(file)
  if len(b['rounds'])<9:continue
  for sender in b['rounds'][7]['messages']:
   for recipient in IDS:
    if recipient==sender['agent']:continue
    reply=next(m for m in b['rounds'][8]['messages']if m['agent']==recipient)
    public.append({'environment':env,'condition':file.stem,'sender':sender['agent'],'recipient':recipient,'offer_text':sender['message'],'reply_text':reply['message'],'proposal_present':'','recipient_addressed':'','response_label':'','expressed_suspicion':'','economic_mistrust':'','question_answered':'','price_support':'','evidence_quote':'','reviewer':'','review_note':''})
 for file in sorted((p/'neutral_assessments').glob('*.json')):
  data=read(file)
  for row in data['accounts']:
   sender=row['proposal_id'].split('_candidate')[0][4:]
   neutral.append({'environment':env,'condition':data['condition'],'recipient':data['recipient'],'sender':sender,'ordinary_C':data['ordinary_C'],'proposal_id':row['proposal_id'],'interpretation':row['interpretation'],'response':row['response'],'concerns':row['concerns'],'proposal_present':'','response_label':'','expressed_suspicion':'','economic_mistrust':'','evidence_quote':'','reviewer':'','review_note':''})
 write_review(p/'public_annotations.csv',public,['condition','sender','recipient'])
 write_review(p/'neutral_annotations.csv',neutral,['condition','sender','recipient'])
 return public,neutral
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--environment',required=True,choices=['E1','E2']);x=a.parse_args();p,n=collect(x.environment);print(json.dumps({'environment':x.environment,'observed_public_pairs':len(p),'observed_neutral_pairs':len(n),'automatic_labels_assigned':0}))
