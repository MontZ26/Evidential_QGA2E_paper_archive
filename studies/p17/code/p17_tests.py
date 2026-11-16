"""P17 technical tests (HV never analysed; equalities/non-leak only). Run before freeze."""
import sys, json, time, numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p17/code")
import p17, p15
P, X, K, p7 = p17.P, p17.X, p17.K, p17.p7; T = {}; B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"; INFO = {}
def chk(k, v): T[k] = bool(v); print(("PASS " if v else "FAIL ") + k, flush=True)
def timed(f):
    t = time.time(); r = f(); print("   %.1fs" % (time.time() - t), flush=True); return r
PRM = json.load(open(B + "/p15/p15_params.json"))["chosen"]; w = PRM["w"]; sg, lm = PRM["sigma"], PRM["lam"]
rng = np.random.RandomState(7); n_p, n_t = 30, 8; M = np.ones((n_p, n_t), int); M[::4, 5:] = 0; M[3, 1:] = 0; mut = M.sum(1) >= 2
def rnd(N): return np.array([[rng.choice(np.flatnonzero(M[p])) for p in range(n_p)] for _ in range(N)])
def near(N):
    base = rnd(max(2, N // 4)); rows = []
    for _ in range(N):
        b = base[rng.randint(len(base))].copy()
        for p in rng.choice(n_p, rng.randint(0, 9), replace=False): b[p] = rng.choice(np.flatnonzero(M[p]))
        rows.append(b)
    return np.array(rows)
# 2 exact gain (evidential) vs full recomputation
errs = []; viol = 0; npairs = 0
for t in range(150):
    N = rng.randint(1, 30); src = near(N) if t % 2 else rnd(N); nc = 25; mem = rng.choice(N, min(N, 8), replace=False)
    cand = np.vstack([src[mem], near(nc - len(mem))]); mp = np.array(list(range(0)) + [int(m) for m in mem] + [-1] * (nc - len(mem)))
    g1 = p17.gain_E(src, M, w, sg, lm, cand, mp); g0 = p17.ref_gain_E(src, M, w, sg, lm, cand, mp); errs.append(np.abs(g1 - g0).max())
    d0 = g0[:, None] - g0[None, :]; d1 = g1[:, None] - g1[None, :]; big = np.abs(d0) > 1e-9; viol += int((np.sign(d0[big]) != np.sign(d1[big])).sum()); npairs += int(big.sum())
errs = np.array(errs); INFO["gainE_err_max"] = float(errs.max()); INFO["gainE_err_q999"] = float(np.quantile(errs, 0.999)); INFO["gainE_rank_violations"] = viol; INFO["gainE_pairs"] = npairs
chk("2_gain_E_exact_vs_full_recompute_max_err_le_1e-9_and_zero_rank_changes", errs.max() <= 1e-9 and viol == 0); print("   ", {k: INFO[k] for k in INFO}, flush=True)
# 3 probabilistic gain
errp = []; violp = 0
for t in range(100):
    N = rng.randint(1, 30); src = near(N) if t % 2 else rnd(N); nc = 25; mem = rng.choice(N, min(N, 8), replace=False)
    cand = np.vstack([src[mem], near(nc - len(mem))]); mp = np.array([int(m) for m in mem] + [-1] * (nc - len(mem)))
    g1 = p17.gain_P(src, M, w, cand, mp); g0 = p17.ref_gain_P(src, M, w, cand, mp); errp.append(np.abs(g1 - g0).max())
    d0 = g0[:, None] - g0[None, :]; d1 = g1[:, None] - g1[None, :]; big = np.abs(d0) > 1e-9; violp += int((np.sign(d0[big]) != np.sign(d1[big])).sum())
INFO["gainP_err_max"] = float(np.max(errp)); INFO["gainP_rank_violations"] = violp
chk("3_gain_P_exact_vs_V0c_recompute", np.max(errp) <= 1e-9 and violp == 0)
# 4 interval width constant and masses/target identity
ok4 = True
for _ in range(30):
    src = near(rng.randint(2, 25)); nt, nM, al, om, D = p17.base_E(src, M, w, sg, lm); Pn, md = p15.da_model(src, M, w, sg, lm); mt = (np.exp(om * nt) - 1) / D[:, None]; mTh = 1 / D; U = M / M.sum(1, keepdims=True)
    ok4 &= bool(np.allclose(Pn, mt + mTh[:, None] * U, atol=1e-12)) and bool(np.allclose(mt.sum(1) + mTh, 1.0, atol=1e-12)) and bool(np.allclose(((mt + mTh[:, None]) - mt), mTh[:, None]))
    ok4 &= abs(float(mTh[mut].mean()) - md["m_theta"]) < 1e-12
chk("4_interval_width_equals_mTheta_for_every_team_and_masses_match_DA_target", ok4)
# 5 sources = first front on 3 real objectives
f3 = rng.rand(40, 3); fr = X.nds(f3); chk("5_sources_index_is_3_objective_first_front", p17.sources_index(f3) == list(fr[0]))
# 10 SELW synthetic
f80 = np.round(rng.rand(80, 3), 1); orig = X.select_next; sel0 = set(orig(np.zeros((80, 1)), f80, 40)); s_const = set(p17.selw_select(f80, np.zeros(80), 40))
chk("10a_SELW_constant_U_selects_same_set_as_original_selection", s_const == sel0)
Ud = rng.rand(80); s_l1 = set(p17.selw_select(f80, Ud, 40, lam=1.0)); chk("10b_SELW_lambda1_follows_U", s_l1 == set(np.argsort(Ud)[:40]))
# 7 SELR independent of genotypes
Ii = P.build("S4-RC101", 11500); selA = p17.make_select17(Ii, PRM, "SELR", orig, [], P.rs("S4-RC101", 11500, "p17_selr")); selB = p17.make_select17(Ii, PRM, "SELR", orig, [], P.rs("S4-RC101", 11500, "p17_selr"))
ff = np.round(rng.rand(80, 3), 2); gA = rnd(80); gB = rnd(80) if False else np.vstack([rnd(40), rnd(40)])
a1 = selA(gA, ff, 40); b1 = selB(gB, ff, 40); a2 = selA(gA, ff, 40)
chk("7a_SELR_selection_independent_of_genotypes_same_stream", a1 == b1)
rr = P.rs("S4-RC101", 11500, "p17_selr").rand(1000); chk("7c_SELR_stream_uniform_0_1", rr.min() >= 0 and rr.max() < 1 and abs(rr.mean() - 0.5) < 0.05)
# runs
sc, seed = "S4-RC101", 11500; I = P.build(sc, seed); W = p17.p9.worlds9(I)
sel4 = timed(lambda: p17.run_arm17(I, "DA+SEL4", PRM, W)); chk("selection_patch_restored_after_run", X.select_next is orig)
chk("6a_budget_exact_6040_SEL4", sel4["n_eval"] == 6040); chk("6b_archive_and_HV_on_3_objectives", np.asarray(sel4["F_search"]).shape[1] == 3 and np.asarray(sel4["F_oracle"]).shape[1] == 3)
chk("9_no_NaN_inf_and_log_has_150_generations", len(sel4["sel_log"]) == 150 and all(d["finite"] for d in sel4["sel_log"]) and all(0 <= d["front4_share"] <= 1 for d in sel4["sel_log"]))
print("   SEL4 diag: front4_share %.3f divergence %.3f S_size %.1f" % (np.mean([d["front4_share"] for d in sel4["sel_log"]]), np.mean([d["divergence"] for d in sel4["sel_log"]]), np.mean([d["S_size"] for d in sel4["sel_log"]])), flush=True)
sel4b = timed(lambda: p17.run_arm17(I, "DA+SEL4", PRM, W)); chk("11_reproducible_run", sel4["D"] == sel4b["D"] and sel4["F_search"] == sel4b["F_search"])
selw = timed(lambda: p17.run_arm17(I, "DA+SELW", PRM, W)); selr = timed(lambda: p17.run_arm17(I, "DA+SELR", PRM, W)); pse = timed(lambda: p17.run_arm17(I, "Dp+SEL4", PRM, W))
chk("6c_budget_exact_all_selection_arms", all(r["n_eval"] == 6040 for r in (selw, selr, pse)) and all(len(r["sel_log"]) == 150 for r in (selw, selr, pse)))
for nm, r in (("SELW", selw), ("SELR", selr), ("Dp+SEL4", pse)): print("   %s diag: front4_share %.3f divergence %.3f" % (nm, np.mean([d["front4_share"] for d in r["sel_log"]]), np.mean([d["divergence"] for d in r["sel_log"]])), flush=True)
# 1 non-regression (baselines) vs P15 and stored P14
I14 = P.build("S4-RC101", 10400); W14 = p17.p9.worlds9(I14); st = json.load(open(B + "/p14/runs/conf/S4-RC101__10400.json"))["conds"]; ok1 = True
for a in ("E", "Dp", "Dg"): r = p17.run_arm17(I14, a, PRM, W14); ok1 &= (r["D"] == st[a]["D"] and r["F_search"] == st[a]["F_search"] and r["hv_oracle"] == st[a]["hv_oracle"])
chk("1a_baselines_E_Dp_Dg_bit_for_bit_vs_P14_stored", ok1)
a15 = p15.run_arm15(I, "DA", PRM, W); a17 = p17.run_arm17(I, "DA", PRM, W); chk("1b_DA_baseline_bit_for_bit_vs_P15_after_selection_runs", a15["D"] == a17["D"] and a15["F_search"] == a17["F_search"])
# 8 no oracle leak
I2 = dict(I); I2["A_true"] = np.random.RandomState(3).rand(*I["A_true"].shape); I2["S_true"] = np.random.RandomState(4).rand(*I["S_true"].shape); ok8 = True
for a, r0 in (("DA+SEL4", sel4), ("Dp+SEL4", pse)): r2 = p17.run_arm17(I2, a, PRM, W); ok8 &= (r2["F_search"] == r0["F_search"] and r2["D"] == r0["D"] and r2["F_oracle"] != r0["F_oracle"])
chk("8_no_oracle_in_search_selection_arms", ok8)
INFO["note"] = "info only: not HV"; json.dump(dict(tests=T, info=INFO), open(B + "/p17/p17_tests_results.json", "w"), indent=1); print("ALL", all(T.values()))
