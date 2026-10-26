"""Generate publication figures with ReportLab from derived recorded outcomes."""
from pathlib import Path
import csv,json,subprocess
from reportlab.graphics.shapes import Drawing,Line,Rect,String,PolyLine
from reportlab.graphics import renderPDF,renderSVG
from reportlab.lib.colors import HexColor
def C(v):return HexColor(v) if isinstance(v,str) else v
ROOT=Path(__file__).resolve().parents[1];REPO=ROOT.parents[1];OUT=ROOT/'figures';TEMP=REPO/'work/final_report/figure_pdf';TEMP.mkdir(exist_ok=True)
M=json.loads((ROOT/'data/report_metrics.json').read_text());BLUE='#21618c';ORANGE='#b04b23';GRAY='#566573'
def text(d,x,y,s,size=10,color='#18232b',anchor='start',bold=False):d.add(String(x,y,s,fontName='Helvetica-Bold'if bold else'Helvetica',fontSize=size,fillColor=C(color),textAnchor=anchor))
def line(d,x1,y1,x2,y2,color=GRAY,width=1,dash=None):d.add(Line(x1,y1,x2,y2,strokeColor=C(color),strokeWidth=width,strokeDashArray=dash))
def save(d,name):
 renderSVG.drawToFile(d,str(OUT/(name+'.svg')));p=TEMP/(name+'.pdf');renderPDF.drawToFile(d,str(p));subprocess.run(['pdftoppm','-singlefile','-r','180','-png',str(p),str(OUT/name)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
# Figure 1 Timeline and channel boundaries.
d=Drawing(650,185)
text(d,5,165,'A  Genuine insider reaction studies',12,bold=True)
labels=[('1–5','Shared formation'),('6–7','C role and preparation'),('8','Offer and actions'),('9','First public reply'),('9–13','Offered action window'),('14–15','Post-window')]
for i,(a,b)in enumerate(labels):
 x=5+i*108;d.add(Rect(x,96,103,48,fillColor=C('#eef4f8'),strokeColor=C('#ccd8df')));text(d,x+51.5,126,a,11,anchor='middle',bold=True);text(d,x+51.5,109,b,7.5,anchor='middle')
text(d,222,75,'Separate explicit and neutral diagnoses use frozen end-8 history only',10,BLUE)
text(d,5,48,'B  Forged-message studies',12,bold=True)
text(d,5,27,'Rounds 1–4: recorded two-firm cartel',10);text(d,235,27,'Round 5: inserted claim before actions',10);text(d,474,27,'Rounds 6–8: recovery or persistence',10)
line(d,5,13,640,13,BLUE,2);save(d,'figure1_design')
# Figure 2 Initial change and trajectories. Counts no independence CIs.
d=Drawing(650,280);text(d,0,263,'A  First action toward competitive benchmark',11,bold=True);text(d,352,263,'B  Paired raw price-index difference',11,bold=True)
models=['gpt-4.1','gpt-4.1-mini','gemini-2.5-flash','gemini-2.5-flash-lite','claude-haiku-4.5','claude-haiku-5.5'];labels=['GPT-4.1','GPT-4.1 mini','Gemini Flash','Gemini Flash Lite','Haiku 4.5','Haiku 5.5']
for i,(m,l)in enumerate(zip(models,labels)):
 y=225-i*32;z=M['V15'][m];a=z['fmsg'];b=z['placebo'];text(d,0,y+2,l,9)
 for count,total,yy,c in [(a['toward_benchmark'],a['n'],y,BLUE),(b['toward_benchmark'],b['n'],y-9,ORANGE)]:
  d.add(Rect(105,yy,160*count/total,7,fillColor=C(c),strokeColor=None));text(d,270,yy,count.__str__()+'/'+str(total),8)
text(d,105,15,'Forged partner message',9,BLUE);text(d,105,3,'Placebo',9,ORANGE)
# Three source models pooled with equal model weighting for plot; matched pairs retained in JSON.
x0,y0,w,h=384,53,245,180;lo,hi=-1.15,.05
for yv in [0,-.5,-1]:
 yy=y0+(yv-lo)/(hi-lo)*h;line(d,x0,yy,x0+w,yy,'#d6dbdf',.6);text(d,x0-5,yy-3,str(yv),8,anchor='end')
for r in range(4,9):xx=x0+(r-4)/4*w;text(d,xx,y0-14,str(r),9,anchor='middle')
for arm,color,label in [('fmsg',BLUE,'Forged message'),('act3',ORANGE,'Three-round real cut')]:
 vs=[sum(M['V17_matched_trajectories'][m+'|'+arm]['raw_index_difference_by_round'][i]for m in ['gpt-4.1-mini','gemini-2.5-flash','gemini-2.5-flash-lite'])/3 for i in range(3,8)]
 pts=[(x0+i*w/4,y0+(v-lo)/(hi-lo)*h)for i,v in enumerate(vs)];d.add(PolyLine(pts,strokeColor=C(color),strokeWidth=2));text(d,x0,y0-38-(12 if arm=='act3'else 0),label,9,color)
text(d,507,244,'Lower means below matched placebo',8,anchor='middle');text(d,507,20,'Round',9,anchor='middle');save(d,'figure2_forgery')
# Figure 3 Sumin two histories, each retained.
rows=list(csv.DictReader((REPO/'studies/exp 5 (env1_disruption)/reports/round_outcomes.csv').open()));cohorts=list(dict.fromkeys(x['cohort']for x in rows));d=Drawing(650,230)
for panel,co in enumerate(cohorts):
 x0=44+panel*325;y0=45;w=265;h=140;scx=lambda r:x0+(r-8)/7*w;scy=lambda v:y0+v/60*h
 text(d,x0,211,('A  'if panel==0 else'B  ')+('History 6101'if panel==0 else'History 6102'),12,bold=True)
 d.add(Rect(scx(9),y0,scx(13)-scx(9),h,fillColor=C('#f3f4f5'),strokeColor=None))
 for y in [4,20,36,52]:line(d,x0,scy(y),x0+w,scy(y),'#d6dbdf',.7);text(d,x0-6,scy(y)-3,str(y),8,anchor='end')
 for r in range(8,16):text(d,scx(r),y0-13,str(r),9,anchor='middle')
 for arm,color,dash in [('talk_only',BLUE,None),('act_only',ORANGE,None)]:
  xs=sorted([x for x in rows if x['cohort']==co and x['arm']==arm],key=lambda z:int(z['round']));d.add(PolyLine([(scx(int(z['round'])),scy(float(z['price'])))for z in xs],strokeColor=C(color),strokeWidth=2,strokeDashArray=dash))
 line(d,x0,scy(4),x0+w,scy(4),'#333333',.8,[3,3]);text(d,x0+w/2,y0-28,'Round',9,anchor='middle')
text(d,45,3,'Talk-only unequal offer with C=16',10,BLUE);text(d,300,3,'Action-only C=32 in rounds 9–13',10,ORANGE);save(d,'figure3_quantity')
print('Three figures generated from actual recorded data')
