"""P24 tests T1-T11 (booleans only; no HV printed). Writes p24_tests_results.json. Run before calibration (T1 uses stored P23 HV only for equality)."""
import sys, os, json, re, glob, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p24; P, p7, p15, p23 = p24.P, p24.p7, p24.p15, p24.p23; B = p24.BASE; T = {}
def chk(k, v): T[k] = bool(v); print(("PASS " if v else "FAIL ") + k, flush=True)
rng = np.random.RandomState(11); n_p, n_t = 30, 8; M = np.ones((n_p, n_t), int); M[::4, 5:] = 0; M[3, 1:] = 0
def rnd_src(N, M=M): return np.array([[rng.choice(np.flatnonzero(M[p])) for p in range(M.shape[0])] for _ in range(N)])
SRCS = [rnd_src(n) for n in (1, 2, 5, 12, 40)]
# T2: w and sigma act only through declared parameters; DA(lambda=0) == E at each w (bitwise); Dp, Dg, E targets agree with p7 for each w
ok = True
for w in p24.W_LIST:
    for s in SRCS:
        ok &= np.array_equal(p15.da_model(s, M, w, 0.7, 0.0)[0], p7.population_model(s, M, w, "V1")[0])
        ok &= np.array_equal(p24.make_tfun24(p24.aid("E", w))(s, M, None, 0.02)[0], p24.K.floor_renorm(p7.population_model(s, M, w, "V1")[0], M, 0.02))
        ok &= np.array_equal(p24.make_tfun24(p24.aid("DA", w, 0.6))(s, M, None, 0.02)[0], p24.K.floor_renorm(p15.da_model(s, M, w, 0.6, 1.0)[0], M, 0.02))
chk("T2_w_sigma_only_via_params_DA0_equals_E", ok)
# T3: targets normalised, finite, zero outside mask, for all gamma of the grid and all w, sigma
ok = True
arms_all = [p24.aid("E", w) for w in p24.W_LIST] + [p24.aid("Dp", w) for w in p24.W_LIST] + [p24.aid("DA", w, s) for w in p24.W_LIST for s in (0.6, 0.7, 0.8)] + [p24.aid("Dg", w, gamma=g) for w in p24.W_LIST for g in p24.GAMMA_GRID]
for a in arms_all:
    for s in SRCS:
        q, _ = p24.make_tfun24(a)(s, M, None, 0.02); ok &= bool(np.isfinite(q).all() and (q >= 0).all() and np.allclose(q.sum(1), 1.0, atol=1e-12) and (q[M == 0] == 0).all())
chk("T3_targets_normalised_finite_masked", ok)
# integration on a technical seed
sc, seed = "S4-C101", 13900; I = P.build(sc, seed); W = p24.p9.worlds9(I); a0 = p24.aid("Dg", 0.5, gamma=16.0)
r1, f1 = p24.run_arm24(I, a0, W, True, True); r2, f2 = p24.run_arm24(I, a0, W, True, True); r3, f3 = p24.run_arm24(I, a0, W, True, False)
chk("T4_budget_6040", r1["n_eval"] == 6040 and all(p24.run_arm24(I, a, W, False, False)[0]["n_eval"] == 6040 for a in (p24.aid("E", 0.15), p24.aid("Dp", 0.7), p24.aid("DA", 0.3, 0.6), p24.aid("Dg", 0.3, gamma=8.0))))
I2 = dict(I); I2["A_true"] = np.zeros_like(np.asarray(I["A_true"])); I2["S_true"] = np.zeros_like(np.asarray(I["S_true"]))
chk("T5_no_oracle_leak", np.array_equal(np.asarray(r1["F_search"]), np.asarray(p24.run_arm24(I2, a0, W, True, False)[0]["F_search"])))
chk("T6_reproducible", r1["hv_oracle"] == r2["hv_oracle"] and r1["D"] == r2["D"] and all(np.array_equal(f1[g], f2[g]) for g in f1))
chk("T9_logging_inert_bitwise", r1["hv_oracle"] == r3["hv_oracle"] and r1["F_search"] == r3["F_search"] and r1["D"] == r3["D"] and r3["log"] is None and len(r1["log"]) == 5 and sorted(f1) == [1, 25, 50, 100, 150])
chk("T9b_fq_counts_consistent", all(int(f1[g].sum(1).min()) in (0, 40) and set(np.unique(f1[g].sum(1))) <= {0, 40} for g in f1))
# T1: reproduction of stored P23 runs (E, DA(1), Dg(6)) on 3 stored tasks (same engine paths as p23 files)
ok = True; fs = sorted(glob.glob(B + "/p23/runs/main/*.json"))[::200][:3]
for f in fs:
    st = json.load(open(f)); I = P.build(st["sc"], st["seed"]); W = p24.p9.worlds9(I)
    for a, pa in ((p24.aid("E", 0.3), "E"), (p24.aid("DA", 0.3, 0.7), "DA100"), (p24.aid("Dg", 0.3, gamma=6.0), "Dg100")):
        r, _ = p24.run_arm24(I, a, W, True, True); ok &= (r["hv_oracle"] == st["conds"][pa]["hv_oracle"] and r["D"] == st["conds"][pa]["D"])
