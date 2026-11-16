"""P18 technical tests (HV never analysed). Run before freeze."""
import sys, json, time, numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p18/code")
import p18; from p18 import p15, p16, p17, P, X
B = p18.BASE; T = {}; INFO = {}; PRM = json.load(open(B + "/p15/p15_params.json"))["chosen"]
def chk(k, v): T[k] = bool(v); print(("PASS " if v else "FAIL ") + k, flush=True)
def timed(f):
    t = time.time(); r = f(); INFO.setdefault("times", []).append(round(time.time() - t, 1)); print("   %.1fs" % (time.time() - t), flush=True); return r
rng = np.random.RandomState(18); orig = X.select_next
I = P.build("S4-RC101", 11000); W = p18.p17.p9.worlds9(I); st = json.load(open(B + "/p16/runs/phaseD/S4-RC101__11000.json"))["conds"]; ok = True
for a in ("DA", "DA+S", "DA+L"):
    r = timed(lambda: p18.run_arm18(I, a, PRM, W)); ok &= (r["D"] == st[a]["D"] and r["F_search"] == st[a]["F_search"])
chk("1_partA_DA_DAS_DAL_bit_for_bit_vs_P16_stored", ok)
I2 = P.build("S4-RC101", 11200); W2 = p18.p17.p9.worlds9(I2); t1 = json.load(open(B + "/p17/runs/tier1/S4-RC101__11200.json"))["conds"]
e = timed(lambda: p18.run_arm18(I2, "E", PRM, W2)); chk("2a_E_bit_for_bit_vs_P17_tier1", e["D"] == t1["E"]["D"] and e["F_search"] == t1["E"]["F_search"])
dg6 = p15.run_arm15(I2, "Dg", PRM, W2); chk("2b_Dg6_bit_for_bit_vs_P17_tier1", dg6["D"] == t1["Dg"]["D"] and dg6["F_search"] == t1["Dg"]["F_search"])
dg12 = timed(lambda: p18.run_arm18(I2, "Dg12", PRM, W2)); chk("2c_Dg12_differs_from_Dg6_and_budget", dg12["D"] != dg6["D"] and dg12["n_eval"] == 6040)
# selection units
f80 = np.round(rng.rand(80, 3) * 8) / 8; sel0 = set(orig(np.zeros((80, 1)), f80, 40)); chk("3a_SELL_constant_U_same_set_as_original", set(p18.sell_select(f80, np.zeros(80), 40)) == sel0)
f80c = rng.rand(80, 3); Ud = rng.rand(80); s_l = set(p18.sell_select(f80c, Ud, 40)); chk("3b_SELL_continuous_fitness_equals_original_set_ties_absent", s_l == set(orig(np.zeros((80, 1)), f80c, 40)))
pop = np.array([rng.randint(0, 5, 30) for _ in range(20)]); Ud = p18.div_U(pop); ref = np.array([np.mean([np.mean(pop[i] == pop[j]) for j in range(20) if j != i]) for i in range(20)]); chk("3c_DIV_matches_bruteforce", np.allclose(Ud, ref, atol=1e-12))
# runs
res = {}
for a in p18.ARMS_B[:3]:
    res[a] = timed(lambda: p18.run_arm18(I2, a, PRM, W2)); r = res[a]
    chk("4_%s_budget_6040_log150_finite" % a, r["n_eval"] == 6040 and len(r["sel_log"]) == 150 and all(d["finite"] for d in r["sel_log"]) and np.asarray(r["F_oracle"]).shape[1] == 3)
    print("   %s diag front4_share %.3f divergence %.3f" % (a, np.mean([d["front4_share"] for d in r["sel_log"]]), np.mean([d["divergence"] for d in r["sel_log"]])), flush=True)
    INFO[a] = dict(front4_share=float(np.mean([d["front4_share"] for d in r["sel_log"]])), divergence=float(np.mean([d["divergence"] for d in r["sel_log"]])))
chk("5_selection_patch_restored", X.select_next is orig)
b = timed(lambda: p18.run_arm18(I2, "DA+DIV", PRM, W2)); chk("6_reproducible_DIV", b["D"] == res["DA+DIV"]["D"] and b["F_search"] == res["DA+DIV"]["F_search"])
I3 = dict(I2); I3["A_true"] = np.random.RandomState(3).rand(*I2["A_true"].shape); I3["S_true"] = np.random.RandomState(4).rand(*I2["S_true"].shape); ok = True
for a in p18.ARMS_B[:3]: r2 = p18.run_arm18(I3, a, PRM, W2); ok &= (r2["F_search"] == res[a]["F_search"] and r2["D"] == res[a]["D"] and r2["F_oracle"] != res[a]["F_oracle"])
chk("7_no_oracle_in_search_partB", ok)
# regulated arms
I4 = P.build("S4-RC101", 11600); W4 = p18.p17.p9.worlds9(I4); lv = {}
for a in ("DA+R1", "DA+R1inv", "DA+SCH", "DA+P11"):
    r = timed(lambda: p18.run_arm18(I4, a, PRM, W4)); lv[a] = r["levels"]; chk("8_%s_budget_and_levels" % a, r["n_eval"] == 6040 and len(r["levels"]) == 150 and set(r["levels"]) <= {"S", "L", "P11"})
chk("9_SCH_L_then_S", lv["DA+SCH"][:50] == ["L"] * 50 and lv["DA+SCH"][50:] == ["S"] * 100)
INFO["R1_share_L"] = float(np.mean([x == "L" for x in lv["DA+R1"]])); INFO["R1inv_share_L"] = float(np.mean([x == "L" for x in lv["DA+R1inv"]])); INFO["note"] = "info only: not HV"
json.dump(dict(tests=T, info=INFO), open(B + "/p18/p18_tests_results.json", "w"), indent=1); print("ALL", all(T.values()), INFO)
