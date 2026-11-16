import re
s=open('Paper_v0_9_num.md').read()
parts=re.split(r'(?m)^(?=#{1,2} )',s)
B={}
for p in parts: B[p.split('\n')[0]]=p
def blk(prefix):
    k=[k for k in B if k.startswith(prefix)]; assert len(k)==1,(prefix,k); return B[k[0]]
def body(prefix): return blk(prefix).split('\n',1)[1].strip()+'\n\n'
def table(tag,droplast=False):
    i=s.index('**Table %s.**'%tag); j=s.index('\n\n',i); cap=s[i:j]
    k=s.index('\n\n',j+2); tb=s[j+2:k]
    if droplast:
        rows=[]
        for r in tb.split('\n'):
            c=r.strip().strip('|').split('|'); rows.append('|'+'|'.join(c[:-1])+'|')
        tb='\n'.join(rows)
    return cap+'\n\n'+tb+'\n\n'
hdr=s.split('# Abstract')[0]
hdr=re.sub(r'(?m)^author: .*$','author: ["Dr Montassar Zaghdoud", "Manouba School of Engineering, Manouba University, Tunisia", "montassar.zaghdoud@mse.uma.tn"]',hdr,1)
hdr=re.sub(r'(?m)^date: .*$','date: "15 November 2026"',hdr,1)
hdr=re.sub(r'(?s)\*\*Status of this draft\.\*\*.*$','',hdr).replace('Draft v0.9, 15 November 2026 (v0.1 to v0.8 kept)','Condensed version (extended version: Paper v0.9), 15 November 2026').replace('v0.1 to v0.8 kept','')
out=hdr+'''# Abstract

Multiobjective team assignment in home health care must cope with uncertain affinities between patients and care teams. We ask whether aggregating population information with Dempster–Shafer evidence, rather than with a probabilistic frequency model, improves a quantum-inspired genetic algorithm, which can be read as a univariate model-based search. We report a sequence of studies whose contrasts, equivalence margins and decision rules were fixed before each run, using paired seeds, an oracle hypervolume measure and semi-synthetic instances built on benchmark geographies, with simulated hidden truth and evidence. The evidential target clearly outperformed the simple probabilistic target, but a probabilistic target sharpened by a power transformation did at least as well on the main instances, and sharpening the evidential target further degraded its performance. Refinements of the evidential structure brought no robust gain, and guiding the mutation of a classical algorithm with the same targets did not help. On two new families of instances, the advantage over the simple probabilistic target was reproduced, whereas the ordering against the sharpened target was not stable. A final study gave the probabilistic target a concentration schedule calibrated to follow that of the evidential target: the evidential target was better when the source strength was low and worse when it was high, and the calibration controlled only two concentration diagnostics. Classical multiobjective algorithms remained far better than all variants of the quantum-inspired algorithm. No representation advantage independent of concentration was established.

**Keywords:** home health care; team assignment; multiobjective optimisation; quantum-inspired genetic algorithm; Dempster–Shafer theory; estimation of distribution; hypervolume; pre-registered experiments.

'''
intro=blk('# 1. Introduction')
i=intro.index('We formalise the two targets')
out+=intro[:i]+'''We formalise the two targets and their concentration (Section 4) and answer the question with a sequence of pre-registered experiments (Sections 5 and 6): a controlled comparison with paired seeds and an equivalence margin; a symmetric sharpening of both representations; refinements of the evidential structure; a transfer to NSGA-II; a dependence-degree and sensitivity study; two independent evaluations on new instance families; and a study that gives the probabilistic target the concentration schedule of the evidential one. The conclusions are limited: the results are compatible with an important role of concentration, they do not show that it is the only mechanism, and they do not show that the evidential representation can never help. NSGA-II and MOEA/D are far better at the same budget, so the study concerns a representation *inside* QGA2-E.

'''
out+='# 2. Related work\n\n'
for h in ['## 2.2','## 2.3','## 2.4']: out+=blk(h).rstrip()+'\n\n'
out+=blk('## 2.6').rstrip()+'\n\n'
for h in ['# 3. Problem','## 3.1','## 3.2','## 3.3','## 3.4','# 4. Algorithms','## 4.1','## 4.2','## 4.3']: out+=blk(h).rstrip()+'\n\n'
out+='## 4.4 Baselines and other variants\n\nNSGA-II [26] and MOEA/D [27] are run on the same instances, seeds, decoder and budget, with an archive of every evaluated solution re-evaluated in the oracle world as for QGA2-E. Guided mutation in NSGA-II draws the new team of a mutated gene (probability $1/n_p$) from the target $q$ restricted to the other allowed teams; with $q$ uniform it is bit-for-bit NSGA-II. Each algorithm received the same small tuning effort, three candidate parameter sets evaluated on separate tuning seeds under a selection rule written before the runs (the rotation step of QGA2-E, the crossover and mutation probabilities of NSGA-II, the neighbourhood size of MOEA/D; the a priori set was kept unless another improved the criterion by at least 0.001). The comparison with the classical algorithms is therefore contextual: it is made at equal budget, on one problem family and with a limited tuning effort, and it is not a ranking of algorithm families or evidence about other model-based algorithms.\n\n'
out+='# 5. Experimental design and decision rules\n\n'
for h in ['## 5.1','## 5.2','## 5.3']: out+=blk(h).rstrip()+'\n\n'
out+='## 5.4 Seeds and sample sizes\n\nEach study uses seeds not used by calibration or technical tests. Main ranges: 11200–11299 and 10400–10499 (100 seeds, six scenarios derived from three Solomon geographies), 12000–12099 (two studies, not independent), 14000–14059 (first independent evaluation), 15000–15059 (second) and 16000–16059 (concentration-schedule study). Sample sizes are 100 seeds for most studies, 200 or 300 for the earliest ones and 60 for the latest; contrasts are paired within a study only.\n\n'
out+='''# 6. Results

All differences are in oracle hypervolume (the mean of the QGA2-E variants is about 0.5, that of NSGA-II about 0.65); intervals are 99% for primary contrasts with the margin 0.005 and 95% for secondary or descriptive ones, and each quoted contrast says which. Question 1 (does the evidential target beat the simple probabilistic target?): Sections 6.2 and 6.6. Question 2 (is concentration the mechanism, or the representation, or the schedule?): Sections 6.3, 6.5 and 6.7. Question 3 (transfer to another algorithm): Section 6.8. Question 4 (does it hold outside the original instances?): Section 6.6. The pairwise matrix of all methods (Table 1) and the detail of Sections 6.3 to 6.5 are in the extended version.

## 6.1 Classical algorithms against QGA2-E

At equal budget NSGA-II and MOEA/D exceed every QGA2-E variant: NSGA-II − E = +0.1258 [+0.1214, +0.1301], NSGA-II − Dg = +0.1221 [+0.1177, +0.1265], MOEA/D − Dg = +0.1286 [+0.1239, +0.1331] (100 seeds, 99% CI; MOEA/D slightly better than NSGA-II, −0.0065 [−0.0092, −0.0037]). The gap is 0.11 to 0.17 depending on the variant, and earlier studies gave 0.13 to 0.16; adding elitism to QGA2 did not close it.

## 6.2 Evidential against probabilistic targets

In every early study an evidential target built by Dempster's rule had a higher hypervolume than the matched probabilistic target of the same study (n = 200): Dempster's rule over the matched probabilistic control +0.0250 [+0.0238, +0.0262]; fully evidential against fully probabilistic pipeline +0.0275 [+0.0261, +0.0289]; in the QGA2-E architecture E − P = +0.0459 [+0.0444, +0.0473], 100% of seeds favourable; the cautious rule was worse than both. Stacking evidential layers gave no additional benefit. These probabilistic targets were not matched in concentration, so these studies do not say whether the representation or the resulting sharpness is responsible.

## 6.3 Concentration of the target

At generation 150 the mean maximum of the target was 0.281 for Dp, 0.805 for Dg (γ = 6) and 0.851 for E, with entropies 1.452, 0.646 and 0.525: the evidential target is far more concentrated than the simple probabilistic target, as Proposition 2 predicts. A power-sharpened probabilistic target reproduced and slightly exceeded the evidential advantage: in a descriptive study (n = 200) Dg − Dp = +0.0454 and E − Dg = −0.0040 [−0.0055, −0.0025]; in the confirmatory comparison (n = 100) DA − Dp = +0.0427 [+0.0401, +0.0454] and DA − Dg = −0.0036 [−0.0064, −0.0009], an inferiority whose interval extends beyond the margin. The exponent of Dg was chosen by concentration matching on calibration seeds without reading hypervolume; the matching gate was not met by any exponent in the descriptive study (best attempt γ = 6, declared non-conforming).

Sharpening the evidential target made it worse (n = 100): Eg2 − E = −0.0046 [−0.0076, −0.0016], Eg6 − E = −0.016 [−0.0188, −0.0130], Eg6 − Dg = −0.0204 [−0.0231, −0.0177], while exponents between 0.9 and 1.25 were equivalent to E (for example Eg1.1 − E = +0.0010 [−0.0015, +0.0036]). The key contrast for representation, the evidential target sharpened to match the concentration of Dg against Dg (n = 60), was *inconclusive*: DAgm − Dg = −0.0025 [−0.0057, +0.0009]. The calibration used other scenarios and compared means only, so matching on the evaluation scenarios was not guaranteed. This study does not show that the two representations are equivalent, nor that concentration is the exclusive cause of the evidential advantage.

'''
out+=blk('## 6.5').replace('## 6.5 Refinements of the evidential structure','## 6.4 Refinements of the evidential structure').replace('Appendix E','the extended version (Appendix E)').rstrip()+'\n\n'
out+='''## 6.5 Dependence degree and local sensitivity

Two later studies (n = 100, seeds 12000–12099, not independent) varied the dependence degree λ of the dependence-corrected target DA and then the source strength w, the similarity threshold σ and the exponent, one at a time. The parameter λ changed the concentration of the target markedly (maximum probability at generation 150 from 0.845 for E to 0.709 for λ = 1) without changing hypervolume (DA(1) − E = −0.0009 [−0.0025, +0.0007], equivalence; DA − Dg between −0.0029 and −0.0039 with a conforming match). In the sensitivity study the evidential target kept a large advantage over the simple probabilistic target at every source strength (E − Dp = +0.028 to +0.043), but the sign of DA − Dg depended on the setting: +0.0032 [+0.0010, +0.0052] at w = 0.15 and −0.0039 [−0.0066, −0.0014] at the reference w = 0.3 (both with a conforming match), and unattributable where the match failed (w = 0.5, w = 0.7, σ = 0.6). Post hoc observations are in the extended version.

## 6.6 Independent evaluations on new families of instances

'''+'''All earlier decisions were made on scenarios derived from three Solomon geographies. Two studies, each with a protocol written before any calibration or run, ask which main contrasts hold on instances that played no role in those decisions (new geographies, sizes and seeds; the free exponent was recalibrated each time; only the geography changes, so the instances are semi-synthetic). The first used synthetic Solomon-like geographies (uniform, clustered, mixed; 40 patients and 9 teams, or 70 and 12; 60 seeds per scenario, 360 instances); the second used customer coordinates of six public benchmark files (Uchoa X-n101-k25 [30], Christofides M-n101-k10 [31], Golden_1 [32], Li_21 [33], ORTEC-n242-k12 and Homberger C1_2_1 [34]) from the test data of VRPLIB [35], with 50 patients sampled per seed, 10 teams, day end 240 and visit 10 (60 seeds, 360 instances). Skills, windows, hidden truth and evidence are simulated by the unchanged generator. The concentration gate was satisfied at w = 0.7 only; at w = 0.3 the match failed in both evaluations.

'''+table('6')+table('7')+'''In both evaluations the simple probabilistic target was clearly the weakest (about 0.02 below E and DA) in every geography, and DA and E were equivalent at w = 0.7; the earlier small advantage of DA over E at w = 0.7 was not reproduced. The ordering between the evidential targets and the sharpened probabilistic target was not stable: Dg was better on the synthetic geographies; on the benchmark geographies it was worse than E and DA with the calibrated exponent at w = 0.3 (γ = 4), better with γ = 6, and inconclusive at w = 0.7. A sharpened probabilistic target is therefore not a robust substitute unless its exponent is tuned on instances of the target family; this agrees with the importance of concentration and does not show that the representation matters independently of it.

## 6.7 Matching the concentration trajectory: representation or schedule?

The evidential target concentrates on a schedule of its own, whereas Dg uses one fixed exponent, so earlier comparisons mix representation and schedule. This study gives the simple probabilistic target a time-varying exponent $\\gamma_t=g_0+(g_1-g_0)\\min\\{1,(t-1)/(G_s-1)\\}$ (renormalised, floor 0.02; Dgt; a constant ramp equals Dg bit for bit). On the benchmark geographies of the second evaluation (new seeds 16000–16059 and patient samples, 360 instances; not independent of that evaluation), the schedule was selected once per source strength and reference target (E or DA) without reading hypervolume, on other seeds, among 12 candidates ($g_0\\in\\{1,3\\}$, $g_1\\in\\{6,10,16\\}$, $G_s\\in\\{30,90\\}$), using a gate on the whole trajectory (mean relative entropy gap ≤ 10% and mean $|\\Delta q_{\\max}|$ ≤ 0.05) and the least squared gap among the candidates that passed; the match was then verified on the evaluation instances without recalibration. The schedules were 3→6 over 90 generations at w = 0.3 and 3→6 over 30 generations at w = 0.7 (the same for E and DA). The match was conforming for E at both strengths (entropy gap 4.8% and 5.9%) and for DA at w = 0.3, and not conforming for DA at w = 0.7 (21.7%, $|\\Delta q_{\\max}|$ 0.061), where the contrast is descriptive. The pre-registered reading: with a conforming match, a superior E means that the advantage is not explained by the schedule alone; a superior Dgt means that a probabilistic schedule does better than Dempster's rule.

'''+table('8',True)+'''Mean hypervolumes were, at w = 0.3, 0.2013 (E), 0.2008 (DA), 0.1783 (Dp), 0.1947 (Dgt) and 0.2078 (Dg with γ = 6); at w = 0.7, 0.2066, 0.2072, 0.1824, 0.2117 and 0.2073. At w = 0.3 the evidential target was better than the scheduled probabilistic target, in four of six geographies; at w = 0.7 the sign reversed and Dgt was better than E in each geography; Bonferroni intervals gave the same decisions. A fixed exponent of 6 was better than both E and the scheduled target at w = 0.3, so the schedule selected by the gate is not the one that maximises hypervolume. The advantage of E over a probabilistic target with the same schedule of entropy and maximum probability is thus not explained by the schedule of these two diagnostics alone at w = 0.3, but it is not consistent across source strengths, and no general advantage or disadvantage of the representation follows. The match covers two scalar diagnostics: the effective decoded distributions of the matched arms remained far apart at generation 150 (Jensen–Shannon divergence 0.17 at w = 0.3 and 0.33 at w = 0.7; L1 distance 0.74 to 0.96 out of 2). The schedule family has three parameters, was selected on three geographies, and the geographies are those of the second evaluation.

## 6.8 Transfer to NSGA-II

A transfer study (n = 100, five primary contrasts, 99% CI) guided the mutation of NSGA-II by the targets. Guiding with the probabilistic target did not change hypervolume (GDp − NSGA-II = 0.0000 [−0.0033, +0.0033], equivalence); the evidential target was not better than the probabilistic one (GE − GDp = −0.0040 [−0.0072, −0.0008], the interval partly inside the margin; equivalent after the same sharpening, +0.0021 [−0.0006, +0.0049]). The concentration-matched evidential arm degenerated into the natural evidential arm, so that contrast does not isolate the representation. All guided arms stayed within 0.004 of unguided NSGA-II (0.6429).

'''
out+='''# 7. Discussion

**What the evidence supports.** Within QGA2-E, an evidential target built by Dempster's rule is better than a simple probabilistic target, by 0.025 to 0.046 depending on the study, and this was reproduced on two new instance families. A power-sharpened probabilistic target obtains at least as much on the main instances, so the evidential target has no advantage over the best probabilistic target tested; sharpening the evidential target does not help (flat plateau from γ = 0.9 to 1.5, decline beyond). This is consistent with the view that much of the initial advantage is a matter of concentration, as Proposition 2 suggests: the evidential target responds to agreement exponentially, the frequency target only linearly.

**Representation or schedule.** The schedule study (Section 6.7) gives a source-strength-dependent result: the evidential target was better than the scheduled probabilistic target at w = 0.3 and worse at w = 0.7, and a fixed exponent of 6 was better than both at w = 0.3. The schedule therefore does not explain away the evidential advantage at w = 0.3 in this design, but there is no consistent advantage of the representation, and the match was on two diagnostics only; the study neither establishes nor excludes a representation effect independent of concentration. **Possible explanation (untested hypothesis).** The trajectory match controls the mean entropy and the mean maximum probability, but the decoded distributions of the matched arms stayed far apart at generation 150 (Jensen–Shannon divergence 0.17 at w = 0.3 and 0.33 at w = 0.7, with mean relative entropy gaps of 4.8% and 5.9%). Two targets with the same entropy and the same maximum can spread the remaining probability differently over the other allowed teams, and can differ in the patients on which they concentrate first; such differences may matter more at the higher source strength, where the divergence was larger and the sign of the contrast changed. We did not test this: it would require comparing per-patient distributions and archive diversity from the stored runs, a post hoc analysis that was not part of the pre-registered protocol.

**Sensitivity and independent evaluations.** The dependence degree changes the concentration of the evidential target without changing hypervolume, and the comparison of DA with a concentration-matched sharpened target changes sign with the setting; the independent evaluations did not reproduce a stable ordering against the sharpened target. Matching mean concentration is a weak notion of equivalence: trajectories and decoded distributions differ. A practitioner who sharpens a probabilistic target should tune the exponent on instances of the target family.

**Why the effect does not transfer, and why classical algorithms are better.** In QGA2-E the target is the only driver of the search; in NSGA-II it decides only the new team of about one mutated gene per child, so there was little room for the representation to matter (a hypothesis, not tested). A candidate, untested explanation of the 0.11–0.17 gap is structural: QGA2-E samples each patient independently and cannot learn dependences between the team choices of different patients, which crossover can exploit; hence the paper studies target construction in a univariate model-based search and is not a contribution to home-care optimisation. For practice, a classical NSGA-II or MOEA/D is the safer choice at this budget.

# 8. Limitations

1. **Set-up.** One algorithm, one problem formulation (assignment with fixed visit order; a step in the time-window satisfaction, Section 3.2), one budget, one hypervolume reference point and one evidence generator.
2. **Semi-synthetic data.** Only the coordinates come from benchmark files; windows, skills, certifications, hidden truth and evidence are generated; no real home-care data are included.
3. **Adaptive sequence.** Studies reuse seeds and reference results seen earlier; each controls its own family of contrasts but nothing controls the whole sequence; several studies are descriptive or share seeds; the latest have 60 seeds.
4. **Approximate concentration matching.** Two scalar summaries of mean concentration, calibrated on other scenarios, failed on the evaluation instances in several settings; decoded distributions of matched arms remained far apart.
5. **Parameters.** The source strength w = 0.3 was inherited from a calibration informed by hypervolume; sensitivity was local; the schedule family has three parameters.

# 9. Conclusion

In QGA2-E for home health care team assignment, an evidential target built with Dempster's rule outperformed a simple probabilistic target, but a power-sharpened probabilistic target performed at least as well on the main instances, further sharpening of the evidential target lowered its performance, and the comparison designed to match concentration was inconclusive. Refinements of the evidential structure gave no robust gain, and guiding NSGA-II with the same targets did not help; NSGA-II and MOEA/D stayed 0.11 to 0.17 hypervolume above all QGA2-E variants. Two independent evaluations reproduced the large advantage over the simple probabilistic target and the equivalence of DA and E at a high source strength, but not a stable ordering against the sharpened target. A final study that gives the probabilistic target the concentration schedule of the evidential target found the evidential target better at w = 0.3 and worse at w = 0.7. No representation advantage independent of concentration was established in the configurations tested, on semi-synthetic instances. Perspectives: designs that manipulate concentration and representation independently with exact distributional matching, other integration points of evidence in classical algorithms, multivariate models, other budgets and instance families, real evidence data, and integrated routing and scheduling.

'''
out+=blk('# References').rstrip()+'\n\n'
out+='''# Appendix A. Declared incidents and deviations (summary)

No run was repeated to improve a result and no hypothesis, margin or rule was changed after results were read; the incidents are declared in the Supplementary Material (Appendix A).

'''
gl="""# Appendix B. Glossary of abbreviations

**Algorithms.** QGA2-E: the quantum-inspired GA of this paper (one angle θ per gene, selection probability sin²θ, target computed from the first non-dominated front). NSGA-II, MOEA/D: classical multiobjective GAs (non-dominated sorting with crowding; decomposition).

**Targets.** q: target probability per team. Dp: simple probabilistic target. E: evidential target (Dempster's rule, then BetP). DA(λ): E with source discounting by similarity (λ = 1 is DA, σ = 0.7). Dg(γ), Eg(γ): Dp, E sharpened by the power γ (γ = 6 unless stated).

"""
out+=gl
out=out.replace('Appendix D','Appendix B')

