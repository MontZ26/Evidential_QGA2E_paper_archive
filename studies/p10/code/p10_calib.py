import sys, json, numpy as np; sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p10/code")
import p10
from multiprocessing import Pool
DP = json.load(open("/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p12/p11_params.json")); WG = [0.3, 0.5, 0.7, 0.9]
def job(a):
    sc, seed = a; I = p10.P.build(sc, seed); W = p10.p9.worlds9(I); out = {}
    for w in WG:
        prm = dict(w=w, eps=0.02, dec=DP); out[w] = {arm: p10.run_one10(I, arm, prm, W)["hv_oracle"] for arm in ("E", "P")}
    return sc, seed, out
if __name__ == "__main__":
    jobs = [(sc, s) for s in range(9300, 9315) for sc in p10.p8.SC3]
    with Pool(2) as p: res = p.map(job, jobs, chunksize=1)
    summ = {w: dict(E=float(np.mean([o[w]["E"] for _, _, o in res])), P=float(np.mean([o[w]["P"] for _, _, o in res]))) for w in WG}
    for w in WG: summ[w]["crit"] = (summ[w]["E"] + summ[w]["P"]) / 2
    best = max(WG, key=lambda w: (round(summ[w]["crit"], 4), -w)); out = dict(summary={str(w): v for w, v in summ.items()}, chosen=dict(w=best, eps=0.02, dec=DP))
    json.dump(out, open("/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p10/p10_calib.json", "w"), indent=1); print(json.dumps(out, indent=1))
