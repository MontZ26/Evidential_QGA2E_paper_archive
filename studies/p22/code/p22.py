"""P22 engine: NSGA-II with guided mutation. Frozen P14/P10/P7 modules UNMODIFIED; boucle de X.nsga2 copiee ici. q computed once per generation from the first front of the parent population (as in p10.run_q), per patient, via p14.make_target(g)."""
import sys, json, random
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p14/code")
import numpy as np, p14
P, R, K, X, p7, p10, p9, p8 = p14.P, p14.R, p14.K, p14.X, p14.p7, p14.p10, p14.p9, p14.p8
Q, POP, GEN = X.Q, X.POP, X.GEN
class _Seeds22:
    def __contains__(self, s): return (10400 <= s <= 10499 or 11700 <= s <= 11714 or s in (7000, 5200))
P.ALLOWED_SEEDS = _Seeds22()
PRM = json.load(open(BASE + "/p14/p14_params.json"))["chosen"]
ARMS = {"GDp": ("V0c", 1.0), "GE": ("V1", 1.0), "GDg6": ("V0c", 6.0), "GEg6": ("V1", 6.0)}   # GEgm: ("V1", gamma_m) from p22_gamma.json
def cond_law(qp, allowed, cur):
    """exact conditional law: q restricted to allowed teams other than the current one, renormalised"""
    other = allowed[allowed != cur]
    if len(other) == 0: return other, None
    pr = np.asarray(qp)[other].astype(float); return other, pr / pr.sum()
def vary_guided(decs, a, b, r_c, r_m, r_g, pc, pm, M, n_p, q, cnt):
    child = decs[a].copy()
    if r_c.rand() < pc: take = r_c.rand(n_p) < 0.5; child = np.where(take, decs[a], decs[b])
    mu = r_m.rand(n_p) < pm; cnt["drawn"] += int(mu.sum())
    for p in np.flatnonzero(mu):
        allowed = np.flatnonzero(M[p]); other = allowed[allowed != child[p]]
        if len(other):
            k = r_m.randint(len(other))                              # stream consumed identically to X.vary
            if q is None: child[p] = other[k]
            else:
                _, pr = cond_law(q[p], allowed, child[p]); u = r_g.rand(); j = int(np.searchsorted(np.cumsum(pr), u, side="right")); j = min(j, len(other) - 1); new = other[j]
                cnt["effective"] += int(new != child[p]); child[p] = new; continue
            cnt["effective"] += 1
    return child
def nsga2_guided(I, qfun, pc=0.9, pmk=1.0, gen=GEN):
    """qfun(src, M) -> (q, md) or None for the unmodified uniform path"""
    n_p, n_t, M, sc, seed = I["n_p"], I["n_t"], I["M"], I["sc"], I["seed"]; random.seed(seed); ev = p14.RecCnt(I); pm = pmk / n_p; elitist = True
    rs_ = lambda nm: P.rs(sc, seed, "nsga_" + nm + ("_el" if elitist else "_ne"))
    r_t, r_c, r_m, r_d = rs_("tour"), rs_("cross"), rs_("mut"), rs_("tie"); r_g = P.rs(sc, seed, "p22_gm")
    decs = Q.init_pop(I); fits = np.array([ev(decs[i]) for i in range(POP)]); cnt = dict(drawn=0, effective=0); dyn = []; mut = M.sum(1) >= 2
    for g in range(gen):
        q = None
        if qfun is not None:
            fr = X.nds(fits); src = decs[fr[0]] if fr[0] else decs[:1]; q, md = qfun(src, M); qq = np.where(q > 0, q, 1.0)
            dyn.append(dict(gen=g, q_ent=float(np.mean(-(q * np.log(qq)).sum(1)[mut])), q_max=float(np.mean(q.max(1)[mut])), src_n=int(len(src))))
        rank, crowd = Q.rank_crowd(fits); kids = np.empty_like(decs)
        for c in range(POP):
            a = Q._tour(rank, crowd, r_t, r_d); b = Q._tour(rank, crowd, r_t, r_d); kids[c] = vary_guided(decs, a, b, r_c, r_m, r_g, pc, pm, M, n_p, q, cnt)
        kf = np.array([ev(kids[i]) for i in range(POP)])
        ad = np.vstack([decs, kids]); af = np.vstack([fits, kf]); sel = X.select_next(ad, af, POP); decs, fits = ad[sel], af[sel]
    return dict(n_eval=ev.n, cnt=cnt, dyn=dyn)
def run_arm22(I, arm, prm=PRM, wd=None, gm=None):
    W = p9.worlds9(I) if wd is None else wd; Aw, Sw = W["nom"]; Is = dict(I); Is["A_true"], Is["S_true"] = Aw, Sw
    if arm == "NSGA2U": qfun = None
    else:
        rule, g = ARMS[arm] if arm != "GEgm" else ("V1", float(gm)); tf = p14.make_target(g); qfun = lambda src, M: tf(src, M, prm["w"], rule, prm["eps"])
    p14.RecCnt.arch = X.Arch(); res = nsga2_guided(Is, qfun)
    F, D = p14.RecCnt.arch.F, p14.RecCnt.arch.D; p14.RecCnt.arch = None; Fo = p14._oracle_eval(I, D)
    return dict(n_eval=res["n_eval"], hv_oracle=float(R.hv(Fo)), hv_search=float(R.hv(F)), F_search=np.asarray(F).tolist(), F_oracle=Fo.tolist(), D=np.asarray(D).tolist(), dyn=res["dyn"], cnt=res["cnt"])
def task22(sc, seed, arms, gm=None, prm=PRM):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    W = p9.worlds9(I); out["conds"] = {a: run_arm22(I, a, prm, W, gm) for a in arms}; return out
