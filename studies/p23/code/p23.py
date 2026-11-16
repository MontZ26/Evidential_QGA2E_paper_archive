"""P23 engine. QGA2-E with first-front population target; arms: E, DA(lambda), Dg(gamma), R_rho (continuous pairwise dependence), R_mix (simplified mixed rule).
Frozen modules (P3..P22) are used UNMODIFIED. run_q23 is a copy of p10.run_q with the target function passed in and an INERT log hook (no RNG use, no state change; T13).
Targets act on source populations = first non-dominated front, like P15."""
import sys, math, random, json
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p15/code")
import numpy as np, p15, p14, p10, p11, p9, p8, p7
K, P, R, X = p7.K, p7.P, p7.R, p7.X
class _Seeds23:
    def __contains__(self, s): return (12000 <= s <= 12099 or 12700 <= s <= 12714 or 12900 <= s <= 12909 or 11200 <= s <= 11209 or s in (10400, 10401, 9290, 7000, 5200))
P.ALLOWED_SEEDS = _Seeds23()
POP, GEN = P.POP, P.GEN
LOGG = (0, 24, 49, 99, 149)   # children generated at these loop indices -> generations 1, 25, 50, 100, 150
ARMS23 = {"E": ("E", None), "DA25": ("DA", 0.25), "DA50": ("DA", 0.5), "DA100": ("DA", 1.0), "Dg25": ("Dg", "DA25"), "Dg50": ("Dg", "DA50"), "Dg100": ("Dg", "DA100"), "RHO": ("RHO", None), "MIX": ("MIX", None)}
def dempster_cnt(nt, M, w):
    """Dempster closed form on simple supports with (possibly fractional) effective counts nt; same expression order as p15.da_model/p7 V1."""
    Kp = M.sum(1, keepdims=True); U = M / Kp; T = nt > 0
    lu = np.where(T, nt * math.log(1 - w), 0.0); L = lu.sum(1, keepdims=True); mT = np.exp(L); u = np.exp(lu)
    mS = np.where(T, (1 - u) * np.exp(L - lu), 0.0); s = mT + mS.sum(1, keepdims=True); fb = (s < 1e-300).ravel()
    Pn = (mS + mT * U) / np.where(s < 1e-300, 1.0, s); Pn = np.where(fb[:, None], U, Pn); mut = (M.sum(1) >= 2)
    return Pn, dict(m_empty=float(np.mean((1 - s.ravel())[mut])), m_theta=float(np.mean((mT / np.where(s < 1e-300, 1.0, s)).ravel()[mut])), fallback=float(fb[mut].mean()))
def rho_matrix_alpha(src, Rho):
    """alpha_i(p) = 1/(1 + sum_{j != i, x_j(p) = x_i(p)} Rho_ij) ; Rho [N,N] with zero diagonal."""
    agree = (src[:, None, :] == src[None, :, :]).astype(float)
    return 1.0 / (1.0 + np.einsum("ij,ijp->ip", Rho, agree))
def counts_from_alpha(src, alpha, n_t):
    N, n_p = src.shape; nt = np.zeros((n_p, n_t))
    for i in range(N): np.add.at(nt, (np.arange(n_p), src[i]), alpha[i])
    return nt
def sim_matrix(src): return (src[:, None, :] == src[None, :, :]).mean(2)
def rho_model(src, M, w, rho0):
    N = len(src); S = sim_matrix(src); Rho = rho0 * S; np.fill_diagonal(Rho, 0.0)
    alpha = rho_matrix_alpha(src, Rho); nt = counts_from_alpha(src, alpha, M.shape[1]); Pn, md = dempster_cnt(nt, M, w); mut = (M.sum(1) >= 2)
    md["alpha_mean"] = float(alpha.mean()); md["neff_ratio"] = float(nt.sum(1)[mut].mean() / N); return Pn, md
def mix_model(src, M, w, gmix):
    P1, m1 = p7.population_model(src, M, w, "V1"); P2, m2 = p7.population_model(src, M, w, "V2")
    return gmix * P1 + (1 - gmix) * P2, dict(m_empty=gmix * m1["m_empty"] + (1 - gmix) * m2["m_empty"], m_theta=gmix * m1["m_theta"] + (1 - gmix) * m2["m_theta"], fallback=0.0)
def harden(Pn, M, g):
    Pg = np.where(M > 0, np.power(np.maximum(Pn, 0.0), g), 0.0); return Pg / Pg.sum(1, keepdims=True)
