"""P23 unit/integration tests T1-T13 (no HV value is printed; booleans only). Writes p23_tests_results.json."""
import sys, json, math, os, re, hashlib, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import p23; P, X, K, p7, p14, p15 = p23.P, p23.X, p23.K, p23.p7, p23.p14, p23.p15
B = p23.BASE; T = {}
def chk(k, v): T[k] = bool(v); print(("PASS " if v else "FAIL ") + k, flush=True)
base = json.load(open(B + "/p15/p15_params.json"))["chosen"]; w, eps = base["w"], base["eps"]
PRM = dict(base, gamma={"DA25": 1.5, "DA50": 2.0, "DA100": 3.0}, rho0=0.1, gmix=0.5)
rng = np.random.RandomState(7); n_p, n_t = 30, 8; M = np.ones((n_p, n_t), int); M[::4, 5:] = 0; M[3, 1:] = 0; mut = M.sum(1) >= 2
def rnd_src(N, M=M):
    return np.array([[rng.choice(np.flatnonzero(M[p])) for p in range(M.shape[0])] for _ in range(N)])
def near_dup_src():
    b = rnd_src(5); rows = []
    for x in b:
        rows.append(x)
        for _ in range(rng.randint(0, 5)):
            c = x.copy(); idx = rng.choice(n_p, rng.randint(0, 6), replace=False)
            for p in idx: c[p] = rng.choice(np.flatnonzero(M[p]))
            rows.append(c)
    return np.array(rows)
SRCS = [near_dup_src() for _ in range(12)] + [rnd_src(1), rnd_src(2), rnd_src(40)]
# T1 lambda=0 reproduces E (bit for bit) on the target ; and DA(0) engine path
t1 = all(np.array_equal(p15.da_model(s, M, w, 0.7, 0.0)[0], p7.population_model(s, M, w, "V1")[0]) for s in SRCS); chk("T1_lambda0_equals_E_target_bitwise", t1)
# T3 sums, finite, positive
ok = True
for s in SRCS:
    for a in p23.ARMS23:
        q, md = p23.make_tfun(a, PRM)(s, M, w, eps); ok &= bool(np.isfinite(q).all() and (q >= 0).all() and np.allclose(q.sum(1), 1.0, atol=1e-12) and (q[M == 0] == 0).all())
chk("T3_q_sums_finite_nonneg_masked", ok)
# T4 m(Theta) non-decreasing in lambda
ok = True
for s in SRCS:
    ms = [p15.da_model(s, M, w, 0.7, l)[1]["m_theta"] for l in (0.0, 0.25, 0.5, 1.0)]; ok &= all(ms[i] <= ms[i + 1] + 1e-12 for i in range(3))
chk("T4_mTheta_nondecreasing_in_lambda", ok)
# T5 permutation invariance and exact-duplication invariance at lambda=1
s = SRCS[0]; perm = rng.permutation(len(s)); ok = True
for a in ("DA100", "RHO", "E"):
    f = p23.make_tfun(a, PRM); ok &= np.allclose(f(s, M, w, eps)[0], f(s[perm], M, w, eps)[0], atol=1e-12)
chk("T5a_permutation_invariance", ok)
x = rnd_src(1); f = p23.make_tfun("DA100", PRM); qs = [f(np.repeat(x, c, 0), M, w, eps)[0] for c in (1, 2, 3, 5)]; chk("T5b_duplication_invariance_lambda1", all(np.allclose(qs[0], q, atol=1e-12) for q in qs))
# T6 edge cases: N=1, K=1 (single allowed team), single supported team
M1 = np.zeros((n_p, n_t), int); M1[:, 2] = 1; s1 = np.full((3, n_p), 2); ok = True
for a in p23.ARMS23:
    q, _ = p23.make_tfun(a, PRM)(s1, M1, w, eps); ok &= bool(np.isfinite(q).all() and np.allclose(q, M1, atol=1e-9))
for a in p23.ARMS23:
    q, _ = p23.make_tfun(a, PRM)(rnd_src(1), M, w, eps); ok &= bool(np.isfinite(q).all() and np.allclose(q.sum(1), 1))
chk("T6_edge_cases", ok)
# T11 Rho / Rmix identities
ok = True
for s in SRCS:
    ok &= np.array_equal(p23.rho_model(s, M, w, 0.0)[0], p7.population_model(s, M, w, "V1")[0])
    S = p23.sim_matrix(s); N = len(s)
    for lam in (0.25, 0.5, 1.0):
        Rho = lam * (S >= 0.7).astype(float); np.fill_diagonal(Rho, 0.0); al = p23.rho_matrix_alpha(s, Rho); nt = p23.counts_from_alpha(s, al, n_t)
        ok &= np.allclose(p23.dempster_cnt(nt, M, w)[0], p15.da_model(s, M, w, 0.7, lam)[0], atol=1e-12)
    ok &= np.array_equal(p23.mix_model(s, M, w, 1.0)[0], p7.population_model(s, M, w, "V1")[0]); ok &= np.array_equal(p23.mix_model(s, M, w, 0.0)[0], p7.population_model(s, M, w, "V2")[0])
