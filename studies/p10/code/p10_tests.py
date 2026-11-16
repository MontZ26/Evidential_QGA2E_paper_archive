"""G-Q0 (maths of V0c-Q / V1-Q), G-Q1 (non-regression, budget, oracle leak), G-Q3 (DEC on/off, diagnostics read-only)."""
import sys, json, numpy as np; sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p10/code")
import p10
P, X, K = p10.P, p10.X, p10.K; T = {}; DP = dict(sigma=0.7, n_max=2, rho_max=0.2, r_max=3)
def chk(k, v): T[k] = bool(v); print(("PASS " if v else "FAIL ") + k)
prm = dict(w=0.5, eps=0.02, dec=DP)
# ---- G-Q0 maths
rng = np.random.RandomState(0); n_p, n_t = 30, 8; M = np.ones((n_p, n_t), int); M[::4, 5:] = 0; M[3, 1:] = 0
src = np.array([[rng.choice(np.flatnonzero(M[p])) for p in range(n_p)] for _ in range(7)])
for rule in ("V0c", "V1"):
    q, md = p10.target(src, M, 0.5, rule, 0.02)
    chk(f"{rule}_normalised_floor_support", np.allclose(q.sum(1), 1) and (q[M == 0] == 0).all() and (q[M == 1] >= 0.02 - 1e-12).all())
    q2, _ = p10.target(src[rng.permutation(len(src))], M, 0.5, rule, 0.02); chk(f"{rule}_permutation_invariance", np.array_equal(q, q2))
    qi, _ = p10.target(src, M, 0.0, rule, 0.0); U = M / M.sum(1, keepdims=True); chk(f"{rule}_total_ignorance_uniform", np.allclose(qi, U))
    one = src[:1]; q1, _ = p10.target(one, M, 0.5, rule, 0.02); chk(f"{rule}_singleton_front_mode_is_source", (q1.argmax(1)[M.sum(1) >= 2] == one[0][M.sum(1) >= 2]).all())
# monotone in count (duplicates by design, P7): more copies of a team's source -> higher mass
a = src[:1].copy(); b = np.vstack([a, a, src[1:2]]); qa, _ = p10.target(np.vstack([a, src[1:2]]), M, 0.5, "V1", 0.02); qb, _ = p10.target(b, M, 0.5, "V1", 0.02)
p = 1; chk("V1_monotone_in_count", qb[p, a[0][p]] >= qa[p, a[0][p]] - 1e-12 and qb[p, a[0][p]] > 0)
# ---- G-Q1 on real instances
okR = okB = okO = True
for sc in ("S4-RC101", "S4-C101", "S5-R101"):
    I = P.build(sc, 9290); o = X.qga_pareto(I, True, archive=True); r = p10.run_q(I); okB &= np.array_equal(o["arch_F"], r["F"]) and np.array_equal(o["arch_cands"], r["D"]) and r["n_eval"] == 6040
    s0 = p10.run_q(I, "V0c", 1.0, 0.0, single=True); okR &= np.array_equal(o["arch_F"], s0["F"]) and np.array_equal(o["arch_cands"], s0["D"])
    s1 = p10.run_q(I, "V1", 1 - 1e-12, 0.0, single=True); okR &= np.allclose(np.sort(o["arch_F"], axis=0), np.sort(s1["F"], axis=0), atol=1e-9) if len(o["arch_F"]) == len(s1["F"]) else False
chk("GQ1_nonregression_QGA2E_bit_for_bit_3_instances", okB); chk("GQ0_single_source_reduces_to_QGA2E_rotation_(w=1,eps=0)", okR)
I = P.build("S4-RC101", 9291); W = p10.p9.worlds9(I)
ra = {a: p10.run_one10(I, a, prm, W) for a in p10.ARMS10}; chk("GQ1_budget_exact_6040_all_arms", all(v["n_eval"] == 6040 for v in ra.values()))
I2 = dict(I); I2["A_true"] = np.random.RandomState(3).rand(*I["A_true"].shape); I2["S_true"] = np.random.RandomState(4).rand(*I["S_true"].shape)
rb = p10.run_one10(I2, "E", prm, W); chk("GQ1_no_oracle_in_search", rb["F_search"] == ra["E"]["F_search"] and rb["D"] == ra["E"]["D"] and rb["F_oracle"] != ra["E"]["F_oracle"])
# ---- G-Q3
Is = dict(I); Is["A_true"], Is["S_true"] = W["nom"]
inert = p10.p11.Dec(0.7, 10 ** 6, 0.2, 3, P.rs(I["sc"], I["seed"], "p10_dec")); ri = p10.run_q(Is, "V1", 0.5, 0.02, inert); rn = p10.run_q(Is, "V1", 0.5, 0.02, None)
chk("GQ3_DEC_inert_cap_equals_DEC_off_bit_for_bit", np.array_equal(ri["F"], rn["F"]) and np.array_equal(ri["D"], rn["D"]) and inert.c["mutations"] == 0)
rd = p10.run_q(Is, "V1", 0.5, 0.02, None, diag=False); chk("GQ3_diagnostics_read_only_identical_fronts", np.array_equal(rd["F"], rn["F"]) and np.array_equal(rd["D"], rn["D"]))
e = ra["E_DEC"]; chk("GQ3_DEC_on_budget_and_counters", e["n_eval"] == 6040 and e["dec"]["cands"] > 0); print("   E_DEC counters", e["dec"])
fin = np.array(e["D"]); ndyn = [d["n_max_obs"] for d in e["dyn"]]; viol = e["dec"]["violations"]; chk("GQ3_cap_respected_or_violations_declared", max(ndyn) <= 2 or viol > 0); print("   max n_max_obs over gens", max(ndyn), "violations", viol)
json.dump(T, open("/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p10/p10_tests_results.json", "w"), indent=1); print("ALL", all(T.values()))
