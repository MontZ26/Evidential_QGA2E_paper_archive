# Protocol P4 (follow-up of P3): does adding quantum-inspired crossover and mutation to the two-amplitude QGA close the gap with NSGA-II?
**v0.5, 7 November 2026 (v0.4.1 plus the sample-size amendment of section 9d, written after the pilot and before the freeze; see sections 5 and 9d). Code, technical tests, tuning and pilot have been run under the author's written authorisation of 7 November 2026 (20:30 Tunis, 'toute la chaine'; n = 300 chosen by the author at 22:08). Nothing is frozen, no code is written, no experiment is run. Every item is [P] until the author confirms it in writing. Code, tuning/pilot, freeze and confirmatory run need the author's written authorisation. The GitHub repository is not touched.**

## 0. Status and disclosure
- Origin: in P3 (frozen protocol v1.1, 100 confirmatory seeds) the rotation-only QGA2 and QGA2-E were beaten by NSGA-II (hypervolume differences -0.017 and -0.148). Neither has crossover or mutation. P4 asks whether adding them changes this.
- **P4 is motivated by P3's results (post hoc as to the idea) but is itself pre-registered**: new seeds, one primary variant fixed in advance, hypotheses and analysis written before any code. It does not replace, re-run or reinterpret P3, whose conclusions stand whatever P4 finds. The paper must say that P4 was designed after seeing P3, report both studies, and state how many algorithm variants were tried in total (P3: 2 QGA variants; P4: 1 primary and the descriptive ones below).
- Legend: [INHERITED] from P3 (code and rules frozen in `p3_freeze.txt`, reused unchanged); [P] proposal.
- Pasted external reviews are not authorisations.
- **Required statement in the paper**: "This follow-up study was designed after the results of P3 had been observed. Its hypotheses, primary algorithmic variant, new random seeds and analysis plan were specified before the implementation and the confirmatory experiments of P4." P4 is not an independent replication of P3. The SHA-256 of this protocol version is recorded, with its date, before any code is written.

## 1. Question
Under deterministic information and an equal budget of 6 040 evaluations, can a two-amplitude QGA that uses, besides the rotation gate, angle-level crossover and mutation (inspired by the Q-bit representation, by analogy only) compete with NSGA-II, and does it improve on the rotation-only QGA2-E?

## 2. Algorithms [P]
**Common [INHERITED from P3]**: the problem and the three objectives (all minimised, in [0,1], reference point (1.2, 1.2, 1.2), exact 3D hypervolume, world T), POP = 40, 150 generations, budget 40 + 150 x 40 = 6 040, mask M, decoder `collapse_r(theta, M, ux, ur)`, the common initial population of `p3.init_qga`, survival `select_next` (80 to 40), individual record (theta, x, r = (ux, ur), f), output = first front of the final population re-evaluated by `final_front`. **Budget accounting**: the search budget counts the calls to `evaluate()` made by the algorithm itself (6 040; MOEA/D 6 030, declared). The re-evaluation of the output by `final_front` and the diagnostic evaluations (convergence, diversity) use the uncounted evaluator; they are not part of the search budget (this is how P3 was run). The diagnostic procedures are applied consistently to the algorithms and subsets of seeds specified for each diagnostic (diversity: QGA2, QGA2-E, QGA-XM-E, NSGA-II; convergence: first 20 confirmatory seeds). Their actual evaluation counts are recorded separately. Descriptive runtime = wall-clock time of the search loop only, excluding `final_front` and the diagnostics (timer paused during them), measured with the same number of concurrent processes for all algorithms. (P3 runtimes had included `final_front` and, on the first 20 seeds, the convergence diagnostics; they are descriptive only.)

