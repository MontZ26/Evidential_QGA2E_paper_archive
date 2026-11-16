"""P24 technical pilot: seeds 13900-13909 x {S4-C101, S5-R101} x all arms. Checks budget, finiteness, log/npz completeness; measures wall time. HV stored, NEVER printed or analysed."""
import sys, os, json, time, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p24
from multiprocessing import Pool
B = p24.BASE; PRM = json.load(open(B + "/p24/p24_params.json")); ARMS = PRM["arms"]; OUT = B + "/p24/p24_pilot.json"
def job(a):
    sc, seed = a; t0 = time.time(); r, npz = p24.task24(sc, seed, ARMS); return sc, seed, time.time() - t0, r, npz
if __name__ == "__main__":
    assert not os.path.exists(OUT); jobs = [(sc, s) for s in range(13900, 13910) for sc in ("S4-C101", "S5-R101")]; t0 = time.time()
    with Pool(2) as p: res = p.map(job, jobs, chunksize=1)
    bad = []; walls = []; os.makedirs(B + "/p24/pilot_runs", exist_ok=True)
    for sc, s, w, r, npz in res: json.dump(r, open(B + f"/p24/pilot_runs/{sc}__{s}.json", "w")); np.savez_compressed(B + f"/p24/pilot_runs/{sc}__{s}.npz", **npz)
    for sc, s, w, r, npz in res:
        walls.append(w)
        if not r.get("feasible"): bad.append((sc, s, "infeasible")); continue
        for a, c in r["conds"].items():
            if c["n_eval"] != 6040 or not (math.isfinite(c["hv_oracle"]) and math.isfinite(c["hv_search"])) or len(c["log"]) != 5 or len(c["dyn"]) != 151 or any(("%s|%d" % (a, g)) not in npz for g in (1, 25, 50, 100, 150)): bad.append((sc, s, a))
    tot = time.time() - t0; per = float(np.mean(walls)); est_h = per * 600 / 2 / 3600
    json.dump(dict(n_tasks=len(res), n_arms=len(ARMS), wall_total_s=tot, mean_task_wall_s=per, est_main_hours_2procs=est_h, problems=bad), open(OUT, "w"), indent=1); print("pilot", len(res), "tasks", round(tot), "s; est main %.2f h; problems:" % est_h, bad); assert not bad
