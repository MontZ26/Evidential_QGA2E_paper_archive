"""P16 analysis, HV-BLIND (descriptive). python p16_an.py calib DIR OUT.json | precheck DIR FREEZE | final DIR OUT.json FREEZE THRESHOLDS.json (RUN ONCE). This script reads only ignorance/population/DEC fields of the shards."""
import sys, os, json, glob, math
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"; sys.path.insert(0, B + "/p6/code"); sys.path.insert(0, B + "/p5")
import numpy as np, p6_stats as S, run_p1m as R0
from scipy.stats import spearmanr
ARMS = ["DA", "DA+S", "DA+L", "DA+P11"]; SC = S.SC; GENS = [1, 25, 50, 100, 150]
KEYS = ["m_theta", "m_theta_E", "dm", "m_empty", "m_empty_E", "dep", "neff", "frac_dup", "q_max", "q_ent"]
SC3 = ["S4-RC101", "S4-R101", "S4-C101"]
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=str); os.replace(tmp, p)
def load_dir(d):
    out = {}
    for f in sorted(glob.glob(d + "/*__*.json")): r = json.load(open(f)); out[f"{r['sc']}|{r['seed']}"] = r
    return out
def series(run, arm, k): return np.array([run["conds"][arm]["dyn"][g][k] for g in range(1, 151)], float)
def calib(d, out):
    assert not os.path.exists(out), "RUN ONCE"; res = load_dir(d); bad = []
    if sorted({r["seed"] for r in res.values()}) != list(range(11100, 11115)) or len(res) != 45: bad.append("shape")
    med_m, med_d, neg = [], [], 0
    for k, r in res.items():
        if not r.get("feasible", False): bad.append("infeasible " + k); continue
        m = series(r, "DA", "m_theta"); dm = series(r, "DA", "dm"); neg += int((dm < -1e-12).sum()); med_m.append(float(np.median(m))); med_d.append(float(np.median(dm)))
    assert not bad, bad
    th = dict(tau=float(np.median(med_m)), tau_dm=float(np.median(med_d)), n_runs=len(med_m), per_run_median_m_theta=dict(min=min(med_m), max=max(med_m)), per_run_median_dm=dict(min=min(med_d), max=max(med_d)), n_negative_dm=neg,
              rule="median over generations 1-150 per run, then median over the 45 runs (SC3 x 11100-11114), DA without DEC; HV not read")
    save(th, out); print(json.dumps(th, indent=1))
def precheck(d, freeze):
    bad = []
    if not R0.verify_freeze(freeze): bad.append("freeze")
    res = load_dir(d); seeds = sorted({r["seed"] for r in res.values()})
    if seeds != list(range(11000, 11030)): bad.append(f"seeds {len(seeds)}")
    if len(res) != 180: bad.append(f"{len(res)} shards")
    for k, r in res.items():
        if not r.get("feasible", False): bad.append(f"infeasible {k}"); continue
        for a in ARMS:
            c = r.get("conds", {}).get(a)
            if c is None or c["n_eval"] != 6040: bad.append(f"{k} {a}")
    print("PRECHECK", "OK" if not bad else bad[:10]); return not bad
