"""P24 pre-registered analysis. python p24_an.py precheck DIR FREEZE | final DIR OUT.json FREEZE (RUN ONCE; HV read only here, and in precheck only for bitwise equality with stored P23 HV, printing booleans)."""
import sys, os, json, glob
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"; sys.path.insert(0, B + "/p6/code"); sys.path.insert(0, B + "/p5")
import numpy as np, p6_stats as S, run_p1m as R0
from scipy.stats import spearmanr
SC = S.SC; DELTA = 0.005
PRM = json.load(open(B + "/p24/p24_params.json")); ARMS = PRM["arms"]; ROLES = PRM["roles"]
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=str); os.replace(tmp, p)
def load_dir(d): return {f"{r['sc']}|{r['seed']}": r for r in (json.load(open(f)) for f in sorted(glob.glob(d + "/*__*.json")))}
def p23_runs(): return load_dir(B + "/p23/runs/main")
def precheck(d, freeze):
    bad = []
    if not R0.verify_freeze(freeze): bad.append("freeze")
    res = load_dir(d)
    if sorted({r["seed"] for r in res.values()}) != list(range(12000, 12100)) or len(res) != 600: bad.append(f"shape {len(res)}")
    old = p23_runs(); eqDA = eqDg = True
    for k, r in res.items():
        if not r.get("feasible"): bad.append(f"{k} infeasible"); continue
        if not os.path.exists(d + "/" + k.replace("|", "__") + ".npz"): bad.append(f"{k} npz")
        for a in ARMS:
            c = r.get("conds", {}).get(a)
            if c is None or c["n_eval"] != 6040: bad.append(f"{k} {a}")
        try:
            eqDA &= r["conds"][ROLES["DA_w0.3"]]["hv_oracle"] == old[k]["conds"]["DA100"]["hv_oracle"]; eqDg &= r["conds"][ROLES["Dg6_w0.3"]]["hv_oracle"] == old[k]["conds"]["Dg100"]["hv_oracle"]
        except Exception as e: bad.append(f"{k} rerun check {e}")
    if not eqDA: bad.append("rerun DA(1) differs from P23")
    if not eqDg: bad.append("rerun Dg(6) differs from P23")
    print("PRECHECK", "OK" if not bad else bad[:10], "| rerun DA(1)==P23:", eqDA, "| rerun Dg(6)==P23:", eqDg); return not bad
def cls(lo, hi):
    if lo > 0: return "superiority"
    if hi < 0: return "inferiority"
    if lo > -DELTA and hi < DELTA: return "equivalence"
    return "inconclusive"
def pos(lo, hi): return "pos" if lo > 0 else ("neg" if hi < 0 else "zero")
def sgn(x): return 1 if x > 0 else (-1 if x < 0 else 0)
def js_l1(fa, fb, M):
    mut = M.sum(1) >= 2; fa = fa[mut] / 40.0; fb = fb[mut] / 40.0; l1 = np.abs(fa - fb).sum(1); m = (fa + fb) / 2
    def kl(p, q): return np.where(p > 0, p * np.log2(np.where(p > 0, p, 1.0) / np.where(q > 0, q, 1.0)), 0.0).sum(1)
    return float(l1.mean()), float((0.5 * kl(fa, m) + 0.5 * kl(fb, m)).mean())
