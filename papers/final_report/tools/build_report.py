"""Build Word/Markdown from a retained Apart template; preserve unrelated package parts."""
from pathlib import Path
import argparse,copy,hashlib,json,re,zipfile,io
from docx import Document
from docx.shared import Inches,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[1]
P=argparse.ArgumentParser();P.add_argument('--template',required=True);a=P.parse_args();template=Path(a.template)
assert hashlib.sha256(template.read_bytes()).hexdigest()=='5fc0d819e2f56294d2d966cabd4e4bea91de3353e2d139f4c87e25dff0a67766'
D=json.loads((ROOT/'report_content.json').read_text());doc=Document(template);body=doc.element.body;title_table=doc.tables[0]
# Collapse only the empty author-slot subtable, as the user requested no authors.
for t in list(title_table._element.iter(qn('w:tbl'))):
 txt=''.join(x.text or '' for x in t.iter(qn('w:t')))
 if t is not title_table._element and 'Author name' in txt and 'Abstract' not in txt and 'With' not in txt:t.getparent().remove(t)
# Patch only editable title/author/abstract slots in the retained source component.
for para in title_table._element.iter(qn('w:p')):
 ts=list(para.iter(qn('w:t')));txt=''.join(t.text or''for t in ts)
 if txt=='PROJECT TITLE':
  ts[0].text=D['title'];new=OxmlElement('w:p');pr=OxmlElement('w:pPr');jc=OxmlElement('w:jc');jc.set(qn('w:val'),'center');pr.append(jc);sp=OxmlElement('w:spacing');sp.set(qn('w:after'),'200');pr.append(sp);new.append(pr);rr=OxmlElement('w:r');rp=OxmlElement('w:rPr');font=OxmlElement('w:rFonts');font.set(qn('w:ascii'),'Old Standard TT');font.set(qn('w:hAnsi'),'Old Standard TT');rp.append(font);sz=OxmlElement('w:sz');sz.set(qn('w:val'),'28');rp.append(sz);rr.append(rp);t=OxmlElement('w:t');t.text=D['subtitle'];rr.append(t);new.append(rr);para.addnext(new)
 elif 'Author name'in txt or txt=='Affiliation':
  for t in ts:t.text=''
 elif txt.startswith('Summarize your project'):
  # Preserve paragraph role, replacing instruction runs with non-italic body text.
  for e in list(para):
   if e.tag!=qn('w:pPr'):para.remove(e)
  rr=OxmlElement('w:r');rp=OxmlElement('w:rPr');font=OxmlElement('w:rFonts');font.set(qn('w:ascii'),'Old Standard TT');font.set(qn('w:hAnsi'),'Old Standard TT');rp.append(font);sz=OxmlElement('w:sz');sz.set(qn('w:val'),'24');rp.append(sz);rr.append(rp);t=OxmlElement('w:t');t.text=D['abstract'];rr.append(t);para.append(rr)
# Keep the edited title table, section properties and source package furniture.
for e in list(body):
 if e is not title_table._element and e.tag!=qn('w:sectPr'):body.remove(e)

def runfont(r,size=12,bold=False,italic=False):
 r.font.name='Old Standard TT';r.font.size=Pt(size);r.font.bold=bold;r.font.italic=italic;r.font.color.rgb=RGBColor(0,0,0)
def paragraph(text,style='normal',size=12,bold=False,after=8,before=0,keep=False):
 p=doc.add_paragraph(style=style);p.paragraph_format.space_after=Pt(after);p.paragraph_format.space_before=Pt(before);p.paragraph_format.line_spacing=1;p.paragraph_format.keep_with_next=keep
 pos=0
 for match in re.finditer(r'https://[^\s]+',text):
  r=p.add_run(text[pos:match.start()]);runfont(r,size,bold)
  url=match.group().rstrip('.,;');link=OxmlElement('w:hyperlink');link.set(qn('r:id'),p.part.relate_to(url,RT.HYPERLINK,is_external=True));r=OxmlElement('w:r');rp=OxmlElement('w:rPr');f=OxmlElement('w:rFonts');f.set(qn('w:ascii'),'Old Standard TT');f.set(qn('w:hAnsi'),'Old Standard TT');rp.append(f);sz=OxmlElement('w:sz');sz.set(qn('w:val'),str(int(size*2)));rp.append(sz);u=OxmlElement('w:u');u.set(qn('w:val'),'single');rp.append(u);r.append(rp);t=OxmlElement('w:t');t.text='Repository source' if 'github.com' in url else 'arXiv source';r.append(t);link.append(r);p._p.append(link);pos=match.start()+len(url)
 r=p.add_run(text[pos:]);runfont(r,size,bold);return p
PAGE_PENDING=False
def heading(text,level=2):
 global PAGE_PENDING
 p=paragraph(text,'Heading '+str(level),16 if level==2 else 14,True,after=6,before=0 if level==2 else 8,keep=True)
 if PAGE_PENDING:p.paragraph_format.page_break_before=True;PAGE_PENDING=False
 return p
