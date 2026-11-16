"""P21 gates A-G1..A-G5, B-G1..B-G5 (HV never analysed)."""
import sys, json, hashlib, inspect, os, numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p21/code")
import p21; from p21 import p14, P, R, K, p7, p10
B = p21.BASE; T = {}; INFO = {}
def chk(k, v): T[k] = bool(v); print(("PASS " if v else "FAIL ") + k, flush=True)
SC6 = p14.p8.SC6; st14 = lambda sc, s: json.load(open(f"{B}/p14/runs/conf/{sc}__{s}.json")); st17 = lambda sc, s: json.load(open(f"{B}/p17/runs/tier1/{sc}__{s}.json")); st20 = lambda sc, s: json.load(open(f"{B}/p20/runs/main/{sc}__{s}.json"))
# A-G5 / seeds
chk("AG5_seed_allowlist", all(s in P.ALLOWED_SEEDS for s in (10400, 10499, 11200, 11299)) and 11300 not in P.ALLOWED_SEEDS and 10500 not in P.ALLOWED_SEEDS)
# A-G4 P17 references
f17 = [f"{B}/p17/runs/tier1/{sc}__{s}.json" for s in range(11200, 11300) for sc in SC6]; chk("AG4a_600_P17_shards_exist", all(os.path.exists(f) for f in f17))
ok = True; okb = True
for f in f17[::23]:
    r = json.load(open(f))["conds"]
    for a in ("E", "DA", "Dp", "Dg", "DA+SELR", "DA+SEL4"): okb &= r[a]["n_eval"] == 6040; ok &= abs(R.hv(np.asarray(r[a]["F_oracle"])) - r[a]["hv_oracle"]) < 1e-12
chk("AG4b_P17_budget_6040_and_hv_recomputes_from_stored_front", ok and okb)
src_ora = inspect.getsource(p14.run_arm14); chk("AG4c_same_oracle_and_hv_definition", "_oracle_eval(I, D)" in src_ora and "R.hv(Fo)" in src_ora)
fb = [f"{B}/p14/runs/conf/{sc}__{s}.json" for s in range(10400, 10500) for sc in SC6]; fb20 = [f"{B}/p20/runs/main/{sc}__{s}.json" for s in range(10400, 10500) for sc in SC6]
chk("BG0_P14_and_P20_reference_shards_exist", all(os.path.exists(f) for f in fb + fb20))
INFO["reference_manifest_sha256"] = {("p17/" if "p17" in f else "p14/" if "/p14/" in f else "p20/") + f.split("/")[-1]: hashlib.sha256(open(f, "rb").read()).hexdigest() for f in f17 + fb + fb20}
# runs
sc, seed = "S4-RC101", 10400; I = P.build(sc, seed); W = p21.p9.worlds9(I); ref = st14(sc, seed)["conds"]; orig_t = p10.target
ns = p21.run_arm21(I, "NSGA2", p21.PRM, W); mo = p21.run_arm21(I, "MOEAD", p21.PRM, W)
chk("AG1_NSGA2_MOEAD_bit_for_bit_equal_P14_stored", all(x["D"] == ref[a]["D"] and x["F_search"] == ref[a]["F_search"] and x["hv_oracle"] == ref[a]["hv_oracle"] for a, x in (("NSGA2", ns), ("MOEAD", mo))))
chk("AG2_budget_NSGA2_6040_MOEAD_6030_archive_nonempty", ns["n_eval"] == 6040 and mo["n_eval"] == 6030 and len(ns["D"]) > 0 and len(mo["D"]) > 0)
chk("AG3a_counter_patch_restored", p14.X.Cnt is p14._Cnt0)
ns2 = p21.run_arm21(I, "NSGA2", p21.PRM, W); chk("AG3b_reproducible", ns["D"] == ns2["D"] and ns["F_search"] == ns2["F_search"])
I2 = dict(I); I2["A_true"] = np.random.RandomState(3).rand(*I["A_true"].shape); I2["S_true"] = np.random.RandomState(4).rand(*I["S_true"].shape); r2 = p21.run_arm21(I2, "NSGA2", p21.PRM, W)
chk("AG3c_no_oracle_in_search", r2["F_search"] == ns["F_search"] and r2["D"] == ns["D"] and r2["F_oracle"] != ns["F_oracle"])
# B gates
rng = np.random.RandomState(20); M = np.ones((12, 5), int); M[::3, 3:] = 0; src = np.array([[rng.choice(np.flatnonzero(M[p])) for p in range(12)] for _ in range(9)]); w, eps = p21.PRM["w"], p21.PRM["eps"]; okop = True
for rule in ("V1", "V0c"):
    Pn, _ = p7.population_model(src, M, w, rule)
    for g in (0.8, 0.9, 1.1, 1.25):
        Pg = np.where(M > 0, np.power(np.maximum(Pn, 0.0), g), 0.0); rf = K.floor_renorm(Pg / Pg.sum(1, keepdims=True), M, eps); out, _ = p14.make_target(g)(src, M, w, rule, eps)
        okop &= bool(np.abs(out - rf).max() <= 1e-15) and bool(np.allclose(out.sum(1), 1)) and bool((out[M == 0] == 0).all())