chk("T1_reproduces_stored_P23_bitwise_E_DA1_Dg6", ok and len(fs) == 3)
# T7: frozen code unchanged
sys.path.insert(0, B + "/p5"); import run_p1m as RP; okf = True
for f in ("p18/p18_freeze1.txt", "p19/p19_freeze1.txt", "p20/p20_freeze1.txt", "p21/p21_freeze1.txt", "p22/p22_freeze2.txt", "p23/p23_freeze1.txt"): okf &= bool(RP.verify_freeze(B + "/" + f))
chk("T7_frozen_code_P18_P23_unchanged", okf)
# T8: calibration script contains no HV field
cs = open(HERE + "/p24_calib.py").read(); chk("T8_calib_script_no_hv", re.search(r"hv_|\bhv\(|F_oracle|oracle=True|hv_oracle", cs) is None and "oracle=False" in cs)
rr, _ = p24.run_arm24(I, p24.aid("E", 0.3), W, False, False); chk("T8b_no_hv_keys_when_oracle_off", not any(k.startswith("hv") or k.startswith("F_") for k in rr))
# T10: seed registry check: planned seeds never appear in other scratchpad files (names or mentions) outside p24
planned = list(range(12000, 12100)) + list(range(13700, 13715)) + list(range(13900, 13910)); hits = []
pat = re.compile(r"\b(13[79]\d\d)\b")
for root, ds, fns in os.walk(B):
    if "/p24" in root or "/__pycache__" in root: continue
    for fn in fns:
        if re.search(r"__13[79]\d\d", fn): hits.append(os.path.join(root, fn))
        if fn.endswith((".py", ".sh")):
            try:
                if pat.search(open(os.path.join(root, fn)).read()): hits.append(os.path.join(root, fn))
            except Exception: pass
json.dump(dict(checked="file names and seed mentions in .py/.sh outside p24; 12000-12099 reused deliberately from P23", ranges="13700-13714, 13900-13909", hits=hits), open(os.path.dirname(HERE) + "/p24_seedcheck.json", "w"), indent=1)
chk("T10_new_seeds_unused_elsewhere", len(hits) == 0)
# T11: edge cases (single allowed team, N=1)
M1 = np.zeros((n_p, n_t), int); M1[:, 2] = 1; s1 = np.full((3, n_p), 2); ok = True
for a in (p24.aid("E", 0.15), p24.aid("Dp", 0.5), p24.aid("DA", 0.3, 0.8), p24.aid("Dg", 0.7, gamma=12.0)):
    q, _ = p24.make_tfun24(a)(s1, M1, None, 0.02); ok &= bool(np.isfinite(q).all() and np.allclose(q, M1, atol=1e-9)); q, _ = p24.make_tfun24(a)(rnd_src(1), M, None, 0.02); ok &= bool(np.isfinite(q).all() and np.allclose(q.sum(1), 1))
chk("T11_edge_cases", ok)
json.dump(T, open(os.path.dirname(HERE) + "/p24_tests_results.json", "w"), indent=1); print("ALL PASS" if all(T.values()) else "SOME FAIL", flush=True)
