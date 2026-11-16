"""P21 engine. Frozen P14 module UNMODIFIED. Part A: arms NSGA2, MOEAD (run_arm14) on seeds 11200-11299. Part B: arms Eg(gamma) via run_arm14 'Es' with gamma_e, seeds 10400-10499."""
import sys, json
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
sys.path.insert(0, BASE + "/p14/code")
import numpy as np, p14
P, R, K, p7, p10, p9, p8 = p14.P, p14.R, p14.K, p14.p7, p14.p10, p14.p9, p14.p8
class _Seeds21:
    def __contains__(self, s): return (10400 <= s <= 10499 or 11200 <= s <= 11299 or 10290 <= s <= 10299 or s in (7000, 5200))
P.ALLOWED_SEEDS = _Seeds21()
PRM = json.load(open(BASE + "/p14/p14_params.json"))["chosen"]
GAMMAS = {"Eg1.1": 1.1, "Eg1.25": 1.25, "Eg0.9": 0.9, "Eg0.8": 0.8}
ARMS_A = ["NSGA2", "MOEAD"]; ARMS_B = list(GAMMAS)
def run_arm21(I, arm, prm=PRM, wd=None):
    W = p9.worlds9(I) if wd is None else wd
    if arm in ("NSGA2", "MOEAD"): return p14.run_arm14(I, arm, prm, W)
    return p14.run_arm14(I, "Es", dict(prm, gamma_e=GAMMAS[arm] if arm in GAMMAS else float(arm)), W)
def task21(sc, seed, arms, prm=PRM):
    I = P.build(sc, seed); out = dict(sc=sc, seed=seed, feasible=I["feasible"])
    if not I["feasible"]: return out
    W = p9.worlds9(I); out["conds"] = {a: run_arm21(I, a, prm, W) for a in arms}; return out
