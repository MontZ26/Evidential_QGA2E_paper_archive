"""P7 gate G1 — instrumented audit of M2 evidence coverage (Amendement P7 v0.3, D7-5, D7-8). Seeds 7000-7009, six scenarios. PRIMARY audit configuration (fixed before running): P5 retained C2c parameters
(N, pc, eta_k, eps, p_LS, k_LS, rule) with V0c, w=0.5. Rule D7-5: M2 retained iff the coverage (median over generations of the share of population individuals carrying >=1 patient with a non-empty
observation set L_i = evaluated 1-shift neighbours NOT dominated by their parent, accepted or rejected [D7-8]; mean over scenarios and seeds) is >= 30%. Sensitivity (descriptive): p_LS = 0.05 and 0.25."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, p7
OUT = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad/p7/p7_g1_results.json"
t = json.load(open(p7.P5DIR + "/p5_tuned.json"))["C2c"]["prm"]; base = dict(N=t["N"], pc=t["pc"], eta_k=t["eta_k"], w=0.5, eps=t["eps"], p_LS=t["p_LS"], k_LS=t["k_LS"], rule=t["rule"])
res = {}
for name, over in (("primary_P5_C2c", {}), ("sens_pLS_0.05", {"p_LS": 0.05}), ("sens_pLS_0.25", {"p_LS": 0.25})):
    prm = dict(base, **over); per_sc = {}
    for sc in p7.SC6:
        cov = []; s1 = s2 = nd = ac = 0; npat = []
        for seed in range(7000, 7010):
            I = p7.P.build(sc, seed)
            if not I["feasible"]: continue
            r = p7.run7(I, "V0c", prm, audit=True); a = r["audit"]; cov.append(float(np.median(a["gen_cov"])) if a["gen_cov"] else 0.0); s1 += a["n1"]; s2 += a["n2"]; nd += a["nd1"]; ac += a["acc1"]; npat += a["pat_with_ev"]
        per_sc[sc] = dict(n_runs=len(cov), median_coverage_mean=float(np.mean(cov)) if cov else None, n_1shift=s1, n_2swap=s2, share_1shift=s1 / max(s1 + s2, 1), share_1shift_nondominated=nd / max(s1, 1), share_1shift_accepted=ac / max(s1, 1),
                          mean_patients_with_evidence_per_flagged_individual=float(np.mean(npat)) if npat else None)
    mc = float(np.mean([v["median_coverage_mean"] for v in per_sc.values() if v["median_coverage_mean"] is not None])); res[name] = dict(prm=prm, mean_coverage_over_scenarios=mc, per_scenario=per_sc)
    print(name, round(mc, 4), flush=True)
res["rule"] = "M2 retained iff primary mean coverage >= 0.30"; res["M2_retained"] = bool(res["primary_P5_C2c"]["mean_coverage_over_scenarios"] >= 0.30)
json.dump(res, open(OUT, "w"), indent=1); print("M2_retained", res["M2_retained"])
