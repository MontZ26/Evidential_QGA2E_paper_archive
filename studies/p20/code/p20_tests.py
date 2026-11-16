"""P10 v3 gates G0-G5 (HV never analysed)."""
import sys, json, glob, hashlib, inspect, numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p20/code")
import p20; from p20 import p14, P, R, K, p7, p10
B = p20.BASE; T = {}; INFO = {}
def chk(k, v): T[k] = bool(v); print(("PASS " if v else "FAIL ") + k, flush=True)
SC6 = p14.p8.SC6; st = lambda sc, s: json.load(open(f"{B}/p14/runs/conf/{sc}__{s}.json"))
# G0 references
files = [f"{B}/p14/runs/conf/{sc}__{s}.json" for s in range(10400, 10500) for sc in SC6]; ok = all(__import__("os").path.exists(f) for f in files); chk("G0a_600_reference_shards_exist", ok)
okb = True; okh = True
for f in files[::37]:
    r = json.load(open(f))["conds"]
    for a in ("E", "Dp", "Dg"): okb &= r[a]["n_eval"] == 6040; okh &= abs(R.hv(np.asarray(r[a]["F_oracle"])) - r[a]["hv_oracle"]) < 1e-12
chk("G0b_reference_budget_6040_and_hv_recomputes_from_stored_front", okb and okh)
src_ora = inspect.getsource(p14.run_arm14); chk("G0c_same_oracle_eval_and_hv_definition_for_new_and_reference_arms", "_oracle_eval(I, D)" in src_ora and "R.hv(Fo)" in src_ora)
INFO["reference_manifest_sha256"] = {f.split("/")[-1]: hashlib.sha256(open(f, "rb").read()).hexdigest() for f in files}
# G2 hardening operation identity
rng = np.random.RandomState(20); M = np.ones((12, 5), int); M[::3, 3:] = 0; src = np.array([[rng.choice(np.flatnonzero(M[p])) for p in range(12)] for _ in range(9)]); w, eps = p20.PRM["w"], p20.PRM["eps"]; okop = True
for rule in ("V1", "V0c"):
    Pn, _ = p7.population_model(src, M, w, rule)
    for g in (1.5, 2.0, 4.0, 6.0):
        Pg = np.where(M > 0, np.power(np.maximum(Pn, 0.0), g), 0.0); ref = K.floor_renorm(Pg / Pg.sum(1, keepdims=True), M, eps); out, _ = p14.make_target(g)(src, M, w, rule, eps)
        okop &= bool(np.abs(out - ref).max() <= 1e-15) and bool(np.allclose(out.sum(1), 1)) and bool((out[M == 0] == 0).all())
    out1, _ = p14.make_target(1.0)(src, M, w, rule, eps); okop &= bool(np.abs(out1 - K.floor_renorm(Pn, M, eps)).max() <= 1e-15)
chk("G2a_make_target_equals_reference_power_then_floor_for_V1_and_V0c_gamma_1.5_to_6_normalised", okop)
chk("G2b_Eg_and_Dg_use_the_same_function_make_target", src_ora.count("make_target(g)") == 1 and '"Dg": prm["gamma"], "Es": prm["gamma_e"]' in src_ora)
Pn1, _ = p7.population_model(src, M, w, "V1"); oh, _ = p14.make_target(6.0)(src, M, w, "V1", eps); o1, _ = p14.make_target(1.0)(src, M, w, "V1", eps); chk("G2c_hardened_more_concentrated_than_gamma1", (oh.max(1) >= o1.max(1) - 1e-12).all() and oh.max(1).mean() > o1.max(1).mean())
# runs
sc, seed = "S4-RC101", 10400; I = P.build(sc, seed); W = p20.p9.worlds9(I); ref = st(sc, seed)["conds"]; orig_t = p10.target
e1 = p20.run_arm20(I, "1.0", p20.PRM, W); chk("G1_gamma1_bit_for_bit_equals_stored_E", e1["D"] == ref["E"]["D"] and e1["F_search"] == ref["E"]["F_search"] and e1["hv_oracle"] == ref["E"]["hv_oracle"])
g6 = p20.run_arm20(I, "Eg6", p20.PRM, W); chk("G3a_budget_6040_Eg6", g6["n_eval"] == 6040); chk("G3b_target_patch_restored", p10.target is orig_t)
g6b = p20.run_arm20(I, "Eg6", p20.PRM, W); chk("G3c_reproducible", g6["D"] == g6b["D"] and g6["F_search"] == g6b["F_search"])
I2 = dict(I); I2["A_true"] = np.random.RandomState(3).rand(*I["A_true"].shape); I2["S_true"] = np.random.RandomState(4).rand(*I["S_true"].shape); r2 = p20.run_arm20(I2, "Eg6", p20.PRM, W)
chk("G3d_no_oracle_in_search", r2["F_search"] == g6["F_search"] and r2["D"] == g6["D"] and r2["F_oracle"] != g6["F_oracle"])
g2 = p20.run_arm20(I, "Eg2", p20.PRM, W); qm = lambda r: float(np.mean([d["q_max"] for d in r["dyn"] if "q_max" in d]))
chk("G2d_Eg2_and_Eg6_more_concentrated_than_E_in_runs", qm(g2) > qm(ref["E"]) and qm(g6) > qm(g2)); INFO["qmax_E_Eg2_Eg6"] = [qm(ref["E"]), qm(g2), qm(g6)]; print("   q_max E %.3f Eg2 %.3f Eg6 %.3f" % tuple(INFO["qmax_E_Eg2_Eg6"]), flush=True)
chk("G4_finite_values", all(np.isfinite([d.get("q_max", 0.0) for d in r["dyn"]]).all() and np.isfinite(r["hv_oracle"]) for r in (g6, g2, e1)))
dp = p14.run_arm14(I, "Dp", p20.PRM, W); dg = p14.run_arm14(I, "Dg", p20.PRM, W)
chk("G5_Dp_Dg_non_regression_bit_for_bit_vs_stored", dp["D"] == ref["Dp"]["D"] and dp["F_search"] == ref["Dp"]["F_search"] and dg["D"] == ref["Dg"]["D"] and dg["F_search"] == ref["Dg"]["F_search"])
json.dump(dict(tests=T, info=INFO), open(B + "/p20/p20_tests_results.json", "w"), indent=1); print("ALL", all(T.values()))
