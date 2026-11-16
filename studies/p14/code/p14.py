"""P14 engine (Protocol P14 v0.2 + Amendement 10 nov. 11:09). Uses frozen P3/P5/P7/P8/P9/P10/P11 modules UNMODIFIED (runtime-patched only inside try/finally):
 - sharpened / softened QGA2-E target (power gamma applied to the model BEFORE the floor, then the P10 floor_renorm),
 - NSGA-II and MOEA/D of P3 run in the nominal evidential world with a recording evaluation counter (archive of all evaluated solutions, like the other arms),
 - C0b = P8/P9 classical GA."""
import sys, math, random, json
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p10/code")
import numpy as np, p10, p9, p8, p7
K, P, R, X = p7.K, p7.P, p7.R, p7.X
class _Seeds14:
    def __contains__(self, s): return (9290 <= s <= 9291 or 10290 <= s <= 10299 or 10300 <= s <= 10314 or 10350 <= s <= 10379 or 10400 <= s <= 10699 or s == 10803 or s in (7000, 5200))
P.ALLOWED_SEEDS = _Seeds14()
ARMS14 = ["E", "Dp", "Dg", "Es", "B", "Bt", "NSGA2", "MOEAD", "C0"]
def make_target(g):
    def f(src, M, w, rule, eps):
        Pn, md = p7.population_model(src, M, w, rule)
        if g != 1.0:
            Pg = np.where(M > 0, np.power(np.maximum(Pn, 0.0), g), 0.0); Pn = Pg / Pg.sum(1, keepdims=True)
        return K.floor_renorm(Pn, M, eps), md
    return f
_Cnt0 = X.Cnt
class RecCnt(_Cnt0):
    """P3 evaluation counter that also records every evaluated solution (archive of non-dominated seen, same as the other arms)"""
    arch = None
    def __call__(s, d):
        f = _Cnt0.__call__(s, d)
        if RecCnt.arch is not None: RecCnt.arch.add(np.asarray(d)[None], np.asarray(f)[None])
        return f
def _oracle_eval(I, D):
    Ao, So = I["A_true"], I["S_true"]; return np.array([P.evaluate(d, I, Ao, So) for d in D]) if len(D) else np.empty((0, 3))
def run_arm14(I, arm, prm, wd=None):
    W = p9.worlds9(I) if wd is None else wd; Aw, Sw = W["nom"]; Is = dict(I); Is["A_true"], Is["S_true"] = Aw, Sw
    if arm in ("E", "Dp", "Dg", "Es", "B", "Bt"):
        rule = {"E": "V1", "Dp": "V0c", "Dg": "V0c", "Es": "V1", "B": None, "Bt": None}[arm]; g = {"Dg": prm["gamma"], "Es": prm["gamma_e"]}.get(arm, 1.0)
        old_t, old_d = p10.target, P.DELTA
        p10.target = make_target(g)
        if arm == "Bt": P.DELTA = 0.1 * math.pi
        try: r = p10.run_q(Is, rule, prm["w"], prm["eps"], None, diag=True)
        finally: p10.target = old_t; P.DELTA = old_d
        F, D, dyn = r["F"], r["D"], r["dyn"]; n_eval = r["n_eval"]
    elif arm in ("NSGA2", "MOEAD"):
        RecCnt.arch = X.Arch(); old = _Cnt0; X.Cnt = RecCnt
        try:
            res = X.nsga2(Is, True, 0.9, 1.0) if arm == "NSGA2" else X.moead(Is, 20)
        finally: X.Cnt = old
        F, D = RecCnt.arch.F, RecCnt.arch.D; n_eval = res["n_eval"]; dyn = None; RecCnt.arch = None
    elif arm == "C0":
        o = p8.run_one(I, "nom", None, None, None, W); o.pop("snap", None); o["dyn"] = None; return o
    Fo = _oracle_eval(I, D)
    return dict(n_eval=n_eval, hv_oracle=float(R.hv(Fo)), hv_search=float(R.hv(F)), F_search=np.asarray(F).tolist(), F_oracle=Fo.tolist(), D=np.asarray(D).tolist(), dyn=dyn)
def task14(sc, seed, arms, prm):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    W = p9.worlds9(I); out["conds"] = {a: run_arm14(I, a, prm, W) for a in arms}; return out
