"""Blocking input checks BEFORE the single run of p6_final.py. Usage: python p6_precheck.py CONF_DIR FREEZE.txt. Exit 0 only if everything passes."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p6_stats as S, p6_load as L
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p5"); import run_p1m as R
BASE = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p6"
def main(d, freeze):
    bad = []
    if not R.verify_freeze(freeze): bad.append("freeze verification failed")
    n = json.load(open(BASE + "/p6_n.json"))["n"]; res = L.load_dir(d); seeds = sorted({r["seed"] for r in res.values()})
    if seeds != list(range(6200, 6200 + n)): bad.append(f"seed set differs from 6200..{6200 + n - 1}: {len(seeds)} seeds")
    if len(res) != 6 * n: bad.append(f"{len(res)} shards, expected {6 * n}")
    infeasible = []
    for k, r in res.items():
        if not r.get("feasible", False):
            infeasible.append(k)
            if r.get("conds"): bad.append(f"{k}: infeasible task carries results")
            continue
        for a in S.ARMS:
            c = r.get("conds", {}).get(a)
            if c is None: bad.append(f"{k}: missing {a}"); continue
            F = np.asarray(c["front"], float)
            if F.ndim != 2 or F.shape[1] != 3 or F.size == 0 or not np.isfinite(F).all() or F.min() < 0 or F.max() > 1 + 1e-9: bad.append(f"{k}|{a}: front invalid")
            if c["n_eval"] != 6040: bad.append(f"{k}|{a}: n_eval {c['n_eval']}")
    print("infeasible tasks (excluded by design, listed):", infeasible); print("PRECHECK", "PASS" if not bad else "FAIL"); [print(" -", b) for b in bad[:30]]
    return 0 if not bad else 1
if __name__ == "__main__": sys.exit(main(sys.argv[1], sys.argv[2]))
