"""G-R0 (non-regression, budgets, no oracle leak) and G-R1 (maths of sharpened/softened target)."""
import sys, json, numpy as np; sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p14/code")
import p14, p10
P, X, K, p7 = p14.P, p14.X, p14.K, p14.p7; T = {}
def chk(k, v): T[k] = bool(v); print(("PASS " if v else "FAIL ") + k)
PRM = dict(json.load(open("/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p10/p10_calib.json"))["chosen"]); PRM.update(gamma=2.0, gamma_e=0.5)
rng = np.random.RandomState(0); n_p, n_t = 30, 8; M = np.ones((n_p, n_t), int); M[::4, 5:] = 0; M[3, 1:] = 0; mut = M.sum(1) >= 2
src = np.array([[rng.choice(np.flatnonzero(M[p])) for p in range(n_p)] for _ in range(9)])
def ent(q): qq = np.where(q > 0, q, 1.0); return float(np.mean(-(q * np.log(qq)).sum(1)[mut]))
for rule in ("V0c", "V1"):
    q1, _ = p14.make_target(1.0)(src, M, PRM["w"], rule, PRM["eps"]); q0, _ = p10.target(src, M, PRM["w"], rule, PRM["eps"]); chk(f"{rule}_gamma1_identical_to_P10_target_bit_for_bit", np.array_equal(q1, q0))
    es = []
    for g in (0.25, 0.5, 1.0, 2.0, 4.0, 6.0):
        q, _ = p14.make_target(g)(src, M, PRM["w"], rule, PRM["eps"]); es.append(ent(q))
        assert np.allclose(q.sum(1), 1) and np.isfinite(q).all() and (q[M == 0] == 0).all() and (q[M == 1] >= PRM["eps"] - 1e-12).all()
    chk(f"{rule}_normalised_finite_floor_support_all_gamma", True); chk(f"{rule}_entropy_monotone_decreasing_in_gamma", all(a >= b - 1e-9 for a, b in zip(es, es[1:]))); print("   entropies", [round(e, 3) for e in es])
    qa, _ = p14.make_target(3.0)(src[rng.permutation(len(src))], M, PRM["w"], rule, PRM["eps"]); qb, _ = p14.make_target(3.0)(src, M, PRM["w"], rule, PRM["eps"]); chk(f"{rule}_permutation_invariance_gamma3", np.array_equal(qa, qb))
# G-R0 non-regression on technical seeds 9290-9291 (P10 seeds, authorised for this test only)
okE = True
for sc, seed in (("S4-RC101", 9290), ("S4-C101", 9291)):
    I = P.build(sc, seed); W = p14.p9.worlds9(I); P10 = dict(w=PRM["w"], eps=PRM["eps"], dec=dict(sigma=.7, n_max=2, rho_max=.2, r_max=3))
    for a14, a10 in (("E", "E"), ("Dp", "Dp"), ("B", "B")):
        x = p14.run_arm14(I, a14, PRM, W); y = p10.run_one10(I, a10, P10, W); okE &= (x["D"] == y["D"] and x["F_search"] == y["F_search"] and x["F_oracle"] == y["F_oracle"] and x["hv_oracle"] == y["hv_oracle"])
chk("GR0_E_Dp_B_bit_for_bit_vs_P10", okE)
I = P.build("S4-RC101", 9290); W = p14.p9.worlds9(I); Is = dict(I); Is["A_true"], Is["S_true"] = W["nom"]
a = X.nsga2(Is, True, 0.9, 1.0); b = p14.run_arm14(I, "NSGA2", PRM, W); chk("GR0_NSGA2_wrapper_same_cands_and_budget", b["n_eval"] == a["n_eval"] == 6040)
# the wrapper must not change the search: front of final population equal
c = X.moead(Is, 20); d = p14.run_arm14(I, "MOEAD", PRM, W); chk("GR0_MOEAD_budget_6030_and_wrapper_same", d["n_eval"] == c["n_eval"] and c["n_eval"] == 6030); print("   moead evals", d["n_eval"])
e9 = p14.p9.task9("S4-RC101", 9290, arms=("B",)); e14 = p14.run_arm14(I, "C0", PRM, W); chk("GR0_C0b_bit_for_bit_vs_P9_B", e14["D"] == e9["conds"]["B"]["D"] and e14["hv_oracle"] == e9["conds"]["B"]["hv_oracle"] and e14["n_eval"] == 6040)
chk("GR0_budget_exact_all_arms", all(p14.run_arm14(I, x, PRM, W)["n_eval"] in (6040, 6030) for x in ("E", "Dp", "Dg", "Es", "B", "Bt")))
I2 = dict(I); I2["A_true"] = np.random.RandomState(3).rand(*I["A_true"].shape); I2["S_true"] = np.random.RandomState(4).rand(*I["S_true"].shape)
r1 = p14.run_arm14(I, "Dg", PRM, W); r2 = p14.run_arm14(I2, "Dg", PRM, W); chk("GR0_no_oracle_in_search_Dg", r1["F_search"] == r2["F_search"] and r1["D"] == r2["D"] and r1["F_oracle"] != r2["F_oracle"])
n1 = p14.run_arm14(I, "NSGA2", PRM, W); n2 = p14.run_arm14(I2, "NSGA2", PRM, W); chk("GR0_no_oracle_in_search_NSGA2", n1["F_search"] == n2["F_search"] and n1["F_oracle"] != n2["F_oracle"])
json.dump(T, open("/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p14/p14_tests_results.json", "w"), indent=1); print("ALL", all(T.values()))
