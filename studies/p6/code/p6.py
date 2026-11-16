"""P6 engine (Protocol_P6_Interaction_v2_6). Hybrid probabilistic QIGA (route M: model sample + mutation; route G: two parents from P_t, uniform crossover + mutation),
parental selection T (binary tournaments) / R (uniform), LS on/off. Re-uses the FROZEN P5 modules WITHOUT modifying them. All evaluations in world T.
RANDOM STREAMS (P.rs(scenario, seed, 'p6_'+name)): route (1 rand/child), samp (route M: rand(n_p)), par (R: randint(0,N,2) per route-G child), tour/tie (T: two binary tournaments),
cross (2 draws/child, always), mut, gate (1 rand/child, also when p_LS=0), order, w (LS). Initial population: P5 stream p5_init (identical in every arm of equal N)."""
import os, sys, math, time, random
import numpy as np
P5DIR = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p5"; sys.path.insert(0, P5DIR)
import p5 as K
P, Q, X, Z4, R = K.P, K.Q, K.X, K.Z4, K.R
class _Seeds6:
    def __contains__(self, s): return (6000 <= s <= 6014 or 6050 <= s <= 6099 or 6200 <= s <= 6499 or 6900 <= s <= 6909)
P.ALLOWED_SEEDS = _Seeds6()
BUDGET = K.BUDGET; SC6 = K.SC6; SC3 = K.SC3
ARMS8 = [f"{m}-{s}-{l}" for m in ("C2", "C3") for l in ("on", "off") for s in ("T", "R")]
ARMS = ARMS8 + ["C0b-T", "C0b-T-off"]