def make_tfun(arm, prm):
    kind, par = ARMS23[arm]
    def f(src, M, w, eps):
        if kind == "E": Pn, md = p7.population_model(src, M, w, "V1")
        elif kind == "DA": Pn, md = p15.da_model(src, M, w, prm["sigma"], par)
        elif kind == "Dg":
            Pn, md = p7.population_model(src, M, w, "V0c"); Pn = harden(Pn, M, prm["gamma"][par])
        elif kind == "RHO": Pn, md = rho_model(src, M, w, prm["rho0"])
        elif kind == "MIX": Pn, md = mix_model(src, M, w, prm["gmix"])
        return K.floor_renorm(Pn, M, eps), md
    return f
def run_q23(I, tfun, w, eps, log=None):
    n_p, n_t, M, sc, seed = I["n_p"], I["n_t"], I["M"], I["sc"], I["seed"]; random.seed(seed); ev = X.Cnt(I); delta = P.DELTA; mutable = M.sum(1) >= 2
    th, decs, dr, rng = X.init_qga(I); fits = np.array([ev(decs[i]) for i in range(POP)]); arch = X.Arch(); arch.add(decs, fits); dyn = []
    def rec(g, src=None, q=None, md=None):
        d = p11.dep_stats(decs, 0.7, n_t); d["gen"] = g
        if src is not None and len(src) > 1: ds = p11.dep_stats(src, 0.7, n_t); d["src_n"] = int(len(src)); d["src_dep"] = ds["dep"]; d["src_neff"] = ds["neff"]; d["src_nmax"] = ds["n_max_obs"]
        elif src is not None: d["src_n"] = 1
        if q is not None:
            mut = M.sum(1) >= 2; qq = np.where(q > 0, q, 1.0); d["q_ent"] = float(np.mean(-(q * np.log(qq)).sum(1)[mut])); d["q_max"] = float(np.mean(q.max(1)[mut]))
        if md is not None: d.update(md)
        dyn.append(d)
    rec(0)
    for g in range(GEN):
        if g == 0: sel = X.select_next(decs, fits, POP); th, decs, fits = th[sel], decs[sel], fits[sel]
        fr = X.nds(fits); src = decs[fr[0]] if fr[0] else decs[:1]; q, md = tfun(src, M, w, eps)
        nth = np.empty_like(th); new = np.empty_like(decs)
        for i in range(POP):
            nth[i] = np.clip(th[i] + delta * (q - np.eye(n_t)[decs[i]]), 0.0, P.HALF) * M
            ux = rng.rand(n_p, n_t); ur = rng.rand(n_p); new[i] = P.collapse_r(nth[i], M, ux, ur)
        if log is not None and g in LOGG:      # inert diagnostics: no RNG, no mutation
            s2 = np.sin(nth) ** 2 * M; sn = s2 / np.maximum(s2.sum(2, keepdims=True), 1e-300); fq = np.zeros((n_p, n_t))
            for i in range(POP): np.add.at(fq, (np.arange(n_p), new[i]), 1.0)
            fq /= POP; fqq = np.where(fq > 0, fq, 1.0)
            log.append(dict(gen=g + 1, ang_max_raw=float(s2.max(2)[:, mutable].mean()), ang_max_norm=float(sn.max(2)[:, mutable].mean()), dec_max=float(fq.max(1)[mutable].mean()), dec_ent=float(np.mean(-(fq * np.log(fqq)).sum(1)[mutable])), L1_dec_target=float(np.abs(fq - q).sum(1)[mutable].mean()), q_max=float(q.max(1)[mutable].mean())))
        nf = np.array([ev(new[i]) for i in range(POP)]); arch.add(new, nf)
        ath = np.concatenate([th, nth]); ad = np.vstack([decs, new]); af = np.vstack([fits, nf]); sel = X.select_next(ad, af, POP); th, decs, fits = ath[sel], ad[sel], af[sel]
        rec(g + 1, src, q, md)
    return dict(F=arch.F, D=arch.D, n_eval=ev.n, dyn=dyn)
def run_arm23(I, arm, prm, wd=None, oracle=True, logging=True):
    W = p9.worlds9(I) if wd is None else wd; Aw, Sw = W["nom"]; Is = dict(I); Is["A_true"], Is["S_true"] = Aw, Sw
    lg = [] if logging else None; r = run_q23(Is, make_tfun(arm, prm), prm["w"], prm["eps"], lg)
    out = dict(n_eval=r["n_eval"], dyn=r["dyn"], log=lg)
    if oracle:
        Fo = p14._oracle_eval(I, r["D"]); out.update(hv_oracle=float(R.hv(Fo)), hv_search=float(R.hv(r["F"])), F_search=np.asarray(r["F"]).tolist(), F_oracle=Fo.tolist(), D=np.asarray(r["D"]).tolist())
    return out
def task23(sc, seed, arms, prm, oracle=True, logging=True):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    W = p9.worlds9(I); out["conds"] = {a: run_arm23(I, a, prm, W, oracle, logging) for a in arms}; return out
