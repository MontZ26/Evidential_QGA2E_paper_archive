"""P26 engine (new file; frozen P3..P25b code UNMODIFIED). Adds a TIME-VARYING tempered probabilistic target Dgt: Dp sharpened by a power gamma_t that ramps linearly from g0 to g1 over Gs generations, then stays at g1. Arm id: Gt_w{w}_{ref}_{g0}_{g1}_{Gs} (ref = E or DA = the evidential target whose entropy/q_max TRAJECTORY the schedule is calibrated to match, HV-blind).
Other arms = P24 (p24.make_tfun24). Geographies and instance generator = P25b (benchmark files)."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p25b/code"); sys.path.insert(0, BASE + "/p24/code")
import numpy as np, p25b, p24
from p24 import P, p7
from p24 import K, harden
class _Seeds26:
    def __contains__(self, s): return (16000 <= s <= 16099 or 16700 <= s <= 16714 or 16900 <= s <= 16909 or s in p25b._Seeds25b())
P.ALLOWED_SEEDS = _Seeds26()
SC_B6, SC_B3 = p25b.SC_B6, p25b.SC_B3
def gid(w, ref, g0, g1, Gs): return "Gt_w%g_%s_%g_%g_%d" % (w, ref, g0, g1, Gs)
def gparse(a):
    t = a.split("_"); return float(t[1][1:]), t[2], float(t[3]), float(t[4]), int(t[5])
def gamma_at(g, g0, g1, Gs):  # g = 1..150 (index of the target built at generation g)
    return g0 + (g1 - g0) * min(1.0, (g - 1) / max(Gs - 1, 1))
_orig = p24.make_tfun24
def make_tfun26(a):
    if not a.startswith("Gt_"): return _orig(a)
    w, ref, g0, g1, Gs = gparse(a); state = {"g": 0}
    def f(src, M, _w, eps):
        state["g"] += 1; gam = gamma_at(state["g"], g0, g1, Gs)
        Pn, md = p7.population_model(src, M, w, "V0c"); Pn = harden(Pn, M, gam); md = dict(md or {}); md["gamma_t"] = float(gam)
        return K.floor_renorm(Pn, M, eps), md
    return f
p24.make_tfun24 = make_tfun26
def task26(sc, seed, arms, oracle=True, logging=True):
    I = p25b.build25b(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"]); npz = {}
    if not I["feasible"]: return out, npz
    W = p24.p9.worlds9(I); out["conds"] = {}
    for a in arms:
        o, fql = p24.run_arm24(I, a, W, oracle, logging); out["conds"][a] = o
        if logging:
            for g, c in fql.items(): npz["%s|%d" % (a, g)] = c
    if logging: npz["M"] = np.asarray(I["M"]).astype(np.uint8)
    return out, npz
