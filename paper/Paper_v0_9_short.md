---
title: "Evidential versus Probabilistic Target Distributions in a Quantum-Inspired Multiobjective Genetic Algorithm: The Case of Home Health Care Team Assignment"
author: ["Dr Montassar Zaghdoud", "Manouba School of Engineering, Manouba University, Tunisia", "montassar.zaghdoud@mse.uma.tn"]
date: "15 November 2026"
---

# Abstract

Multiobjective team assignment in home health care must cope with uncertain affinities between patients and care teams. We ask whether aggregating population information with Dempster–Shafer evidence, rather than with a probabilistic frequency model, improves a quantum-inspired genetic algorithm, which can be read as a univariate model-based search. We report a sequence of studies whose contrasts, equivalence margins and decision rules were fixed before each run, using paired seeds, an oracle hypervolume measure and semi-synthetic instances built on benchmark geographies, with simulated hidden truth and evidence. The evidential target clearly outperformed the simple probabilistic target, but a probabilistic target sharpened by a power transformation did at least as well on the main instances, and sharpening the evidential target further degraded its performance. Refinements of the evidential structure brought no robust gain, and guiding the mutation of a classical algorithm with the same targets did not help. On two new families of instances, the advantage over the simple probabilistic target was reproduced, whereas the ordering against the sharpened target was not stable. A final study gave the probabilistic target a concentration schedule calibrated to follow that of the evidential target: the evidential target was better when the source strength was low and worse when it was high, and the calibration controlled only two concentration diagnostics. Classical multiobjective algorithms remained far better than all variants of the quantum-inspired algorithm. No representation advantage independent of concentration was established.

**Keywords:** home health care; multiobjective optimisation; quantum-inspired genetic algorithm; Dempster–Shafer theory; estimation of distribution algorithms; hypervolume.

# 1. Introduction

Home health care (HHC) organisations assign patients to care teams under competing objectives: travel effort, patient-side quality of service, and workload balance with skill adequacy (Braekers et al. 2016; Cissé et al. 2017; Di Mascolo et al. 2021; Fikar and Hirsch 2017; Rasmussen et al. 2012). The quality of a candidate assignment depends on quantities that are only partially known when the plan is built, such as the adequacy of a team for a skill or the satisfaction a team is expected to produce. Belief-function (Dempster–Shafer) models represent partial, imprecise and conflicting information, and can carry it into a search algorithm. Quantum-inspired evolutionary algorithms maintain, for each decision variable, a probability-like amplitude that is rotated towards good solutions; they can be read as model-based search schemes whose sampling distribution is parametrised by angles (Section 2.1).

This paper asks a narrow question. In one quantum-inspired genetic algorithm, QGA2-E, the amplitudes are rotated towards a *target distribution* built from the best individuals of the current population. The target can be built by a probabilistic frequency model, or by Dempster–Shafer evidence combined with Dempster's rule and converted to a probability by the pignistic transformation. We observed early on that the evidential target gives a better hypervolume than a simple probabilistic target. The question is why. Two explanations compete. The first is that the evidential *representation* carries something the probabilistic model does not. The second is that the evidential construction simply yields a *more concentrated* target, and that concentration, not representation, drives the gain. They make different predictions: if concentration is the mechanism, a probabilistic target sharpened by a power transformation should reproduce the gain, and sharpening the evidential target further should not help.

**Why study QGA2-E, which is not competitive?** QGA2-E keeps one angle vector per patient and rotates it towards a target; sampling is independent across patients, so the algorithm is a *univariate model-based search* in the family of estimation-of-distribution algorithms (EDAs), with a rotation update comparable to the probability-vector update of PBIL (Section 2.3). That structure makes the object of study explicit: the update direction is a single, inspectable distribution per patient, the *target*, which can be built in different ways and whose concentration can be measured and tempered. In a crossover-based algorithm the corresponding component (what bias a population imposes on new solutions) is spread over selection, recombination and mutation and cannot be isolated. We therefore use QGA2-E as a *testbed for target construction in model-based search*, not as a proposal to solve the home-care assignment problem: NSGA-II and MOEA/D, run at the same budget, are far better on every instance family (Section 6.1), and we make no claim of competitiveness. A plausible reason for the gap, which we did not test, is that a univariate model cannot represent dependences between the team choices of different patients, which crossover can exploit implicitly (Section 7); how to close the gap is outside the scope of this paper.

We formalise the two targets and their concentration (Section 4) and answer the question with a sequence of pre-registered experiments (Sections 5 and 6): a controlled comparison with paired seeds and an equivalence margin; a symmetric sharpening of both representations; refinements of the evidential structure; a transfer to NSGA-II; a dependence-degree and sensitivity study; two independent evaluations on new instance families; and a study that gives the probabilistic target the concentration schedule of the evidential one. The conclusions are limited: the results are compatible with an important role of concentration, they do not show that it is the only mechanism, and they do not show that the evidential representation can never help. NSGA-II and MOEA/D are far better at the same budget, so the study concerns a representation *inside* QGA2-E.

# 2. Related work

## 2.1 Quantum-inspired evolutionary algorithms

Han and Kim (2002) introduced a quantum-inspired evolutionary algorithm (QIEA) for combinatorial optimisation, where each variable has a Q-bit whose observation yields a binary value, and a rotation gate moves the amplitudes towards the best solution found; a later version added a termination criterion, a different gate and a two-phase scheme (Han and Kim 2004). Multiobjective extensions include a QIEA for multiobjective knapsack problems (Kim et al. 2006) and a framework with convergence conditions (Li and Rudolph 2007). In these algorithms a probability distribution over decisions is parametrised by angles; the update is a stochastic-approximation step towards a target. The QGA2 of this paper uses two amplitudes per team and a categorical observation (Section 4.1).

## 2.2 Dempster–Shafer theory

Dempster (1967) introduced upper and lower probabilities induced by a multivalued mapping and the rule of combination later formalised by Shafer (1976). The transferable belief model of Smets and Kennes (1994) separates credal and pignistic levels and defines the pignistic transformation used here to obtain a probability for decisions. Yager's variant (1987) transfers the conflicting mass to the whole frame instead of renormalising; it is used for the evidence on team–skill adequacy (Section 3.4). Denœux (2019) reviews decision-making with belief functions. Evidence theory has also been used to model epistemic uncertainty in design optimisation and reliability analysis (Agarwal et al. 2004; Mourelatos and Zhou 2006; Zhang and Jiang 2021) and, through the evidential reasoning approach, for multiple-attribute decision analysis (Yang and Xu 2002); these works concern the evaluation of solutions or the ranking of alternatives. Their positioning relative to target aggregation in model-based search is summarised in Section 2.4.

## 2.3 Estimation of distribution algorithms and concentration

Estimation-of-distribution algorithms (EDAs) replace crossover and mutation by sampling from a probabilistic model estimated from selected individuals; Baluja's PBIL (Baluja 1994) keeps a probability vector updated towards the best individuals, and Hauschild and Pelikan (2011) survey the field (see also the book of Larrañaga and Lozano (2002)). A recurrent theme is the loss of diversity: Shapiro (2005) shows that the finite sampling and selection of EDAs produce drift that drives the model to a degenerate distribution, with consequences for scalability. The *concentration* of the sampling distribution (its entropy or its maximum probability) is therefore a central control parameter of such algorithms. In Section 4.3 we show that the power transformation used to sharpen targets is a tempering whose inverse temperature is the exponent, which puts concentration on an explicit one-parameter scale. QGA2-E belongs to this family: it keeps a separate distribution for each patient (a univariate model) and moves it towards a target built from the non-dominated individuals, so the way the target is built, and how concentrated it becomes over time, is the part of the algorithm that decides how fast the model degenerates.

## 2.4 Positioning

