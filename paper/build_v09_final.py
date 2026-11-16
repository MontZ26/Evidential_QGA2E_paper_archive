import json
S='/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/'
d=json.load(open(S+'p26/p26_final_analysis.json'))
s=open('Paper_v0_9_pre.md').read()
def rep(old,new,n=1):
    global s
    assert s.count(old)==n,('COUNT',s.count(old),old[:90]); s=s.replace(old,new)
C=d['contrasts']; M=d['matching_trajectory_SC6P26']; H=d['hv_oracle_means']
def f(x): return ('%+.4f'%x).replace('-','−')
def ci(k): a,b=C[k]['ci99']; return '[%s, %s]'%(f(a),f(b))
# status, date
i=s.index('**Status of this draft.**'); j=s.index('# Abstract')
s=s[:i]+'''**Status of this draft.** v0.9 revises v0.8 in response to a review of the manuscript: it adds a justification of why a non-competitive algorithm is studied (Introduction, Section 2.6), reports a pre-registered study that separates the evidential representation from the concentration *schedule* (Section 6.8, Table 8, Table 9), condenses Section 6 (the refinement studies moved to Appendix E), clarifies the interpretation of the time-window objective, resolves a notation collision (worlds are written $\\xi$, the weight of evidence $\\omega$), and corrects the description of required skills. No earlier result, protocol or experiment was changed. The numbers of the new study come from the single final analysis file of that study. Entries of the reference list marked † still have at least one detail that was not confirmed (Section References). The author's own systematic search ("RS1") has not been done, so **this draft makes no novelty claim**. Remaining notes marked [AUTHOR TO COMPLETE], [AUTHOR TO DECIDE] or [AUTHOR TO CHECK] require the author.

'''+s[j:]
# abstract
rep('The instances are semi-synthetic: benchmark geographies, simulated hidden truth and evidence sources.\n','The instances are semi-synthetic: benchmark geographies, simulated hidden truth and evidence sources. A final pre-registered study replaced the fixed exponent of the probabilistic target by a schedule calibrated, without hypervolume, to follow the concentration trajectory of the evidential target. At the reference strength (w = 0.3, trajectory match conforming) the evidential target was better than this scheduled probabilistic target (E − Dgt = %s, 99%% CI %s), whereas at w = 0.7 it was worse (%s, 99%% CI %s); the effect therefore depends on the source strength, and a fixed exponent of 6 was better than both at w = 0.3. The match covered two concentration diagnostics only; decoded distributions remained far apart.\n'%(f(C['L1 E-Dgt_E w=0.3']['mean']),ci('L1 E-Dgt_E w=0.3'),f(C['L1 E-Dgt_E w=0.7']['mean']),ci('L1 E-Dgt_E w=0.7')))
# contributions
rep('7. a full account of what was and was not pre-registered, including declared incidents.','7. a study that replaces the fixed exponent of the sharpened probabilistic target by a concentration schedule calibrated to the trajectory of the evidential target, to separate representation from schedule (on two concentration diagnostics only);\n8. a full account of what was and was not pre-registered, including declared incidents.')
rep('Section 6 reports results, including the sequence of studies.','Section 6 reports results, including the sequence of studies and the concentration-schedule study (Section 6.8).')
# cross refs
rep('not transfer to guiding NSGA-II mutation (Section 6.8)','not transfer to guiding NSGA-II mutation (Section 6.9)')
rep('Question 3 (does the effect transfer to another algorithm?): Section 6.8.','Question 3 (does the effect transfer to another algorithm?): Section 6.9.')
rep('Question 2 (is concentration the mechanism? does a sharpened probabilistic target reproduce the gain?): Sections 6.4 and 6.6.','Question 2 (is concentration the mechanism? does a sharpened probabilistic target reproduce the gain? is it the representation or the concentration schedule?): Sections 6.4, 6.6 and 6.8.')
rep('Sections 6.3 to 6.8 on one scale','Sections 6.3 to 6.9 on one scale')
rep('and 6.9 (summary).','and 6.10 (summary).')
rep('## 6.8 Transfer to NSGA-II','@@NEW68@@## 6.9 Transfer to NSGA-II')
rep('## 6.9 Summary of the confirmatory contrasts','## 6.10 Summary of the confirmatory contrasts')
rep('the independent evaluations (Section 6.7) in Tables 6 and 7; neither is drawn in it.','the independent evaluations (Section 6.7) in Tables 6 and 7 and the concentration-schedule study (Section 6.8) in Tables 8 and 9; none is drawn in it.')
# seeds
rep('Contrasts are paired within a study only:','The concentration-schedule study (Section 6.8) uses seeds 16000–16059 on the six benchmark geographies of the second evaluation (new seeds and new patient samples; calibration 16700–16714, technical tests 16900–16909). Contrasts are paired within a study only:')
# new section
def row(k,lab,reading): 
    v=C[k]; return '| %s | %s | %s | %s | %s | %s |'%(lab,f(v['mean']),ci(k),v['decision'],v['decision_bonferroni'],reading)