def final(d, out, freeze):
    assert not os.path.exists(out), "RUN ONCE"; assert precheck(d, freeze); res = load_dir(d); old = p23_runs(); seeds = sorted({r["seed"] for r in res.values()}); n = len(seeds)
    ref23 = json.load(open(B + "/p23/p23_final_analysis.json"))["primary"]; refDg = ref23["C3 DA100-Dg100"]; refE = ref23["C4 DA100-E"]
    src = {a: {sc: np.array([res[f"{sc}|{s}"]["conds"][a]["hv_oracle"] for s in seeds]) for sc in SC} for a in ARMS}
    srcE30 = {sc: np.array([old[f"{sc}|{s}"]["conds"]["E"]["hv_oracle"] for s in seeds]) for sc in SC}; src["E_w0.3"] = srcE30
    H = {a: np.mean([src[a][sc] for sc in SC], axis=0) for a in src}
    idx = S.sub_rng("p24_final", 13993).randint(0, n, size=(20000, n)).astype(np.int32)
    def ci(dd, a2): bm = dd[idx].mean(1); return float(np.percentile(bm, a2 / 2)), float(np.percentile(bm, 100 - a2 / 2))
    R = ROLES; C = []   # (name, a, b, family, reference)
    for w in (0.15, 0.5, 0.7):
        C.append(("DA-Dg w=%g" % w, R["DA_w%g" % w], R["Dg_w%g" % w], "w", "Dg")); C.append(("DA-E w=%g" % w, R["DA_w%g" % w], R["E_w%g" % w], "w", "E"))
    for s in (0.6, 0.8):
        C.append(("DA-Dg sigma=%g" % s, R["DA_s%g" % s], R["Dg_s%g" % s], "sigma", "Dg")); C.append(("DA-E sigma=%g" % s, R["DA_s%g" % s], "E_w0.3", "sigma", "E"))
    C.append(("DA-Dg8 w=0.3", R["DA_w0.3"], R["Dg8"], "gamma", "Dg")); C.append(("DA-Dg12 w=0.3", R["DA_w0.3"], R["Dg12"], "gamma", "Dg"))
    EDP = [("E-Dp w=%g" % w, "E_w0.3" if w == 0.3 else R["E_w%g" % w], R["Dp_w%g" % w], "EDp", None) for w in (0.15, 0.3, 0.5, 0.7)]
    assert len(C) == 12 and len(EDP) == 4
    kfam = {"w": 6, "sigma": 4, "gamma": 2, "EDp": 4}
    rep = dict(status="PRE-REGISTERED P24 v0.2 (16 contrasts, 99% marginal CI, margin 0.005)", n_seeds=n, params=dict(gamma_w=PRM["gamma_w"], gamma_sigma=PRM["gamma_sigma"], gamma_cal_baseline=PRM["gamma_cal_baseline"], gate_calibration=PRM["gate_satisfied"], roles=ROLES), hv_oracle_means={a: float(H[a].mean()) for a in H}, hv_oracle_sd={a: float(H[a].std(ddof=1)) for a in H}, contrasts={}, secondary={}, reference_P23=dict(Dg=refDg, E=refE))
    for (nm, a, b, fam, ref) in C + EDP:
        dd = H[a] - H[b]; lo, hi = ci(dd, 1.0); blo, bhi = ci(dd, 1.0 / kfam[fam]); r = dict(a=a, b=b, family=fam, mean=float(dd.mean()), sd=float(dd.std(ddof=1)), ci99=[lo, hi], decision=cls(lo, hi), ci_bonferroni=[blo, bhi], decision_bonferroni=cls(blo, bhi), share_pos=float((dd > 0).mean()))
        if ref is not None:
            rf = refDg if ref == "Dg" else refE; rlo, rhi = rf["ci99"]
            r["ref_P23"] = dict(mean=rf["mean"], ci99=rf["ci99"], decision=rf["decision"])
            dir_ok = bool(sgn(r["mean"]) == sgn(rf["mean"]) and pos(lo, hi) == pos(rlo, rhi)); cls_ok = bool(r["decision"] == rf["decision"]); amp_ok = bool(abs(r["mean"] - rf["mean"]) <= DELTA)
            if dir_ok and cls_ok and amp_ok: v = "maintenu"
            elif dir_ok: v = "partiellement maintenu"
            elif sgn(r["mean"]) == sgn(rf["mean"]) and amp_ok: v = "partiellement maintenu"
            else: v = "modifie"
            r["robustness"] = dict(direction=dir_ok, practical_class=cls_ok, amplitude=amp_ok, verdict=v)
        rep["contrasts"][nm] = r
        rep["secondary"][nm] = dict(per_scenario={sc: float((src[a][sc] - src[b][sc]).mean()) for sc in SC}, by_type={t: dict(mean=float(np.mean([(src[a][sc] - src[b][sc]) for sc in SC if sc.endswith(t)], axis=0).mean()), ci95=list(ci(np.mean([(src[a][sc] - src[b][sc]) for sc in SC if sc.endswith(t)], axis=0), 5.0))) for t in ("RC101", "R101", "C101")})
    # setting differences (paired) vs baseline contrasts
    Hb = H[R["DA_w0.3"]] - H[R["Dg6_w0.3"]]; HbE = H[R["DA_w0.3"]] - H["E_w0.3"]; sd_ = {}
    for (nm, a, b, fam, ref) in C:
        base = Hb if ref == "Dg" else HbE; dd = (H[a] - H[b]) - base; lo, hi = ci(dd, 5.0); sd_[nm + " minus baseline(w=0.3,s=0.7,g=6)"] = dict(mean=float(dd.mean()), ci95=[lo, hi])
    rep["secondary"]["setting_differences_vs_baseline"] = sd_
    # matching verification on SC6 (mean over generations 1-150 and runs), descriptive gens 1 and 150
    def mser(a, key): return float(np.mean([x[key] for r in res.values() for x in r["conds"][a]["dyn"] if "q_ent" in x]))
    def at(a, key, g): return float(np.mean([r["conds"][a]["dyn"][g][key] for r in res.values()]))
    pairs = {"w=0.15": ("DA_w0.15", "Dg_w0.15"), "w=0.5": ("DA_w0.5", "Dg_w0.5"), "w=0.7": ("DA_w0.7", "Dg_w0.7"), "sigma=0.6": ("DA_s0.6", "Dg_s0.6"), "sigma=0.8": ("DA_s0.8", "Dg_s0.8"), "baseline Dg6": ("DA_w0.3", "Dg6_w0.3"), "Dg8": ("DA_w0.3", "Dg8"), "Dg12": ("DA_w0.3", "Dg12"), "Dgcal (supplementary)": ("DA_w0.3", "Dgcal")}
    mt = {}
    for k, (ra, rb) in pairs.items():
        a, b = R[ra], R[rb]; Hr, Ho, Qr, Qo = mser(a, "q_ent"), mser(b, "q_ent"), mser(a, "q_max"), mser(b, "q_max"); gap = abs(Ho - Hr) / Hr; qg = abs(Qo - Qr)
        mt[k] = dict(ref=a, other=b, entropy_ref=Hr, entropy_other=Ho, rel_entropy_gap=gap, qmax_ref=Qr, qmax_other=Qo, abs_qmax_gap=qg, conform=bool(gap <= 0.10 and qg <= 0.05), gen1=dict(qmax_ref=at(a, "q_max", 1), qmax_other=at(b, "q_max", 1), ent_ref=at(a, "q_ent", 1), ent_other=at(b, "q_ent", 1)), gen150=dict(qmax_ref=at(a, "q_max", 150), qmax_other=at(b, "q_max", 150), ent_ref=at(a, "q_ent", 150), ent_other=at(b, "q_ent", 150)))
    rep["matching_SC6"] = mt
    # effective distribution: logged means per arm; per-patient L1 and JS between arms
    gens = (1, 25, 50, 100, 150); ek = ("ang_max_raw", "ang_max_norm", "dec_max", "dec_ent", "L1_dec_target", "q_max")
    rep["effective_distribution"] = {a: {k: {str(g): float(np.mean([x[k] for r in res.values() for x in r["conds"][a]["log"] if x["gen"] == g])) for g in gens} for k in ek} for a in ARMS}
    dpairs = {"DA-Dg w=%g" % w: (R["DA_w%g" % w], R["Dg_w%g" % w]) for w in (0.15, 0.5, 0.7)}; dpairs["DA-Dg baseline Dg6"] = (R["DA_w0.3"], R["Dg6_w0.3"])
    for s in (0.6, 0.8): dpairs["DA-Dg sigma=%g" % s] = (R["DA_s%g" % s], R["Dg_s%g" % s])
    dpairs["DA-Dg8"] = (R["DA_w0.3"], R["Dg8"]); dpairs["DA-Dg12"] = (R["DA_w0.3"], R["Dg12"])
    for w in (0.15, 0.5, 0.7): dpairs["DA-E w=%g" % w] = (R["DA_w%g" % w], R["E_w%g" % w]); dpairs["E-Dp w=%g" % w] = (R["E_w%g" % w], R["Dp_w%g" % w])
    dist = {k: {sc: {str(g): {"L1": [], "JS": []} for g in gens} for sc in SC} for k in dpairs}
    for s in seeds:
        for sc in SC:
            z = np.load(d + f"/{sc}__{s}.npz"); M = z["M"]
            for k, (a, b) in dpairs.items():
                for g in gens: l1, js = js_l1(z[f"{a}|{g}"], z[f"{b}|{g}"], M); dist[k][sc][str(g)]["L1"].append(l1); dist[k][sc][str(g)]["JS"].append(js)
    ed = {}
    for k, (a, b) in dpairs.items():
        ed[k] = dict(per_scenario={sc: {g: dict(L1=float(np.mean(v["L1"])), JS=float(np.mean(v["JS"]))) for g, v in dist[k][sc].items()} for sc in SC}, global_mean_over_scenarios={g: dict(L1=float(np.mean([np.mean(dist[k][sc][g]["L1"]) for sc in SC])), JS=float(np.mean([np.mean(dist[k][sc][g]["JS"]) for sc in SC]))) for g in map(str, gens)},
                     spearman_JS150_vs_HVgap={sc: (lambda r: dict(rho=float(r[0]), p=float(r[1])))(spearmanr(dist[k][sc]["150"]["JS"], src[a][sc] - src[b][sc])) for sc in SC})
    rep["effective_distance"] = ed; rep["note_effective_distance"] = "E_w0.3 has no per-patient log (stored P23 run): pairs with E at w=0.3 are not available."
    save(rep, out); print(json.dumps(dict(contrasts=rep["contrasts"], matching=mt), indent=1, default=str)[:12000])
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "precheck": sys.exit(0 if precheck(sys.argv[2], sys.argv[3]) else 1)
    elif m == "final": final(sys.argv[2], sys.argv[3], sys.argv[4])