def boot(dd, idx): return dd[idx].mean(1)
def final(d, out, freeze, thf):
    assert not os.path.exists(out), "RUN ONCE"; assert precheck(d, freeze); res = load_dir(d); th = json.load(open(thf)); seeds = sorted({r["seed"] for r in res.values()}); n = len(seeds)
    X = {a: {k: np.array([np.mean([series(res[f"{sc}|{s}"], a, k) for sc in SC], axis=0) for s in seeds]) for k in KEYS} for a in ARMS}       # [n_seeds,150] mean over the six scenarios per seed
    rng = S.sub_rng("p16phaseD", 11990); idx = rng.randint(0, n, size=(20000, n)).astype(np.int32)
    rep = dict(status="PHASE D, DESCRIPTIVE, HV-BLIND (HV fields never read)", n_seeds=n, thresholds=th, arm_means={a: {k: {str(g): float(X[a][k][:, g - 1].mean()) for g in GENS} for k in KEYS} for a in ARMS}, contrasts={}, per_scenario_m_theta={})
    for a, b in [("DA+L", "DA"), ("DA+S", "DA"), ("DA+P11", "DA")]:
        c = {}
        for k in KEYS:
            dd = X[a][k] - X[b][k]; bm = np.stack([boot(dd[:, g - 1], idx) for g in GENS], 1)
            c[k] = {str(g): dict(mean=float(dd[:, g - 1].mean()), ci95=[float(np.percentile(bm[:, i], 2.5)), float(np.percentile(bm[:, i], 97.5))]) for i, g in enumerate(GENS)}
        full = X[a]["m_theta"] - X[b]["m_theta"]; c["m_theta_full_trajectory_mean"] = [float(v) for v in full.mean(0)]; fb = np.stack([boot(full[:, j], idx) for j in range(150)], 1)
        c["m_theta_full_trajectory_ci95_lo"] = [float(v) for v in np.percentile(fb, 2.5, axis=0)]; c["m_theta_full_trajectory_ci95_hi"] = [float(v) for v in np.percentile(fb, 97.5, axis=0)]; rep["contrasts"][f"{a}-{b}"] = c
        rep["per_scenario_m_theta"][f"{a}-{b}"] = {sc: {str(g): float(np.mean([series(res[f"{sc}|{s}"], a, "m_theta")[g - 1] - series(res[f"{sc}|{s}"], b, "m_theta")[g - 1] for s in seeds])) for g in GENS} for sc in SC}
    cm = rep["contrasts"]["DA+L-DA"]["m_theta"]; ub = {g: cm[str(g)]["ci95"][1] for g in (50, 100, 150)}
    rep["decision_rule"] = dict(premise="DEC strong (L) reduces mean ignorance of DA", upper_bounds_ci95_gen_50_100_150=ub, supported=bool(all(v < 0 for v in ub.values())), rule_text="supported iff the upper bound of the 95% CI of m(Theta)[DA+L]-m(Theta)[DA] is < 0 at generations 50, 100 and 150 simultaneously")
    # actual DEC intervention per arm (cumulative counters are 'before loop-generation j' for dyn gen j+1; final snapshot closes the run)
    dec = {}
    for a in ARMS[1:]:
        rows = []
        for sc in SC:
            for s in seeds:
                c = res[f"{sc}|{s}"]["conds"][a]; snaps = [c["dyn"][g]["dec_c"] for g in range(1, 151)] + [c["dec_final"]]; rows.append(snaps)
        def tot(i, k): return float(np.mean([r[i][k] for r in rows]))
        dd = dict(init_cleaning_counts={k: tot(0, k) for k in rows[0][0]})
        for nm, (i0, i1) in {"gen1-50": (0, 50), "gen51-100": (50, 100), "gen101-150": (100, 150)}.items():
            inc = {k: tot(i1, k) - tot(i0, k) for k in rows[0][0]}; inc["share_candidates_repaired"] = inc["cands_repaired"] / max(inc["cands"], 1e-12); inc["violation_per_candidate"] = inc["violations"] / max(inc["cands"], 1e-12); dd[nm] = inc
        dec[a] = dd
    rep["dec_effective_intervention"] = dec
    # passive R1 / R2 signals (no action): decisions from thresholds, per arm
    pas = {}
    for a in ARMS:
        m = np.array([series(res[f"{sc}|{s}"], a, "m_theta") for sc in SC for s in seeds]); dm = np.array([series(res[f"{sc}|{s}"], a, "dm") for sc in SC for s in seeds])
        r1 = m >= th["tau"]; r2 = dm >= th["tau_dm"]
        pas[a] = dict(share_L_R1=float(r1.mean()), share_L_R2=float(r2.mean()), share_generations_decisions_differ=float((r1 != r2).mean()), spearman_signals_pooled=float(spearmanr(m.ravel(), dm.ravel())[0]), n_dm_negative=int((dm < -1e-12).sum()))
    rep["passive_R1_R2"] = pas; save(rep, out); print(json.dumps(rep, indent=1, default=str))
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "calib": calib(sys.argv[2], sys.argv[3])
    elif m == "precheck": sys.exit(0 if precheck(sys.argv[2], sys.argv[3]) else 1)
    elif m == "final": final(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
