"""P17 pre-registered analysis (Tier 1). python p17_an.py precheck DIR FREEZE | final DIR OUT.json FREEZE  (RUN ONCE, after all runs; HV is read ONLY here)."""
import sys, os, json, glob
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"; sys.path.insert(0, B + "/p6/code"); sys.path.insert(0, B + "/p5")
import numpy as np, p6_stats as S, run_p1m as R0
ARMS = ["E", "DA", "Dp", "Dg", "DA+SEL4", "DA+SELW", "DA+SELR", "Dp+SEL4"]; SC = S.SC; GENS = [1, 25, 50, 100, 150]; DELTA = 0.005; LEVEL = 99.0; NPRIM = 5
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=str); os.replace(tmp, p)
def load_dir(d):
    out = {}
    for f in sorted(glob.glob(d + "/*__*.json")): r = json.load(open(f)); out[f"{r['sc']}|{r['seed']}"] = r
    return out
def precheck(d, freeze):
    bad = []
    if not R0.verify_freeze(freeze): bad.append("freeze")
    res = load_dir(d); seeds = sorted({r["seed"] for r in res.values()})
    if seeds != list(range(11200, 11300)): bad.append(f"seeds {len(seeds)}")
    if len(res) != 600: bad.append(f"{len(res)} shards")
    for k, r in res.items():
        if not r.get("feasible", False): bad.append(f"infeasible {k}"); continue
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
    assert not os.path.exists(out), "RUN ONCE"; assert precheck(d, freeze); res = load_dir(d); seeds = sorted({r["seed"] for r in res.values()}); n = len(seeds)
    H = {a: np.array([np.mean([res[f"{sc}|{s}"]["conds"][a]["hv_oracle"] for sc in SC]) for s in seeds]) for a in ARMS}
    Hsc = {sc: {a: np.array([res[f"{sc}|{s}"]["conds"][a]["hv_oracle"] for s in seeds]) for a in ARMS} for sc in SC}
    rng = S.sub_rng("p17_final", 11990); idx = rng.randint(0, n, size=(20000, n)).astype(np.int32)
    prim = {"P1": H["DA+SEL4"] - H["DA"], "P2": H["DA+SEL4"] - H["DA+SELR"], "P3": (H["DA+SEL4"] - H["DA"]) - (H["Dp+SEL4"] - H["Dp"]), "P4": H["DA"] - H["Dp"], "P5": H["DA"] - H["Dg"]}
    rep = dict(status="PRE-REGISTERED TIER 1 (primary contrasts, Bonferroni 99% for 5 primaries, margin 0.005)", n_seeds=n, hv_oracle_means={a: float(H[a].mean()) for a in ARMS}, primary={}, secondary={}, per_scenario={}, diagnostics={})
    lo_q, hi_q = (100 - LEVEL) / 2, 100 - (100 - LEVEL) / 2
    for k, dd in prim.items():
        bm = dd[idx].mean(1); lo, hi = float(np.percentile(bm, lo_q)), float(np.percentile(bm, hi_q)); rep["primary"][k] = dict(mean=float(dd.mean()), sd=float(dd.std(ddof=1)), ci99=[lo, hi], decision=cls(lo, hi), share_pos=float((dd > 0).mean()))
    sec = {"DA+SELW-DA": H["DA+SELW"] - H["DA"], "DA+SELR-DA": H["DA+SELR"] - H["DA"], "E-DA": H["E"] - H["DA"], "E-Dg": H["E"] - H["Dg"], "E-Dp": H["E"] - H["Dp"], "Dp+SEL4-Dp": H["Dp+SEL4"] - H["Dp"], "DA+SEL4-E": H["DA+SEL4"] - H["E"], "Dg-Dp": H["Dg"] - H["Dp"]}
    for k, dd in sec.items():
        bm = dd[idx].mean(1); rep["secondary"][k] = dict(mean=float(dd.mean()), ci95=[float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))], sd=float(dd.std(ddof=1)))
    for k, (a, b) in {"P1": ("DA+SEL4", "DA"), "P4": ("DA", "Dp"), "P5": ("DA", "Dg"), "P2": ("DA+SEL4", "DA+SELR")}.items(): rep["per_scenario"][k] = {sc: float((Hsc[sc][a] - Hsc[sc][b]).mean()) for sc in SC}
    keys = ("m_theta", "m_theta_E", "m_empty", "dep", "neff", "q_max", "q_ent")
    for a in ARMS:
        rows = [res[f"{sc}|{s}"]["conds"][a]["dyn"] for sc in SC for s in seeds]; rep["diagnostics"][a] = {k: {str(g): (float(np.mean([r[g][k] for r in rows if k in r[g]])) if any(k in r[g] for r in rows) else None) for g in GENS} for k in keys}
    sl = {}
    for a in ("DA+SEL4", "DA+SELW", "DA+SELR", "Dp+SEL4"):
        L = [res[f"{sc}|{s}"]["conds"][a]["sel_log"] for sc in SC for s in seeds]; sl[a] = {k: float(np.mean([np.mean([x[k] for x in l]) for l in L])) for k in ("front4_share", "divergence", "G_sel", "G_all", "S_size")}
        sl[a]["share_runs_front4_mean_gt_0.6"] = float(np.mean([np.mean([x["front4_share"] for x in l]) > 0.6 for l in L]))
    rep["selection_diagnostics"] = sl; save(rep, out); print(json.dumps(rep, indent=1, default=str))
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "precheck": sys.exit(0 if precheck(sys.argv[2], sys.argv[3]) else 1)
    elif m == "final": final(sys.argv[2], sys.argv[3], sys.argv[4])