def R(a,b,n=None):
    global out
    assert a in out,a; out=out.replace(a,b)
R('(Section 6.2), and we make no claim','(Section 6.1), and we make no claim')
R('(Section 8). The implementation guards','(Section 8). The implementation guards')
R('Appendix B). Only the customer','Appendix B). Only the customer')
R('early comparisons of Section 6.3','early comparisons of Section 6.2')
R('Sections 6.4 to 6.6 all use','Sections 6.3 to 6.7 all use')
for a,c in [('## 2.2 ','## 2.1 '),('## 2.3 ','## 2.2 '),('## 2.4 ','## 2.3 '),('## 2.6 ','## 2.4 '),('(Section 2.4)','(Section 2.3)'),('(Section 2.2)','(Section 2.1)')]:
    assert a in out,a; out=out.replace(a,c)
out=out.replace('**Table 6.**','**Table 2.**').replace('**Table 7.**','**Table 3.**').replace('**Table 8.**','**Table 4.**').replace('(Table 1) and the detail','(Table 1) and the detail')

full=open('Paper_v0_9_num.md').read()
i=full.index('**Table 1.**'); j=full.index('## 6.2 Classical algorithms'); t1=full[i:j].rstrip()+'\n\n'
t1=t1.replace('Abbreviations are defined in Appendix D.','Abbreviations are defined in Appendix B.').replace('Other abbreviations: Appendix D.','Other abbreviations: Appendix B.')
assert '## 6.1 Classical algorithms against QGA2-E' in out
out=out.replace('## 6.1 Classical algorithms against QGA2-E', t1+'## 6.1 Classical algorithms against QGA2-E',1)
for a,c in [('**Table 3.**','**Table 4.**'),('**Table 2.**','**Table 3.**'),('**Table 1.** Independent','**Table 2.** Independent')]:
    pass