The question addressed is whether, when an evidential target outperforms a probabilistic one in a model-based search, the advantage comes from the representation or from the concentration it induces, and, more finely, whether it comes from the representation or from the *schedule* on which the target concentrates (Dempster's rule sharpens adaptively as agreement grows; a power transformation of a frequency model sharpens by a fixed amount). We study this in a univariate model-based search (an EDA-like algorithm), on a stylised home-care assignment problem with simulated information, with a design that sharpens both targets by the same operation, matches concentration where possible, and reports pre-registered contrasts, including inconclusive and negative ones. The contribution is a controlled comparison and a documented set of negative results about when the evidential representation does not help, not a new competitive algorithm. In the literature reviewed in Sections 2.1–2.3, belief functions in optimisation address uncertain objective evaluations or post-optimisation decision analysis (Agarwal et al. 2004; Mourelatos and Zhou 2006; Yang and Xu 2002; Zhang and Jiang 2021), whereas estimation-of-distribution and quantum-inspired algorithms update their sampling models from probabilistic frequencies or amplitude vectors (Baluja 1994; Han and Kim 2002; Han and Kim 2004; Hauschild and Pelikan 2011; Kim et al. 2006; Larrañaga and Lozano 2002; Li and Rudolph 2007; Shapiro 2005). Within the scope of this targeted review, the present study provides a controlled comparison, with pre-specified decision rules, of evidential versus probabilistic target aggregation inside a univariate model-based search after matching concentration and annealing schedules.

# 3. Problem, instances and information model

## 3.1 Decision space

*Notation.* A *world* of adequacies and satisfactions is written $\xi=(A,S)$; the symbol $\omega=-\ln(1-w)$ is reserved for the weight of evidence of a source (Section 4.2).

Let $\mathcal P=\{1,\dots,n_p\}$ be the patients and $\mathcal T=\{1,\dots,N_T\}$ the $N_T$ teams. Each patient $p$ requires a set of skills $\mathrm{need}_p\subseteq\{1,\dots,5\}$; team $t$ is certified for a skill set given by a binary matrix $C\in\{0,1\}^{N_T\times 5}$. The formulation allows sets of skills; in the generated instances each patient requires exactly one skill ($|\mathrm{need}_p|=1$, Section 3.4). The mask $M_{pt}=1$ iff $C_{tk}=1$ for all $k\in\mathrm{need}_p$, and $\mathcal A_p=\{t:M_{pt}=1\}$ is the set of allowed teams, of size $K_p$. A solution is an assignment $x\in\prod_p\mathcal A_p$. Each team visits its patients in increasing patient index (fixed visit order); the visit sequence is not optimised, so the problem is assignment with a fixed order, not integrated routing. Team 0 is an ordinary team except in instance generation, where it is used as a technical device (Section 3.4).

## 3.2 Schedule and objectives

For team $t$ let $\mathcal V_t=\{p_1<\dots<p_m\}$ be its patients, $D$ the travel-time matrix with depot $0$, $[e_p,l_p]$ the time window of $p$, $v$ the visit duration and $T_{\mathrm{end}}$ the day end. Arrival at $p_j$ is
$$a_{p_j}=\max\{e_{p_j},\;c_{j-1}+D(p_{j-1},p_j)\},\qquad c_j=a_{p_j}+v,$$
with $c_0=0$ and $p_0$ the depot. The route length is $rl_t=\sum_j D(p_{j-1},p_j)+D(p_m,0)$ (waiting is not counted). The three objectives, all in $[0,1]$ and all minimised, are
$$f_1=\min\Big\{1,\frac{\sum_t rl_t}{T_{\mathrm{end}}\,N_T}\Big\},$$
$$f_2=1-\frac1{n_p}\sum_{p}\Big[0.7\big(0.5\,tw_p+0.3\,pref_p+0.2\,punct_p\big)+0.3\,S(x_p,g_p)\Big],$$
$$f_3=1-\mathrm{clip}_{[0,1]}\Big(0.3\max\{0,bal\}+0.7\,\frac1{n_p}\sum_p\min_{k\in\mathrm{need}_p}A(x_p,k)-0.2\,over\Big),$$
where

- $tw_p=1$ if $e_p\le a_p\le l_p$, and otherwise $tw_p=\max\{0,\,1-|a_p-\tfrac{e_p+l_p}{2}|/(l_p-e_p+10^{-9})\}$. Because arrivals before $e_p$ are replaced by waiting, only late arrivals ($a_p>l_p$) reach the second branch, where it equals $\max\{0,\,\tfrac12-(a_p-l_p)/(l_p-e_p)\}$. The function therefore **jumps from 1 to about 0.5 when a window is missed**; this is the implemented behaviour and is kept as is. **Interpretation.** We read the jump as a service-level step: meeting the window is rewarded in full, while missing it is a breach that removes about half of the satisfaction, after which the value decays linearly with the lateness measured relative to the window length (it reaches zero when the lateness equals half the window length). The step is a modelling choice made for the original experiments and kept unchanged here so that all pre-registered results remain valid; the results are therefore conditional on this objective, and a continuous penalty was not evaluated (Section 8). The implementation guards the denominator by $10^{-9}$; the instance generator guarantees $l_p>e_p$ (it asserts it when drawing each window; checked in the code).
- $pref_p=1$ if $p$ has no preferred team or $x_p$ is the preferred team, and $0.10$ otherwise;
- $punct_p=\max\{0,\,1-|a_p-PT_p|/(T_{\mathrm{end}}+1)\}$ for a target arrival time $PT_p$;
- $S(t,g)$ is the satisfaction of team $t$ for the care type $g_p$ of patient $p$ (the group of its lowest-numbered required skill; skills are grouped as $\{0,1\},\{2,3\},\{4\}$);
- $A(t,k)$ is the adequacy of team $t$ for skill $k$;
- $bal=1-\mathrm{std}(rl)/(\mathrm{mean}(rl)+10^{-9})$ is the workload balance (it can be negative, hence the $\max$) and $over$ is the share of teams with $rl_t>MR$. The overload penalty is subtracted *inside* the clipping, as written.


The objective vector is $f(x;\xi)=(f_1,f_2,f_3)$ and depends on a *world* $\xi=(A,S)$ of adequacies and satisfactions. $f_1$ does not depend on the world.

## 3.3 Quality measure

The hypervolume indicator is the standard unary quality measure for multiobjective fronts (Zitzler and Thiele 1999; Zitzler et al. 2003). For a finite set $F\subset[0,1]^3$ and the reference point $r=(1.2,1.2,1.2)$, the hypervolume is the Lebesgue measure of the region dominated by $F$ and bounded by $r$:
$$\mathrm{HV}(F)=\lambda\Big(\bigcup_{f\in F}[f,r]\Big),$$
computed exactly. For a run, let $\mathcal X$ be the archive of all solutions evaluated during the search that are non-dominated *with respect to the nominal objectives* $f(\cdot;\hat\xi)$ (the archive is updated after each evaluation and the oracle values play no part in it). The **oracle hypervolume** is $\mathrm{HV}\big(\{f(x;\xi^\ast):x\in\mathcal X\}\big)$, where $\xi^\ast$ is the hidden true world. It is therefore the hypervolume of the *nominally selected* archive after a single oracle re-evaluation, not of the set of solutions that are non-dominated in the oracle world among all those evaluated; the search itself only evaluates in a *nominal* world $\hat\xi$ (Section 3.4). The oracle world enters only in this last re-evaluation, a rule that was tested before every confirmatory run.

## 3.4 Instances and information model

**Instances.** Six scenarios derive from the Solomon benchmark (Solomon 1987): S4 (30 patients, 8 teams) and S5 (50 patients, 10 teams) crossed with the topologies RC101, R101 and C101. Only the customer coordinates come from the Solomon instance (the depot and the first 30 or 50 customers); for each scenario and seed an instance is generated: time windows, certification matrix $C$ (with a repair step: if some patient cannot be served by any team, team 0 is given all the skills that patient requires, with random skill levels, so that every instance is feasible; team 0 is otherwise an ordinary team, but the repair raises its coverage and can shape assignment patterns in the instances where it is triggered), and hidden truth. Public home-care benchmark sets exist (Mankowska et al. 2014) but contain no observed affinities or evidence sources, which is why the evidence is simulated here.

**Hidden truth** (as generated). A fraction 25% of certified cells is flagged *unverified*, and 35% of those are in truth not competent (hidden failure, $C^{\mathrm{true}}_{tk}=0$). Let $Q_{tk}=\text{level}_{tk}/2$ for a skill level in $\{0,1,2\}$ and $E_{tk}=\mathrm{clip}(0.15+0.6Q_{tk}+\epsilon,0,1)$ with $\epsilon\sim\mathcal N(0,0.15^2)$. The true adequacy is $A^\ast_{tk}=C^{\mathrm{true}}_{tk}(0.6Q_{tk}+0.4E_{tk})$ and the true satisfaction is $S^\ast_{tg}=\mathrm{clip}(0.35+0.45\bar A_{tg}+\eta,\,0.02,\,0.98)$ with $\eta\sim\mathcal N(0,0.10^2)$ and $\bar A_{tg}$ the mean true adequacy over the certified cells of group $g$. (The constants were checked against the generator code.)

**Evidence on adequacy.** For each certified cell $(t,k)$ the frame is $\Theta_A=\{a,\bar a\}$ (adequate, not adequate). Three sources, generated from separate pseudo-random streams and therefore independent conditionally on the hidden truth (their errors are not correlated beyond the common truth $A^\ast$), provide mass functions $m(\{a\}),m(\{\bar a\}),m(\Theta_A)$:

- *Document* (covering a random 75% of the certified, non-flagged cells): $(0.5,\,0,\,0.5)$ if covered, and the vacuous $(0,0,1)$ otherwise (also for flagged and non-certified cells).
- *Supervision*: a noisy score $\hat y=\mathrm{clip}(A^\ast+\mathcal N(0,0.25^2),0,1)$ and $s=|2\hat y-1|$, giving $(s,0,1-s)$ if $\hat y\ge 0.5$ and $(0,s,1-s)$ otherwise.
- *History*: $n\sim\mathrm{Poisson}(2)$ past observations, $x\sim\mathrm{Bin}(n,A^\ast)$ successes, and masses $\big(\tfrac{x}{n+2},\tfrac{n-x}{n+2},\tfrac{2}{n+2}\big)$.

Each source $i$ is discounted by a reliability $r_i$ (Shafer's rule): ${}^{r}m(B)=r\,m(B)$ for $B\in\{\{a\},\{\bar a\}\}$ and ${}^{r}m(\Theta_A)=1-r+r\,m(\Theta_A)$, with $r=0.95$ (document), $0.80$ (supervision) and $1.0$ (history). The discounted masses are combined by the conjunctive rule $m_{12}(B)=\sum_{C\cap D=B}m_1(C)m_2(D)$; the conflict $\kappa=m_{12}(\emptyset)$ is recorded and transferred to the frame (Yager), $m(\Theta_A)\leftarrow m(\Theta_A)+\kappa$. The nominal adequacy of a certified cell is
$$\hat A_{tk}=0.25+0.60\,\mathrm{BetP}(a),\qquad \mathrm{BetP}(a)=m(\{a\})+\tfrac12 m(\Theta_A),$$
and $\hat A_{tk}=0$ on non-certified cells.

**Evidence on satisfaction.** For each team and group, $v\sim\mathrm{Poisson}(2)$ votes with $x\sim\mathrm{Bin}(v,S^\ast)$ positive votes give the masses $\big(\tfrac{x}{v+2},\tfrac{v-x}{v+2},\tfrac2{v+2}\big)$ and the nominal satisfaction $\hat S=\tfrac{x}{v+2}+\tfrac1{v+2}$ (its pignistic probability). The nominal world is $\hat\xi=(\hat A,\hat S)$. The optimiser uses these point estimates as if they were the true values: the masses, the ignorance and the conflict are *not* propagated into the objectives $f_1$ to $f_3$. The independence of the evidence sources in this paragraph is distinct from the dependence between *individuals* of the population that is discussed for the target in Section 4.2.

**Comparison worlds.** Two further worlds appear only in the early comparisons of Section 6.2: a *non-informative world* ($\hat A=0.55$ on certified cells, $\hat S=0.5$), and a *probabilistic-average world*, where $\hat A=0.25+0.60\cdot\tfrac13\sum_i \mathrm{BetP}_i(a)$ averages the pignistic probabilities of the three discounted sources without Dempster combination and $\hat S$ is as in the nominal world. The main experiments of Sections 6.3 to 6.7 all use the nominal world.

![Figure 1. Information model and measurement. The search only sees the nominal world built from three discounted sources of evidence; the archive it produces is re-evaluated once in the hidden oracle world and the hypervolume of that re-evaluated set is the outcome.](fig/fig1_information_pipeline.png){width=100%}

**Budget.** Every algorithm in a comparison uses a population of 40 and 150 generations, i.e. $40+150\times40=6{,}040$ evaluations (MOEA/D uses 6,030, declared).

# 4. Algorithms and target models

## 4.1 QGA2-E

**State.** The population has $\mu=40$ individuals. Each individual $i$ carries its own angle array $\theta^{(i)}\in[0,\pi/2]^{n_p\times N_T}$ (entries outside the mask $M$ are zero) and the assignment $x^{(i)}\in\prod_p\mathcal A_p$ obtained from it. Initial angles are $\arcsin\sqrt{1/N_T}$ plus Gaussian noise ($\sigma=0.02$), clipped to $[0,\pi/2]$ and masked.

**Decoding (observation with collapse).** For individual $i$ and patient $p$, let $\pi_{pt}=\sin^2\theta^{(i)}_{pt}\,M_{pt}$. A Bernoulli measurement $z_{pt}\sim\mathrm{Bernoulli}(\pi_{pt})$ is drawn for each allowed team. If at least one team is measured as 1, the team is drawn among the measured ones with probabilities $\pi_{pt}z_{pt}/\sum_s\pi_{ps}z_{ps}$; otherwise it is drawn among the allowed teams with probabilities $\pi_{pt}/\sum_s\pi_{ps}$; if all $\pi_{pt}$ vanish, it is drawn uniformly on $\mathcal A_p$. A forbidden team is never returned. The normalisation $\pi_{pt}/\sum_s\pi_{ps}$ therefore describes only the second branch.

**Generation.** At generation $g$, (i) the current population consists of the survivors of the previous selection (at $g=0$, after a first selection on the initial population); (ii) the source set $S$ is the first non-dominated front of this population on the three nominal objectives and the target $q$ is computed from it *before any child of the generation exists*; (iii) every individual's angles are rotated towards $q$ (below) and a child is decoded from the rotated angles, the child keeping them; (iv) the 40 children are evaluated; (v) the 40 parents and 40 children, each with its angles, are pooled and the best 40 by non-dominated sorting and crowding distance survive (the "E" for elitist).

In the original rotation, child $i$ moves towards the single best individual. Here the rotation is directed to a *target distribution* $q(p,\cdot)$ computed once per generation from the *source set* $S$ (step ii above) and shared by all individuals:
$$\theta^{(i)\prime}_{p\cdot}=\mathrm{clip}\Big(\theta^{(i)}_{p\cdot}+\delta\,\big(q_{p\cdot}-e_{x^{(i)}(p)}\big),\,0,\,\tfrac\pi2\Big)\odot M_{p\cdot},\qquad \delta=0.05\pi,$$
where $e_x$ is the one-hot vector of team $x$ and $x^{(i)}(p)$ is the team currently assigned to $p$ by individual $i$. When the target is the one-hot vector of a single source (the best individual), the update reduces exactly to the original rotation; this reduction was a blocking test.

![Figure 2. One generation of QGA2-E. The target q is the only element that differs between the arms studied.](fig/fig2_qga2e_loop.png){width=100%}

## 4.2 Targets

Fix a patient $p$ with $K=K_p$ allowed teams (patients with $K_p=1$ are not mutable; their target is trivially $q=1$ on the single team, the singleton coincides with the frame, and they are excluded from the concentration statistics). Let $N=|S|$ be the number of sources, $c_t$ the number of sources assigning team $t$ ($\sum_t c_t=N$), $w=0.3$ the support strength and $\varepsilon=0.02$ a probability floor.

**Dp (probabilistic).** $q(t)=w\,c_t/N+(1-w)/K$, the mean over sources of the pignistic distribution of a source that supports its team with mass $w$ (the remaining $1-w$ spread uniformly).

**E (evidential).** Each source $i$ is a simple support function: mass $w$ on $\{x_i(p)\}$ and $1-w$ on the frame $\Theta_p=\mathcal A_p$. Dempster's rule combines the $N$ sources; the target is the pignistic probability $q(t)=m(\{t\})+m(\Theta_p)/K$.

> **Proposition 1 (closed form).** With $\omega=-\ln(1-w)$ and $D=1+\sum_{t}(e^{\omega c_t}-1)$, Dempster's combination of the $N$ simple supports gives $m(\{t\})=(e^{\omega c_t}-1)/D$ and $m(\Theta_p)=1/D$.
>
> *Proof.* Put $u_t=(1-w)^{c_t}$. The $c_t$ identical supports of team $t$ combine into a simple support with masses $1-u_t$ on $\{t\}$ and $u_t$ on $\Theta_p$. Combining across teams, a non-empty intersection arises when one team's focal element meets frames of the others or when $\Theta_p$ meets $\Theta_p$; two distinct singletons give the empty set. The unnormalised masses are therefore $\tilde m(\{t\})=(1-u_t)\prod_{s\ne t}u_s$ and $\tilde m(\Theta_p)=\prod_s u_s$. Dempster's normalisation divides by their sum, a common factor; dividing all by $\prod_s u_s$ gives weights $(1-u_t)/u_t=e^{\omega c_t}-1$ and $1$. $\square$

Hence $q_E(t)=\dfrac{e^{\omega c_t}-1+1/K}{1+\sum_s(e^{\omega c_s}-1)}$. A cautious conjunctive rule (canonical decomposition with the minimum of weights) was also evaluated in an early study.

**DA (similarity-based source discounting).** This is a heuristic discounting of sources that are similar to other sources assigning the same team; it does not establish independence and does not recover an unbiased effective sample size. The counts are corrected for similarity between sources: $g_i(p)=1+\#\{j\ne i:x_j(p)=x_i(p),\,s_{ij}\ge\sigma\}$, $\alpha_i(p)=1/(1+\lambda(g_i(p)-1))$, $\tilde c_t=\sum_{i:x_i(p)=t}\alpha_i(p)$, and the closed form of Proposition 1 is applied to $\tilde c$ ($\lambda=1$, $\sigma=0.7$; $s_{ij}$ is the similarity of sources $i,j$ over the patients).

**Dg and Eg (sharpened).** Any target $P$ is sharpened by the same operation
$$P^{(\gamma)}(t)=\varepsilon+(1-K\varepsilon)\,\frac{P(t)^\gamma}{\sum_{s\in\mathcal A_p}P(s)^\gamma}.$$
Dg is Dp sharpened with $\gamma=6$; Eg($\gamma$) is E sharpened with exponent $\gamma$; for $\gamma=1$ the target is not recovered exactly: it is affinely mixed with the uniform distribution, $P^{(1)}=\varepsilon\mathbf 1+(1-K\varepsilon)P$. The operation is identical for both representations, which makes the comparison symmetric.

The value $w=0.3$ was inherited from an earlier calibration on the edge of its grid and is therefore informed by hypervolume; this is declared as a limitation (Section 8).

## 4.3 Concentration: three properties

We measure the concentration of a target by its maximum $q_{\max}=\max_tq(t)$ and its entropy $H(q)=-\sum_tq(t)\ln q(t)$.

> **Proposition 2 (response to unanimity).** If all $N$ sources agree on team $t$, then $q_E(t)=1-(1-1/K)(1-w)^N$, which tends to 1 exponentially fast in $N$, whereas $q_{Dp}(t)=w+(1-w)/K$ for every $N$.
>
> *Proof.* Unanimity gives $c_t=N$, $D=e^{\omega N}$, $m(\{t\})=1-(1-w)^N$, $m(\Theta_p)=(1-w)^N$; add $m(\Theta_p)/K$. For Dp, $c_t/N=1$. $\square$

With $w=0.3$ and $K=4$: $q_E=0.98$ for $N=10$ against $q_{Dp}=0.475$. More generally, for large counts $m(\{t\})/m(\{s\})\to e^{\omega(c_t-c_s)}$: the evidential target behaves like a Boltzmann distribution on counts with inverse temperature $\omega=-\ln(1-w)\approx0.357$ (each source contributes the weight of evidence $\omega$, which adds), while Dp is affine in the counts. The evidential target is therefore *adaptively* concentrated: it sharpens as agreement among sources grows, unlike a fixed power.

> **Proposition 3 (sharpening is tempering).** Let $P$ have strictly positive components, $\gamma>0$ and $0\le\varepsilon<1/K$. (a) For $\varepsilon=0$, $P^{(\gamma)}\propto\exp(\gamma\ln P)$ is a Boltzmann distribution with inverse temperature $\gamma$ and $\dfrac{d}{d\gamma}H(P^{(\gamma)})=-\gamma\,\mathrm{Var}_{P^{(\gamma)}}(\ln P)\le0$. (b) For every $\varepsilon$, $\gamma_2>\gamma_1$ implies that $P^{(\gamma_2)}$ majorises $P^{(\gamma_1)}$, hence $H(P^{(\gamma_2)})\le H(P^{(\gamma_1)})$ and $q_{\max}$ is non-decreasing in $\gamma$. (c) $q_{\max}\le1-(K-1)\varepsilon$.
>
> *Proof.* (a) Write $P^{(\gamma)}=e^{\gamma s-A(\gamma)}$ with $s=\ln P$ and $A=\ln\sum e^{\gamma s}$. Then $H=A-\gamma E[s]$ and $A'=E[s]$, so $H'=-\gamma\,E'[s]=-\gamma\,\mathrm{Var}(s)$. (b) Let $r^{(\gamma)}=P^\gamma/\sum P^\gamma$ and order the teams so that $P_1\ge\dots\ge P_K$ (this order is the same for every $\gamma$). The partial sum $F_j(\gamma)=\sum_{i\le j}r^{(\gamma)}_i=E_\gamma[\mathbf 1_{i\le j}]$ has derivative $\mathrm{Cov}_\gamma(\mathbf 1_{i\le j},\ln P_i)\ge0$, because both functions are non-increasing in $i$ (Chebyshev's association inequality). All partial sums of the ordered vector are therefore non-decreasing in $\gamma$ and the totals are equal to 1, which is majorisation. The floored target is $q=(1-K\varepsilon)r+K\varepsilon u$ with $u$ uniform; it has the same order and partial sums $(1-K\varepsilon)F_j+K\varepsilon\,j/K$, again non-decreasing in $\gamma$, so majorisation is preserved. Shannon entropy is Schur-concave, hence $H$ is non-increasing; $q_{\max}=\varepsilon+(1-K\varepsilon)F_1$ is non-decreasing. (c) follows from $F_1\le1$. $\square$

With $\varepsilon=0.02$ and $K=4$ the plateau is $0.94$ (Figure 3a). The exponent is therefore a one-parameter concentration scale on which the evidential target (an adaptive, count-dependent sharpening) and the sharpened frequency target (a fixed power of an affine function of the counts) can be placed, but they are not the same family: a match of mean concentration does not imply a match of distributions.

![Figure 3. Concentration of the targets. (a) Maximum of the target as a function of the number of agreeing sources (K = 4, N = 10, other sources split evenly; Dg and Eg with exponent 6 coincide on this range). (b) Mean maximum of the target observed during the runs (six scenarios, 100 seeds, generations 1, 25, 50, 100, 150).](fig/fig3_target_concentration.png){width=100%}

## 4.4 Baselines and other variants

NSGA-II (Deb et al. 2002) and MOEA/D (Zhang and Li 2007) are run on the same instances, seeds, decoder and budget, with an archive of every evaluated solution re-evaluated in the oracle world as for QGA2-E. Guided mutation in NSGA-II draws the new team of a mutated gene (probability $1/n_p$) from the target $q$ restricted to the other allowed teams; with $q$ uniform it is bit-for-bit NSGA-II. Each algorithm received the same small tuning effort, three candidate parameter sets evaluated on separate tuning seeds under a selection rule written before the runs (the rotation step of QGA2-E, the crossover and mutation probabilities of NSGA-II, the neighbourhood size of MOEA/D; the a priori set was kept unless another improved the criterion by at least 0.001). The comparison with the classical algorithms is therefore contextual: it is made at equal budget, on one problem family and with a limited tuning effort, and it is not a ranking of algorithm families or evidence about other model-based algorithms.

# 5. Experimental design and decision rules

## 5.1 Outcome, pairing and statistics

Reporting follows standard practice: percentile bootstrap intervals (Efron 1979); practical equivalence assessed by two one-sided tests (Schuirmann 1987) or, equivalently, by a confidence interval lying inside an equivalence margin (Lakens 2017); Holm adjustment for multiplicity within a family (Holm 1979); and the reproducibility and pre-registration practices advocated for evolutionary computation (López-Ibáñez et al. 2021) and for empirical science (Nosek et al. 2018).

The outcome of a run is the oracle hypervolume (Section 3.3). For seed $s$ and arm $a$ let $h_{a,s}=\frac16\sum_{c=1}^6\mathrm{HV}^{\mathrm{oracle}}_{a,s,c}$ over the six scenarios. A contrast between arms $a$ and $b$ is $\Delta_{ab}=\frac1n\sum_s(h_{a,s}-h_{b,s})$ on the same seeds and instances. Intervals are percentile bootstrap intervals from resampling seeds jointly ($B=20{,}000$, deterministic random stream per analysis).

Two reporting regimes were used. The earlier studies were analysed with 95% bootstrap intervals and Holm-adjusted tests, without an equivalence margin. The later studies define a family of $m=4$ or $5$ primary contrasts with $(1-\alpha/m)$ intervals, i.e. 99% for $\alpha=0.05$, $m=5$ (for $m=4$, 99% is slightly conservative relative to 98.75%), and a practical-equivalence margin $\delta=0.005$ of hypervolume. Holm-adjusted $p$-values do not make the accompanying 95% intervals simultaneous; the two regimes do not give the same protection against multiplicity. With interval $[L,U]$ the decision for a contrast is:

- *superiority* if $L>0$; *inferiority* if $U<0$;
- *equivalence* if $[L,U]\subset[-\delta,\delta]$;
- *inconclusive* otherwise.

An interval that contains 0 does not demonstrate equivalence, and an inferiority whose interval extends beyond $-\delta$ is not an equivalence either. Likewise, a superiority or inferiority decision means that the interval excludes zero: it does not show that the difference exceeds the margin $\delta$ over the whole interval, and a difference smaller than $\delta$ may be detectable without being of practical relevance. Secondary contrasts are reported with 95% intervals and are exploratory. The sequence of studies was not corrected for multiplicity globally (Section 8).

## 5.2 Governance

Every confirmatory result comes from a protocol written before the run, with the following steps in a fixed order: written protocol (hypotheses, contrasts, margins, decision rules, seeds); implementation with unit and integration tests (gates, e.g. exact reproduction of earlier arms, exact budget, no use of oracle values in the search, reproducibility); any calibration done without reading hypervolume; a freeze file of cryptographic hashes of protocol, code and parameters, verified before the run; the run, with results stored in atomic shards; a pre-analysis check of completeness and freeze; and one single analysis in which hypervolume is read for the first time. No run was repeated to improve a result, and no hypothesis, margin or rule was changed after results were read. Defects found in tests or checks were corrected before the freeze or, when found at the analysis check, before any hypervolume was read; each is declared in the supplementary appendix.

## 5.3 What "pre-registered" means here

New contrasts, margins and decision rules were fixed before each run. The reference results of earlier studies (for example the stored runs of E, Dp and Dg on seeds 10400–10499) had already been seen when later studies were designed, and several later studies reuse those seeds as paired references. The design is therefore sequential and adaptive across studies, and blind only within each study's own run.

## 5.4 Seeds and sample sizes

Each study uses seeds not used by calibration or technical tests. Main ranges: 11200–11299 and 10400–10499 (100 seeds, six scenarios derived from three Solomon geographies), 12000–12099 (two studies, not independent), 14000–14059 (first independent evaluation), 15000–15059 (second) and 16000–16059 (concentration-schedule study). Sample sizes are 100 seeds for most studies, 200 or 300 for the earliest ones and 60 for the latest; contrasts are paired within a study only.

# 6. Results

All differences are in oracle hypervolume (the mean of the QGA2-E variants is about 0.5, that of NSGA-II about 0.65); intervals are 99% for primary contrasts with the margin 0.005 and 95% for secondary or descriptive ones, and each quoted contrast says which. Question 1 (does the evidential target beat the simple probabilistic target?): Sections 6.2 and 6.6. Question 2 (is concentration the mechanism, or the representation, or the schedule?): Sections 6.3, 6.5 and 6.7. Question 3 (transfer to another algorithm): Section 6.8. Question 4 (does it hold outside the original instances?): Section 6.6. Table 1 gathers the pairwise differences in oracle hypervolume between the 14 methods on the six Solomon-derived scenarios (SC6): bold values are primary pre-registered paired contrasts (99% CI), round brackets secondary paired contrasts (95% CI), and square or curly brackets differences of means (within or across seed ranges) without intervals. The values quoted in Sections 6.1, 6.3 and 6.8 are taken from it or from the paired contrasts it lists; studies on other seed ranges (Sections 6.5 to 6.7) are reported in their own tables and are not in it. The detail of Sections 6.3 to 6.5 is provided in Online Resource 1.

**Table 1.** Mean difference in oracle hypervolume, row minus column (SC6; positive: the row is better; negative: the column is better; near zero: comparable, equivalence margin ±0.005). The matrix is antisymmetric. Style of each value: **bold**, primary pre-registered paired contrast (99% CI); (round brackets), secondary or descriptive paired contrast (95% CI); [square brackets], difference of means within one seed range, without CI; {curly brackets}, difference of means from different seed ranges, an order of magnitude only. The intervals of the paired contrasts are given in the supplementary traceability table. Abbreviations are defined in Appendix B.

| row ↓ \ column → | NSGA2 | MOEAD | GDp | GE | GDg6 | GEg6 | Dp | Dg | DA | E | Eg1.1 | Eg0.8 | Eg2 | Eg6 |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| **NSGA2** |—|**−0.0065**|**−0.0000**|(+0.0040)|(+0.0028)|(+0.0007)|(+0.1684)|**+0.1221**|(+0.1257)|**+0.1258**|[+0.1215]|[+0.1273]|[+0.1272]|[+0.1385]|
| **MOEAD** |**+0.0065**|—|{+0.0157}|{+0.0197}|{+0.0185}|{+0.0164}|(+0.1749)|**+0.1286**|(+0.1322)|(+0.1322)|{+0.1372}|{+0.1430}|{+0.1429}|{+0.1542}|
| **GDp** |**+0.0000**|{−0.0157}|—|**+0.0040**|(+0.0028)|[+0.0007]|(+0.1637)|[+0.1182]|{+0.1165}|[+0.1226]|[+0.1215]|[+0.1273]|[+0.1272]|[+0.1385]|
| **GE** |(−0.0040)|{−0.0197}|**−0.0040**|—|[−0.0012]|(−0.0033)|[+0.1597]|[+0.1142]|{+0.1125}|(+0.1186)|[+0.1175]|[+0.1233]|[+0.1232]|[+0.1345]|
| **GDg6** |(−0.0028)|{−0.0185}|(−0.0028)|[+0.0012]|—|**−0.0021**|[+0.1609]|(+0.1154)|{+0.1137}|[+0.1197]|[+0.1187]|[+0.1245]|[+0.1244]|[+0.1357]|
| **GEg6** |(−0.0007)|{−0.0164}|[−0.0007]|(+0.0033)|**+0.0021**|—|[+0.1630]|[+0.1175]|{+0.1158}|[+0.1218]|[+0.1208]|[+0.1266]|[+0.1265]|[+0.1378]|
| **Dp** |(−0.1684)|(−0.1749)|(−0.1637)|[−0.1597]|[−0.1609]|[−0.1630]|—|(−0.0463)|**−0.0427**|(−0.0427)|(−0.0422)|(−0.0364)|[−0.0365]|[−0.0251]|
| **Dg** |**−0.1221**|**−0.1286**|[−0.1182]|[−0.1142]|(−0.1154)|[−0.1175]|(+0.0463)|—|**+0.0036**|(+0.0036)|(+0.0033)|(+0.0091)|[+0.0090]|[+0.0204]|
| **DA** |(−0.1257)|(−0.1322)|{−0.1165}|{−0.1125}|{−0.1137}|{−0.1158}|**+0.0427**|**−0.0036**|—|(+0.0000)|{+0.0050}|{+0.0108}|{+0.0107}|{+0.0220}|
| **E** |**−0.1258**|(−0.1322)|[−0.1226]|(−0.1186)|[−0.1197]|[−0.1218]|(+0.0427)|(−0.0036)|(−0.0000)|—|**−0.0010**|**+0.0047**|(+0.0046)|(+0.0160)|
| **Eg1.1** |[−0.1215]|{−0.1372}|[−0.1215]|[−0.1175]|[−0.1187]|[−0.1208]|(+0.0422)|(−0.0033)|{−0.0050}|**+0.0010**|—|[+0.0058]|[+0.0057]|[+0.0170]|
| **Eg0.8** |[−0.1273]|{−0.1430}|[−0.1273]|[−0.1233]|[−0.1245]|[−0.1266]|(+0.0364)|(−0.0091)|{−0.0108}|**−0.0047**|[−0.0058]|—|[−0.0001]|[+0.0112]|
| **Eg2** |[−0.1272]|{−0.1429}|[−0.1272]|[−0.1232]|[−0.1244]|[−0.1265]|[+0.0365]|[−0.0090]|{−0.0107}|(−0.0046)|[−0.0057]|[+0.0001]|—|[+0.0113]|
| **Eg6** |[−0.1385]|{−0.1542}|[−0.1385]|[−0.1345]|[−0.1357]|[−0.1378]|[+0.0251]|[−0.0204]|{−0.0220}|(−0.0160)|[−0.0170]|[−0.0112]|[−0.0113]|—|

**Key.** NSGA2, MOEAD: classical NSGA-II and MOEA/D, no guidance. GDp, GE, GDg6, GEg6: NSGA-II whose mutation is guided by Dp, E, Dg and Eg6 respectively. Dp: QGA2-E with the simple probabilistic target. Dg: Dp sharpened by the power γ = 6. DA: evidential target with dependence correction (source discounting by similarity). E: evidential target (Dempster's rule, pignistic probability). Eg1.1, Eg0.8, Eg2, Eg6: E sharpened or softened with exponent γ. Other abbreviations: Appendix B.

## 6.1 Classical algorithms against QGA2-E

At equal budget NSGA-II and MOEA/D exceed every QGA2-E variant: NSGA-II − E = +0.1258 [+0.1214, +0.1301], NSGA-II − Dg = +0.1221 [+0.1177, +0.1265], MOEA/D − Dg = +0.1286 [+0.1239, +0.1331] (Table 1; 100 seeds, 99% CI; MOEA/D slightly better than NSGA-II, −0.0065 [−0.0092, −0.0037]). The gap is 0.11 to 0.17 depending on the variant, and earlier studies gave 0.13 to 0.16; adding elitism to QGA2 did not close it.

## 6.2 Evidential against probabilistic targets

In every early study an evidential target built by Dempster's rule had a higher hypervolume than the matched probabilistic target of the same study (n = 200): Dempster's rule over the matched probabilistic control +0.0250 [+0.0238, +0.0262]; fully evidential against fully probabilistic pipeline +0.0275 [+0.0261, +0.0289]; in the QGA2-E architecture E − P = +0.0459 [+0.0444, +0.0473], 100% of seeds favourable; the cautious rule was worse than both. Stacking evidential layers gave no additional benefit. These probabilistic targets were not matched in concentration, so these studies do not say whether the representation or the resulting sharpness is responsible.

## 6.3 Concentration of the target

At generation 150 the mean maximum of the target was 0.281 for Dp, 0.805 for Dg (γ = 6) and 0.851 for E, with entropies 1.452, 0.646 and 0.525: the evidential target is far more concentrated than the simple probabilistic target, as Proposition 2 predicts. A power-sharpened probabilistic target reproduced and slightly exceeded the evidential advantage: in a descriptive study (n = 200) Dg − Dp = +0.0454 and E − Dg = −0.0040 [−0.0055, −0.0025]; in the confirmatory comparison (n = 100; Table 1 gives the confirmatory values) DA − Dp = +0.0427 [+0.0401, +0.0454] and DA − Dg = −0.0036 [−0.0064, −0.0009], an inferiority whose interval extends beyond the margin. The exponent of Dg was chosen by concentration matching on calibration seeds without reading hypervolume; the matching gate was not met by any exponent in the descriptive study (best attempt γ = 6, declared non-conforming).

Sharpening the evidential target made it worse (n = 100): Eg2 − E = −0.0046 [−0.0076, −0.0016], Eg6 − E = −0.016 [−0.0188, −0.0130], Eg6 − Dg = −0.0204 [−0.0231, −0.0177], while exponents between 0.9 and 1.25 were equivalent to E (for example Eg1.1 − E = +0.0010 [−0.0015, +0.0036]). The key contrast for representation, the evidential target sharpened to match the concentration of Dg against Dg (n = 60), was *inconclusive*: DAgm − Dg = −0.0025 [−0.0057, +0.0009]. The calibration used other scenarios and compared means only, so matching on the evaluation scenarios was not guaranteed. This study does not show that the two representations are equivalent, nor that concentration is the exclusive cause of the evidential advantage.

## 6.4 Refinements of the evidential structure

Four further ideas were tested, each pre-registered, to see whether the evidential structure could add something beyond a sharper target: a dependence correction (DA), ignorance as a fourth survival objective, adaptive regulation of the dependence cap, and diversity as a fourth objective. None produced a robust gain: the only positive effect (ignorance as a fourth objective, +0.0077) was matched or exceeded by a random fourth objective (−0.0042 for ignorance against the random one), the adaptive regulation was equivalent to the fixed cap in all five contrasts, and diversity as a fourth objective was inferior (−0.0094). The full list of contrasts is provided in Online Resource 1 (Appendix E).

## 6.5 Dependence degree and local sensitivity

Two later studies (n = 100, seeds 12000–12099, not independent) varied the dependence degree λ of the dependence-corrected target DA and then the source strength w, the similarity threshold σ and the exponent, one at a time. The parameter λ changed the concentration of the target markedly (maximum probability at generation 150 from 0.845 for E to 0.709 for λ = 1) without changing hypervolume (DA(1) − E = −0.0009 [−0.0025, +0.0007], equivalence; DA − Dg between −0.0029 and −0.0039 with a conforming match). In the sensitivity study the evidential target kept a large advantage over the simple probabilistic target at every source strength (E − Dp = +0.028 to +0.043), but the sign of DA − Dg depended on the setting: +0.0032 [+0.0010, +0.0052] at w = 0.15 and −0.0039 [−0.0066, −0.0014] at the reference w = 0.3 (both with a conforming match), and unattributable where the match failed (w = 0.5, w = 0.7, σ = 0.6). Post hoc observations are in Online Resource 1.

## 6.6 Independent evaluations on new families of instances

All earlier decisions were made on scenarios derived from three Solomon geographies. Two studies, each with a protocol written before any calibration or run, ask which main contrasts hold on instances that played no role in those decisions (new geographies, sizes and seeds; the free exponent was recalibrated each time; only the geography changes, so the instances are semi-synthetic). The first used synthetic Solomon-like geographies (uniform, clustered, mixed; 40 patients and 9 teams, or 70 and 12; 60 seeds per scenario, 360 instances); the second used customer coordinates of six public benchmark files (Uchoa X-n101-k25 (Uchoa et al. 2017), Christofides M-n101-k10 (Christofides et al. 1979), Golden_1 (1998), Li_21 (2005), ORTEC-n242-k12 and Homberger C1_2_1 (Gehring and Homberger 1999)) from the test data of VRPLIB (Lan 2023), with 50 patients sampled per seed, 10 teams, day end 240 and visit 10 (60 seeds, 360 instances). Skills, windows, hidden truth and evidence are simulated by the unchanged generator. The concentration gate was satisfied at w = 0.7 only; at w = 0.3 the match failed in both evaluations. Results are in Tables 2 and 3.

**Table 2.** Independent evaluation (60 seeds, six new scenarios; paired differences in oracle hypervolume, 99% intervals, margin 0.005).

| Contrast | Difference | 99% interval | Decision | Earlier study |
|---|---|---|---|---|
| DA − E, w = 0.3 | −0.0005 | [−0.0015, +0.0005] | equivalence | equivalence (−0.0009) |
| DA − E, w = 0.7 | +0.0001 | [−0.0018, +0.0019] | equivalence | superiority (+0.0039) |
| DA − Dg(6), w = 0.3 (match not conforming) | −0.0072 | [−0.0099, −0.0044] | inferiority | inferiority (−0.0039) |
| DA − Dg(4), w = 0.7 (match conforming) | −0.0047 | [−0.0076, −0.0019] | inferiority | inferiority (−0.0105, match not conforming) |
| Dg(6) − E, w = 0.3 | +0.0067 | [+0.0038, +0.0096] | superiority | not a registered contrast |
| Dg(4) − E, w = 0.7 | +0.0048 | [+0.0018, +0.0078] | superiority | not a registered contrast |
| DA − Dp, w = 0.3 | +0.0216 | [+0.0189, +0.0244] | superiority | large positive in all earlier studies |
| DA − Dp, w = 0.7 | +0.0216 | [+0.0188, +0.0247] | superiority | large positive in all earlier studies |

**Table 3.** Second independent evaluation (benchmark geographies; 60 seeds, six geographies; paired differences in oracle hypervolume, 99% intervals, margin 0.005; the last column gives the first evaluation).

| Contrast | Difference | 99% interval | Decision | First evaluation |
|---|---|---|---|---|
| DA − E, w = 0.3 | −0.0009 | [−0.0019, −0.0001] | inferiority (within the margin) | equivalence (−0.0005) |
| DA − E, w = 0.7 | +0.0002 | [−0.0011, +0.0015] | equivalence | equivalence (+0.0001) |
| DA − Dg(4), w = 0.3 (match not conforming) | +0.0090 | [+0.0066, +0.0114] | superiority | inferiority (−0.0072, γ = 6) |
| DA − Dg(4), w = 0.7 (match conforming) | −0.0032 | [−0.0067, +0.0002] | inconclusive | inferiority (−0.0047) |
| Dg(4) − E, w = 0.3 | −0.0099 | [−0.0129, −0.0071] | inferiority | superiority (+0.0067, γ = 6) |
| Dg(4) − E, w = 0.7 | +0.0033 | [−0.0001, +0.0069] | inconclusive | superiority (+0.0048) |
| DA − Dp, w = 0.3 | +0.0203 | [+0.0176, +0.0232] | superiority | superiority (+0.0216) |
| DA − Dp, w = 0.7 | +0.0247 | [+0.0222, +0.0272] | superiority | superiority (+0.0216) |
| DA − Dg(6), w = 0.3 (match not conforming) | −0.0086 | [−0.0117, −0.0056] | inferiority | inferiority (−0.0072) |

In both evaluations the simple probabilistic target was clearly the weakest (about 0.02 below E and DA) in every geography, and DA and E were equivalent at w = 0.7; the earlier small advantage of DA over E at w = 0.7 was not reproduced. The ordering between the evidential targets and the sharpened probabilistic target was not stable: Dg was better on the synthetic geographies; on the benchmark geographies it was worse than E and DA with the calibrated exponent at w = 0.3 (γ = 4), better with γ = 6, and inconclusive at w = 0.7. A sharpened probabilistic target is therefore not a robust substitute unless its exponent is tuned on instances of the target family; this agrees with the importance of concentration and does not show that the representation matters independently of it.

## 6.7 Matching the concentration trajectory: representation or schedule?

The evidential target concentrates on a schedule of its own, whereas Dg uses one fixed exponent, so earlier comparisons mix representation and schedule. This study gives the simple probabilistic target a time-varying exponent $\gamma_t=g_0+(g_1-g_0)\min\{1,(t-1)/(G_s-1)\}$ (renormalised, floor 0.02; Dgt; a constant ramp equals Dg bit for bit). On the benchmark geographies of the second evaluation (new seeds 16000–16059 and patient samples, 360 instances; not independent of that evaluation), the schedule was selected once per source strength and reference target (E or DA) without reading hypervolume, on other seeds, among 12 candidates ($g_0\in\{1,3\}$, $g_1\in\{6,10,16\}$, $G_s\in\{30,90\}$), using a gate on the whole trajectory (mean relative entropy gap ≤ 10% and mean $|\Delta q_{\max}|$ ≤ 0.05) and the least squared gap among the candidates that passed; the match was then verified on the evaluation instances without recalibration. The schedules were 3→6 over 90 generations at w = 0.3 and 3→6 over 30 generations at w = 0.7 (the same for E and DA). The match was conforming for E at both strengths (entropy gap 4.8% and 5.9%) and for DA at w = 0.3, and not conforming for DA at w = 0.7 (21.7%, $|\Delta q_{\max}|$ 0.061), where the contrast is descriptive (Table 4). The pre-registered reading: with a conforming match, a superior E means that the advantage is not explained by the schedule alone; a superior Dgt means that a probabilistic schedule does better than Dempster's rule.

**Table 4.** Concentration-schedule study (60 seeds, six benchmark geographies; paired differences in oracle hypervolume; 99% intervals; margin 0.005). "Bonf." is the decision with Bonferroni intervals (m = 5 per source strength). L2 at w = 0.7 is descriptive (the match was not conforming for the DA reference).

| Contrast | Difference | 99% interval | Decision | Bonf. |
|---|---|---|---|---|
| L1: E − Dgt, w = 0.3 | +0.0066 | [+0.0035, +0.0095] | superiority | superiority |
| L2: DA − Dgt, w = 0.3 | +0.0061 | [+0.0031, +0.0089] | superiority | superiority |
| L3: DA − E, w = 0.3 | −0.0005 | [−0.0013, +0.0002] | equivalence | equivalence |
| L4: DA − Dp, w = 0.3 | +0.0224 | [+0.0199, +0.0250] | superiority | superiority |
| L5: DA − Dg(6), w = 0.3 | −0.0071 | [−0.0096, −0.0045] | inferiority | inferiority |
| L1: E − Dgt, w = 0.7 | −0.0050 | [−0.0084, −0.0017] | inferiority | inferiority |
| L2: DA − Dgt, w = 0.7 (descriptive) | −0.0045 | [−0.0079, −0.0011] | inferiority | inferiority |
| L3: DA − E, w = 0.7 | +0.0006 | [−0.0010, +0.0021] | equivalence | equivalence |
| L4: DA − Dp, w = 0.7 | +0.0248 | [+0.0222, +0.0274] | superiority | superiority |
| L5: DA − Dg(6), w = 0.7 | −0.0001 | [−0.0027, +0.0025] | equivalence | equivalence |

Mean hypervolumes were, at w = 0.3, 0.2013 (E), 0.2008 (DA), 0.1783 (Dp), 0.1947 (Dgt) and 0.2078 (Dg with γ = 6); at w = 0.7, 0.2066, 0.2072, 0.1824, 0.2117 and 0.2073. At w = 0.3 the evidential target was better than the scheduled probabilistic target, in four of six geographies; at w = 0.7 the sign reversed and Dgt was better than E in each geography; Bonferroni intervals gave the same decisions. A fixed exponent of 6 was better than both E and the scheduled target at w = 0.3, so the schedule selected by the gate is not the one that maximises hypervolume. The advantage of E over a probabilistic target with the same schedule of entropy and maximum probability is thus not explained by the schedule of these two diagnostics alone at w = 0.3, but it is not consistent across source strengths, and no general advantage or disadvantage of the representation follows. The match covers two scalar diagnostics: the effective decoded distributions of the matched arms remained far apart at generation 150 (Jensen–Shannon divergence 0.17 at w = 0.3 and 0.33 at w = 0.7; L1 distance 0.74 to 0.96 out of 2). The schedule family has three parameters, was selected on three geographies, and the geographies are those of the second evaluation.

## 6.8 Transfer to NSGA-II

A transfer study (n = 100, five primary contrasts, 99% CI) guided the mutation of NSGA-II by the targets. Guiding with the probabilistic target did not change hypervolume (GDp − NSGA-II = 0.0000 [−0.0033, +0.0033], equivalence); the evidential target was not better than the probabilistic one (GE − GDp = −0.0040 [−0.0072, −0.0008], the interval partly inside the margin; equivalent after the same sharpening, +0.0021 [−0.0006, +0.0049]). The concentration-matched evidential arm degenerated into the natural evidential arm, so that contrast does not isolate the representation. All guided arms stayed within 0.004 of unguided NSGA-II (0.6429; Table 1).

# 7. Discussion

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

**Online Resource 1.** The extended manuscript (with the full results of Sections 6.3 to 6.5, the post hoc analyses, the full limitations, the declared incidents and the refinement studies), the frozen protocols and code, and the final analysis files are provided as Online Resource 1 and archived in release V1.0 of https://github.com/MontZ26/Evidential_QGA2E_paper_archive (permanent link: https://github.com/MontZ26/Evidential_QGA2E_paper_archive/releases/tag/V1.0).

# Appendix A. Declared incidents and deviations (summary)

No run was repeated to improve a result and no hypothesis, margin or rule was changed after results were read; the incidents are declared in Online Resource 1 (Appendix A).

# Appendix B. Glossary of abbreviations

**Algorithms.** QGA2-E: the quantum-inspired GA of this paper (one angle θ per gene, selection probability sin²θ, target computed from the first non-dominated front). NSGA-II, MOEA/D: classical multiobjective GAs (non-dominated sorting with crowding; decomposition).

**Targets.** q: target probability per team. Dp: simple probabilistic target. E: evidential target (Dempster's rule, then BetP). DA(λ): E with source discounting by similarity (λ = 1 is DA, σ = 0.7). Dg(γ), Eg(γ): Dp, E sharpened by the power γ (γ = 6 unless stated).

# References

Agarwal H., Renaud J.E., Preston E.L., Padmanabhan D. Uncertainty quantification using evidence theory in multidisciplinary design optimization. *Reliability Engineering & System Safety* 85(1–3) (2004) 281–294. https://doi.org/10.1016/j.ress.2004.03.017.

Baluja S. Population-based incremental learning: a method for integrating genetic search based function optimization and competitive learning. Technical report CMU-CS-94-163, School of Computer Science, Carnegie Mellon University, June 1994.

Braekers K., Hartl R.F., Parragh S.N., Tricoire F. A bi-objective home care scheduling problem: analyzing the trade-off between costs and client inconvenience. *European Journal of Operational Research* 248(2) (2016) 428–443.

Christofides N., Mingozzi A., Toth P. The vehicle routing problem. In: *Combinatorial Optimization*. Wiley, Chichester, 1979.

Cissé M., Yalçındağ S., Kergosien Y., Şahin E., Lenté C., Matta A. OR problems related to Home Health Care: a review of relevant routing and scheduling problems. *Operations Research for Health Care* 13–14 (2017) 1–22. https://doi.org/10.1016/j.orhc.2017.06.001.

Deb K., Pratap A., Agarwal S., Meyarivan T. A fast and elitist multiobjective genetic algorithm: NSGA-II. *IEEE Transactions on Evolutionary Computation* 6(2) (2002) 182–197. https://doi.org/10.1109/4235.996017.

Dempster A.P. Upper and lower probabilities induced by a multivalued mapping. *Annals of Mathematical Statistics* 38(2) (1967) 325–339. https://doi.org/10.1214/aoms/1177698950.

Denœux T. Decision-making with belief functions: a review. *International Journal of Approximate Reasoning* 109 (2019) 87–110. https://doi.org/10.1016/j.ijar.2019.03.009; arXiv:1808.05322.

Di Mascolo M., Martinez C., Espinouse M.-L. Routing and scheduling in Home Health Care: a literature survey and bibliometric analysis. *Computers & Industrial Engineering* 158 (2021) 107255. https://doi.org/10.1016/j.cie.2021.107255.

Efron B. Bootstrap methods: another look at the jackknife. *Annals of Statistics* 7(1) (1979) 1–26. https://doi.org/10.1214/aos/1176344552.

Fikar C., Hirsch P. Home health care routing and scheduling: a review. *Computers & Operations Research* 77 (2017) 86–95. https://doi.org/10.1016/j.cor.2016.07.019.

Gehring H., Homberger J. A parallel hybrid evolutionary metaheuristic for the vehicle routing problem with time windows. In: *Proceedings of EUROGEN99*, 1999.

Golden B.L., Wasil E.A., Kelly J.P., Chao I.-M. The impact of metaheuristics on solving the vehicle routing problem: algorithms, problem sets, and computational results. In: *Fleet Management and Logistics*. Springer, Boston, MA, 1998. https://doi.org/10.1007/978-1-4615-5755-5_2.

Han K.-H., Kim J.-H. Quantum-inspired evolutionary algorithm for a class of combinatorial optimization. *IEEE Transactions on Evolutionary Computation* 6(6) (2002) 580–593. https://doi.org/10.1109/TEVC.2002.804320.

Han K.-H., Kim J.-H. Quantum-inspired evolutionary algorithms with a new termination criterion, Hε gate, and two-phase scheme. *IEEE Transactions on Evolutionary Computation* 8(2) (2004) 156–169. https://doi.org/10.1109/TEVC.2004.823467.

Hauschild M., Pelikan M. An introduction and survey of estimation of distribution algorithms. *Swarm and Evolutionary Computation* 1(3) (2011) 111–128. https://doi.org/10.1016/j.swevo.2011.08.003.

Holm S. A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics* 6(2) (1979) 65–70.

Kim Y., Kim J.-H., Han K.-H. Quantum-inspired multiobjective evolutionary algorithm for multiobjective 0/1 knapsack problems. *Proc. 2006 IEEE Congress on Evolutionary Computation* (2006) 2601–2606. https://doi.org/10.1109/CEC.2006.1688633.

Lakens D. Equivalence tests: a practical primer for t tests, correlations, and meta-analyses. *Social Psychological and Personality Science* 8(4) (2017) 355–362. https://doi.org/10.1177/1948550617697177.

Lan L. VRPLIB: a Python package for working with routing problem instances (software and test data, MIT licence), 2023, https://github.com/PyVRP/VRPLIB, commit 309f1890 (distributed copy of the benchmark files used in Section 6.6).

Larrañaga P., Lozano J.A. *Estimation of Distribution Algorithms: A New Tool for Evolutionary Computation*. Kluwer Academic Publishers, Boston, 2002. ISBN 978-0-7923-7466-4.

Li F., Golden B., Wasil E. Very large-scale vehicle routing: new test problems, algorithms, and results. *Computers & Operations Research* 32(5) (2005) 1165–1179.

Li Z., Rudolph G. A framework of quantum-inspired multi-objective evolutionary algorithms and its convergence properties. Technical report, TU Dortmund (SFB 531), 2007. https://doi.org/10.17877/DE290R-8713.

López-Ibáñez M., Branke J., Paquete L. Reproducibility in evolutionary computation. *ACM Transactions on Evolutionary Learning and Optimization* 1(4) (2021), article 14. https://doi.org/10.1145/3466624; arXiv:2102.03380.

Mankowska D.S., Meisel F., Bierwirth C. The home health care routing and scheduling problem with interdependent services. *Health Care Management Science* 17(1) (2014) 15–30. https://doi.org/10.1007/s10729-013-9243-1.

Mourelatos Z.P., Zhou J. A design optimization method using evidence theory. *Journal of Mechanical Design* 128(4) (2006) 901–908. https://doi.org/10.1115/1.2204970.

Nosek B.A., Ebersole C.R., DeHaven A.C., Mellor D.T. The preregistration revolution. *Proceedings of the National Academy of Sciences* 115(11) (2018) 2600–2606. https://doi.org/10.1073/pnas.1708274114.

Rasmussen M.S., Justesen T., Dohn A., Larsen J. The home care crew scheduling problem: preference-based visit clustering and temporal dependencies. *European Journal of Operational Research* 219(3) (2012) 598–610.

Schuirmann D.J. A comparison of the two one-sided tests procedure and the power approach for assessing the equivalence of average bioavailability. *Journal of Pharmacokinetics and Biopharmaceutics* 15(6) (1987) 657–680.

Shafer G. *A Mathematical Theory of Evidence*. Princeton University Press, 1976.

Shapiro J.L. Drift and scaling in estimation of distribution algorithms. *Evolutionary Computation* 13(1) (2005) 99–123. https://doi.org/10.1162/1063656053583414.

Smets P., Kennes R. The transferable belief model. *Artificial Intelligence* 66(2) (1994) 191–234. https://doi.org/10.1016/0004-3702(94)90026-4.

Solomon M.M. Algorithms for the vehicle routing and scheduling problems with time window constraints. *Operations Research* 35(2) (1987) 254–265. https://doi.org/10.1287/opre.35.2.254.

Uchoa E., Pecin D., Pessoa A., Poggi M., Vidal T., Subramanian A. New benchmark instances for the capacitated vehicle routing problem. *European Journal of Operational Research* 257(3) (2017) 845–858. https://doi.org/10.1016/j.ejor.2016.08.012.

Yager R.R. On the Dempster–Shafer framework and new combination rules. *Information Sciences* 41(2) (1987) 93–137. https://doi.org/10.1016/0020-0255(87)90007-7.

Yang J.-B., Xu D.-L. On the evidential reasoning algorithm for multiple attribute decision analysis under uncertainty. *IEEE Transactions on Systems, Man, and Cybernetics – Part A* 32(3) (2002) 289–304. https://doi.org/10.1109/TSMCA.2002.802746.

Zhang Z., Jiang C. Evidence-theory-based structural reliability analysis with epistemic uncertainty: a review. *Structural and Multidisciplinary Optimization* 63(6) (2021) 2935–2953. https://doi.org/10.1007/s00158-021-02863-w.

Zhang Q., Li H. MOEA/D: a multiobjective evolutionary algorithm based on decomposition. *IEEE Transactions on Evolutionary Computation* 11(6) (2007) 712–731. https://doi.org/10.1109/TEVC.2007.892759.

Zitzler E., Thiele L. Multiobjective evolutionary algorithms: a comparative case study and the strength Pareto approach. *IEEE Transactions on Evolutionary Computation* 3(4) (1999) 257–271. https://doi.org/10.1109/4235.797969.

Zitzler E., Thiele L., Laumanns M., Fonseca C.M., da Fonseca V.G. Performance assessment of multiobjective optimizers: an analysis and review. *IEEE Transactions on Evolutionary Computation* 7(2) (2003) 117–132. https://doi.org/10.1109/TEVC.2003.810758.

# Statements and Declarations

**Funding.** The author received no funding for this work.

**Competing interests.** The author has no competing interests to declare.

**Author contributions.** Single author: Montassar Zaghdoud (conceptualisation, methodology, experiments, analysis, writing, review and editing).

**Data availability.** The frozen protocols, the code, the parameter and freeze records, the final reports and the final analysis files of all studies reported here, together with both versions of this manuscript, are archived in release V1.0 of the repository https://github.com/MontZ26/Evidential_QGA2E_paper_archive (permanent link: https://github.com/MontZ26/Evidential_QGA2E_paper_archive/releases/tag/V1.0). The raw per-run result files are not included because of their size; they can be regenerated with the code and the seeds stated in each protocol. A public repository for the earlier manuscript contains the generator of that paper, the RC101 file and the raw results of its 20-seed experiments.

**Ethics.** Not applicable: no human participants or animals were involved, and all patient information is simulated.

**Use of AI tools.** The author used Claude (Anthropic) to assist with drafting and editing the manuscript text, preparing tables and figures from the analysis files, and checking cross-references and citations. The experimental design, the experiments, the interpretation of the results and the final content were produced and verified by the author, who takes full responsibility for the manuscript.

