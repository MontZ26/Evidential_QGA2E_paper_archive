"""P26 tests: schedule arithmetic; constant schedule == static Dg bit-for-bit; counter reset per run; seed guard; feasibility."""
import sys, os, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p26, p24
from p24 import P
res = {}
res["ramp_values"] = [p26.gamma_at(g, 1.0, 10.0, 30) for g in (1, 15, 30, 31, 150)]
res["ramp_ok"] = abs(res["ramp_values"][0] - 1.0) < 1e-12 and abs(res["ramp_values"][2] - 10.0) < 1e-12 and res["ramp_values"][3] == 10.0 and res["ramp_values"][4] == 10.0 and 1 < res["ramp_values"][1] < 10
a_const = p26.gid(0.7, "E", 6.0, 6.0, 30); a_static = p24.aid("Dg", 0.7, gamma=6.0)
r, _ = p26.task26("B-M", 16900, [a_const, a_static], oracle=True, logging=False)
c1, c2 = r["conds"][a_const], r["conds"][a_static]
res["const_equals_static_hv"] = c1["hv_oracle"] == c2["hv_oracle"]; res["const_equals_static_F"] = c1["F_oracle"] == c2["F_oracle"]
a_ramp = p26.gid(0.7, "E", 1.0, 10.0, 30); r2, _ = p26.task26("B-M", 16900, [a_ramp], oracle=False, logging=False)
g_series = [d.get("gamma_t") for d in r2["conds"][a_ramp]["dyn"] if "gamma_t" in d]
r3, _ = p26.task26("B-M", 16900, [a_ramp], oracle=False, logging=False); g3 = [d.get("gamma_t") for d in r3["conds"][a_ramp]["dyn"] if "gamma_t" in d]
res["gamma_series_len"] = len(g_series); res["gamma_series_monotone"] = all(np.diff(g_series) >= -1e-12) and abs(g_series[0] - 1.0) < 1e-9 and abs(g_series[-1] - 10.0) < 1e-9; res["counter_reset_between_runs"] = g_series == g3
try: P.build("B-X", 5); res["guard"] = False
except Exception: res["guard"] = True
res["pass"] = bool(res["ramp_ok"] and res["const_equals_static_hv"] and res["const_equals_static_F"] and res["gamma_series_len"] == 150 and res["gamma_series_monotone"] and res["counter_reset_between_runs"] and res["guard"])
json.dump(res, open(p26.BASE + "/p26/p26_tests_results.json", "w"), indent=1, default=str); print(json.dumps(res, indent=1, default=str))
