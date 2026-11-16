import re,sys,unicodedata
def parse_refs(block):
    refs={}
    for m in re.finditer(r'(?m)^(\d+)\. (.+)$',block):
        n=int(m.group(1)); t=m.group(2).strip()
        mm=re.search(r'(?<=[A-Z]\.) ',t); seg=t[:mm.start()]
        auth=[a.strip() for a in seg.split(', ')]
        sur=[a.rsplit(' ',1)[0] for a in auth]
        pre=re.split(r'DOI|https://',t)[0]
        ys=re.findall(r'\((\d{4})\)',pre) or re.findall(r'(?:, |\b[A-Z][a-z]+ )((?:19|20)\d{2})\b',pre)
        year=ys[-1] if ys else 'n.d.'
        refs[n]=dict(text=t,sur=sur,year=year)
    return refs
def short(r):
    s=r['sur']
    return s[0] if len(s)==1 else (f"{s[0]} and {s[1]}" if len(s)==2 else f"{s[0]} et al.")
def doi_links(t):
    t=re.sub(r'DOI (10\.\S+?)(?=[;. ]*$|; |\.? arXiv)',lambda m:'https://doi.org/'+m.group(1).rstrip('.'),t)
    return t
def sortkey(r):
    k=unicodedata.normalize('NFKD',' '.join(r['sur'])).encode('ascii','ignore').decode().lower()
    return (k,r['year'])
def expand(lst):
    out=[]
    for part in re.split(r'\s*,\s*',lst):
        if re.search(r'[–-]',part):
            a,b=re.split(r'\s*[–-]\s*',part); out+=list(range(int(a),int(b)+1))
        else: out.append(int(part))
    return out
def transform(s):
    head,rest=s.split('# References',1)
    m=re.search(r'(?m)^# (Appendix|Statements)',rest)
    refblock=rest[:m.start()] if m else rest; tail=rest[m.start():] if m else ''
    refs=parse_refs(refblock)
    for n,r in refs.items(): assert r['year'],n
    cite=lambda n:f"{short(refs[n])} {refs[n]['year']}"
    def rep(mo):
        lst=mo.group(1); ns=expand(lst)
        if not all(1<=n<=41 for n in ns): return mo.group(0)
        return '('+'; '.join(sorted({cite(n) for n in ns},key=lambda x:x))+')'
    # narrative: "Name [n]" and "Name and Name [n]"
    def narr(mo):
        n=int(mo.group(2)); r=refs[n]
        if mo.group(1).strip().startswith(r['sur'][0]) or r['sur'][0] in mo.group(1):
            return f"{mo.group(1)} ({r['year']})"
        return mo.group(0)
    def conv(head):
      head=re.sub(r"((?:[A-Z][\w’'À-ÿœ\-]+)(?: (?:and|et al\.|&) ?[A-Z]?[\w’'À-ÿœ\-]*)?(?:'s variant|’s variant)?) \[(\d+)\]",narr,head)
      head=re.sub(r'\[(\d+(?:\s*[–,-]\s*\d+)*)\]',rep,head)
      return head.replace(' (Li and Rudolph, technical report)','')
    head=conv(head); tail=conv(tail)
    ordered=sorted(refs.values(),key=sortkey)
    lines=[doi_links(r['text']) for r in ordered]
    reflist='# References\n\n'+'\n\n'.join(lines)+'\n\n'
    return head,reflist,tail
if __name__=='__main__':
    for f in sys.argv[1:]:
        s=open(f).read(); h,r,t=transform(s)
        open(f.replace('_num','')+'.tmp','w').write(h+r+t)
