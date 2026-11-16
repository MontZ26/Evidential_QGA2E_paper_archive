"""Technical test of the P6 statistics on synthetic data (protocol 10): Lambda/Gamma/Holm, bootstrap-t vs independent implementation, null rejection rate, Holm, edge cases. Output JSON."""
import sys, json, time, math
import numpy as np
sys.path.insert(0, "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p6/code")
import p6_stats as S
out = {}; rng = np.random.RandomState(1)
# 1. factorial contrasts on a known additive+interaction structure
n = 50; H = {}
cell = lambda m, s, l: (0.50 + (0.05 if m == "C2" else 0) + (0.02 if s == "T" else 0) + (0.03 if l == "on" else 0) + (0.04 if (m == "C2" and l == "on") else 0) + (0.01 if (m == "C2" and s == "T" and l == "on") else 0))
for m in ("C2", "C3"):
    for l in ("on", "off"):
        for s in ("T", "R"): H[f"{m}-{s}-{l}"] = np.full(n, cell(m, s, l)) + rng.normal(0, 0.001, n)
H["C0b-T"] = np.full(n, 0.60) + rng.normal(0, 0.001, n); se = S.series(H)
out["contrast_means"] = {k: float(v.mean()) for k, v in se.items()}
exp = dict(H61=0.04 + 0.005 * 0, H65=0.01, H62=0.25 * (0.02 * 4 + 0.01), H66=cell("C2", "T", "on") - 0.60)
# Lambda = [HV(C2,on)-HV(C3,on)]-[HV(C2,off)-HV(C3,off)] ; D(C2,on)=0.03, D(others)=0.02 => Gamma = 0.01
out["expected"] = dict(H6_1=0.04 + 0.005, H6_5=0.01, H6_2=0.2275 * 0 + 0.0225, H6_6=exp["H66"])
ok1 = abs(se["H6.1"].mean() - 0.045) < 1e-3 and abs(se["H6.5"].mean() - 0.01) < 1e-3 and abs(se["H6.2"].mean() - 0.0225) < 1e-3 and abs(se["H6.3"].mean() - 0.005) < 1e-3 and abs(se["H6.4"].mean() - 0.005) < 1e-3 and abs(se["H6.6"].mean() - (cell("C2", "T", "on") - 0.60)) < 1e-3
out["contrasts_ok"] = bool(ok1)
# 2. bootstrap-t vs independent implementation on the same index matrix (B small for the slow loop, B_rule bypassed with B=600 both)
d = rng.normal(0.01, 0.03, 40); B = 600; idx = rng.randint(0, len(d), (B, len(d))).astype(np.int32)
p1, info = S.boot_t(d, None, B, idx=idx); p2 = S.boot_t_reference(list(d), idx, B); out["boot_vs_reference"] = dict(p_fast=p1, p_ref=p2, equal=bool(abs(p1 - p2) < 1e-12))
# 3. edge cases
out["sd_zero_mean_zero"] = S.boot_t(np.zeros(30), None)[0]; out["sd_zero_mean_nonzero"] = S.boot_t(np.full(30, 0.01), None)[0]; out["expected_sd0"] = 1 / 20001
dd = np.zeros(100); dd[0] = 1.0; p, info = S.boot_t(dd, S.sub_rng("edge")); out["mostly_constant"] = dict(p=p, info=info)   # resamples without the outlier are constant -> excluded; Bv/B<0.99 -> p=1
# 4. Holm
ps = [0.001, 0.04, 0.01, 0.2, 0.012]; adj = S.holm(ps); out["holm"] = dict(p=ps, adj=adj); exp_adj = [0.005, 0.08, 0.04, 0.2, 0.04]
out["holm_ok"] = bool(np.allclose(adj, exp_adj))
# 5. null rejection rate (alpha 0.05) and power vs normal theory, modest sims with B=2000
rr = np.random.RandomState(5); rej0 = 0; rej1 = 0; ns = 300; t0 = time.time()
for _ in range(ns):
    x = rr.normal(0, 0.03, 60); rej0 += S.boot_t(x, rr, 2000)[0] < 0.05
    x = rr.normal(0.02, 0.03, 60); rej1 += S.boot_t(x, rr, 2000)[0] < 0.05
out["null_reject_rate"] = rej0 / ns; out["power_effect_0.02_sd0.03_n60"] = rej1 / ns; out["normal_theory_power"] = 0.915   # approx: z=0.02/(0.03/sqrt60)=5.16 -> ~1.0
# 6. timing of the confirmatory test at n=300, B=20000
x = rr.normal(0, 0.03, 300); t0 = time.time(); S.boot_t(x, rr, 20000); out["time_boot_t_n300_B20000_s"] = time.time() - t0
x = rr.normal(0, 0.03, 100); t0 = time.time(); S.boot_t(x, rr, 20000); out["time_boot_t_n100_B20000_s"] = time.time() - t0
out["all_ok"] = bool(ok1 and out["boot_vs_reference"]["equal"] and abs(out["sd_zero_mean_nonzero"] - out["expected_sd0"]) < 1e-12 and out["sd_zero_mean_zero"] == 1.0 and out["mostly_constant"]["p"] == 1.0 and out["holm_ok"] and 0.02 < out["null_reject_rate"] < 0.09)
json.dump(out, open("/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p6/p6_tests_stats.json", "w"), indent=1, default=float); print(json.dumps(out, indent=1, default=float))
