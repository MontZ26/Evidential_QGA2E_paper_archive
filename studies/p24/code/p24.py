"""P24 engine (new file; frozen P3..P23 code used UNMODIFIED). Arms are specs (kind, w, sigma, gamma).
Kinds: E (Dempster, V1), Dp (V0c), DA (p15.da_model lambda=1, sigma), Dg (V0c hardened by gamma, floor eps).
run_q24 is a copy of p23.run_q23 with an INERT log hook that also stores per-patient decoded counts (uint8, out of POP children). No RNG use, no state change (T9)."""
import sys, os, json, math, random
HERE = os.path.dirname(os.path.abspath(__file__)); BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p23/code"); sys.path.insert(0, BASE + "/p15/code")
import numpy as np, p23
from p23 import P, X, K, R, p7, p9, p11, p14, p15, harden
class _Seeds24:
    def __contains__(self, s): return (12000 <= s <= 12099 or 13700 <= s <= 13714 or 13900 <= s <= 13909 or 12700 <= s <= 12714 or 12900 <= s <= 12909 or 11200 <= s <= 11209 or s in (10400, 10401, 9290, 7000, 5200))
P.ALLOWED_SEEDS = _Seeds24()
POP, GEN, LOGG = P.POP, P.GEN, p23.LOGG
GAMMA_GRID = [1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 10.0, 12.0, 16.0]
W_LIST = [0.15, 0.3, 0.5, 0.7]; SIGMAS = [0.6, 0.8]; EPS = 0.02
def aid(kind, w, sigma=None, gamma=None):
    if kind == "E": return "E_w%g" % w
    if kind == "Dp": return "Dp_w%g" % w
    if kind == "DA": return "DA_w%g_s%g" % (w, sigma)
    if kind == "Dg": return "Dg_w%g_g%g" % (w, gamma)
def spec(a):
    """arm id -> (kind, w, sigma, gamma)"""
    t = a.split("_"); kind = t[0]; w = float(t[1][1:]); s = float(t[2][1:]) if kind == "DA" else None; g = float(t[2][1:]) if kind == "Dg" else None
    return kind, w, s, g
def make_tfun24(a):
    kind, w, s, g = spec(a)
    def f(src, M, _w, eps):
        if kind == "E": Pn, md = p7.population_model(src, M, w, "V1")
        elif kind == "Dp": Pn, md = p7.population_model(src, M, w, "V0c")
        elif kind == "DA": Pn, md = p15.da_model(src, M, w, s, 1.0)
        elif kind == "Dg": Pn, md = p7.population_model(src, M, w, "V0c"); Pn = harden(Pn, M, g)
        return K.floor_renorm(Pn, M, eps), md
    return f
def run_q24(I, tfun, eps, log=None, fqlog=None):
    n_p, n_t, M, sc, seed = I["n_p"], I["n_t"], I["M"], I["sc"], I["seed"]; random.seed(seed); ev = X.Cnt(I); delta = P.DELTA; mutable = M.sum(1) >= 2
    th, decs, dr, rng = X.init_qga(I); fits = np.array([ev(decs[i]) for i in range(POP)]); arch = X.Arch(); arch.add(decs, fits); dyn = []
    def rec(g, src=None, q=None, md=None):
        d = p11.dep_stats(decs, 0.7, n_t); d["gen"] = g
        if src is not None and len(src) > 1: ds = p11.dep_stats(src, 0.7, n_t); d["src_n"] = int(len(src)); d["src_dep"] = ds["dep"]; d["src_neff"] = ds["neff"]; d["src_nmax"] = ds["n_max_obs"]
        elif src is not None: d["src_n"] = 1
        if q is not None:
            qq = np.where(q > 0, q, 1.0); d["q_ent"] = float(np.mean(-(q * np.log(qq)).sum(1)[mutable])); d["q_max"] = float(np.mean(q.max(1)[mutable]))
        if md is not None: d.update(md)
        dyn.append(d)
    rec(0)
    for g in range(GEN):
        if g == 0: sel = X.select_next(decs, fits, POP); th, decs, fits = th[sel], decs[sel], fits[sel]
        fr = X.nds(fits); src = decs[fr[0]] if fr[0] else decs[:1]; q, md = tfun(src, M, None, eps)
        nth = np.empty_like(th); new = np.empty_like(decs)
        for i in range(POP):
            nth[i] = np.clip(th[i] + delta * (q - np.eye(n_t)[decs[i]]), 0.0, P.HALF) * M
            ux = rng.rand(n_p, n_t); ur = rng.rand(n_p); new[i] = P.collapse_r(nth[i], M, ux, ur)
        if log is not None and g in LOGG:      # inert diagnostics
            s2 = np.sin(nth) ** 2 * M; sn = s2 / np.maximum(s2.sum(2, keepdims=True), 1e-300); cnt = np.zeros((n_p, n_t))
            for i in range(POP): np.add.at(cnt, (np.arange(n_p), new[i]), 1.0)
            fq = cnt / POP; fqq = np.where(fq > 0, fq, 1.0)
            log.append(dict(gen=g + 1, ang_max_raw=float(s2.max(2)[:, mutable].mean()), ang_max_norm=float(sn.max(2)[:, mutable].mean()), dec_max=float(fq.max(1)[mutable].mean()), dec_ent=float(np.mean(-(fq * np.log(fqq)).sum(1)[mutable])), L1_dec_target=float(np.abs(fq - q).sum(1)[mutable].mean()), q_max=float(q.max(1)[mutable].mean())))
            if fqlog is not None: fqlog[g + 1] = cnt.astype(np.uint8)
        nf = np.array([ev(new[i]) for i in range(POP)]); arch.add(new, nf)
        ath = np.concatenate([th, nth]); ad = np.vstack([decs, new]); af = np.vstack([fits, nf]); sel = X.select_next(ad, af, POP); th, decs, fits = ath[sel], ad[sel], af[sel]
        rec(g + 1, src, q, md)
    return dict(F=arch.F, D=arch.D, n_eval=ev.n, dyn=dyn)
def run_arm24(I, a, wd=None, oracle=True, logging=True):
    W = p9.worlds9(I) if wd is None else wd; Aw, Sw = W["nom"]; Is = dict(I); Is["A_true"], Is["S_true"] = Aw, Sw
    lg = [] if logging else None; fql = {} if logging else None; r = run_q24(Is, make_tfun24(a), EPS, lg, fql)
    out = dict(n_eval=r["n_eval"], dyn=r["dyn"], log=lg)
    if oracle:
        Fo = p14._oracle_eval(I, r["D"]); out.update(hv_oracle=float(R.hv(Fo)), hv_search=float(R.hv(r["F"])), F_search=np.asarray(r["F"]).tolist(), F_oracle=Fo.tolist(), D=np.asarray(r["D"]).tolist())
    return out, fql
def task24(sc, seed, arms, oracle=True, logging=True):
    """returns (json-able dict, dict of npz arrays 'arm|gen' -> uint8 counts, plus 'M' mask)"""
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"]); npz = {}
    if not I["feasible"]: return out, npz
    W = p9.worlds9(I); out["conds"] = {}
    for a in arms:
        o, fql = run_arm24(I, a, W, oracle, logging); out["conds"][a] = o
        if logging:
            for g, c in fql.items(): npz["%s|%d" % (a, g)] = c
    if logging: npz["M"] = np.asarray(I["M"]).astype(np.uint8)
    return out, npz
