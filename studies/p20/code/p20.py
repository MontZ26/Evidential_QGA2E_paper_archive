"""P10 v3 engine: E (V1-Q, QGA2-E) hardened by the same power operation as Dg. Frozen P14 module UNMODIFIED (arm 'Es' of run_arm14 applies make_target(gamma_e); gamma_e>1 hardens)."""
import sys, json
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p14/code")
import numpy as np, p14
P, R, K, p7, p10, p9, p8 = p14.P, p14.R, p14.K, p14.p7, p14.p10, p14.p9, p14.p8
PRM = json.load(open(BASE + "/p14/p14_params.json"))["chosen"]
GAMMAS = {"Eg1.5": 1.5, "Eg2": 2.0, "Eg4": 4.0, "Eg6": 6.0}
def run_arm20(I, arm, prm=PRM, wd=None):
    W = p9.worlds9(I) if wd is None else wd
    return p14.run_arm14(I, "Es", dict(prm, gamma_e=GAMMAS[arm] if arm in GAMMAS else float(arm)), W)
def task20(sc, seed, arms, prm=PRM):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    W = p9.worlds9(I); out["conds"] = {a: run_arm20(I, a, prm, W) for a in arms}; return out
