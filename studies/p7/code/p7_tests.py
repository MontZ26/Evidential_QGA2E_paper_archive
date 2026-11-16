"""P7 technical tests (seeds 7900-7909). Output p7_tests_engine.json"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p7, p7_g0 as G
OUT = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p7/p7_tests_engine.json"; res = {}; ok_all = True
def rec(n, ok, **kw):
    global ok_all; ok_all &= bool(ok); res[n] = dict(ok=bool(ok), **kw); print(n, "OK" if ok else "FAIL", kw, flush=True)
P, K = p7.P, p7.K; I = P.build("S4-RC101", 7900); M = I["M"]; n_p, n_t = I["n_p"], I["n_t"]; rng = np.random.RandomState(3)
base = dict(N=20, pc=0.8, eta_k=2.0, w=0.5, eps=0.005, p_LS=0.25, k_LS=50, rule="pondere")
# 1 closed forms in engine == G0 closed forms
mx = 0.0
for rule, mode in (("V1", "dempster"), ("V2", "cautious")):
    for t in range(10):
        N = int(rng.randint(5, 80)); decs = np.zeros((N, n_p), int)
        for p in range(n_p):
            al = np.flatnonzero(M[p]); decs[:, p] = rng.choice(al, N)
        w = float(rng.uniform(0.1, 0.95)); Pn, md = p7.population_model(decs, M, w, rule)
        for p in range(n_p):
            Kp = int(M[p].sum()); al = np.flatnonzero(M[p]); counts = [int((decs[:, p] == a).sum()) for a in al]
            pg, _ = G.closed_M1(counts, w, mode, Kp); mx = max(mx, float(np.max(np.abs(Pn[p, al] - pg))))
rec("T1_engine_matches_G0_closed_forms", mx < 1e-9, max_dev=mx)
# 2 V0c formula
decs = np.zeros((40, n_p), int)
for p in range(n_p): decs[:, p] = rng.choice(np.flatnonzero(M[p]), 40)
Pn, _ = p7.population_model(decs, M, 0.4, "V0c"); fr = np.zeros((n_p, n_t))
for p in range(n_p): fr[p] = np.bincount(decs[:, p], minlength=n_t) / 40.0
ref = 0.4 * fr + 0.6 * M / M.sum(1, keepdims=True); rec("T2_V0c_formula", np.allclose(Pn, ref) and np.allclose(Pn.sum(1), 1), )
# 3 identical initial populations (budget = N)
fr_ = [p7.run7(I, r, base, budget=20)["front"] for r in p7.RULES]; rec("T3_same_initial_population", all(f == fr_[0] for f in fr_))
# 4 exact budget, N=20/100, LS on/off
bad = []
for N in (20, 100):
    for rule in p7.RULES:
        for pl in (0.0, 0.25):
            r = p7.run7(I, rule, dict(base, N=N, p_LS=pl), ); 
            if r["n_eval"] != 6040: bad.append((N, rule, pl, r["n_eval"]))
rec("T4_budget_exact", not bad, bad=bad)
# 5 floor / normalisation in the sampled model and no fallback in a normal run
r = p7.run7(I, "V1", dict(base, N=40)); m = r["model"].P; mask = M == 1
rec("T5_floor_norm", np.allclose(m.sum(1), 1) and (m[mask] >= base["eps"] - 1e-12).all() and (m[~mask] == 0).all() and r["cnt"]["fallback_events"] == 0)
# 6 budget stop rule inside LS
bad = []
for bud in (150, 157, 163, 233, 1001):
    r = p7.run7(I, "V2", dict(base, N=20), budget=bud)
    if r["n_eval"] != bud: bad.append((bud, r["n_eval"]))
rec("T6_budget_stop", not bad, bad=bad)
# 7 determinism
a = p7.run7(I, "V2", base); b = p7.run7(I, "V2", base); rec("T7_determinism", a["front"] == b["front"])
# 8 V0 (P5 code) equals stored P5 shard (C2 arm) via run_arm
t5 = json.load(open(p7.P5DIR + "/p5_tuned.json")); cfg = dict(kind="rot", strat="c", prm=t5["C2c"]["prm"]); sh = json.load(open(p7.P5DIR + "/runs/conf/S4-RC101__5200.json")); Ia = P.build("S4-RC101", 5200)
c = K.run_arm(Ia, cfg); rec("T8_V0_equals_stored_P5_C2", c["front"] == sh["conds"]["C2"]["front"])
# 9 distinct rules give different models on a diverse population (non-degeneracy)
decs = np.zeros((40, n_p), int)
for p in range(n_p): decs[:, p] = rng.choice(np.flatnonzero(M[p]), 40)
Ps = {r_: p7.population_model(decs, M, 0.6, r_)[0] for r_ in p7.RULES}; rec("T9_rules_differ", float(np.abs(Ps["V1"] - Ps["V2"]).mean()) > 1e-3 and float(np.abs(Ps["V2"] - Ps["V0c"]).mean()) > 1e-3)
res["all_ok"] = ok_all; json.dump(res, open(OUT, "w"), indent=1, default=str); print("ALL_OK", ok_all)