def run6(I, mkind, prm, ls_on, sel, budget=BUDGET, diag=None, neutral=False):
    """mkind 'rot' (C2) | 'pbil' (C3); sel 'T'|'R'; ls_on bool. Strategy c (top-k_e crowding from the archive)."""
    diag = diag or {}; n_p, M, sc, seed = I["n_p"], I["M"], I["sc"], I["seed"]; random.seed(seed)
    N = int(prm["N"]); pc = prm["pc"]; eta = prm["eta_k"] / n_p; rho = prm["rho"]
    p_ls = float(prm.get("p_LS", 0.0)) if ls_on else 0.0; k_ls = int(prm.get("k_LS", 0)); rule = prm.get("rule", "dominance")
    ev = X.Cnt(I); arch = K.Archive(n_p); rs_ = lambda nm: P.rs(sc, seed, "p6_" + nm)
    r_route, r_samp, r_par, r_tour, r_tie, r_cross, r_mut, r_gate, r_order, r_w = (rs_(n) for n in ("route", "samp", "par", "tour", "tie", "cross", "mut", "gate", "order", "w"))
    mutable = M.sum(1) >= 2; SH, PRS = K.moves(I)
    cnt = dict(children=0, crossed=0, mutated=0, n_M=0, n_G=0, ins_M=0, ins_G=0, ins_init=0, ls_trig=0, ls_eval=0, ls_dec=0, ls_acc=0, ins_L=0, ins_all=0)
    model = K.Model(I, mkind, prm["eps"], prm.get("delta"), prm.get("lam")); st = dict(t_diag=0.0, div=[], ent=[], conv=[]); next_div = [0, 2000, 4000, 6000]
    def E(d, tag):
        if ev.n >= budget: raise K.Budget()
        f = ev(d); ins = arch.add(d, f); cnt["ins_all"] += int(ins)
        if tag == "M": cnt["ins_M"] += int(ins)
        elif tag == "G": cnt["ins_G"] += int(ins)
        elif tag == "L": cnt["ins_L"] += int(ins)
        else: cnt["ins_init"] += int(ins)
        if diag.get("conv") and ev.n % 100 == 0: t0 = time.perf_counter(); st["conv"].append((ev.n, float(R.hv(arch.F)))); st["t_diag"] += time.perf_counter() - t0
        return f, ins
    t_start = time.perf_counter(); decs = K.init_pop(I, N); fits = np.zeros((N, 3))
    for i in range(N): fits[i], _ = E(decs[i], "I")
    def record_div():
        while next_div and ev.n >= next_div[0]:
            t0 = time.perf_counter(); st["div"].append((next_div.pop(0), Z4.diversity(decs))); st["t_diag"] += time.perf_counter() - t0
    record_div(); gen = 0
    def local_search(d0, f0):
        cnt["ls_trig"] += 1; w = r_w.dirichlet([1.0, 1.0, 1.0]); order = r_order.permutation(len(SH) + len(PRS)); cur, cf = d0.copy(), f0.copy(); n_ev = 0
        for mv in order:
            if n_ev >= k_ls: break
            if mv < len(SH):
                p, t = SH[mv]
                if cur[p] == t: continue
                nd_ = cur.copy(); nd_[p] = t
            else:
                p, q = PRS[mv - len(SH)]; tp, tq = cur[p], cur[q]
                if tp == tq or not M[p, tq] or not M[q, tp]: continue
                nd_ = cur.copy(); nd_[p], nd_[q] = tq, tp
            try: fn, _ = E(nd_, "L")
            except K.Budget: break
            n_ev += 1; cnt["ls_eval"] += 1
            acc = K.dominates(fn, cf) if rule == "dominance" else ((not K.dominates(cf, fn)) and float(w @ fn) < float(w @ cf))
            cnt["ls_dec"] += 1                        # the decision on an already evaluated neighbour is always executed
            if acc: cur, cf = nd_, fn; cnt["ls_acc"] += 1
        return cur, cf
    while ev.n < budget:
        rank = crowd = None
        if sel == "T" and not neutral: rank, crowd = Q.rank_crowd(fits)
        pool_d, pool_f = [], []; partial = False
        for c in range(N):
            if ev.n >= budget: partial = True; break
            route_M = r_route.rand() < rho
            if route_M:
                pa = model.sample(r_samp.rand(n_p)); child = K.vary(pa, pa, r_cross, r_mut, 0.0, eta, M, mutable, cnt); tag = "M"; cnt["n_M"] += 1
            else:
                if sel == "R" or neutral: a, b = r_par.randint(0, N, 2)
                else: a = Q._tour(rank, crowd, r_tour, r_tie); b = Q._tour(rank, crowd, r_tour, r_tie)
                child = K.vary(decs[a], decs[b], r_cross, r_mut, pc, eta, M, mutable, cnt); tag = "G"; cnt["n_G"] += 1
            f, _ = E(child, tag); fd, ff = child, f
            if r_gate.rand() < p_ls and ev.n < budget: fd, ff = local_search(child, f)
            pool_d.append(fd); pool_f.append(ff)
        if pool_d:
            ad = np.vstack([decs, np.array(pool_d)]); af = np.vstack([fits, np.array(pool_f)]); s_ = K.select_next(ad, af, N); decs, fits = ad[s_], af[s_]
        gen += 1; record_div()
        if partial or ev.n >= budget: break                    # final (partial or complete) generation: survival done, NO model update
        model.update(K.distinct(list(arch.top_crowd(int(prm["k_e"])))))
        if diag.get("ent") and gen % 10 == 0: t0 = time.perf_counter(); st["ent"].append((gen, model.entropy())); st["t_diag"] += time.perf_counter() - t0
    wall = time.perf_counter() - t_start - st["t_diag"]
    return dict(front=arch.F.tolist(), n_eval=ev.n, search_time_s=wall, cnt=cnt, n_arch=int(len(arch.F)), gens=gen, div={str(k): v for k, v in st["div"]}, ent=st["ent"], conv=st["conv"], D=arch.D, model=model)

def run_arm6(I, cfg, diag=None):
    if cfg["kind"] == "p6":
        r = run6(I, cfg["mkind"], cfg["prm"], cfg["ls_on"], cfg["sel"], diag=diag); r.pop("D", None); r.pop("model", None); return r
    return K.run_arm(I, cfg, diag)

def task6(sc, seed, cfgs, diag=None):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    out["conds"] = {lab: run_arm6(I, cfg, diag) for lab, cfg in cfgs.items()}; return out
