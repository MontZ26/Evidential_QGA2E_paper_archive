import json
S='/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/'
D=0.005
def cls(lo,hi):
    if lo>0:return '+'
    if hi<0:return '-'
    if lo>-D and hi<D:return '='
    return '?'
M=['NSGA2','MOEAD','GDp','GE','GDg6','GEg6','Dp','Dg','DA','E','Eg1.1','Eg0.8','Eg2','Eg6']
ent={}  # (a,b)->(mean,lo,hi,level,study)
def add(a,b,mean,ci,lvl,st): ent[(a,b)]=(mean,ci[0],ci[1],lvl,st)
A=json.load(open(S+'p21/p21_final_analysis_A.json'));B=json.load(open(S+'p21/p21_final_analysis_B.json'))
P22=json.load(open(S+'p22/p22_final_analysis.json'));P17=json.load(open(S+'p17/p17_final_analysis.json'))
pa=A['primary']; sa=A['secondary']
for k,(a,b) in {'A1 NSGA2-MOEAD':('NSGA2','MOEAD'),'A2 NSGA2-E':('NSGA2','E'),'A3 NSGA2-Dg':('NSGA2','Dg'),'A4 MOEAD-Dg':('MOEAD','Dg')}.items():
    v=pa[k];add(a,b,v['mean'],v['ci99'],'P','P21 A')
for k in ['NSGA2-DA','NSGA2-Dp','MOEAD-E','MOEAD-DA','MOEAD-Dp']:
    a,b=k.split('-');v=sa[k];add(a,b,v['mean'],v['ci95'],'S','P21 A')
p=P17['primary'];add('DA','Dg',p['P5']['mean'],p['P5']['ci99'],'P','P17');add('DA','Dp',p['P4']['mean'],p['P4']['ci99'],'P','P17')
s=P17['secondary']
for k,(a,b) in {'E-DA':('E','DA'),'E-Dg':('E','Dg'),'E-Dp':('E','Dp'),'Dg-Dp':('Dg','Dp')}.items():
    add(a,b,s[k]['mean'],s[k]['ci95'],'S','P17')
pb=B['primary'];sb=B['secondary']
add('Eg1.1','E',pb['B1 Eg1.1-E']['mean'],pb['B1 Eg1.1-E']['ci99'],'P','P21 B');add('Eg0.8','E',pb['B4 Eg0.8-E']['mean'],pb['B4 Eg0.8-E']['ci99'],'P','P21 B')
for k,(a,b) in {'Eg2-E':('Eg2','E'),'Eg6-E':('Eg6','E'),'Eg1.1-Dg':('Eg1.1','Dg'),'Eg1.1-Dp':('Eg1.1','Dp'),'Eg0.8-Dg':('Eg0.8','Dg'),'Eg0.8-Dp':('Eg0.8','Dp')}.items():
    add(a,b,sb[k]['mean'],sb[k]['ci95'],'S','P21 B')
pp=P22['primary'];sp=P22['secondary']
add('GE','GDp',pp['P1 GE-GDp']['mean'],pp['P1 GE-GDp']['ci99'],'P','P22');add('GEg6','GDg6',pp['P2 GEg6-GDg6']['mean'],pp['P2 GEg6-GDg6']['ci99'],'P','P22');add('GDp','NSGA2',pp['P4 GDp-NSGA2']['mean'],pp['P4 GDp-NSGA2']['ci99'],'P','P22')
for k,(a,b) in {'GE-NSGA2':('GE','NSGA2'),'GDg6-NSGA2':('GDg6','NSGA2'),'GEg6-NSGA2':('GEg6','NSGA2'),'GEg6-GE':('GEg6','GE'),'GDg6-GDp':('GDg6','GDp'),'GE-E (descriptive)':('GE','E'),'GDp-Dp (descriptive)':('GDp','Dp'),'GDg6-Dg (descriptive)':('GDg6','Dg')}.items():
    add(a,b,sp[k]['mean'],sp[k]['ci95'],'S','P22')
for (a,b),v in list(ent.items()): ent[(b,a)]=(-v[0],-v[2],-v[1],v[3],v[4])
# means-only
means={'A':{'NSGA2':.6522,'MOEAD':.6586,'E':.5264,'DA':.5264,'Dp':.4837,'Dg':.5300},
'Z':{k:v for k,v in {**{x:P22['hv_oracle_means'][x] for x in P22['hv_oracle_means']},**{x:B['hv_oracle_means'][x] for x in B['hv_oracle_means']}}.items()}}
def mo(a,b):
    sts=[s for s in means if a in means[s] and b in means[s]]
    if sts: d=means[sts[0]][a]-means[sts[0]][b];th=.02
    else:
        ma=[means[s][a] for s in means if a in means[s]];mb=[means[s][b] for s in means if b in means[s]]
        if not ma or not mb: return None
        d=sum(ma)/len(ma)-sum(mb)/len(mb);th=.05
    return d if abs(d)>=th else None
def cell(a,b):
    if a==b:return '—'
    if (a,b) in ent:
        m,lo,hi,l,_=ent[(a,b)];c=cls(lo,hi)
        if c=='?':sym='?'
        else:sym=c if c=='=' else (c*2 if abs(m)>=.02 else c)
        sym=sym.replace('-','−')
        return f'**{sym}**' if l=='P' else f'({sym})'
    d=mo(a,b)
    if d is None:return '·'
    sym=('+' if d>0 else '−')*(2 if abs(d)>=.02 else 1);return f'[{sym}]'
rows=['| ligne ↓ \\ colonne → |'+'|'.join(f' {m} ' for m in M)+'|','|---|'+'|'.join(':-:' for _ in M)+'|']
for a in M: rows.append(f'| **{a}** |'+'|'.join(cell(a,b) for b in M)+'|')
open(S+'paper/matrix_table.md','w').write('\n'.join(rows)+'\n')
# detail list
det=['| Contraste (ligne − colonne) | Étude | Moyenne | IC | Niveau | Décision |','|---|---|---|---|---|---|']
seen=set()
for (a,b),(m,lo,hi,l,st) in ent.items():
    if (b,a) in seen: continue
    seen.add((a,b));det.append(f'| {a} − {b} | {st} | {m:+.4f} | [{lo:+.4f} ; {hi:+.4f}] | {"primaire 99 %" if l=="P" else "secondaire/descriptif 95 %"} | {cls(lo,hi)} |')
open(S+'paper/matrix_detail.md','w').write('\n'.join(det)+'\n')
print('\n'.join(rows));print(len(seen))
