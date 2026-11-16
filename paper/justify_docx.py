import sys
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH as A
for f in sys.argv[1:]:
    d=Document(f); n=0; sty={}
    for p in d.paragraphs:
        st=p.style.name; sty[st]=sty.get(st,0)+1
        if st in ('Body Text','First Paragraph','Compact','Block Text','Bibliography') and p.text.strip():
            p.alignment=A.JUSTIFY; n+=1
    d.save(f); print(f,n,sty)
