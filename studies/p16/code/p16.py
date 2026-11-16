"""P16 engine: DEC (fixed or regulated) on top of the P15 DA-DST target. Frozen P3-P5, P7, P10, P11, P14, P15 modules are used UNMODIFIED; the p10.target runtime patch (inside try/finally) carries the DEC controller.
Timing: the target is called at the start of loop-generation g (sources = first front of the current population), BEFORE the children of generation g are created and repaired; the DEC level decided there applies to those children.
Initial cleaning (p11._init_clean, run inside p10.run_q) uses level S in every DEC arm; DA without DEC has no DEC object (no repair)."""
import sys, math, json
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p15/code")
import numpy as np, p15, p14, p10, p11, p9, p8, p7
K, P, R, X = p7.K, p7.P, p7.R, p7.X
class _Seeds16:
    def __contains__(self, s): return (11000 <= s <= 11029 or 11100 <= s <= 11114 or 10400 <= s <= 10401 or s in (9290, 7000, 5200))
P.ALLOWED_SEEDS = _Seeds16()
LEVELS = {"S": (5, 0.2), "L": (2, 0.4), "P11": (2, 0.2)}      # (n_max, rho_max = Dec.m_max_frac)
SIGMA, RMAX, SCH_SWITCH = 0.7, 3, 50
MODE = {"DA": "none", "DA+S": "S", "DA+L": "L", "DA+P11": "P11", "DA+R1": "R1", "DA+R2": "R2", "DA+R1inv": "R1inv", "DA+SCH": "SCH"}
ARMS16 = list(MODE)
def decide(mode, g, m_da, dm, th):
    """level for the children of loop-generation g"""
    if mode in ("S", "L", "P11"): return mode
    if mode == "R1": return "L" if m_da >= th["tau"] else "S"
    if mode == "R2": return "L" if dm >= th["tau_dm"] else "S"
    if mode == "R1inv": return "S" if m_da >= th["tau"] else "L"
    if mode == "SCH": return "L" if g < SCH_SWITCH else "S"
    raise ValueError(mode)
def make_dec16(I, level="S"):
    return p11.Dec(SIGMA, LEVELS[level][0], LEVELS[level][1], RMAX, P.rs(I["sc"], I["seed"], "p16_dec"))
def make_target16(prm, dec, mode, th, log):
    def f(src, M, w, rule, eps):
        g = len(log)
        Pn, md = p15.da_model(src, M, w, prm["sigma"], prm["lam"]); _, me = p7.population_model(src, M, w, "V1")
        d = dict(md); d["m_theta_E"] = me["m_theta"]; d["m_empty_E"] = me["m_empty"]; d["dm"] = md["m_theta"] - me["m_theta"]
        if dec is not None:
            lv = decide(mode, g, md["m_theta"], d["dm"], th); dec.n_max = int(LEVELS[lv][0]); dec.m_max_frac = float(LEVELS[lv][1])
            d["level"] = lv; d["n_max"] = dec.n_max; d["rho_max"] = dec.m_max_frac; d["dec_c"] = dict(dec.c)
        log.append(d); return K.floor_renorm(Pn, M, eps), md
    return f
def run_arm16(I, arm, prm, th=None, wd=None):
    W = p9.worlds9(I) if wd is None else wd; Aw, Sw = W["nom"]; Is = dict(I); Is["A_true"], Is["S_true"] = Aw, Sw
    mode = MODE[arm]; log = []; dec = None if mode == "none" else make_dec16(I, "S")
    old = p10.target; p10.target = make_target16(prm, dec, mode, th, log)
    try: r = p10.run_q(Is, "V1", prm["w"], prm["eps"], dec, diag=True)
    finally: p10.target = old
    dyn = r["dyn"]
    for d in dyn:
        g = d["gen"]
        if g >= 1 and g - 1 < len(log): d.update(log[g - 1])
    Fo = p14._oracle_eval(I, r["D"])
    return dict(n_eval=r["n_eval"], hv_oracle=float(R.hv(Fo)), hv_search=float(R.hv(r["F"])), F_search=np.asarray(r["F"]).tolist(), F_oracle=Fo.tolist(), D=np.asarray(r["D"]).tolist(), dyn=dyn, dec_final=(dict(dec.c) if dec else None), levels=[d.get("level") for d in log])
def task16(sc, seed, arms, prm, th=None):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    W = p9.worlds9(I); out["conds"] = {a: run_arm16(I, a, prm, th, W) for a in arms}; return out
