"""P7 engine (Amendement P7 v0.3 decisions). M1 individual-based evidence: each of the N individuals of the current population (after survival) is a source supporting, for patient i, its own team with strength w
(m({x_j(i)})=w, m(Theta_i)=1-w). Arms: V0c (probabilistic control: p = w*freq + (1-w)*uniform), V1 (Dempster), V2 (Denoeux cautious), all followed by the SAME floor eps (K.floor_renorm).
Loop = P5 loop (two sampled parents, uniform crossover, targeted mutation, LS of P5, archive 200, (mu+lambda) survival, budget 6040); model rebuilt from the population once per generation, never after the last (partial or complete) generation.
Re-uses the frozen P5 modules WITHOUT modifying them. Streams: P.rs(sc, seed, 'p7_'+name); initial population = P5 stream p5_init."""
import os, sys, math, time, random
import numpy as np
P5DIR = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p5"; sys.path.insert(0, P5DIR)
import p5 as K
P, Q, X, Z4, R = K.P, K.Q, K.X, K.Z4, K.R
class _Seeds7:
    def __contains__(self, s): return (7000 <= s <= 7009 or 7100 <= s <= 7114 or 7150 <= s <= 7179 or 7200 <= s <= 7499 or 7900 <= s <= 7909 or s == 5200)
P.ALLOWED_SEEDS = _Seeds7()
BUDGET = K.BUDGET; SC6 = K.SC6; SC3 = K.SC3; RULES = ("V0c", "V1", "V2"); ARMS = ["V0", "V0c", "V1", "V2"]

def population_model(decs, M, w, rule):
    """returns (P_before_floor [n_p,n_t], diag) from the population decs [N,n_p]. Closed forms validated against the general implementations in G0 (T8)."""
    N, n_p = decs.shape; n_t = M.shape[1]; C = np.zeros((n_p, n_t)); np.add.at(C, (np.tile(np.arange(n_p), N), decs.ravel()), 1.0)
    Kp = M.sum(1, keepdims=True); U = M / Kp
    if rule == "V0c": return w * C / N + (1 - w) * U, dict(m_empty=0.0, m_theta=1 - w, fallback=0.0)
    T = C > 0; lu = np.where(T, (C if rule == "V1" else 1.0) * math.log(1 - w), 0.0); L = lu.sum(1, keepdims=True); mT = np.exp(L); u = np.exp(lu)
    mS = np.where(T, (1 - u) * np.exp(L - lu), 0.0); s = mT + mS.sum(1, keepdims=True); fb = (s < 1e-300).ravel()
    Pn = (mS + mT * U) / np.where(s < 1e-300, 1.0, s); Pn = np.where(fb[:, None], U, Pn)
    mut = (M.sum(1) >= 2); return Pn, dict(m_empty=float(np.mean((1 - s.ravel())[mut])), m_theta=float(np.mean(mT.ravel()[mut])), fallback=float(fb[mut].mean()),
                                         betp_vs_freq_L1=float(np.mean(np.abs(Pn - C / N).sum(1)[mut])))

