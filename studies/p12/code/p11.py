"""P11 engine: DEC (Dependency Entropy Cleaner) before the Dempster combination, on the P5/P7 engine (option A). Frozen P5/P7/P8/P9 modules are used UNMODIFIED; run7 and the GA loop of P5 are re-implemented here as copies with
DEC hooks that are inert when dec is None (G-D0 verifies bit-for-bit equality with p7.run7 / K.run). Protocol_P11_DEC_v0_1_candidate.md section 4:
 cap max_i n_i <= n_max on population U already-evaluated batch U candidate (n_i = #individuals incl. self with similarity >= sigma); minimal-intervention bounded repair of the UNEVALUATED candidate only;
 at most m_max patients changed per repair, at most r_max regenerations per slot, else candidate kept and counted as violation; LS neighbours violating the cap are skipped BEFORE evaluation (no evaluation consumed).
Repair randomness: own stream p11_dec (never consumed when dec is None)."""
import sys, math, time, random, json
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p9/code")
import numpy as np, p9, p8, p7
K, P, R, X, Q, Z4 = p7.K, p7.P, p7.R, p7.X, p7.Q, p7.Z4
class _Seeds11:
    def __contains__(self, s): return (9910 <= s <= 9919 or 9920 <= s <= 9934 or 9940 <= s <= 9969 or 10000 <= s <= 10199 or s == 9805 or s in (7000, 5200))
P.ALLOWED_SEEDS = _Seeds11()
ARMS11 = {"E0": ("V1", False), "E1": ("V1", True), "P0": ("V0c", False), "P1": ("V0c", True), "C0": ("GA", False), "C1": ("GA", True)}

class Dec:
    def __init__(s, sigma, n_max, rho_max, r_max, rng):
        s.sigma, s.n_max, s.m_max_frac, s.r_max, s.rng = float(sigma), int(n_max), float(rho_max), int(r_max), rng
        s.c = dict(repairs=0, mutations=0, violations=0, regen=0, ls_skipped=0, cands=0, cands_repaired=0)
    def counts(s, S, d):
        """neighbour mask of d among S (m,n_p) and similarities"""
        if len(S) == 0: return np.zeros(0, float), np.zeros(0, bool)
        sm = (S == d).mean(1); return sm, sm >= s.sigma - 1e-12
    def ok(s, S, d):
        """cap holds on S U {d}"""
        sm, nb = s.counts(S, d)
        if nb.sum() + 1 > s.n_max: return False
        for j in np.flatnonzero(nb):
            if int(((S == S[j]).mean(1) >= s.sigma - 1e-12).sum()) + 1 > s.n_max: return False
        return True
    def repair(s, S, d, M, mutable):
        """minimal-intervention repair of candidate d against fixed set S; returns (d', ok, n_mut)"""
        n_p = len(d); d = d.copy(); m_max = max(1, int(math.ceil(s.m_max_frac * n_p))); used = 0; s.c["cands"] += 1; first = True
        while not s.ok(S, d):
            if first: s.c["cands_repaired"] += 1; first = False
            sm, nb = s.counts(S, d); idx = np.flatnonzero(nb)
            if len(idx) == 0: break
            block = [j for j in idx if int(((S == S[j]).mean(1) >= s.sigma - 1e-12).sum()) + 1 > s.n_max]
            tgt = block if (nb.sum() + 1 <= s.n_max and block) else list(idx)
            j = tgt[int(np.argmax(sm[tgt]))]; m = int(math.ceil((sm[j] - s.sigma) * n_p)) + 1; m = max(1, m)
            if used + m > m_max: m = m_max - used
            if m <= 0: break
            agree = np.flatnonzero((S[j] == d) & mutable)
            if len(agree) == 0: break
            share = np.array([(S[idx][:, p] == d[p]).sum() for p in agree], float); order = np.lexsort((s.rng.rand(len(agree)), -share)); pick = agree[order[:m]]
            for p in pick:
                al = np.flatnonzero(M[p]); al = al[al != d[p]]
                if len(al) == 0: continue
                d[p] = al[s.rng.randint(len(al))]; used += 1; s.c["mutations"] += 1
            s.c["repairs"] += 1
            if used >= m_max: break
        return d, s.ok(S, d), used

