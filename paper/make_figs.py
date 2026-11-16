import json, math, numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
S="/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/"; O=S+"paper/fig/"
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"axes.spines.top":False,"axes.spines.right":False})
BL,OR,GR,RD,PU="#0072B2","#D55E00","#009E73","#CC79A7","#555555"
def box(ax,x,y,w,h,t,fc="#EEF3F8",ec="#33506B",fs=8.5,bold=False):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.01,rounding_size=0.02",fc=fc,ec=ec,lw=1.1))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs,fontweight="bold" if bold else "normal",wrap=True)
def arr(ax,a,b,t=None,rad=0):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=11,lw=1.1,color="#33506B",connectionstyle=f"arc3,rad={rad}"))
    if t: ax.text((a[0]+b[0])/2,(a[1]+b[1])/2+0.025,t,ha="center",fontsize=7.5,color="#33506B")

# ---- Fig 1: information model and evaluation pipeline
fig,ax=plt.subplots(figsize=(7.4,3.9)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
box(ax,0.02,0.72,0.17,0.2,"Document\nmass 0.5\nreliability 0.95"); box(ax,0.02,0.45,0.17,0.2,"Supervision\nnoisy score\nreliability 0.80"); box(ax,0.02,0.18,0.17,0.2,"History\nPoisson(2) counts\nreliability 1.0")
box(ax,0.30,0.45,0.17,0.2,"Shafer discount\n+ conjunctive rule\nconflict K → frame",fc="#FFF4E0",ec="#9C6B00"); 
for y in (0.82,0.55,0.28): arr(ax,(0.19,y),(0.30,0.55))
box(ax,0.55,0.45,0.17,0.2,"Nominal adequacy\n0.25 + 0.60·BetP",fc="#FFF4E0",ec="#9C6B00"); arr(ax,(0.47,0.55),(0.55,0.55))
box(ax,0.55,0.12,0.17,0.2,"Search\nevaluates f1, f2, f3\nin NOMINAL world\n(budget 6,040)"); arr(ax,(0.635,0.45),(0.635,0.32))
box(ax,0.80,0.12,0.18,0.2,"Archive of\nnon-dominated\nsolutions"); arr(ax,(0.72,0.22),(0.80,0.22))
box(ax,0.80,0.45,0.18,0.2,"ORACLE world\ntrue A, S\n(never seen by search)",fc="#E8F5EE",ec="#1B6B47"); 
box(ax,0.80,0.74,0.18,0.18,"Outcome:\noracle hypervolume\n(ref. point 1.2)",fc="#E8F5EE",ec="#1B6B47",bold=True)
arr(ax,(0.89,0.32),(0.89,0.45),"re-evaluate once"); arr(ax,(0.89,0.65),(0.89,0.74))
ax.text(0.02,0.97,"Information available to the optimiser",fontsize=8.5,fontweight="bold",va="top")
ax.text(0.55,0.97,"Search and measurement",fontsize=8.5,fontweight="bold",va="top")
fig.tight_layout(); fig.savefig(O+"fig1_information_pipeline.png",dpi=220); plt.close(fig)

# ---- Fig 2: QGA2-E generation loop with target
fig,ax=plt.subplots(figsize=(7.4,3.6)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
box(ax,0.02,0.60,0.26,0.3,"Population of 40\nangles θ[p,t]\ndecoded to teams x(p)")
box(ax,0.37,0.60,0.26,0.3,"Evaluate 3 objectives\nnon-dominated sorting\nelitist survival (40)")
box(ax,0.72,0.60,0.26,0.3,"Source set S =\nfirst front F1",fc="#FFF4E0",ec="#9C6B00")
box(ax,0.72,0.10,0.26,0.32,"Target q[p,·]\nDp: frequency\nE: Dempster + BetP\nhardening: q^γ",fc="#FFF4E0",ec="#9C6B00")
box(ax,0.37,0.10,0.26,0.32,"Rotation of every\nindividual towards q\nδ = 0.05π")
arr(ax,(0.28,0.75),(0.37,0.75)); arr(ax,(0.63,0.75),(0.72,0.75)); arr(ax,(0.85,0.60),(0.85,0.42)); arr(ax,(0.72,0.26),(0.63,0.26)); arr(ax,(0.37,0.26),(0.15,0.60),rad=-0.15); ax.text(0.03,0.47,"new angles,\nnew draws",fontsize=7.5,color="#33506B")
ax.text(0.02,0.12,"q is computed once per generation\nand used for every individual.",fontsize=8,color=PU)
fig.tight_layout(); fig.savefig(O+"fig2_qga2e_loop.png",dpi=220); plt.close(fig)

# ---- Fig 3: analytic concentration of targets
w=0.3; om=-math.log(1-w); K=4; N=10; eps=0.02
def tgt(n_vec,kind,g=1.0):
    n=np.array(n_vec,float)
    if kind=="Dp": q=w*n/n.sum()+(1-w)/K
    else:
        e=np.exp(om*n)-1; D=1+e.sum(); q=e/D+(1/D)/K
    if g!=1.0 or kind in("Dg",):
        gg=6 if kind=="Dg" else g
        qp=q**gg; q=eps+(1-K*eps)*qp/qp.sum()
    return q
ns=np.linspace(2.5,N,101); fig,axs=plt.subplots(1,2,figsize=(7.6,3.2))
for lab,kind,g,c,ls in [("Dp (frequency)","Dp",1,BL,"-"),("Dg (frequency, γ = 6)","Dg",6,OR,"-"),("E (Dempster + BetP)","E",1,GR,"-"),("Eg (γ = 1.5)","E",1.5,RD,"--"),("Eg (γ = 6)","E",6,PU,"--")]:
    qm=[tgt([n]+[(N-n)/3]*3,kind,g).max() for n in ns]; axs[0].plot(ns,qm,label=lab,color=c,ls=ls,lw=1.8)
axs[0].set_xlabel("sources agreeing on the leading team (N = 10; others split evenly)"); axs[0].set_ylabel("target maximum q_max"); axs[0].set_title("(a) Response to agreement (K = 4 teams)",fontsize=9); axs[0].legend(fontsize=7,frameon=False); axs[0].set_ylim(0,1)
# (b) empirical
B=json.load(open(S+"p21/p21_final_analysis_B.json"))["diagnostics"]; gens=[1,25,50,100,150]
for lab,key,c,ls in [("Dp","Dp",BL,"-"),("Dg","Dg",OR,"-"),("E","E",GR,"-"),("Eg1.5","Eg1.5",RD,"--"),("Eg6","Eg6",PU,"--")]:
    axs[1].plot(gens,[B[key]["q_max"][str(g)] for g in gens],marker="o",ms=3.5,label=lab,color=c,ls=ls,lw=1.6)
axs[1].set_xlabel("generation"); axs[1].set_ylabel("mean q_max (scenarios × seeds)"); axs[1].set_title("(b) Observed during the runs",fontsize=9); axs[1].set_ylim(0,1); axs[1].legend(fontsize=7,frameon=False,ncol=2)
fig.tight_layout(); fig.savefig(O+"fig3_target_concentration.png",dpi=220); plt.close(fig)

# ---- Fig 4: gamma plateau
M=json.load(open(S+"p21/p21_final_analysis_B.json"))["hv_oracle_means"]
gs=[0.8,0.9,1.0,1.1,1.25,1.5,2,4,6]; keys=["Eg0.8","Eg0.9","E","Eg1.1","Eg1.25","Eg1.5","Eg2","Eg4","Eg6"]
fig,ax=plt.subplots(figsize=(5.8,3.4)); ax.plot(gs,[M[k] for k in keys],marker="o",color=GR,lw=1.8,label="Evidential target, hardened (Eg)")
ax.axhline(M["Dg"],color=OR,ls="--",lw=1.3); ax.text(5.9,M["Dg"]+0.0007,"Dg (probabilistic, γ = 6)",color=OR,ha="right",fontsize=8)
ax.axhline(M["Dp"],color=BL,ls="--",lw=1.3); ax.text(5.9,M["Dp"]+0.0005,"Dp (probabilistic, natural)",color=BL,ha="right",fontsize=8)
ax.axhspan(M["E"]-0.005,M["E"]+0.005,color=GR,alpha=0.12); ax.text(2.1,M["E"]-0.0075,"band: E ± 0.005",fontsize=7.5,color="#1B6B47")
ax.set_xscale("log"); ax.set_xticks(gs); ax.set_xticklabels([str(g) for g in gs]); ax.minorticks_off()
ax.set_xlabel("hardening exponent γ (log scale; γ = 1 is E)"); ax.set_ylabel("mean oracle hypervolume"); ax.legend(frameon=False,fontsize=8,loc="lower left")
ax.set_ylim(0.470,0.535); fig.tight_layout(); fig.savefig(O+"fig4_gamma_curve.png",dpi=220); plt.close(fig)

# ---- Fig 5: forest plot of confirmatory contrasts
def L(p): return json.load(open(S+p))["primary"]
rows=[]
def add(group,label,d): rows.append((group,label,d["mean"],d["ci99"][0],d["ci99"][1],d["decision"]))
p17=L("p17/p17_final_analysis.json"); add("Evidential vs probabilistic, QGA2-E","DA − Dp",p17["P4"]); add("Evidential vs probabilistic, QGA2-E","DA − Dg",p17["P5"])
p20=L("p20/p20_final_analysis.json")
for k,l in [("C1 Eg2-E","Eg2 − E"),("C2 Eg6-E","Eg6 − E"),("C3 Eg6-Dg","Eg6 − Dg")]: add("Hardening the evidential target",l,p20[k])
p21=L("p21/p21_final_analysis_B.json")
for k,l in [("B4 Eg0.8-E","Eg0.8 − E"),("B3 Eg0.9-E","Eg0.9 − E"),("B1 Eg1.1-E","Eg1.1 − E"),("B2 Eg1.25-E","Eg1.25 − E")]: add("Exponent near the natural value",l,p21[k])
p19=L("p19/p19_final_analysis.json"); add("Concentration-matched","DAgm − Dg",p19["C2 DAgm-Dg"]); add("Concentration-matched","DAgm − DA",p19["C4 DAgm-DA"])
p22=L("p22/p22_final_analysis.json")
for k,v in p22.items(): pass
names={"P1 GE-GDp":"GE − GDp","P2 GEg6-GDg6":"GEg6 − GDg6","P3 GEgm-GDg6":"GEgm − GDg6","P4 GDp-NSGA2":"GDp − NSGA-II"}
for k,l in names.items(): add("Guided mutation in NSGA-II",l,p22[k])
col={"superiority":BL,"inferiority":OR,"equivalence":GR,"inconclusive":PU}
fig,ax=plt.subplots(figsize=(7.2,5.6)); y=0; yt=[]; yl=[]; lastg=None; gy={}
for g,l,m,lo,hi,d in rows:
    if g!=lastg: y-=0.8; gy[g]=y; lastg=g
    y-=1; ax.plot([lo,hi],[y,y],color=col[d],lw=2); ax.plot(m,y,"o",color=col[d],mfc=("white" if d=="inconclusive" else col[d]),ms=5); yt.append(y); yl.append(l)
ax.axvspan(-0.005,0.005,color="#999",alpha=0.15); ax.axvline(0,color="k",lw=0.8)
ax.set_yticks(yt); ax.set_yticklabels(yl,fontsize=8)
for g,yy in gy.items(): ax.text(-0.0295,yy+0.1,g,fontsize=8,fontweight="bold",va="center")
ax.set_xlim(-0.03,0.05); ax.set_xlabel("paired difference in oracle hypervolume (mean and 99% bootstrap CI); grey band = ±0.005 margin")
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([0],[0],color=c,lw=2,label=k) for k,c in col.items()],frameon=False,fontsize=8,loc="lower right",title="decision")
fig.tight_layout(); fig.savefig(O+"fig5_forest_contrasts.png",dpi=220); plt.close(fig)

# ---- Fig 6: classical vs QGA2-E
A=json.load(open(S+"p21/p21_final_analysis_A.json"))["hv_oracle_means"]
order=["MOEAD","NSGA2","DA+SELR","DA+SEL4","Dg","DA","E","Dp"]; lab={"MOEAD":"MOEA/D","NSGA2":"NSGA-II"}
fig,ax=plt.subplots(figsize=(5.8,3.3)); ax.barh([lab.get(k,k) for k in order][::-1],[A[k] for k in order][::-1],color=[OR if k in("MOEAD","NSGA2") else BL for k in order][::-1])
for i,k in enumerate(order[::-1]): ax.text(A[k]+0.003,i,f"{A[k]:.4f}",va="center",fontsize=8)
ax.set_xlim(0,0.75); ax.set_xlabel("mean oracle hypervolume (same 100 seeds, same budget)"); fig.tight_layout(); fig.savefig(O+"fig6_classical_vs_qga.png",dpi=220); plt.close(fig)
print("ok")
