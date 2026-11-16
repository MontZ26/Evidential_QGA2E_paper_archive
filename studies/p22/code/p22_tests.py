"""P22 gates G1-G6, G8, G9 (G7 is checked in the analysis precheck; HV never analysed)."""
import sys, json, hashlib, inspect, os, numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p22/code")
import p22; from p22 import p14, P, R, K, X, p7, p10
B = p22.BASE; T = {}; INFO = {}; SC6 = p14.p8.SC6
def chk(k, v): T[k] = bool(v); print(("PASS " if v else "FAIL ") + k, flush=True)
st = lambda sc, s: json.load(open(f"{B}/p14/runs/conf/{sc}__{s}.json"))["conds"]
chk("G8_seed_allowlist", all(s in P.ALLOWED_SEEDS for s in (10400, 10499, 11700, 11714)) and 10500 not in P.ALLOWED_SEEDS and 11200 not in P.ALLOWED_SEEDS)
files = [f"{B}/p14/runs/conf/{sc}__{s}.json" for s in range(10400, 10500) for sc in SC6]; chk("G9a_600_P14_reference_shards_exist", all(os.path.exists(f) for f in files))
ok = True
for f in files[::37]:
    r = json.load(open(f))["conds"]; ok &= r["NSGA2"]["n_eval"] == 6040 and abs(R.hv(np.asarray(r["NSGA2"]["F_oracle"])) - r["NSGA2"]["hv_oracle"]) < 1e-12
chk("G9b_stored_NSGA2_budget_and_hv_recomputes_from_stored_front", ok)
INFO["reference_manifest_sha256"] = {f.split("/")[-1]: hashlib.sha256(open(f, "rb").read()).hexdigest() for f in files}
# G1 / G9c bit for bit on 3 tasks, q=None path
okb = True
for sc, s in (("S4-RC101", 10400), ("S5-R101", 10401), ("S4-C101", 10499)):
    I = P.build(sc, s); r = p22.run_arm22(I, "NSGA2U"); ref = st(sc, s)["NSGA2"]; okb &= r["D"] == ref["D"] and r["F_search"] == ref["F_search"] and r["hv_oracle"] == ref["hv_oracle"] and r["n_eval"] == 6040
chk("G1_G9c_unguided_path_bit_for_bit_equals_stored_NSGA2_on_3_tasks", okb)
# G2 sampler
rng = np.random.RandomState(22); M = np.ones((6, 5), int); M[1, 3:] = 0; M[2, :4] = 0; qv = rng.dirichlet(np.ones(5), size=6); qv = np.where(M > 0, qv, 0.0); qv /= qv.sum(1, keepdims=True); okc = True; maxdev = 0.0
for p in range(6):
    allowed = np.flatnonzero(M[p])
    for cur in allowed:
        other, pr = p22.cond_law(qv[p], allowed, cur)
        if pr is None: okc &= len(allowed) == 1; continue
        okc &= abs(pr.sum() - 1) < 1e-12 and (pr > 0).all() and cur not in other and all(M[p, o] > 0 for o in other)
        ex = qv[p][other] / qv[p][other].sum(); okc &= np.abs(pr - ex).max() < 1e-15
        rg = np.random.RandomState(p * 10 + int(cur)); u = rg.rand(200000); idx = np.minimum(np.searchsorted(np.cumsum(pr), u, side="right"), len(other) - 1); f = np.bincount(idx, minlength=len(other)) / 200000.0; maxdev = max(maxdev, float(np.abs(f - pr).max()))
