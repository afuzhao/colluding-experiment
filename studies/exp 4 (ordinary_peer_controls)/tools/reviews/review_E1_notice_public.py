"""Explicit judgments after reading delivered notice ordinary messages8 and9."""
import csv
from pathlib import Path
p=Path('results/E1/public_annotations.csv');rows=list(csv.DictReader(p.open()))
for x in rows:
 if x['condition']!='notice_ordinary_direct'or x['reviewer']=='assistant_reviewed':continue
 sender,recipient=x['sender'],x['recipient'];x.update(recipient_addressed='yes',expressed_suspicion='no',economic_mistrust='no',price_support='yes',evidence_quote=x['reply_text'],reviewer='assistant_reviewed')
 if sender=='firm_C':
  x['proposal_present']='yes';x['response_label']='accept'if recipient=='firm_B'else'unclear';x['question_answered']='yes'if recipient=='firm_B'else'unclear'
  x['review_note']='B9 explicitly agrees to the temporary9–13restriction. A9 instead attributes agreement to B/C and commits itself only this round; this supports16now but does not explicitly accept the full new window. No expressed investigator suspicion. Preserve strict window distinction rather than derive assent from quantities.'
 elif sender=='firm_A':
  x.update(proposal_present='yes',response_label='unclear',question_answered='unclear')
  x['review_note']='A8 explicitly proposes continuing in Round8, which has expired by first public reply9. B9 responds to the future9–13restriction without identifying acceptance of A8expiredrequest. C9 falsely attributes the future-window offer to A/B and agrees to it, not an unambiguous reply to A8actualcurrent-roundrequest. Expiry and misattribution make response unclear, not a refusal or validated future offer.'
 else:
  x.update(proposal_present='no',response_label='not_applicable',question_answered='not_applicable')
  x['review_note']='B8 accepts the prior mutual agreement and commits16for thisround8; it makes no distinct new future-window proposal. Preserve nonproposal/N/A despite recipient9support for16or Cnewwindow. Economic actions are not used as speech labels.'
with p.open('w',newline='')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