def run7(I, rule, prm, budget=BUDGET, diag=None, audit=False):
    diag = diag or {}; n_p, n_t, M, sc, seed = I["n_p"], I["n_t"], I["M"], I["sc"], I["seed"]; random.seed(seed)
    N = int(prm["N"]); pc = prm["pc"]; eta = prm["eta_k"] / n_p; w = float(prm["w"]); eps = float(prm["eps"]); p_ls = float(prm.get("p_LS", 0.0)); k_ls = int(prm.get("k_LS", 0)); lrule = prm.get("rule", "dominance")
    ev = X.Cnt(I); arch = K.Archive(n_p); rs_ = lambda nm: P.rs(sc, seed, "p7_" + nm)
    r_samp, r_cross, r_mut, r_gate, r_order, r_w = (rs_(n) for n in ("samp", "cross", "mut", "gate", "order", "w"))
    mutable = M.sum(1) >= 2; SH, PRS = K.moves(I); cnt = dict(children=0, crossed=0, mutated=0, ins_child=0, ins_all=0, ls_trig=0, ls_eval=0, ls_acc=0, fallback_events=0)
    model = K.Model(I, "pbil", eps, None, 0.1); st = dict(t_diag=0.0, div=[], ent=[], conv=[], mdiag=[]); next_div = [0, 2000, 4000, 6000]
    aud = dict(gen_cov=[], n1=0, n2=0, nd1=0, acc1=0, nbr1=0, cur_flag_count=0, pat_with_ev=[]) if audit else None
    def E(d):
        if ev.n >= budget: raise K.Budget()
        f = ev(d); ins = arch.add(d, f); cnt["ins_all"] += int(ins)
        if diag.get("conv") and ev.n % 100 == 0: t0 = time.perf_counter(); st["conv"].append((ev.n, float(R.hv(arch.F)))); st["t_diag"] += time.perf_counter() - t0
        return f, ins
    t_start = time.perf_counter(); decs = K.init_pop(I, N); fits = np.zeros((N, 3))
    for i in range(N): fits[i], _ = E(decs[i])
    flags = np.zeros(N, bool)
    def record_div():
        while next_div and ev.n >= next_div[0]:
            t0 = time.perf_counter(); st["div"].append((next_div.pop(0), Z4.diversity(decs))); st["t_diag"] += time.perf_counter() - t0
    record_div(); gen = 0
    def local_search(d0, f0):
        cnt["ls_trig"] += 1; w_ = r_w.dirichlet([1.0, 1.0, 1.0]); order = r_order.permutation(len(SH) + len(PRS)); cur, cf = d0.copy(), f0.copy(); n_ev = 0; ev_pat = set()
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
            if audit:
                if one:
                    aud["n1"] += 1; aud["nd1"] += int(nondom); aud["acc1"] += int(acc)
                    if nondom: ev_pat.add(int(p))
                else: aud["n2"] += 1
            if acc: cur, cf = nd_, fn; cnt["ls_acc"] += 1
        return cur, cf, ev_pat
    while ev.n < budget:
        pool_d, pool_f, pool_fl = [], [], []; partial = False
        for c in range(N):
            if ev.n >= budget: partial = True; break
            pa = model.sample(r_samp.rand(n_p)); pb = model.sample(r_samp.rand(n_p)); child = K.vary(pa, pb, r_cross, r_mut, pc, eta, M, mutable, cnt); f, ins = E(child); cnt["ins_child"] += int(ins); fd, ff = child, f; fl = False
            if r_gate.rand() < p_ls and ev.n < budget:
                fd, ff, evp = local_search(child, f); fl = len(evp) > 0
                if audit and fl: aud["pat_with_ev"].append(len(evp))
            pool_d.append(fd); pool_f.append(ff); pool_fl.append(fl)
        if pool_d:
            ad = np.vstack([decs, np.array(pool_d)]); af = np.vstack([fits, np.array(pool_f)]); fl_all = np.concatenate([flags, np.array(pool_fl)]); sel = K.select_next(ad, af, N); decs, fits, flags = ad[sel], af[sel], fl_all[sel]
        gen += 1; record_div()
        if audit: aud["gen_cov"].append(float(flags.mean()))
        if partial or ev.n >= budget: break
        Pn, md = population_model(decs, M, w, rule); model.P = K.floor_renorm(Pn, M, eps); cnt["fallback_events"] += int(md["fallback"] > 0)
        if diag.get("ent") and gen % 10 == 0:
            t0 = time.perf_counter(); st["ent"].append((gen, model.entropy())); st["mdiag"].append((gen, md)); st["t_diag"] += time.perf_counter() - t0
    wall = time.perf_counter() - t_start - st["t_diag"]
    out = dict(front=arch.F.tolist(), n_eval=ev.n, search_time_s=wall, cnt=cnt, n_arch=int(len(arch.F)), gens=gen, div={str(k): v for k, v in st["div"]}, ent=st["ent"], mdiag=st["mdiag"], conv=st["conv"], model=model)
    if audit: out["audit"] = aud
    return out

def run_arm7(I, cfg, diag=None):
    if cfg["kind"] == "p7":
        r = run7(I, cfg["rule"], cfg["prm"], diag=diag); r.pop("model", None); return r
    return K.run_arm(I, cfg, diag)

def task7(sc, seed, cfgs, diag=None):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    out["conds"] = {lab: run_arm7(I, cfg, diag) for lab, cfg in cfgs.items()}; return out
