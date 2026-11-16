"""P15 unit tests: maths of DA-DST target, non-regression vs P14/P7, budgets, no oracle leak."""
import sys, json, math, numpy as np; sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p15/code")
import p15, p10
P, X, K, p7, p14 = p15.P, p15.X, p15.K, p15.p7, p15.p14; T = {}
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
def chk(k, v): T[k] = bool(v); print(("PASS " if v else "FAIL ") + k)
PRM = json.load(open(B + "/p15/p15_params.json"))["chosen"]; w, eps = PRM["w"], PRM["eps"]
rng = np.random.RandomState(1); n_p, n_t = 30, 8; M = np.ones((n_p, n_t), int); M[::4, 5:] = 0; M[3, 1:] = 0; mut = M.sum(1) >= 2
def rnd_src(N): return np.array([[rng.choice(np.flatnonzero(M[p])) for p in range(n_p)] for _ in range(N)])
def near_dup_src():
    base = rnd_src(5); rows = []
    for b in base:
        rows.append(b)
        for _ in range(rng.randint(0, 5)):
            c = b.copy(); k = rng.randint(0, 6); idx = rng.choice(n_p, k, replace=False)
            for p in idx: c[p] = rng.choice(np.flatnonzero(M[p]))
            rows.append(c)
    return np.array(rows)
# lambda=0 -> exactly V1
src = near_dup_src()
q0, _ = p15.da_model(src, M, w, 0.7, 0.0); q1, _ = p7.population_model(src, M, w, "V1"); chk("DA_lambda0_equals_V1_bit_for_bit", np.array_equal(q0, q1))
# permutation invariance
qa, _ = p15.da_model(src[rng.permutation(len(src))], M, w, 0.7, 1.0); qb, _ = p15.da_model(src, M, w, 0.7, 1.0); chk("DA_permutation_invariance", np.allclose(qa, qb, atol=1e-12))
# exact-copy duplication invariance (equivalence-class case)
base = rnd_src(6); dup = np.vstack([base] + [base[:3]] * 4)      # first 3 rows get 5 copies, others 1
qd, _ = p15.da_model(dup, M, w, 0.7, 1.0); qu, _ = p15.da_model(base, M, w, 0.7, 1.0); chk("DA_duplication_invariance_equivalence_classes", np.allclose(qd, qu, atol=1e-12))
# bounds 1 <= n_tilde_t <= n_t on supported teams, near-duplicates (non transitive allowed)
ok = True; okth = True; okvalid = True; okmono = True
for _ in range(60):
    s_ = near_dup_src(); nt, nM = p15.eff_counts(s_, M, 0.7, 1.0); C = np.zeros((n_p, n_t)); [np.add.at(C, (np.arange(n_p), r), 1.0) for r in s_]
    sup = C > 0; ok &= bool(((nt[sup] >= 1 - 1e-9) & (nt[sup] <= C[sup] + 1e-9)).all())
    Pd, md = p15.da_model(s_, M, w, 0.7, 1.0); Pe, me = p7.population_model(s_, M, w, "V1"); okth &= md["m_theta"] >= me["m_theta"] - 1e-12
    qd_ = K.floor_renorm(Pd, M, eps); okvalid &= bool(np.allclose(qd_.sum(1), 1) and np.isfinite(qd_).all() and (qd_[M == 0] == 0).all() and (qd_[M == 1] >= eps - 1e-12).all())
    ms = [p15.da_model(s_, M, w, sg, 1.0)[1]["m_theta"] for sg in (0.0, 0.3, 0.5, 0.7, 0.9, 1.01)]; okmono &= all(a >= b - 1e-12 for a, b in zip(ms, ms[1:]))
chk("DA_bounds_1_le_ntilde_le_n", ok); chk("DA_ignorance_mTheta_ge_Dempster_mTheta", okth); chk("DA_normalised_finite_floor_support", okvalid); chk("DA_mTheta_nonincreasing_in_sigma", okmono)
Pp, _ = p15.pda_model(src, M, w, 0.7, 1.0); chk("PDA_rows_sum_to_one", np.allclose(Pp.sum(1), 1) and np.isfinite(Pp).all())
# non-regression vs P14 stored runs (E, Dp, Dg) and P7 V2
import glob
sc, seed = "S4-RC101", 10400; I = P.build(sc, seed); W = p14.p9.worlds9(I); st = json.load(open(B + f"/p14/runs/conf/{sc}__{seed}.json"))["conds"]; okn = True
for a in ("E", "Dp", "Dg"):
    r = p15.run_arm15(I, a, PRM, W); okn &= (r["D"] == st[a]["D"] and r["F_search"] == st[a]["F_search"] and r["hv_oracle"] == st[a]["hv_oracle"])
chk("NONREG_E_Dp_Dg_bit_for_bit_vs_P14_stored_10400", okn)
Is = dict(I); Is["A_true"], Is["S_true"] = W["nom"]; v2 = p10.run_q(Is, "V2", PRM["w"], PRM["eps"], None, diag=True); r2 = p15.run_arm15(I, "V2", PRM, W); chk("NONREG_V2_bit_for_bit_vs_direct_run_q", r2["D"] == np.asarray(v2["D"]).tolist() and r2["F_search"] == np.asarray(v2["F"]).tolist())
chk("budget_exact_all_arms", all(p15.run_arm15(I, a, PRM, W)["n_eval"] == 6040 for a in ("DA", "PDA", "V2", "E")))
rd = p15.run_arm15(I, "DA", PRM, W); dy = rd["dyn"]; chk("diag_mTheta_mEmpty_recorded_gen1_150", all(("m_theta" in d and "m_empty" in d and 0 <= d["m_theta"] <= 1) for d in dy[1:]) and len(dy) == 151); print("   DA gen150", {k: round(dy[-1][k], 3) for k in ("m_theta", "m_empty", "q_max", "q_ent", "neff_ratio", "alpha_mean")})
re = p15.run_arm15(I, "E", PRM, W)["dyn"]; chk("E_diag_mTheta_recorded", all("m_theta" in d for d in re[1:])); print("   E  gen150", {k: round(re[-1][k], 3) for k in ("m_theta", "m_empty", "q_max", "q_ent")})
# (no gate on cross-run m_theta ordering: the theorem holds for identical sources; across runs the populations differ -> reported descriptively in the pilot)
I2 = dict(I); I2["A_true"] = np.random.RandomState(3).rand(*I["A_true"].shape); I2["S_true"] = np.random.RandomState(4).rand(*I["S_true"].shape)
for a in ("DA", "PDA"):
    r1 = p15.run_arm15(I, a, PRM, W); r2_ = p15.run_arm15(I2, a, PRM, W); chk(f"no_oracle_in_search_{a}", r1["F_search"] == r2_["F_search"] and r1["D"] == r2_["D"] and r1["F_oracle"] != r2_["F_oracle"])
json.dump(T, open(B + "/p15/p15_tests_results.json", "w"), indent=1); print("ALL", all(T.values()))
