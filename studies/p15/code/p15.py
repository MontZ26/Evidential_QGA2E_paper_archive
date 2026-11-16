"""P15 pilot engine: DA-DST target (copy of the P14 engine pattern; frozen modules UNMODIFIED, runtime patch of p10.target inside try/finally)."""
import sys, math
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p14/code"); sys.path.insert(0, BASE + "/p10/code")
import numpy as np, p14, p10, p9, p8, p7
K, P, R, X = p7.K, p7.P, p7.R, p7.X
class _Seeds15:
    def __contains__(self, s): return (9290 <= s <= 9291 or 10400 <= s <= 10401 or 10850 <= s <= 10859 or 10900 <= s <= 10929 or s == 10990 or s in (7000, 5200))
P.ALLOWED_SEEDS = _Seeds15()
ARMS15 = ["E", "Dp", "Dg", "DA", "PDA", "V2"]
def eff_counts(src, M, sigma, lam):
    """returns (n_tilde [n_p,n_t], n_M [N,n_p]) ; n_M includes the source itself; alpha = 1/(1+lam*(n_M-1))"""
    N, n_p = src.shape; n_t = M.shape[1]
    S = (src[:, None, :] == src[None, :, :]).mean(2); sim = S >= sigma; np.fill_diagonal(sim, False)
    agree = (src[:, None, :] == src[None, :, :])                      # [i,j,p]
    nM = 1 + (agree & sim[:, :, None]).sum(1)                         # [i,p]
    alpha = 1.0 / (1.0 + lam * (nM - 1)); nt = np.zeros((n_p, n_t))
    for i in range(N): np.add.at(nt, (np.arange(n_p), src[i]), alpha[i])
    return nt, nM
def da_model(src, M, w, sigma=0.7, lam=1.0):
    """Dempster closed form (same code path as p7.population_model V1) with raw counts replaced by dependence-corrected effective counts; returns Pn_before_floor, diag"""
    nt, nM = eff_counts(src, M, sigma, lam); n_p, n_t = nt.shape
    Kp = M.sum(1, keepdims=True); U = M / Kp; T = nt > 0
    lu = np.where(T, nt * math.log(1 - w), 0.0); L = lu.sum(1, keepdims=True); mT = np.exp(L); u = np.exp(lu)
    mS = np.where(T, (1 - u) * np.exp(L - lu), 0.0); s = mT + mS.sum(1, keepdims=True); fb = (s < 1e-300).ravel()
    Pn = (mS + mT * U) / np.where(s < 1e-300, 1.0, s); Pn = np.where(fb[:, None], U, Pn); mut = (M.sum(1) >= 2)
    return Pn, dict(m_empty=float(np.mean((1 - s.ravel())[mut])), m_theta=float(np.mean((mT / np.where(s < 1e-300, 1.0, s)).ravel()[mut])), fallback=float(fb[mut].mean()), alpha_mean=float(np.mean(1.0 / (1.0 + lam * (nM - 1)))), neff_ratio=float(nt.sum(1)[mut].mean() / len(src)))
def pda_model(src, M, w, sigma=0.7, lam=1.0):
    nt, nM = eff_counts(src, M, sigma, lam); Kp = M.sum(1, keepdims=True); U = M / Kp
    Pn = w * nt / nt.sum(1, keepdims=True) + (1 - w) * U; mut = (M.sum(1) >= 2)
    return Pn, dict(m_empty=0.0, m_theta=1 - w, fallback=0.0, alpha_mean=float(np.mean(1.0 / (1.0 + lam * (nM - 1)))), neff_ratio=float(nt.sum(1)[mut].mean() / len(src)))
DIAG = []
def make_target15(arm, prm):
    def f(src, M, w, rule, eps):
        if arm == "DA": Pn, md = da_model(src, M, w, prm["sigma"], prm["lam"])
        elif arm == "PDA": Pn, md = pda_model(src, M, w, prm["sigma"], prm["lam"])
        else:
            Pn, md = p7.population_model(src, M, w, rule); g = prm["gamma"] if arm == "Dg" else 1.0
            if g != 1.0: Pg = np.where(M > 0, np.power(np.maximum(Pn, 0.0), g), 0.0); Pn = Pg / Pg.sum(1, keepdims=True)
        DIAG.append(dict(md)); return K.floor_renorm(Pn, M, eps), md
    return f
def run_arm15(I, arm, prm, wd=None):
    W = p9.worlds9(I) if wd is None else wd; Aw, Sw = W["nom"]; Is = dict(I); Is["A_true"], Is["S_true"] = Aw, Sw
    rule = {"E": "V1", "Dp": "V0c", "Dg": "V0c", "DA": "V1", "PDA": "V0c", "V2": "V2"}[arm]
    old = p10.target; p10.target = make_target15(arm, prm); DIAG.clear()
    try: r = p10.run_q(Is, rule, prm["w"], prm["eps"], None, diag=True)
    finally: p10.target = old
    dyn = r["dyn"]; dg = list(DIAG)
    for d in dyn:                                    # target called at generation g -> recorded in dyn entry g+1
        g = d["gen"]
        if g >= 1 and g - 1 < len(dg): d.update({k: v for k, v in dg[g - 1].items()})
    Fo = p14._oracle_eval(I, r["D"])
    return dict(n_eval=r["n_eval"], hv_oracle=float(R.hv(Fo)), hv_search=float(R.hv(r["F"])), F_search=np.asarray(r["F"]).tolist(), F_oracle=Fo.tolist(), D=np.asarray(r["D"]).tolist(), dyn=dyn)
def task15(sc, seed, arms, prm):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    W = p9.worlds9(I); out["conds"] = {a: run_arm15(I, a, prm, W) for a in arms}; return out
