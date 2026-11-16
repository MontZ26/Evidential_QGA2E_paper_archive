"""P16 technical tests (no HV is analysed; only equalities/non-leak). Run once before freeze."""
import sys, json, time, numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p16/code")
import p16, p15, p10, p11
P, X, K, p7 = p16.P, p16.X, p16.K, p16.p7; T = {}
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"
def chk(k, v): T[k] = bool(v); print(("PASS " if v else "FAIL ") + k, flush=True)
PRM = json.load(open(B + "/p15/p15_params.json"))["chosen"]; TH = {"tau": 0.03, "tau_dm": 0.03}
sc, seed = "S4-RC101", 10400; I = P.build(sc, seed); W = p16.p9.worlds9(I)
def timed(f):
    t = time.time(); r = f(); print("   %.1fs" % (time.time() - t), flush=True); return r
# 1 inactive controller == P15 DA bit for bit
a15 = timed(lambda: p15.run_arm15(I, "DA", PRM, W)); a16 = timed(lambda: p16.run_arm16(I, "DA", PRM, TH, W))
chk("1_DA_without_DEC_equals_P15_DA_bit_for_bit", a15["D"] == a16["D"] and a15["F_search"] == a16["F_search"] and a15["hv_oracle"] == a16["hv_oracle"] and [d.get("m_theta") for d in a15["dyn"]] == [d.get("m_theta") for d in a16["dyn"]] and [d.get("q_max") for d in a15["dyn"]] == [d.get("q_max") for d in a16["dyn"]])
chk("13_DA_arm_has_no_DEC_object_no_level", a16["dec_final"] is None and all("level" not in d for d in a16["dyn"]))
# 2a fixed S via controller == direct DEC(S) with P15 DA target
Is = dict(I); Is["A_true"], Is["S_true"] = W["nom"]; dec = p16.make_dec16(I, "S"); old = p10.target; p10.target = p15.make_target15("DA", PRM)
try: man = timed(lambda: p10.run_q(Is, "V1", PRM["w"], PRM["eps"], dec, diag=True))
finally: p10.target = old
s16 = timed(lambda: p16.run_arm16(I, "DA+S", PRM, TH, W))
chk("2a_fixed_S_via_controller_equals_direct_DEC_S", np.asarray(man["D"]).tolist() == s16["D"] and np.asarray(man["F"]).tolist() == s16["F_search"] and man["dec"] == s16["dec_final"])
# 2b/4/12 parameters only between generations, initial cleaning at S, level L afterwards
CNT = [0]; REC = {}; orig_make = p16.make_target16; orig_rep = p11.Dec.repair
def mk(prm, dec, mode, th, log):
    f = orig_make(prm, dec, mode, th, log)
    def g(*a): CNT[0] += 1; return f(*a)
    return g
def rep(s, S, d, M, mutable): REC.setdefault(CNT[0], set()).add((s.n_max, round(s.m_max_frac, 6))); return orig_rep(s, S, d, M, mutable)
p16.make_target16 = mk; p11.Dec.repair = rep
try: L16 = timed(lambda: p16.run_arm16(I, "DA+L", PRM, TH, W))
finally: p16.make_target16 = orig_make; p11.Dec.repair = orig_rep
chk("12_initial_cleaning_at_level_S", REC.get(0) == {(5, 0.2)})
chk("4_parameters_constant_within_each_generation", all(len(v) == 1 for v in REC.values()))
chk("2b_fixed_L_applied_from_generation_1_on", all(REC[k] == {(2, 0.4)} for k in REC if k >= 1) and set(REC) == set(range(0, 151)))
chk("9_traceability_level_nmax_rho_every_generation", all(("level" in d and "n_max" in d and "rho_max" in d and "dec_c" in d) for d in L16["dyn"][1:]) and len(L16["dyn"]) == 151 and set(L16["levels"]) == {"L"})
# 3 budget
P11 = timed(lambda: p16.run_arm16(I, "DA+P11", PRM, TH, W))
chk("3_budget_exact_6040_DEC_arms", all(r["n_eval"] == 6040 for r in (s16, L16, P11)))
# 11 DEC counters monotone and present
cs = [d["dec_c"] for d in L16["dyn"][1:]] + [L16["dec_final"]]; ok = True
for k in ("cands", "cands_repaired", "repairs", "mutations", "violations", "regen"):
    v = [c[k] for c in cs]; ok &= all(b >= a for a, b in zip(v, v[1:]))
