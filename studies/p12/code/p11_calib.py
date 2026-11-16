import sys, json, numpy as np; sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p12/code")
import p11
from multiprocessing import Pool
GRID = [(n, r) for n in (2, 3, 5) for r in (0.2, 0.4)]
def job(a):
    sc, seed, n, r = a; dp = dict(sigma=0.7, n_max=n, rho_max=r, r_max=3); res = p11.task11(sc, seed, ["E1"], dp); c = res["conds"]["E1"]; d = c["dec"]
    return dict(sc=sc, seed=seed, n_max=n, rho=r, viol=d["violations"] / max(1, d["cands"]), regen=d["regen"] / max(1, d["cands"]), dep_last=c["dyn"][-1]["dep"], mut=d["mutations"], repaired=d["cands_repaired"] / max(1, d["cands"]), hv_not_used=c["hv_oracle"])
if __name__ == "__main__":
    jobs = [(sc, s, n, r) for (n, r) in GRID for s in range(9920, 9935) for sc in p11.p8.SC3]
    with Pool(2) as p: rows = p.map(job, jobs, chunksize=1)
    json.dump(rows, open("/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p12/p11_calib_raw.json", "w"))
    summ = {}
    for (n, r) in GRID:
        x = [q for q in rows if q["n_max"] == n and q["rho"] == r]; summ[f"{n}_{r}"] = dict(n_max=n, rho=r, viol=float(np.mean([q["viol"] for q in x])), regen=float(np.mean([q["regen"] for q in x])), dep_last=float(np.mean([q["dep_last"] for q in x])), mut=float(np.mean([q["mut"] for q in x])), repaired=float(np.mean([q["repaired"] for q in x])))
        summ[f"{n}_{r}"]["eligible"] = bool(summ[f"{n}_{r}"]["viol"] <= .05 and summ[f"{n}_{r}"]["regen"] <= 1 and summ[f"{n}_{r}"]["dep_last"] <= .10)
    el = [v for v in summ.values() if v["eligible"]]
    if el: ch = sorted(el, key=lambda v: (v["n_max"], v["rho"]))[0]; why = "rule"
    else: c5 = [v for v in summ.values() if v["n_max"] == 5]; ch = min(c5, key=lambda v: v["viol"]); why = "fallback_no_eligible"
    out = dict(summary=summ, chosen=dict(sigma=0.7, n_max=ch["n_max"], rho_max=ch["rho"], r_max=3), why=why); json.dump(out, open("/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p12/p11_calib.json", "w"), indent=1); print(json.dumps(out, indent=1))