chk("T11a_rho0_E_binary_rho_DA_mix_limits", ok)
ok = True; om = -math.log(1 - w)
for s in SRCS:                                  # independent closed form of the cautious target
    C = np.zeros((n_p, n_t)); np.add.at(C, (np.tile(np.arange(n_p), len(s)), s.ravel()), 1.0); Sup = (C > 0).astype(float); Kp = M.sum(1, keepdims=True)
    D = 1 + Sup.sum(1, keepdims=True) * (math.exp(om) - 1); ref = (Sup * (math.exp(om) - 1) + M / Kp) / D; ok &= np.allclose(p7.population_model(s, M, w, "V2")[0], ref, atol=1e-12)
chk("T11b_cautious_closed_form", ok)
# integration tests on one real task (technical seed): T7, T8, T9, T13 ; T2 on stored P17 run
sc, seed = "S4-C101", 12900; I = P.build(sc, seed); W = p23.p9.worlds9(I)
r1 = p23.run_arm23(I, "DA100", PRM, W, oracle=True, logging=True); r2 = p23.run_arm23(I, "DA100", PRM, W, oracle=True, logging=True); r3 = p23.run_arm23(I, "DA100", PRM, W, oracle=True, logging=False)
chk("T7_budget_6040_all_arms", all(p23.run_arm23(I, a, PRM, W, oracle=False, logging=False)["n_eval"] == 6040 for a in p23.ARMS23))
chk("T9_reproducible", r1["hv_oracle"] == r2["hv_oracle"] and r1["F_search"] == r2["F_search"] and r1["D"] == r2["D"])
chk("T13_logging_inert", r1["hv_oracle"] == r3["hv_oracle"] and r1["F_search"] == r3["F_search"] and r1["D"] == r3["D"] and r3["log"] is None and len(r1["log"]) == 5)
I2 = dict(I); I2["A_true"] = np.zeros_like(np.asarray(I["A_true"])); I2["S_true"] = np.zeros_like(np.asarray(I["S_true"]))
r4 = p23.run_arm23(I2, "DA100", PRM, W, oracle=False, logging=False); chk("T8_no_oracle_leak_search_independent_of_oracle_world", r4["n_eval"] == 6040 and np.array_equal(np.asarray(r1["F_search"]), np.asarray(p23.run_arm23(I2, "DA100", PRM, W, oracle=True, logging=False)["F_search"])) is True)
chk("T8b_oracle_recomputed_from_archive", np.allclose(np.asarray(r1["F_oracle"]), p14._oracle_eval(I, np.asarray(r1["D"])), atol=0))
# T2 : reproduces the stored P17 E and DA runs (same instance, seed 11200)
st = json.load(open(B + "/p17/runs/tier1/S4-C101__11200.json"))["conds"]; I = P.build("S4-C101", 11200); W = p23.p9.worlds9(I)
chk("T2a_E_reproduces_stored_P17", p23.run_arm23(I, "E", PRM, W, True, False)["hv_oracle"] == st["E"]["hv_oracle"])
chk("T2b_DA_lambda1_reproduces_stored_P17", p23.run_arm23(I, "DA100", PRM, W, True, False)["hv_oracle"] == st["DA"]["hv_oracle"])
# T10 frozen code unchanged (existing freeze files of P18, P19, P20, P21, P22)
sys.path.insert(0, B + "/p5"); import run_p1m as RP
okf = True
for f in ("p18/p18_freeze1.txt", "p19/p19_freeze1.txt", "p20/p20_freeze1.txt", "p21/p21_freeze1.txt", "p22/p22_freeze2.txt"): okf &= bool(RP.verify_freeze(B + "/" + f))
chk("T10_frozen_code_unchanged_hash_check", okf)
# T12 calibration script has no HV field and run_arm23(oracle=False) yields none
cs = HERE + "/p23_calib.py"; chk("T12a_calib_script_no_hv", (not os.path.exists(cs)) or re.search(r"hv_|\bhv\(|F_oracle|oracle=True|hv_oracle", open(cs).read()) is None)
rr = p23.run_arm23(I, "E", PRM, W, oracle=False, logging=False); chk("T12b_no_hv_keys_when_oracle_off", not any(k.startswith("hv") or k.startswith("F_") for k in rr))
json.dump(T, open(os.path.dirname(HERE) + "/p23_tests_results.json", "w"), indent=1); print("ALL PASS" if all(T.values()) else "SOME FAIL", flush=True)
