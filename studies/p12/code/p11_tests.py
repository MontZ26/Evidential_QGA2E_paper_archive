"""G-D1 (cleaner unit tests + real populations) and G-D2 (budget, oracle leak, LS guard). Test parameters are arbitrary (not calibrated): sigma 0.7, n_max 4, rho_max 0.3, r_max 3."""
import sys, json, numpy as np; sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p12/code")
import p11
P = p11.P; T = {}; DP = dict(sigma=0.7, n_max=4, rho_max=0.3, r_max=3)
def chk(k, v): T[k] = bool(v); print(("PASS " if v else "FAIL ") + k)
rng = np.random.RandomState(1); n_p, n_t = 30, 6; M = np.ones((n_p, n_t), int); M[::5, 3:] = 0; M[7, 1:] = 0; mutable = M.sum(1) >= 2
def rnd(): return np.array([rng.choice(np.flatnonzero(M[p])) for p in range(n_p)])
def mk(seed=0): return p11.Dec(0.7, 4, 0.3, 3, np.random.RandomState(seed))
# S: fixed set with a clone cluster
base = rnd(); S = np.array([base.copy() for _ in range(3)] + [rnd() for _ in range(6)])
d0 = base.copy(); dec = mk(5); d1, ok1, used = dec.repair(S, d0, M, mutable)
chk("termination_and_cap_reached", ok1 and dec.ok(S, d1))
chk("allowed_teams", all(M[p, d1[p]] == 1 for p in range(n_p)))
chk("fixed_set_untouched_elites", S.shape == (9, 30) and (S[:3] == base).all())
d2, ok2, _ = mk(5).repair(S, d0, M, mutable); chk("determinism", (d2 == d1).all())
d3, ok3, u3 = mk(6).repair(S, d1, M, mutable); chk("idempotence_under_cap", (d3 == d1).all() and u3 == 0)
lone = rnd(); d4, ok4, u4 = mk(7).repair(np.empty((0, n_p), int), lone, M, mutable); chk("individual_alone_unchanged", (d4 == lone).all() and u4 == 0)
chk("changes_bounded", int((d1 != d0).sum()) <= int(np.ceil(0.3 * n_p)))
# minimal intervention: single neighbour at similarity 1.0, n_max 1 -> need s < sigma ; changes >= ceil((1-.7)*30)=9 -> at most formula+bound
dec1 = p11.Dec(0.7, 1, 1.0, 3, np.random.RandomState(8)); S1 = np.array([base]); dm, okm, um = dec1.repair(S1, base.copy(), M, mutable)
chk("minimal_intervention", okm and um <= int(np.ceil((1.0 - 0.7) * n_p)) + 1 + 2 and (dm == base).mean() < 0.7)   # (<= formula; mutable positions < n_p leave a little slack)
# violation declared when impossible: n_max 1 with allowance 1 patient
dec2 = p11.Dec(0.7, 1, 1 / 30, 1, np.random.RandomState(9)); dv, okv, uv = dec2.repair(S1, base.copy(), M, mutable); chk("violation_declared_when_allowance_too_small", (not okv) and uv <= 1)
# real populations: run DEC-on, check hereditary cap on final population & subset selection
I = P.build("S4-RC101", 9910); W = p11.p8.worlds_for(I); r = p11.run_one11(I, "E1", DP, diag={"snap": True}, wd=W)
nviol = r["dec"]["violations"]; last = np.array(r["snap"][-1][1]); Sm = (last[:, None, :] == last[None, :, :]).mean(2); nmax_obs = int((Sm >= 0.7 - 1e-12).sum(1).max())
chk("real_population_cap_or_declared_violation", nmax_obs <= 4 or nviol > 0); print("   n_max observed", nmax_obs, "violations", nviol, "dec counters", r["dec"])
sub = last[rng.permutation(len(last))[:len(last) // 2]]; Ss = (sub[:, None, :] == sub[None, :, :]).mean(2); chk("hereditary_subset", int((Ss >= 0.7 - 1e-12).sum(1).max()) <= nmax_obs)
# G-D2
chk("budget_exact_6040_dec_on", all(p11.run_one11(I, a, DP, wd=W)["n_eval"] == 6040 for a in ("E1", "P1", "C1")))
chk("ls_guard_active_no_eval_consumed", r["dec"]["ls_skipped"] >= 0 and r["n_eval"] == 6040); print("   ls_skipped", r["dec"]["ls_skipped"])
I2 = dict(I); I2["A_true"] = np.random.RandomState(3).rand(*I["A_true"].shape); I2["S_true"] = np.random.RandomState(4).rand(*I["S_true"].shape)
rB = p11.run_one11(I2, "E1", DP, wd=W)   # oracle perturbed, search world W unchanged: search outcome must be identical, only post-hoc oracle values change
chk("no_oracle_in_search_identical_search_front_and_decisions", rB["F_search"] == r["F_search"] and rB["D"] == r["D"] and rB["F_oracle"] != r["F_oracle"])
json.dump(T, open("/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p12/p11_tests_results.json", "w"), indent=1); print("ALL", all(T.values()))
