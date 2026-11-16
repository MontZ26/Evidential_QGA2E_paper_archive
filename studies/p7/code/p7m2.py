"""P7 M2 extension (descriptive arms V0c-M2, V1-M2, V2-M2; G1 retained M2: coverage 83.7% >= 30%). Evidence of individual j on patient i:
A_i(x_j) = {x_j(i)} U L_i(x_j), L_i = teams of evaluated 1-shift neighbours (from LS) NOT dominated by their parent (accepted or rejected, D7-8), swaps excluded; m(A_i)=w, m(Theta_i)=1-w; A_i=Theta_i -> vacuous.
Individuals without any LS episode are vacuous sources (m(Theta_i)=1): no effect on V1/V2, uniform pignistic term (q=U) in V0c (all N individuals averaged, r_j=1). Same eps floor, loop and budget as M1 arms.
Combination on subset vectors of size 2^n_t: Dempster: c copies of a set -> m(A)=1-(1-w)^c; cautious: each distinct set once with weight (1-w) (G0 T7)."""
import os, sys, math, time, random
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p7
from p7 import K, P, Q, X, Z4, R
_B = {}
def _tables(n_t):
    if n_t not in _B:
        S = np.arange(1 << n_t); card = np.array([bin(s).count("1") for s in S]); B = np.zeros((1 << n_t, n_t))
        for k in range(n_t): B[:, k] = ((S >> k) & 1) / np.maximum(card, 1)
        B[0] = 0.0; _B[n_t] = (S, B)
    return _B[n_t]
def model_m2(decs, Lm, has, M, w, rule):
    """decs [N,n_p]; Lm [N,n_p] int bitmask of alternative teams; has [N] bool. returns (P before floor, diag)"""
    N, n_p = decs.shape; n_t = M.shape[1]; S, B = _tables(n_t); out = np.zeros((n_p, n_t)); me = []; fb = 0
    for p in range(n_p):
        E = int(sum(1 << t for t in np.flatnonzero(M[p]))); Kp = int(M[p].sum()); Ucat = M[p] / Kp
        A = ((1 << decs[:, p]) | Lm[:, p]) if True else None; A = np.where(has, A, E)             # vacuous source = Theta
        if rule == "V0c":
            q = np.zeros(n_t)
            for a in A:
                msk = np.array([(a >> t) & 1 for t in range(n_t)], float); ca = msk.sum(); q += w * msk / ca + (1 - w) * Ucat
            out[p] = q / N; continue
        sets, cnts = np.unique(A[A != E], return_counts=True); m = np.zeros(1 << n_t); m[E] = 1.0
        for a, c in zip(sets, cnts):
            s = (1 - (1 - w) ** int(c)) if rule == "V1" else w
            new = (1 - s) * m; np.add.at(new, S & int(a), s * m); m = new
        sm = m[1:].sum()
        if sm < 1e-300: out[p] = Ucat; fb += 1; continue
        out[p] = (m[1:] @ B[1:]) / sm
        if Kp >= 2: me.append(1 - sm)
    return out, dict(m_empty=float(np.mean(me)) if me else 0.0, fallback=fb)
