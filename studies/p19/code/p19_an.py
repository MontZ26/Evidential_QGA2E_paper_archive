"""P19 pre-registered analysis. python p19_an.py precheck DIR FREEZE | final DIR OUT.json FREEZE (RUN ONCE; HV read only here). Reference arms Dp, Dg, DA, E come from the P17 Tier 1 shards (same seeds, deterministic)."""
import sys, os, json, glob
B = "/tmp/claude-0/-home-claude/98ab71eb-5e16-56eb-b7da-e2e37d41cb81/scratchpad"; sys.path.insert(0, B + "/p6/code"); sys.path.insert(0, B + "/p5")
import numpy as np, p6_stats as S, run_p1m as R0
SC = S.SC; DELTA = 0.005; T1 = B + "/p17/runs/tier1"; NEWA = ["DAg6", "DAgm"]; REF = ["Dp", "Dg", "DA", "E"]
def save(o, p): tmp = p + ".tmp"; json.dump(o, open(tmp, "w"), indent=1, default=str); os.replace(tmp, p)
def load_dir(d): return {f"{r['sc']}|{r['seed']}": r for r in (json.load(open(f)) for f in sorted(glob.glob(d + "/*__*.json")))}
def precheck(d, freeze):
    bad = []
    if not R0.verify_freeze(freeze): bad.append("freeze")
    res = load_dir(d)
    if sorted({r["seed"] for r in res.values()}) != list(range(11200, 11260)) or len(res) != 360: bad.append(f"shape {len(res)}")
    for k, r in res.items():
        for a in NEWA:
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
    t1 = {f"{sc}|{s}": json.load(open(f"{T1}/{sc}__{s}.json")) for sc in SC for s in seeds}
    src = {a: {sc: np.array([(res if a in NEWA else t1)[f"{sc}|{s}"]["conds"][a]["hv_oracle"] for s in seeds]) for sc in SC} for a in NEWA + REF}; H = {a: np.mean([src[a][sc] for sc in SC], axis=0) for a in src}
    idx = S.sub_rng("p19_final", 11993).randint(0, n, size=(20000, n)).astype(np.int32)
    prim = {"C1 DAg6-Dg": H["DAg6"] - H["Dg"], "C2 DAgm-Dg": H["DAgm"] - H["Dg"], "C3 DAg6-DA": H["DAg6"] - H["DA"], "C4 DAgm-DA": H["DAgm"] - H["DA"], "C5 interaction (DAg6-DA)-(Dg-Dp)": (H["DAg6"] - H["DA"]) - (H["Dg"] - H["Dp"])}
    gm = res[next(iter(res))]["gamma_m"]; rep = dict(status="PRE-REGISTERED P19 (5 primaries, 99% CI, margin 0.005)", n_seeds=n, gamma_m=gm, hv_oracle_means={a: float(H[a].mean()) for a in H}, primary={}, secondary={}, per_scenario={})
    for k, dd in prim.items():
        bm = dd[idx].mean(1); lo, hi = float(np.percentile(bm, 0.5)), float(np.percentile(bm, 99.5)); rep["primary"][k] = dict(mean=float(dd.mean()), sd=float(dd.std(ddof=1)), ci99=[lo, hi], decision=cls(lo, hi), share_pos=float((dd > 0).mean()))
    sec = {"DAg6-Dp": H["DAg6"] - H["Dp"], "DAgm-Dp": H["DAgm"] - H["Dp"], "DAg6-E": H["DAg6"] - H["E"], "DAgm-E": H["DAgm"] - H["E"], "interaction_matched (DAgm-DA)-(Dg-Dp)": (H["DAgm"] - H["DA"]) - (H["Dg"] - H["Dp"]), "Dg-DA": H["Dg"] - H["DA"], "Dg-Dp": H["Dg"] - H["Dp"], "DAg6-DAgm": H["DAg6"] - H["DAgm"]}
    for k, dd in sec.items(): bm = dd[idx].mean(1); rep["secondary"][k] = dict(mean=float(dd.mean()), ci95=[float(np.percentile(bm, 2.5)), float(np.percentile(bm, 97.5))])
    for k, (a, b) in {"C1": ("DAg6", "Dg"), "C2": ("DAgm", "Dg"), "C3": ("DAg6", "DA"), "C4": ("DAgm", "DA")}.items(): rep["per_scenario"][k] = {sc: float((src[a][sc] - src[b][sc]).mean()) for sc in SC}
    rep["diagnostics"] = {a: {k: {str(g): float(np.mean([(res if a in NEWA else t1)[f"{sc}|{s}"]["conds"][a]["dyn"][g][k] for sc in SC for s in seeds])) for g in (1, 50, 100, 150)} for k in ("q_max", "q_ent", "m_theta")} for a in NEWA + ["DA", "Dg", "Dp"]}
    save(rep, out); print(json.dumps(rep, indent=1, default=str))
if __name__ == "__main__":
    m = sys.argv[1]
    if m == "precheck": sys.exit(0 if precheck(sys.argv[2], sys.argv[3]) else 1)
    elif m == "final": final(sys.argv[2], sys.argv[3], sys.argv[4])
