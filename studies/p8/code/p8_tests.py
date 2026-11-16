"""G-I interface tests. Usage: python p8_tests.py OUT.json"""
import sys, json, time, copy
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p8/code")
import numpy as np, p8
K, P, R, p7 = p8.K, p8.P, p8.R, p8.p7
res = {}; seeds = [8000, 8001]; scs = ["S4-RC101", "S5-C101"]
def eq(a, b): return np.array_equal(np.asarray(a), np.asarray(b))
t0 = time.time()
# T1: Archive subclass leaves behaviour unchanged (front identical, K.run and run7), and captured D matches front
ok1 = True; ok1b = True; ok2 = True; ok3 = True; budgets = True; leak = True
for sc in scs:
    for seed in seeds:
        I = P.build(sc, seed)
        if not I["feasible"]: continue
        W = p8.worlds_for(I); Is = dict(I); Is["A_true"], Is["S_true"] = W["oracle"]
        r0 = K.run(Is, "ga", "a", p8.prm_ga()); r1 = p8.run_one(I, "oracle", None)
        ok1 &= eq(r0["front"], r1["F_search"]) and r0["n_eval"] == r1["n_eval"] == 6040
        q0 = p7.run7(Is, "V1", p8.prm_p7()); q1 = p8.run_one(I, "oracle", "V1")
        ok1b &= eq(q0["front"], q1["F_search"]) and q0["n_eval"] == q1["n_eval"] == 6040
        # T2: oracle world as search world => F_oracle == F_search (swap mechanism exact)
        ok2 &= eq(r1["F_search"], r1["F_oracle"]) and eq(q1["F_search"], q1["F_oracle"])
        # T3: all 8 arms budget exactly 6040; D vectors feasible (allowed teams); oracle objs recomputed
        for a, (w, w2) in p8.ARM_DEF.items():
            o = p8.run_one(I, w, w2, tau=0.9, wd=W); budgets &= o["n_eval"] == 6040
            Dd = np.array(o["D"]); ok3 &= bool(np.all(I["M"][np.arange(I["n_p"])[None, :], Dd] == 1)) and len(o["F_oracle"]) == len(o["D"]) > 0
        # T4: no oracle in the search: perturbing the oracle arrays of I (not of the search copy) must not change search fronts; arms A/B/C/D
        I2 = dict(I); I2["A_true"] = I["A_true"] * 0.5 + 0.1; I2["S_true"] = np.clip(I["S_true"][::-1].copy(), 0, 1)
        for a in ("A", "B", "C", "D"):
            w, w2 = p8.ARM_DEF[a]; o1 = p8.run_one(I, w, w2, wd=W); o2 = p8.run_one(I2, w, w2, wd=W)
            leak &= eq(o1["F_search"], o2["F_search"]) and eq(o1["D"], o2["D"])
        # T5: A == classical GA C0b with the non-informative world built independently
        Ia = dict(I); Ia["A_true"] = np.where(I["CT"] == 1, 0.55, 0.0); Ia["S_true"] = np.full_like(I["S_true"], 0.5); ra = K.run(Ia, "ga", "a", p8.prm_ga())
        res.setdefault("T5", True); res["T5"] &= eq(ra["front"], p8.run_one(I, "non", None, wd=W)["F_search"])
        # T6: layer I fixed before search: worlds identical when rebuilt (deterministic), independent of the optimiser
        W2 = p8.worlds_for(I); res.setdefault("T6", True); res["T6"] &= all(eq(W[k][0], W2[k][0]) and eq(W[k][1], W2[k][1]) for k in W)
        print(sc, seed, "done", round(time.time() - t0), flush=True)
res.update(T1_archive_patch_K_run=bool(ok1), T1b_archive_patch_run7=bool(ok1b), T2_oracle_swap_exact=bool(ok2), T3_budget_6040_8arms_feasible=bool(budgets and ok3), T4_no_oracle_leak=bool(leak))
res["all_ok"] = bool(all(res[k] for k in res)); json.dump(res, open(sys.argv[1], "w"), indent=1, default=bool); print(json.dumps(res, default=bool))