chk("G2_conditional_law_exact_and_empirical_freq_within_0.01", okc and maxdev < 0.01); INFO["g2_max_dev"] = maxdev
# G2b: vary_guided uses the sampler, mutation decision independent of q, no mutation without alternative
M2 = np.ones((6, 1), int); decs = np.zeros((2, 6), int); cnt = dict(drawn=0, effective=0); r_c = np.random.RandomState(1); r_m = np.random.RandomState(2); r_g = np.random.RandomState(3)
ch = p22.vary_guided(decs, 0, 1, r_c, r_m, r_g, 0.9, 1.0, M2, 6, np.ones((6, 1)), cnt); chk("G2b_no_mutation_without_alternative_team", (ch == 0).all() and cnt["effective"] == 0 and cnt["drawn"] == 6)
# G3 target identity (inputs, masks, normalisation)
src = np.array([[rng.choice(np.flatnonzero(M[p])) for p in range(6)] for _ in range(9)]); w, eps = p22.PRM["w"], p22.PRM["eps"]; ok3 = True
for rule in ("V1", "V0c"):
    Pn, _ = p7.population_model(src, M, w, rule)
    for g in (1.0, 6.0):
        Pg = Pn if g == 1.0 else (lambda Z: Z / Z.sum(1, keepdims=True))(np.where(M > 0, np.power(np.maximum(Pn, 0.0), g), 0.0)); ref = K.floor_renorm(Pg, M, eps); out, _ = p14.make_target(g)(src, M, w, rule, eps)
        ok3 &= bool(np.abs(out - ref).max() <= 1e-15) and bool(np.allclose(out.sum(1), 1)) and bool((out[M == 0] == 0).all())
chk("G3a_target_equals_reference_gamma_1_and_6_V0c_V1", ok3)
src_run = inspect.getsource(p22.run_arm22); src_ng = inspect.getsource(p22.nsga2_guided)
chk("G3b_arms_use_make_target_and_first_front_sources_once_per_generation", "p14.make_target(g)" in src_run and "src = decs[fr[0]]" in src_ng and src_ng.count("= qfun(src, M)") == 1 and src_ng.index("= qfun(src, M)") < src_ng.index("for c in range(POP)"))
chk("G3c_arm_table_rules", p22.ARMS == {"GDp": ("V0c", 1.0), "GE": ("V1", 1.0), "GDg6": ("V0c", 6.0), "GEg6": ("V1", 6.0)})
# runs
sc, seed = "S4-RC101", 10400; I = P.build(sc, seed); W = p22.p9.worlds9(I); ra = {a: p22.run_arm22(I, a, p22.PRM, W) for a in ("GDp", "GE", "GDg6", "GEg6", "GEgm") if a != "GEgm"}; rm = p22.run_arm22(I, "GEgm", p22.PRM, W, 2.0)
allr = dict(ra, GEgm=rm); chk("G4a_budget_6040_all_guided_arms", all(r["n_eval"] == 6040 for r in allr.values())); chk("G4b_archive_nonempty_and_counter_restored", all(len(r["D"]) > 0 for r in allr.values()) and p14.X.Cnt is p14._Cnt0 and p14.RecCnt.arch is None)
rb = p22.run_arm22(I, "GEg6", p22.PRM, W); chk("G4c_reproducible", rb["D"] == ra["GEg6"]["D"] and rb["F_search"] == ra["GEg6"]["F_search"])
I2 = dict(I); I2["A_true"] = np.random.RandomState(3).rand(*I["A_true"].shape); I2["S_true"] = np.random.RandomState(4).rand(*I["S_true"].shape); r2 = p22.run_arm22(I2, "GEg6", p22.PRM, W)
chk("G5_no_oracle_in_search", r2["F_search"] == ra["GEg6"]["F_search"] and r2["D"] == ra["GEg6"]["D"] and r2["F_oracle"] != ra["GEg6"]["F_oracle"])
chk("G6_finite_values", all(np.isfinite([d["q_max"] for d in r["dyn"]]).all() and np.isfinite([d["q_ent"] for d in r["dyn"]]).all() and np.isfinite(r["hv_oracle"]) for r in allr.values()))
chk("G6b_mutation_counts_effective_le_drawn_and_nearly_all_effective", all(0.9 * r["cnt"]["drawn"] <= r["cnt"]["effective"] <= r["cnt"]["drawn"] for r in allr.values()))
m = lambda r, k: float(np.mean([d[k] for d in r["dyn"]])); INFO["qmax_GDp_GE_GDg6_GEg6"] = [m(ra[a], "q_max") for a in ("GDp", "GE", "GDg6", "GEg6")]; INFO["mut_counts_GEg6"] = ra["GEg6"]["cnt"]; print("   q_max GDp/GE/GDg6/GEg6 (info)", INFO["qmax_GDp_GE_GDg6_GEg6"], flush=True)
json.dump(dict(tests=T, info=INFO), open(B + "/p22/p22_tests_results.json", "w"), indent=1); print("ALL", all(T.values()))
