"""G-D3 step 1: real-population dependency diagnostic on TECHNICAL seeds 9910-9919 (DEC off: E0, P0, C0), no hypothesis. Output: p11_diag_raw.json (summaries over sigma grid)."""
import sys, json, numpy as np; sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p12/code")
import p11
from multiprocessing import Pool
SIG = [0.5, 0.6, 0.7, 0.8, 0.9]
def job(a):
    sc, seed = a; r = p11.task11(sc, seed, ["E0", "P0", "C0"], diag={"snap": True}); out = {}
    for arm, c in r["conds"].items():
        rows = []
        for g, decs in c["snap"]:
            X = np.array(decs); N = len(X); Sm = (X[:, None, :] == X[None, :, :]).mean(2); row = dict(gen=g)
            for s in SIG:
                ni = (Sm >= s - 1e-12).sum(1); row[f"nmax@{s}"] = int(ni.max()); row[f"dep@{s}"] = float(np.log(ni).mean() / np.log(N)); row[f"neff@{s}"] = float((1 / ni).sum())
            rows.append(row)
        out[arm] = dict(rows=rows, hv=c["hv_oracle"], N=len(decs))
    return sc, seed, out
if __name__ == "__main__":
    jobs = [(sc, s) for s in range(9910, 9920) for sc in p11.p8.SC6]
    with Pool(2) as p: res = p.map(job, jobs, chunksize=1)
    json.dump([dict(sc=a, seed=b, arms=c) for a, b, c in res], open("/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p12/p11_diag_raw.json", "w"))
    for arm in ("E0", "P0", "C0"):
        print(arm)
        for s in SIG:
            for gsel in ("early", "mid", "last"):
                v = []
                for _, _, o in res:
                    rows = o[arm]["rows"]; r = rows[1] if gsel == "early" and len(rows) > 1 else rows[len(rows) // 2] if gsel == "mid" else rows[-1]; v.append((r[f"nmax@{s}"], r[f"dep@{s}"], r[f"neff@{s}"]))
                v = np.array(v); print(f"  sigma={s} {gsel}: n_max mean {v[:,0].mean():.1f} (p10 {np.percentile(v[:,0],10):.0f}, p90 {np.percentile(v[:,0],90):.0f}) Dep {v[:,1].mean():.3f} Neff {v[:,2].mean():.2f}")