chk("BG2a_make_target_equals_reference_power_then_floor_gamma_0.8_to_1.25", okop)
chk("BG2b_Eg_and_Dg_same_function_make_target", src_ora.count("make_target(g)") == 1 and '"Dg": prm["gamma"], "Es": prm["gamma_e"]' in src_ora)
e1 = p21.run_arm21(I, "1.0", p21.PRM, W); chk("BG1_gamma1_bit_for_bit_equals_stored_E", e1["D"] == ref["E"]["D"] and e1["F_search"] == ref["E"]["F_search"] and e1["hv_oracle"] == ref["E"]["hv_oracle"])
g125 = p21.run_arm21(I, "Eg1.25", p21.PRM, W); g08 = p21.run_arm21(I, "Eg0.8", p21.PRM, W); g11 = p21.run_arm21(I, "Eg1.1", p21.PRM, W)
chk("BG3a_budget_6040", g125["n_eval"] == 6040 and g08["n_eval"] == 6040 and g11["n_eval"] == 6040); chk("BG3b_target_patch_restored", p10.target is orig_t)
g125b = p21.run_arm21(I, "Eg1.25", p21.PRM, W); chk("BG3c_reproducible", g125["D"] == g125b["D"] and g125["F_search"] == g125b["F_search"])
r3 = p21.run_arm21(I2, "Eg1.25", p21.PRM, W); chk("BG3d_no_oracle_in_search", r3["F_search"] == g125["F_search"] and r3["D"] == g125["D"] and r3["F_oracle"] != g125["F_oracle"])
qm = lambda r: float(np.mean([d["q_max"] for d in r["dyn"] if "q_max" in d])); INFO["qmax_Eg0.8_E_Eg1.1_Eg1.25"] = [qm(g08), qm(ref["E"]), qm(g11), qm(g125)]; print("   q_max (info, not a gate)", INFO["qmax_Eg0.8_E_Eg1.1_Eg1.25"], flush=True)
chk("BG4_finite_values", all(np.isfinite([d.get("q_max", 0.0) for d in r["dyn"]]).all() and np.isfinite(r["hv_oracle"]) for r in (g125, g08, g11)))
r20 = st20(sc, seed)["conds"]; e15 = p21.run_arm21(I, "1.5", p21.PRM, W); e2 = p21.run_arm21(I, "2.0", p21.PRM, W)
chk("BG5_Eg1.5_Eg2_non_regression_bit_for_bit_vs_P20_stored", e15["D"] == r20["Eg1.5"]["D"] and e15["F_search"] == r20["Eg1.5"]["F_search"] and e2["D"] == r20["Eg2"]["D"] and e2["F_search"] == r20["Eg2"]["F_search"])
json.dump(dict(tests=T, info=INFO), open(B + "/p21/p21_tests_results.json", "w"), indent=1); print("ALL", all(T.values()))