def run7m2(I, rule, prm, budget=p7.BUDGET, diag=None):
    diag = diag or {}; n_p, n_t, M, sc, seed = I["n_p"], I["n_t"], I["M"], I["sc"], I["seed"]; random.seed(seed)
    N = int(prm["N"]); pc = prm["pc"]; eta = prm["eta_k"] / n_p; w = float(prm["w"]); eps = float(prm["eps"]); p_ls = float(prm.get("p_LS", 0.0)); k_ls = int(prm.get("k_LS", 0)); lrule = prm.get("rule", "dominance")
    ev = X.Cnt(I); arch = K.Archive(n_p); rs_ = lambda nm: P.rs(sc, seed, "p7_" + nm)
    r_samp, r_cross, r_mut, r_gate, r_order, r_w = (rs_(n) for n in ("samp", "cross", "mut", "gate", "order", "w"))
    mutable = M.sum(1) >= 2; SH, PRS = K.moves(I); cnt = dict(children=0, crossed=0, mutated=0, ins_child=0, ins_all=0, ls_trig=0, ls_eval=0, ls_acc=0, fallback_events=0)
    model = K.Model(I, "pbil", eps, None, 0.1); st = dict(t_diag=0.0, div=[], ent=[], conv=[], mdiag=[]); next_div = [0, 2000, 4000, 6000]
    def E(d):
        if ev.n >= budget: raise K.Budget()
        f = ev(d); ins = arch.add(d, f); cnt["ins_all"] += int(ins)
        if diag.get("conv") and ev.n % 100 == 0: t0 = time.perf_counter(); st["conv"].append((ev.n, float(R.hv(arch.F)))); st["t_diag"] += time.perf_counter() - t0
        return f, ins
    t_start = time.perf_counter(); decs = K.init_pop(I, N); fits = np.zeros((N, 3))
    for i in range(N): fits[i], _ = E(decs[i])
    Lm = np.zeros((N, n_p), np.int64); has = np.zeros(N, bool)
    def record_div():
        while next_div and ev.n >= next_div[0]:
            t0 = time.perf_counter(); st["div"].append((next_div.pop(0), Z4.diversity(decs))); st["t_diag"] += time.perf_counter() - t0
    record_div(); gen = 0
    def local_search(d0, f0):
        cnt["ls_trig"] += 1; w_ = r_w.dirichlet([1.0, 1.0, 1.0]); order = r_order.permutation(len(SH) + len(PRS)); cur, cf = d0.copy(), f0.copy(); n_ev = 0; Lc = np.zeros(n_p, np.int64); any_ = False
        for mv in order:
            if n_ev >= k_ls: break
            if mv < len(SH):
                p, t = SH[mv]
                if cur[p] == t: continue
                nd_ = cur.copy(); nd_[p] = t; one = True
            else:
                p, q = PRS[mv - len(SH)]; tp, tq = cur[p], cur[q]
                if tp == tq or not M[p, tq] or not M[q, tp]: continue
                nd_ = cur.copy(); nd_[p], nd_[q] = tq, tp; one = False
            try: fn, _ = E(nd_)
            except K.Budget: break
            n_ev += 1; cnt["ls_eval"] += 1; nondom = not K.dominates(cf, fn)
            acc = K.dominates(fn, cf) if lrule == "dominance" else (nondom and float(w_ @ fn) < float(w_ @ cf))
            if one and nondom: Lc[p] |= (1 << int(t)); any_ = True
            if acc: cur, cf = nd_, fn; cnt["ls_acc"] += 1
        return cur, cf, Lc, any_
    while ev.n < budget:
        pool_d, pool_f, pool_L, pool_h = [], [], [], []; partial = False
        for c in range(N):
            if ev.n >= budget: partial = True; break
            pa = model.sample(r_samp.rand(n_p)); pb = model.sample(r_samp.rand(n_p)); child = K.vary(pa, pb, r_cross, r_mut, pc, eta, M, mutable, cnt); f, ins = E(child); cnt["ins_child"] += int(ins); fd, ff = child, f; Lc = np.zeros(n_p, np.int64); hh = False
            if r_gate.rand() < p_ls and ev.n < budget: fd, ff, Lc, hh = local_search(child, f)
            pool_d.append(fd); pool_f.append(ff); pool_L.append(Lc); pool_h.append(hh)
        if pool_d:
            ad = np.vstack([decs, np.array(pool_d)]); af = np.vstack([fits, np.array(pool_f)]); aL = np.vstack([Lm, np.array(pool_L)]); ah = np.concatenate([has, np.array(pool_h)])
            sel = K.select_next(ad, af, N); decs, fits, Lm, has = ad[sel], af[sel], aL[sel], ah[sel]
        gen += 1; record_div()
        if partial or ev.n >= budget: break
        Pn, md = model_m2(decs, Lm, has, M, w, rule); model.P = K.floor_renorm(Pn, M, eps); cnt["fallback_events"] += int(md["fallback"] > 0)
        if diag.get("ent") and gen % 10 == 0: t0 = time.perf_counter(); st["ent"].append((gen, model.entropy())); st["mdiag"].append((gen, dict(md, evidence_share=float(has.mean())))); st["t_diag"] += time.perf_counter() - t0
    wall = time.perf_counter() - t_start - st["t_diag"]
    return dict(front=arch.F.tolist(), n_eval=ev.n, search_time_s=wall, cnt=cnt, n_arch=int(len(arch.F)), gens=gen, div={str(k): v for k, v in st["div"]}, ent=st["ent"], mdiag=st["mdiag"], conv=st["conv"], model=model)
def run_arm7m2(I, cfg, diag=None):
    if cfg["kind"] == "p7" and cfg.get("m2"): r = run7m2(I, cfg["rule"], cfg["prm"], diag=diag); r.pop("model", None); return r
    return p7.run_arm7(I, cfg, diag)
def task7m2(sc, seed, cfgs, diag=None):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    out["conds"] = {lab: run_arm7m2(I, cfg, diag) for lab, cfg in cfgs.items()}; return out
