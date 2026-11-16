"""P23 calibration (HV-BLIND): SC3 x seeds 12700-12714, generations 1-150. Records target entropy and q_max series of DA(lambda), Dg(gamma grid), R_rho(rho0 grid), R_mix(gmix grid). No oracle evaluation is performed. Run once."""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p23; from p23 import P
from multiprocessing import Pool
B = p23.BASE; BASE = json.load(open(B + "/p15/p15_params.json"))["chosen"]; OUT = B + "/p23/p23_calib.json"
GG = [1.0, 1.25, 1.5, 2.0, 3.0, 4.0, 6.0]; RR = [0.02, 0.05, 0.1, 0.2]; GM = [0.25, 0.5, 0.75]
def ser(r): return [(d["q_ent"], d["q_max"]) for d in r["dyn"] if "q_ent" in d]
def job(a):
    sc, seed = a; I = P.build(sc, seed); W = p23.p9.worlds9(I); o = {}
    prm0 = dict(BASE, gamma={}, rho0=0.1, gmix=0.5)
    for lam in ("DA25", "DA50", "DA100"): o[lam] = ser(p23.run_arm23(I, lam, prm0, W, oracle=False, logging=False))
    # Dg depends only on gamma (not on lambda): one series per gamma, via the arm Dg100 with gamma map
    for g in GG: o["Dg_%s" % g] = ser(p23.run_arm23(I, "Dg100", dict(prm0, gamma={"DA100": g}), W, oracle=False, logging=False))
    for r in RR: o["RHO_%s" % r] = ser(p23.run_arm23(I, "RHO", dict(prm0, rho0=r), W, oracle=False, logging=False))
    for m in GM: o["MIX_%s" % m] = ser(p23.run_arm23(I, "MIX", dict(prm0, gmix=m), W, oracle=False, logging=False))
    return o
if __name__ == "__main__":
    assert not os.path.exists(OUT); jobs = [(sc, s) for s in range(12700, 12715) for sc in p23.p8.SC3]
    with Pool(2) as p: res = p.map(job, jobs, chunksize=1)
    keys = list(res[0]); Hm = {k: float(np.mean([np.mean([x[0] for x in r[k]]) for r in res])) for k in keys}; Qm = {k: float(np.mean([np.mean([x[1] for x in r[k]]) for r in res])) for k in keys}
    json.dump(dict(entropy=Hm, qmax=Qm, n_runs=len(res), note="means over generations with diagnostics and over runs; SC3 x 12700-12714; HV not computed"), open(OUT, "w"), indent=1); print("calibration done", len(res))