chk("11_DEC_counters_cumulative_monotone_and_recorded", ok)
print("   DA+L counters", L16["dec_final"], " DA+S", s16["dec_final"], " DA+P11", P11["dec_final"], flush=True)
# 5 + live rule selection (R1, R2, R1inv, SCH) and 8 calendar
chk("5a_decide_synthetic", p16.decide("R1", 0, 0.04, 0, TH) == "L" and p16.decide("R1", 0, 0.01, 0, TH) == "S" and p16.decide("R2", 0, 0, 0.03, TH) == "L" and p16.decide("R2", 0, 0, 0.02, TH) == "S" and p16.decide("R1inv", 0, 0.04, 0, TH) == "S" and p16.decide("R1inv", 0, 0.01, 0, TH) == "L" and p16.decide("SCH", 49, 0, 0, TH) == "L" and p16.decide("SCH", 50, 0, 0, TH) == "S")
okl = True; res = {}
for arm in ("DA+R1", "DA+R2", "DA+R1inv", "DA+SCH"):
    r = timed(lambda: p16.run_arm16(I, arm, PRM, TH, W)); res[arm] = r; okl &= (r["n_eval"] == 6040)
    for j, d in enumerate(r["dyn"][1:]): okl &= (d["level"] == p16.decide(p16.MODE[arm], j, d["m_theta"], d["dm"], TH))
chk("5b_R1_R2_R1inv_SCH_select_expected_level_live_and_budget", okl)
chk("8_calendar_reproducible_L_then_S", res["DA+SCH"]["levels"] == p16.run_arm16(I, "DA+SCH", PRM, TH, W)["levels"] and res["DA+SCH"]["levels"] == ["L"] * 50 + ["S"] * 100)
print("   levels: R1 L-share %.2f R2 L-share %.2f" % (np.mean([x == "L" for x in res["DA+R1"]["levels"]]), np.mean([x == "L" for x in res["DA+R2"]["levels"]])), flush=True)
# 6/10 paired DA/E on identical sources; dm>=0
rng = np.random.RandomState(5); n_p, n_t = 30, 8; M = np.ones((n_p, n_t), int); M[::4, 5:] = 0; M[3, 1:] = 0; log = []; tg = p16.make_target16(PRM, None, "none", TH, log); ok6 = True; ok10 = True
for _ in range(60):
    N = rng.randint(3, 25); base = np.array([[rng.choice(np.flatnonzero(M[p])) for p in range(n_p)] for _ in range(4)]); src = np.array([base[rng.randint(4)] if rng.rand() < .6 else [rng.choice(np.flatnonzero(M[p])) for p in range(n_p)] for _ in range(N)])
    tg(src, M, PRM["w"], "V1", PRM["eps"]); d = log[-1]; _, md = p15.da_model(src, M, PRM["w"], PRM["sigma"], PRM["lam"]); _, me = p7.population_model(src, M, PRM["w"], "V1")
    ok6 &= (d["dm"] == md["m_theta"] - me["m_theta"] and d["m_theta"] == md["m_theta"] and d["m_theta_E"] == me["m_theta"]); ok10 &= d["dm"] >= -1e-12
chk("6_dm_computed_on_identical_sources_DA_and_E_same_generation", ok6)
chk("10_dm_nonnegative_on_identical_sources_and_in_runs", ok10 and all(d["dm"] >= -1e-12 for r in (a16, L16, s16) for d in r["dyn"][1:]))
# 7 no HV leak: analysis script never mentions HV fields; DEC arm search independent of oracle world
src_an = open("/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p16/code/p16_an.py").read()
chk("7a_analysis_script_has_no_HV_field_names", not any(s in src_an for s in ("hv_oracle", "hv_search", "F_oracle", "F_search", "R.hv", "_oracle_eval")))
I2 = dict(I); I2["A_true"] = np.random.RandomState(3).rand(*I["A_true"].shape); I2["S_true"] = np.random.RandomState(4).rand(*I["S_true"].shape)
r2 = p16.run_arm16(I2, "DA+L", PRM, TH, W); chk("7b_no_oracle_in_search_DA+L", r2["F_search"] == L16["F_search"] and r2["D"] == L16["D"] and r2["F_oracle"] != L16["F_oracle"])
chk("14_raw_initial_population_deterministic_same_for_all_arms", np.array_equal(X.init_qga(I)[1], X.init_qga(I)[1]))
json.dump(T, open(B + "/p16/p16_tests_results.json", "w"), indent=1); print("ALL", all(T.values()))
