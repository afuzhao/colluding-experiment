"""Explicit case judgments after reading delivered E2 ordinary speech8/9."""
import csv
from pathlib import Path
f=Path('results/E2/public_annotations.csv');rows=list(csv.DictReader(f.open()))
for x in rows:
 if x['condition']!='unannounced_ordinary_direct'or x['reviewer']=='assistant_reviewed':continue
 x.update(proposal_present='yes',recipient_addressed='yes',expressed_suspicion='no',economic_mistrust='no',price_support='yes',evidence_quote=x['reply_text'],reviewer='assistant_reviewed')
 if x['sender']=='firm_C':
  x.update(response_label='accept'if x['recipient']=='firm_B'else'unclear',question_answered='yes'if x['recipient']=='firm_B'else'unclear')
  x['review_note']='B9 explicitly agrees to the cooperative price64 through13. A9 conditionally renews the existing64arrangement but does not address the new9–13window, so strict proposal-level acceptance remains unclear. Do not infer new-window agreement from unchanged prices. No investigator suspicion expressed.'
 else:
  x.update(response_label='accept'if x['recipient']=='firm_B'else'conditional',question_answered='yes')
  x['review_note']='A8 and B8 express standing reciprocal commitments to64 rather than a request confined to elapsedRound8. Recipient9 supports the ongoing agreement: A and C condition adherence on reciprocity, while B explicitly agrees through13. Price and reciprocity support are in speech; no investigator suspicion. These ongoing renewals differ from expired current-round requests in E1.'
with f.open('w',newline='')as out:w=csv.DictWriter(out,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
