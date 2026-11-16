"""P25b tests: file parsing, determinism, rescaling, seed guard, feasibility, budget."""
import sys, os, json, hashlib; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p25b, p24
from p24 import P
res = {}
exp = {l.split()[1]: l.split()[0] for l in open(p25b.BASE + "/p25b/files_sha256.txt")}
res["file_hashes_match"] = all(hashlib.sha256(open(p25b.FD + f, "rb").read()).hexdigest() == h for f, h in exp.items())
res["n_nodes"] = {sc: len(p25b.coords(sc)) for sc in p25b.SC_B6}
res["expected_nodes"] = res["n_nodes"] == {"B-X": 101, "B-M": 101, "B-G": 241, "B-L": 561, "B-O": 242, "B-H": 201}
a = p25b.gen_points("B-O", 15000); b = p25b.gen_points("B-O", 15000); c = p25b.gen_points("B-O", 15001)
res["deterministic"] = a == b; res["seed_differs"] = a != c; res["n_pts"] = len(a)
res["in_box"] = all(0 <= x <= 100 + 1e-6 and 0 <= y <= 100 + 1e-6 for sc in p25b.SC_B6 for x, y in p25b.gen_points(sc, 15000))
res["distinct_customers"] = all(len(set(p25b.gen_points(sc, 15000)[1:])) >= 95 for sc in p25b.SC_B6)
feas = {sc: sum(bool(p25b.build25b(sc, s)["feasible"]) for s in range(15700, 15710)) for sc in p25b.SC_B6}; res["feasible_of_10"] = feas
try: P.build("B-X", 5); res["guard"] = False
except Exception: res["guard"] = True
r, npz = p25b.task25b("B-M", 15900, [p24.aid("E", 0.3), p24.aid("DA", 0.3, 0.7)])
res["budget_ok"] = all(c["n_eval"] == 6040 for c in r["conds"].values()); res["finite"] = all(np.isfinite(c["hv_oracle"]) for c in r["conds"].values())
res["pass"] = bool(res["file_hashes_match"] and res["expected_nodes"] and res["deterministic"] and res["seed_differs"] and res["in_box"] and res["distinct_customers"] and min(feas.values()) >= 9 and res["guard"] and res["budget_ok"] and res["finite"])
json.dump(res, open(p25b.BASE + "/p25b/p25b_tests_results.json", "w"), indent=1, default=str); print(json.dumps(res, indent=1, default=str))