### 2.1 QGA-XM-E (primary) — one generation, in this order
Let the current population be in the order returned by the last survival (generation 0: after the initial `select_next` 40 to 40, as in QGA2-E). Fixed at the start of the generation, and not changed while the 40 children are built: **best** = the first individual (lowest index) of the first non-dominated front of the current population.
For child c = 0..39, in this order:
1. **Parents**: a and b by two binary tournaments (two indices drawn uniformly with replacement; lower rank wins; equal rank: larger crowding wins; equal crowding: coin flip) [INHERITED functions `p2s2.rank_crowd`, `p2s2._tour`].
2. **Angle crossover**: **one Bernoulli draw per child** with probability p_c = 0.9 (fixed, not tuned), on the "xm_cross" stream. If it succeeds, **one independent draw per patient** (probability 0.5 each) decides whether the row theta[p, :] comes from parent a or from parent b; if it fails, all rows come from a. Parents are never modified. (Same structure as the uniform crossover of the P3 NSGA-II, checked in the frozen `p3.py`, function `vary`: one Bernoulli draw per child with probability p_c, then one draw per patient with probability 0.5, the unit being the patient; failure gives a copy of parent a. The P4 operator acts on angle rows, the P3 one on team indices.)
3. **Rotation** (the QGA2 gate, applied to the whole crossed array): with yo = one-hot(x_a) (the decoded assignment of **parent a for every row, including rows copied from b** — a declared asymmetry), bo = one-hot(x_best), s = bo (1 - yo) - (1 - bo) yo, theta <- clip(theta + delta s, 0, pi/2) x M. Rows where x_a and x_best agree are unchanged; ties cannot occur.
4. **Quantum mutation**: each patient with at least 2 allowed teams is mutated independently with probability pmk/n_p; a mutated patient swaps the angles of two distinct allowed teams chosen uniformly among the unordered allowed pairs. Patients with fewer than 2 allowed teams cannot mutate (their probability is not redistributed). Forbidden cells stay exactly 0 and angles stay in [0, pi/2] (a swap keeps both). The expected number of mutated patients per child is pmk x (share of mutable patients); the probability of at least one mutation per child is 1 - (1 - pmk/n_p)^(mutable patients), not pmk/n_p. A swap of two equal angles changes nothing. For every algorithm that mutates and every instance the following are recorded: the number of mutable patients, the number of patients selected for mutation, the number of effective mutations (swaps that change theta) and the number of no-effect swaps (equal angles), so that an absence of gain can be attributed to the operator or to a low effective mutation rate.
5. **Decoding**: draws (ux, ur) from the continuing "evo" stream, `collapse_r`; evaluation (one call).
After the 40 children: survival by `select_next` on the 80 records (40 parents then 40 children) to 40. Children become parents with their own theta, draws and stored x; nothing is re-decoded or re-evaluated, and the draws are kept only as traces for the invariant test. The term "quantum" is used by analogy with the Q-bit representation; the operators are not physical quantum operators.

### 2.2 Random streams
Instance: built from (scenario, seed) only. Initial population: streams "init" and "evo" as in P3. The identity required is on the **decoded initial assignments**, which are the same for every algorithm: the QGA family also shares the generating angles, objective vectors and decoding draws (QGA-XM-E and QGA2-E individual by individual); NSGA-II starts from those same decoded assignments (it has no angle representation, so there is no conversion rule beyond using x); MOEA/D uses those 40 assignments plus 5 more drawn by the same procedure. No claim of identical chromosomes across different representations is made. Operators use their own named streams, never the "evo" stream: "xm_tour", "xm_tie", "xm_cross", "xm_mut"; only the decoding draws use "evo". Changing an operator's probability therefore never changes another operator's or the decoder's random numbers.

### 2.3 Reference algorithms
Recomputed on the new seeds with the P3-tuned parameters from `p3_tuned.json`, no re-tuning: QGA2 (delta 0.025 pi), QGA2-E (delta 0.1 pi), NSGA-II standard (elitist, J1), NSGA-II paired (generational, J1; the two NSGA-II differ only by replacement, 80 to 40 versus 40 children), MOEA/D (T = 20; 45 Das-Dennis vectors H = 8, p_c 0.9, p_m 1/n_p, 2 replacements, neighbourhood probability 0.9, 6 030 evaluations).
MOEA/D is a reference algorithm at its inherited budget, 10 evaluations (0.17 percent) below the others, and is not presented as a strictly equal-budget comparison. The paper's equal-budget statements concern only the algorithms receiving 6 040 evaluations (QGA2, QGA2-E, QGA-XM-E and its variants, NSGA-II both versions).