def newpage():
 global PAGE_PENDING
 PAGE_PENDING=True
def addtable(item):
 # Source-derived black rules and serif text, fixed width within source margins.
 t=doc.add_table(rows=1,cols=len(item['headers']));t.autofit=False
 for c,w in zip(t.columns,item['widths']):c.width=Inches(w)
 for i,h in enumerate(item['headers']):t.rows[0].cells[i].text=h
 for row in item['rows']:
  cs=t.add_row().cells
  for i,s in enumerate(row):cs[i].text=s
 for ir,row in enumerate(t.rows):
  trpr=row._tr.get_or_add_trPr();el=OxmlElement('w:cantSplit');trpr.append(el)
  if ir==0:el=OxmlElement('w:tblHeader');trpr.append(el)
  for ic,c in enumerate(row.cells):
   c.width=Inches(item['widths'][ic]);tcpr=c._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
   for edge in ['bottom']:
    z=OxmlElement('w:'+edge);z.set(qn('w:val'),'single');z.set(qn('w:sz'),'4');z.set(qn('w:color'),'808080');b.append(z)
   tcpr.append(b);mar=OxmlElement('w:tcMar')
   for edge in ['top','bottom','left','right']:
    z=OxmlElement('w:'+edge);z.set(qn('w:w'),'60');z.set(qn('w:type'),'dxa');mar.append(z)
   tcpr.append(mar)
   for p in c.paragraphs:
    p.paragraph_format.space_after=Pt(3);p.paragraph_format.line_spacing=1
    for r in p.runs:runfont(r,10,ir==0)
 paragraph(item['caption'],size=10.5,after=7)
def items(xs):
 for it in xs:
  if it['type']=='p':paragraph(it['text'])
  elif it['type']=='h2':heading(it['text'])
  elif it['type']=='h3':heading(it['text'],3)
  elif it['type']=='table':addtable(it)
  elif it['type']=='figure':
   p=doc.add_paragraph(style='normal');p.paragraph_format.space_after=Pt(3);p.paragraph_format.keep_with_next=True;p.add_run().add_picture(str(ROOT/'figures'/(it['name']+'.png')),width=Inches(6.5));paragraph(it['caption'],size=10.5,after=7)
for page in D['main_pages']:
 newpage();heading(page['title']);items(page['items'])
newpage();heading('References')
for ref in D['references']:paragraph(ref,size=11,after=12)
for page in D['appendices']:
 newpage();heading(page['title']);items(page['items'])
# New source-derived body controls only; retain original style and other package bytes.
buf=io.BytesIO();doc.save(buf);newzip=zipfile.ZipFile(io.BytesIO(buf.getvalue()));base=zipfile.ZipFile(template)
editable={'word/document.xml','word/_rels/document.xml.rels','[Content_Types].xml'}
out=ROOT/'what_breaks_an_ai_cartel.docx'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED)as z:
 for name in base.namelist():z.writestr(name,newzip.read(name)if name in editable else base.read(name))
 for name in newzip.namelist():
  if name not in base.namelist():z.writestr(name,newzip.read(name))
f=zipfile.ZipFile(out);preserved=[n for n in base.namelist()if n not in editable];assert all(base.read(n)==f.read(n)for n in preserved)
verify={'template_sha256':hashlib.sha256(template.read_bytes()).hexdigest(),'preserve_only_parts_unchanged':len(preserved),'changed_existing_parts':sorted(n for n in base.namelist()if base.read(n)!=f.read(n)),'added_parts':sorted(n for n in f.namelist()if n not in base.namelist()),'section_properties_unchanged':Document(template).sections[0]._sectPr.xml==Document(out).sections[0]._sectPr.xml,'abstract_words':len(D['abstract'].split()),'authors_intentionally_blank':True,'author_contributions_omitted':True}
assert verify['section_properties_unchanged'];(ROOT/'TEMPLATE_FIDELITY.json').write_text(json.dumps(verify,indent=2)+'\n')
# Markdown mirrors the same document content and source figures.
md=['# '+D['title'],'\n'+D['subtitle'],'\n## Abstract','\n'+D['abstract']]
def mditems(xs):
 out=[]
 for it in xs:
  typ=it['type']
  if typ=='p':out.append(it['text'])
  elif typ in ['h2','h3']:out.append(('## 'if typ=='h2'else'### ')+it['text'])
  elif typ=='figure':out+=['!['+it['caption'].split('.')[0]+'](figures/'+it['name']+'.png)',it['caption']]
  elif typ=='table':out+=['| '+' | '.join(it['headers'])+' |','|'+'|'.join('---'for _ in it['headers'])+'|',*['| '+' | '.join(r)+' |'for r in it['rows']],it['caption']]
 return '\n\n'.join(out)
for page in D['main_pages']:md+=['\n## '+page['title'],mditems(page['items'])]
md+=['\n## References',*D['references']]
for page in D['appendices']:md+=['\n## '+page['title'],mditems(page['items'])]
(ROOT/'REPORT.md').write_text('\n\n'.join(md)+'\n');print(json.dumps(verify,indent=2))
