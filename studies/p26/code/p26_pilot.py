"""P26 technical pilot: seeds 15900-15909 x {B-X, B-O} x all arms. Integrity + wall time. HV stored, never printed."""
import sys, os, json, time, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p26 as p25, p24
from multiprocessing import Pool
B = p25.BASE; PRM = json.load(open(B + "/p26/p26_params.json")); ARMS = PRM["arms"]; OUT = B + "/p26/p26_pilot.json"
def job(a):
    sc, seed = a; t0 = time.time(); r, npz = p25.task26(sc, seed, ARMS); return sc, seed, time.time() - t0, r, npz
if __name__ == "__main__":
    assert not os.path.exists(OUT); jobs = [(sc, s) for s in range(16900, 16910) for sc in ("B-X", "B-O")]; t0 = time.time()
    with Pool(2) as p: res = p.map(job, jobs, chunksize=1)
    bad = []; walls = []
    for sc, s, w, r, npz in res:
        walls.append(w)
        if not r.get("feasible"): bad.append((sc, s, "infeasible")); continue
        for a, c in r["conds"].items():
            if c["n_eval"] != 6040 or not (math.isfinite(c["hv_oracle"]) and math.isfinite(c["hv_search"])) or len(c["dyn"]) != 151 or any(("%s|%d" % (a, g)) not in npz for g in (1, 25, 50, 100, 150)): bad.append((sc, s, a))
    per = float(np.mean(walls)); est = per * 360 / 2 / 3600
    json.dump(dict(n_tasks=len(res), n_arms=len(ARMS), wall_total_s=time.time() - t0, mean_task_wall_s=per, est_main_hours_2procs=est, problems=bad), open(OUT, "w"), indent=1); print("pilot", len(res), "est main %.2f h; problems:" % est, bad); assert not bad