def dep_stats(decs, sigma, n_t):
    N, n_p = decs.shape; Sm = (decs[:, None, :] == decs[None, :, :]).mean(2); ni = (Sm >= sigma - 1e-12).sum(1).astype(float)
    dep = float(np.log(ni).mean() / math.log(N)) if N > 1 else 0.0
    mh = float(np.mean([-(q[q > 0] * np.log(q[q > 0])).sum() for q in (np.bincount(decs[:, p], minlength=n_t) / N for p in range(n_p))]))
    off = Sm[~np.eye(N, dtype=bool)]
    return dict(dep=dep, neff=float((1 / ni).sum()), n_max_obs=float(ni.max()), frac_dup=float((ni > 1).mean()), marg_ent=mh, s_mean=float(off.mean()), s_q=[float(np.quantile(off, q)) for q in (.5, .9, .99)])

def _init_clean(decs, dec, M, mutable, I):
    """initial population cleaned before evaluation by the same rule (sequentially, against already accepted rows)"""
    out = []
    for i in range(len(decs)):
        S = np.array(out) if out else np.empty((0, decs.shape[1]), int); d, ok_, _ = dec.repair(S, decs[i], M, mutable); t = 0
        while not ok_ and t < dec.r_max:
            d = np.array([dec.rng.choice(np.flatnonzero(M[p])) for p in range(len(d))]); d, ok_, _ = dec.repair(S, d, M, mutable); t += 1; dec.c["regen"] += 1
        if not ok_: dec.c["violations"] += 1
        out.append(d)
    return np.array(out)

def run7d(I, rule, prm, dec=None, budget=K.BUDGET, diag=None, sigma_diag=0.5):
    diag = diag or {}; n_p, n_t, M, sc, seed = I["n_p"], I["n_t"], I["M"], I["sc"], I["seed"]; random.seed(seed)
    N = int(prm["N"]); pc = prm["pc"]; eta = prm["eta_k"] / n_p; w = float(prm["w"]); eps = float(prm["eps"]); p_ls = float(prm.get("p_LS", 0.0)); k_ls = int(prm.get("k_LS", 0)); lrule = prm.get("rule", "dominance")
    ev = X.Cnt(I); arch = K.Archive(n_p); rs_ = lambda nm: P.rs(sc, seed, "p7_" + nm)
    r_samp, r_cross, r_mut, r_gate, r_order, r_w = (rs_(n) for n in ("samp", "cross", "mut", "gate", "order", "w"))
    mutable = M.sum(1) >= 2; SH, PRS = K.moves(I); cnt = dict(children=0, crossed=0, mutated=0, ins_child=0, ins_all=0, ls_trig=0, ls_eval=0, ls_acc=0, fallback_events=0)
    model = K.Model(I, "pbil", eps, None, 0.1); st = dict(div=[], dyn=[]); next_div = [0, 2000, 4000, 6000]
    def E(d):
        if ev.n >= budget: raise K.Budget()
        f = ev(d); ins = arch.add(d, f); cnt["ins_all"] += int(ins); return f, ins
    decs = K.init_pop(I, N)
    if dec is not None: decs = _init_clean(decs, dec, M, mutable, I)
    fits = np.zeros((N, 3))
    for i in range(N): fits[i], _ = E(decs[i])
    anc = np.eye(N, dtype=bool) if diag.get("anc") else None
    def record_div():
        while next_div and ev.n >= next_div[0]: st["div"].append((next_div.pop(0), Z4.diversity(decs)))
    record_div(); gen = 0
    def dyn(g):
        if diag.get("snap"): st.setdefault("snap", []).append((g, decs.tolist()))
        d = dep_stats(decs, dec.sigma if dec else sigma_diag, n_t); d["gen"] = g; d["model_ent"] = model.entropy()
        if anc is not None: d["anc_distinct"] = int((anc.sum(0) > 0).sum()); d["anc_top"] = float(anc.mean(0).max())
        st["dyn"].append(d)
    dyn(0)
    def local_search(d0, f0, base):
        cnt["ls_trig"] += 1; w_ = r_w.dirichlet([1.0, 1.0, 1.0]); order = r_order.permutation(len(SH) + len(PRS)); cur, cf = d0.copy(), f0.copy(); n_ev = 0
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
            if dec is not None and not dec.ok(base, nd_): dec.c["ls_skipped"] += 1; continue
            try: fn, _ = E(nd_)
            except K.Budget: break
            n_ev += 1; cnt["ls_eval"] += 1; nondom = not K.dominates(cf, fn)
            acc = K.dominates(fn, cf) if lrule == "dominance" else (nondom and float(w_ @ fn) < float(w_ @ cf))
            if acc: cur, cf = nd_, fn; cnt["ls_acc"] += 1
        return cur, cf
    while ev.n < budget:
        pool_d, pool_f, pool_a = [], [], []; partial = False
        for c in range(N):
            if ev.n >= budget: partial = True; break
            tries = 0
            while True:
                pa = model.sample(r_samp.rand(n_p)); pb = model.sample(r_samp.rand(n_p)); child = K.vary(pa, pb, r_cross, r_mut, pc, eta, M, mutable, cnt)
                if dec is None: break
                base = np.vstack([decs] + ([np.array(pool_d)] if pool_d else [])); child, ok_, _ = dec.repair(base, child, M, mutable)
                if ok_ or tries >= dec.r_max:
                    if not ok_: dec.c["violations"] += 1
                    break
                tries += 1; dec.c["regen"] += 1
            f, ins = E(child); cnt["ins_child"] += int(ins); fd, ff = child, f
            if r_gate.rand() < p_ls and ev.n < budget:
                base = np.vstack([decs] + ([np.array(pool_d)] if pool_d else [])) if dec is not None else None; fd, ff = local_search(child, f, base)
            pool_d.append(fd); pool_f.append(ff)
            if anc is not None: pool_a.append(anc[int(np.argmax((decs == child).mean(1)))].copy())
        if pool_d:
            ad = np.vstack([decs, np.array(pool_d)]); af = np.vstack([fits, np.array(pool_f)]); sel = K.select_next(ad, af, N)
            if anc is not None: anc = np.vstack([anc, np.array(pool_a)])[sel]
            decs, fits = ad[sel], af[sel]
        gen += 1; record_div()
        if partial or ev.n >= budget: break
        Pn, md = p7.population_model(decs, M, w, rule); model.P = K.floor_renorm(Pn, M, eps); cnt["fallback_events"] += int(md["fallback"] > 0); dyn(gen)
    return dict(front=arch.F.tolist(), n_eval=ev.n, cnt=cnt, n_arch=int(len(arch.F)), gens=gen, div={str(k): v for k, v in st["div"]}, dyn=st["dyn"], dec=(dec.c if dec else None), final_decs=decs, snap=st.get("snap"))

