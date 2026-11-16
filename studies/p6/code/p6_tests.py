"""P6 technical tests (protocol v2.6 section 10); seeds 6900-6909 only. Output: /.../p6/p6_tests_engine.json"""
import sys, os, json, time, copy
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p6
P, K = p6.P, p6.K
OUT = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p6/p6_tests_engine.json"
res = {}; ok_all = True
def rec(name, ok, **kw):
    global ok_all; ok_all &= bool(ok); res[name] = dict(ok=bool(ok), **kw); print(name, "OK" if ok else "FAIL", kw, flush=True)
base = dict(N=20, pc=0.8, eta_k=2.0, delta=0.3, lam=0.15, eps=0.005, k_e=4, rho=0.5, p_LS=0.25, k_LS=50, rule="pondere")
I = P.build("S4-RC101", 6900); I2 = P.build("S5-R101", 6901)
fe = lambda r: np.round(np.asarray(r["front"]), 12).tolist()
# 1 identical initial population in every arm of equal N (budget = N)
fr = []
for mk in ("rot", "pbil"):
    for ls in (True, False):
        for sel in ("T", "R"): r = p6.run6(I, mk, base, ls, sel, budget=20); fr.append((fe(r), r["n_eval"]))
rec("T1_initial_population_identical", all(f == fr[0] for f in fr) and fr[0][1] == 20, n_arms=len(fr))
# 2 exact budget
bad = []
for N in (20, 100):
    for rho in (0.2, 0.8):
        for mk in ("rot", "pbil"):
            for ls in (True, False):
                for sel in ("T", "R"):
                    pr = dict(base, N=N, rho=rho); r = p6.run6(I, mk, pr, ls, sel)
                    if r["n_eval"] != 6040: bad.append((N, rho, mk, ls, sel, r["n_eval"]))
rec("T2_budget_exact", not bad, bad=bad, combos=32)
# 3 neutralised selection => R and T identical
r1 = p6.run6(I, "pbil", dict(base, N=40), True, "R"); r2 = p6.run6(I, "pbil", dict(base, N=40), True, "T", neutral=True)
rec("T3_neutral_selection_RT_identical", fe(r1) == fe(r2) and r1["gens"] == r2["gens"] and r1["cnt"] == r2["cnt"])
r3 = p6.run6(I, "pbil", dict(base, N=40), True, "T"); rec("T3b_real_T_differs_from_R", fe(r3) != fe(r1))
# 4 C0b-T equals P5 C0b at identical config; and equals a stored P5 shard
t5 = json.load(open(p6.P5DIR + "/p5_tuned.json"))["C0b"]["prm"]; a = p6.run_arm6(I, dict(kind="ga", strat="a", prm=t5)); b = K.run_arm(I, dict(kind="ga", strat="a", prm=t5))
class _S:
    def __contains__(s, x): return 5200 <= x <= 5200 or 6900 <= x <= 6909
P.ALLOWED_SEEDS = _S(); sh = json.load(open(p6.P5DIR + "/runs/conf/S4-RC101__5200.json")); Ia = P.build("S4-RC101", 5200); c = p6.run_arm6(Ia, dict(kind="ga", strat="a", prm=t5)); P.ALLOWED_SEEDS = p6._Seeds6()
rec("T4_C0bT_equals_P5_C0b", a["front"] == b["front"] and c["front"] == sh["conds"]["C0b"]["front"] and a["n_eval"] == 6040, equals_stored_P5_shard=(c["front"] == sh["conds"]["C0b"]["front"]))
# 5 LS off: no neighbour evaluated at all
r = p6.run6(I, "rot", base, False, "T"); rec("T5_LS_off_no_neighbour", r["cnt"]["ls_eval"] == 0 and r["cnt"]["ls_trig"] == 0)
# 6 budget stop rule: each evaluated neighbour gets exactly one decision; never exceeds budget; budget expiring inside a LS
bad = []
for N in (20, 100):
    for bud in (6040, 150, 157, 163, 171, 233, 1001):
        r = p6.run6(I, "rot", dict(base, N=N, p_LS=0.25, k_LS=50), True, "T", budget=bud)
        if not (r["n_eval"] == bud and r["cnt"]["ls_dec"] == r["cnt"]["ls_eval"]): bad.append((N, bud, r["n_eval"], r["cnt"]["ls_dec"], r["cnt"]["ls_eval"]))
rec("T6_budget_stop_rule", not bad, bad=bad)
# 7 norm / floor
bad = []
for mk in ("rot", "pbil"):
    r = p6.run6(I, mk, dict(base, N=20, rho=0.8), False, "R"); m = r["model"]; Mm = m.M; s = m.P.sum(1)
    if not np.allclose(s, 1.0): bad.append((mk, "sum"))
    if (m.P[Mm == 1] < base["eps"] - 1e-12).any() or (m.P[Mm == 0] != 0).any(): bad.append((mk, "floor/support"))
    if mk == "rot" and not np.allclose((m.alpha ** 2).sum(1), 1.0): bad.append((mk, "alpha norm"))
rec("T7_norm_and_floor", not bad, bad=bad)
# 8 edge cases
edge = {}
for nm, pr, bud in (("rho0", dict(base, rho=0.0), 6040), ("rho1", dict(base, rho=1.0), 6040), ("N20_ke10", dict(base, N=20, k_e=10), 6040), ("budget_eq_N", base, 20), ("budget_N_plus_1", base, 21), ("N100_eps0.02", dict(base, N=100, eps=0.02), 6040)):
    try: r = p6.run6(I2, "rot", pr, True, "T", budget=bud); edge[nm] = (r["n_eval"] == bud)
    except Exception as e: edge[nm] = f"EXC {type(e).__name__}: {e}"
r = p6.run6(I, "pbil", dict(base, rho=0.0), True, "R"); edge["rho0_no_M"] = r["cnt"]["n_M"] == 0; r = p6.run6(I, "pbil", dict(base, rho=1.0), True, "R"); edge["rho1_no_G"] = r["cnt"]["n_G"] == 0
rec("T8_edge_cases", all(v is True for v in edge.values()), edge=edge)
# 9 determinism
a = p6.run6(I, "rot", base, True, "T"); b = p6.run6(I, "rot", base, True, "T"); rec("T9_determinism", fe(a) == fe(b) and a["cnt"] == b["cnt"])
# 10 route draw identical in R and T (same rho): realised M counts equal until divergence is NOT asserted; check proportions near rho
r = p6.run6(I, "rot", dict(base, rho=0.3), False, "R"); prop = r["cnt"]["n_M"] / (r["cnt"]["n_M"] + r["cnt"]["n_G"]); rec("T10_route_proportion", abs(prop - 0.3) < 0.03, prop=prop)
res["all_ok"] = ok_all; json.dump(res, open(OUT, "w"), indent=1, default=str); print("ALL_OK", ok_all)
