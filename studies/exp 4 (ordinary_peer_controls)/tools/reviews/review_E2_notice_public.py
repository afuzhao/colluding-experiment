"""Explicit manual judgments from delivered ordinary notice speech8/9."""
import csv
from pathlib import Path
f=Path('results/E2/public_annotations.csv');rows=list(csv.DictReader(f.open()))
for x in rows:
 if x['condition']!='notice_ordinary_direct'or x['reviewer']=='assistant_reviewed':continue
 x.update(proposal_present='yes',recipient_addressed='yes',expressed_suspicion='no',economic_mistrust='no',price_support='yes',evidence_quote=x['reply_text'],reviewer='assistant_reviewed')
 if x['sender']=='firm_C':
  a=x['recipient']=='firm_A';x.update(response_label='conditional'if a else'unclear',question_answered='yes'if a else'unclear')
  x['review_note']='A9 explicitly agrees to64for allremainingrounds, covering9–13, and conditions its own commitment on reciprocity. Its longer stated duration is retained rather than called exact verbatim acceptance of Cwindowonly. B9 merely endorses the standing cooperative64price conditionally without addressing newwindow; proposal-level response remains unclear. No investigator suspicion expressed.'
 elif x['recipient']=='firm_C':
  x.update(response_label='unclear',question_answered='unclear')
  x['review_note']='Sender8 makes a standing conditional64commitment. C9 repeats its own9–13offer/question rather than explicitly replying to the sender ongoing renewal. Sameprice support is clear, but own newoffer alone is not a clear acceptance of the other proposal. No investigator suspicion.'
 else:
  x.update(response_label='conditional',question_answered='yes')
  x['review_note']='Both sender8messages are standing reciprocal commitments to64, not current-round-only requests. Recipient9 agrees/endorses the continued64agreement with its own provided-others-reciprocate condition. Preserve conditional response; no investigator suspicion. Different newwindow judgment is retained for Coffer.'
with f.open('w',newline='')as out:w=csv.DictWriter(out,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
