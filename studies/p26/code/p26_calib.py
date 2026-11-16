"""P26 calibration (HV-BLIND): B-X,B-G,B-O x seeds 16700-16714; refs E_w, DA_w and 12 Gt candidates per (w, ref-agnostic); per-generation mean entropy and q_max (g=1..150). No oracle."""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p26, p24
from multiprocessing import Pool
OUT = p26.BASE + "/p26/p26_calib.json"; WS = [0.3, 0.7]
CAND = [(g0, g1, Gs) for g0 in (1.0, 3.0) for g1 in (6.0, 10.0, 16.0) for Gs in (30, 90)]
REFS = [p24.aid("E", w) for w in WS] + [p24.aid("DA", w, 0.7) for w in WS]
GT = [p26.gid(w, "X", g0, g1, Gs) for w in WS for (g0, g1, Gs) in CAND]
ARMS = REFS + GT
def ser(r): return [(d["q_ent"], d["q_max"]) for d in r["dyn"] if "q_ent" in d]
def job(a):
    sc, seed = a; I = p26.p25b.build25b(sc, seed); W = p24.p9.worlds9(I); return {k: ser(p24.run_arm24(I, k, W, oracle=False, logging=False)[0]) for k in ARMS}
if __name__ == "__main__":
    assert not os.path.exists(OUT); jobs = [(sc, s) for s in range(16700, 16715) for sc in p26.SC_B3]
    with Pool(2) as p: res = p.map(job, jobs, chunksize=1)
    H = {k: np.mean([[x[0] for x in r[k]] for r in res], axis=0).tolist() for k in ARMS}; Q = {k: np.mean([[x[1] for x in r[k]] for r in res], axis=0).tolist() for k in ARMS}
    json.dump(dict(entropy_traj=H, qmax_traj=Q, n_runs=len(res), arms=ARMS, cand=CAND, note="per-generation means g=1..150; HV not computed"), open(OUT, "w"), indent=1); print("calibration done", len(res), len(H[ARMS[0]]))
