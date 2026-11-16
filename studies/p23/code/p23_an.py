"""P23 pre-registered analysis. python p23_an.py precheck DIR FREEZE | final DIR OUT.json FREEZE (RUN ONCE; HV read only here)."""
import sys, os, json, glob
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"; sys.path.insert(0, B + "/p6/code"); sys.path.insert(0, B + "/p5")
import numpy as np, p6_stats as S, run_p1m as R0
SC = S.SC; DELTA = 0.005; ARMS = ["E", "DA25", "DA50", "DA100", "Dg25", "Dg50", "Dg100", "RHO", "MIX"]
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=str); os.replace(tmp, p)
def load_dir(d): return {f"{r['sc']}|{r['seed']}": r for r in (json.load(open(f)) for f in sorted(glob.glob(d + "/*__*.json")))}
def precheck(d, freeze):
    bad = []
    if not R0.verify_freeze(freeze): bad.append("freeze")
    res = load_dir(d)
    if sorted({r["seed"] for r in res.values()}) != list(range(12000, 12100)) or len(res) != 600: bad.append(f"shape {len(res)}")
    for k, r in res.items():
        if not r.get("feasible"): bad.append(f"{k} infeasible"); continue
        for a in ARMS:
            c = r.get("conds", {}).get(a)
            if c is None or c["n_eval"] != 6040: bad.append(f"{k} {a}")
    print("PRECHECK", "OK" if not bad else bad[:10]); return not bad
def cls(lo, hi):
    if lo > 0: return "superiority"
    if hi < 0: return "inferiority"
    if lo > -DELTA and hi < DELTA: return "equivalence"
    return "inconclusive"
def final(d, out, freeze):
    assert not os.path.exists(out), "RUN ONCE"; assert precheck(d, freeze); res = load_dir(d); seeds = sorted({r["seed"] for r in res.values()}); n = len(seeds); PRM = json.load(open(B + "/p23/p23_params.json"))
    src = {a: {sc: np.array([res[f"{sc}|{s}"]["conds"][a]["hv_oracle"] for s in seeds]) for sc in SC} for a in ARMS}; H = {a: np.mean([src[a][sc] for sc in SC], axis=0) for a in ARMS}
    idx = S.sub_rng("p23_final", 12993).randint(0, n, size=(20000, n)).astype(np.int32)
    prim = {"C1 DA25-Dg25": ("DA25", "Dg25"), "C2 DA50-Dg50": ("DA50", "Dg50"), "C3 DA100-Dg100": ("DA100", "Dg100"), "C4 DA100-E": ("DA100", "E")}
    rep = dict(status="PRE-REGISTERED P23 v1.0 (4 primaries, 99% CI, margin 0.005)", n_seeds=n, params=dict(gamma=PRM["gamma"], rho0=PRM["rho0"], gmix=PRM["gmix"], gate_satisfied_calibration=PRM["gate_satisfied"]), hv_oracle_means={a: float(H[a].mean()) for a in ARMS}, hv_oracle_sd={a: float(H[a].std(ddof=1)) for a in ARMS}, primary={}, exploratory={}, per_scenario={})
    def ci(dd, lo_p, hi_p): bm = dd[idx].mean(1); return float(np.percentile(bm, lo_p)), float(np.percentile(bm, hi_p))
    for k, (a, b) in prim.items():
        dd = H[a] - H[b]; lo, hi = ci(dd, 0.5, 99.5); rep["primary"][k] = dict(mean=float(dd.mean()), sd=float(dd.std(ddof=1)), ci99=[lo, hi], decision=cls(lo, hi), share_pos=float((dd > 0).mean()))
    expl = {"DA25-E": ("DA25", "E"), "DA50-E": ("DA50", "E"), "RHO-E": ("RHO", "E"), "RHO-DA100": ("RHO", "DA100"), "RHO-Dg100": ("RHO", "Dg100"), "MIX-E": ("MIX", "E"), "MIX-Dg100": ("MIX", "Dg100")}
    for k, (a, b) in expl.items(): dd = H[a] - H[b]; lo, hi = ci(dd, 2.5, 97.5); rep["exploratory"][k] = dict(mean=float(dd.mean()), ci95=[lo, hi])
    for k, (a, b) in prim.items(): rep["per_scenario"][k] = {sc: float((src[a][sc] - src[b][sc]).mean()) for sc in SC}
    for k, (a, b) in expl.items(): rep["per_scenario"][k] = {sc: float((src[a][sc] - src[b][sc]).mean()) for sc in SC}
    # concentration (target) diagnostics on SC6: mean over generations 1-150 and runs, and at gens 1/50/100/150
    keys = ("q_max", "q_ent", "m_theta", "m_empty", "dep", "neff", "frac_dup")
    rep["diagnostics"] = {a: {k: {str(g): float(np.mean([r["conds"][a]["dyn"][g][k] for r in res.values() if k in r["conds"][a]["dyn"][g]])) for g in (1, 50, 100, 150)} for k in keys} for a in ARMS}
    meanH = {a: float(np.mean([x[k0] for r in res.values() for x in r["conds"][a]["dyn"] if "q_ent" in x for k0 in ("q_ent",)])) for a in ARMS}; meanQ = {a: float(np.mean([x["q_max"] for r in res.values() for x in r["conds"][a]["dyn"] if "q_ent" in x])) for a in ARMS}
    conf = {}
    for k, (a, b) in {"C1": ("DA25", "Dg25"), "C2": ("DA50", "Dg50"), "C3": ("DA100", "Dg100"), "RHO_vs_DA100": ("RHO", "DA100"), "MIX_vs_DA100": ("MIX", "DA100")}.items():
        ref = a if k in ("C1", "C2", "C3") else "DA100"; oth = b if k in ("C1", "C2", "C3") else a
        gap = abs(meanH[oth] - meanH[ref]) / meanH[ref]; qg = abs(meanQ[oth] - meanQ[ref]); conf[k] = dict(ref=ref, other=oth, entropy_ref=meanH[ref], entropy_other=meanH[oth], rel_entropy_gap=gap, qmax_ref=meanQ[ref], qmax_other=meanQ[oth], abs_qmax_gap=qg, conform=bool(gap <= 0.10 and qg <= 0.05))
    rep["matching_SC6"] = conf
    gens = (1, 25, 50, 100, 150); ek = ("ang_max_raw", "ang_max_norm", "dec_max", "dec_ent", "L1_dec_target", "q_max")
    rep["effective_distribution"] = {a: {k: {str(g): float(np.mean([x[k] for r in res.values() for x in r["conds"][a]["log"] if x["gen"] == g])) for g in gens} for k in ek} for a in ARMS}
    save(rep, out); print(json.dumps(rep, indent=1, default=str))
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "precheck": sys.exit(0 if precheck(sys.argv[2], sys.argv[3]) else 1)
    elif m == "final": final(sys.argv[2], sys.argv[3], sys.argv[4])
