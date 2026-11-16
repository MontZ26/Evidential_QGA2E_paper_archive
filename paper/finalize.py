import re,subprocess
exec(open('ay_transform.py').read().split("if __name__")[0])
AI="The author used Claude (Anthropic) to assist with drafting and editing the manuscript text, preparing tables and figures from the analysis files, and checking cross-references and citations. The experimental design, the experiments, the interpretation of the results and the final content were produced and verified by the author, who takes full responsibility for the manuscript."
ext=open('Paper_v0_9_num.md').read()
avail=re.search(r'\*\*Availability\.\*\* ([^\n]+)',ext).group(1)
def statements():
    return ("# Statements and Declarations\n\n"
    "**Funding.** The author received no funding for this work.\n\n"
    "**Competing interests.** The author has no competing interests to declare.\n\n"
    "**Author contributions.** Single author: Montassar Zaghdoud (conceptualisation, methodology, experiments, analysis, writing, review and editing).\n\n"
    "**Data availability.** "+avail+"\n\n"
    "**Ethics.** Not applicable: no human participants or animals were involved, and all patient information is simulated.\n\n"
    "**Use of AI tools.** "+AI+"\n\n")
for src,dst,short_ in [('Paper_v0_9_num.md','Paper_v0_9.md',False),('Paper_v0_9_short_num.md','Paper_v0_9_short.md',True)]:
    s=open(src).read()
    s=re.sub(r'\*\*Use of AI tools\.\*\*[^\n]*\n\n','',s)
    s=re.sub(r'\*\*Availability\.\*\*[^\n]*\n\n?','',s)
    s=re.sub(r'(?m)^\*\*Keywords:\*\*[^\n]*$','**Keywords:** home health care; multiobjective optimisation; quantum-inspired genetic algorithm; Dempster–Shafer theory; estimation of distribution algorithms; hypervolume.',s,1)
    if short_: s=s.replace('Supplementary Material','Online Resource 1').replace('Supplementary material','Online Resource 1').replace('is in the Online Resource 1','is provided in Online Resource 1').replace('the Online Resource 1','Online Resource 1')
    head,reflist,tail=transform(s)
    open(dst,'w').write(head.rstrip()+'\n\n'+tail.rstrip()+'\n\n'+reflist.rstrip()+'\n\n'+statements())
