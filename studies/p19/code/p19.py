"""P19 engine: evidential target DA hardened by the same power transform as Dg (Pn^gamma, renormalised, then P10 floor). Frozen modules UNMODIFIED; runtime patch of p15.make_target15 inside try/finally."""
import sys, json
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p15/code")
import numpy as np, p15, p14, p10, p9, p8, p7
K, P, R, X = p7.K, p7.P, p7.R, p7.X
class _Seeds19:
    def __contains__(self, s): return (11700 <= s <= 11714 or 11200 <= s <= 11259 or 11800 <= s <= 11809 or s in (10400, 10401, 9290, 7000, 5200))
P.ALLOWED_SEEDS = _Seeds19()
def harden(Pn, M, g):
    Pg = np.where(M > 0, np.power(np.maximum(Pn, 0.0), g), 0.0); return Pg / Pg.sum(1, keepdims=True)
_orig_mt = p15.make_target15
def _mt(arm, prm):
    g = prm.get("gamma_da", 1.0)
    if arm == "DA" and g != 1.0:
        def f(src, M, w, rule, eps):
            Pn, md = p15.da_model(src, M, w, prm["sigma"], prm["lam"]); Pn = harden(Pn, M, g); p15.DIAG.append(dict(md)); return K.floor_renorm(Pn, M, eps), md
        return f
    return _orig_mt(arm, prm)
def run_arm19(I, arm, prm, wd=None):
    """arm: 'DAg' (gamma = prm['gamma_da']) ; 'DA' is gamma 1 ; 'Dg' = P15 Dg with prm['gamma']"""
    W = p9.worlds9(I) if wd is None else wd
    p15.make_target15 = _mt
    try: r = p15.run_arm15(I, "DA" if arm == "DAg" else arm, prm, W)
    finally: p15.make_target15 = _orig_mt
    return r
def task19(sc, seed, arms, prm):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    W = p9.worlds9(I); out["conds"] = {a: run_arm19(I, "DAg", dict(prm, gamma_da=g), W) for a, g in arms.items()}; return out