### 2.4 Descriptive variants (ablations; parameters inherited from the chosen QGA-XM-E set, not individually tuned; no confirmatory test)
| Variant | Parent selection | p_c | p_m | Replacement | Rotation |
|---|---|---|---|---|---|
| QGA-T-E | tournament | 0 | 0 | elitist | yes |
| QGA-M-E | tournament | 0 | pmk/n_p | elitist | yes |
| QGA-X-E | tournament | 0.9 | 0 | elitist | yes |
| QGA-XM-G | tournament | 0.9 | pmk/n_p | generational (40 children, reordered by `select_next`) | yes |
| QGA-XM-E, delta = 0 | tournament | 0.9 | pmk/n_p | elitist | no |
QGA-T-E isolates the effect of tournament parent selection, which differs from QGA2-E (child i built from parent i). H-4.2 therefore compares QGA2-E with an algorithm that differs in three components (selection, crossover, mutation), and the ablations are what allows the paper to attribute any difference. Reading rules (descriptive): QGA-T-E versus QGA2-E = effect of tournament selection in this configuration; QGA-X-E versus QGA-T-E = effect of crossover given tournament selection; QGA-M-E versus QGA-T-E = effect of mutation given tournament selection; QGA-XM-E versus QGA-X-E and QGA-M-E = value of combining both. These contrasts are not a complete factorial design and do not allow all interactions to be estimated, so causal attribution must stay cautious.

### 2.5 Diversity (descriptive)
For the population at generations 0, 50, 100, 150 of QGA2, QGA2-E, QGA-XM-E and NSGA-II: mean normalised Hamming distance between the **complete decoded assignments**, D_H = 2/(N(N-1)) x sum over pairs of (number of differing patients)/n_p, over all 780 pairs (identical assignments count as distance 0), plus the number of distinct assignments. It is not a selection criterion.

## 3. Tuning [P]
Rule written here, before any tuning: 20 tuning seeds (4610-4629), world T; criterion = mean over the seeds of the per-seed mean over the six scenarios of the HV of the output; a seed counts only if its six scenarios are feasible. Three sets of (delta, pmk): S1 = (0.05 pi, 1) **a priori reference**, S2 = (0.05 pi, 2), S3 = (0.025 pi, 1). S2 and S3 are compared with S1; if the best of the three exceeds S1 by less than 0.001, S1 is kept; otherwise the set with the highest criterion is kept; ties go to S1. p_c stays 0.9. No added set, no second pass.

## 4. Hypotheses [P]
Primary family: 3 two-sided paired Wilcoxon tests (zero_method "wilcox"; p = 1 if all differences are zero or fewer than 6 are non-zero), Holm, alpha = 0.05. **Single primary measure**: the per-seed mean over the six scenarios, with equal weights, of the true-world hypervolume, HV_i(A) = (1/6) sum_s HV_{i,s}(A); objectives are bounded in [0,1] with the same reference point in every scenario (as in P3), so the average is comparable across scenarios. Difference convention D_i = HV_i(QGA-XM-E) - HV_i(reference): positive = advantage of QGA-XM-E.
- H-4.1: QGA-XM-E versus NSGA-II standard.
- H-4.2: QGA-XM-E versus QGA2-E.
- H-4.3: QGA-XM-E versus QGA2.
Effect sizes, interpretation rule and "no equivalence margin" as in P3: a non-significant result is reported as "no difference detected", never as equivalence; superiority and inferiority are reported as such. IGD+, runtime, convergence (first 20 confirmatory seeds), diversity and the ablations are descriptive only. The primary variant is fixed; none is chosen after results.

