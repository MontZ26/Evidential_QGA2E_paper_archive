"""Shard loading for P6 analysis scripts."""
import os, json, glob, numpy as np
import p6_stats as S
sys_path_set = False
def hvl(f):
    import sys; sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p5"); import run_p1m as R
    return float(R.hv(np.asarray(f, float).reshape(-1, 3))) if f is not None and len(f) else 0.0
def load_dir(d):
    assert os.path.isabs(d); out = {}
    for f in sorted(glob.glob(d + "/*__*.json")):
        r = json.load(open(f)); out[f"{r['sc']}|{r['seed']}"] = r
    return out
def usable(res, arms, seeds=None):
    seeds = seeds if seeds is not None else sorted({r["seed"] for r in res.values()}); keep = []; excl = {}
    for s in seeds:
        why = []
        for sc in S.SC:
            r = res.get(f"{sc}|{s}")
            if r is None: why.append(f"{sc}: shard missing"); continue
            if not r.get("feasible", False): why.append(f"{sc}: infeasible"); continue
            miss = [a for a in arms if a not in r.get("conds", {})]
            if miss: why.append(f"{sc}: missing {miss}")
        if why: excl[s] = why
        else: keep.append(s)
    return keep, excl
def hv_matrix(res, seeds):
    return {a: np.array([np.mean([hvl(res[f"{sc}|{s}"]["conds"][a]["front"]) for sc in S.SC]) for s in seeds]) for a in S.ARMS}
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=str); os.replace(tmp, p)