def run_gad(I, prm, dec=None, budget=K.BUDGET, diag=None, sigma_diag=0.5):
    """copy of the 'ga' branch of K.run (C0b) with DEC hooks"""
    diag = diag or {}; n_p, n_t, M, sc, seed = I["n_p"], I["n_t"], I["M"], I["sc"], I["seed"]; random.seed(seed)
    N = int(prm["N"]); pc = prm["pc"]; eta = prm["eta_k"] / n_p; p_ls = prm.get("p_LS", 0.0); k_ls = int(prm.get("k_LS", 0)); rule = prm.get("rule", "dominance")
    ev = X.Cnt(I); arch = K.Archive(n_p); rs_ = lambda nm: P.rs(sc, seed, "p5_" + nm)
    r_samp, r_tour, r_tie, r_cross, r_mut, r_gate, r_order, r_w = (rs_(n) for n in ("samp", "tour", "tie", "cross", "mut", "gate", "order", "w"))
    mutable = M.sum(1) >= 2; SH, PRS = K.moves(I); cnt = dict(children=0, crossed=0, mutated=0, ins_child=0, ins_all=0, ls_trig=0, ls_eval=0, ls_acc=0); st = dict(div=[], dyn=[]); next_div = [0, 2000, 4000, 6000]
    def E(d):
        if ev.n >= budget: raise K.Budget()
        f = ev(d); ins = arch.add(d, f); cnt["ins_all"] += int(ins); return f, ins
    decs = K.init_pop(I, N)
    if dec is not None: decs = _init_clean(decs, dec, M, mutable, I)
    fits = np.zeros((N, 3))
    for i in range(N): fits[i], _ = E(decs[i])
    def record_div():
        while next_div and ev.n >= next_div[0]: st["div"].append((next_div.pop(0), Z4.diversity(decs)))
    record_div(); gen = 0
    def dyn(g):
        if diag.get("snap"): st.setdefault("snap", []).append((g, decs.tolist()))
        d = dep_stats(decs, dec.sigma if dec else sigma_diag, n_t); d["gen"] = g; st["dyn"].append(d)
    dyn(0)
    def local_search(d0, f0, base):
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
            if dec is not None and not dec.ok(base, nd_): dec.c["ls_skipped"] += 1; continue
            try: fn, _ = E(nd_)
            except K.Budget: break
            n_ev += 1; cnt["ls_eval"] += 1
            acc = K.dominates(fn, cf) if rule == "dominance" else ((not K.dominates(cf, fn)) and float(w @ fn) < float(w @ cf))
            if acc: cur, cf = nd_, fn; cnt["ls_acc"] += 1
        return cur, cf
    while ev.n < budget:
        rank, crowd = Q.rank_crowd(fits); pool_d, pool_f = [], []; partial = False
        for c in range(N):
            if ev.n >= budget: partial = True; break
            tries = 0
            while True:
                a = Q._tour(rank, crowd, r_tour, r_tie); b = Q._tour(rank, crowd, r_tour, r_tie); child = K.vary(decs[a], decs[b], r_cross, r_mut, pc, eta, M, mutable, cnt)
                if dec is None: break
                base = np.vstack([decs] + ([np.array(pool_d)] if pool_d else [])); child, ok_, _ = dec.repair(base, child, M, mutable)
                if ok_ or tries >= dec.r_max:
                    if not ok_: dec.c["violations"] += 1
                    break
                tries += 1; dec.c["regen"] += 1
            f, ins = E(child); cnt["ins_child"] += int(ins); fd, ff = child, f
            if r_gate.rand() < p_ls and ev.n < budget:
                base = np.vstack([decs] + ([np.array(pool_d)] if pool_d else [])) if dec is not None else None; fd, ff = local_search(child, f, base)
            pool_d.append(fd); pool_f.append(ff)
        if pool_d:
            ad = np.vstack([decs, np.array(pool_d)]); af = np.vstack([fits, np.array(pool_f)]); sel = K.select_next(ad, af, N); decs, fits = ad[sel], af[sel]
        gen += 1; record_div(); dyn(gen)
        if partial or ev.n >= budget: break
    return dict(front=arch.F.tolist(), n_eval=ev.n, cnt=cnt, n_arch=int(len(arch.F)), gens=gen, div={str(k): v for k, v in st["div"]}, dyn=st["dyn"], dec=(dec.c if dec else None), final_decs=decs, snap=st.get("snap"))