mk=lambda k:M[k]
def trow(k,lab):
    v=M[k]; return '| %s | %s | %.1f%% | %.3f | %.1f%% | %s | %.2f |'%(lab,v['schedule'].split('_',3)[3].replace('_',' to ',1).replace('_',' over ')+' generations' if False else lab[1],v['rel_entropy_gap_mean_over_gens']*100,v['abs_qmax_gap_mean_over_gens'],v['max_rel_entropy_gap']*100,'yes' if v['conform'] else 'no',v['profile']['effective_distribution_gen150']['js'])
sch={'w=0.3':'3→6, 90 gen.','w=0.7':'3→6, 30 gen.'}
def trow(k):
    v=M[k]; w='w = '+k.split()[0][2:]; ref=k.split()[-1]
    return '| %s | %s | %s | %.1f%% | %.3f | %.1f%% | %s | %.2f |'%(w,ref,sch[k.split()[0]],v['rel_entropy_gap_mean_over_gens']*100,v['abs_qmax_gap_mean_over_gens'],v['max_rel_entropy_gap']*100,'yes' if v['conform'] else 'no',v['profile']['effective_distribution_gen150']['js'])
new='''## 6.8 Matching the concentration trajectory: representation or schedule?

**Purpose.** In the earlier comparisons the evidential target concentrates on a schedule of its own (Dempster's rule sharpens as the non-dominated individuals agree), whereas the sharpened probabilistic target Dg uses one fixed exponent for all 150 generations; a difference between them therefore mixes representation and schedule. This study replaces the fixed exponent by an exponent that varies in time, $\\gamma_t=g_0+(g_1-g_0)\\min\\{1,(t-1)/(G_s-1)\\}$ at generation $t$, applied to the simple probabilistic target and renormalised with the same floor (0.02); the resulting target is denoted Dgt. A constant ramp ($g_0=g_1$) reproduces Dg bit for bit (tested). The protocol was written before any calibration or run.

**Design.** Geographies, sizes, generator and search engine are those of the second independent evaluation (six benchmark geographies, 50 patients, 10 teams), with new seeds (16000–16059, 60 per geography, 360 instances) and new patient samples; the geographies are therefore *not* independent of the second evaluation. The schedule was selected once per source strength and per reference target (E or DA, λ = 1, σ = 0.7) without reading hypervolume, on other seeds (16700–16714; geographies X, Golden and ORTEC) from 12 candidates ($g_0\\in\\{1,3\\}$, $g_1\\in\\{6,10,16\\}$, $G_s\\in\\{30,90\\}$): among the candidates that satisfied a gate on the whole trajectory (mean over generations 1–150 of the relative entropy gap ≤ 10% and of $|\\Delta q_{\\max}|$ ≤ 0.05), the one minimising the sum of the mean squared relative entropy gap and of the mean squared $\\Delta q_{\\max}/0.05$; if none satisfied the gate, the best attempt was kept and declared. The gate was satisfied in calibration for three of the four (strength, reference) pairs, and not for w = 0.7 with the DA reference. The same schedule was selected for E and for DA at each strength, so there are two Dgt arms, one per source strength. Whether the match holds was verified on the evaluation instances, without recalibration (Table 9). Twelve arms were run (E, DA, Dp, Dgt and the fixed Dg with γ = 6, at w = 0.3 and w = 0.7), with the oracle hypervolume, the budget of 6,040 evaluations and the decision rules of the other studies (per-seed mean over the six geographies, paired bootstrap B = 20,000, 99% marginal intervals, margin 0.005; the Bonferroni intervals for the five contrasts of each strength are given as a sensitivity analysis). The pre-registered reading was conditional on the conformity of the trajectory: with a conforming match, a superior E (or DA) would mean that an advantage of the representation or of the dynamics is not explained by the schedule alone; a superior Dgt, that a probabilistic schedule does better than Dempster's rule; a non-conforming match would make the contrast descriptive only.

**Table 8.** Concentration-schedule study (60 seeds, six benchmark geographies; paired differences in oracle hypervolume; 99% intervals; margin 0.005). "Bonf." is the decision with Bonferroni intervals (m = 5 per source strength). L2 at w = 0.7 is descriptive (the match was not conforming for the DA reference).

| Contrast | Difference | 99% interval | Decision | Bonf. | Reading |
|---|---|---|---|---|---|
'''
new+='\n'.join([
 row('L1 E-Dgt_E w=0.3','L1: E − Dgt, w = 0.3','E better than the scheduled probabilistic target'),
 row('L2 DA-Dgt_DA w=0.3','L2: DA − Dgt, w = 0.3','same'),
 row('L3 DA-E w=0.3','L3: DA − E, w = 0.3','equivalent'),
 row('L4 DA-Dp w=0.3','L4: DA − Dp, w = 0.3','large advantage over Dp'),
 row('L5 DA-Dg6 w=0.3','L5: DA − Dg(6), w = 0.3','fixed γ = 6 better'),
 row('L1 E-Dgt_E w=0.7','L1: E − Dgt, w = 0.7','scheduled probabilistic target better'),
 row('L2 DA-Dgt_DA w=0.7','L2: DA − Dgt, w = 0.7 (descriptive)','not interpretable as a separation'),
 row('L3 DA-E w=0.7','L3: DA − E, w = 0.7','equivalent'),
 row('L4 DA-Dp w=0.7','L4: DA − Dp, w = 0.7','large advantage over Dp'),
 row('L5 DA-Dg6 w=0.7','L5: DA − Dg(6), w = 0.7','equivalent')])
