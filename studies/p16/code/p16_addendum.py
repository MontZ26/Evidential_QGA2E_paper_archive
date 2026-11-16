"""P16 addendum (exploratory, HV-BLIND): direct DA+L - DA+S contrast on existing phase D shards. Run once."""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p16_an as A
d = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p16/runs/phaseD"; out = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p16/p16_addendum.json"
assert not os.path.exists(out); res = A.load_dir(d); seeds = sorted({r["seed"] for r in res.values()}); n = len(seeds)
rng = A.S.sub_rng("p16_addendum", 11991); idx = rng.randint(0, n, size=(20000, n)).astype(np.int32); rep = dict(status="EXPLORATORY ADDENDUM, HV-blind, does not alter the P16 decision rule", n_seeds=n, contrast="DA+L - DA+S", ci="percentile bootstrap 95%, unit=seed", res={})
for k in ("m_theta", "dep", "neff", "q_max", "q_ent", "m_empty"):
    X = {a: np.array([np.mean([A.series(res[f"{sc}|{s}"], a, k) for sc in A.SC], axis=0) for s in seeds]) for a in ("DA+L", "DA+S")}; dd = X["DA+L"] - X["DA+S"]
    rep["res"][k] = {str(g): dict(mean=float(dd[:, g - 1].mean()), ci95=[float(np.percentile(dd[:, g - 1][idx].mean(1), q)) for q in (2.5, 97.5)]) for g in A.GENS}
json.dump(rep, open(out, "w"), indent=1); print(json.dumps(rep, indent=1))
