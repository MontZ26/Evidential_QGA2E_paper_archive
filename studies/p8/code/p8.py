"""P8 engine (Protocol P8 v0.2.1 + Amendement). 7 main arms + D_V2:
 A  : layer I off (non-informative world), layer II off (classical GA C0b)      B  : nominal world, GA C0b
 C  : non-informative world, P7 V1                                               D  : nominal world, V1
 C' : non-informative world, V0c                                                 D' : nominal world, V0c
 Dt : nominal world, V0c-tau (V0c with w = tau)                                  DV2: nominal world, V2 (sensitivity)
The optimiser sees ONLY the search world (A_hat, S_hat) through I['A_true'], I['S_true'] of a COPY of the instance; every final archive is re-evaluated under the oracle world post hoc.
Frozen P5/P7 modules are used unmodified; Archive is subclassed at run time only to expose the decision vectors (identical behaviour, verified in G-I)."""
import os, sys, json
import numpy as np
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p7/code")
import p7
K, P, R = p7.K, p7.P, p7.R
class _Seeds8:
    def __contains__(self, s): return (8000 <= s <= 8399 or s == 9801 or s in (7000, 5200))
P.ALLOWED_SEEDS = _Seeds8()
SC6, SC3 = K.SC6, K.SC3
_orig_Archive = K.Archive; _LAST = []
class CapArchive(_orig_Archive):
    def __init__(s, *a, **k): super().__init__(*a, **k); _LAST.append(s)
def worlds_for(I):
    st = P.make_state(I); nom = P.worlds(I, st)["nom"]; cert = (I["CT"] == 1)
    non = (np.where(cert, 0.55, 0.0), np.full_like(nom[1], 0.5))
    return {"nom": nom, "non": non, "oracle": (I["A_true"], I["S_true"])}
def prm_ga(): return json.load(open(K.HERE + "/p5_tuned.json"))["C0b"]["prm"]
def prm_p7(): return json.load(open(BASE + "/p7/p7_tuned.json"))["prm"]
ARM_DEF = {  # arm -> (world, layer II)  layer II in {None,'V1','V0c','V0c-tau','V2'}
    "A": ("non", None), "B": ("nom", None), "C": ("non", "V1"), "D": ("nom", "V1"), "Cp": ("non", "V0c"), "Dp": ("nom", "V0c"), "Dt": ("nom", "V0c-tau"), "DV2": ("nom", "V2")}
def run_one(I, world, w2, tau=None, diag=None, wd=None):
    """Run one arm with search world `world` (name or (A,S)); returns dict with front (search), D (decisions), oracle objective vectors, HV oracle."""
    W = worlds_for(I) if wd is None else wd; Aw, Sw = (W[world] if isinstance(world, str) else world)
    Is = dict(I); Is["A_true"], Is["S_true"] = Aw, Sw; del _LAST[:]; K.Archive = CapArchive
    try:
        if w2 is None: r = K.run(Is, "ga", "a", prm_ga(), diag=diag)
        else:
            prm = dict(prm_p7()); rule = w2
            if w2 == "V0c-tau": prm["w"] = float(tau); rule = "V0c"
            r = p7.run7(Is, rule, prm, diag=diag)
    finally: K.Archive = _orig_Archive
    arch = _LAST[-1]; Dd = arch.D.copy(); Fs = arch.F.copy(); Ao, So = I["A_true"], I["S_true"]
    Fo = np.array([P.evaluate(d, I, Ao, So) for d in Dd]) if len(Dd) else np.empty((0, 3))
    out = dict(n_eval=r["n_eval"], D=Dd.tolist(), F_search=Fs.tolist(), F_oracle=Fo.tolist(), hv_search=float(R.hv(Fs)), hv_oracle=float(R.hv(Fo)), gens=r.get("gens"), cnt=r.get("cnt"),
               search_time_s=r.get("search_time_s"), ent=r.get("ent"), mdiag=r.get("mdiag"), div={str(k): v for k, v in (r.get("div") or {}).items()} if isinstance(r.get("div"), dict) else r.get("div"))
    # objective variation / selection pressure diagnostic (descriptive): sd of f2,f3 over the search archive
    if len(Fs) > 1: out["sd_f"] = Fs.std(0).tolist()
    return out
def task8(sc, seed, arms, tau=None, diag=None):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    W = worlds_for(I); out["conds"] = {a: run_one(I, ARM_DEF[a][0], ARM_DEF[a][1], tau, diag, W) for a in arms}; return out
