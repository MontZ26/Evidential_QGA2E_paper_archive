"""P24 calibration (HV-BLIND): SC3 x seeds 13700-13714, generations 1-150. Records target entropy / q_max series of DA(1; w, sigma) and Dg(gamma; w) over gamma grid. No oracle evaluation, no HV. Run once."""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p24; from p24 import P
from multiprocessing import Pool
B = p24.BASE; OUT = B + "/p24/p24_calib.json"
ARMS = [p24.aid("DA", w, 0.7) for w in p24.W_LIST] + [p24.aid("DA", 0.3, s) for s in p24.SIGMAS] + [p24.aid("Dg", w, gamma=g) for w in p24.W_LIST for g in p24.GAMMA_GRID]
def ser(r): return [(d["q_ent"], d["q_max"]) for d in r["dyn"] if "q_ent" in d]
def job(a):
    sc, seed = a; I = P.build(sc, seed); W = p24.p9.worlds9(I); return {k: ser(p24.run_arm24(I, k, W, oracle=False, logging=False)[0]) for k in ARMS}
if __name__ == "__main__":
    assert not os.path.exists(OUT); jobs = [(sc, s) for s in range(13700, 13715) for sc in p24.p23.p8.SC3]
    with Pool(2) as p: res = p.map(job, jobs, chunksize=1)
    Hm = {k: float(np.mean([np.mean([x[0] for x in r[k]]) for r in res])) for k in ARMS}; Qm = {k: float(np.mean([np.mean([x[1] for x in r[k]]) for r in res])) for k in ARMS}
    json.dump(dict(entropy=Hm, qmax=Qm, n_runs=len(res), arms=ARMS, note="means over generations 1-150 and runs; SC3 x 13700-13714; HV not computed"), open(OUT, "w"), indent=1); print("calibration done", len(res))
