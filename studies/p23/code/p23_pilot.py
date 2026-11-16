"""P23 technical pilot: seeds 12900-12909 x {S4-C101, S5-R101} x 9 arms with the selected parameters. Checks budget, finiteness, archive completeness and measures wall time. HV values are stored but NEVER printed or analysed here."""
import sys, os, json, time, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p23
from multiprocessing import Pool
B = p23.BASE; PRM = json.load(open(B + "/p23/p23_params.json")); ARMS = list(p23.ARMS23); OUT = B + "/p23/p23_pilot.json"
def job(a):
    sc, seed = a; t0 = time.time(); r = p23.task23(sc, seed, ARMS, PRM); return sc, seed, time.time() - t0, r
if __name__ == "__main__":
    assert not os.path.exists(OUT); jobs = [(sc, s) for s in range(12900, 12910) for sc in ("S4-C101", "S5-R101")]; t0 = time.time()
    with Pool(2) as p: res = p.map(job, jobs, chunksize=1)
    bad = []; walls = []; os.makedirs(B + '/p23/pilot_runs', exist_ok=True)
    for sc, s, w, r in res: json.dump(r, open(B + f'/p23/pilot_runs/{sc}__{s}.json', 'w'))
    for sc, s, w, r in res:
        walls.append(w)
        if not r.get("feasible"): bad.append((sc, s, "infeasible")); continue
        for a, c in r["conds"].items():
            if c["n_eval"] != 6040 or not (math.isfinite(c["hv_oracle"]) and math.isfinite(c["hv_search"])) or len(c["log"]) != 5 or len(c["dyn"]) != 151: bad.append((sc, s, a))
    tot = time.time() - t0; per_task = float(np.mean(walls)); est_h = per_task * 600 / 2 / 3600
    json.dump(dict(n_tasks=len(res), wall_total_s=tot, mean_task_wall_s=per_task, est_main_hours_2procs=est_h, problems=bad), open(OUT, "w"), indent=1); print("pilot", len(res), "tasks", round(tot), "s; est main (600 tasks, 2 procs) %.2f h; problems:" % est_h, bad)
    assert not bad
