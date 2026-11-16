import subprocess,re,copy
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
D='/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/paper/'
import os; os.chdir(D)
s=open('Paper_v0_9_short.md').read()
# ---------- PDF
p=re.sub(r'(?m)^!\[Figure [0-9]+\. ','![',s)
a=p.index('**Table 1.**'); b=p.index('## 6.1 Classical algorithms')
k=p.index('**Key.**'); p=p[:k]+'```{=latex}\n\\begingroup\\fontsize{9.5}{11.5}\\selectfont\n```\n\n'+p[k:b]+'```{=latex}\n\\endgroup\n```\n\n'+p[b:]; b=p.index('## 6.1 Classical algorithms')
p=p[:a]+'```{=latex}\n\\newgeometry{top=1.0cm,bottom=1.0cm,left=1.2cm,right=1.2cm}\\begin{landscape}\\fontspec{TeX Gyre Termes}\\fontsize{10.3}{12.4}\\selectfont\\setlength{\\tabcolsep}{3.4pt}\\renewcommand{\\arraystretch}{1.75}\n```\n\n'+p[a:b]+'\n```{=latex}\n\\end{landscape}\\restoregeometry\n```\n\n'+p[b:]
open('_pdf_short.md','w').write(p)
subprocess.run(['pandoc','_pdf_short.md','-o','Paper_v0_9_short.pdf','--pdf-engine=xelatex','-H','_hdr.tex','-V','geometry:margin=2.2cm','-V','fontsize=10pt','-V','mainfont=DejaVu Serif','-V','colorlinks=true','--resource-path=.'],check=True)
# ---------- DOCX
subprocess.run(['pandoc','Paper_v0_9_short.md','-o','Paper_v0_9_short.docx','--resource-path=.'],check=True)
d=Document('Paper_v0_9_short.docx')
tbl=next(t for t in d.tables if t.rows[0].cells[0].text.strip().startswith('row'))
cap=next(q for q in d.paragraphs if q.text.startswith('Table 1. Mean difference'))
for row in tbl.rows:
    for c in row.cells:
        for q in c.paragraphs:
            q.paragraph_format.space_before=Pt(2);q.paragraph_format.space_after=Pt(2)
            for r in q.runs: r.font.size=Pt(10); r.font.name='Times New Roman'
m=OxmlElement('w:tblCellMar')
for side in ('left','right'):
    e=OxmlElement(f'w:{side}');e.set(qn('w:w'),'25');e.set(qn('w:type'),'dxa');m.append(e)
tbl._tbl.tblPr.append(m)
for r in cap.runs: r.font.size=Pt(10.5); r.font.name='Times New Roman'
base=d.element.body.sectPr
def mk(land):
    sp=copy.deepcopy(base)
    for tag in ('w:pgSz','w:pgMar'):
        for o in sp.findall(qn(tag)): sp.remove(o)
    pg=OxmlElement('w:pgSz')
    if land: pg.set(qn('w:w'),'15840');pg.set(qn('w:h'),'12240');pg.set(qn('w:orient'),'landscape')
    else: pg.set(qn('w:w'),'12240');pg.set(qn('w:h'),'15840')
    mg=OxmlElement('w:pgMar')
    for k,v in (('top',700 if land else 1440),('right',680 if land else 1440),('bottom',700 if land else 1440),('left',680 if land else 1440),('header',720),('footer',720),('gutter',0)): mg.set(qn('w:'+k),str(v))
    sp.insert(0,pg);sp.insert(1,mg);return sp
def sect_after(prev,land):
    q=OxmlElement('w:p');pPr=OxmlElement('w:pPr');pPr.append(mk(land));q.append(pPr);prev.addnext(q)
sect_after(cap._p.getprevious(),False)
key=next(q for q in d.paragraphs if q.text.startswith('Key.'))
for r in key.runs: r.font.size=Pt(9.5); r.font.name='Times New Roman'
key.paragraph_format.space_before=Pt(6)
sect_after(key._p,True)
for o in base.findall(qn('w:pgSz')): base.remove(o)
pg=OxmlElement('w:pgSz');pg.set(qn('w:w'),'12240');pg.set(qn('w:h'),'15840');base.insert(0,pg)
d.save('Paper_v0_9_short.docx')
print('done')