## 5. Seeds and sample size [P]
Technical tests and pilot 4600-4609; tuning 4610-4629; confirmatory 4700 to 4700 + n - 1 (at most 4999). Disjoint from all earlier seeds. The pilot serves only to size n; it does not choose the variant or change any hypothesis.
**Order of phases**: (1) technical tests at the a priori set S1; (2) tuning on 4610-4629; (3) pilot on 4600-4609 **with the QGA-XM-E set chosen by the tuning**, so the dispersion used for sizing is that of the algorithm finally evaluated; (4) freeze; (5) confirmatory run; (6) analysis, once. The reference algorithms use their P3 parameters.
Sizing. The planning difference is written Delta_HV = 0.01 (delta is the rotation step). Target: a **location shift of Delta_HV in the paired differences, detected by the two-sided Wilcoxon test** at level 0.05/3 with power 0.80 (planning convention, not an established effect).
- Formula n_f = ceil(((z_{1-alpha'/2} + z_power) sd_up / Delta_HV)^2), alpha' = 0.05/3, z = 2.394 + 0.842, sd_up = s sqrt((n_p - 1)/chi2_{0.20}(n_p - 1)) = the 80 percent one-sided upper confidence bound of the standard deviation of the paired differences (normal-theory chi-square), largest value over the three contrasts. It is a preliminary normal-approximation estimate, not a validation of power.
- **Simulation always run** (not only when the distribution diagnostics trigger, because they are unreliable with 10 seeds): 1 500 resamples of size n of the pilot differences, centred at their median and shifted by Delta_HV, Wilcoxon at 0.05/3 (zero differences dropped as in the test); n_s = smallest n of the grid {100, 150, 200, 300} with power >= 0.80 for the three contrasts.
- n = the smallest grid value >= max(n_f, n_s); stop and report if this exceeds 300. [v0.5 amendment, section 9d: the pilot ended in this stop; the author fixed n = 300.] The simulated power is an exploratory estimate conditional on the empirical distribution of 10 pilot differences, not on new independent observations; its Monte-Carlo standard error (about 0.010 at power 0.80 with 1 500 resamples) is reported with it, and if a simulated power lies within two standard errors of 0.80 this is stated together with the sensitivity to the pilot values (the selection rule itself is not changed). The result is a sample-size estimate from a 10-seed pilot, not a guarantee of power; the zeros/skewness/kurtosis diagnostics are reported.
Failure cases: (a) infeasible instance: whole seed excluded for all algorithms; (b) technical failure: recompute, exclude only if impossible; (c) algorithmic failure: never excluded, HV = 0 counted.

## 6. Technical tests [P]
Those of P3 that apply: feasibility against M; exact budgets (6 040; MOEA/D 6 030); determinism; invariant (collapse_r(theta, M, ux, ur) = x for every surviving record); survival input 80, output 40; common initial population; parents are not evaluated again; hypervolume and reference point. Added:
- **Equivalence test**: the implementation has a parent-selection switch ("tournament" or "index"). With the switch on "index" (child c built from parent c) and p_c = p_m = 0, QGA-XM-E reproduces QGA2-E **exactly**: identical theta, x and f for every individual at every generation for several generations, same initial state, same streams. (With tournament selection the two cannot be equal, which is why QGA-T-E exists.)
- Operators: same input and same streams give the same output; crossover leaves the parents unchanged and takes each row only from a or b; with p_c = 0 the child equals a's theta before rotation; mutation exchanges two angles of distinct allowed teams only, keeps the multiset of angles of the row, keeps forbidden cells at 0 and angles in [0, pi/2]; a patient with 0 or 1 allowed teams is never mutated; rotation precedes mutation (checked on a constructed case); best is the same for the whole generation; the delta = 0 variant performs no rotation; the number of mutable patients per instance is reported.
- **Initial state**: at generation 0 the angles, decoded assignments, objective vectors and decoding draws of QGA-XM-E (all variants) and of QGA2-E are identical, individual by individual; NSGA-II and MOEA/D start from the same decoded initial assignments (the first 40 for MOEA/D).
- **Streams**: each named stream is created reproducibly from (scenario, seed, name); the order of use is stable (same call sequence gives the same numbers); two independence checks on the decoding draws of the first generation: (i) two different p_c at the same p_m, (ii) two different p_m at the same p_c; in both the "evo" draws must be identical.
- **Non-regression against P3**: QGA2, QGA2-E and NSGA-II of P4 reproduce the stored P3 fronts of `p3_pilot.json` (three instances: S4-RC101, S5-R101, S4-C101, seed 4200 — not confirmatory data) with exact equality of the assignments and fronts equal to 1e-12, using the parameters of `p3_tuned.json`.
Failures are reported, not bypassed.

## 7. Analysis, limits, conduct
Analysis script adapted from `an_p3_final.py` (primary contrasts above, pairwise differences with bootstrap CI of 5 000 whole-seed replicates, rank-biserial, IGD+ against the pooled non-dominated front of all runs of the job, runtime, convergence, diversity, ablations), written and tested on pilot and synthetic data before the run, run once; absolute paths; atomic writes.
Limits: one operator design (row crossover with parent-a reference, angle-swap mutation) among many, and the asymmetry of the reference in the rotation is a design choice, not a neutral one; the selection mechanism differs from QGA2-E (handled by QGA-T-E); three tuning sets; same problem family, fixed visit order and decoder as P3; operators are quantum-inspired by analogy and their literature precedents have not been verified source by source. The conclusion is limited to this family of problems and this design of QGA; no general claim about quantum-inspired algorithms.
Conduct: no change after results; no re-run to improve a result; SHA-256 freeze; negative results reported; no promise of acceptance.

## 8. Decisions needed from the author
1. Framing: follow-up study with the disclosure of section 0.
2. Operator definitions (section 2.1), including the parent-a reference in the rotation. Alternative, not retained: use the source parent of each row as the reference.
3. Primary variant QGA-XM-E, three hypotheses, Holm.
4. Tuning sets S1-S3 and the written rule.
5. Seed ranges and the sizing rule of section 5 (always-simulated Wilcoxon power, pilot run with the tuned set).
6. Descriptive ablations (now including QGA-T-E) and the diversity measure.
7. Written authorisation for code and technical tests, then (in one message, as for P3, or separately) tuning, pilot, freeze, confirmatory run and analysis.

## 9d. Changes in v0.5 (amendment AFTER the pilot, BEFORE the freeze and any confirmatory run)
- Pilot result (seeds 4600-4609, QGA-XM-E at the tuned set S1): n_f = 92 (grid value 100); simulated Wilcoxon power for a +0.01 location shift = 0.96 (H-4.1) and 1.00 (H-4.2) at n = 100, but 0.07 (n = 100) to 0.19 (n = 300) for H-4.3. The rule of section 5 therefore ended in STOP (n > 300).
- Cause: the 10 pilot differences of H-4.3 are asymmetric and all negative (mean -0.051); after median centring, a +0.01 shift leaves the signed-rank statistic almost unchanged. The pilot shows no positive effect of QGA-XM-E to detect.
- Amendment decided by the author: n = 300 for all three hypotheses (seeds 4700-4999, the maximum allowed). The stop rule is NOT applied; this is a deviation from the written rule, decided after seeing the pilot, and must be reported as such. H-4.3 is under-powered for a +0.01 advantage of QGA-XM-E over QGA2; no equivalence claim will be made.
- Nothing else changes: hypotheses, variants, tuning rule and set (S1 chosen: criteria S1 0.5156, S2 0.5161, S3 0.5007; S2 gains 0.0005 < 0.001), budget, analysis.
- Reconstruction disclosure: the original run_p1m.py and ablation_loo.py were unavailable; they were reconstructed (ablation_loo = loader of the P1 library run_main_experiment.py without its main loop; run_p1m = exact 3D hypervolume, verify_freeze). Verified: the nine P3 algorithms reproduce the stored P3 fronts to 1e-12 on three instances (non-regression) and the P3 contrast QGA2-E minus NSGA-II = -0.1475 is reproduced from stored fronts. This must be stated in the paper.

## 9c. Changes in v0.4.1
- Diagnostics wording made specific to each diagnostic (algorithms and seed subsets).
- Crossover statement verified against the frozen P3 code (patient-level unit confirmed) and made explicit.
- No hypothesis, variant, seed range, budget or tuning rule changed.

## 9b. Changes in v0.4
- Crossover made unambiguous: one Bernoulli draw per child, then one draw per patient.
- MOEA/D (6 030) declared as a reference algorithm, not strictly equal-budget.
- Initial population: identity defined on the decoded assignments across representations; test extended to NSGA-II and MOEA/D.
- Stream tests: both independences (p_c with p_m fixed, p_m with p_c fixed).
- Power simulation: exploratory, Monte-Carlo error reported, near-threshold rule of disclosure.
- Diagnostic evaluations counted separately; runtime defined as search time only.
- No hypothesis, seed range, budget, tuning set or primary variant changed.

## 9a. Changes in v0.3
- Budget accounting stated (search calls only; final-front and diagnostic evaluations uncounted and uniform).
- Pilot run with the tuned QGA-XM-E set (order of phases written); planning difference renamed Delta_HV; targeted effect = Wilcoxon location shift; the power simulation is always run and n = max of formula and simulation.
- Mutation counts to be recorded (mutable, selected, effective, no-effect).
- Reading rules for the ablations; required disclosure sentence; protocol hash recorded before code.
- Tests added: identical initial state QGA2-E / QGA-XM-E, reproducibility and independence of the random streams.
- No hypothesis, seed range, budget, tuning set or primary variant changed.

## 9. Changes in v0.2
- Rotation formula written out; the parent-a reference stated for all rows.
- Mutation fully defined (distinct allowed pairs, immobile patients, no redistribution, rate vs probability of at least one mutation, no-op swaps recorded).
- Equivalence test corrected: v0.1 claimed equality with QGA2-E at p_c = p_m = 0, which cannot hold with tournament selection; replaced by an exact test with a parent-selection switch, plus the new ablation QGA-T-E.
- Order of operations, fixed best and tie-break, random streams, HV definition and weighting, difference sign, sizing details, tuning rule, diversity formula, ablation table, MOEA/D and NSGA-II differences, non-regression tolerance (instances from the P3 pilot, not from confirmatory data) added.
- No hypothesis, seed range, budget or primary variant changed.