def make_dec(I, prm):
    return Dec(prm["sigma"], prm["n_max"], prm["rho_max"], prm["r_max"], P.rs(I["sc"], I["seed"], "p11_dec"))

def run_one11(I, arm, dprm=None, diag=None, wd=None):
    """arm in ARMS11; world = nominal evidential (as P9/E, P9/D', C0b/B); oracle re-evaluation post hoc."""
    kind, on = ARMS11[arm]; W = p8.worlds_for(I) if wd is None else wd; Aw, Sw = W["nom"]; Is = dict(I); Is["A_true"], Is["S_true"] = Aw, Sw
    del p8._LAST[:]; K.Archive = p8.CapArchive; dec = make_dec(I, dprm) if on else None
    try:
        if kind == "GA": r = run_gad(Is, p8.prm_ga(), dec, diag=diag, sigma_diag=(dprm or {}).get("sigma", 0.5))
        else: r = run7d(Is, kind, dict(p8.prm_p7()), dec, diag=diag, sigma_diag=(dprm or {}).get("sigma", 0.5))
    finally: K.Archive = p8._orig_Archive
    arch = p8._LAST[-1]; Dd = arch.D.copy(); Fs = arch.F.copy(); Ao, So = I["A_true"], I["S_true"]
    Fo = np.array([P.evaluate(d, I, Ao, So) for d in Dd]) if len(Dd) else np.empty((0, 3))
    fd = r.pop("final_decs", None)
    out = dict(n_eval=r["n_eval"], D=Dd.tolist(), F_search=Fs.tolist(), F_oracle=Fo.tolist(), hv_search=float(R.hv(Fs)), hv_oracle=float(R.hv(Fo)), gens=r["gens"], cnt=r["cnt"], dyn=r["dyn"], dec=r["dec"], snap=r.get("snap"))
    return out
def task11(sc, seed, arms, dprm=None, diag=None):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    W = p8.worlds_for(I); out["conds"] = {a: run_one11(I, a, dprm, diag, W) for a in arms}; return out
