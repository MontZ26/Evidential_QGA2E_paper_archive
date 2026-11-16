"""P19 technical tests (HV never analysed)."""
import sys, json, numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p19/code")
import p19; from p19 import p15, P
B = p19.BASE; T = {}; PRM = json.load(open(B + "/p15/p15_params.json"))["chosen"]
def chk(k, v): T[k] = bool(v); print(("PASS " if v else "FAIL ") + k, flush=True)
rng = np.random.RandomState(19); M = np.ones((10, 5), int); M[::3, 3:] = 0; Pn = rng.dirichlet(np.ones(5), 10) * M; Pn = Pn / Pn.sum(1, keepdims=True); h = p19.harden(Pn, M, 6.0)
chk("1_harden_rows_sum_1_zero_outside_M_more_concentrated", np.allclose(h.sum(1), 1) and (h[M == 0] == 0).all() and (h.max(1) >= Pn.max(1) - 1e-12).all() and np.allclose(p19.harden(Pn, M, 1.0), Pn))
I = P.build("S4-RC101", 11200); W = p19.p9.worlds9(I); t1 = json.load(open(B + "/p17/runs/tier1/S4-RC101__11200.json"))["conds"]
da = p19.run_arm19(I, "DA", PRM, W); chk("2a_DA_bit_for_bit_vs_tier1", da["D"] == t1["DA"]["D"] and da["F_search"] == t1["DA"]["F_search"])
g1 = p19.run_arm19(I, "DAg", dict(PRM, gamma_da=1.0), W); chk("2b_DAg_gamma1_equals_DA", g1["D"] == da["D"] and g1["F_search"] == da["F_search"])
g6 = p19.run_arm19(I, "DAg", dict(PRM, gamma_da=6.0), W); chk("3a_DAg6_budget_6040_and_differs", g6["n_eval"] == 6040 and g6["D"] != da["D"])
qm = lambda r: np.mean([d["q_max"] for d in r["dyn"] if "q_max" in d]); chk("3b_DAg6_more_concentrated_than_DA", qm(g6) > qm(da)); print("   q_max DA %.3f DAg6 %.3f" % (qm(da), qm(g6)), flush=True)
chk("3c_target_patch_restored", p15.make_target15 is p19._orig_mt)
g6b = p19.run_arm19(I, "DAg", dict(PRM, gamma_da=6.0), W); chk("4_reproducible", g6b["D"] == g6["D"] and g6b["F_search"] == g6["F_search"])
I2 = dict(I); I2["A_true"] = np.random.RandomState(3).rand(*I["A_true"].shape); I2["S_true"] = np.random.RandomState(4).rand(*I["S_true"].shape); r2 = p19.run_arm19(I2, "DAg", dict(PRM, gamma_da=6.0), W)
chk("5_no_oracle_in_search", r2["F_search"] == g6["F_search"] and r2["D"] == g6["D"] and r2["F_oracle"] != g6["F_oracle"])
dg = p19.run_arm19(I, "Dg", PRM, W); chk("6_Dg_bit_for_bit_vs_tier1", dg["D"] == t1["Dg"]["D"] and dg["F_search"] == t1["Dg"]["F_search"])
json.dump(dict(tests=T, info=dict(qmax_DA=float(qm(da)), qmax_DAg6=float(qm(g6)), note="info only: not HV")), open(B + "/p19/p19_tests_results.json", "w"), indent=1); print("ALL", all(T.values()))
