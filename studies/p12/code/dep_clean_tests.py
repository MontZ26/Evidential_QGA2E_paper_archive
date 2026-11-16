import sys, json; sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p12/code")
import numpy as np, dep_clean as D
rng = np.random.RandomState(1); N, n_p, n_t = 44, 60, 5; M = (rng.rand(n_p, n_t) < 0.7).astype(int); M[np.arange(n_p), rng.randint(0, n_t, n_p)] = 1
def pop(clone_groups):
    X = np.zeros((N, n_p), int)
    for p in range(n_p): X[:, p] = rng.choice(np.flatnonzero(M[p]), N)
    for g in clone_groups: base = X[g[0]].copy(); X[g] = base
    return X
res = {}; sigma, tau, rho = 0.9, 0.3, 0.3
Xi = pop([]); res["T1_all_distinct_dep0"] = D.dep(Xi, sigma)[0] < 1e-9
Xc = np.tile(pop([])[0], (N, 1)); d, neff, _ = D.dep(Xc, sigma); res["T2_all_clones_dep1_neff1"] = abs(d - 1) < 1e-9 and abs(neff - 1) < 1e-9
X2 = pop([list(range(22)), list(range(22, 44))]); d2 = D.dep(X2, sigma)[0]; res["dep_two_clone_groups"] = d2; res["marg_entropy_two_groups"] = D.marg_entropy(X2, n_t)
mov = np.zeros(N, bool); mov[10:44] = True; elite = ~mov
Xo, log = D.clean(X2, M, mov, sigma, tau, rho, np.random.RandomState(7)); res["T3_reaches_threshold_or_stalls"] = bool(log[-1] <= tau or log[-1] <= log[0]); res["dep_before_after"] = [log[0], log[-1]]; res["steps"] = len(log) - 1
res["T4_elites_unchanged"] = bool(np.array_equal(Xo[elite], X2[elite])); res["T5_allowed_teams_only"] = bool(np.all(M[np.arange(n_p)[None, :], Xo] == 1))
res["T6_deterministic_same_seed"] = bool(np.array_equal(Xo, D.clean(X2, M, mov, sigma, tau, rho, np.random.RandomState(7))[0]))
Xo2, log2 = D.clean(Xo, M, mov, sigma, tau, rho, np.random.RandomState(8)); res["T7_idempotent_below_tau"] = bool(log[-1] > tau or np.array_equal(Xo, Xo2))
res["T8_single_individual_unchanged"] = bool(np.array_equal(D.clean(X2[:1], M, np.ones(1, bool), sigma, tau, rho, np.random.RandomState(7))[0], X2[:1]))
res["T9_dep_nonincreasing_along_steps"] = bool(all(log[i + 1] <= log[i] + 1e-12 for i in range(len(log) - 1))); res["marg_entropy_after"] = D.marg_entropy(Xo, n_t)
# elites-only dependent: nothing movable -> unchanged, stall
Xe, loge = D.clean(X2, M, np.zeros(N, bool), sigma, tau, rho, np.random.RandomState(7)); res["T10_no_movable_unchanged"] = bool(np.array_equal(Xe, X2))
res["all_ok"] = bool(all(v for k, v in res.items() if k.startswith("T"))); json.dump(res, open("/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p12/dep_clean_synthetic_tests.json", "w"), indent=1, default=float); print(json.dumps(res, indent=1, default=float))
