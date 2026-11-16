"""P25 calibration (HV-BLIND): V6-U,V6-K,V6-M x seeds 14700-14714, gens 1-150; DA(1;w) and Dg(gamma;w) for w in {0.3,0.7}. No oracle, no HV. Run once."""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p25, p24
from multiprocessing import Pool
OUT = p25.BASE + "/p25/p25_calib.json"; WS = [0.3, 0.7]
ARMS = [p24.aid("DA", w, 0.7) for w in WS] + [p24.aid("Dg", w, gamma=g) for w in WS for g in p24.GAMMA_GRID]
def ser(r): return [(d["q_ent"], d["q_max"]) for d in r["dyn"] if "q_ent" in d]
def job(a):
    sc, seed = a; I = p25.build25(sc, seed); W = p24.p9.worlds9(I); return {k: ser(p24.run_arm24(I, k, W, oracle=False, logging=False)[0]) for k in ARMS}
if __name__ == "__main__":
    assert not os.path.exists(OUT); jobs = [(sc, s) for s in range(14700, 14715) for sc in p25.SC_V3]
    with Pool(2) as p: res = p.map(job, jobs, chunksize=1)
    Hm = {k: float(np.mean([np.mean([x[0] for x in r[k]]) for r in res])) for k in ARMS}; Qm = {k: float(np.mean([np.mean([x[1] for x in r[k]]) for r in res])) for k in ARMS}
    json.dump(dict(entropy=Hm, qmax=Qm, n_runs=len(res), arms=ARMS, note="means gens 1-150; HV not computed"), open(OUT, "w"), indent=1); print("calibration done", len(res))
