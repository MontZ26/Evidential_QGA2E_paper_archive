"""P25 tests: generator determinism, seed guard, geography stats, feasibility, budget, lambda=0 identity not needed. Writes p25_tests_results.json."""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p25, p24
from p24 import P
res = {}
a = p25.gen_points("CLU", 14000); b = p25.gen_points("CLU", 14000); c = p25.gen_points("CLU", 14001)
res["deterministic"] = a == b; res["seed_differs"] = a != c; res["n_pts"] = len(a); res["depot_first"] = a[0] == (40.0, 50.0)
res["coords_in_range"] = all(0 <= x <= 100 and 0 <= y <= 100 for x, y in a[1:])
feas = {}
for sc in p25.SC_V6:
    ok = 0
    for s in range(14700, 14705): ok += bool(p25.build25(sc, s)["feasible"])
    feas[sc] = ok
res["feasible_of_5"] = feas
try: P.build("V6-U", 5); res["guard_rejects_unregistered_seed"] = False
except Exception: res["guard_rejects_unregistered_seed"] = True
I1 = p25.build25("V6-U", 14900); I2 = p25.build25("V6-U", 14900); res["build_deterministic"] = bool(np.array_equal(I1["M"], I2["M"]) and np.allclose(I1["D"], I2["D"]))
for k in ("a", "b"):
    pass
r, npz = p25.task25("V6-K", 14900, [p24.aid("E", 0.3), p24.aid("DA", 0.3, 0.7)])
res["budget_ok"] = all(c["n_eval"] == 6040 for c in r["conds"].values()); res["finite"] = all(np.isfinite(c["hv_oracle"]) for c in r["conds"].values()); res["npz_keys"] = sorted(npz)[:3]
res["pass"] = bool(res["deterministic"] and res["seed_differs"] and res["depot_first"] and res["coords_in_range"] and min(feas.values()) >= 4 and res["guard_rejects_unregistered_seed"] and res["build_deterministic"] and res["budget_ok"] and res["finite"])
json.dump(res, open(p25.BASE + "/p25/p25_tests_results.json", "w"), indent=1, default=str); print(json.dumps(res, indent=1, default=str))