out=out.replace('the extended version (Table B2)','the Supplementary Material (Table B2)').replace('extended version','Supplementary Material')
out=out.replace('summarised in Section 2.6','summarised in Section 2.4')
out=out.replace('Sections 2.2–2.4, belief','Sections 2.1–2.3, belief')
out=out.replace('# References','**Supplementary material.** The extended manuscript (with the full results of Sections 6.3 to 6.5, the post hoc analyses, the full limitations, the declared incidents and the refinement studies), the frozen protocols and code, and the final analysis files are provided as Supplementary Material and archived in release V1.0 of https://github.com/MontZ26/Evidential_QGA2E_paper_archive (permanent link: https://github.com/MontZ26/Evidential_QGA2E_paper_archive/releases/tag/V1.0).\n\n**Use of AI tools.** The author used Claude (Anthropic) to assist with drafting and editing the manuscript text, preparing tables and figures from the analysis files, and checking cross-references and citations. The experimental design, the experiments, the interpretation of the results and the final content were produced and verified by the author, who takes full responsibility for the manuscript.\n\n# References',1)

def Q(a,c):
    global out
    assert out.count(a)==1,(out.count(a),a); out=out.replace(a,c)
import re as _re
m=_re.search(r"The pairwise matrix of all methods \(Table 1\) and the detail of Sections 6\.3 to 6\.5 are in the (?:Supplementary Material|extended version)\.",out); assert m
out=out.replace(m.group(0),"Table 1 gathers the pairwise differences in oracle hypervolume between the 14 methods on the six Solomon-derived scenarios (SC6): bold values are primary pre-registered paired contrasts (99% CI), round brackets secondary paired contrasts (95% CI), and square or curly brackets differences of means (within or across seed ranges) without intervals. The values quoted in Sections 6.1, 6.3 and 6.8 are taken from it or from the paired contrasts it lists; studies on other seed ranges (Sections 6.5 to 6.7) are reported in their own tables and are not in it. The detail of Sections 6.3 to 6.5 is in the Supplementary Material.")
Q("(100 seeds, 99% CI; MOEA/D slightly better","(Table 1; 100 seeds, 99% CI; MOEA/D slightly better")
Q("in the confirmatory comparison (n = 100) DA − Dp","in the confirmatory comparison (n = 100; Table 1 gives the confirmatory values) DA − Dp")
Q("The concentration gate was satisfied at w = 0.7 only; at w = 0.3 the match failed in both evaluations.","The concentration gate was satisfied at w = 0.7 only; at w = 0.3 the match failed in both evaluations. Results are in Tables 2 and 3.")
Q("where the contrast is descriptive.","where the contrast is descriptive (Table 4).")
Q("unguided NSGA-II (0.6429).","unguided NSGA-II (0.6429; Table 1).")
Q("used in Section 6.7)","used in Section 6.6)")
out=out.replace('Section 3.4 and Appendix B)','Section 3.4)').replace('RC101, R101 and C101 (Appendix B).','RC101, R101 and C101.')
out=out.replace('softened by γ.;\n','softened by γ.\n').replace('softened by γ;\n','softened by γ.\n')
out=out.replace('weight of evidence;\n','weight of evidence.\n')
import re as _r2
_m=_r2.search(r"(?m)^\*\*Instances\.\*\* Six scenarios[^\n]*$",out); assert _m
out=out.replace(_m.group(0),_m.group(0)+" Public home-care benchmark sets exist [29] but contain no observed affinities or evidence sources, which is why the evidence is simulated here.",1)
open('Paper_v0_9_short_num.md','w').write(out); print(len(out.split()))