new+='''

**Table 9.** Match of the concentration trajectory on the evaluation instances (no recalibration). The first three numeric columns compare the Dgt arm with its reference target over generations 1–150; the last is the Jensen–Shannon divergence (base 2, maximum 1) between the effective decoded distributions of the two arms at generation 150, averaged over the 360 instances.

| Source strength | Reference | Schedule of $\\gamma_t$ | Mean relative entropy gap | Mean $|\\Delta q_{\\max}|$ | Largest relative entropy gap | Conforming | JS at generation 150 |
|---|---|---|---|---|---|---|---|
'''
new+='\n'.join(trow(k) for k in M)
new+='''

**Results.** Mean hypervolumes were, at w = 0.3, %.4f (E), %.4f (DA), %.4f (Dp), %.4f (Dgt) and %.4f (Dg with γ = 6); at w = 0.7, %.4f, %.4f, %.4f, %.4f and %.4f; levels are not comparable with other studies. The large advantage of DA over Dp was again present at both strengths (L4 = %s and %s), and DA and E were equivalent (L3). The match of the trajectory was conforming for E at both strengths and for DA at w = 0.3, and not conforming for DA at w = 0.7 (mean relative entropy gap 21.7%%, mean $|\\Delta q_{\\max}|$ = 0.061, growing after generation 50). At w = 0.3 the evidential target was better than the scheduled probabilistic target (L1 = %s, 99%% CI %s; L2 = %s, 99%% CI %s), in four of the six geographies (smaller or negative on X and H), and the Bonferroni intervals gave the same decisions. At w = 0.7 the sign reversed: the scheduled probabilistic target was better than E (L1 = %s, 99%% CI %s) in each of the six geographies; this is the contrast with a conforming match. The corresponding contrast for DA (L2 = %s) is descriptive. The fixed exponent γ = 6, which was not calibrated to the evidential trajectory, was better than DA at w = 0.3 (L5 = %s) and equivalent to it at w = 0.7.

**Reading.** At the reference strength, where the trajectory match was conforming for both references, the evidential target remained better than a probabilistic target that concentrates on the same schedule of entropy and maximum probability, so in this design the advantage of E over this probabilistic target is not explained by the schedule of these two diagnostics alone; it may come from the representation, from other features of the dynamics that the match does not control, or from the particular schedule. At the high strength the conclusion was the opposite: with a conforming match, the probabilistic schedule did better than Dempster's rule. A fixed exponent of 6 was better than the scheduled target at w = 0.3, which shows that the form of the schedule selected by the gate (a slow ramp from 3 to 6 over 90 generations) is not the one that gives the best hypervolume. Taken together with the second evaluation (the same geographies; DA − Dg(4) = +0.0090 and DA − Dg(4) = −0.0032 at the two strengths), the evidential target compares favourably with a moderately sharpened probabilistic target at w = 0.3 and not at w = 0.7, and neither with the best fixed exponent. No general advantage or disadvantage of the evidential representation follows.

**Limits of the match.** The gate controls two scalar summaries of the mean concentration per generation. The effective decoded distributions of the matched arms remained far apart at generation 150 (JS between 0.17 and 0.33, and an L1 distance between 0.74 and 0.96 out of a maximum of 2), so the arms are not equivalent in distribution. The schedule family has three parameters and was selected on three geographies; the gate failed for one of the four pairs, the two Dgt arms are the same arm for the two references, the geographies are those of the second evaluation, and only one algorithm and one evidence generator are used. These results are conditional on this design.

'''%(H['E_w0.3'],H['DA_w0.3_s0.7'],H['Dp_w0.3'],H['Gt_w0.3_E_3_6_90'],H['Dg_w0.3_g6'],H['E_w0.7'],H['DA_w0.7_s0.7'],H['Dp_w0.7'],H['Gt_w0.7_E_3_6_30'],H['Dg_w0.7_g6'],f(C['L4 DA-Dp w=0.3']['mean']),f(C['L4 DA-Dp w=0.7']['mean']),f(C['L1 E-Dgt_E w=0.3']['mean']),ci('L1 E-Dgt_E w=0.3'),f(C['L2 DA-Dgt_DA w=0.3']['mean']),ci('L2 DA-Dgt_DA w=0.3'),f(C['L1 E-Dgt_E w=0.7']['mean']),ci('L1 E-Dgt_E w=0.7'),f(C['L2 DA-Dgt_DA w=0.7']['mean']),f(C['L5 DA-Dg6 w=0.3']['mean']))
rep('@@NEW68@@',new)
# discussion
rep('**What it does not show.**','''**Representation or schedule.** A last pre-registered study (Section 6.8) replaced the fixed exponent of the probabilistic target by a schedule that follows the evidential trajectory of entropy and maximum probability. The result depends on the source strength: at w = 0.3 the evidential target was better than the scheduled probabilistic target (E − Dgt = %s), at w = 0.7 it was worse (%s), and a fixed exponent of 6 was better than both at w = 0.3. The schedule therefore does not explain away the evidential advantage at w = 0.3 in this design, but there is no consistent advantage of the representation across source strengths, and the match was on two diagnostics only (decoded distributions remained far apart); the study does not establish a representation effect independent of concentration, nor exclude it.

**What it does not show.**'''%(f(C['L1 E-Dgt_E w=0.3']['mean']),f(C['L1 E-Dgt_E w=0.7']['mean'])))
rep('The concentration of the evidential target is adaptive (it grows with agreement among the sources), while that of Dg is fixed by the exponent;','The concentration of the evidential target is adaptive (it grows with agreement among the sources), while that of Dg is fixed by the exponent (Section 6.8 tests a scheduled exponent, but matches only two diagnostics);')
# limitations
rep('17. **No novelty claim.**','19. **No novelty claim.**')
rep('16. **No real home-care data.**','18. **No real home-care data.**')
rep('15. **Independent evaluations.**','16. **Independent evaluations.**')
rep('14b. **Objective function.**','15. **Objective function.**')
rep('18. **No real home-care data.**','17. **Concentration-schedule study.** The schedule family has three parameters and was selected on three geographies; the trajectory match covers two scalar diagnostics and the decoded distributions remained far apart; the gate was not satisfied for one of the four pairs; the two scheduled arms are the same arm; the geographies are those of the second evaluation (new seeds and patient samples); the sign of the main contrast changed with the source strength.\n18. **No real home-care data.**')
# conclusion
rep('Perspectives: a design','A final pre-registered study separated, as far as two concentration diagnostics allow, the representation from the concentration schedule by giving the probabilistic target an exponent that varies in time. With a conforming match, the evidential target was better than the scheduled probabilistic target at w = 0.3 and worse at w = 0.7, and a fixed exponent of 6 was better than both at w = 0.3, so the data support neither a general evidential advantage nor a general disadvantage once the schedule is taken into account; decoded distributions of the matched arms remained far apart.\n\nPerspectives: a design')
# appendix A
rep('- Several background-monitoring time-outs occurred;','- Concentration-schedule study: the first launch of the automatic chain stopped at the dry run of the analysis because the analysis script read a parameter key that did not exist (the parameter file stores the schedules); the script was corrected, and trajectory-profile and decoded-distribution diagnostics were added, both before the freeze and before any hypervolume of the main run existed; the chain was relaunched; a detached launch of the main run started by mistake was stopped and replaced by a monitored background run with the same frozen code; the calibration gate was not satisfied for w = 0.7 with the DA reference (best attempt, declared) and the match was not conforming on the evaluation instances for that pair; the pilot (seeds 16900–16909) showed no technical problem; no rerun.\n- Several background-monitoring time-outs occurred;')
# appendix B
rep('**Scenarios of Section 6.7.**','**Scenarios of Sections 6.7 and 6.8.**')
rep('Three main seed ranges are used:','The concentration-schedule study (Section 6.8) uses seeds 16000–16059 on the six geographies of Table B2 (calibration 16700–16714, technical tests 16900–16909); its additional arm Dgt is defined in Section 6.8. Three main seed ranges are used:')
# glossary
rep('**Targets of Section 6.6.**','**Targets of Section 6.8.** Dgt: the simple probabilistic target raised to a time-varying exponent $\\gamma_t$ (linear ramp from $g_0$ to $g_1$ over $G_s$ generations, then constant), renormalised with the floor 0.02; ξ: a world of adequacies and satisfactions (Section 3.1); ω: weight of evidence.\n\n**Targets of Section 6.6.**')
open('Paper_v0_9.md','w').write(s); print(len(s.split()),s.count('AUTHOR TO'))
